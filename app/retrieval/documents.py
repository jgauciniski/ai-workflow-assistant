# Separate retrieval representation from raw ticket storage.
# This keeps embedding logic independent from the data model.
def build_retrieval_document(ticket: dict) -> str:
    return f"""
Issue: {ticket.get("issue", "")}
Actions taken: {ticket.get("actions_taken", "")}
Requested resolution: {ticket.get("requested_resolution", "")}
Priority: {ticket.get("priority", "")}
""".strip()