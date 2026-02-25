# 快速启动指南

## 前置要求

- Python 3.11+
- Node.js 20+
- pnpm (推荐)
- Docker & Docker Compose (可选)

## 本地开发

### 1. 启动后端 API

```bash
cd reservoir-digital-twin/services/api

# 创建虚拟环境 (可选)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库和种子数据
python seeds/init_data.py

# 启动 API 服务
uvicorn main:app --reload --port 8000
```

API 服务将在 http://localhost:8000 运行

- API 文档: http://localhost:8000/docs
- OpenAPI: http://localhost:8000/openapi.json

### 2. 启动前端

```bash
cd reservoir-digital-twin/apps/frontend

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

前端将在 http://localhost:3000 运行

### 3. 使用 Docker 启动所有服务

```bash
cd reservoir-digital-twin/infra

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

服务端口:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## 登录信息

默认管理员账户:
- 用户名: `admin`
- 密码: `admin123`

## API 端点

### 水库大坝
- `GET /api/v1/dams` - 获取水库列表
- `GET /api/v1/dams/{id}` - 获取水库详情
- `POST /api/v1/dams` - 创建水库
- `PUT /api/v1/dams/{id}` - 更新水库
- `DELETE /api/v1/dams/{id}` - 删除水库

### 监测点
- `GET /api/v1/monitoring-points` - 获取监测点列表
- `GET /api/v1/dams/{damId}/monitoring-points` - 获取水库的监测点

### 告警
- `GET /api/v1/alarms` - 获取告警列表
- `POST /api/v1/alarms/{id}/acknowledge` - 确认告警
- `POST /api/v1/alarms/{id}/resolve` - 解决告警

### 认证
- `POST /api/v1/auth/login` - 登录获取 JWT token

## 技术栈

### 后端
- FastAPI
- SQLAlchemy
- PostgreSQL + PostGIS
- JWT/OAuth2

### 前端
- Next.js 14 (App Router)
- TypeScript
- CSS Variables (支持 Dark/Light 主题)

## 项目结构

```
reservoir-digital-twin/
├── apps/
│   └── frontend/          # Next.js 前端应用
├── services/
│   ├── api/               # FastAPI 后端服务
│   └── ml/                # ML 预测服务
├── infra/                 # 基础设施配置
│   └── docker-compose.yml
├── tests/                 # 测试文件
└── .github/
    └── workflows/         # CI/CD 配置
```
