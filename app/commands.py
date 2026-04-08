import json

from app.session import Session, save_session, load_session


def handle_command(user_input: str, session: Session) -> bool:
    command = user_input.lower()

    if command == "help":
        print("\nAvailable commands:")
        print("- Type a support ticket to process it")
        print("- Type 'question: ...' to ask about saved tickets")
        print("- Type 'summary' to see the current session overview")
        print("- Type 'list' to see all current tickets")
        print("- Type 'list questions' to see all saved questions and answers")
        print("- Type 'stats' to see ticket and question statistics")
        print("- Type 'save' to save tickets and Q&A history")
        print("- Type 'load' to load previously saved tickets and Q&A history")
        print("- Type 'clear' to reset the current in-memory session")
        print("- Type 'delete last' to remove the most recently added ticket")
        print("- Type 'delete last question' to remove the most recent Q&A entry")
        print("- Type 'exit' to quit")

        print("\nExamples:")
        print("My order says delivered but I didn’t receive it.")
        print("question: how many high priority tickets are there?")
        print("summary")
        print("list")
        print("list questions")
        print("stats")
        print("save")
        print("load")
        print("clear")
        print("delete last")
        print("delete last question")
        print("exit")

        print("\n----------------------\n")
        return True

    if command == "save":
        try:
            save_session(session)
            print("Session saved.")
        except RuntimeError as error:
            print(f"Warning: {error}")

        print("\n----------------------\n")
        return True

    if command == "load":
        loaded_session = load_session()
        session.tickets = loaded_session.tickets
        session.qa_history = loaded_session.qa_history
        print(f"Loaded {len(session.tickets)} ticket(s) and {len(session.qa_history)} Q&A item(s).")
        print("\n----------------------\n")
        return True

    if command == "clear":
        session.tickets = []
        session.qa_history = []
        print("Session cleared from memory.")
        print("Type 'save' if you also want to overwrite the saved files.")
        print("\n----------------------\n")
        return True

    if command == "delete last":
        if not session.tickets:
            print("No tickets to delete.")
        else:
            removed_ticket = session.tickets.pop()
            print("Removed last ticket:")
            print(json.dumps(removed_ticket, indent=2))

        print("\n----------------------\n")
        return True

    if command == "delete last question":
        if not session.qa_history:
            print("No questions to delete.")
        else:
            removed_question = session.qa_history.pop()
            print("Removed last Q&A entry:")
            print(json.dumps(removed_question, indent=2))

        print("\n----------------------\n")
        return True

    if command == "list questions":
        if not session.qa_history:
            print("No questions in the current session.")
        else:
            print("\nQ&A History:\n")

            for index, item in enumerate(session.qa_history, start=1):
                print(f"--- Q&A {index} ---")
                print("Question:", item["question"])
                print("Answer:", item["answer"])
                print()

        print("\n----------------------\n")
        return True

    if command == "list":
        if not session.tickets:
            print("No tickets in the current session.")
        else:
            print("\nCurrent tickets:\n")

            for index, ticket in enumerate(session.tickets, start=1):
                print(f"--- Ticket {index} ---")
                print("Issue:", ticket["issue"])
                print("Actions taken:", ticket["actions_taken"])
                print("Requested resolution:", ticket["requested_resolution"])
                print("Priority:", ticket["priority"])
                print()

        print("\n----------------------\n")
        return True

    if command == "stats":
        total_tickets = len(session.tickets)
        total_questions = len(session.qa_history)

        high_priority = len([t for t in session.tickets if t["priority"] == "high"])
        medium_priority = len([t for t in session.tickets if t["priority"] == "medium"])
        low_priority = len([t for t in session.tickets if t["priority"] == "low"])

        print("\nSession Stats")
        print(f"Total tickets: {total_tickets}")
        print(f"Total questions: {total_questions}")
        print(f"High priority tickets: {high_priority}")
        print(f"Medium priority tickets: {medium_priority}")
        print(f"Low priority tickets: {low_priority}")

        print("\n----------------------\n")
        return True

    if command == "summary":
        high_priority = [t for t in session.tickets if t["priority"] == "high"]

        print("\nSession Summary")
        print(f"Total tickets: {len(session.tickets)}")
        print(f"High priority tickets: {len(high_priority)}")
        print(f"Questions asked: {len(session.qa_history)}")

        if session.tickets:
            print("\nIssues seen so far:")
            for index, ticket in enumerate(session.tickets, start=1):
                print(f"{index}. {ticket['issue']}")

        print("\n----------------------\n")
        return True

    return False