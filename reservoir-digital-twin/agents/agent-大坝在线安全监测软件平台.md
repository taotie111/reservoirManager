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

## 8) Frontend 实现计划（Next.js MVP 版本）

### 8.1 技术栈
- 前端框架：Next.js 14 (App Router)
- 开发语言：TypeScript
- 样式方案：纯 CSS + CSS Variables（支持 Light/Dark 主题）
- 状态管理：Zustand
- 数据请求：SWR + Fetch
- 图表库：ECharts / 自定义 SVG 图表
- 地图/3D：CesiumJS / Three.js（预留占位）

### 8.2 页面结构
```
app/
├── layout.tsx              # 根布局（App Shell）
├── components/
│   ├── Sidebar.tsx        # 左侧导航栏
│   ├── Header.tsx          # 顶部栏
│   ├── ThemeToggle.tsx    # 主题切换
│   ├── Card.tsx           # 卡片组件
│   └── TimeSeriesChart.tsx # 时序图表
├── styles/
│   └── ui.css             # 全局样式系统
├── dams/
│   ├── page.tsx           # 水库大坝列表
│   └── [damId]/page.tsx  # 水库详情
├── dashboard/page.tsx     # 数据看板
├── alerts/page.tsx        # 告警中心
├── forecasts/page.tsx     # 预测分析
├── admin/page.tsx         # 系统管理
└── api/                   # API 路由
```

### 8.3 UI 设计系统

#### 颜色主题（Light）
- 主色：#2563eb（蓝色）
- 背景：#f6f7fb
- 卡片：#ffffff
- 边框：#e5e7eb
- 文字：#374151
- 文字次要：#6b7280

#### 颜色主题（Dark）
- 背景：#0b1020
- 卡片：#141a2b
- 边框：#2f3656
- 文字：#e5e7eb
- 文字次要：#8b92a6

#### 组件规范
- 卡片圆角：12px
- 按钮圆角：6-8px
- 间距单位：4px 基础倍数
- 阴影：柔和投影

### 8.4 导航结构
- 左侧 Sidebar：品牌区域 + 导航菜单
  - 品牌：水库大坝安全监测 + 数字孪生平台
  - 导航项：水库大坝、数据看板、告警中心、预测分析、系统管理
- 顶部 Header：仅保留主题切换按钮

### 8.5 数据契约
- API 端点：/api/dams（GET）
- 数据格式：JSON，与数据字典字段一致（camelCase）
- 坐标系：CGCS2000

### 8.6 里程碑
- MVP1：完成基础框架、水库列表、主题切换
- MVP2：数据看板、告警中心、预测分析页面
- MVP3：3D 地图集成、实时数据绑定

(End of file)
