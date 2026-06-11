# Multi-AI Debate Agent - 剩余功能详细实现计划

> 版本: 1.0 | 日期: 2026-06-03
> 状态: 待执行
> 关联仓库: https://github.com/invader05-language/Debate_style_agent

---

## 一、当前项目状态总结

| 模块 | 完成度 | 说明 |
|------|--------|------|
| 辩论引擎核心 | 80% | protocol/roles/engine 已实现，缺集成测试和错误恢复 |
| AI Agent 对接 | 70% | MIMO/DeepSeek 已实现，缺降级策略和响应解析健壮性 |
| 记忆系统 | 60% | PostgreSQL 存储已实现，缺语义搜索(pgvector)和 Redis 缓存 |
| 执行引擎 | 40% | 基础 subprocess 执行已有，缺沙箱隔离、代码生成、测试运行 |
| 后端 API | 65% | REST + WebSocket 框架已有，缺错误处理中间件、认证、限流 |
| 前端 | 50% | React 组件框架已有，缺实时辩论界面、执行结果展示 |
| 测试 | 25% | 仅基础单元测试，无集成测试、无 API 测试、无性能测试 |
| Docker | 0% | 无 Dockerfile、无 docker-compose |
| 文档 | 20% | 有设计文档，缺 API 文档、部署文档、用户手册 |

---

## 二、Feature 1: 执行引擎完善

### 2.1 设计思路

执行引擎的目标是将辩论产生的 `action_plan` 转化为可运行的代码，并在安全沙箱中执行验证。当前的 `CodeExecutor` 只有基础的 subprocess 调用，存在以下问题：

1. **无代码生成能力**: 直接执行 action_plan 文本，而非生成结构化代码
2. **无沙箱隔离**: 直接在宿主机执行，有安全风险
3. **无测试运行**: 执行后不验证结果正确性
4. **无多语言支持**: 仅支持 Python/JS 的简单 subprocess

设计方向：引入 Docker 作为沙箱，使用 AI 生成代码 + 自动测试的流水线。

### 2.2 当前代码分析

```
execution/executor.py
├── ExecutionResult (数据类) - OK
├── CodeExecutor
│   ├── execute_python() - 基础可用，缺沙箱
│   ├── execute_javascript() - 基础可用，缺沙箱
│   └── execute() - 路由分发，缺代码生成
└── 问题:
    ├── 直接 subprocess 无隔离
    ├── 无 code_generation() 方法
    ├── 无 run_tests() 方法
    └── 无 Docker 沙箱支持
```

### 2.3 实现步骤

#### Step 1: 添加代码生成器 (execution/code_generator.py) [新建]

```
功能: 调用 AI 将 action_plan 转化为结构化代码
输入: action_plan: List[str], language: str
输出: GeneratedCode { main_code, test_code, dependencies }

实现要点:
- 使用 MIMOAgent 或 DeepSeekAgent 的 chat 方法
- Prompt 模板: "根据以下行动方案生成 {language} 代码和单元测试"
- 返回结构化的代码和测试代码
- 支持 Python / JavaScript / TypeScript
```

**类设计:**
```python
class CodeGenerator:
    """将辩论的 action_plan 转化为可执行代码"""

    def __init__(self, agent: BaseAgent):
        self.agent = agent

    async def generate(self, action_plan: List[str],
                       language: str = "python") -> GeneratedCode:
        """生成代码和测试"""
        # 1. 构建 prompt
        # 2. 调用 AI 生成代码
        # 3. 解析返回的 JSON (main_code, test_code, deps)
        # 4. 验证代码语法 (ast.parse / esprima)
        # 5. 返回 GeneratedCode

    async def refine(self, code: GeneratedCode,
                     error: str) -> GeneratedCode:
        """根据执行错误修复代码"""
        # 1. 将错误信息和原代码发给 AI
        # 2. AI 返回修复后的代码
        # 3. 重新验证语法
```

**依赖:** 无新增外部依赖

