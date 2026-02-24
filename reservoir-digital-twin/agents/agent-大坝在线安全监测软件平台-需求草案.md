# 大坝在线安全监测软件平台 — 需求草案 v0.2

日期：2026-02-24
版本：0.2
作者：OpenCode

本草案将现有规划整理为可落地的需求蓝图，聚焦命名规范、坐标系、核心数据模型与 API 对齐，便于后续开发、验收与上线工作。

## 1) 设计原则
- camelCase 字段命名，实体名采用 CamelCase；单数实体名与端点集合名区分清晰。
- 坐标系统一为 CGCS2000（大地2000），地理字段 location 使用 GEOMETRY(POINT, CGCS2000)。
- 数据模型应具备清晰外键、约束、索引与枚举字段。

## 2) 模块与功能清单
- 三维场景展示与数据可视化
- 基础信息与监测点管理
- 安全监管工作流（履职、鉴定、养护、隐患闭环、年报）
- 整编分析与可视化（误差识别、数据特征、过程线、布置图、分布图、相关图等）
- 在线监控预警与智能巡更（多级阈值、告警、巡查路线、移动端打卡、隐患闭环）
- 预测/会商与预案（模型管理、因子管理、预测输出、演练记录、预案版本化、滚动优化）
- 报表与文档管理（日/周/月报、模板、分发）
- 与其他系统的一体化工作流（水文调度、应急资源等）
- 安全与运维基础设施（基线、密钥管理、数据脱敏、日志审计、CI/CD 安全落地）

## 3) 核心数据模型草案（核心实体 camelCase）
- Dam
  - damId: UUID
  - name: string
  - location: GEOMETRY(POINT, CGCS2000)
  - type: string
  - designParameters: JSON
  - status: string
  - createdAt: TIMESTAMP
  - updatedAt: TIMESTAMP
- MonitoringPoint
  - pointId: UUID
  - damId: UUID (FK -> Dam.damId)
  - name: string
  - location: GEOMETRY(POINT, CGCS2000)
  - pointType: string
  - sensorId: UUID
  - status: string
  - lastValue: float
  - unit: string
  - createdAt: TIMESTAMP
  - updatedAt: TIMESTAMP
- Sensor
  - sensorId: UUID
  - type: string
  - model: string
  - unit: string
  - samplingRate: float
  - accuracy: float
  - status: string
  - installedAt: TIMESTAMP
  - removedAt: TIMESTAMP NULL
- Timeseries
  - tsId: UUID
  - pointId: UUID (FK -> MonitoringPoint.pointId)
  - timestamp: TIMESTAMP
  - value: float
- Alarm
  - alarmId: UUID
  - damId: UUID (FK -> Dam.damId) NULL
  - pointId: UUID (FK -> MonitoringPoint.pointId) NULL
  - level: string
  - message: string
  - createdAt: TIMESTAMP
  - acknowledgedAt: TIMESTAMP NULL
  - resolvedAt: TIMESTAMP NULL
  - status: string
- PatrolRoute
  - routeId: UUID
  - damId: UUID (FK)
  - name: string
  - path: JSON (GeoJSON)
  - createdAt: TIMESTAMP
  - updatedAt: TIMESTAMP
- HazardRecord
  - hazardId: UUID
  - damId: UUID (FK)
  - description: TEXT
  - severity: string
  - status: string
  - reportedAt: TIMESTAMP
  - dueAt: TIMESTAMP
  - closedAt: TIMESTAMP NULL
- RectificationTask
  - taskId: UUID
  - hazardId: UUID (FK)
  - description: TEXT
  - responsible: string
  - status: string
  - createdAt: TIMESTAMP
  - dueDate: TIMESTAMP
  - closedAt: TIMESTAMP NULL
- Model
  - modelId: UUID
  - name: string
  - version: string
  - description: TEXT
  - factors: JSON
  - status: string
  - lastTrainedAt: TIMESTAMP
- Prediction
  - predictionId: UUID
  - modelId: UUID (FK)
  - timestamp: TIMESTAMP
  - forecastValues: JSON
  - confidence: float
