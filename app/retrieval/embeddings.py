from openai import OpenAI

# Service to generate embeddings for text using OpenAI's API
class EmbeddingService:
    def __init__(self, client: OpenAI, model: str = "text-embedding-3-small"):
        self.client = client
        self.model = model

    def embed_text(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise ValueError("Text for embedding cannot be empty.")

        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )

        return response.data[0].embedding