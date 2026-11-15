"""Pure helper functions (no database or web code)."""
from statistics import mean, median

GRADE_BANDS: tuple[tuple[int, str], ...] = (
    (70, "A"), (60, "B"), (50, "C"), (45, "D"), (40, "E"),
)


def grade_for(score: float) -> str:
    """Convert a numeric score to a letter grade."""
    for minimum, grade in GRADE_BANDS:
        if score >= minimum:
            return grade
    return "F"


def compute_stats(scores: list[float]) -> dict:
    """Return count/highest/lowest/average/median; safe for an empty list."""
    if not scores:
        return {"count": 0, "highest": None, "lowest": None, "average": 0.0, "median": 0.0}
    return {
        "count": len(scores),
        "highest": max(scores),
        "lowest": min(scores),
        "average": round(mean(scores), 2),
        "median": median(scores),
    }
