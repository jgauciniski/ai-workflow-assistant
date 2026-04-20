from dataclasses import dataclass


@dataclass
class Ticket:
    issue: str
    actions_taken: str
    requested_resolution: str
    priority: str
    summary: str | None = None

    def to_dict(self) -> dict:
        return {
            "issue": self.issue,
            "actions_taken": self.actions_taken,
            "requested_resolution": self.requested_resolution,
            "priority": self.priority,
            "summary": self.summary,
        }