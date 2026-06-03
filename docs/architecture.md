# 系统架构

## 整体架构

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

## 核心模块

### 辩论引擎 (debate/)

```
debate/
├── protocol.py    # 数据模型: Message, Round, Verdict, DebateConfig
├── roles.py       # 角色定义: ProRole, ConRole, JudgeRole
└── engine.py      # 引擎核心: DebateEngine.start_debate()
```

**辩论流程:**
1. 用户提交辩题 → 创建 DebateConfig
2. 引擎获取相关记忆 → 注入角色提示
3. 循环执行 N 轮辩论:
   - 正方 (MIMO) 发言 → 通知 WebSocket
   - 反方 (DeepSeek) 发言 → 通知 WebSocket
   - 裁判 (MIMO) 轮次总结 → 通知 WebSocket
   - 检查共识 → 提前终止
4. 裁判输出最终裁决 (JSON)
5. 保存到记忆系统

### Agent 系统 (agents/)

```
agents/
├── base_agent.py      # 抽象基类: chat(), get_embedding()
├── mimo_agent.py      # MIMO API 调用
├── deepseek_agent.py  # DeepSeek API 调用
└── fallback.py        # 降级策略
```

### 记忆系统 (memory/)

```
memory/
└── store.py       # MemoryStore: save(), search(), get_relevant()
```

- PostgreSQL 存储记忆条目
- pgvector 支持语义搜索
- Redis 缓存热门查询

### 执行引擎 (execution/)

```
execution/
├── executor.py        # CodeExecutor: 基础代码执行
├── code_generator.py  # CodeGenerator: AI 生成代码
└── sandbox.py         # DockerSandbox: 沙箱执行
```

## 数据库设计

### ER 图

```
debates (1) ──── (N) messages
   │
   └────────── (N) executions

memories (独立)
```

### 表结构

**debates**
- id (UUID, PK)
- topic (VARCHAR)
- status (VARCHAR: pending/running/completed/failed)
- created_at (TIMESTAMP)
- completed_at (TIMESTAMP)
- verdict (JSONB)
- action_plan (JSONB)

**messages**
- id (UUID, PK)
- debate_id (UUID, FK → debates)
- round_number (INTEGER)
- role (VARCHAR: pro/con/judge)
- content (TEXT)
- model_used (VARCHAR)
- confidence (FLOAT)

**memories**
- id (UUID, PK)
- topic (VARCHAR)
- debate_summary (TEXT)
- outcome (TEXT)
- confidence (FLOAT)
- tags (TEXT[])
- lessons_learned (TEXT[])

**executions**
- id (UUID, PK)
- debate_id (UUID, FK → debates)
- status (VARCHAR: pending/running/success/failed)
- code_generated (TEXT)
- execution_result (TEXT)
- error_message (TEXT)

## API 设计

### RESTful 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/debates | 创建辩论 |
| GET | /api/debates | 列表（分页） |
| GET | /api/debates/{id} | 详情 |
| POST | /api/debates/{id}/start | 开始辩论 |
| POST | /api/debates/{id}/execute | 执行方案 |
| POST | /api/debates/{id}/generate-code | 生成代码 |
| GET | /api/memories | 记忆列表 |
| GET | /api/memories/search?q= | 搜索记忆 |
| GET | /api/executions/{id} | 执行结果 |
| POST | /api/executions/{id}/retry | 重试执行 |

### WebSocket 协议

连接: `ws://localhost:8000/ws/debate/{debate_id}`

消息类型:
```json
{"type": "connected", "debate_id": "...", "message": "..."}
{"type": "debate_message", "role": "pro", "content": "...", "round_number": 1}
{"type": "status_update", "status": "completed", "message": "..."}
{"type": "verdict", "verdict": {"recommendation": "...", "winner": "pro"}}
{"type": "pong", "timestamp": "..."}
```

## 安全设计

- **沙箱隔离**: Docker 容器执行代码，无网络、只读文件系统、内存限制
- **API 限流**: 滑动窗口限流器，60 请求/分钟
- **输入验证**: Pydantic 模式验证所有 API 输入
- **错误处理**: 统一错误类型，结构化错误响应
