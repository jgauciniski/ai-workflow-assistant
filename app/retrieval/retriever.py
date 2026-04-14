import math
from typing import Any


class Retriever:
    def cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        if len(vec1) != len(vec2):
            raise ValueError("Vectors must have the same length.")

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def find_most_similar(
        self,
        query_embedding: list[float],
        tickets: list[dict[str, Any]],
        top_k: int = 3,
    ) -> list[dict[str, Any]]:
        scored_tickets = []

        for ticket in tickets:
            ticket_embedding = ticket.get("embedding")
            if not ticket_embedding:
                continue

            score = self.cosine_similarity(query_embedding, ticket_embedding)

            scored_tickets.append({
                "score": score,
                "ticket": ticket
            })

        scored_tickets.sort(key=lambda item: item["score"], reverse=True)

        return scored_tickets[:top_k]