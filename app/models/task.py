from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base

# This script creates the database table


class Task(Base):  # SQLAlchemy ORM Model
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    is_done = Column(Boolean, nullable=False, server_default="0")
