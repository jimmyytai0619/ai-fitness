from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from routes import users  # your router file

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to ["http://localhost:3000"] later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/")
def root():
    return {"message": "AI Fitness Backend running!"}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    u = crud.create_user(db, email=user.email, name=user.name)
    return u

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

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
