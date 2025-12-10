import uuid
from pathlib import Path

from app.embeddings import embed_texts
from app.vector_store import add_documents

NOTES_DIR = Path("notes")

def load_notes():
    docs = []
    for path in NOTES_DIR.glob("**/*"):
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
            try:
                text = path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"⚠️ Could not read {path}: {e}")
                continue

            title = path.stem
            docs.append((str(path), title, text))
    return docs

def main():
    notes = load_notes()
    if not notes:
        print("No notes found in ./notes. Add some .md or .txt files first.")
        return

    print(f"Found {len(notes)} notes. Embedding them one by one...")

    ids = []
    texts = []
    metadatas = []
    embeddings = []

    for path, title, text in notes:
        # Clean & validate
        if text is None:
            print(f"⚠️ Skipping {path}: content is None")
            continue

        text_str = str(text).strip()
        if not text_str:
            print(f"⚠️ Skipping {path}: content is empty after stripping")
            continue

        try:
            emb_list = embed_texts([text_str])
            if not emb_list:
                print(f"⚠️ No embedding returned for {path}")
                continue
            emb = emb_list[0]
        except Exception as e:
            print(f"❌ Failed to embed {path}: {e}")
            continue

        note_id = str(uuid.uuid4())

        ids.append(note_id)
        texts.append(text_str)
        metadatas.append({"path": path, "title": title})
        embeddings.append(emb)

        print(f"✅ Embedded: {path}")

    if not ids:
        print("No valid notes were embedded. Nothing to add to the vector store.")
        return

    print(f"\nAdding {len(ids)} embedded notes to Chroma...")
    add_documents(
        ids=ids,
        texts=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    print("✅ Ingestion complete.")

if __name__ == "__main__":
    main()
