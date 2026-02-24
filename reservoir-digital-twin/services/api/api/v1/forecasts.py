from fastapi import APIRouter

router = APIRouter()

@router.post("/forecasts")
def create_forecast():
    # Stub: in real, enqueue a background task to compute forecast
    return {"forecast_id": 1, "status": "queued"}

@router.get("/forecasts/{id}")
def get_forecast(id: int):
    return {"forecast_id": id, "data": {"level": "low"}}
