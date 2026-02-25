from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from db.database import SessionLocal
from models import Timeseries

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TimeseriesCreate(BaseModel):
    pointId: str
    timestamp: datetime
    value: float


class TimeseriesBatchCreate(BaseModel):
    pointId: str
    data: List[dict]


class TimeseriesResponse(BaseModel):
    tsId: str
    pointId: str
    timestamp: datetime
    value: float

    class Config:
        from_attributes = True


@router.get("/timeseries", response_model=List[TimeseriesResponse])
def get_timeseries(
    skip: int = 0, 
    limit: int = 1000,
    pointId: Optional[str] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Timeseries)
    
    if pointId:
        query = query.filter(Timeseries.pointId == pointId)
    if start:
        query = query.filter(Timeseries.timestamp >= start)
    if end:
        query = query.filter(Timeseries.timestamp <= end)
    
    timeseries = query.order_by(Timeseries.timestamp.desc()).offset(skip).limit(limit).all()
    return timeseries


@router.get("/monitoring-points/{point_id}/timeseries", response_model=List[TimeseriesResponse])
def get_point_timeseries(
    point_id: str,
    skip: int = 0, 
    limit: int = 1000,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Timeseries).filter(Timeseries.pointId == point_id)
    
    if start:
        query = query.filter(Timeseries.timestamp >= start)
    if end:
        query = query.filter(Timeseries.timestamp <= end)
    
    timeseries = query.order_by(Timeseries.timestamp.desc()).offset(skip).limit(limit).all()
    return timeseries


@router.post("/timeseries", response_model=TimeseriesResponse)
def create_timeseries(data: TimeseriesCreate, db: Session = Depends(get_db)):
    db_ts = Timeseries(**data.dict())
    db.add(db_ts)
    db.commit()
    db.refresh(db_ts)
    return db_ts


@router.post("/timeseries/batch")
def create_timeseries_batch(batch: TimeseriesBatchCreate, db: Session = Depends(get_db)):
    created = 0
    for item in batch.data:
        ts = Timeseries(
            pointId=batch.pointId,
            timestamp=item.get("timestamp"),
            value=item.get("value")
        )
        db.add(ts)
        created += 1
    
    db.commit()
    return {"message": f"Created {created} timeseries records"}
