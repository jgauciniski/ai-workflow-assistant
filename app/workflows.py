import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.llm import ask_llm
from app.prompts import (
    EXTRACTION_PROMPT,
    CLASSIFICATION_PROMPT,
    QUESTION_ANSWER_PROMPT,
    INTENT_CLASSIFICATION_PROMPT,
    TICKET_SUMMARY_PROMPT,
    TOOL_SELECTION_PROMPT
)
from app.retrieval import EmbeddingService, Retriever
from app.retrieval.documents import build_retrieval_document
from app.utils.json_utils import safe_json_loads
from app.utils.retry import retry
from app.utils.validators import validate_priority, validate_ticket
from app.models.ticket import Ticket

#not being used right now, but keeping the intent classification code in case I want to pivot back to that approach. The tool selection is more flexible for now and doesn't require a strict intent schema.
def classify_intent(user_input: str) -> str:
    response = retry(lambda: ask_llm(
        system_prompt=INTENT_CLASSIFICATION_PROMPT,
        user_prompt=user_input
    ), label="Intent Classification")

    parsed = safe_json_loads(response)
    return parsed.get("intent", "ticket")

def select_tool(user_input: str) -> str:
    response =  retry(lambda: ask_llm(
        system_prompt=TOOL_SELECTION_PROMPT,
        user_prompt=user_input
    ), label="Tool Selection")

    parsed = safe_json_loads(response)
    return parsed.get("tool", "process_ticket")

# Format a list of tickets into a string suitable for LLM input
def format_tickets_for_llm(tickets: list[dict]) -> str:
    formatted = []

    for i, ticket in enumerate(tickets, start=1):
        entry = f"""
Ticket #{i}
Issue: {ticket.get("issue", "")}
Actions taken: {ticket.get("actions_taken", "")}
Requested resolution: {ticket.get("requested_resolution", "")}
Priority: {ticket.get("priority", "")}
"""
        
        formatted.append(entry.strip())

    return "\n\n".join(formatted)

def process_ticket(ticket_text: str) -> dict:
    extraction_result = retry(lambda: ask_llm(
        system_prompt=EXTRACTION_PROMPT,
        user_prompt=ticket_text
    ), label="Ticket Extraction")

    parsed_ticket = validate_ticket(
        safe_json_loads(extraction_result)
    )

    ticket_summary = f"""
Issue: {parsed_ticket["issue"]}
Actions taken: {parsed_ticket["actions_taken"]}
Requested resolution: {parsed_ticket["requested_resolution"]}
"""

    classification_result = retry(lambda: ask_llm(
        system_prompt=CLASSIFICATION_PROMPT,
        user_prompt=ticket_summary
    ), label="Priority Classification")
    parsed_priority = validate_priority(
        safe_json_loads(classification_result)
    )

    ticket_obj = Ticket(
        issue=parsed_ticket["issue"],
        actions_taken=parsed_ticket["actions_taken"],
        requested_resolution=parsed_ticket["requested_resolution"],
        priority=parsed_priority["priority"],
    )

    summary_input = f"""
Issue: {ticket_obj.issue}
Priority: {ticket_obj.priority}
"""

    summary = retry(lambda: ask_llm(
        system_prompt=TICKET_SUMMARY_PROMPT,
        user_prompt=summary_input
    ), label="Ticket Summary")

    ticket_obj.summary = summary.strip()

    enriched_ticket = ticket_obj.to_dict()

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)
    embedding_service = EmbeddingService(client)

    enriched_ticket["embedding"] = embedding_service.embed_text(
        build_retrieval_document(enriched_ticket)
    )

    return enriched_ticket


def answer_question(saved_tickets: list, question: str) -> tuple[str, list]:
    relevant_tickets = select_relevant_tickets(saved_tickets, question)
    formatted_context = format_tickets_for_llm(relevant_tickets)

    user_prompt = f"""
You are an assistant helping analyze support tickets.

Here are the most relevant tickets:

{formatted_context}

Question:
{question}

Answer clearly and based only on the provided tickets.
"""

    answer =  retry(lambda: ask_llm(
        system_prompt=QUESTION_ANSWER_PROMPT,
        user_prompt=user_prompt
    ), label="Question Answering")

    return answer, relevant_tickets

def select_relevant_tickets(saved_tickets: list, question: str) -> list:
    if not saved_tickets:
        return []

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)
    embedding_service = EmbeddingService(client)
    retriever = Retriever()

    query_embedding = embedding_service.embed_text(question)

    top_results = retriever.find_most_similar(
        query_embedding=query_embedding,
        tickets=saved_tickets,
        top_k=3,
        min_score=0.25,
    )

    print("\n--- Semantic Retrieval Debug ---")
    for i, item in enumerate(top_results, start=1):
        print(
            f"{i}. Score={item['score']:.4f} | "
            f"Issue={item['ticket'].get('issue', '')}"
        )

    relevant_tickets = [item["ticket"] for item in top_results]
    return relevant_tickets