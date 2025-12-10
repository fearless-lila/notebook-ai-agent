import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from .config import CHROMA_DB_DIR, COLLECTION_NAME

# Create a persistent Chroma client
_client = chromadb.PersistentClient(
    path=CHROMA_DB_DIR,
    settings=Settings(anonymized_telemetry=False),
)

_collection = _client.get_or_create_collection(
    name=COLLECTION_NAME,
)

def add_documents(
    ids: List[str],
    texts: List[str],
    embeddings: List[List[float]],
    metadatas: List[Dict[str, Any]],
):
    _collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

def query_documents(query_embedding: List[float], k: int = 5):
    result = _collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )
    return result
