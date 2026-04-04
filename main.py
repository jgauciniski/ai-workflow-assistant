import json
from llm import ask_llm

tickets = [
    """
    Customer says their order was marked as delivered, but they never received it.
    They already checked with neighbors and the building front desk.
    They want either a replacement or a refund as soon as possible.
    """,
    """
    The employee cannot log into the internal HR portal.
    They already reset the password twice and tried another browser.
    They need access today because they must download tax documents.
    """,
    """
    A user reports that the mobile app crashes during checkout.
    They tried uninstalling and reinstalling the app.
    They want to complete the purchase before tonight’s promotion ends.
    """,
    """
    A user didn't like the color of the system buttons and wants to change it.
    They haven't tried any troubleshooting steps yet.
    """
]

system_prompt = """
You are an AI assistant for support operations.

Extract the information and return ONLY valid JSON in this format:

{
  "issue": "...",
  "actions_taken": "...",
  "requested_resolution": "..."
}

Do not include any extra text. Only JSON.
"""

processed_tickets = []

for index, ticket in enumerate(tickets, start=1):
    print(f"\n--- Ticket {index} ---")

    try:
        result = ask_llm(system_prompt=system_prompt, user_prompt=ticket)
        parsed_result = json.loads(result)

        processed_tickets.append(parsed_result)

        print("Issue:", parsed_result["issue"])
        print("Actions taken:", parsed_result["actions_taken"])
        print("Requested resolution:", parsed_result["requested_resolution"])

    except json.JSONDecodeError:
        print("ERROR: Model did not return valid JSON.")
        print("Raw output was:")
        print(result)

    except Exception as error:
        print("ERROR: Something unexpected happened.")
        print(error)

print("\n=== Final processed tickets list ===")
print(processed_tickets)

with open("processed_tickets.json", "w", encoding="utf-8") as file:
    json.dump(processed_tickets, file, indent=2)

print("\nSaved results to processed_tickets.json")