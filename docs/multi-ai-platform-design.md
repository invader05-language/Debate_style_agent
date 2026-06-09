# Multi-AI Platform 完整设计文档

> 版本：v2.0
> 日期：2026-06-08
> 状态：设计阶段 → 实施准备
> 来源：/office-hours（2026-06-03）+ /plan-eng-review（2026-06-03）+ v2.0 扩展设计

---

## 一、项目概述

### 1.1 问题陈述

用户希望构建一个多 AI 对话 Agent，当用户提出需求时，系统调用多款不同的 AI（MIMO、DeepSeek 等），让它们以"辩论赛"模式互相反复讨论，直到形成一个完整的方案。用户根据讨论结果决定是否执行，确认后系统自动完成执行流程。系统能记住历史讨论，形成知识库，越用越聪明。

### 1.2 核心亮点

**AI 辩论赛模式** — 不同 AI 针对同一个问题互相挑战，形成对抗性思维，产生更优方案。这不是简单的协作，而是通过观点碰撞激发更好的解决方案。

**三阶段自动化**：
1. 讨论阶段 → AI 们自由辩论
2. 决策阶段 → 用户审核方案
3. 执行阶段 → 一旦确认，自动执行（代码生成、测试）

**记忆进化** — 系统记住每次讨论的结论和执行结果，形成知识库，下次讨论时能参考历史经验。

### 1.3 项目定位

Multi-AI Platform（原 Debate Agent）是一个多模型协作平台，支持多个 AI 模型通过辩论和独立思考两种工作模式，对同一问题进行多角度分析，最终输出高质量的综合结论。

### 1.4 核心价值

- **多模型协作**：同时调用 MIMO、DeepSeek、Claude、GPT、Gemini 等多款 AI
- **辩论模式**：正方 vs 反方 → 裁判总结，通过对抗提升答案质量
- **独立思考模式**（v2.0 新增）：多个 AI 独立分析 → 综合裁判汇总，避免从众效应
- **记忆系统**：基于 pgvector 的语义搜索，积累历史辩论经验
- **实时交互**：WebSocket 实时推送，支持用户中途引导

### 1.5 目标模型

- **MIMO** — 小米的 AI 模型，国内访问方便
- **DeepSeek** — 国产高性能模型，性价比高
- **Claude** — Anthropic 出品，推理能力强（v2.0 新增）
- **GPT-4o** — OpenAI 出品，综合能力领先（v2.0 新增）
- **Gemini** — Google 出品，多模态支持（v2.0 新增）

### 1.6 约束条件

- 学习阶段项目，用户是主要使用者
- 基于现有框架改造，不从零开始
- 需要支持 MIMO 和 DeepSeek 两个模型（v1.0），后续扩展更多模型
- 用户希望 1 个月内能看到可用版本

### 1.7 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | React + TypeScript + Vite | 端口 3000 |
| 后端 | FastAPI + async SQLAlchemy | 端口 8000 |
| 数据库 | PostgreSQL + pgvector | 向量语义搜索 |
| 缓存 | Redis | 会话缓存、限流 |
| 实时通信 | WebSocket | 辩论/思考进度推送 |
| 容器化 | Docker Compose | 一键部署 |
| CLI | click/typer | 命令行界面（Phase 1） |

---

## 二、方案对比与选型

### 2.1 曾考虑的方案

#### 方案 A：最简原型

- **概述**：用 Python 写一个简单脚本，调用不同 AI API，实现基本辩论循环和 JSON 存储记忆
- **工作量**：S（1-2 周）
- **风险**：低
- **优点**：快速验证核心逻辑，学习成本低，容易调试
- **缺点**：功能有限，扩展性差，没有 Web 界面

#### 方案 B：理想架构

- **概述**：从头设计完整架构，包含 Web 界面、向量数据库、插件系统
- **工作量**：XL（2-3 个月）
- **风险**：高
- **优点**：功能完整，扩展性强，用户体验好
- **缺点**：开发周期长，学习曲线陡峭，可能过度设计

#### 方案 C：借力现有框架（推荐 ✅）

- **概述**：基于现有框架改造，添加辩论逻辑、记忆层和执行模块
- **工作量**：M（1 个月）
- **风险**：中
- **优点**：快速实现，利用成熟框架，学习现有最佳实践
- **缺点**：依赖第三方框架，可能需要 hack 框架代码

### 2.2 最终选型

**选择方案 C：借力现有框架**

理由：
1. 学习阶段，需要快速看到成果
2. 现有框架已解决多 Agent 协作的核心问题
3. 只需添加辩论逻辑、记忆层和执行模块
4. 框架代码本身就是学习资源

---

## 三、架构决策记录

以下为 /plan-eng-review 阶段做出的 11 项关键架构决策：

| 编号 | 决策点 | 选择 | 理由 |
|------|--------|------|------|
| D1 | 多 Agent 框架 | AutoGen | 微软出品，成熟稳定，社区活跃 |
| D2 | 记忆存储 | 一步到位 PostgreSQL | CLI 和 Web 共享数据库，避免迁移 |
| D3 | 实时性 | WebSocket 实时推送 | 用户实时看到辩论过程，体验最好 |
| D4 | 轮次控制 | 用户控制轮次 | 默认 3 轮，用户可手动干预 |
| D5 | 执行策略 | 沙箱自动执行 | 自动生成代码并执行，安全性高 |
| D6 | 模型集成 | LangChain LLM 封装 | 统一接口，支持动态切换模型 |
| D7 | 存储策略 | 一步到位统一接口 | PostgreSQL 从 Phase 1 开始使用 |
| D8 | 错误处理 | 统一重试策略 | API 调用失败重试 3 次，超时切换备用模型 |
| D9 | 配置管理 | .env 文件管理 | python-dotenv 加载，安全且简单 |
| D10 | 缓存策略 | Redis 缓存 | 辩论结果和记忆查询缓存，减少数据库压力 |
| D11 | 并发策略 | 多用户并发 | 数据库连接池 + WebSocket 房间隔离 |

