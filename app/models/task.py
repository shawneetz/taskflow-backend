# Task model
import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, func, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    in_review = "in_review"
    done = "done"

class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("tasks_user_id_idx", "user_id"),
        Index("tasks_user_id_status_idx", "user_id", "status"),
        Index("tasks_due_date_idx", "due_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.todo)
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority), default=TaskPriority.medium)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    position: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="tasks") # pyright: ignore[reportUndefinedVariable]
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary="task_tags", back_populates="tasks")  # pyright: ignore[reportUndefinedVariable]
