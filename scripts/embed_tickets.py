import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.retrieval import EmbeddingService


def build_ticket_text(ticket: dict) -> str:
    return f"""
Issue: {ticket.get("issue", "")}
Actions taken: {ticket.get("actions_taken", "")}
Requested resolution: {ticket.get("requested_resolution", "")}
Priority: {ticket.get("priority", "")}
""".strip()


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "processed_tickets.json"

    client = OpenAI(api_key=api_key)
    embedding_service = EmbeddingService(client)

    with open(data_path, "r", encoding="utf-8") as f:
        tickets = json.load(f)

    for ticket in tickets:
        if "embedding" in ticket:
            continue

        text_to_embed = build_ticket_text(ticket)

        if not text_to_embed.strip():
            print(f"Skipping empty ticket: {ticket}")
            continue

        embedding = embedding_service.embed_text(text_to_embed)
        ticket["embedding"] = embedding

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2)

    print("Embeddings added to tickets successfully.")


if __name__ == "__main__":
    main()