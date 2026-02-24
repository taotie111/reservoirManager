from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ScheduleCompare(BaseModel):
    reservoir_id: int
    schemes: list[dict]

@router.post("/schedules/compare")
def compare_schedules(payload: ScheduleCompare):
    # Stub: return a simple comparison result
    return {"best": payload.schemes[0] if payload.schemes else None, "count": len(payload.schemes)}
