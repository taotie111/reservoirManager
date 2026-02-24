# 大坝在线安全监测软件平台 - 核心大纲

此文档聚焦实现层面的核心大纲，确保命名规范、坐标系以及模块化落地的一致性，作为后续需求草案、数据字典与 API 契约对齐的基线。

## 1) 目标与范围
- 架构一个可落地的监测平台，覆盖数据接入、可视化、告警、巡检、会商、预案与跨系统对接的 MVP。
- 坐标系统一为 CGCS2000，大地2000；地理字段采用 location: GEOMETRY(POINT, CGCS2000)。

## 2) 命名规范
- 实体名：CamelCase（单数）如 Dam、MonitoringPoint、Sensor、Timeseries、Alarm、PatrolRoute、HazardRecord、RectificationTask、Model、Prediction、Plan、DrillRecord、Report、Document、UserRolePermission。
- 端点集合名：Dam、MonitoringPoints 等复数形式，如 /dams、/monitoringPoints、/timeseries、/alarms、/patrolRoutes 等。
- 字段名：camelCase，如 damId、monitoringPointId、location、designParameters、createdAt、updatedAt。
- 地理字段：location: GEOMETRY(POINT, CGCS2000)。

## 3) 坐标系
- CGCS2000（大地2000）为统一的地理坐标系，全球适用，地理字段均使用该坐标系。

## 4) 核心模块与数据流
- Dam、MonitoringPoint、Sensor、Timeseries、Alarm、PatrolRoute、HazardRecord、RectificationTask、Model、Prediction、Plan、DrillRecord、Report、Document、UserRolePermission
- 数据流简述：数据接入 → 建模/存储 → 可视化与告警 → 巡查/演练 → 预测/预案/跨系统对接

## 5) MVP 路线
- MVP1：核心数据模型骨架、/dams 与 /monitoringPoints 的增删改查、Timeseries 入库占位、初版 JWT/RBAC、3D 场景占位
- MVP2：3D 数据绑定、告警面板、巡查路线、报表样例
- MVP3：预测/会商/预案、跨系统工作流、端到端测试集合

## 6) 验证与落地
- 验证点：数据绑定有效性、告警规则、巡查路线、隐患闭环、3D 渲染性能、报表正确性
- 落地建议：对接监测数据源，逐步替换占位组件为真实数据绑定控件；上线回滚与变更管理

## 7) 附录
- 术语表、坐标系与地理信息标准参考

(End of file)
