"""SQLite access layer: connection handling and schema."""
import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "students.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT NOT NULL,
    score REAL NOT NULL CHECK (score BETWEEN 0 AND 100)
)
"""


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Yield a connection that commits on success and rolls back on error."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create the students table if it does not exist."""
    with get_connection() as conn:
        conn.execute(SCHEMA)