#### Step 2: Docker 沙箱执行器 (execution/sandbox.py) [新建]

```
功能: 在 Docker 容器中安全执行代码
输入: code: str, language: str, timeout: int
输出: ExecutionResult

安全约束:
- 只读文件系统 (tmpfs 可写 /tmp)
- 无网络访问 (--network none)
- 内存限制 (默认 256MB)
- CPU 限制 (默认 0.5 核)
- 执行超时 (默认 30s)
- 非 root 用户运行
```

**类设计:**
```python
class DockerSandbox:
    """Docker 容器沙箱执行器"""

    # 预构建的执行镜像
    IMAGES = {
        "python": "debate-agent/python-sandbox:3.11",
        "javascript": "debate-agent/node-sandbox:20",
    }

    def __init__(self, timeout: int = 30, memory_limit: str = "256m",
                 cpu_limit: float = 0.5):
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit

    async def execute(self, code: str, language: str = "python") -> ExecutionResult:
        """在 Docker 容器中执行代码"""
        # 1. 写入临时文件
        # 2. 构建 docker run 命令 (带安全约束)
        # 3. 执行并捕获输出
        # 4. 处理超时
        # 5. 清理容器
        # 6. 返回 ExecutionResult

    async def execute_with_tests(self, code: str, test_code: str,
                                  language: str = "python") -> TestResult:
        """执行代码并运行测试"""
        # 1. 先执行主代码
        # 2. 如果成功，执行测试代码
        # 3. 解析测试结果 (pytest --tb=short --json-report)
        # 4. 返回 TestResult { passed, failed, errors, coverage }
```

**Docker 镜像构建 (docker/sandbox/):**
```dockerfile
# docker/sandbox/python.Dockerfile
FROM python:3.11-slim
RUN useradd -m sandbox
USER sandbox
WORKDIR /app
# 预装常用库
RUN pip install --no-cache-dir pytest requests numpy pandas
```

```dockerfile
# docker/sandbox/node.Dockerfile
FROM node:20-slim
RUN useradd -m sandbox
USER sandbox
WORKDIR /app
```

**依赖:** Docker Engine (开发/部署环境)

#### Step 3: 增强 CodeExecutor (execution/executor.py) [修改]

```
修改内容:
1. 添加 CodeGenerator 和 DockerSandbox 的集成
2. 添加 generate_and_execute() 方法 - 从 action_plan 生成代码并执行
3. 添加自动重试逻辑 - 代码执行失败时自动修复重试 (最多 3 次)
4. 保留原有的 execute_python/execute_javascript 作为 fallback
5. 添加执行记录持久化 (写入 executions 表)
```

**新增方法:**
```python
class CodeExecutor:
    def __init__(self, use_sandbox: bool = True):
        self.sandbox = DockerSandbox() if use_sandbox else None
        self.generator = None  # 延迟初始化

    async def generate_and_execute(
        self, action_plan: List[str], language: str = "python",
        max_retries: int = 3
    ) -> ExecutionResult:
        """从 action_plan 生成代码并执行，失败自动重试"""
        # 1. 生成代码
        # 2. 在沙箱中执行
        # 3. 如果失败且重试次数未用完，调用 refine 修复
        # 4. 循环直到成功或重试耗尽
        # 5. 记录执行历史

    async def run_tests(self, code: str, test_code: str,
                        language: str = "python") -> TestResult:
        """运行代码测试"""
```

#### Step 4: 执行 API 端点增强 (backend/api/execution.py) [修改]

```
修改内容:
1. 添加 POST /api/debates/{id}/generate-code - 从辩论结果生成代码
2. 修改 POST /api/debates/{id}/execute - 集成新的执行引擎
3. 添加 GET /api/executions/{id}/tests - 获取测试结果
4. 添加 POST /api/executions/{id}/retry - 手动重试执行
5. WebSocket 推送执行进度
```

