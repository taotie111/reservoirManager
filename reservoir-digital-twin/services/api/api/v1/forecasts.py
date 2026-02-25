from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from db.database import SessionLocal
from models import Model, Prediction, Plan, DrillRecord

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ModelCreate(BaseModel):
    name: str
    version: Optional[str] = "1.0.0"
    description: Optional[str] = None
    factors: Optional[dict] = None
    status: Optional[str] = "draft"


class ModelResponse(BaseModel):
    modelId: str
    name: str
    version: str
    description: Optional[str]
    factors: Optional[dict]
    status: str
    lastTrainedAt: Optional[datetime]

    class Config:
        from_attributes = True


@router.get("/models", response_model=List[ModelResponse])
def get_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    models = db.query(Model).offset(skip).limit(limit).all()
    return models


@router.get("/models/{model_id}", response_model=ModelResponse)
def get_model(model_id: str, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.modelId == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@router.post("/models", response_model=ModelResponse)
def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    db_model = Model(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


@router.post("/models/{model_id}/train")
def train_model(model_id: str, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.modelId == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    model.status = "training"
    model.lastTrainedAt = datetime.utcnow()
    db.commit()
    return {"message": "Model training started", "modelId": model_id}


class PredictionCreate(BaseModel):
    modelId: str
    timestamp: datetime
    forecastValues: dict
    confidence: Optional[float] = None


class PredictionResponse(BaseModel):
    predictionId: str
    modelId: str
    timestamp: datetime
    forecastValues: dict
    confidence: Optional[float]

    class Config:
        from_attributes = True


@router.get("/predictions", response_model=List[PredictionResponse])
def get_predictions(skip: int = 0, limit: int = 100, modelId: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Prediction)
    if modelId:
        query = query.filter(Prediction.modelId == modelId)
    predictions = query.order_by(Prediction.timestamp.desc()).offset(skip).limit(limit).all()
    return predictions


@router.post("/predictions", response_model=PredictionResponse)
def create_prediction(prediction: PredictionCreate, db: Session = Depends(get_db)):
    db_prediction = Prediction(**prediction.dict())
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction


class PlanCreate(BaseModel):
    damId: str
    version: Optional[str] = "1.0.0"
    description: Optional[str] = None
    status: Optional[str] = "draft"


class PlanResponse(BaseModel):
    planId: str
    damId: str
    version: str
    description: Optional[str]
    createdAt: datetime
    updatedAt: datetime
    status: str

    class Config:
        from_attributes = True


@router.get("/plans", response_model=List[PlanResponse])
def get_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plans = db.query(Plan).offset(skip).limit(limit).all()
    return plans


@router.get("/dams/{dam_id}/plans", response_model=List[PlanResponse])
def get_dam_plans(dam_id: str, db: Session = Depends(get_db)):
    plans = db.query(Plan).filter(Plan.damId == dam_id).all()
    return plans


@router.post("/plans", response_model=PlanResponse)
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    db_plan = Plan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


class DrillRecordCreate(BaseModel):
    planId: str
    time: datetime
    participants: Optional[dict] = None
    results: Optional[dict] = None


class DrillRecordResponse(BaseModel):
    drillId: str
    planId: str
    time: datetime
    participants: Optional[dict]
    results: Optional[dict]

    class Config:
        from_attributes = True


@router.get("/drill-records", response_model=List[DrillRecordResponse])
def get_drill_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    records = db.query(DrillRecord).offset(skip).limit(limit).all()
    return records


@router.get("/plans/{plan_id}/drill-records", response_model=List[DrillRecordResponse])
def get_plan_drill_records(plan_id: str, db: Session = Depends(get_db)):
    records = db.query(DrillRecord).filter(DrillRecord.planId == plan_id).all()
    return records


@router.post("/drill-records", response_model=DrillRecordResponse)
def create_drill_record(record: DrillRecordCreate, db: Session = Depends(get_db)):
    db_record = DrillRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
