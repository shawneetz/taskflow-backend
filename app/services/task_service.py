# Business logic for task operations
from re import search
from turtle import position, title
from unittest import result
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.task import Task, TaskPriority, TaskStatus
from app.models.tag import Tag, task_tags
from app.schemas.task import TaskCreate, TaskRead, TaskReorder
from app.core.exceptions import NotFoundException

# Reassigning of positions 0, 1, 2... to all of the tasks in a column
async def _renormalize_column(db: AsyncSession, user_id: uuid.UUID, status: TaskStatus, exclude_id: uuid.UUID | None = None):
    task = select(Task).where(Task.user_id==user_id, Task.status==status).order_by(Task.position)
    if exclude_id: 
        task = task.where(Task.id != exclude_id)
    
    result = await db.execute(task)
    tasks = list(result.scalars().all())
    for i, t in enumerate(tasks): # reassign the id per task
        t.position = i
    
async def reorder_task(db: AsyncSession, data: TaskReorder, user_id: uuid.UUID) -> Task:
    task = await get_task_by_id(db, data.task_id, user_id)
    old_status = task.status

    task.status = data.new_status
    task.position = data.new_position
    await db.flush()

    if old_status != data.new_status:
        await _renormalize_column(db, user_id, old_status)

    dest_result = await db.execute(select(Task).where(Task.user_id==user_id, Task.status==data.new_status, Task.id==task.id).order_by(Task.position))
    dest_tasks = list(dest_result.scalars().all())
    dest_tasks.insert(Task.position, task)

    for i, t in enumerate(dest_tasks): # reassign the id per task
        t.position = i

    await db.commit()
    await db.refresh(task)
    return task

# Get all task
async def get_all_task(
    db: AsyncSession, 
    user_id: uuid.UUID, 
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None, 
    tag_id: uuid.UUID | None = None,
    search: str | None = None,
) -> list[Task]:

    task = select(Task).where(Task.user_id==user_id).options(selectinload(Task.tags))
    if status:
        task = task.where(Task.status==status)
    if priority:
        task = task.where(Task.priority==priority)
    if tag_id:
        task = task.where(Task.tag_id==tag_id)
    if search:
        task = task.where(Task.title.ilike(f"%{search}"))
    task = task.order_by(Task.position)
    result = await db.execute((task))

    return list(result.scalars().all())
    
# Get task per id
async def get_task_by_id(db: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID) -> Task:
    task_selection = select(Task).where(Task.id==task_id, Task.user_id==user_id).options(selectinload(Task.tags))
    result = await db.execute(task_selection)
    task = result.scalar_one_or_none()
    if not task:
        raise NotFoundException("Task")
    return task

# Create task
async def create_task(db: AsyncSession, user_id: uuid.UUID, data: TaskCreate) -> Task:
    
    task = Task(
        user_id = user_id,
        title = data.title,
        descrition = data.description,
        status = data.status,
        priority = data.priority,
        due_date = data.due_date,
        position=0,
    )

    if data.tag_ids:
        tag_result = await db.execute(select(Tag).where(Tag.id.in_(data.tag_ids), Tag.user_id == user_id))
        task_tags = list(tag_result.scalars().all())

    db.add(task)
    await db.flush()
    await _renormalize_column(db,user_id,data.status) 
    await db.commit()
    await db.refresh(task)
    return task

# Update task fields
async def update_task(db: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID, data) -> Task:
    task = await get_task_by_id(db, task_id, user_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        if field == "tags_ids":
            tags_result = await db.execute(select(Tag).where(Tag.id.in_(value), Tag.user_id==user_id))
            task.tags = list(tags_result.scalars().all())
        else:
            setattr(task, field, value)
    
    await db.commit()
    await db.refresh(task)
    return task 

# Delete task
async def delete_task(db: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID) -> None:
    task = await get_task_by_id(db, task_id, user_id)
    await db.delete(task)
    await db.commit()
