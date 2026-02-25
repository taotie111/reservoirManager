from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from passlib.context import CryptContext

from db.database import SessionLocal
from models import User
from security import hash_password, verify_password, get_current_user, require_role

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    password: str
    role: Optional[str] = "viewer"
    permissions: Optional[dict] = None


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    permissions: Optional[dict] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    userId: str
    username: str
    email: Optional[str]
    role: str
    permissions: Optional[dict]
    is_active: bool
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


@router.get("/users", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(require_role("admin"))):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users/me", response_model=UserResponse)
def get_current_user_info(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db), current_user: dict = Depends(require_role("admin"))):
    user = db.query(User).filter(User.userId == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_role("admin"))):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role=user.role,
        permissions=user.permissions
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db), current_user: dict = Depends(require_role("admin"))):
    db_user = db.query(User).filter(User.userId == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.email is not None:
        db_user.email = user.email
    if user.password is not None:
        db_user.password_hash = hash_password(user.password)
    if user.role is not None:
        db_user.role = user.role
    if user.permissions is not None:
        db_user.permissions = user.permissions
    if user.is_active is not None:
        db_user.is_active = user.is_active
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db), current_user: dict = Depends(require_role("admin"))):
    db_user = db.query(User).filter(User.userId == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