---

## 四、当前系统架构（v1.0 已实现）

### 4.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      React 前端 (端口 3000)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │ DebatePage│  │HistoryPage│  │MemoryPage│                   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                   │
│       └──────────────┼──────────────┘                        │
│                      │ axios / WebSocket                      │
└──────────────────────┼──────────────────────────────────────┘
                       │
┌──────────────────────┼──────────────────────────────────────┐
│                FastAPI 后端 (端口 8000)                       │
│  ┌───────────────────┼───────────────────┐                  │
│  │           API Router (/api)           │                  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ │                  │
│  │  │ debate  │ │ memory  │ │execution│ │                  │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ │                  │
│  └───────┼──────────┼───────────┼───────┘                  │
│          │          │           │                            │
│  ┌───────┼──────────┼───────────┼───────┐                  │
│  │       │   Services Layer     │       │                  │
│  │  ┌────┴────┐ ┌────┴────┐ ┌───┴───┐  │                  │
│  │  │ Debate  │ │ Memory  │ │ Exec  │  │                  │
│  │  │ Service │ │ Service │ │Service│  │                  │
│  │  └────┬────┘ └────┬────┘ └───┬───┘  │                  │
│  └───────┼──────────┼───────────┼───────┘                  │
│          │          │           │                            │
│  ┌───────┴──────────┴───────────┴───────┐                  │
│  │        Core Engine (debate/)         │                  │
│  │  ┌─────────┐ ┌─────────┐ ┌────────┐ │                  │
│  │  │ protocol│ │  roles  │ │ engine │ │                  │
│  │  └─────────┘ └─────────┘ └────────┘ │                  │
│  └──────────────────────────────────────┘                  │
│          │                            │                     │
│  ┌───────┴───────┐          ┌────────┴────────┐           │
│  │  AI Agents    │          │  Memory Store   │           │
│  │ ┌────┐ ┌─────┐│          │  (PostgreSQL)   │           │
│  │ │MIMO│ │Deep ││          └─────────────────┘           │
│  │ └────┘ │Seek ││                                        │
│  │        └─────┘│                                        │
│  └───────────────┘                                        │
└───────────────────────────────────────────────────────────┘
                       │
┌──────────────────────┼──────────────────────────────────────┐
│                数据层                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │    Redis     │  │ Docker 沙箱  │     │
│  │  + pgvector  │  │    缓存      │  │  代码执行    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 核心模块

#### 辩论引擎 (debate/)

```
debate/
├── protocol.py    # 数据模型: Message, Round, Verdict, DebateConfig
├── roles.py       # 角色定义: ProRole, ConRole, JudgeRole
└── engine.py      # 引擎核心: DebateEngine.start_debate()
```

**辩论流程：**
1. 用户提交辩题 → 创建 DebateConfig
2. 引擎获取相关记忆 → 注入角色提示
3. 循环执行 N 轮辩论：
   - 正方 (MIMO) 发言 → 通知 WebSocket
   - 反方 (DeepSeek) 发言 → 通知 WebSocket
   - 裁判 (MIMO) 轮次总结 → 通知 WebSocket
   - 检查共识 → 提前终止
4. 裁判输出最终裁决 (JSON)
5. 保存到记忆系统

#### Agent 系统 (agents/)

```
agents/
├── base_agent.py      # 抽象基类: chat(), get_embedding()
├── mimo_agent.py      # MIMO API 调用
├── deepseek_agent.py  # DeepSeek API 调用
└── fallback.py        # 降级策略
```

#### 记忆系统 (memory/)

```
memory/
└── store.py       # MemoryStore: save(), search(), get_relevant()
```

- PostgreSQL 存储记忆条目
- pgvector 支持语义搜索（余弦相似度）
- Redis 缓存热门查询
- ILIKE 文本搜索作为降级方案

#### 执行引擎 (execution/)

```
execution/
├── executor.py        # CodeExecutor: 基础代码执行
├── code_generator.py  # CodeGenerator: AI 生成代码
└── sandbox.py         # DockerSandbox: 沙箱执行
```

### 4.3 核心模块接口设计

#### 辩论引擎接口

```
┌─────────────────────────────────────────────┐
│              DebateEngine                    │
├─────────────────────────────────────────────┤
│ + start_debate(topic: str) -> DebateResult  │
│ + run_round(pro, con, judge) -> Round       │
│ + check_termination(rounds) -> bool         │
│ + format_output(result) -> JSON             │
└─────────────────────────────────────────────┘
         ↓ 调用
┌─────────────────────────────────────────────┐
│              AgentPool                       │
├─────────────────────────────────────────────┤
│ + get_pro_agent() -> Agent                  │
│ + get_con_agent() -> Agent                  │
│ + get_judge_agent() -> Agent                │
└─────────────────────────────────────────────┘
         ↓ 使用
┌─────────────────────────────────────────────┐
│              MemoryStore                     │
├─────────────────────────────────────────────┤
│ + save(memory: Memory)                      │
│ + search(query: str) -> List[Memory]        │
│ + get_relevant(topic: str) -> List[Memory]  │
└─────────────────────────────────────────────┘
```

#### 记忆系统数据结构

```python
Memory = {
    "id": str,
    "timestamp": datetime,
    "topic": str,
    "debate_summary": str,
    "outcome": str,
    "confidence": float,
    "tags": List[str],
    "lessons_learned": List[str]
}
```

#### 模型封装接口

