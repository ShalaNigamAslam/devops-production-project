from fastapi import FastAPI

from app.database import SessionLocal
from app.models import User

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users")
def users():
    db = SessionLocal()

    try:
        users = db.query(User).all()
        print("SQLAlchemy returned:", users)
        print("Number of users:", len(users))  
        return [
            {"id": user.id, "name": user.name}
            for user in users
        ]

    finally:
        db.close()
