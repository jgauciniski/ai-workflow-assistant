def validate_priority(data: dict) -> dict:
    allowed = {"low", "medium", "high"}

    priority = data.get("priority")

    if priority not in allowed:
        raise ValueError(f"Invalid priority: {priority}")

    return {"priority": priority}


def validate_ticket(data: dict) -> dict:
    required_fields = ["issue", "actions_taken", "requested_resolution"]

    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"Missing field: {field}")

    return {
        "issue": data["issue"],
        "actions_taken": data["actions_taken"],
        "requested_resolution": data["requested_resolution"],
    }