```python
class BaseAgent:
    def __init__(self, model_name: str, api_key: str)
    def chat(message: str, context: List[Message]) -> str
    def get_embedding(text: str) -> List[float]

class MIMOAgent(BaseAgent): ...
class DeepSeekAgent(BaseAgent): ...
```

### 4.4 记忆影响机制

1. **首次使用**：无记忆，辩论基于通用知识
2. **第 N 次使用**：系统检索相关历史记忆，注入到辩论 prompt 中
3. **学习效果**：辩论中引用历史经验，避免重复错误

### 4.5 辩论协议

#### 角色定义

- **正方（Pro）**：支持某个方案，负责论证其优点
- **反方（Con）**：质疑方案，负责找出问题和风险
- **裁判（Judge）**：综合双方观点，给出最终建议

#### 终止条件

1. 达到最大轮次（默认 3 轮）
2. 双方达成共识
3. 用户手动终止

#### 辩论输出格式

```json
{
  "topic": "需求描述",
  "debate_rounds": [
    {
      "round": 1,
      "pro": {"argument": "...", "confidence": 0.8},
      "con": {"argument": "...", "confidence": 0.7}
    }
  ],
  "verdict": {
    "recommendation": "最终建议",
    "winner": "pro|con|draw",
    "confidence": 0.85,
    "action_plan": ["步骤1", "步骤2"]
  }
}
```

### 4.6 当前数据库设计

#### ER 图

```
debates (1) ──── (N) messages
   │
   └────────── (N) executions

memories (独立)
```

#### 表结构

**debates 表**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| topic | VARCHAR(500) | 辩题 |
| status | VARCHAR(20) | 状态：pending/running/completed/executed |
| created_at | TIMESTAMP | 创建时间 |
| completed_at | TIMESTAMP | 完成时间 |
| verdict | JSONB | 最终裁决 |
| action_plan | JSONB | 执行计划 |

**messages 表**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| debate_id | UUID, FK → debates | 所属辩论 |
| round_number | INTEGER | 轮次 |
| role | VARCHAR(20) | 角色：pro/con/judge |
| content | TEXT | 消息内容 |
| model_used | VARCHAR(50) | 使用的模型 |
| confidence | FLOAT | 信心度 |

**memories 表**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| topic | VARCHAR(500) | 主题 |
| debate_summary | TEXT | 辩论摘要 |
| outcome | TEXT | 结论 |
| confidence | FLOAT | 信心度 |
| tags | TEXT[] | 标签 |
| lessons_learned | TEXT[] | 经验教训 |
| embedding | Vector(1024) | pgvector 向量嵌入 |

**executions 表**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| debate_id | UUID, FK → debates | 所属辩论 |
| status | VARCHAR(20) | 状态：pending/running/success/failed |
| code_generated | TEXT | AI 生成的代码 |
| execution_result | TEXT | 执行结果 |
| error_message | TEXT | 错误信息 |

### 4.7 当前 API 端点

#### RESTful 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/debates | 创建辩论 |
| GET | /api/debates | 列表（分页） |
| GET | /api/debates/{id} | 详情（含消息） |
| POST | /api/debates/{id}/start | 开始辩论 |
| POST | /api/debates/{id}/execute | 执行方案 |
| POST | /api/debates/{id}/generate-code | 生成代码 |
| GET | /api/memories | 记忆列表 |
| GET | /api/memories/search?q= | 搜索记忆 |
| GET | /api/executions/{id} | 执行结果 |
| POST | /api/executions/{id}/retry | 重试执行 |

#### WebSocket 协议

连接地址：`ws://localhost:8000/ws/debate/{debate_id}`

消息类型：
```json
// 连接确认
{"type": "connected", "debate_id": "...", "message": "已连接到辩论房间"}

// 辩论消息（每轮发言）
{"type": "debate_message", "role": "pro", "content": "...", "round_number": 1, "model_used": "mimo"}

// 状态更新
{"type": "status_update", "status": "completed", "message": "辩论已完成"}

// 最终裁决
{"type": "verdict", "verdict": {"recommendation": "...", "winner": "pro", "confidence": 0.85}}

// 心跳
{"type": "ping"} → {"type": "pong", "timestamp": "..."}
```

#### 错误响应格式

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "辩论不存在",
    "request_id": "req-uuid",
    "details": {}
  }
}
```

| HTTP 状态码 | 错误码 | 说明 |
|------------|--------|------|
| 400 | BAD_REQUEST | 请求参数错误 |
| 401 | UNAUTHORIZED | 未认证 |
| 404 | NOT_FOUND | 资源不存在 |
| 409 | CONFLICT | 状态冲突 |
| 422 | VALIDATION_ERROR | 请求体验证失败 |
| 429 | RATE_LIMITED | 请求过于频繁 (60次/分钟) |
| 500 | INTERNAL_ERROR | 服务器内部错误 |

#### 限流策略

| 端点类别 | 限制 |
|----------|------|
| 全局默认 | 60 请求/分钟 |
| 辩论创建 | 30 请求/分钟 |
| 代码执行 | 10 请求/分钟 |
| 记忆搜索 | 60 请求/分钟 |

### 4.8 错误处理策略

| 错误类型 | 处理方式 |
|---------|---------|
| API 调用失败 | 重试 3 次，失败后切换到备用模型 |
| 辩论死循环 | 达到最大轮次后强制终止，裁判总结 |
| 输出格式错误 | 要求 AI 重新输出，最多重试 2 次 |
| 执行失败 | 记录错误，用户决定是否重试 |

### 4.9 安全设计

- **沙箱隔离**：Docker 容器执行代码，无网络、只读文件系统、内存限制
- **API 限流**：滑动窗口限流器
- **输入验证**：Pydantic 模式验证所有 API 输入
- **错误处理**：统一错误类型，结构化错误响应
- **JWT 认证**：Bearer Token 认证机制

### 4.10 监控体系

项目内置 Prometheus + Grafana 监控栈：

- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001`（默认账号 admin/admin，自动配置数据源）
- Redis Exporter: `http://localhost:9121`
- 指标端点：`GET /metrics`
- 健康检查：`GET /health`（含 Redis 连接状态和延迟）

