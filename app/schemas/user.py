# UserCreate, UserRead, UserUpdate
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str          # min 8 chars — validated in service
    full_name: str

class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = None
