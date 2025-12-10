# Notebook AI Agent 🧠

An AI-powered "second brain" that lets you **store notes** and **chat with them** using Retrieval-Augmented Generation (RAG).

- Notes live as simple `.md` / `.txt` files in a `notes/` folder.
- They are embedded into a local vector database (Chroma).
- A FastAPI backend exposes:
  - `POST /notes` – create notes via API
  - `GET /notes` – list in-memory notes
  - `POST /chat` – ask questions grounded in your notes

This project is inspired by “AI note-taking / second-brain” style apps and is structured as a learning project.

---

## 🚀 Features

- 📝 Write notes in plain text or Markdown files.
- 📥 Ingest notes into a vector store with a single script.
- 🔍 Retrieve relevant notes via embeddings.
- 💬 Chat endpoint that answers **only based on your notes**.
- 🧱 Simple architecture and readable code – easy to extend.

---

## 🧰 Tech Stack

- **Language:** Python 3.10+ (tested with 3.13)
- **Framework:** FastAPI
- **Vector DB:** Chroma (persistent local store)
- **LLM & Embeddings:** OpenAI API
- **Environment:** `venv` + `.env` for secrets

---

## 📂 Project Structure

```bash
notebook-ai-agent/
├── app/
│   ├── __init__.py
│   ├── config.py          # Loads .env, constants, paths
│   ├── embeddings.py      # OpenAI embeddings helper
│   ├── vector_store.py    # ChromaDB wrapper
│   ├── schemas.py         # Pydantic models (Notes, Chat)
│   ├── llm.py             # Chat completion with context
│   └── main.py            # FastAPI app (routes)
├── notes/                 # Your .md / .txt notes live here
│   ├── ai.md
│   ├── rag.md
│   ├── vector_databases.md
│   └── ...
├── chroma_db/             # Chroma's persistent storage (auto-created)
├── ingest_notes.py        # Script to embed notes from `notes/`
├── requirements.txt
├── .env                   # OpenAI API key + model config
└── README.md
