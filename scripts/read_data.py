import json
from pathlib import Path

input_path = Path(__file__).resolve().parent.parent / "data" / "processed_tickets.json"

with open(input_path, "r", encoding="utf-8") as file:
    tickets = json.load(file)

print("\nLoaded processed tickets:\n")

for index, ticket in enumerate(tickets, start=1):
    print(f"--- Ticket {index} ---")
    print("Issue:", ticket["issue"])
    print("Actions taken:", ticket["actions_taken"])
    print("Requested resolution:", ticket["requested_resolution"])
    print("Priority:", ticket["priority"])
    print()

total_tickets = len(tickets)
high_priority_count = len([ticket for ticket in tickets if ticket["priority"] == "high"])

print("Summary:")
print(f"Total tickets: {total_tickets}")
print(f"High priority tickets: {high_priority_count}")