# Tasks router

import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.task import TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead, TaskReorder
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("", response_model=list[TaskRead])
async def list_tasks(
    status: TaskStatus | None = Query(default=None),
    priority: TaskPriority | None = Query(default=None),
    tag_id: uuid.UUID | None = Query(default=None),
    search: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.get_all_task(db, current_user.id, status, priority, tag_id, search)

@router.post("", response_model=TaskRead, status_code=201)
async def create_task(data: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await task_service.create_task(db, current_user.id, data)

# IMPORTANT: /reorder must be above /{task_id}
@router.patch("/reorder", response_model=TaskRead)
async def reorder_task(data: TaskReorder, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await task_service.reorder_task(db, data, current_user.id)

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await task_service.get_task_by_id(db, task_id, current_user.id)

@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(task_id: uuid.UUID, data: TaskUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await task_service.update_task(db, task_id, current_user.id, data)

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await task_service.delete_task(db, task_id, current_user.id)