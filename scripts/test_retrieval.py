import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.retrieval import EmbeddingService, Retriever


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "processed_tickets.json"

    with open(data_path, "r", encoding="utf-8") as f:
        tickets = json.load(f)

    client = OpenAI(api_key=api_key)
    embedding_service = EmbeddingService(client)
    retriever = Retriever()

    query = "A user cannot access the HR system to get tax documents"
    query_embedding = embedding_service.embed_text(query)

    results = retriever.find_most_similar(query_embedding, tickets, top_k=3)

    print(f"Query: {query}\n")

    for index, result in enumerate(results, start=1):
        ticket = result["ticket"]
        score = result["score"]

        print(f"Result #{index}")
        print(f"Score: {score:.4f}")
        print(f"Issue: {ticket.get('issue', '')}")
        print(f"Priority: {ticket.get('priority', '')}")
        print("-" * 50)


if __name__ == "__main__":
    main()