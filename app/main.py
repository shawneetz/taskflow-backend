# FastAPI app factory, middleware, routers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, users, tasks, tags

app = FastAPI(title="TaskFlow API", version="1.0.0")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.CORS_ORIGINS, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
    )

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(tags.router)

@app.get("/health")
async def health():
    return {"status": "ok"}