Grafana Dashboard 包含 14 个面板：活跃辩论数、WebSocket 连接数、HTTP 请求速率、p95 延迟、AI Agent 请求时长、降级事件、记忆搜索速率、缓存命中率、代码执行统计、限流命中等。

### 4.11 成本估算

| 操作 | MIMO 成本 | DeepSeek 成本 | 总计 |
|------|---------|-------------|------|
| 单次辩论(3轮) | ~¥0.1 | ~¥0.15 | ~¥0.25 |
| 月使用(100次) | ~¥10 | ~¥15 | ~¥25 |
| 记忆存储 | 免费 | 免费 | 免费 |

**成本控制**：使用较短的 prompt，限制输出长度，避免不必要的轮次。

---

## 五、v2.0 升级目标：Multi-AI Platform

### 5.1 升级定位

从"辩论 Agent"升级为"Multi-AI Platform"——一个多模型协作平台，支持辩论和独立思考两种工作模式。

### 5.2 v2.0 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                      前端 (React + TS)                        │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ 模型管理  │  │  辩论模式    │  │  独立思考 + 综合模式   │ │
│  └──────────┘  └──────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    后端 API (FastAPI)                         │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ 模型CRUD │  │  辩论引擎    │  │  思考引擎 + 综合引擎   │ │
│  └──────────┘  └──────────────┘  └────────────────────────┘ │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ 记忆系统  │  │  WebSocket   │  │  执行引擎              │ │
│  └──────────┘  └──────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    AI 模型适配层                              │
│  ┌──────┐ ┌─────────┐ ┌───────┐ ┌──────┐ ┌───────┐ ┌─────┐│
│  │ MIMO │ │DeepSeek │ │ Claude│ │ GPT  │ │Gemini │ │自定义││
│  └──────┘ └─────────┘ └───────┘ └──────┘ └───────┘ └─────┘│
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PostgreSQL + Redis + pgvector                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 六、AI 模型管理模块（v2.0 新增）

### 6.1 数据模型

```sql
CREATE TABLE ai_models (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(100) NOT NULL,          -- 显示名称，如 "DeepSeek V4"
    provider      VARCHAR(50) NOT NULL,           -- 供应商：mimo / deepseek / openai / anthropic / google / custom
    model_id      VARCHAR(100) NOT NULL,          -- 模型标识，如 "deepseek-chat", "claude-sonnet-4-20250514"
    api_url       VARCHAR(500) NOT NULL,          -- API 端点
    api_key       VARCHAR(500) NOT NULL,          -- API Key（加密存储）
    api_format    VARCHAR(20) DEFAULT 'openai',   -- API 格式：openai / anthropic / gemini
    max_tokens    INT DEFAULT 4096,
    temperature   FLOAT DEFAULT 0.7,
    is_preset     BOOLEAN DEFAULT FALSE,          -- 是否预置模型
    is_active     BOOLEAN DEFAULT TRUE,           -- 是否启用
    icon          VARCHAR(50),                    -- 模型图标标识
    color         VARCHAR(20),                    -- 用于UI展示的颜色
    created_at    TIMESTAMP DEFAULT NOW(),
    updated_at    TIMESTAMP DEFAULT NOW()
);
```

### 6.2 预置模型

| 名称 | Provider | Model ID | API Format | 图标 | 颜色 |
|------|----------|----------|------------|------|------|
| MIMO V2.5 Pro | mimo | mimo-v2.5-pro | openai | 🟢 | #4CAF50 |
| DeepSeek V4 | deepseek | deepseek-chat | openai | 🔵 | #2196F3 |
| Claude Sonnet 4 | anthropic | claude-sonnet-4-20250514 | anthropic | 🟣 | #9C27B0 |
| GPT-4o | openai | gpt-4o | openai | ⚫ | #424242 |
| Gemini 2.5 Pro | google | gemini-2.5-pro | gemini | 🔴 | #F44336 |

### 6.3 API 适配层设计

```python
# 统一接口
class AIModelAdapter:
    """AI模型统一适配器"""

    async def chat(self, messages: list, **kwargs) -> str:
        """统一的对话接口"""

    async def chat_stream(self, messages: list, **kwargs) -> AsyncGenerator[str, None]:
        """流式对话接口"""

# 不同格式的实现
class OpenAIFormatAdapter:     # MIMO, DeepSeek, GPT
class AnthropicFormatAdapter:  # Claude
class GeminiFormatAdapter:     # Gemini
```

**关键设计：**
- 所有模型通过统一接口调用，上层逻辑不关心具体模型
- 支持流式输出（SSE），为后续实时显示做准备
- API Key 加密存储，前端不暴露完整 Key

### 6.4 模型管理 API

```
GET    /api/models              # 获取所有模型列表
GET    /api/models/{id}         # 获取单个模型详情
POST   /api/models              # 添加自定义模型
PUT    /api/models/{id}         # 更新模型配置
DELETE /api/models/{id}         # 删除模型（仅自定义）
POST   /api/models/{id}/test    # 测试模型连通性
GET    /api/models/presets       # 获取预置模型列表
```

### 6.5 模型管理页面设计