### 2.4 文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `execution/code_generator.py` | 新建 | AI 代码生成器 |
| `execution/sandbox.py` | 新建 | Docker 沙箱执行器 |
| `execution/executor.py` | 修改 | 集成生成器和沙箱 |
| `execution/__init__.py` | 修改 | 导出新模块 |
| `backend/api/execution.py` | 修改 | 增强 API 端点 |
| `docker/sandbox/python.Dockerfile` | 新建 | Python 沙箱镜像 |
| `docker/sandbox/node.Dockerfile` | 新建 | Node.js 沙箱镜像 |
| `tests/test_code_generator.py` | 新建 | 代码生成器测试 |
| `tests/test_sandbox.py` | 新建 | 沙箱执行器测试 |

---

## 三、Feature 2: 测试覆盖率提升

### 3.1 设计思路

当前测试仅覆盖基础数据结构和初始化，缺乏：
- 辩论流程的集成测试（模拟完整的辩论流程）
- API 端点测试（HTTP 请求/响应）
- WebSocket 测试（实时消息推送）
- 数据库操作测试（CRUD + 查询）
- 错误场景测试（网络超时、模型异常、并发冲突）

目标：单元测试覆盖率 ≥ 80%，集成测试覆盖核心流程。

### 3.2 当前测试分析

```
tests/
├── test_debate.py (204 行)
│   ├── TestDebateProtocol - 7 个测试 ✅
│   ├── TestDebateRoles - 6 个测试 ✅
│   └── TestDebateEngine - 2 个测试 ⚠️ 缺集成测试
├── test_memory.py (42 行)
│   └── TestMemoryStore - 2 个测试 ⚠️ 缺数据库测试
├── test_executor.py (80 行)
│   ├── TestExecutionResult - 2 个测试 ✅
│   └── TestCodeExecutor - 3 个测试 ⚠️ 缺超时/JS测试
└── 问题:
    ├── 无 API 测试
    ├── 无 WebSocket 测试
    ├── 无 Agent 对接测试 (mock)
    ├── 无错误场景测试
    └── 无性能测试
```

### 3.3 实现步骤

#### Step 1: 测试基础设施 (tests/conftest.py) [新建/增强]

```python
"""测试配置和公共 fixtures"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport

# Fixtures:
# - mock_mimo_agent: Mock MIMOAgent (不真实调用 API)
# - mock_deepseek_agent: Mock DeepSeekAgent
# - mock_memory_store: Mock MemoryStore (内存数据库)
# - test_db: SQLite 内存数据库 (替代 PostgreSQL)
# - test_app: FastAPI 测试应用
# - async_client: httpx AsyncClient (用于 API 测试)
# - sample_debate_config: 标准辩论配置
# - sample_debate_result: 完整辩论结果
```

#### Step 2: Agent Mock 测试 (tests/test_agents.py) [新建]

```
测试用例:
- test_mimo_agent_chat_success: Mock API 返回成功
- test_mimo_agent_chat_retry: Mock API 失败后重试成功
- test_mimo_agent_chat_max_retries: Mock API 连续失败
- test_mimo_agent_chat_timeout: Mock API 超时
- test_mimo_agent_get_embedding: Mock embedding API
- test_deepseek_agent_chat_success: DeepSeek 对应测试
- test_agent_build_messages: 消息构建正确性
- test_agent_context_truncation: 上下文过长时截断
```

#### Step 3: 辩论集成测试 (tests/test_debate_integration.py) [新建]

```
测试用例:
- test_full_debate_flow: 完整辩论流程 (mock agents)
  → 验证: 正方发言 → 反方发言 → 裁判总结 → 最终裁决
- test_debate_early_consensus: 共识提前终止
- test_debate_agent_failure_recovery: 单个 agent 失败时的恢复
- test_debate_round_progression: 多轮辩论的消息累积
- test_debate_memory_integration: 记忆系统集成
- test_debate_verdict_json_parsing: 裁决 JSON 解析健壮性
- test_debate_verdict_fallback: 裁决解析失败时的降级
```

#### Step 4: 记忆系统测试 (tests/test_memory.py) [增强]

