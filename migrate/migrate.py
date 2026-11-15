"""One-off migration: load seed/students.json into the SQLite database.

Idempotent - it does nothing if the table already contains data.
Run with:  python -m migrate.migrate
"""
import json
import os
from pathlib import Path

from app.database import DB_PATH, get_connection, init_db

SEED_FILE = Path(os.getenv("SEED_FILE", "seed/students.json"))


def migrate() -> int:
    """Insert seed rows if the table is empty; return the number inserted."""
    init_db()
    with get_connection() as conn:
        if conn.execute("SELECT COUNT(*) FROM students").fetchone()[0] > 0:
            print("Database already contains data - skipping migration.")
            return 0
        rows = json.loads(SEED_FILE.read_text(encoding="utf-8"))
        conn.executemany("INSERT INTO students (name, score) VALUES (:name, :score)", rows)
    print(f"Migrated {len(rows)} students from {SEED_FILE} into {DB_PATH}")
    return len(rows)


if __name__ == "__main__":
    migrate()
