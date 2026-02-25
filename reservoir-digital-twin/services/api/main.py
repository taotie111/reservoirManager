import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine, Base
from api.v1 import auth, reservoirs, measurements, forecasts, alerts, timeseries, patrol, users

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        if db:
            db.close()

def create_app() -> FastAPI:
    app = FastAPI(title="Reservoir Digital Twin API", version="1.0.0")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(reservoirs.router, prefix="/api/v1")
    app.include_router(measurements.router, prefix="/api/v1")
    app.include_router(forecasts.router, prefix="/api/v1")
    app.include_router(alerts.router, prefix="/api/v1")
    app.include_router(timeseries.router, prefix="/api/v1")
    app.include_router(patrol.router, prefix="/api/v1")
    app.include_router(users.router, prefix="/api/v1")
    return app

app = create_app()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
