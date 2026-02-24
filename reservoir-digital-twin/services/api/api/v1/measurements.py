from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Measurement(BaseModel):
    sensor_id: int
    timestamp: str
    value: float
    quality_flag: str | None = None

@router.post("/measurements/bulk")
def bulk_measurements(payload: list[Measurement]):
    # Stub: pretend to write to DB
    return {"count": len(payload), "status": "accepted"}
