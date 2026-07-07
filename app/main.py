# FastAPI app factory, middleware, routers
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.session import get_db
from app.routers import auth, users, tasks, tags

app = FastAPI(title="TaskFlow API", version="1.0.0")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.cors_origins_list, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
    )

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(tags.router)

@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {"status": "ok"}