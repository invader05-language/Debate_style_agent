# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-06-03

### Added

**执行引擎完善 (Feature 1)**
- `execution/code_generator.py`: AI 代码生成器，将 action_plan 转化为可执行代码
- `execution/sandbox.py`: Docker 沙箱执行器，安全隔离执行环境
- `docker/sandbox/`: Python 和 Node.js 沙箱 Dockerfile
- 执行 API 增强：`/generate-code` 端点、`/retry` 端点、自动重试逻辑

**测试覆盖率提升 (Feature 2)**
- `tests/conftest.py`: 测试基础设施和公共 fixtures
- `tests/test_agents.py`: Agent 单元测试
- `tests/test_debate_integration.py`: 辩论集成测试
- `tests/test_websocket.py`: WebSocket 测试
- `pytest.ini`: pytest 配置

**错误处理优化 (Feature 3)**
- `exceptions.py`: 统一错误类型体系 (AgentError, ExecutionError, ValidationError 等)
- `backend/middleware.py`: 全局错误处理中间件 + Request ID 注入 + 滑动窗口限流
- `backend/logging_config.py`: JSON 格式结构化日志
- `agents/fallback.py`: Agent 降级策略，自动切换备用 Agent

**Docker 配置 (Feature 4)**
- `Dockerfile`: 后端多阶段构建
- `frontend/Dockerfile`: 前端构建 (Node → Nginx)
- `frontend/nginx.conf`: Nginx 配置 (SPA 路由, API/WebSocket 代理)
- `docker-compose.yml`: 服务编排 (backend, frontend, PostgreSQL+pgvector, Redis)
- `scripts/init-db.sql`: 数据库初始化脚本
- `Makefile`: 常用命令快捷方式

**文档完善 (Feature 5)**
- `README.md`: 项目主文档
- `docs/deployment.md`: 部署指南
- `docs/development.md`: 开发指南
- `docs/architecture.md`: 架构文档
- `CHANGELOG.md`: 变更日志

### Fixed

- `requirements.txt`: 补全缺失依赖 (fastapi, uvicorn, asyncpg, websockets)
- WebSocket 广播函数接入辩论引擎，实时消息推送正常工作
- 移除前端未使用的 `socket.io-client` 依赖
- 删除重复的 `prompts/templates.py` (与 `debate/roles.py` 重复)

## [0.1.0] - 2026-06-03

### Added

- 初始版本：CLI 辩论 MVP
- 辩论引擎核心 (MIMO + DeepSeek)
- FastAPI 后端 + WebSocket
- React 前端框架
- PostgreSQL 记忆系统
