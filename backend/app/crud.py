from sqlalchemy.orm import Session
from app import models, schemas

def create_user(db: Session, email: str, name: str | None = None):
    user = models.User(email=email, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_workout(db: Session, user_id, workout: schemas.WorkoutIn):
    db_w = models.Workout(user_id=user_id, date=workout.date, type=workout.type,
                          duration_min=workout.duration_min, calories_burned=workout.calories_burned,
                          details=workout.details)
    db.add(db_w)
    db.commit()
    db.refresh(db_w)
    return db_w

def list_workouts(db: Session, user_id, skip=0, limit=100):
    return db.query(models.Workout).filter(models.Workout.user_id == user_id).order_by(models.Workout.date.desc()).offset(skip).limit(limit).all()
