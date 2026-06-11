# Changelog

All notable changes to this project will be documented in this file.

## [0.5.0] - 2026-06-04

### Added

**性能压测 (O1)**
- `tests/test_performance.py`: API 延迟基准测试（根端点 <50ms、创建辩论 <100ms）、50 并发请求压测、限流器检查速度、缓存性能

**CI/CD 流水线 (O2)**
- `.github/workflows/ci.yml`: GitHub Actions 配置，Ruff lint → 后端测试(PostgreSQL+pgvector+Redis) → 前端测试(tsc+lint+build) → Docker 构建

**Prometheus 监控 (O3)**
- `backend/metrics.py`: 14 个 Prometheus 指标（HTTP、辩论、AI Agent、记忆、执行、缓存、限流、WebSocket）
- `backend/metrics_middleware.py`: HTTP 请求指标自动采集中间件
- `backend/main.py`: 接入 metrics 中间件，新增 `/metrics` 端点，`/health` 端点增加 Redis 状态

**Grafana Dashboard (O4)**
- `monitoring/grafana-dashboard.json`: 14 个可视化面板（活跃辩论、WebSocket、请求速率、延迟、Agent、缓存、执行、限流）
- `monitoring/prometheus.yml`: Prometheus 抓取配置
- `monitoring/provisioning/datasources/prometheus.yml`: Grafana 数据源自动配置
- `docker-compose.yml`: 新增 Prometheus、Grafana、Redis Exporter 服务

**部署验证脚本 (O5)**
- `scripts/healthcheck.sh`: 全链路健康检查（后端/前端/API/Redis/Metrics）

### Changed

- `requirements.txt`: 新增 prometheus-client，flake8 替换为 ruff
- `docs/deployment.md`: 新增监控栈部署章节

## [0.4.0] - 2026-06-04

### Added

**Alembic 数据库迁移系统 (T1)**
- `alembic.ini`: Alembic 配置文件，PostgreSQL 连接，UTC 时区
- `alembic/env.py`: 异步迁移环境，自动导入所有模型，启用 pgvector 扩展
- `alembic/script.py.mako`: 迁移脚本模板
- `alembic/versions/2026_06_04_1200_001_initial_schema.py`: 初始迁移，创建 5 张表 (users, debates, messages, memories, executions)，HNSW 向量索引
- `scripts/migrate.py`: CLI 迁移管理工具 (upgrade/downgrade/revision/current/history/check)

**Docker 沙箱镜像增强 (T2)**
- `docker/sandbox/python.Dockerfile`: 增强 Python 沙箱，添加 gcc、pytest-cov、httpx、pydantic
- `docker/sandbox/node.Dockerfile`: 增强 Node 沙箱，添加 jest、typescript、ts-node

**前端 Nginx 安全加固 (T3)**
- `frontend/nginx.conf`: 添加安全头 (X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy)，/health 端点，WebSocket 86400s 超时，隐藏文件拒绝

**pgvector 语义搜索完善 (T4)**
- `memory/store.py`: 完整 pgvector 余弦相似度搜索，保存时自动生成 embedding，ILIKE 降级搜索

**Redis 缓存增强 (T5)**
- `backend/cache.py`: 添加 `health_check()` 返回 status/latency_ms/error，`flush_pattern()` 模式删除，`close()` 连接清理

**API 限流中间件完善 (T6)**
- `backend/middleware.py`: 增强 RateLimiter，支持 per-endpoint 限流配置，自动清理过期条目，X-RateLimit-Remaining/Limit 响应头

**Agent 降级策略测试 (T7)**
- `tests/test_agent_fallback.py`: 10 个测试用例，覆盖首选成功、降级切换、双失败异常、不健康跳过、恢复探测、失败计数、成功重置

**API 端点测试补全 (T8)**
- `tests/test_api.py`: 新增 12 个测试用例 (TestDebateAPIExtended, TestMemoryAPIExtended, TestAuthAPI)

**WebSocket 测试补全 (T9)**
- `tests/test_websocket.py`: 新增 3 个测试用例 (多房间广播隔离、空 debate ID、序列化异常处理)

**端到端集成测试 (T10)**
- `tests/test_e2e.py`: 完整流程测试 (创建→列表→查询、记忆创建→搜索、注册→登录、健康检查)

## [0.3.0] - 2026-06-04

### Added

**前端实时辩论界面增强 (Feature 8)**
- `frontend/src/components/RoundProgress.tsx`: 轮次进度条组件，支持当前轮次高亮、已完成轮次打勾、动画连接线
- `frontend/src/components/MessageBubble.tsx`: 增强消息气泡，添加角色头像、入场动画、优化布局
- `frontend/src/components/DebateView.tsx`: 增强辩论视图，添加轮次分隔器、消息入场动画、加载状态优化
- `frontend/src/components/VerdictCard.tsx`: 重构判决卡片，添加渐变头部、编号步骤、优化按钮布局
- `frontend/src/components/ExecutionPanel.tsx`: 重构执行面板，添加状态图标、优化代码展示区域
- `frontend/src/pages/DebatePage.tsx`: 集成轮次进度条、WebSocket 连接状态栏、键盘回车提交、优化整体布局
- `frontend/src/App.tsx`: 重构导航栏，添加图标、路由高亮、粘性定位
- `frontend/src/index.css`: 自定义动画 (fadeInUp, slideInLeft, slideInRight, pulse-ring)、轮次连接线样式