```
新增测试用例:
- test_save_memory_to_db: 保存到数据库 (使用 SQLite)
- test_search_memory_by_topic: 按主题搜索
- test_search_memory_by_content: 按内容搜索
- test_get_relevant_memories: 获取相关记忆
- test_get_relevant_deduplication: 记忆去重
- test_memory_pagination: 分页查询
- test_memory_concurrent_save: 并发保存
```

#### Step 5: API 端点测试 (tests/test_api.py) [新建/增强]

```
测试用例:
- test_create_debate: POST /api/debates
- test_get_debate: GET /api/debates/{id}
- test_list_debates: GET /api/debates (分页)
- test_create_debate_validation: 无效输入验证
- test_execute_debate: POST /api/debates/{id}/execute
- test_execute_not_completed: 未完成辩论的执行
- test_get_execution: GET /api/executions/{id}
- test_search_memories: GET /api/memories/search
- test_health_endpoint: GET /health
- test_cors_headers: CORS 头验证
- test_404_handling: 不存在资源的处理
- test_500_handling: 服务器错误处理
```

#### Step 6: WebSocket 测试 (tests/test_websocket.py) [新建]

```
测试用例:
- test_websocket_connect: 连接成功
- test_websocket_welcome_message: 欢迎消息
- test_websocket_ping_pong: 心跳机制
- test_websocket_broadcast: 消息广播
- test_websocket_disconnect_cleanup: 断开连接清理
- test_websocket_invalid_json: 无效 JSON 处理
- test_websocket_multiple_clients: 多客户端连接
```

#### Step 7: 执行引擎测试 (tests/test_executor.py) [增强]

```
新增测试用例:
- test_execute_python_timeout: Python 执行超时
- test_execute_javascript_hello: JS 执行成功
- test_execute_javascript_error: JS 执行失败
- test_execute_with_sandbox: 沙箱执行 (mock docker)
- test_generate_and_execute: 生成+执行流程
- test_generate_and_execute_retry: 生成失败重试
- test_code_generator: 代码生成器单元测试
```

### 3.4 测试运行配置

```ini
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --cov=. --cov-report=html --cov-report=term-missing
markers =
    asyncio: mark a test as an asyncio test
    integration: mark as integration test (slow)
    unit: mark as unit test (fast)
```

### 3.5 文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `tests/conftest.py` | 新建 | 测试配置和 fixtures |
| `tests/test_agents.py` | 新建 | Agent 单元测试 |
| `tests/test_debate_integration.py` | 新建 | 辩论集成测试 |
| `tests/test_memory.py` | 增强 | 记忆系统测试 |
| `tests/test_executor.py` | 增强 | 执行引擎测试 |
| `tests/test_api.py` | 新建 | API 端点测试 |
| `tests/test_websocket.py` | 新建 | WebSocket 测试 |
| `pytest.ini` | 新建 | pytest 配置 |

---

## 四、Feature 3: 错误处理优化

### 4.1 设计思路

当前错误处理分散在各模块中，缺乏统一的错误分类、上报和恢复机制。需要建立：

1. **统一错误分类**: 区分可重试错误 vs 不可重试错误
2. **全局错误处理中间件**: FastAPI 的异常处理器
3. **结构化错误响应**: 统一的 JSON 错误格式
4. **错误日志和监控**: 结构化日志 + 错误统计
5. **降级策略**: API 不可用时的 fallback

### 4.2 当前错误处理分析

```
已有:
├── BaseAgent._retry_with_backoff() - 指数退避重试 ✅
├── CodeExecutor 超时处理 - asyncio.wait_for ✅
└── WebSocket 断连处理 - WebSocketDisconnect ✅

缺失:
├── 无统一错误类型定义
├── 无 FastAPI 全局异常处理器
├── 无结构化错误响应格式
├── 无错误日志聚合
├── 无 API 限流
├── 无 Agent 降级策略 (MIMO 不可用时 fallback 到 DeepSeek)
└── 无数据库连接池错误处理
```

### 4.3 实现步骤

