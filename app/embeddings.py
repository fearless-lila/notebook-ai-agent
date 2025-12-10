from typing import List
from openai import OpenAI
from .config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Returns a list of embedding vectors for the provided texts.
    """
    if not texts:
        return []

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    # response.data is a list of objects with .embedding
    return [item.embedding for item in response.data]
