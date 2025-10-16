from celery import Celery
import os
from app.config import settings
from app.database import SessionLocal
import pandas as pd
from datetime import datetime

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery_app.task
def parse_workout_csv(file_path: str, user_id: str):
    """
    Example CSV parser expected columns: date,type,duration_min,calories_burned,details
    file_path is a path inside the container (you can mount /uploads or similar)
    """
    df = pd.read_csv(file_path)
    from app import crud
    db = SessionLocal()
    created = []
    for _, row in df.iterrows():
        try:
            wk = {
                "date": pd.to_datetime(row["date"]).date(),
                "type": row["type"],
                "duration_min": int(row["duration_min"]),
                "calories_burned": int(row["calories_burned"]) if "calories_burned" in row and not pd.isna(row["calories_burned"]) else None,
                "details": {}
            }
            created.append(crud.create_workout(db, user_id, wk))
        except Exception as e:
            print("skip row", e)
    db.close()
    return len(created)
