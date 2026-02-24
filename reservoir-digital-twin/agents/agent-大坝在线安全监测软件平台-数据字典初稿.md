# 大坝在线安全监测软件平台 - 数据字典初稿 v0.2

以下为核心实体的数据字典初稿，后续将扩展字段约束、索引、关系及业务规则。

## 1) Dam（坝体/水库）
- damId: UUID
- name: string
- location: GEOMETRY(POINT, CGCS2000)
- type: string
- designParameters: JSON
- status: string
- createdAt: TIMESTAMP
- updatedAt: TIMESTAMP

## 2) MonitoringPoint（监测点）
- pointId: UUID
- damId: UUID (FK -> Dam.damId)
- name: string
- location: GEOMETRY(POINT, CGCS2000)
- pointType: string
- sensorId: UUID (FK -> Sensor.sensorId)
- status: string
- lastValue: float
- unit: string
- createdAt: TIMESTAMP
- updatedAt: TIMESTAMP

## 3) Sensor（传感器）
- sensorId: UUID
- type: string
- model: string
- unit: string
- samplingRate: float
- accuracy: float
- status: string
- installedAt: TIMESTAMP
- removedAt: TIMESTAMP NULL

## 4) Timeseries（时间序列数据）
- tsId: UUID
- pointId: UUID (FK -> MonitoringPoint.pointId)
- timestamp: TIMESTAMP
- value: float

## 5) Alarm（告警）
- alarmId: UUID
- damId: UUID (FK -> Dam.damId) NULL
- pointId: UUID (FK -> MonitoringPoint.pointId) NULL
- level: string
- message: string
- createdAt: TIMESTAMP
- acknowledgedAt: TIMESTAMP NULL
- resolvedAt: TIMESTAMP NULL
- status: string

## 6) PatrolRoute（巡查路线）
- routeId: UUID
- damId: UUID (FK)
- name: string
- path: JSON (GeoJSON)
- createdAt: TIMESTAMP
- updatedAt: TIMESTAMP

## 7) HazardRecord（隐患记录）
- hazardId: UUID
- damId: UUID (FK)
- description: TEXT
- severity: string
- status: string
- reportedAt: TIMESTAMP
- dueAt: TIMESTAMP
- closedAt: TIMESTAMP NULL

## 8) RectificationTask（整改任务）
- taskId: UUID
- hazardId: UUID (FK)
- description: TEXT
- responsible: string
- status: string
- createdAt: TIMESTAMP
- dueDate: TIMESTAMP
- closedAt: TIMESTAMP NULL

## 9) Model（预测/分析模型）
- modelId: UUID
- name: string
- version: string
- description: TEXT
- factors: JSON
- status: string
- lastTrainedAt: TIMESTAMP

## 10) Prediction（预测输出）
- predictionId: UUID
- modelId: UUID (FK)
- timestamp: TIMESTAMP
- forecastValues: JSON
- confidence: float

## 11) Plan（预案/滚动）
- planId: UUID
- damId: UUID (FK)
- version: string
- description: TEXT
- createdAt: TIMESTAMP
- updatedAt: TIMESTAMP
- status: string

## 12) DrillRecord（演练记录）
- drillId: UUID
- planId: UUID (FK)
- time: TIMESTAMP
- participants: JSON
- results: JSON

## 13) Report（报表）
- reportId: UUID
- damId: UUID (FK)
- type: string
- date: DATE
- content: JSON
- generatedAt: TIMESTAMP

## 14) Document（文档）
- docId: UUID
- type: string
- title: string
- content: TEXT
- attachments: JSON

## 15) User/Role/Permission（简要）
- userId: UUID
- username: string
- role: string
- permissions: JSON

> 说明：此数据字典初稿以核心实体为主，后续将逐步形成字段约束、索引与关系等的详细信息。

(End of file)
