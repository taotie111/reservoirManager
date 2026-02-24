from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Reservoir ML Service")

class History(BaseModel):
    history: list[float]

@app.post('/ml/train')
def train_model():
    # Stub: pretend to train a simple model
    return {"status": "trained", "version": "1.0.0"}

@app.post('/ml/predict/water_level')
def predict(history: History):
    # Very simple heuristic: last value + small random noise
    if not history.history:
        return {"prediction": []}
    last = history.history[-1]
    pred = [float(last + np.random.normal(scale=0.1)) for _ in range(10)]
    return {"prediction": pred}
