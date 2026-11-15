# Reverse Engineering of Lab 2 / Lab 3 Code

## 1. Inventory of the existing code

### Lab 2 - student-scm (v1.1)
| Module | Classes / functions | Responsibility |
|---|---|---|
| `students.py` | `Student`, `StudentRegistry` (`add`, `all`, `average`, `median`), `_validate_name`, `_validate_score` | Data + validation + statistics |
| `utils/helpers.py` | `highest_score`, `lowest_score`, `grade_for`, `rank_students`, `GRADE_BANDS` | Helper logic |
| `app.py` | `print_report`, `main` | Presentation (console) + demo data |

### Lab 3 - inventory-csa (v1.0)
| Module | Classes / functions | Responsibility |
|---|---|---|
| `inventory.py` | `Item`, `inventory` list | Data + validation |
| `utils/helpers.py` | `item_value`, `total_stock_value`, `highest_stock_item`, `lowest_stock_item`, `low_stock_items` | Calculations |
| `app.py` | `print_report`, `_name`, `main` | Presentation |

## 2. Dependency diagram (existing system)
```mermaid
flowchart LR
    subgraph Lab2[Lab 2 - student-scm]
        A2[app.py] --> S2[students.py]
        A2 --> H2[utils/helpers.py]
        H2 --> S2
    end
    subgraph Lab3[Lab 3 - inventory-csa]
        A3[app.py] --> I3[inventory.py]
        A3 --> H3[utils/helpers.py]
        H3 --> I3
    end
```

## 3. Coupling and code smells found
- **Mixed responsibilities:** `students.py` holds the data model, the default demo data, validation and statistics in one file (low cohesion).
- **Presentation tied to data:** `app.py` hard-codes demo data via `registry.add(...)`, so the console UI cannot be reused by another front end.
- **Hard-coded data source:** records live in Python source; changing data means changing code. No persistence.
- **Duplicated logic:** both labs repeat the same patterns (validation, highest/lowest, report formatting).
- **Helpers depend on the data module** (`helpers -> students`), so pure utility code is coupled to the model.
- **No separation between logic and I/O:** formatting and calculation sit together in `print_report`.
- **Global mutable state:** `default_registry` is a module-level singleton shared by importers.

## 4. Improvement plan (implemented in this repo)
| Smell | Fix |
|---|---|
| Mixed responsibilities | Split into `models.py`, `controllers.py`, `utils.py`, `database.py`, `main.py` |
| Hard-coded data | Migrate JSON data to SQLite (`migrate/migrate.py`) |
| Console-only access | Expose RESTful endpoints with FastAPI |
| Duplicated logic (DRY) | One `_to_out()` converter, one `compute_stats()`, one `GRADE_BANDS` |
| Weak typing | Type hints everywhere, Pydantic validation |
| Hard to deploy | Dockerfiles + `docker-compose.yml` |

## 5. Dependency diagram (re-engineered system)
```mermaid
flowchart TD
    Client([Client / Swagger UI]) --> MAIN[app/main.py<br/>FastAPI routes]
    MAIN --> CTRL[app/controllers.py<br/>business logic]
    MAIN --> MODELS[app/models.py<br/>Pydantic schemas]
    CTRL --> MODELS
    CTRL --> UTILS[app/utils.py<br/>pure helpers]
    CTRL --> DB[app/database.py<br/>SQLite access]
    MIG[migrate/migrate.py] --> DB
    SEED[(seed/students.json)] --> MIG
    DB --> SQLITE[(students.db)]
```

## 6. Container architecture
```mermaid
flowchart LR
    subgraph Compose[docker compose]
        M[migrate service<br/>runs once] -->|writes| V[(db_data volume<br/>/data/students.db)]
        V -->|reads/writes| API[api service<br/>FastAPI :8000]
    end
    User([Browser]) -->|localhost:8000| API
```
