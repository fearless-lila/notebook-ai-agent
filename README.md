
# Notebook AI Agent 🧠

An AI-powered "second brain" that lets you **store notes** and **chat with them** using Retrieval-Augmented Generation (RAG).

- Notes can live as simple `.md` / `.txt` files in a `notes/` folder.
- They are embedded into a local vector database (Chroma).
- A FastAPI backend exposes:
  - `POST /notes` – create notes via API
  - `GET /notes` – list notes created via the API (from `notes.json`)
  - `POST /chat` – ask questions grounded in your notes

This project is structured as a learning project, but can evolve into a real AI notebook.

---

## 🚀 Features

- 📝 Write notes in plain text or Markdown files.
- 📥 Ingest notes into a vector store with a single script.
- 🔍 Retrieve relevant notes via embeddings.
- 💬 Chat endpoint that answers **only based on your notes**.
- 💾 Persistent storage for API-created notes in `notes.json`.
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
│   ├── storage.py         # JSON persistence for API-created notes
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
├── notes.json             # Persistent storage for API-created notes
└── README.md
```

---

## 🧑‍💻 Setup

### 1. Clone & enter the project

From wherever you keep your code:

```bash
cd ~/Desktop
git clone <your-repo-url> notebook-ai-agent  # if using git
cd notebook-ai-agent
```

Or just `cd` into the folder where you created the project.

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
# On Windows (PowerShell):
# .venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-real-key-here
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4.1-mini

# Optional (defaults provided)
CHROMA_DB_DIR=chroma_db
COLLECTION_NAME=second_brain_notes
```

> ⚠️ Never commit `.env` or your API key to Git.

---

## 📝 Notes: File-based vs API-created

There are **two ways** to add notes:

1. **File-based notes** (stored as `.md` / `.txt` in `notes/`, ingested with `ingest_notes.py`)
2. **API-created notes** (created via `POST /notes` in the Swagger UI and stored in `notes.json`)

Both types are embedded and stored in Chroma and are used by `/chat`.  
Only API-created notes appear in `/notes` (because they live in `notes.json`).

---

## 🧪 How to Run, Edit Notes, and Use the Server

This section explains the **everyday workflow**: how to start the server, edit notes, re-ingest them, and use the API UI.

---

### 1. Activate the virtual environment

From the project root (e.g. `notebook-ai-agent/`):

```bash
source .venv/bin/activate
# On Windows (PowerShell):
# .venv\Scripts\Activate.ps1
```

---

### 2. Run the FastAPI server

From the project root, with the venv activated:

```bash
uvicorn app.main:app --reload
```

You should see something like:

```text
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
📂 Loaded N notes from disk at startup.
```

Leave this running while you use the app.

---

### 3. Open the API UI (Swagger)

In your browser, go to:

```text
http://127.0.0.1:8000/docs
```

From here you can:

- `POST /notes` → create a note via the API (stored in `notes.json` + embedded into Chroma)
- `GET /notes` → list all notes created via the API in this project
- `POST /chat` → ask questions grounded in your notes

---

### 4. Adding or editing file-based notes (`notes/*.md` or `.txt`)

To **add or edit file-based notes**:

1. Create or edit `.md` / `.txt` files in the `notes/` folder, for example:

   ```text
   notes/
     ai.md
     rag.md
     vector_databases.md
     personal_notes.md
   ```

2. After adding or editing files, run the ingestion script:

   ```bash
   python ingest_notes.py
   ```

This will:

- Read all `.md` / `.txt` files under `notes/`
- Skip empty files
- Generate embeddings via the OpenAI API
- Store text + embeddings + metadata in Chroma

You **do not** need to restart the server after editing files; you only need to re-run `ingest_notes.py` so the changes are reflected in the vector store.

---

### 5. Creating notes from the UI (`POST /notes`)

To create notes via the API UI:

1. Ensure the server is running (`uvicorn app.main:app --reload`).
2. Open `http://127.0.0.1:8000/docs`.
3. Expand `POST /notes` → click **“Try it out”**.
4. Use a body like:

   ```json
   {
     "title": "New note from UI",
     "content": "This note was created from the Swagger UI and will be persisted."
   }
   ```

5. Click **“Execute”**.

This will:

- Embed the note content with OpenAI embeddings
- Store the embedding + text in Chroma
- Save the note (id, title, content) into `notes.json`
- Make the note visible in `GET /notes`
- Make it available immediately to `/chat` (no extra steps needed)

You **do not** need to run `ingest_notes.py` for notes created via `POST /notes`, and you **do not** need to restart the server.

---

### 6. Using `/chat` to query your notes

In the Swagger UI:

