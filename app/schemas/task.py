# TaskCreate, TaskRead, TaskUpdate, TaskReorder

import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.task import TaskStatus, TaskPriority
from app.schemas.tag import TagRead

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    due_date: datetime | None = None
    tag_ids: list[uuid.UUID] = []

class TaskUpdate(BaseModel): 
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None
    tag_ids: list[uuid.UUID] | None = None

class TaskReorder(BaseModel):
    task_id: uuid.UUID
    new_status: TaskStatus
    new_position: int

class TaskRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None 
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None
    position: int
    tags: list[TagRead]
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}