from app.workflows import process_ticket, answer_question, classify_intent,select_tool
from app.session import Session

def handle_user_input(session: Session, user_input: str) -> tuple[str, list]:
    #I started with intent classification, then evolved the system to tool-based routing for better extensibility.
    """intent = classify_intent(user_input)

    if intent == "question":
        return handle_question(session, user_input)

    return handle_ticket(session, user_input), []"""

    tool = select_tool(user_input)

    if tool == "answer_question":
        return handle_question(session, user_input)

    return handle_ticket(session, user_input), []

def format_ticket_for_display(ticket: dict) -> dict:
    return {
        "issue": ticket.get("issue", ""),
        "actions_taken": ticket.get("actions_taken", ""),
        "requested_resolution": ticket.get("requested_resolution", ""),
        "priority": ticket.get("priority", ""),
    }


def handle_ticket(session: Session, user_input: str) -> dict:
    enriched_ticket = process_ticket(user_input)
    session.tickets.append(enriched_ticket)
    return enriched_ticket


def handle_question(session: Session, question: str) -> tuple[str, list]:
    answer, relevant_tickets = answer_question(session.tickets, question)

    qa_entry = {
        "question": question,
        "retrieved_tickets": [
            format_ticket_for_display(ticket)
            for ticket in relevant_tickets
        ],
        "answer": answer
    }

    session.qa_history.append(qa_entry)

    return answer, relevant_tickets


def handle_batch_tickets(session: Session, tickets: list[str]) -> list[dict]:
    processed = []

    for ticket in tickets:
        enriched_ticket = handle_ticket(session, ticket)
        processed.append(enriched_ticket)

    return processed