# Business logic for tag operations
from multiprocessing import Value
from unittest import async_case
import re, uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import AsyncAdaptedQueuePool, result_tuple, select
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagRead, TagUpdate
from app.core.exceptions import NotFoundException, ConflictException

HEX_RE = re.compile(r'^#[0-9a-fA-F]{6}$') # validate hex colors

async def get_all_tags(db: AsyncSession, user_id: uuid.UUID) -> list[Tag]:
    result = await db.execute(select(Tag).where(Tag.user_id==user_id))
    return list(result.scalars().all())

async def create_tag(db: AsyncSession, user_id: uuid.UUID, data: TagCreate) -> Tag:
    if not HEX_RE.match(data.color):
        raise ValueError("Color must be a valid hex code e.g. #6366f1")
    existing = await db.execute(select(Tag).where(Tag.user_id==user_id, Tag.name==data.name))
    if existing.scalar_one_or_none():
        raise ConflictException(f"Tag '{data.name}' already exists")
    tag = Tag(user_id=user_id, name=data.name, color=data.color)
    db.add(tag)
    await db.commit()
    return tag

async def update_tag(db: AsyncSession, tag_id: uuid.UUID, user_id: uuid.UUID, data: TagUpdate) -> Tag:
    result = await db.execute(select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise NotFoundException("Tag")
    if data.name:
        tag.name = data.name
    if data.color:
        if not HEX_RE.match(data.color):
            raise ValueError("Color must be a valid hex code")
        tag.color = data.color
    await db.commit()
    return tag

async def delete_tag(db: AsyncSession, tag_id: uuid.UUID, user_id: uuid.UUID) -> None:
    result = await db.execute(select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise NotFoundException("Tag")
    await db.delete(tag)
    await db.commit()