**JWT 认证机制 (Feature 6)**
- `backend/models/user.py`: 用户模型 (UserModel)，支持用户名、邮箱、密码哈希
- `backend/auth.py`: JWT 认证依赖，包含密码哈希、Token 生成/验证、`get_current_user` 依赖注入
- `backend/api/auth.py`: 认证 API 端点 (`/api/auth/register`, `/api/auth/login`, `/api/auth/me`)
- `backend/schemas/auth.py`: 认证 Pydantic 模型 (UserCreate, UserLogin, UserResponse, TokenResponse)
- `backend/config.py`: 新增 JWT 配置 (JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES)
- `requirements.txt`: 新增 PyJWT, passlib, bcrypt 依赖

**pgvector 语义搜索 (Feature 7)**
- `backend/models/memory.py`: 新增 `embedding` 列 (Vector(1024))，使用 pgvector 扩展
- `backend/services/embedding_service.py`: MIMO API 嵌入服务，支持单文本和批量嵌入生成
- `backend/services/memory_service.py`: 升级搜索方法，优先使用 pgvector 余弦相似度搜索，降级到 ILIKE 文本搜索
- `backend/api/memory.py`: 新增语义搜索支持 (`use_semantic` 参数)、`/memories/{id}/generate-embedding` 端点、`/memories/generate-all-embeddings` 批量端点
- `backend/database.py`: 初始化时自动启用 pgvector 扩展 (`CREATE EXTENSION IF NOT EXISTS vector`)
- `backend/config.py`: 新增 MIMO_API_KEY, MIMO_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_API_URL 配置
- `requirements.txt`: 新增 pgvector 依赖

## [0.2.0] - 2026-06-03

### Added

**执行引擎完善 (Feature 1)**
- `execution/code_generator.py`: AI 代码生成器，将 action_plan 转化为可执行代码
- `execution/executor.py`: 集成 CodeGenerator + DockerSandbox/FallbackSandbox 的统一执行器
- `execution/sandbox.py`: Docker 沙箱执行器 + FallbackSandbox 本地降级方案
- `execution/__init__.py`: 统一导出 CodeExecutor, CodeGenerator, GeneratedCode 等
- `CodeExecutor.generate_and_execute()`: 代码生成 → 沙箱执行 → AI 修复自动重试
- `CodeExecutor.run_tests()`: 代码 + 测试一体化执行
- `FallbackSandbox.execute_with_tests()`: 本地执行器测试支持
- 执行 API 增强：`/generate-code` 端点、`/retry` 端点、自动重试逻辑

**测试覆盖率提升 (Feature 2)**
- `tests/test_agents.py`: Agent 单元测试 (MIMO, DeepSeek, fallback)
- `tests/test_debate_integration.py`: 辩论集成测试
- `tests/test_websocket.py`: WebSocket 测试
- `tests/test_code_generator.py`: 代码生成器测试 (11 tests, JSON 解析/降级/错误处理)
- `tests/test_sandbox.py`: 沙箱执行器测试 (14 tests, DockerSandbox + FallbackSandbox)
- `tests/test_executor.py`: 执行器集成测试 (16 tests, generate_and_execute/retry/run_tests)
- `tests/test_memory.py`: 记忆系统测试 (13 tests, save/search/get_by_topic/get_relevant)
- `tests/test_api.py`: API 端点测试 (16 tests, 辩论/执行/记忆全端点覆盖)
- `pytest.ini`: pytest 配置
- 总计 113 个测试全部通过

**错误处理优化 (Feature 3)**
- `exceptions.py`: 统一错误类型体系 (AgentError, ExecutionError, ValidationError 等)
- `backend/middleware.py`: 全局错误处理中间件 + Request ID 注入 + 滑动窗口限流
- `backend/logging_config.py`: JSON 格式结构化日志
- `agents/fallback.py`: Agent 降级策略，自动切换备用 Agent

**Docker 配置 (Feature 4)**
- `Dockerfile`: 后端多阶段构建，非 root 用户，健康检查
- `frontend/Dockerfile`: 前端构建 (Node → Nginx)
- `frontend/nginx.conf`: Nginx 配置 (SPA 路由, API/WebSocket 代理, 静态资源缓存)
- `docker-compose.yml`: 服务编排 (backend, frontend, PostgreSQL+pgvector, Redis)
- `.dockerignore`: 构建排除规则
- `.env.example`: 环境变量模板
- `scripts/init-db.sql`: 数据库初始化脚本 (pgvector, 4 张表, 索引)
- `Makefile`: 常用命令快捷方式

**文档完善 (Feature 5)**
- `README.md`: 项目主文档 (功能特性、快速开始、架构概览、API 文档)
- `docs/deployment.md`: 部署指南 (Docker/手动/生产环境)
- `docs/development.md`: 开发指南 (环境搭建、代码规范、测试、调试)
- `docs/architecture.md`: 架构文档 (系统架构图、模块说明、数据库设计、API 设计)
- `CHANGELOG.md`: 变更日志

### Fixed

- `requirements.txt`: 补全缺失依赖 (fastapi, uvicorn, asyncpg, websockets)
- WebSocket 广播函数接入辩论引擎，实时消息推送正常工作
- 移除前端未使用的 `socket.io-client` 依赖
- 删除重复的 `prompts/templates.py` (与 `debate/roles.py` 重复)
- `backend/api/execution.py`: 修复后台任务 `SessionLocal` 导入错误，改用 `AsyncSessionLocal`

## [0.1.0] - 2026-06-03

### Added

- 初始版本：CLI 辩论 MVP
- 辩论引擎核心 (MIMO + DeepSeek)
- FastAPI 后端 + WebSocket
- React 前端框架
- PostgreSQL 记忆系统
