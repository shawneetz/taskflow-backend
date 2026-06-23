# Tag model
import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func, UniqueConstraint, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("user_id", "name", name="tags_user_id_name_key"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(7), default="#6366f1")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="tags") # pyright: ignore[reportUndefinedVariable]
    tasks: Mapped[list["Task"]] = relationship("Task", secondary=task_tags, back_populates="tags") # pyright: ignore[reportUndefinedVariable]
