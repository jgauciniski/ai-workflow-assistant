import json

from app.services import handle_ticket, handle_question
from app.session import Session, save_session, load_session
from app.commands import handle_command


def format_ticket_for_display(ticket: dict) -> dict:
    return {
        "issue": ticket.get("issue", ""),
        "actions_taken": ticket.get("actions_taken", ""),
        "requested_resolution": ticket.get("requested_resolution", ""),
        "priority": ticket.get("priority", ""),
    }


print("AI Workflow Assistant")
print("Type a support ticket OR ask a question (type 'exit' to quit)\n")

try:
    session = load_session()

    if session.tickets or session.qa_history:
        print(
            f"Loaded previous session with {len(session.tickets)} ticket(s) "
            f"and {len(session.qa_history)} Q&A item(s)."
        )
    else:
        print("No previous session found. Starting fresh.")

except RuntimeError as error:
    print(f"Warning: {error}")
    print("Starting with a fresh session instead.\n")
    session = Session()

while True:
    user_input = input("Enter input: ").strip()

    if user_input.lower() == "exit":
        break

    handled = handle_command(user_input, session)

    if handled:
        continue

    try:
        if user_input.lower().startswith("question:"):
            question = user_input[len("question:"):].strip()
            answer, relevant_tickets = handle_question(session, question)

            display_tickets = [
                format_ticket_for_display(ticket)
                for ticket in relevant_tickets
            ]

            print(f"\nRetrieved {len(display_tickets)} ticket(s):")
            print(json.dumps(display_tickets, indent=2))

            print("\nAnswer:")
            print(answer)

            print("\n----------------------\n")
            continue

        enriched_ticket = handle_ticket(session, user_input)

        print("\nEnriched Output:")
        print(json.dumps(format_ticket_for_display(enriched_ticket), indent=2))

    except Exception as error:
        print("Error:", error)

    print("\n----------------------\n")

try:
    save_session(session)
except RuntimeError as error:
    print(f"Warning: {error}")
    print("Exiting without saving the latest session changes.")

print("Goodbye.")