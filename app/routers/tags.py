# Tags router
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.tag import TagCreate, TagUpdate, TagRead
from app.services import tag_service

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("",response_model=list([TagRead]))
async def list_tags(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await tag_service.get_all_tags(db, current_user.id)

@router.post("", response_model=TagRead, status_code=201)
async def create_tag(data: TagCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await tag_service.create_tag(db, current_user.id, data)

@router.patch("/{tag_id}", response_model=TagRead)
async def update_tag(tag_id: uuid.UUID, data: TagUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await tag_service.update_tag(db, tag_id, current_user.id, data)

@router.delete("/{tag_id}", status_code=204)
async def delete_tag(tag_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await tag_service.delete_tag(db, tag_id, current_user.id)