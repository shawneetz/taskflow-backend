# Token creation, verification, refresh logic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import ConflictException, UnauthorizedException

async def register_user(db: AsyncSession, data: UserCreate) -> User:
    if len(data.password) < 8:
        raise ValueError("Password must be at least 8 characters")
    
    result = await db.execute(select(User).where(User.email==data.email))
    if result.scalar_one_or_none():
        raise ConflictException("Email already registered")

    user = User(email=data.email, hashed_password=hash_password(data.password), full_name=data.full_name)
    db.add(user)
    
    await db.commit()
    return user

async def login_user(db: AsyncSession, email: str, password: str) -> dict:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedException("Incorrect email or password")
    
    return {
        "access_token": create_access_token(str(user.id)),
        "refresh_token": create_refresh_token(str(user.id)), 
        "token_type":"bearer",
    }

async def refresh_access_token(db: AsyncSession, refresh_token:str) -> dict:
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise UnauthorizedException()
        
        user_id = payload.get("sub")
    except Exception:
        raise UnauthorizedException("Invalid or expired refresh token")
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise UnauthorizedException()
    
    return {
        "access_token": create_access_token(str(user.id)), 
        "token_type": "bearer",
    }