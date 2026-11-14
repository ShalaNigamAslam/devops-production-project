from app.database import SessionLocal
from app.models import User

db = SessionLocal()

try:
    user = db.query(User).filter(User.name == "Carey").first()

    if user is None:
        user = User(name="Carey")
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created user: {user.id} - {user.name}")
    else:
        print("Carey already exists; skipping insert.")

finally:
    db.close()
