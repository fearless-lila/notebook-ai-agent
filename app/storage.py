import json
import os
from pathlib import Path
from typing import Dict, Any

# JSON file on disk where we store notes created via the API
DATA_FILE = Path(os.getenv("NOTES_JSON_PATH", "notes.json"))

def load_notes() -> Dict[str, Dict[str, Any]]:
    """
    Load notes from a JSON file on disk.
    Returns a dict: {note_id: {id, title, content}}.
    """
    if not DATA_FILE.exists():
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {str(k): v for k, v in data.items()}
        return {}
    except Exception as e:
        print(f"⚠️ Failed to load notes from {DATA_FILE}: {e}")
        return {}

def save_notes(notes: Dict[str, Dict[str, Any]]) -> None:
    """
    Save notes dict to JSON on disk.
    """
    try:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
        print(f"💾 Saved {len(notes)} notes to {DATA_FILE}")
    except Exception as e:
        print(f"❌ Failed to save notes to {DATA_FILE}: {e}")
