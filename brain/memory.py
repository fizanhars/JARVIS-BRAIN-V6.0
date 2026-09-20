import sqlite3
from pathlib import Path

DB_PATH = Path("data/memory.db")


def init_memory():
    """Create the memory database and table."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_memory(content):
    """Save a new memory."""
    if not content or not content.strip():
        return

    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "INSERT INTO memories (content) VALUES (?)",
            (content.strip(),)
        )


def get_memories(limit=10):
    """Get recent memories."""
    with sqlite3.connect(DB_PATH) as db:
        rows = db.execute(
            """
            SELECT content
            FROM memories
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    return [row[0] for row in rows]


def clear_memory():
    """Delete all stored memories."""
    with sqlite3.connect(DB_PATH) as db:
        db.execute("DELETE FROM memories")
