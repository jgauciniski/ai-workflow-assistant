import os
from dotenv import load_dotenv
from openai import OpenAI
from app.retrieval import EmbeddingService


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)
    embedding_service = EmbeddingService(client)

    text = "Customer cannot reset password and needs urgent help."
    vector = embedding_service.embed_text(text)

    text1 = "Customer cannot reset password"
    text2 = "User is unable to log in to the system"

    vec1 = embedding_service.embed_text(text1)
    vec2 = embedding_service.embed_text(text2)

    print(f"Embedding generated successfully.")
    print(f"Vector length: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")

    print("value of vec1:", vec1[:5])
    print("value of vec2:", vec2[:5])   




if __name__ == "__main__":
    main()