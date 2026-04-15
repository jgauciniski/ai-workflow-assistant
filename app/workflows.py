import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.llm import ask_llm
from app.prompts import (
    EXTRACTION_PROMPT,
    CLASSIFICATION_PROMPT,
    QUESTION_ANSWER_PROMPT,
)
from app.retrieval import EmbeddingService, Retriever
from app.retrieval.documents import build_retrieval_document

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
    extraction_result = ask_llm(
        system_prompt=EXTRACTION_PROMPT,
        user_prompt=ticket_text
    )
    parsed_ticket = json.loads(extraction_result)

    ticket_summary = f"""
Issue: {parsed_ticket["issue"]}
Actions taken: {parsed_ticket["actions_taken"]}
Requested resolution: {parsed_ticket["requested_resolution"]}
"""

    classification_result = ask_llm(
        system_prompt=CLASSIFICATION_PROMPT,
        user_prompt=ticket_summary
    )
    parsed_priority = json.loads(classification_result)

    enriched_ticket = {
        "issue": parsed_ticket["issue"],
        "actions_taken": parsed_ticket["actions_taken"],
        "requested_resolution": parsed_ticket["requested_resolution"],
        "priority": parsed_priority["priority"]
    }

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)
    embedding_service = EmbeddingService(client)
    # Add embedding to the enriched ticket for future retrieval
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

    answer = ask_llm(
        system_prompt=QUESTION_ANSWER_PROMPT,
        user_prompt=user_prompt
    )

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