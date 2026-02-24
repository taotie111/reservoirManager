from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...db.database import SessionLocal
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from ...security import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    # Very small login example for demonstration purposes
    # In a real app, validate against the users table
    if req.username == "admin" and req.password == "admin123":
        token = create_access_token({"sub": req.username, "role": "admin"})
        return {"access_token": token, "token_type": "bearer"}
    # Fallback: raise unauthorized
    raise HTTPException(status_code=401, detail="Invalid credentials")
