from fastapi import FastAPI, HTTPException
from typing import List
import uuid

from .schemas import NoteCreate, Note, ChatRequest, ChatResponse, RetrievedContext
from .embeddings import embed_texts
from .vector_store import add_documents, query_documents
from .llm import answer_with_context

app = FastAPI(title="Second Brain Note Assistant")

# Simple in-memory store (demo only)
NOTES_DB: dict[str, dict] = {}

@app.post("/notes", response_model=Note)
def create_note(note: NoteCreate):
    note_id = str(uuid.uuid4())
    embeddings = embed_texts([note.content])
    if not embeddings:
        raise HTTPException(status_code=500, detail="Failed to create embedding for note.")
    embedding = embeddings[0]

    add_documents(
        ids=[note_id],
        texts=[note.content],
        embeddings=[embedding],
        metadatas=[{"title": note.title}],
    )

    NOTES_DB[note_id] = {
        "id": note_id,
        "title": note.title,
        "content": note.content,
    }

    return Note(**NOTES_DB[note_id])

@app.get("/notes", response_model=List[Note])
def list_notes():
    return list(NOTES_DB.values())

@app.post("/chat", response_model=ChatResponse)
def chat_with_notes(req: ChatRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    query_embedding_list = embed_texts([question])
    if not query_embedding_list:
        raise HTTPException(status_code=500, detail="Failed to create embedding for query.")
    query_embedding = query_embedding_list[0]

    result = query_documents(query_embedding, k=req.top_k)

    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]

    if not docs:
        answer = "I couldn't find anything in your notes related to that."
        return ChatResponse(answer=answer, contexts=[])

    answer = answer_with_context(question, docs)

    contexts = [
        RetrievedContext(text=doc, metadata=meta or {})
        for doc, meta in zip(docs, metas)
    ]

    return ChatResponse(answer=answer, contexts=contexts)
