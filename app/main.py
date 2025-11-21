from fastapi import FastAPI

from app.core.database import Base, engine

from app.models import task as task_model  # noqa: F401
from app.models import user as user_model  # noqa: F401

from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router

app = FastAPI(title="Todo List API")

# Create tables in the database (for now we do this at startup)
Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


# Mount the task endpoints

app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(auth_router)
