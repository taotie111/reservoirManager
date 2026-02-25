from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from db.database import SessionLocal
from models import Alarm

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AlarmCreate(BaseModel):
    damId: Optional[str] = None
    pointId: Optional[str] = None
    level: str
    message: str
    status: Optional[str] = "active"


class AlarmUpdate(BaseModel):
    level: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None
    acknowledgedAt: Optional[datetime] = None
    resolvedAt: Optional[datetime] = None


class AlarmResponse(BaseModel):
    alarmId: str
    damId: Optional[str]
    pointId: Optional[str]
    level: str
    message: str
    createdAt: datetime
    acknowledgedAt: Optional[datetime]
    resolvedAt: Optional[datetime]
    status: str

    class Config:
        from_attributes = True


@router.get("/alarms", response_model=List[AlarmResponse])
def get_alarms(
    skip: int = 0, 
    limit: int = 100, 
    damId: Optional[str] = None,
    level: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Alarm)
    
    if damId:
        query = query.filter(Alarm.damId == damId)
    if level:
        query = query.filter(Alarm.level == level)
    if status:
        query = query.filter(Alarm.status == status)
    
    alarms = query.order_by(Alarm.createdAt.desc()).offset(skip).limit(limit).all()
    return alarms


@router.get("/alarms/{alarm_id}", response_model=AlarmResponse)
def get_alarm(alarm_id: str, db: Session = Depends(get_db)):
    alarm = db.query(Alarm).filter(Alarm.alarmId == alarm_id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    return alarm


@router.post("/alarms", response_model=AlarmResponse)
def create_alarm(alarm: AlarmCreate, db: Session = Depends(get_db)):
    db_alarm = Alarm(**alarm.dict())
    db.add(db_alarm)
    db.commit()
    db.refresh(db_alarm)
    return db_alarm


@router.put("/alarms/{alarm_id}", response_model=AlarmResponse)
def update_alarm(alarm_id: str, alarm: AlarmUpdate, db: Session = Depends(get_db)):
    db_alarm = db.query(Alarm).filter(Alarm.alarmId == alarm_id).first()
    if not db_alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    
    for key, value in alarm.dict(exclude_unset=True).items():
        setattr(db_alarm, key, value)
    
    db.commit()
    db.refresh(db_alarm)
    return db_alarm


@router.post("/alarms/{alarm_id}/acknowledge", response_model=AlarmResponse)
def acknowledge_alarm(alarm_id: str, db: Session = Depends(get_db)):
    alarm = db.query(Alarm).filter(Alarm.alarmId == alarm_id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    
    alarm.status = "acknowledged"
    alarm.acknowledgedAt = datetime.utcnow()
    db.commit()
    db.refresh(alarm)
    return alarm


@router.post("/alarms/{alarm_id}/resolve", response_model=AlarmResponse)
def resolve_alarm(alarm_id: str, db: Session = Depends(get_db)):
    alarm = db.query(Alarm).filter(Alarm.alarmId == alarm_id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    
    alarm.status = "resolved"
    alarm.resolvedAt = datetime.utcnow()
    db.commit()
    db.refresh(alarm)
    return alarm


@router.delete("/alarms/{alarm_id}")
def delete_alarm(alarm_id: str, db: Session = Depends(get_db)):
    alarm = db.query(Alarm).filter(Alarm.alarmId == alarm_id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    
    db.delete(alarm)
    db.commit()
    return {"message": "Alarm deleted successfully"}
