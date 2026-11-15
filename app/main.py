"""FastAPI application: RESTful access to the student database."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from app import controllers
from app.database import init_db
from app.models import Stats, StudentIn, StudentOut


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Make sure the schema exists when the API starts."""
    init_db()
    yield


app = FastAPI(title="Student Score API", version="2.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    """Liveness check."""
    return {"status": "ok"}


@app.get("/students", response_model=list[StudentOut])
def list_students():
    """List all students."""
    return controllers.list_students()


@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int):
    """Get one student by id."""
    student = controllers.get_student(student_id)
    if student is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student not found")
    return student


@app.post("/students", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentIn):
    """Create a student (validated by Pydantic)."""
    return controllers.create_student(data)


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    """Delete a student."""
    if not controllers.delete_student(student_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student not found")


@app.get("/stats", response_model=Stats)
def stats():
    """Highest, lowest, average and median score."""
    return controllers.get_stats()
