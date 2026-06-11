# Multi-AI Debate Agent

辩论式多AI协作系统 — 多个 AI 模型针对给定主题进行正反方辩论，最终由裁判综合双方观点给出结构化建议和执行方案。

## 功能特性

- **多模型辩论**: MIMO 和 DeepSeek 分别扮演正方、反方、裁判
- **实时更新**: WebSocket 推送辩论过程中的每条消息
- **记忆系统**: PostgreSQL + pgvector 语义搜索，自动保存辩论经验
- **代码执行**: 从辩论结果自动生成代码并在 Docker 沙箱中安全执行
- **自动修复**: 执行失败时 AI 自动分析错误并重试，最多 3 次
- **Web 界面**: React + TypeScript 前端，支持辩论创建、历史查看、记忆搜索

## 技术栈

- **后端**: Python 3.11, FastAPI, SQLAlchemy, Redis
- **前端**: React 18, TypeScript, Tailwind CSS
- **数据库**: PostgreSQL + pgvector, Redis
- **AI**: MIMO, DeepSeek (通过 HTTP API)
- **部署**: Docker, Docker Compose

## 快速开始

### Docker 方式（推荐）

```bash
# 克隆仓库
git clone https://github.com/invader05-language/Debate_style_agent.git
cd Debate_style_agent

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 MIMO_API_KEY 和 DEEPSEEK_API_KEY

# 启动所有服务
docker-compose up -d

# 访问
# 前端: http://localhost:3000
# API: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 手动方式

```bash
# 后端
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload

# 前端
cd frontend
npm install
npm start
```

## 架构概览

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   React 前端  │────→│  FastAPI 后端  │────→│  PostgreSQL  │
│   (端口 3000) │     │   (端口 8000)  │     │   + pgvector │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                     │
       │ WebSocket          │ AI Agents            │ Redis 缓存
       ↓                    ↓                     ↓
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  实时消息推送  │     │ MIMO/DeepSeek │     │   记忆搜索    │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ↓
                     ┌──────────────┐
                     │  执行引擎     │
                     │  代码生成     │
                     │  Docker 沙箱  │
                     │  自动修复     │
                     └──────────────┘
```

### 执行引擎流程

辩论完成 → 提取 action\_plan → AI 生成代码 → Docker 沙箱执行
↓ (失败)
AI 分析错误 → 修复代码 → 重试 (最多 3 次)

## 配置说明

| 环境变量                | 说明               | 默认值                                                          |
| ------------------- | ---------------- | ------------------------------------------------------------ |
| `DATABASE_URL`      | PostgreSQL 连接字符串 | `postgresql://postgres:postgres@localhost:5432/debate_agent` |
| `REDIS_URL`         | Redis 连接字符串      | `redis://localhost:6379/0`                                   |
| `MIMO_API_KEY`      | MIMO API 密钥      | 必填                                                           |
| `MIMO_API_URL`      | MIMO API 地址      | `https://api.mimo.com/v1`                                    |
| `DEEPSEEK_API_KEY`  | DeepSeek API 密钥  | 必填                                                           |
| `DEEPSEEK_API_URL`  | DeepSeek API 地址  | `https://api.deepseek.com/v1`                                |
| `MAX_DEBATE_ROUNDS` | 最大辩论轮数           | `3`                                                          |
| `DEBATE_TIMEOUT`    | 辩论超时（秒）          | `300`                                                        |

## API 文档

启动后端后访问：

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

### 主要 API 端点

| 方法   | 路径                              | 说明         |
| ---- | ------------------------------- | ---------- |
| POST | /api/debates                    | 创建辩论       |
| GET  | /api/debates                    | 辩论列表（分页）   |
| GET  | /api/debates/{id}               | 辩论详情       |
| POST | /api/debates/{id}/start         | 开始辩论       |
| POST | /api/debates/{id}/execute       | 执行方案（直接执行） |
| POST | /api/debates/{id}/generate-code | AI 生成代码并执行 |
| GET  | /api/debates/{id}/executions    | 辩论的执行记录列表  |
| GET  | /api/executions/{id}            | 执行结果详情     |
| POST | /api/executions/{id}/retry      | 重试失败的执行    |
| GET  | /api/memories                   | 记忆列表       |
| GET  | /api/memories/{id}              | 记忆详情       |
| GET  | /api/memories/search?q=         | 语义搜索记忆     |
| WS   | /ws/debate/{id}                 | 辩论实时消息推送   |

## 开发指南

```bash
# 运行测试
make test

# 代码检查
make lint

# 查看日志
make logs

# 数据库 Shell
make db-shell
```

## 项目结构

```
debate-agent/
├── agents/          # AI Agent 实现 (MIMO, DeepSeek)
├── debate/          # 辩论引擎核心 (protocol, roles, engine)
├── memory/          # 记忆系统 (PostgreSQL + pgvector)
├── execution/       # 执行引擎 (代码生成, Docker 沙箱)
├── backend/         # FastAPI 后端
│   ├── api/         # REST API 端点
│   ├── models/      # SQLAlchemy 数据模型
│   ├── schemas/     # Pydantic 验证模式
│   ├── services/    # 业务逻辑层
│   └── websocket/   # WebSocket 处理
├── frontend/        # React 前端
│   └── src/
│       ├── components/  # UI 组件
│       ├── pages/       # 页面
│       ├── hooks/       # 自定义 Hook
│       └── services/    # API 服务
├── tests/           # 测试
├── docs/            # 文档
├── docker/          # Docker 配置
└── scripts/         # 脚本
```

## 许可证

MIT 开源许可证
