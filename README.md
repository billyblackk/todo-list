# FastAPI Todo API

A production-style Todo / task management API built with FastAPI.

## Tech stack

- FastAPI
- Uvicorn
- SQLAlchemy / Alembic (planned)
- JWT-based auth (planned)
- PostgreSQL-ready (using SQLite in dev)

## Running locally

```bash
python3 -m venv .todo-list
source .todo-list/bin/activate
pip install -r requirements.txt  # once we add this
uvicorn app.main:app --reload
