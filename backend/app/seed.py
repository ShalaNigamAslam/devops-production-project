from app.database import SessionLocal
from app.models import User

db = SessionLocal()

user = User(name="Alice")

db.add(user)
db.commit()
db.refresh(user)

print(f"Created user: {user.id} - {user.name}")

db.close()
