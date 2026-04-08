import json
from pathlib import Path

class Session:
    def __init__(self, tickets=None, qa_history=None):
        self.tickets = tickets or []
        self.qa_history = qa_history or []


def get_data_paths() -> tuple[Path, Path]:
    project_root = Path(__file__).resolve().parent.parent
    tickets_output_path = project_root / "data" / "cli_tickets.json"
    qa_output_path = project_root / "data" / "qa_history.json"

    return tickets_output_path, qa_output_path


def save_session(session: Session) -> None:
    tickets_output_path, qa_output_path = get_data_paths()

    try:
        with open(tickets_output_path, "w", encoding="utf-8") as file:
            json.dump(session.tickets, file, indent=2)

        with open(qa_output_path, "w", encoding="utf-8") as file:
            json.dump(session.qa_history, file, indent=2)

    except Exception as error:
        raise RuntimeError(f"Failed to save session: {error}") from error

def load_session() -> Session:
    tickets_output_path, qa_output_path = get_data_paths()

    tickets = []
    qa_history = []

    try:
        if tickets_output_path.exists():
            with open(tickets_output_path, "r", encoding="utf-8") as file:
                tickets = json.load(file)

        if qa_output_path.exists():
            with open(qa_output_path, "r", encoding="utf-8") as file:
                qa_history = json.load(file)

        return Session(tickets, qa_history)

    except Exception as error:
        raise RuntimeError(f"Failed to load session: {error}") from error