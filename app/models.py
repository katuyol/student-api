"""Pydantic models (request/response schemas) for the Student API."""
from pydantic import BaseModel, Field


class StudentIn(BaseModel):
    """Payload for creating a student."""

    name: str = Field(min_length=1, max_length=100)
    score: float = Field(ge=0, le=100)


class StudentOut(StudentIn):
    """Student as returned by the API."""

    id: int
    grade: str


class Stats(BaseModel):
    """Summary statistics for all students."""

    count: int
    highest: float | None
    lowest: float | None
    average: float
    median: float
