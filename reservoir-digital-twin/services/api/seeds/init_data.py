import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from datetime import datetime, timedelta
from db.database import SessionLocal, engine, Base
from models import Dam, Sensor, MonitoringPoint, Timeseries, Alarm, User
from security import hash_password

def create_seed_data():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    existing_dams = db.query(Dam).first()
    if existing_dams:
        print("Seed data already exists")
        db.close()
        return
    
    dam1 = Dam(
        damId=str(uuid.uuid4()),
        name="三峡水库",
        location={"type": "Point", "coordinates": [111.0, 30.8]},
        type="混凝土重力坝",
        designParameters={"design_height_m": 181, "storage_capacity_m3": 39300000000},
        status="normal"
    )
    dam2 = Dam(
        damId=str(uuid.uuid4()),
        name="白鹤滩水电站",
        location={"type": "Point", "coordinates": [103.5, 26.9]},
        type="拱坝",
        designParameters={"design_height_m": 289, "storage_capacity_m3": 206000000000},
        status="normal"
    )
    dam3 = Dam(
        damId=str(uuid.uuid4()),
        name="溪洛渡水电站",
        location={"type": "Point", "coordinates": [103.6, 28.2]},
        type="拱坝",
        designParameters={"designParameters": {"design_height_m": 285.5}, "storage_capacity_m3": 126700000000},
        status="normal"
    )
    
    db.add_all([dam1, dam2, dam3])
    db.commit()
    
    sensors = [
        Sensor(sensorId=str(uuid.uuid4()), type="位移传感器", model="LVDT-100", unit="mm", samplingRate=1.0, accuracy=0.01, status="active"),
        Sensor(sensorId=str(uuid.uuid4()), type="渗压计", model="VW-200", unit="kPa", samplingRate=0.5, accuracy=0.1, status="active"),
        Sensor(sensorId=str(uuid.uuid4()), type="应变计", model="SM-5", unit="με", samplingRate=1.0, accuracy=1.0, status="active"),
        Sensor(sensorId=str(uuid.uuid4()), type="温度计", model="TM-1", unit="°C", samplingRate=1.0, accuracy=0.1, status="active"),
    ]
    db.add_all(sensors)
    db.commit()
    
    monitoring_points = [
        MonitoringPoint(pointId=str(uuid.uuid4()), damId=dam1.damId, name="坝顶位移测点1", pointType="位移", sensorId=sensors[0].sensorId, status="active", lastValue=12.5, unit="mm"),
        MonitoringPoint(pointId=str(uuid.uuid4()), damId=dam1.damId, name="坝基渗压测点1", pointType="渗压", sensorId=sensors[1].sensorId, status="active", lastValue=58.2, unit="kPa"),
        MonitoringPoint(pointId=str(uuid.uuid4()), damId=dam1.damId, name="坝体温度测点1", pointType="温度", sensorId=sensors[3].sensorId, status="active", lastValue=22.5, unit="°C"),
        MonitoringPoint(pointId=str(uuid.uuid4()), damId=dam2.damId, name="拱冠位移测点1", pointType="位移", sensorId=sensors[0].sensorId, status="active", lastValue=8.3, unit="mm"),
        MonitoringPoint(pointId=str(uuid.uuid4()), damId=dam2.damId, name="坝基渗压测点2", pointType="渗压", sensorId=sensors[1].sensorId, status="active", lastValue=45.6, unit="kPa"),
    ]
    db.add_all(monitoring_points)
    db.commit()
    
    now = datetime.utcnow()
    for mp in monitoring_points:
        for i in range(24):
            ts = Timeseries(
                pointId=mp.pointId,
                timestamp=now - timedelta(hours=i),
                value=mp.lastValue + (i * 0.1) - 2
            )
            db.add(ts)
    db.commit()
    
    alarms = [
        Alarm(damId=dam1.damId, pointId=monitoring_points[0].pointId, level="warning", message="坝顶位移超阈值", status="active"),
        Alarm(damId=dam1.damId, pointId=monitoring_points[1].pointId, level="critical", message="渗压值异常偏高", status="active"),
        Alarm(damId=dam2.damId, pointId=monitoring_points[3].pointId, level="info", message="位移数据正常", status="resolved"),
    ]
    db.add_all(alarms)
    db.commit()
    
    admin_user = User(
        userId=str(uuid.uuid4()),
        username="admin",
        email="admin@example.com",
        password_hash=hash_password("admin123"),
        role="admin",
        permissions={"read": True, "write": True, "delete": True},
        is_active=True
    )
    db.add(admin_user)
    db.commit()
    
    print(f"Created {len([dam1, dam2, dam3])} dams")
    print(f"Created {len(sensors)} sensors")
    print(f"Created {len(monitoring_points)} monitoring points")
    print(f"Created {len(alarms)} alarms")
    print(f"Created admin user (username: admin, password: admin123)")
    
    db.close()

if __name__ == "__main__":
    create_seed_data()
