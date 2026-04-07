import json
from pathlib import Path

from app.workflows import process_ticket, answer_question
from app.session import save_session, load_session
from app.commands import handle_command

print("AI Workflow Assistant")
print("Type a support ticket OR ask a question (type 'exit' to quit)\n")

saved_tickets, qa_history = load_session()

if saved_tickets or qa_history:
    print(f"Loaded previous session with {len(saved_tickets)} ticket(s) and {len(qa_history)} Q&A item(s).")
else:
    print("No previous session found. Starting fresh.")


while True:
    user_input = input("Enter input: ").strip()

    if user_input.lower() == "exit":
        break
    handled, saved_tickets, qa_history = handle_command(
        user_input, saved_tickets, qa_history
    )

    if handled:
        continue
    
    try:
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
            print("\n----------------------\n")
            continue

        else:
            enriched_ticket = process_ticket(user_input)
            saved_tickets.append(enriched_ticket)

            print("\nEnriched Output:")
            print(json.dumps(enriched_ticket, indent=2))

    except Exception as error:
        print("Error:", error)

    print("\n----------------------\n")

save_session(saved_tickets, qa_history)
print("Goodbye.")