#### Step 1: 错误类型定义 (exceptions.py) [新建]

```python
"""统一错误类型定义"""

class DebateAgentError(Exception):
    """基础异常类"""
    code: str
    message: str
    status_code: int
    retryable: bool

class AgentError(DebateAgentError):
    """AI Agent 调用错误"""
    pass

class AgentTimeoutError(AgentError):
    """Agent 超时"""
    retryable = True

class AgentRateLimitError(AgentError):
    """Agent 限流"""
    retryable = True

class AgentAuthError(AgentError):
    """Agent 认证失败"""
    retryable = False

class ExecutionError(DebateAgentError):
    """代码执行错误"""
    pass

class SandboxError(ExecutionError):
    """沙箱执行错误"""
    pass

class ValidationError(DebateAgentError):
    """输入验证错误"""
    status_code = 422
    retryable = False

class NotFoundError(DebateAgentError):
    """资源不存在"""
    status_code = 404
    retryable = False

class ConflictError(DebateAgentError):
    """状态冲突"""
    status_code = 409
    retryable = False
```

#### Step 2: 全局错误处理中间件 (backend/middleware.py) [新建]

```python
"""FastAPI 全局错误处理中间件"""

from fastapi import Request
from fastapi.responses import JSONResponse

async def debate_agent_error_handler(request: Request, exc: DebateAgentError):
    """处理自定义业务异常"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "retryable": exc.retryable,
                "request_id": request.state.request_id,
            }
        }
    )

async def generic_error_handler(request: Request, exc: Exception):
    """处理未预期的异常"""
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "retryable": False,
                "request_id": request.state.request_id,
            }
        }
    )

# 中间件: 请求 ID 注入
async def request_id_middleware(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response
```

#### Step 3: Agent 降级策略 (agents/fallback.py) [新建]

```python
"""Agent 降级和负载均衡"""

class AgentFallback:
    """Agent 降级策略"""

    def __init__(self, agents: Dict[str, BaseAgent]):
        self.agents = agents
        self.health_status = {name: True for name in agents}
        self.failure_counts = {name: 0 for name in agents}

    async def chat(self, preferred: str, fallback: str, **kwargs) -> str:
        """带降级的 chat 调用"""
        # 1. 尝试首选 agent
        # 2. 如果失败，标记 unhealthy，切换到 fallback
        # 3. 如果 fallback 也失败，抛出异常
        # 4. 定期探测 unhealthy agent 是否恢复

    async def _probe_health(self, agent_name: str) -> bool:
        """探测 agent 健康状态"""
```

#### Step 4: 结构化日志 (backend/logging_config.py) [新建]

```python
"""结构化日志配置"""

import structlog

def setup_logging(log_level: str = "INFO"):
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

# 日志格式示例:
# {"event":"debate_started","debate_id":"abc-123","topic":"JWT vs Session","level":"info","timestamp":"2026-06-03T10:00:00Z"}
```

#### Step 5: API 限流 (backend/middleware.py) [扩展]

```python
"""API 限流中间件"""

from collections import defaultdict
import time

class RateLimiter:
    """基于滑动窗口的限流器"""

    def __init__(self, requests_per_minute: int = 60):
        self.rpm = requests_per_minute
        self.requests = defaultdict(list)  # ip -> [timestamps]

    async def check(self, client_ip: str) -> bool:
        """检查是否超过限流"""
        now = time.time()
        window_start = now - 60

        # 清理过期记录
        self.requests[client_ip] = [
            t for t in self.requests[client_ip] if t > window_start
        ]

        if len(self.requests[client_ip]) >= self.rpm:
            return False

        self.requests[client_ip].append(now)
        return True
```

#### Step 6: 集成到 main.py (backend/main.py) [修改]

```
修改内容:
1. 注册全局异常处理器
2. 添加 request_id 中间件
3. 添加限流中间件
4. 配置结构化日志
5. 添加 /metrics 端点 (错误统计)
```

