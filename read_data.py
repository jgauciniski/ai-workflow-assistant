import json
from llm import ask_llm

with open("processed_tickets.json", "r", encoding="utf-8") as file:
    tickets = json.load(file)

classification_prompt = """
You are an AI assistant for support triage.

Classify the support ticket into one of these priority levels only:
- low
- medium
- high

Return ONLY valid JSON in this format:
{
  "priority": "low"
}

Rules:
- Return only raw JSON
- No markdown
- No explanation
"""

enriched_tickets = []

for index, ticket in enumerate(tickets, start=1):
    print(f"\n--- Ticket {index} ---")
    print("Issue:", ticket["issue"])

    ticket_summary = f"""
Issue: {ticket["issue"]}
Actions taken: {ticket["actions_taken"]}
Requested resolution: {ticket["requested_resolution"]}
"""

    result = ask_llm(
        system_prompt=classification_prompt,
        user_prompt=ticket_summary
    )

    parsed_result = json.loads(result)

    enriched_ticket = {
        "issue": ticket["issue"],
        "actions_taken": ticket["actions_taken"],
        "requested_resolution": ticket["requested_resolution"],
        "priority": parsed_result["priority"]
    }

    enriched_tickets.append(enriched_ticket)

    print("Priority:", enriched_ticket["priority"])

with open("enriched_tickets.json", "w", encoding="utf-8") as file:
    json.dump(enriched_tickets, file, indent=2)

print("\nSaved results to enriched_tickets.json")