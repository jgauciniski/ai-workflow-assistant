import json
from pathlib import Path

from app.workflows import process_ticket, answer_question

print("AI Workflow Assistant")
print("Type a support ticket OR ask a question (type 'exit' to quit)\n")

def save_session(saved_tickets: list, qa_history: list) -> None:
    tickets_output_path = Path(__file__).resolve().parent.parent / "data" / "cli_tickets.json"
    qa_output_path = Path(__file__).resolve().parent.parent / "data" / "qa_history.json"

    with open(tickets_output_path, "w", encoding="utf-8") as file:
        json.dump(saved_tickets, file, indent=2)

    print("Saved results to cli_tickets.json")

    with open(qa_output_path, "w", encoding="utf-8") as file:
        json.dump(qa_history, file, indent=2)
    
    print("Saved Q&A history to qa_history.json")

    print("Session saved.")

def load_session() -> tuple[list, list]:
    tickets_output_path = Path(__file__).resolve().parent.parent / "data" / "cli_tickets.json"
    qa_output_path = Path(__file__).resolve().parent.parent / "data" / "qa_history.json"

    saved_tickets = []
    qa_history = []

    if tickets_output_path.exists():
        with open(tickets_output_path, "r", encoding="utf-8") as file:
            saved_tickets = json.load(file)

    if qa_output_path.exists():
        with open(qa_output_path, "r", encoding="utf-8") as file:
            qa_history = json.load(file)

    return saved_tickets, qa_history

saved_tickets, qa_history = load_session()

if saved_tickets or qa_history:
    print(f"Loaded previous session with {len(saved_tickets)} ticket(s) and {len(qa_history)} Q&A item(s).")
else:
    print("No previous session found. Starting fresh.")

while True:
    user_input = input("Enter input: ").strip()

    try:
        if user_input.lower() == "save":
            save_session(saved_tickets, qa_history)
            print("\n----------------------\n")
            continue
        if user_input.lower() == "load":
            saved_tickets, qa_history = load_session()
            print(f"Loaded {len(saved_tickets)} ticket(s) and {len(qa_history)} Q&A item(s).")
            print("\n----------------------\n")
            continue
        if user_input.lower() == "list":
            if not saved_tickets:
                print("No tickets in the current session.")
            else:
                print("\nCurrent tickets:\n")

                for index, ticket in enumerate(saved_tickets, start=1):
                    print(f"--- Ticket {index} ---")
                    print("Issue:", ticket["issue"])
                    print("Actions taken:", ticket["actions_taken"])
                    print("Requested resolution:", ticket["requested_resolution"])
                    print("Priority:", ticket["priority"])
                    print()

            print("\n----------------------\n")
            continue
        if user_input.lower() == "list questions":
            if not qa_history:
                print("No questions in the current session.")
            else:
                print("\nQ&A History:\n")

                for index, item in enumerate(qa_history, start=1):
                    print(f"--- Q&A {index} ---")
                    print("Question:", item["question"])
                    print("Answer:", item["answer"])
                    print()

            print("\n----------------------\n")
            continue
        if user_input.lower() == "delete last":
            if not saved_tickets:
                print("No tickets to delete.")
            else:
                removed_ticket = saved_tickets.pop()
                print("Removed last ticket:")
                print(json.dumps(removed_ticket, indent=2))

            print("\n----------------------\n")
            continue
        if user_input.lower() == "delete last question":
            if not qa_history:
                print("No questions to delete.")
            else:
                removed_question = qa_history.pop()
                print("Removed last Q&A entry:")
                print(json.dumps(removed_question, indent=2))

            print("\n----------------------\n")
            continue
        if user_input.lower() == "clear":
            saved_tickets = []
            qa_history = []

            print("Session cleared from memory.")
            print("Type 'save' if you also want to overwrite the saved files.")
            print("\n----------------------\n")
            continue
        if user_input.lower() == "exit":
            break
        if user_input.lower() == "help":
            print("\nAvailable commands:")
            print("- Type a support ticket to process it")
            print("- Type 'question: ...' to ask about saved tickets")
            print("- Type 'summary' to see the current session overview")
            print("- Type 'stats' to see ticket and question statistics")
            print("- Type 'help' to see this message")
            print("- Type 'save' to save tickets and Q&A history")
            print("- Type 'load' to load previously saved tickets and Q&A history")
            print("- Type 'list' to see all current tickets")
            print("- Type 'list questions' to see all saved questions and answers")
            print("- Type 'delete last' to remove the most recently added ticket")
            print("- Type 'delete last question' to remove the most recent Q&A entry")
            print("- Type 'clear' to reset the current in-memory session")
            print("- Type 'exit' to quit")

            print("\nExamples:")
            print("My order says delivered but I didn’t receive it.")
            print("question: how many high priority tickets are there?")
            print("summary")
            print("stats")
            print("save")
            print("load")
            print("list")
            print("list questions")
            print("delete last")
            print("delete last question")
            print("clear")
            print("exit")

            print("\n----------------------\n")
            continue
        if user_input.lower() == "stats":
            total_tickets = len(saved_tickets)
            total_questions = len(qa_history)

            high_priority = len([t for t in saved_tickets if t["priority"] == "high"])
            medium_priority = len([t for t in saved_tickets if t["priority"] == "medium"])
            low_priority = len([t for t in saved_tickets if t["priority"] == "low"])

            print("\nSession Stats")
            print(f"Total tickets: {total_tickets}")
            print(f"Total questions: {total_questions}")
            print(f"High priority tickets: {high_priority}")
            print(f"Medium priority tickets: {medium_priority}")
            print(f"Low priority tickets: {low_priority}")

            print("\n----------------------\n")
            continue
        if user_input.lower() == "summary":
            high_priority = [t for t in saved_tickets if t["priority"] == "high"]

            print("\nSession Summary")
            print(f"Total tickets: {len(saved_tickets)}")
            print(f"High priority tickets: {len(high_priority)}")
            print(f"Questions asked: {len(qa_history)}")

            if saved_tickets:
                print("\nIssues seen so far:")
                for index, ticket in enumerate(saved_tickets, start=1):
                    print(f"{index}. {ticket['issue']}")

            print("\n----------------------\n")
            continue
        if user_input.lower().startswith("question:"):
            question = user_input[len("question:"):].strip()
            answer, relevant_tickets = answer_question(saved_tickets, question)

            print(f"\nRetrieved {len(relevant_tickets)} ticket(s):")
            print(json.dumps(relevant_tickets, indent=2))

            print("\nAnswer:")
            print(answer)

            qa_entry = {
                "question": question,
                "retrieved_tickets": relevant_tickets,
                "answer": answer
            }

            qa_history.append(qa_entry)

        else:
            enriched_ticket = process_ticket(user_input)
            saved_tickets.append(enriched_ticket)

            print("\nEnriched Output:")
            print(json.dumps(enriched_ticket, indent=2))

        print("\nSession summary:")
        print(f"Total tickets: {len(saved_tickets)}")

        high_priority = [t for t in saved_tickets if t["priority"] == "high"]
        print(f"High priority tickets so far: {len(high_priority)}")

    except Exception as error:
        print("Error:", error)

    print("\n----------------------\n")

save_session(saved_tickets, qa_history)
print("Goodbye.")