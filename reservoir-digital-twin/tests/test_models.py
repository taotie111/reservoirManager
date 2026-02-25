"""
Unit tests for core data models
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Dam, MonitoringPoint, Sensor, Alarm, User
from db.database import Base


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


class TestDamModel:
    def test_create_dam(self, db_session):
        dam = Dam(
            damId="test-dam-001",
            name="Test Dam",
            location={"type": "Point", "coordinates": [111.0, 30.0]},
            type="Test Type",
            status="normal"
        )
        db_session.add(dam)
        db_session.commit()
        
        result = db_session.query(Dam).filter(Dam.damId == "test-dam-001").first()
        assert result is not None
        assert result.name == "Test Dam"
        assert result.status == "normal"

    def test_dam_relationships(self, db_session):
        dam = Dam(damId="test-dam-002", name="Dam with relations", status="normal")
        db_session.add(dam)
        db_session.commit()
        
        sensor = Sensor(sensorId="test-sensor-001", type="displacement", status="active")
        db_session.add(sensor)
        db_session.commit()
        
        mp = MonitoringPoint(
            pointId="test-mp-001",
            damId=dam.damId,
            name="Test Point",
            pointType="displacement",
            sensorId=sensor.sensorId,
            status="active"
        )
        db_session.add(mp)
        db_session.commit()
        
        result = db_session.query(Dam).filter(Dam.damId == dam.damId).first()
        assert len(result.monitoring_points) == 1


class TestAlarmModel:
    def test_create_alarm(self, db_session):
        dam = Dam(damId="test-dam-003", name="Dam for alarm", status="normal")
        db_session.add(dam)
        db_session.commit()
        
        alarm = Alarm(
            alarmId="test-alarm-001",
            damId=dam.damId,
            level="critical",
            message="Test alarm message",
            status="active"
        )
        db_session.add(alarm)
        db_session.commit()
        
        result = db_session.query(Alarm).filter(Alarm.alarmId == "test-alarm-001").first()
        assert result is not None
        assert result.level == "critical"
        assert result.status == "active"


class TestUserModel:
    def test_create_user(self, db_session):
        user = User(
            userId="test-user-001",
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            role="admin",
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        result = db_session.query(User).filter(User.username == "testuser").first()
        assert result is not None
        assert result.role == "admin"
        assert result.is_active is True
