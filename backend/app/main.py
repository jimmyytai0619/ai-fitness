from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from app.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI instance
app = FastAPI()

# CORS configuration
origins = [
    "https://ai-fitness-production.up.railway.app",  # your frontend URL
    "http://localhost:3000",                          # for local frontend testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "AI Fitness Backend running!"}

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Users endpoints
@app.get("/api/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/api/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    u = crud.create_user(db, email=user.email, name=user.name)
    return u

# Workouts endpoints
@app.post("/api/users/{user_id}/workouts", response_model=schemas.WorkoutOut)
def add_workout(user_id: str, workout: schemas.WorkoutIn, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    w = crud.create_workout(db, user_id, workout)
    return w

@app.get("/api/users/{user_id}/workouts")
def get_workouts(user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    rows = crud.list_workouts(db, user_id)
    return rows

# ✅ Run with PORT from environment (Railway compatible)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)
