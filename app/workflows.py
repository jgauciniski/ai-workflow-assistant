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

def build_ticket_text(ticket: dict) -> str:
    return f"""
Issue: {ticket.get("issue", "")}
Actions taken: {ticket.get("actions_taken", "")}
Requested resolution: {ticket.get("requested_resolution", "")}
Priority: {ticket.get("priority", "")}
""".strip()

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

    enriched_ticket["embedding"] = embedding_service.embed_text(
        build_ticket_text(enriched_ticket)
    )

    return enriched_ticket


def answer_question(saved_tickets: list, question: str) -> tuple[str, list]:
    relevant_tickets = select_relevant_tickets(saved_tickets, question)
    context = json.dumps(relevant_tickets, indent=2)

    user_prompt = f"""
Data:
{context}

Question:
{question}
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
    )

    print("\n--- Semantic Retrieval Debug ---")
    for i, item in enumerate(top_results, start=1):
        print(
            f"{i}. Score={item['score']:.4f} | "
            f"Issue={item['ticket'].get('issue', '')}"
        )

    relevant_tickets = [item["ticket"] for item in top_results]
    return relevant_tickets