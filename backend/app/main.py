
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.database import SessionLocal, engine
from sqlalchemy import text
from fastapi import HTTPException

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def readiness():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"status": "ready", "database": "connected"}

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

@app.get("/users")
def users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    print("User IDs:", [user.id for user in users])
    print("User names:", [user.name for user in users])
    print("Number of users:", len(users))

    return [
        {"id": user.id, "name": user.name}
        for user in users
    ]
