"""Business logic: the only layer that talks to the database."""
import sqlite3

from app.database import get_connection
from app.models import StudentIn, StudentOut
from app.utils import compute_stats, grade_for


def _to_out(row: sqlite3.Row) -> StudentOut:
    """Convert a database row into a StudentOut (single place, keeps code DRY)."""
    return StudentOut(id=row["id"], name=row["name"], score=row["score"],
                      grade=grade_for(row["score"]))


def list_students() -> list[StudentOut]:
    """Return all students ordered by score (highest first)."""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM students ORDER BY score DESC, id").fetchall()
    return [_to_out(r) for r in rows]


def get_student(student_id: int) -> StudentOut | None:
    """Return one student or None."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    return _to_out(row) if row else None


def create_student(data: StudentIn) -> StudentOut:
    """Insert a student and return the stored record."""
    with get_connection() as conn:
        cur = conn.execute("INSERT INTO students (name, score) VALUES (?, ?)",
                           (data.name.strip(), data.score))
        new_id = cur.lastrowid
    return get_student(new_id)  # type: ignore[arg-type]


def delete_student(student_id: int) -> bool:
    """Delete a student; return True if a row was removed."""
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        return cur.rowcount > 0


def get_stats() -> dict:
    """Summary statistics across all students."""
    with get_connection() as conn:
        scores = [r["score"] for r in conn.execute("SELECT score FROM students")]
    return compute_stats(scores)