```
┌─────────────────────────────────────────────────────────────┐
│  AI 模型管理                                    [+ 添加模型] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─ 预置模型 ────────────────────────────────────────────┐  │
│  │                                                       │  │
│  │  🟢 MIMO V2.5 Pro     [已启用 ✓]    [测试连通性]      │  │
│  │  🔵 DeepSeek V4       [已启用 ✓]    [测试连通性]      │  │
│  │  🟣 Claude Sonnet 4   [未启用]      [启用] [测试]     │  │
│  │  ⚫ GPT-4o            [未启用]      [启用] [测试]     │  │
│  │  🔴 Gemini 2.5 Pro    [未启用]      [启用] [测试]     │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─ 自定义模型 ──────────────────────────────────────────┐  │
│  │                                                       │  │
│  │  还没有自定义模型，点击上方按钮添加                     │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**添加模型弹窗：**

```
┌─────────────────────────────────────────┐
│  添加自定义模型                    [X]  │
├─────────────────────────────────────────┤
│                                         │
│  模型名称 *    [                    ]    │
│  API 格式 *    [OpenAI ▼]               │
│  API 端点 *    [                    ]    │
│  API Key  *    [••••••••••••         ]   │
│  模型标识 *    [                    ]    │
│  Max Tokens    [4096               ]    │
│  Temperature   [0.7                ]    │
│                                         │
│  [取消]              [测试连通性] [保存] │
└─────────────────────────────────────────┘
```

---

## 七、两种工作模式（v2.0 增强 + 新增）

### 7.1 模式一：辩论模式（增强版）

在现有基础上增强，支持更多模型参与。

#### 角色分配

```
用户输入问题
    ↓
选择参与模型（至少2个）
    ↓
自动分配角色：
  - 正方（Pro）：第一个选中的模型
  - 反方（Con）：第二个选中的模型
  - 裁判（Judge）：第三个选中的模型（如果选了3个以上）
                或用户指定的模型
    ↓
辩论进行（可配置轮次：1-10轮）
    ↓
裁判总结 → 输出最终方案
```

#### 辩论流程

```
[轮次1] 正方提出方案 → 反方质疑 → 正方回应
    ↓
[轮次2] 反方提出替代方案 → 正方质疑 → 反方回应
    ↓
[轮次N] ... (用户配置的轮次)
    ↓
裁判综合双方观点，输出：
  - 推荐方案
  - 胜出方
  - 信心度
  - 执行计划
```

#### 辩论页面设计

```
┌─────────────────────────────────────────────────────────────┐
│  辩论模式                                        [新建辩论]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  问题：JWT 还是 Session 更适合我们的认证系统？                 │
│                                                             │
│  参与模型：🟢 MIMO(正方)  🔵 DeepSeek(反方)  🟣 Claude(裁判) │
│  当前轮次：第 2 轮 / 共 3 轮                                 │
│                                                             │
│  ┌─ 第1轮 ───────────────────────────────────────────────┐  │
│  │ 🟢 MIMO [正方]                                        │  │
│  │ JWT 无状态，适合分布式系统，扩展性好...                   │  │
│  │                                                       │  │
│  │ 🔵 DeepSeek [反方]                                    │  │
│  │ JWT 无法主动失效，存在安全风险...                        │  │
│  │                                                       │  │
│  │ 🟣 Claude [裁判]                                      │  │
│  │ 双方各有道理，关键在于场景选择...                        │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─ 第2轮 ───────────────────────────────────────────────┐  │
│  │ 🟢 MIMO [正方]                                        │  │
│  │ 可以用 refresh token 机制解决失效问题...                 │  │
│  │ ⏳ 等待反方回应...                                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  [⏸ 暂停]  [⏹ 终止]  [💬 插入引导]                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 7.2 模式二：独立思考 + 综合决策（v2.0 新增）

这是全新的模式，核心理念：**让每个 AI 独立分析，再由一个"旁观者"综合判断。**

#### 流程设计

```
用户输入问题
    ↓
选择参与思考的 AI（勾选，至少2个）
    ↓
选择综合裁判 AI（从剩余未参与的模型中选1个）
    ↓
[阶段1] 独立思考
  - 每个被选中的 AI 独立分析同一问题
  - 互不干扰，看不到其他 AI 的输出
  - 每个 AI 输出结构化的思考结果
    ↓
[阶段2] 综合决策
  - 所有思考结果汇总给裁判 AI
  - 裁判 AI 不参与思考，只负责综合
  - 输出最终方案
    ↓
展示结果：每个 AI 的独立思考 + 最终综合方案
```

#### 独立思考输出结构

```json
{
  "thinker": "DeepSeek V4",
  "analysis": "对问题的详细分析...",
  "pros": ["优点1", "优点2"],
  "cons": ["缺点1", "缺点2"],
  "recommendation": "我的建议...",
  "confidence": 0.85,
  "key_insight": "最关键的洞察"
}
```

#### 综合裁判输出结构

```json
{
  "synthesizer": "Claude Sonnet 4",
  "summary": "综合所有分析后...",
  "consensus": ["所有AI都认同的观点"],
  "divergence": ["存在分歧的观点"],
  "final_recommendation": "最终建议...",
  "confidence": 0.9,
  "action_plan": ["步骤1", "步骤2", "步骤3"],
  "best_insight": "最值得采纳的洞察（来自哪个AI）"
}
```

#### 独立思考页面设计

