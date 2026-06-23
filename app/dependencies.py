# Shared FastAPI dependencies (get_db, get_current_user)
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token:str = Depends(oauth2_scheme), db:AsyncSession = Depends(get_db)) -> User:
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise UnauthorizedException()
        user_id:str = payload.get("sub")
        if not user_id:
            raise UnauthorizedException()
    except Exception:
        raise UnauthorizedException()
    
    result = await db.execute(select(User).where(User.id==user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise UnauthorizedException()
    
    return user