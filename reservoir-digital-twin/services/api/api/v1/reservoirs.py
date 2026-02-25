from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from db.database import SessionLocal
from models import Dam, MonitoringPoint, Sensor, Timeseries, Alarm

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DamCreate(BaseModel):
    name: str
    location: Optional[dict] = None
    type: Optional[str] = None
    designParameters: Optional[dict] = None
    status: Optional[str] = "normal"


class DamUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[dict] = None
    type: Optional[str] = None
    designParameters: Optional[dict] = None
    status: Optional[str] = None


class DamResponse(BaseModel):
    damId: str
    name: str
    location: Optional[dict]
    type: Optional[str]
    designParameters: Optional[dict]
    status: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


@router.get("/dams", response_model=List[DamResponse])
def get_dams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dams = db.query(Dam).offset(skip).limit(limit).all()
    return dams


@router.get("/dams/{dam_id}", response_model=DamResponse)
def get_dam(dam_id: str, db: Session = Depends(get_db)):
    dam = db.query(Dam).filter(Dam.damId == dam_id).first()
    if not dam:
        raise HTTPException(status_code=404, detail="Dam not found")
    return dam


@router.post("/dams", response_model=DamResponse)
def create_dam(dam: DamCreate, db: Session = Depends(get_db)):
    db_dam = Dam(**dam.dict())
    db.add(db_dam)
    db.commit()
    db.refresh(db_dam)
    return db_dam


@router.put("/dams/{dam_id}", response_model=DamResponse)
def update_dam(dam_id: str, dam: DamUpdate, db: Session = Depends(get_db)):
    db_dam = db.query(Dam).filter(Dam.damId == dam_id).first()
    if not db_dam:
        raise HTTPException(status_code=404, detail="Dam not found")
    
    for key, value in dam.dict(exclude_unset=True).items():
        setattr(db_dam, key, value)
    
    db.commit()
    db.refresh(db_dam)
    return db_dam


@router.delete("/dams/{dam_id}")
def delete_dam(dam_id: str, db: Session = Depends(get_db)):
    db_dam = db.query(Dam).filter(Dam.damId == dam_id).first()
    if not db_dam:
        raise HTTPException(status_code=404, detail="Dam not found")
    
    db.delete(db_dam)
    db.commit()
    return {"message": "Dam deleted successfully"}


class MonitoringPointCreate(BaseModel):
    damId: str
    name: str
    location: Optional[dict] = None
    pointType: str
    sensorId: Optional[str] = None
    status: Optional[str] = "active"
    lastValue: Optional[float] = None
    unit: Optional[str] = None


class MonitoringPointUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[dict] = None
    pointType: Optional[str] = None
    sensorId: Optional[str] = None
    status: Optional[str] = None
    lastValue: Optional[float] = None
    unit: Optional[str] = None


class MonitoringPointResponse(BaseModel):
    pointId: str
    damId: str
    name: str
    location: Optional[dict]
    pointType: str
    sensorId: Optional[str]
    status: str
    lastValue: Optional[float]
    unit: Optional[str]
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


@router.get("/monitoring-points", response_model=List[MonitoringPointResponse])
def get_monitoring_points(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    points = db.query(MonitoringPoint).offset(skip).limit(limit).all()
    return points


@router.get("/dams/{dam_id}/monitoring-points", response_model=List[MonitoringPointResponse])
def get_dam_monitoring_points(dam_id: str, db: Session = Depends(get_db)):
    points = db.query(MonitoringPoint).filter(MonitoringPoint.damId == dam_id).all()
    return points


@router.get("/monitoring-points/{point_id}", response_model=MonitoringPointResponse)
def get_monitoring_point(point_id: str, db: Session = Depends(get_db)):
    point = db.query(MonitoringPoint).filter(MonitoringPoint.pointId == point_id).first()
    if not point:
        raise HTTPException(status_code=404, detail="Monitoring point not found")
    return point


@router.post("/monitoring-points", response_model=MonitoringPointResponse)
def create_monitoring_point(point: MonitoringPointCreate, db: Session = Depends(get_db)):
    db_point = MonitoringPoint(**point.dict())
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point


@router.put("/monitoring-points/{point_id}", response_model=MonitoringPointResponse)
def update_monitoring_point(point_id: str, point: MonitoringPointUpdate, db: Session = Depends(get_db)):
    db_point = db.query(MonitoringPoint).filter(MonitoringPoint.pointId == point_id).first()
    if not db_point:
        raise HTTPException(status_code=404, detail="Monitoring point not found")
    
    for key, value in point.dict(exclude_unset=True).items():
        setattr(db_point, key, value)
    
    db.commit()
    db.refresh(db_point)
    return db_point


@router.delete("/monitoring-points/{point_id}")
def delete_monitoring_point(point_id: str, db: Session = Depends(get_db)):
    db_point = db.query(MonitoringPoint).filter(MonitoringPoint.pointId == point_id).first()
    if not db_point:
        raise HTTPException(status_code=404, detail="Monitoring point not found")
    
    db.delete(db_point)
    db.commit()
    return {"message": "Monitoring point deleted successfully"}


class SensorCreate(BaseModel):
    type: str
    model: Optional[str] = None
    unit: Optional[str] = None
    samplingRate: Optional[float] = None
    accuracy: Optional[float] = None
    status: Optional[str] = "active"


class SensorResponse(BaseModel):
    sensorId: str
    type: str
    model: Optional[str]
    unit: Optional[str]
    samplingRate: Optional[float]
    accuracy: Optional[float]
    status: str
    installedAt: datetime
    removedAt: Optional[datetime]

    class Config:
        from_attributes = True


@router.get("/sensors", response_model=List[SensorResponse])
def get_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensors = db.query(Sensor).offset(skip).limit(limit).all()
    return sensors


@router.get("/sensors/{sensor_id}", response_model=SensorResponse)
def get_sensor(sensor_id: str, db: Session = Depends(get_db)):
    sensor = db.query(Sensor).filter(Sensor.sensorId == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.post("/sensors", response_model=SensorResponse)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    db_sensor = Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


@router.delete("/sensors/{sensor_id}")
def delete_sensor(sensor_id: str, db: Session = Depends(get_db)):
    db_sensor = db.query(Sensor).filter(Sensor.sensorId == sensor_id).first()
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    db.delete(db_sensor)
    db.commit()
    return {"message": "Sensor deleted successfully"}
