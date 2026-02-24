from ..db.database import SessionLocal
from ..models import User  # type: ignore
from ..security import hash_password
from datetime import datetime

def seed():
    db = SessionLocal()
    try:
        # Admin user
        if not db.query(User).filter(User.username == 'admin').first():
            admin = User(username='admin', email='admin@example.com', password_hash=hash_password('admin123'), role='admin', created_at=datetime.utcnow())
            db.add(admin)
        db.commit()
    finally:
        db.close()
