import json

from app.session import Session
from app.commands.core import get_command_data


def handle_command(user_input: str, session: Session) -> bool:
    result = get_command_data(user_input, session)

    if result is None:
        return False

    command = result["command"]

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
        for example in result["examples"]:
            print(example)

        print("\n----------------------\n")
        return True

    if command == "save":
        print(result["message"])
        print("\n----------------------\n")
        return True

    if command == "load":
        print(result["message"])
        print("\n----------------------\n")
        return True

    if command == "clear":
        print(result["message"])
        print(result["note"])
        print("\n----------------------\n")
        return True

    if command == "delete last":
        print(result["message"])
        if result["removed_ticket"]:
            print(json.dumps(result["removed_ticket"], indent=2))
        print("\n----------------------\n")
        return True

    if command == "delete last question":
        print(result["message"])
        if result["removed_question"]:
            print(json.dumps(result["removed_question"], indent=2))
        print("\n----------------------\n")
        return True

    if command == "list questions":
        if result["message"]:
            print(result["message"])
        else:
            print("\nQ&A History:\n")
            for index, item in enumerate(result["items"], start=1):
                print(f"--- Q&A {index} ---")
                print("Question:", item["question"])
                print("Answer:", item["answer"])
                print()

        print("\n----------------------\n")
        return True

    if command == "list":
        if result["message"]:
            print(result["message"])
        else:
            print("\nCurrent tickets:\n")
            for index, ticket in enumerate(result["items"], start=1):
                print(f"--- Ticket {index} ---")
                print("Issue:", ticket["issue"])
                print("Actions taken:", ticket["actions_taken"])
                print("Requested resolution:", ticket["requested_resolution"])
                print("Priority:", ticket["priority"])
                if ticket.get("summary"):
                    print("Summary:", ticket["summary"])
                print()

        print("\n----------------------\n")
        return True

    if command == "stats":
        print("\nSession Stats")
        print(f"Total tickets: {result['total_tickets']}")
        print(f"Total questions: {result['total_questions']}")
        print(f"High priority tickets: {result['high_priority_tickets']}")
        print(f"Medium priority tickets: {result['medium_priority_tickets']}")
        print(f"Low priority tickets: {result['low_priority_tickets']}")
        print("\n----------------------\n")
        return True

    if command == "summary":
        print("\nSession Summary")
        print(f"Total tickets: {result['total_tickets']}")
        print(f"High priority tickets: {result['high_priority_tickets']}")
        print(f"Questions asked: {result['questions_asked']}")

        if result["issues_seen_so_far"]:
            print("\nIssues seen so far:")
            for index, issue in enumerate(result["issues_seen_so_far"], start=1):
                print(f"{index}. {issue}")

        print("\n----------------------\n")
        return True

    return False