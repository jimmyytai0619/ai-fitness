from sqlalchemy import Column, String, Integer, Date, DateTime, JSON, Enum, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
import enum

class WorkoutType(str, enum.Enum):
    strength = "strength"
    cardio = "cardio"
    hiit = "hiit"
    yoga = "yoga"
    stretching = "stretching"
    other = "other"

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    height_cm = Column(Integer, nullable=True)
    weight_kg = Column(Float, nullable=True)
    goals = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    type = Column(Enum(WorkoutType), nullable=False)
    duration_min = Column(Integer, nullable=False)
    calories_burned = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="workouts")
