def format_ticket_for_display(ticket) -> dict:
    if hasattr(ticket, "to_dict"):
        ticket = ticket.to_dict()

    return {
        "issue": ticket.get("issue", ""),
        "actions_taken": ticket.get("actions_taken", ""),
        "requested_resolution": ticket.get("requested_resolution", ""),
        "priority": ticket.get("priority", ""),
        "summary": ticket.get("summary", ""),
    }