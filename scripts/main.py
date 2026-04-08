import json
from pathlib import Path

from app.services import handle_batch_tickets
from app.session import Session

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


session = Session()
processed_tickets = handle_batch_tickets(session, tickets)

for index, ticket in enumerate(processed_tickets, start=1):
    print(f"\n--- Ticket {index} ---")
    print("Issue:", ticket["issue"])
    print("Actions taken:", ticket["actions_taken"])
    print("Requested resolution:", ticket["requested_resolution"])
    print("Priority:", ticket["priority"])

print("\n=== Final processed tickets list ===")
print(processed_tickets)

output_path = Path(__file__).resolve().parent.parent / "data" / "processed_tickets.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(processed_tickets, file, indent=2)

print("\nSaved results to processed_tickets.json")