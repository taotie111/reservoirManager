import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from db.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Dam(Base):
    __tablename__ = "dams"

    damId = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False, index=True)
    location = Column(JSON, nullable=True)
    type = Column(String(50), nullable=True)
    designParameters = Column(JSON, nullable=True)
    status = Column(String(20), nullable=False, default="normal")
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    monitoring_points = relationship("MonitoringPoint", back_populates="dam", cascade="all, delete-orphan")
    alarms = relationship("Alarm", back_populates="dam", cascade="all, delete-orphan")
    patrol_routes = relationship("PatrolRoute", back_populates="dam", cascade="all, delete-orphan")
    hazard_records = relationship("HazardRecord", back_populates="dam", cascade="all, delete-orphan")
    plans = relationship("Plan", back_populates="dam", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="dam", cascade="all, delete-orphan")


class Sensor(Base):
    __tablename__ = "sensors"

    sensorId = Column(String(36), primary_key=True, default=generate_uuid)
    type = Column(String(50), nullable=False)
    model = Column(String(100), nullable=True)
    unit = Column(String(20), nullable=True)
    samplingRate = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)
    status = Column(String(20), nullable=False, default="active")
    installedAt = Column(DateTime, default=datetime.utcnow)
    removedAt = Column(DateTime, nullable=True)

    monitoring_points = relationship("MonitoringPoint", back_populates="sensor")


class MonitoringPoint(Base):
    __tablename__ = "monitoring_points"

    pointId = Column(String(36), primary_key=True, default=generate_uuid)
    damId = Column(String(36), ForeignKey("dams.damId"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    location = Column(JSON, nullable=True)
    pointType = Column(String(50), nullable=False)
    sensorId = Column(String(36), ForeignKey("sensors.sensorId"), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    lastValue = Column(Float, nullable=True)
    unit = Column(String(20), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    dam = relationship("Dam", back_populates="monitoring_points")
    sensor = relationship("Sensor", back_populates="monitoring_points")
    timeseries = relationship("Timeseries", back_populates="monitoring_point", cascade="all, delete-orphan")
    alarms = relationship("Alarm", back_populates="monitoring_point", cascade="all, delete-orphan")


class Timeseries(Base):
    __tablename__ = "timeseries"

    tsId = Column(String(36), primary_key=True, default=generate_uuid)
    pointId = Column(String(36), ForeignKey("monitoring_points.pointId"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    value = Column(Float, nullable=False)

    monitoring_point = relationship("MonitoringPoint", back_populates="timeseries")


class Alarm(Base):
    __tablename__ = "alarms"

    alarmId = Column(String(36), primary_key=True, default=generate_uuid)
    damId = Column(String(36), ForeignKey("dams.damId"), nullable=True, index=True)
    pointId = Column(String(36), ForeignKey("monitoring_points.pointId"), nullable=True, index=True)
    level = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    acknowledgedAt = Column(DateTime, nullable=True)
    resolvedAt = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default="active")

    dam = relationship("Dam", back_populates="alarms")
    monitoring_point = relationship("MonitoringPoint", back_populates="alarms")


class PatrolRoute(Base):
    __tablename__ = "patrol_routes"

    routeId = Column(String(36), primary_key=True, default=generate_uuid)
    damId = Column(String(36), ForeignKey("dams.damId"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    path = Column(JSON, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    dam = relationship("Dam", back_populates="patrol_routes")


class HazardRecord(Base):
    __tablename__ = "hazard_records"

    hazardId = Column(String(36), primary_key=True, default=generate_uuid)
    damId = Column(String(36), ForeignKey("dams.damId"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="open")
    reportedAt = Column(DateTime, default=datetime.utcnow)
    dueAt = Column(DateTime, nullable=True)
    closedAt = Column(DateTime, nullable=True)

    dam = relationship("Dam", back_populates="hazard_records")
    rectification_tasks = relationship("RectificationTask", back_populates="hazard_record", cascade="all, delete-orphan")


class RectificationTask(Base):
    __tablename__ = "rectification_tasks"

    taskId = Column(String(36), primary_key=True, default=generate_uuid)
    hazardId = Column(String(36), ForeignKey("hazard_records.hazardId"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    responsible = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    createdAt = Column(DateTime, default=datetime.utcnow)
    dueDate = Column(DateTime, nullable=True)
    closedAt = Column(DateTime, nullable=True)

    hazard_record = relationship("HazardRecord", back_populates="rectification_tasks")


class Model(Base):
    __tablename__ = "models"

    modelId = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    version = Column(String(20), nullable=False, default="1.0.0")
    description = Column(Text, nullable=True)
    factors = Column(JSON, nullable=True)
    status = Column(String(20), nullable=False, default="draft")
    lastTrainedAt = Column(DateTime, nullable=True)

    predictions = relationship("Prediction", back_populates="model", cascade="all, delete-orphan")


class Prediction(Base):
    __tablename__ = "predictions"

    predictionId = Column(String(36), primary_key=True, default=generate_uuid)
    modelId = Column(String(36), ForeignKey("models.modelId"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False)
    forecastValues = Column(JSON, nullable=False)
    confidence = Column(Float, nullable=True)

    model = relationship("Model", back_populates="predictions")


class Plan(Base):
    __tablename__ = "plans"

    planId = Column(String(36), primary_key=True, default=generate_uuid)
    damId = Column(String(36), ForeignKey("dams.damId"), nullable=False, index=True)
    version = Column(String(20), nullable=False, default="1.0.0")
    description = Column(Text, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(20), nullable=False, default="draft")

    dam = relationship("Dam", back_populates="plans")
    drill_records = relationship("DrillRecord", back_populates="plan", cascade="all, delete-orphan")


class DrillRecord(Base):
    __tablename__ = "drill_records"

    drillId = Column(String(36), primary_key=True, default=generate_uuid)
    planId = Column(String(36), ForeignKey("plans.planId"), nullable=False, index=True)
    time = Column(DateTime, nullable=False)
    participants = Column(JSON, nullable=True)
    results = Column(JSON, nullable=True)

    plan = relationship("Plan", back_populates="drill_records")


class Report(Base):
    __tablename__ = "reports"

    reportId = Column(String(36), primary_key=True, default=generate_uuid)
    damId = Column(String(36), ForeignKey("dams.damId"), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
    content = Column(JSON, nullable=True)
    generatedAt = Column(DateTime, default=datetime.utcnow)

    dam = relationship("Dam", back_populates="reports")


class Document(Base):
    __tablename__ = "documents"

    docId = Column(String(36), primary_key=True, default=generate_uuid)
    type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    attachments = Column(JSON, nullable=True)


class User(Base):
    __tablename__ = "users"

    userId = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), nullable=True)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    permissions = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
