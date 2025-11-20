from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool = False


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.

    Same fields as TaskBase for now.
    """

    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    All fields are optional, so we can do partial updates
    """

    title: Optional[str] = None
    descitption: Optional[str] = None
    is_done: Optional[bool] = None


class Task(TaskBase):
    """
    Schema for reading a task (what we send back to the client).

    Includes DB-generated fields like id and timestamps.
    """

    id: int

    class Config:
        from_attributes = True  # tells pydantic that it can read from ORM objects
