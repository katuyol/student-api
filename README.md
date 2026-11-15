# Student Score API (SEN 401 Lab 4 - Re-engineering & Migration)

Re-engineered version of the Lab 2/3 console app: modular, typed, backed by
SQLite, exposed through FastAPI and deployed with Docker Compose.

## Structure
```
app/models.py        Pydantic schemas (StudentIn, StudentOut, Stats)
app/database.py      SQLite connection + schema
app/controllers.py   Business logic (only layer that touches the DB)
app/utils.py         Pure helpers (grade_for, compute_stats)
app/main.py          FastAPI routes
migrate/migrate.py   JSON -> SQLite migration (idempotent)
seed/students.json   Legacy data being migrated
docker/              api.Dockerfile, migrate.Dockerfile
docker-compose.yml   migrate (one-off) + api services, shared volume
tests/               pytest API tests
docs/                Reverse-engineering notes + dependency diagrams
```

## Run with Docker
```
docker compose up --build
```
Open http://localhost:8000/docs (interactive Swagger UI).

## Run locally (no Docker)
```
pip install -r requirements.txt
python -m migrate.migrate
uvicorn app.main:app --reload
```

## Endpoints
GET /health, GET /students, GET /students/{id}, POST /students,
DELETE /students/{id}, GET /stats