```
┌─────────────────────────────────────────────────────────────┐
│  独立思考模式                                    [新建任务]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  问题：如何设计一个高可用的微服务架构？                        │
│                                                             │
│  ┌─ 参与思考 ─────────────┐  ┌─ 综合裁判 ────────────────┐  │
│  │ ✅ MIMO V2.5 Pro       │  │ 🟣 Claude Sonnet 4       │  │
│  │ ✅ DeepSeek V4         │  │   (不参与思考，只综合)     │  │
│  │ ☐ GPT-4o              │  │                           │  │
│  │ ✅ Gemini 2.5 Pro      │  │                           │  │
│  └────────────────────────┘  └───────────────────────────┘  │
│                                                             │
│  ┌─ 阶段1：独立思考中... ─────────────────────────────────┐  │
│  │                                                       │  │
│  │  🟢 MIMO V2.5 Pro                    ⏳ 思考中...      │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │ 微服务架构需要考虑服务拆分、通信机制、容错处理...  │  │  │
│  │  │ 优点：独立部署、技术栈灵活、团队自治...           │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                                                       │  │
│  │  🔵 DeepSeek V4                      ✅ 已完成        │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │ 建议采用事件驱动架构，使用消息队列解耦服务...      │  │  │
│  │  │ 优点：松耦合、高扩展性...                         │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                                                       │  │
│  │  🔴 Gemini 2.5 Pro                   ⏳ 思考中...      │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │ ...                                             │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─ 阶段2：综合决策 ──────────────────────────────────────┐  │
│  │  🟣 Claude Sonnet 4 (综合裁判)        ⏳ 等待阶段1完成  │  │
│  │                                                       │  │
│  │  等待所有 AI 完成独立思考后开始综合...                    │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 综合完成后的结果页面

```
┌─────────────────────────────────────────────────────────────┐
│  思考结果                                        [导出] [保存]│
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─ 最终方案 ─────────────────────────────────────────────┐  │
│  │  🟣 Claude Sonnet 4 综合决策                           │  │
│  │                                                       │  │
│  │  综合3个AI的分析，推荐采用：                             │  │
│  │  1. 事件驱动微服务架构                                  │  │
│  │  2. 使用 Kafka 作为消息中间件                           │  │
│  │  3. 每个服务独立数据库（Database per Service）          │  │
│  │                                                       │  │
│  │  信心度：90%                                          │  │
│  │                                                       │  │
│  │  共识点：所有AI都认为需要服务拆分和异步通信               │  │
│  │  分歧点：数据库策略上存在分歧                            │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─ 各AI独立思考 ─────────────────────────────────────────┐  │
│  │  [🟢 MIMO]  [🔵 DeepSeek]  [🔴 Gemini]                │  │
│  │                                                       │  │
│  │  🔵 DeepSeek V4 的思考：                               │  │
│  │  分析：建议采用事件驱动架构...                           │  │
│  │  关键洞察：消息队列是微服务通信的核心...                   │  │
│  │  建议：使用 Kafka + 服务网格...                         │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 八、v2.0 数据库变更

### 新增表

```sql
-- AI模型配置表
CREATE TABLE ai_models (...);  -- 见第六章 6.1

-- 任务表（统一辩论和独立思考）
CREATE TABLE tasks (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type          VARCHAR(20) NOT NULL,           -- 'debate' / 'think'
    topic         TEXT NOT NULL,                   -- 问题/主题
    status        VARCHAR(20) DEFAULT 'pending',   -- pending/running/completed/failed
    config        JSONB,                           -- 任务配置（轮次、参与模型等）
    result        JSONB,                           -- 最终结果
    created_at    TIMESTAMP DEFAULT NOW(),
    completed_at  TIMESTAMP
);

-- 任务消息表（记录每个AI的输出）
CREATE TABLE task_messages (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id       UUID REFERENCES tasks(id),
    model_id      UUID REFERENCES ai_models(id),
    role          VARCHAR(20),                    -- pro/con/judge/thinker/synthesizer
    round_number  INT,
    content       TEXT NOT NULL,
    structured    JSONB,                           -- 结构化输出
    created_at    TIMESTAMP DEFAULT NOW()
);
```

### 表关系

```
ai_models (1) ──→ (N) task_messages
tasks      (1) ──→ (N) task_messages
tasks      (1) ──→ (1) result (JSONB)
debates    (1) ──→ (N) messages      (v1.0 保留)
debates    (1) ──→ (N) executions    (v1.0 保留)
memories   (独立)                     (v1.0 保留)
```

---

## 九、v2.0 完整 API 设计

### 9.1 模型管理 API

```
GET    /api/models                 # 获取所有模型
POST   /api/models                 # 添加模型
PUT    /api/models/{id}            # 更新模型
DELETE /api/models/{id}            # 删除模型
POST   /api/models/{id}/test       # 测试连通性
```

### 9.2 辩论模式 API

```
POST   /api/debates                # 创建辩论
POST   /api/debates/{id}/start     # 开始辩论
GET    /api/debates/{id}           # 获取辩论详情
POST   /api/debates/{id}/pause     # 暂停辩论
POST   /api/debates/{id}/resume    # 恢复辩论
POST   /api/debates/{id}/inject    # 用户插入引导语
```

### 9.3 独立思考模式 API

```
POST   /api/thinks                 # 创建思考任务
POST   /api/thinks/{id}/start      # 开始思考
GET    /api/thinks/{id}            # 获取思考详情
GET    /api/thinks/{id}/progress   # 获取各AI思考进度
```

### 9.4 记忆 API（保留 v1.0）

```
GET    /api/memories               # 记忆列表
GET    /api/memories/search?q=     # 搜索记忆
GET    /api/memories/{id}          # 记忆详情
POST   /api/memories               # 创建记忆
POST   /api/memories/{id}/generate-embedding    # 生成嵌入
POST   /api/memories/generate-all-embeddings    # 批量生成嵌入
```

### 9.5 执行 API（保留 v1.0）

```
POST   /api/debates/{id}/execute           # 执行方案
POST   /api/debates/{id}/generate-code     # 生成代码
GET    /api/executions/{id}                # 执行结果
POST   /api/executions/{id}/retry          # 重试执行
```

