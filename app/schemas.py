from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class NoteCreate(BaseModel):
    title: str
    content: str

class Note(BaseModel):
    id: str
    title: str
    content: str

class ChatRequest(BaseModel):
    question: str
    top_k: int = 5

class RetrievedContext(BaseModel):
    text: str
    metadata: Dict[str, Any]

class ChatResponse(BaseModel):
    answer: str
    contexts: List[RetrievedContext]