1. Expand `POST /chat` → click **“Try it out”**.
2. Provide a request body such as:

   ```json
   {
     "question": "What did I write about RAG?",
     "top_k": 3
   }
   ```

3. Click **“Execute”**.

The API will:

- Embed your question
- Query Chroma for the most similar notes (file-based + API-created, as long as they were embedded)
- Send the retrieved context + your question to the chat model
- Return:

  ```json
  {
    "answer": "...",
    "contexts": [
      {
        "text": "note text here...",
        "metadata": {
          "title": "rag",
          "path": "notes/rag.md"
        }
      }
    ]
  }
  ```

---

### 7. When to restart the server

You only need to restart `uvicorn` when:

- You change Python code (e.g., `main.py`, `storage.py`, `embeddings.py`, etc.), or
- You change environment variables in `.env`.

You **do not** need to restart the server when you:

- Add/edit notes in `notes/` → just run `python ingest_notes.py`
- Create notes via `POST /notes` → they are embedded and saved immediately

---

## 📥 Ingest Notes (File-based)

Whenever you add or change files in `notes/`, run:

```bash
python ingest_notes.py
```

Sample output:

```text
Found 5 notes. Embedding them one by one...
✅ Embedded: notes/ai.md
✅ Embedded: notes/rag.md
⚠️ Skipping notes/diary.md: content is empty after stripping

Adding 4 embedded notes to Chroma...
✅ Ingestion complete.
```

---

## 🌐 API Overview

### `POST /notes` – Create a note via API

Creates a note, embeds it, and saves to the vector DB and `notes.json`.

Example request body:

```json
{
  "title": "New Note Created From UI",
  "content": "This note was created via API and will be used by the RAG system."
}
```

Example response:

```json
{
  "id": "uuid-here",
  "title": "New Note Created From UI",
  "content": "This note was created via API..."
}
```

---

### `GET /notes` – List notes (from notes.json)

Returns the notes created via `POST /notes`:

```json
[
  {
    "id": "uuid-here",
    "title": "New Note Created From UI",
    "content": "..."
  }
]
```

File-based notes ingested via `ingest_notes.py` won’t appear here (they’re in Chroma only).

---

### `POST /chat` – Chat with your notes

Ask questions grounded only in your notes.

Example request:

```json
{
  "question": "What did I write about RAG?",
  "top_k": 3
}
```

Example response:

```json
{
  "answer": "You wrote that RAG stands for Retrieval-Augmented Generation and combines vector search with LLMs.",
  "contexts": [
    {
      "text": "# RAG\n\nRAG stands for Retrieval-Augmented Generation...",
      "metadata": {
        "title": "rag",
        "path": "notes/rag.md"
      }
    }
  ]
}
```

---

## 🧱 How It Works (High Level)

1. **Ingestion (`ingest_notes.py`):**
   - Reads note files
   - Cleans & validates text
   - Calls OpenAI embeddings
   - Stores text + embeddings + metadata in Chroma

2. **Retrieval (in `/chat`):**
   - Embeds the user’s question
   - Uses Chroma to find similar note chunks
   - Feeds those as context into the chat model

3. **Generation (`llm.py`):**
   - System prompt forces the LLM to answer *only* using provided context
   - If notes don’t contain the answer → it says it doesn’t know

---

## 🧭 Future Improvements / Ideas

- 🔄 Unify file-based notes and API notes in a single logical view.
- 🧩 Chunk notes by section/heading for better retrieval.
- 💻 Build a custom frontend chat UI (HTML/JS or React).
- 🔍 Add tagging, timestamps, and search.
- 🧪 Add evaluation & debug tools for RAG quality.
- 🗄 Swap JSON for SQLite or MongoDB when the project grows.

---

## 🐛 Troubleshooting

### `openai.BadRequestError: '$.input' is invalid`

One of your notes is likely:

- Empty
- Extremely large
- Not valid UTF-8

The current `ingest_notes.py` already skips empty/unreadable notes and embeds them one by one, printing a clear error per file.

### `openai.RateLimitError` or `insufficient_quota`

Your OpenAI account may be out of credits or have no billing set up.  
Check the billing and usage pages in your OpenAI dashboard.

### `OPENAI_API_KEY is not set`

Make sure `.env` exists and contains:

```env
OPENAI_API_KEY=sk-your-real-key-here
```

---

## 📜 License

This is a personal learning project. Add your preferred license if you open-source it.

---

## 💡 Notes

This project is intentionally small and readable so it’s easy to learn:

- How RAG works end-to-end
- How to combine a vector DB + LLM
- How to build a simple “second brain” AI over your notes

Feel free to extend, break, and rebuild it as you learn more.
