# 大坝在线安全监测软件平台 - 数据字典初稿 v0.3

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

## 16) Frontend/UI 映射字段

### 16.1 通用 UI 字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| displayName | string | UI 展示的友好名称 |
| uiColor | string | 卡片、图表、点位的颜色 |
| isActive | boolean | 是否激活显示 |
| lastValue | number | 来自 Timeseries 的最近值 |
| coordinatesFormat | string | 坐标展示格式 |

### 16.2 前端组件映射

#### Dam 实体前端映射
```
Dam 列表页卡片显示：
- name (displayName) -> 卡片标题
- damId -> 坝体编号
- location -> 地理位置（CGCS2000 格式化显示）
- type -> 水库类型
- status -> 运行状态（对应 badge 颜色）
```

#### MonitoringPoint 实体前端映射
```
监测点卡片显示：
- name -> 点位名称
- pointType -> 点位类型
- lastValue -> 当前值 + 单位
- status -> 状态 badge
- sensorId -> 关联传感器
```

#### Alarm 实体前端映射
```
告警列表显示：
- level -> 告警级别（critical/warning/info）
- message -> 告警消息
- damId -> 关联水库
- pointId -> 关联监测点
- createdAt -> 告警时间
- status -> 处理状态
```

### 16.3 状态映射表

#### Dam Status 映射
| 后端值 | 前端显示 | Badge 样式 |
|--------|----------|------------|
| 正常 | 正常 | badge-success |
| 运行中 | 运行中 | badge-success |
| 维护中 | 维护中 | badge-warning |
| 异常 | 异常 | badge-error |

#### Alarm Level 映射
| 后端值 | 前端显示 | Badge 样式 |
|--------|----------|------------|
| critical | 紧急 | badge-error |
| warning | 警告 | badge-warning |
| info | 提示 | badge-success |

### 16.4 坐标系显示规范
- 存储格式：GEOMETRY(POINT, CGCS2000)
- 前端显示：经度.toFixed(4) + "°, " + 纬度.toFixed(4) + "°"
- 示例：102.0000°, 30.0000°

## 17) API 端点与数据流

### 17.1 前端 API 路由
```
GET  /api/dams           -> 获取水库列表
GET  /api/dams/[id]      -> 获取水库详情
GET  /api/monitoringPoints -> 获取监测点列表
GET  /api/timeseries     -> 获取时序数据
GET  /api/alerts         -> 获取告警列表
```

### 17.2 数据流向
```
后端数据库 -> API 路由 -> 前端 SWR/Fetch -> UI 组件
                                    ↓
                              状态管理 (Zustand)
                                    ↓
                              本地缓存 / LocalStorage
```

(End of file)
