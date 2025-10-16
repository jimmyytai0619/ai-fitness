from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from uuid import UUID
from app.models import WorkoutType

class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    name: Optional[str]

    class Config:
        orm_mode = True

class WorkoutIn(BaseModel):
    date: date
    type: WorkoutType
    duration_min: int
    calories_burned: Optional[int] = None
    details: Optional[dict] = None

class WorkoutOut(WorkoutIn):
    id: UUID

    class Config:
        orm_mode = True
