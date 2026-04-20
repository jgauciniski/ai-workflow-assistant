from app.workflows import process_ticket, answer_question, select_tool
from app.session import Session
from app.utils.formatters import format_ticket_for_display

def handle_simple_queries(session: Session, user_input: str) -> tuple[object, list] | None:
    text = user_input.lower()

    if "how many tickets" in text:
        return f"You have {len(session.tickets)} tickets.", []

    if "list tickets" in text:
        return session.tickets, session.tickets

    return None

def handle_user_input(session: Session, user_input: str) -> tuple[object, list]:
    simple_result = handle_simple_queries(session, user_input)

    if simple_result:
        return simple_result

    tool = select_tool(user_input)

    if tool == "answer_question":
        return handle_question(session, user_input)

    return handle_ticket(session, user_input), []


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

