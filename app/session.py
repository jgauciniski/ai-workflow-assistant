import json
from pathlib import Path


def get_data_paths() -> tuple[Path, Path]:
    project_root = Path(__file__).resolve().parent.parent
    tickets_output_path = project_root / "data" / "cli_tickets.json"
    qa_output_path = project_root / "data" / "qa_history.json"

    return tickets_output_path, qa_output_path


def save_session(saved_tickets: list, qa_history: list) -> None:
    tickets_output_path, qa_output_path = get_data_paths()

    with open(tickets_output_path, "w", encoding="utf-8") as file:
        json.dump(saved_tickets, file, indent=2)
    
    print("Saved results to cli_tickets.json")

    with open(qa_output_path, "w", encoding="utf-8") as file:
        json.dump(qa_history, file, indent=2)
    
    print("Saved Q&A history to qa_history.json")

def load_session() -> tuple[list, list]:
    tickets_output_path, qa_output_path = get_data_paths()

    saved_tickets = []
    qa_history = []

    if tickets_output_path.exists():
        with open(tickets_output_path, "r", encoding="utf-8") as file:
            saved_tickets = json.load(file)

    if qa_output_path.exists():
        with open(qa_output_path, "r", encoding="utf-8") as file:
            qa_history = json.load(file)

    return saved_tickets, qa_history