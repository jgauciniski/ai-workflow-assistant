from app.session import Session, save_session, load_session
from app.utils.formatters import format_ticket_for_display


def get_help_data() -> dict:
    return {
        "command": "help",
        "available_commands": [
            "help",
            "summary",
            "list",
            "list questions",
            "stats",
            "save",
            "load",
            "clear",
            "delete last",
            "delete last question",
            "exit",
        ],
        "examples": [
            "My order says delivered but I didn’t receive it.",
            "question: how many high priority tickets are there?",
            "summary",
            "list",
            "list questions",
            "stats",
            "save",
            "load",
            "clear",
            "delete last",
            "delete last question",
            "exit",
        ],
    }


def get_list_data(session: Session) -> dict:
    tickets = [
        format_ticket_for_display(ticket)
        for ticket in session.tickets
    ]

    return {
        "command": "list",
        "count": len(tickets),
        "items": tickets,
        "message": "No tickets in the current session." if not tickets else None,
    }


def get_list_questions_data(session: Session) -> dict:
    return {
        "command": "list questions",
        "count": len(session.qa_history),
        "items": session.qa_history,
        "message": "No questions in the current session." if not session.qa_history else None,
    }


def get_stats_data(session: Session) -> dict:
    total_tickets = len(session.tickets)
    total_questions = len(session.qa_history)

    high_priority = len([t for t in session.tickets if t["priority"] == "high"])
    medium_priority = len([t for t in session.tickets if t["priority"] == "medium"])
    low_priority = len([t for t in session.tickets if t["priority"] == "low"])

    return {
        "command": "stats",
        "total_tickets": total_tickets,
        "total_questions": total_questions,
        "high_priority_tickets": high_priority,
        "medium_priority_tickets": medium_priority,
        "low_priority_tickets": low_priority,
    }


def get_summary_data(session: Session) -> dict:
    high_priority = [t for t in session.tickets if t["priority"] == "high"]

    return {
        "command": "summary",
        "total_tickets": len(session.tickets),
        "high_priority_tickets": len(high_priority),
        "questions_asked": len(session.qa_history),
        "issues_seen_so_far": [ticket["issue"] for ticket in session.tickets],
    }


def save_session_data(session: Session) -> dict:
    save_session(session)
    return {
        "command": "save",
        "message": "Session saved.",
    }


def load_session_data(session: Session) -> dict:
    loaded_session = load_session()
    session.tickets = loaded_session.tickets
    session.qa_history = loaded_session.qa_history

    return {
        "command": "load",
        "message": f"Loaded {len(session.tickets)} ticket(s) and {len(session.qa_history)} Q&A item(s).",
        "ticket_count": len(session.tickets),
        "qa_count": len(session.qa_history),
    }


def clear_session_data(session: Session) -> dict:
    session.tickets = []
    session.qa_history = []

    return {
        "command": "clear",
        "message": "Session cleared from memory.",
        "note": "Type 'save' if you also want to overwrite the saved files.",
    }


def delete_last_ticket(session: Session) -> dict:
    if not session.tickets:
        return {
            "command": "delete last",
            "message": "No tickets to delete.",
            "removed_ticket": None,
        }

    removed_ticket = session.tickets.pop()

    return {
        "command": "delete last",
        "message": "Removed last ticket.",
        "removed_ticket": format_ticket_for_display(removed_ticket),
    }


def delete_last_question(session: Session) -> dict:
    if not session.qa_history:
        return {
            "command": "delete last question",
            "message": "No questions to delete.",
            "removed_question": None,
        }

    removed_question = session.qa_history.pop()

    return {
        "command": "delete last question",
        "message": "Removed last Q&A entry.",
        "removed_question": removed_question,
    }


def get_command_data(command: str, session: Session) -> dict | None:
    command = command.strip().lower()

    if command == "help":
        return get_help_data()

    if command == "save":
        return save_session_data(session)

    if command == "load":
        return load_session_data(session)

    if command == "clear":
        return clear_session_data(session)

    if command == "delete last":
        return delete_last_ticket(session)

    if command == "delete last question":
        return delete_last_question(session)

    if command == "list questions":
        return get_list_questions_data(session)

    if command == "list":
        return get_list_data(session)

    if command == "stats":
        return get_stats_data(session)

    if command == "summary":
        return get_summary_data(session)

    return None