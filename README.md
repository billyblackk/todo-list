# FastAPI Todo API

A clean, production-style backend service for managing tools, built with FastAPI and SQLAlchemy.

This porject demonstrates backend fundamentals: API design, authentication, database modelling, and cleean project structure.




## Tech stack

Backend
- FastAPI
- SQLAlchemy ORM
- SQLite (dev) - PostgresSQL-ready
- Pydantic schemas
- Uvicorn ASGI server

Infrastructure
- Docker
- Docker Compose
- Environment-based config

Planned
- Alembic migrations
- JWT-based authentication
- Unit & integration tests (pytest)




## Project Structure

.
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── core/                  # Config, database session
│   ├── models/                # SQLAlchemy models
│   ├── routers/               # API endpoint routers
│   ├── schemas/               # Pydantic request/response schemas
│   └── __init__.py
├── tests/                     # pytest tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md




## Running locally

```bash

python3 -m venv .todo-list
source .todo-list/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload

```




## Running the API with Docker

```bash

docker compose up --build
```

Then visit http://localhost:8000/docs




## Database

The app uses:
- SQLite(todo.db) for local development
- Fully compatible with PostgreSQL if you change the DATABASE_URL

Example SQLite URL:

```python

SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"
```




## API Endpoints

Health Check
- GET /health

Tasks
- GET /tasks/
- POST /tasks/
- GET /tasks/{id}
- PUT /tasks/{id}
- DELETE /tasks/{id}

Users (if implemented)
- POST /users/
- GET /users/me

Auth (planned)
- POST /auth/login
- POST /auth/register




## Example Requests (cURL)

- Create a new task
```bash

curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn FastAPI", "description":"Build portfolio backend"}'
```

- List tasks
```bash
curl http://localhost:8000/tasks/
```




## Running Tests (Upcoming)
```bash
pytest
```




## Future Improvements
- Add JWT auth
- Add role-based permissions (admin/user)
- Add Alembic migrations
- Add Postgres support
- Add full pytest test suite
- Add request rate limiting
- Add background jobs (Celery/ RQ)
- Add GitHub Actions CI pipeline