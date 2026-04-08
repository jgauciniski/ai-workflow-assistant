from app.workflows import process_ticket, answer_question
from app.session import Session


def handle_ticket(session: Session, user_input: str) -> dict:
    enriched_ticket = process_ticket(user_input)
    session.tickets.append(enriched_ticket)
    return enriched_ticket


def handle_question(session: Session, question: str) -> tuple[str, list]:
    answer, relevant_tickets = answer_question(session.tickets, question)

    qa_entry = {
        "question": question,
        "retrieved_tickets": relevant_tickets,
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