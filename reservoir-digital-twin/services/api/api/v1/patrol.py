from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from db.database import SessionLocal
from models import PatrolRoute, HazardRecord, RectificationTask

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PatrolRouteCreate(BaseModel):
    damId: str
    name: str
    path: Optional[dict] = None


class PatrolRouteResponse(BaseModel):
    routeId: str
    damId: str
    name: str
    path: Optional[dict]
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


@router.get("/patrol-routes", response_model=List[PatrolRouteResponse])
def get_patrol_routes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    routes = db.query(PatrolRoute).offset(skip).limit(limit).all()
    return routes


@router.get("/dams/{dam_id}/patrol-routes", response_model=List[PatrolRouteResponse])
def get_dam_patrol_routes(dam_id: str, db: Session = Depends(get_db)):
    routes = db.query(PatrolRoute).filter(PatrolRoute.damId == dam_id).all()
    return routes


@router.post("/patrol-routes", response_model=PatrolRouteResponse)
def create_patrol_route(route: PatrolRouteCreate, db: Session = Depends(get_db)):
    db_route = PatrolRoute(**route.dict())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


@router.delete("/patrol-routes/{route_id}")
def delete_patrol_route(route_id: str, db: Session = Depends(get_db)):
    route = db.query(PatrolRoute).filter(PatrolRoute.routeId == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Patrol route not found")
    
    db.delete(route)
    db.commit()
    return {"message": "Patrol route deleted successfully"}


class HazardRecordCreate(BaseModel):
    damId: str
    description: str
    severity: str
    status: Optional[str] = "open"
    dueAt: Optional[datetime] = None


class HazardRecordResponse(BaseModel):
    hazardId: str
    damId: str
    description: str
    severity: str
    status: str
    reportedAt: datetime
    dueAt: Optional[datetime]
    closedAt: Optional[datetime]

    class Config:
        from_attributes = True


@router.get("/hazard-records", response_model=List[HazardRecordResponse])
def get_hazard_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    records = db.query(HazardRecord).offset(skip).limit(limit).all()
    return records


@router.get("/dams/{dam_id}/hazard-records", response_model=List[HazardRecordResponse])
def get_dam_hazard_records(dam_id: str, db: Session = Depends(get_db)):
    records = db.query(HazardRecord).filter(HazardRecord.damId == dam_id).all()
    return records


@router.post("/hazard-records", response_model=HazardRecordResponse)
def create_hazard_record(record: HazardRecordCreate, db: Session = Depends(get_db)):
    db_record = HazardRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@router.put("/hazard-records/{hazard_id}", response_model=HazardRecordResponse)
def update_hazard_record(hazard_id: str, record: HazardRecordCreate, db: Session = Depends(get_db)):
    db_record = db.query(HazardRecord).filter(HazardRecord.hazardId == hazard_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Hazard record not found")
    
    for key, value in record.dict(exclude_unset=True).items():
        setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record


class RectificationTaskCreate(BaseModel):
    hazardId: str
    description: str
    responsible: Optional[str] = None
    status: Optional[str] = "pending"
    dueDate: Optional[datetime] = None


class RectificationTaskResponse(BaseModel):
    taskId: str
    hazardId: str
    description: str
    responsible: Optional[str]
    status: str
    createdAt: datetime
    dueDate: Optional[datetime]
    closedAt: Optional[datetime]

    class Config:
        from_attributes = True


@router.get("/rectification-tasks", response_model=List[RectificationTaskResponse])
def get_rectification_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(RectificationTask).offset(skip).limit(limit).all()
    return tasks


@router.get("/hazard-records/{hazard_id}/rectification-tasks", response_model=List[RectificationTaskResponse])
def get_hazard_rectification_tasks(hazard_id: str, db: Session = Depends(get_db)):
    tasks = db.query(RectificationTask).filter(RectificationTask.hazardId == hazard_id).all()
    return tasks


@router.post("/rectification-tasks", response_model=RectificationTaskResponse)
def create_rectification_task(task: RectificationTaskCreate, db: Session = Depends(get_db)):
    db_task = RectificationTask(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/rectification-tasks/{task_id}/close")
def close_rectification_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(RectificationTask).filter(RectificationTask.taskId == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Rectification task not found")
    
    task.status = "closed"
    task.closedAt = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task