- Plan
  - planId: UUID
  - damId: UUID (FK)
  - version: string
  - description: TEXT
  - createdAt: TIMESTAMP
  - updatedAt: TIMESTAMP
  - status: string
- DrillRecord
  - drillId: UUID
  - planId: UUID (FK)
  - time: TIMESTAMP
  - participants: JSON
  - results: JSON
- Report
  - reportId: UUID
  - damId: UUID (FK)
  - type: string
  - date: DATE
  - content: JSON
  - generatedAt: TIMESTAMP
- Document
  - docId: UUID
  - type: string
  - title: string
  - content: TEXT
  - attachments: JSON

## 4) API 端点草案示例
- Base 路径：/api/v1
- dam（坝体/水库信息）
  - GET /dams
  - POST /dams
  - GET /dams/{damId}
  - PUT /dams/{damId}
  - DELETE /dams/{damId}
- dam/{damId}/monitoringPoints
  - GET /dams/{damId}/monitoringPoints
  - POST /dams/{damId}/monitoringPoints
- monitoringPoints/{pointId}/timeseries
  - GET /monitoringPoints/{pointId}/timeseries?start=...&end=...
- timeseries
  - POST /timeseries
- alarms
  - GET /alarms?damId=...&level=...&status=...
  - POST /alarms
  - POST /alarms/{alarmId}/resolve
- patrolRoutes
  - GET /patrolRoutes
  - POST /patrolRoutes
- models
  - GET /models
  - POST /models
  - GET /models/{modelId}
  - POST /models/{modelId}/train
- predictions
  - GET /predictions
  - POST /predictions
- plans
  - GET /plans
  - POST /plans
- drills
  - GET /drills
  - POST /drills
- reports
  - GET /reports
  - POST /reports/generate
- documents
  - GET /documents
  - POST /documents
- system-audit
  - GET /audit/logs

以下为示例请求/响应（简化）
Request: POST /api/v1/dams
```json
{
  "name": "Example Reservoir",
  "location": { "type": "Point", "coordinates": [120.0, 30.0] },
  "type": "拦洪坝",
  "designParameters": { "design_height_m": 60, "storage_capacity_m3": 10000000 }
}
```
Response:
```json
{ "damId": "uuid", "name": "Example Reservoir", "createdAt": "2026-02-24T12:00:00Z" }
```

（注：以上端点示例仅为草案，实际接口需对齐后端实现，并补充错误码、分页、排序、过滤等细节。）

## 4) MVP 与迭代时间线
 MVP1（第1–2周）：
  - 完成核心数据模型骨架与 DB 初始化脚本
  - 实现 /dams 与 /monitoringPoints 的增删改查
  - 完成 Timeseries 的数据接入占位与简单查询
  - 搭建 JWT/RBAC 初始鉴权
  - 3D 场景占位与前端骨架（不绑定真实数据）
 MVP2（第3–4周）：
  - 实现 3D 场景与监测数据的实时绑定
  - 实现告警产生、告警面板、基本巡查路线
  - 完成报表模板的框架和日/周/月报的导出样例
 MVP3（第5–6周）：
  - 完成预测/会商模型的版本化框架、演练记录与预案滚动优化
  - 跨系统工作流对接示例、数据字典与 API 补充
  - 完整的端到端测试用例与验收用例

## 5) 验证与测试用例设计
- 为各核心模块编写单元测试、集成测试与端到端测试用例框架。
- 覆盖数据正确性、接口稳定性、告警正确性、以及 3D 渲染性能的基线测试。

## 6) 文档与上线准备
- 使用文档、部署文档、API 文档、用户手册等整理。
- 准备演示用例、验收材料与上线回滚方案。

## 7) 里程碑与交付
- MVP1: 核心数据模型、基础 API、3D 场景占位、鉴权、数据接入占位
- MVP2: 3D 实时绑定、告警、巡查路线、报表样例
- MVP3: 预测/会商/预案、跨系统工作流、完整测试集合

(End of file)
