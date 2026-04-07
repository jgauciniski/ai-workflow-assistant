import json

from app.llm import ask_llm
from app.prompts import (
    EXTRACTION_PROMPT,
    CLASSIFICATION_PROMPT,
    QUESTION_ANSWER_PROMPT,
)


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
    cleaned_question = question.lower().replace("?", "").replace(":", "").replace(",", "")
    keywords = [
        word for word in cleaned_question.split()
        if word not in {"which", "what", "are", "is", "the", "about", "tickets", "ticket"}
    ]

    relevant = []

    for ticket in saved_tickets:
        text = (
            ticket["issue"] +
            ticket["actions_taken"] +
            ticket["requested_resolution"]
        ).lower()

        if any(word in text for word in keywords):
            relevant.append(ticket)

    
    print(f"Keywords used: {keywords}")
    print(f"Found {len(relevant)} relevant tickets based on keywords.")

    # fallback: if nothing matches, return all
    return relevant if relevant else saved_tickets