### 4.4 文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `exceptions.py` | 新建 | 统一错误类型 |
| `backend/middleware.py` | 新建 | 错误处理 + 限流中间件 |
| `backend/logging_config.py` | 新建 | 结构化日志配置 |
| `agents/fallback.py` | 新建 | Agent 降级策略 |
| `backend/main.py` | 修改 | 集成中间件 |
| `tests/test_error_handling.py` | 新建 | 错误处理测试 |
| `tests/test_rate_limiter.py` | 新建 | 限流测试 |

---

## 五、Feature 4: Docker 配置

### 5.1 设计思路

提供一键启动的 Docker 环境，包含：
- 应用容器 (FastAPI backend)
- 前端容器 (React dev server)
- PostgreSQL 容器
- Redis 容器
- 沙箱执行容器 (可选)

### 5.2 实现步骤

#### Step 1: 后端 Dockerfile (Dockerfile) [新建]

```dockerfile
# 多阶段构建
FROM python:3.11-slim AS base

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 非 root 用户
RUN useradd -m appuser
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 2: 前端 Dockerfile (frontend/Dockerfile) [新建]

```dockerfile
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
```

#### Step 3: Docker Compose (docker-compose.yml) [新建]

```yaml
version: "3.9"

services:
  # 后端 API
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/debate_agent
      - REDIS_URL=redis://redis:6379/0
      - MIMO_API_KEY=${MIMO_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app/backend  # 开发模式热重载
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

  # 前端
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  # PostgreSQL
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: debate_agent
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  # (可选) 沙箱执行器
  sandbox:
    build:
      context: .
      dockerfile: docker/sandbox/python.Dockerfile
    privileged: false
    read_only: true
    mem_limit: 256m
    cpus: 0.5

volumes:
  pgdata:
  redisdata:
```

#### Step 4: 数据库初始化脚本 (scripts/init-db.sql) [新建]

```sql
-- 启用 pgvector 扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 创建表结构
-- (参考 technical-architecture-plan.md 中的 PostgreSQL schema)
CREATE TABLE IF NOT EXISTS debates (...);
CREATE TABLE IF NOT EXISTS messages (...);
CREATE TABLE IF NOT EXISTS memories (...);
CREATE TABLE IF NOT EXISTS executions (...);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_debates_status ON debates(status);
CREATE INDEX IF NOT EXISTS idx_messages_debate ON messages(debate_id);
CREATE INDEX IF NOT EXISTS idx_memories_topic ON memories USING gin(to_tsvector('chinese', topic));
```

#### Step 5: 环境配置 (.env.example 更新) [修改]

```
确保 .env.example 包含所有 Docker 相关配置:
- 各服务的端口映射
- 数据卷路径
- 日志级别
- 开发/生产模式切换
```

#### Step 6: Makefile (Makefile) [新建]

```makefile
# 常用命令快捷方式
.PHONY: up down build test lint

up:                    ## 启动所有服务
	docker-compose up -d

down:                  ## 停止所有服务
	docker-compose down

build:                 ## 构建所有镜像
	docker-compose build

test:                  ## 运行测试
	docker-compose exec backend pytest

lint:                  ## 代码检查
	docker-compose exec backend ruff check .

logs:                  ## 查看日志
	docker-compose logs -f backend

db-shell:              ## 进入数据库
	docker-compose exec db psql -U postgres debate_agent

redis-shell:           ## 进入 Redis
	docker-compose exec redis redis-cli
```

### 5.3 文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `Dockerfile` | 新建 | 后端多阶段构建 |
| `frontend/Dockerfile` | 新建 | 前端构建 |
| `frontend/nginx.conf` | 新建 | Nginx 配置 |
| `docker-compose.yml` | 新建 | 服务编排 |
| `docker/sandbox/python.Dockerfile` | 新建 | Python 沙箱镜像 |
| `docker/sandbox/node.Dockerfile` | 新建 | Node.js 沙箱镜像 |
| `scripts/init-db.sql` | 新建 | 数据库初始化 |
| `Makefile` | 新建 | 命令快捷方式 |
| `.dockerignore` | 新建 | Docker 忽略文件 |
| `requirements.txt` | 新建/确认 | Python 依赖清单 |

---

## 六、Feature 5: 文档完善

### 6.1 设计思路

文档分为三层：
1. **开发者文档**: API 参考、架构说明、贡献指南
2. **部署文档**: Docker 部署、手动部署、配置说明
3. **用户文档**: 快速开始、功能说明、FAQ

### 6.2 实现步骤

#### Step 1: 项目 README (README.md) [新建]

```
内容结构:
# Multi-AI Debate Agent
## 简介 (一句话说明)
## 功能特性
## 快速开始 (5 分钟跑起来)
  - Docker 方式 (推荐)
  - 手动方式
## 架构概览 (一张图)
## 配置说明
## API 文档 (链接到 /docs)
## 开发指南
  - 项目结构
  - 开发环境搭建
  - 运行测试
  - 代码规范
## 部署指南
## 常见问题
## 许可证
```

#### Step 2: API 文档自动生成 (FastAPI 自带) [增强]

```
修改内容:
1. 为所有 API 端点添加详细的 docstring
2. 添加 OpenAPI tags 描述
3. 添加请求/响应示例
4. 添加错误码说明
5. 确保 /docs 和 /redoc 可正常访问
```

**backend/api/debate.py 示例:**
```python
@router.post("/debates", response_model=DebateResponse,
    summary="创建新辩论",
    description="创建一个新的多AI辩论会话，指定辩题和参与模型",
    responses={
        422: {"description": "输入验证失败"},
        500: {"description": "服务器内部错误"}
    })
async def create_debate(request: CreateDebateRequest):
    """
    创建新辩论

    - **topic**: 辩题 (必填, 10-500 字)
    - **max_rounds**: 最大轮数 (可选, 默认 3, 范围 1-10)
    - **models**: 模型配置 (可选, 默认 MIMO vs DeepSeek)
    """
```

#### Step 3: 部署文档 (docs/deployment.md) [新建]

```
内容结构:
# 部署指南
## Docker 部署 (推荐)
  - 前置条件
  - 配置环境变量
  - 启动服务
  - 验证部署
## 手动部署
  - Python 环境准备
  - PostgreSQL 安装配置
  - Redis 安装配置
  - 应用启动
## 生产环境建议
  - Nginx 反向代理
  - HTTPS 配置
  - 日志收集
  - 监控告警
  - 备份策略
## 常见部署问题
```

#### Step 4: 开发文档 (docs/development.md) [新建]

```
内容结构:
# 开发指南
## 项目结构
  ├── agents/         # AI Agent 实现
  ├── debate/         # 辩论引擎核心
  ├── memory/         # 记忆系统
  ├── execution/      # 执行引擎
  ├── backend/        # FastAPI 后端
  ├── frontend/       # React 前端
  ├── tests/          # 测试
  └── docs/           # 文档
## 开发环境搭建
  - 克隆仓库
  - 创建虚拟环境
  - 安装依赖
  - 配置 .env
  - 启动开发服务
## 代码规范
  - Python: PEP 8 + ruff
  - TypeScript: ESLint + Prettier
  - Commit: Conventional Commits
## 测试指南
  - 运行测试
  - 编写测试
  - 测试覆盖率
## 调试技巧
```

#### Step 5: 架构文档 (docs/architecture.md) [新建]

```
内容:
# 系统架构
## 整体架构图 (Mermaid)
## 核心模块说明
  - 辩论引擎 (debate/)
  - Agent 系统 (agents/)
  - 记忆系统 (memory/)
  - 执行引擎 (execution/)
## 数据流
  - 用户输入 → 辩论 → 裁决 → 执行
## 数据库设计
  - ER 图
  - 表结构说明
## API 设计
  - RESTful 规范
  - WebSocket 协议
## 安全设计
  - 沙箱隔离
  - API 认证
  - 输入验证
```

#### Step 6: CHANGELOG (CHANGELOG.md) [新建]

```
# Changelog
## [0.2.0] - 2026-06-XX
### Added
- 执行引擎: Docker 沙箱执行
- 测试: 集成测试和 API 测试
- Docker: 一键部署配置
- 文档: 完整的开发和部署文档

### Fixed
- 循环导入问题
- CORS 配置硬编码

## [0.1.0] - 2026-06-03
### Added
- 初始版本: CLI 辩论 MVP
- 辩论引擎核心 (MIMO + DeepSeek)
- FastAPI 后端 + WebSocket
- React 前端框架
- PostgreSQL 记忆系统
```

### 6.3 文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `README.md` | 新建 | 项目主文档 |
| `docs/deployment.md` | 新建 | 部署指南 |
| `docs/development.md` | 新建 | 开发指南 |
| `docs/architecture.md` | 新建 | 架构文档 |
| `CHANGELOG.md` | 新建 | 变更日志 |
| `CONTRIBUTING.md` | 新建 | 贡献指南 |
| `docs/api-examples.md` | 新建 | API 使用示例 |

---

## 七、实施优先级和依赖关系

### 7.1 执行顺序

```
Week 3 (核心功能):
├── Day 1-2: 错误处理优化 (Feature 3)
│   ├── exceptions.py
│   ├── middleware.py
│   └── logging_config.py
├── Day 3-4: 执行引擎完善 (Feature 1)
│   ├── code_generator.py
│   ├── sandbox.py
│   └── executor.py 增强
└── Day 5: 测试基础设施
    ├── conftest.py
    └── pytest.ini

Week 4 (完善和交付):
├── Day 1-2: 测试覆盖率提升 (Feature 2)
│   ├── Agent 测试
│   ├── 辩论集成测试
│   ├── API 测试
│   └── WebSocket 测试
├── Day 3: Docker 配置 (Feature 4)
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── init-db.sql
└── Day 4-5: 文档完善 (Feature 5)
    ├── README.md
    ├── 部署文档
    ├── 开发文档
    └── CHANGELOG
```

### 7.2 依赖关系图

```
Feature 3 (错误处理) ──→ Feature 1 (执行引擎)
       │                       │
       ↓                       ↓
Feature 2 (测试) ←─────────────┘
       │
       ↓
Feature 4 (Docker) ──→ Feature 5 (文档)
```

### 7.3 估算工作量

| Feature | 文件数 | 代码量 | 工时估算 |
|---------|--------|--------|----------|
| Feature 1: 执行引擎 | 9 | ~800 行 | 2 天 |
| Feature 2: 测试覆盖 | 8 | ~1200 行 | 2 天 |
| Feature 3: 错误处理 | 7 | ~600 行 | 1.5 天 |
| Feature 4: Docker | 10 | ~300 行 | 1 天 |
| Feature 5: 文档 | 7 | ~2000 行 | 1.5 天 |
| **总计** | **41** | **~4900 行** | **~8 天** |

---

## 八、验收标准

### 8.1 功能验收

- [ ] 执行引擎: 能从 action_plan 生成代码并在沙箱中执行
- [ ] 测试覆盖: 单元测试覆盖率 ≥ 80%
- [ ] 错误处理: 所有 API 返回统一格式的错误响应
- [ ] Docker: `docker-compose up` 一键启动所有服务
- [ ] 文档: README 包含完整的快速开始指南

### 8.2 质量验收

- [ ] 所有测试通过 (`pytest` 0 failures)
- [ ] 无循环导入 (`python -c "from backend.main import app"` 成功)
- [ ] API 文档可访问 (`/docs` 返回 200)
- [ ] Docker 镜像构建成功
- [ ] 无高危安全漏洞 (`pip audit` / `npm audit`)

### 8.3 性能验收

- [ ] 辩论 API 响应时间 < 200ms (不含 AI 调用)
- [ ] WebSocket 消息延迟 < 100ms
- [ ] Docker 镜像大小 < 500MB
- [ ] 冷启动时间 < 10s