### 9.6 WebSocket 事件（v2.0 增强）

```
WS /ws/task/{task_id}

事件类型：
- task_started       任务开始
- think_progress     某个AI思考进度更新
- think_completed    某个AI思考完成
- round_completed    辩论某轮完成
- synthesis_started  综合裁判开始工作
- task_completed     任务完成
- task_failed        任务失败
```

---

## 十、前端路由设计（v2.0）

```
/                          → 首页（任务列表）
/models                    → AI模型管理页面
/debate/new                → 新建辩论
/debate/{id}               → 辩论详情/进行中
/think/new                 → 新建独立思考
/think/{id}                → 思考详情/进行中
/history                   → 历史记录（辩论+思考）
/memory                    → 记忆库
```

---

## 十一、CLI 命令设计（Phase 1）

```bash
# 开始辩论
debate start "设计一个用户登录系统"

# 查看辩论结果
debate review <debate_id>

# 确认执行
debate execute <debate_id>

# 查看历史
debate history

# 查看记忆
debate memories
```

---

## 十二、风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| AutoGen 框架学习曲线 | 中 | 先读官方文档和示例 |
| API 调用成本 | 低 | 限制轮次，使用短 prompt |
| WebSocket 稳定性 | 中 | 添加重连机制 |
| 数据库迁移 | 低 | 使用 Alembic 管理迁移 |
| 沙箱安全 | 高 | 使用 Docker 容器隔离执行环境 |
| API Key 安全 | 高 | 后端代理所有 AI 调用，前端不接触 Key |
| 并发限制 | 中 | 多 AI 同时调用时的速率限制和队列管理 |
| 成本控制 | 中 | 防止用户滥用导致 API 费用过高 |
| 模型可用性 | 中 | 某些模型国内不可用，需要代理方案 |

---

## 十三、测试策略

### 测试金字塔

- 单元测试：60%（100-150 个用例）
- 集成测试：30%（30-40 个场景）
- E2E 测试：10%（5-8 个核心流程）

### 关键路径测试

- **P0**：辩论引擎核心循环、Agent 调用重试、执行引擎沙箱安全、WebSocket 实时推送
- **P1**：记忆存储与检索、API 端点正确性、数据库迁移
- **P2**：前端组件交互

### 测试工具栈

- pytest + pytest-asyncio
- httpx + TestClient
- factory_boy
- pytest-cov
- pytest-mock

### 测试覆盖率目标

| 类型 | 目标 |
|------|------|
| 单元测试 | ≥ 85% |
| 集成测试 | ≥ 70% |
| E2E 核心流程 | 100% |

---

## 十四、部署指南

### 14.1 Docker 部署（推荐）

#### 前置条件

- Docker Engine 20.10+
- Docker Compose v2.0+
- MIMO API Key
- DeepSeek API Key

#### 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 必填
MIMO_API_KEY=your_mimo_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key

# 可选
MIMO_API_URL=https://token-plan-sgp.xiaomimimo.com/v1
DEEPSEEK_API_URL=https://api.deepseek.com/v1
DEBUG=false
LOG_LEVEL=INFO
```

#### 启动服务

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend

# 检查状态
docker-compose ps
```

#### 验证部署

```bash
# 检查后端健康
curl http://localhost:8000/health

# 检查前端
curl http://localhost:3000

# 检查 API 文档
open http://localhost:8000/docs
```

### 14.2 手动部署

#### Python 环境准备

```bash
# Python 3.11+
python --version

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

#### PostgreSQL 安装配置

```bash
# 创建数据库
sudo -u postgres psql
CREATE DATABASE debate_agent;
CREATE USER debate_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE debate_user TO debate_agent;
\q

# 启用 pgvector 扩展
sudo -u postgres psql -d debate_agent -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

#### 数据库迁移（Alembic）

```bash
# 升级到最新版本
python scripts/migrate.py upgrade

# 查看当前版本
python scripts/migrate.py current

# 查看迁移历史
python scripts/migrate.py history
```

迁移文件位于 `alembic/versions/`，初始迁移创建以下表：
- `users` - 用户认证表
- `debates` - 辩论记录表
- `messages` - 辩论消息表
- `memories` - 记忆存储表（含 pgvector embedding）
- `executions` - 代码执行记录表

#### 应用启动

```bash
# 配置环境变量
export DATABASE_URL=postgresql://debate_user:your_password@localhost:5432/debate_agent
export REDIS_URL=redis://localhost:6379/0
export MIMO_API_KEY=your_key
export DEEPSEEK_API_KEY=your_key

# 执行数据库迁移
python scripts/migrate.py upgrade

# 启动后端
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# 启动前端（另一个终端）
cd frontend
npm install
npm start
```

### 14.3 生产环境建议

#### Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

#### 备份策略

```bash
# 数据库备份
pg_dump -U postgres debate_agent > backup_$(date +%Y%m%d).sql

# 恢复
psql -U postgres debate_agent < backup_20260603.sql
```

---

## 十五、开发指南

### 15.1 项目结构

```
debate-agent/
├── agents/              # AI Agent 实现
│   ├── base_agent.py    # 抽象基类
│   ├── mimo_agent.py    # MIMO API 调用
│   ├── deepseek_agent.py# DeepSeek API 调用
│   └── fallback.py      # 降级策略
├── debate/              # 辩论引擎核心
│   ├── protocol.py      # 数据模型
│   ├── roles.py         # 角色定义
│   └── engine.py        # 引擎逻辑
├── memory/              # 记忆系统
│   └── store.py         # PostgreSQL 存储
├── execution/           # 执行引擎
│   ├── executor.py      # 基础执行
│   ├── code_generator.py# AI 代码生成
│   └── sandbox.py       # Docker 沙箱
├── prompts/             # Prompt 模板
│   └── templates.py     # 辩论/角色模板
├── backend/             # FastAPI 后端
│   ├── api/             # REST API 端点
│   ├── models/          # SQLAlchemy 模型
│   ├── schemas/         # Pydantic 模式
│   ├── services/        # 业务逻辑
│   └── websocket/       # WebSocket
├── frontend/            # React 前端
│   └── src/
│       ├── components/  # UI 组件
│       ├── pages/       # 页面
│       ├── hooks/       # 自定义 Hook
│       └── services/    # API 服务
├── tests/               # 测试
├── docs/                # 文档
├── scripts/             # 脚本
└── docker-compose.yml   # Docker 编排
```

### 15.2 开发环境搭建

```bash
# 1. 克隆仓库
git clone <repo-url>
cd debate-agent

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt
cd frontend && npm install && cd ..

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API Keys

# 5. 启动开发服务
# 终端 1: 后端
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 终端 2: 前端
cd frontend && npm start

# 终端 3: 数据库
docker-compose up -d db redis
```

### 15.3 代码规范

**Python：**
- 遵循 PEP 8
- 使用 type hints
- 使用 `ruff` 进行 linting，`black` 格式化

**TypeScript：**
- 使用 ESLint + Prettier
- 遵循 React 最佳实践
- TypeScript 严格模式

**Commit 规范（Conventional Commits）：**
```
feat: 添加新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 添加测试
chore: 构建/工具变更
```

---

## 十六、技术要点

### 16.1 并行调用

独立思考模式需要同时调用多个 AI，使用 `asyncio.gather()` 实现：

```python
async def parallel_think(models: list, topic: str) -> list:
    """并行调用多个AI进行独立思考"""
    tasks = [think(model, topic) for model in models]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### 16.2 流式输出

前端实时显示 AI 的思考过程，使用 SSE（Server-Sent Events）：

```python
async def stream_think(model, topic):
    async for chunk in model.chat_stream(messages):
        yield f"data: {json.dumps({'chunk': chunk})}\n\n"
```

### 16.3 错误处理

某个 AI 调用失败不应影响其他 AI：

```python
results = await asyncio.gather(*tasks, return_exceptions=True)
for i, result in enumerate(results):
    if isinstance(result, Exception):
        results[i] = {"error": str(result), "model": models[i].name}
```

### 16.4 缓存策略

- Redis 缓存辩论结果和记忆查询结果
- 减少数据库查询压力
- 数据库连接池（SQLAlchemy）
- WebSocket 房间隔离（每个辩论独立房间）

---

## 十七、实施计划

### 架构优势

1. **核心复用**：Phase 1 的辩论引擎、记忆系统、Agent 封装在 Phase 2 直接复用
2. **渐进升级**：从 CLI 到 Web 是增量升级，不是重写
3. **技术栈匹配**：FastAPI + PostgreSQL + React 完全满足 Web 版需求
4. **实时体验**：WebSocket 让用户实时看到辩论过程

### Phase 1：CLI MVP（第 1-2 周）

- [ ] 搭建 Python 项目结构
- [ ] 集成 MIMO 和 DeepSeek API
- [ ] 实现辩论引擎核心逻辑
- [ ] 实现 PostgreSQL 记忆存储
- [ ] 实现 CLI 界面（debate start/review/execute/history/memories）

### Phase 2：Web 全栈（第 3-4 周）

- [ ] 搭建 FastAPI 后端
- [ ] 实现 WebSocket 实时通信
- [ ] 搭建 React 前端
- [ ] 集成 Redis 缓存
- [ ] 集成测试

### Phase 3：v2.0 模型管理模块（第 5 周）

- [ ] 数据库：ai_models 表 + 预置数据
- [ ] 后端：模型 CRUD API + 连通性测试
- [ ] 前端：模型管理页面 + 添加/编辑弹窗
- [ ] AI 适配层：OpenAI/Anthropic/Gemini 三种格式

### Phase 4：v2.0 辩论模式增强（第 6 周）

- [ ] 数据库：tasks + task_messages 表
- [ ] 后端：辩论引擎改造（支持多模型选择）
- [ ] 前端：辩论页面重构（模型选择、实时显示）
- [ ] WebSocket：实时推送辩论进度

### Phase 5：v2.0 独立思考模式（第 7-8 周）

- [ ] 后端：思考引擎（并行调用多个 AI）
- [ ] 后端：综合引擎（汇总 + 裁判 AI 生成最终方案）
- [ ] 前端：独立思考页面（进度展示、结果展示）
- [ ] WebSocket：实时推送思考进度

### Phase 6：打磨优化（第 9 周）

- [ ] 辩论回放功能
- [ ] 结果导出（Markdown/PDF）
- [ ] 思考过程可视化
- [ ] 性能优化（并行调用、缓存）

---

## 十八、成功标准

1. 能调用 MIMO 和 DeepSeek 两个模型
2. AI 能以辩论模式互相讨论，产出结构化 JSON 方案
3. 用户能审核方案并决定是否执行
4. 执行阶段能自动生成代码并运行测试
5. 系统能记住历史讨论，下次能参考
6. 1 个月内完成 MVP 版本

---

## 十九、开放问题

1. **API Key 安全**：是否需要后端代理所有 AI 调用，前端不直接接触 Key？
2. **并发限制**：多个 AI 同时调用时的速率限制和队列管理
3. **成本控制**：如何防止用户滥用导致 API 费用过高
4. **模型可用性**：某些模型可能在国内不可用（如 GPT、Claude），需要代理方案？
5. **v1.0 兼容性**：现有 debates/messages/executions 表是否需要迁移到新的 tasks/task_messages 结构？
