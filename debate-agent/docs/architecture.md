# 系统架构

> 更新日期：2026-06-09
> 状态：v2.0 — 前端已替换为 React 19 + Tailwind CSS v4 + Express.js 架构

## 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    前端 (React 19 + TypeScript + Vite)             │
│                     端口 3000 (Express.js Server)                  │
│                                                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌────────────────┐  │
│  │  Header   │ │ Sidebar  │ │ HomeDashboard│ │DebateWorkspace │  │
│  └──────────┘ └──────────┘ └──────────────┘ └────────────────┘  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │
│  │ThinkWorkspace│ │ModelMgmt     │ │ HistoryAndLogs           │ │
│  └──────────────┘ └──────────────┘ └──────────────────────────┘ │
│  ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌──────────────┐  │
│  │MemoryBank│ │AnalyticsPanel│ │Terminal   │ │AccountSettings│ │
│  └──────────┘ └──────────────┘ └──────────┘ └──────────────┘  │
│  ┌──────────┐                                                    │
│  │HelpCenter│                                                    │
│  └──────────┘                                                    │
│                                                                   │
│  导航模式: Tab-based (非 React Router)                             │
│  状态管理: props lifted to App component                           │
│  样式: Tailwind CSS v4 (@tailwindcss/vite)                        │
│  图标: lucide-react                                                │
└───────────────────────────┬──────────────────────────────────────┘
                            │ fetch / WebSocket
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                    Express.js 后端 (server.ts)                     │
│                    端口 3000 (同进程，Vite 中间件模式)               │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                    API Routes                              │   │
│  │  POST /api/debate/next-turn    → 辩论轮次生成              │   │
│  │  POST /api/debate/synthesize   → 裁判综合裁决              │   │
│  │  POST /api/think/process       → 多模型独立思考             │   │
│  │  GET  /api/health              → 健康检查                  │   │
│  └───────────────────────────────────────────────────────────┘   │
│                            │                                      │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │              Google Gemini AI SDK                          │   │
│  │              (@google/genai)                               │   │
│  │  - gemini-3.5-flash 模型                                   │   │
│  │  - JSON Schema 结构化输出                                   │   │
│  │  - 懒加载初始化（防止 API Key 缺失导致启动崩溃）              │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
│  降级策略: API 调用失败时返回硬编码的模拟响应                        │
└───────────────────────────────────────────────────────────────────┘

                     (v2.0 目标架构，待实现)
┌───────────────────────────────────────────────────────────────────┐
│                    FastAPI 后端 (端口 8000)                         │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐      │
│  │ 模型CRUD │  │  辩论引擎    │  │  思考引擎 + 综合引擎   │      │
│  └──────────┘  └──────────────┘  └────────────────────────┘      │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐      │
│  │ 记忆系统  │  │  WebSocket   │  │  执行引擎              │      │
│  └──────────┘  └──────────────┘  └────────────────────────┘      │
└───────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                    AI 模型适配层                                    │
│  ┌──────┐ ┌─────────┐ ┌───────┐ ┌──────┐ ┌───────┐             │
│  │ MIMO │ │DeepSeek │ │ Claude│ │ GPT  │ │Gemini │             │
│  └──────┘ └─────────┘ └───────┘ └──────┘ └───────┘             │
└───────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│  PostgreSQL + Redis + pgvector + Docker Sandbox                    │
└───────────────────────────────────────────────────────────────────┘
```

## 前端架构（v2.0 已实现）

### 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| React | 19.x | UI 框架 |
| TypeScript | 5.x | 类型安全 |
| Vite | 6.x | 构建工具 |
| Tailwind CSS | v4 (@tailwindcss/vite) | 样式系统 |
| lucide-react | latest | 图标库 |
| Express.js | 4.x | 后端服务器（同进程） |
| @google/genai | latest | Gemini AI SDK |

### 组件架构

```
src/
├── App.tsx              # 主应用组件，状态管理 + 视图路由
├── main.tsx             # 入口文件
├── types.ts             # TypeScript 类型定义
├── data.ts              # 初始模拟数据
├── components/
│   ├── Header.tsx       # 顶部导航栏（品牌 + Tab 切换 + 设置入口）
│   ├── Sidebar.tsx      # 左侧边栏（工作区/分析/终端/设置/帮助）
│   ├── HomeDashboard.tsx    # 首页仪表盘（活动流 + 模型状态 + 快速入口）
│   ├── DebateWorkspace.tsx  # 辩论工作台（辩题配置 + 模型选择 + 轮次展示）
│   ├── ThinkWorkspace.tsx   # 思考工作台（多模型独立思考 + 综合裁判）
│   ├── ModelManagement.tsx  # 模型管理（注册表 + 启用/禁用 + 测试连通性）
│   ├── HistoryAndLogs.tsx   # 历史记录（搜索/过滤 + 日志详情弹窗）
│   ├── MemoryBank.tsx       # 记忆库（语义搜索 + 标签过滤 + 增删）
│   ├── AnalyticsPanel.tsx   # 分析面板（性能指标 + 使用趋势）
│   ├── TerminalPanel.tsx    # 终端面板（实时遥测日志流）
│   ├── AccountSettings.tsx  # 账户设置（语言/主题/通知/API Key）
│   └── HelpCenter.tsx       # 帮助中心（FAQ + 搜索）
```

### 导航逻辑

```
Header Tab 点击 → setActiveTab(tab) + setActiveView('workspace')
  ├── home    → HomeDashboard
  ├── debate  → DebateWorkspace
  ├── think   → ThinkWorkspace
  ├── models  → ModelManagement
  ├── history → HistoryAndLogs
  └── memory  → MemoryBank

Sidebar 点击 → setActiveView(view)
  ├── workspace  → 跟随 activeTab
  ├── analytics  → AnalyticsPanel（覆盖 Tab）
  ├── terminal   → TerminalPanel
  ├── settings   → AccountSettings
  └── help       → HelpCenter
```

### 状态管理

所有状态通过 props 提升到 App 组件，无 Redux/Zustand 等外部状态库：

```
App.tsx
├── activeTab: string        # 当前 Tab
├── activeView: string       # 当前视图（sidebar 可覆盖 tab）
├── activities: ActivityItem[]   # 活动流
├── models: ModelStatus[]        # 模型状态
├── history: HistoryItem[]       # 历史记录
├── memories: MemoryInsight[]    # 记忆条目
└── settings: AppSettings        # 用户设置
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
   - 正方发言 → WebSocket 推送
   - 反方发言 → WebSocket 推送
   - 裁判轮次总结 → WebSocket 推送
   - 检查共识 → 提前终止
4. 裁判输出最终裁决 (JSON)
5. 保存到记忆系统

### Agent 系统 (agents/)

```
agents/
├── base_agent.py      # 抽象基类: chat(), get_embedding()
├── mimo_agent.py      # MIMO API 调用
├── deepseek_agent.py  # DeepSeek API 调用
├── claude_agent.py    # Claude API 调用 (v2.0)
├── gpt_agent.py       # GPT-4o API 调用 (v2.0)
├── gemini_agent.py    # Gemini API 调用 (v2.0)
└── fallback.py        # 降级策略
```

### 记忆系统 (memory/)

```
memory/
└── store.py       # MemoryStore: save(), search(), get_relevant()
```

- PostgreSQL 存储记忆条目
- pgvector 支持语义搜索（余弦相似度）
- Redis 缓存热门查询
- ILIKE 文本搜索作为降级方案

### 执行引擎 (execution/)

```
execution/
├── executor.py        # CodeExecutor: 基础代码执行
├── code_generator.py  # CodeGenerator: AI 生成代码
└── sandbox.py         # DockerSandbox: 沙箱执行
```

### AI 模型适配层 (adapters/) — v2.0 新增

```
adapters/
├── base_adapter.py        # 统一接口: chat(), chat_stream()
├── openai_format.py       # MIMO, DeepSeek, GPT (OpenAI 兼容格式)
├── anthropic_format.py    # Claude (Anthropic 格式)
└── gemini_format.py       # Gemini (Google GenAI 格式)
```

## 数据库设计

### ER 图

```
ai_models (1) ──→ (N) task_messages    (v2.0 新增)
tasks      (1) ──→ (N) task_messages    (v2.0 新增)
tasks      (1) ──→ (1) result (JSONB)   (v2.0 新增)

debates (1) ──── (N) messages           (v1.0 保留)
   │
   └────────── (N) executions           (v1.0 保留)

memories (独立)
user_settings (独立)                     (v2.0 新增)
api_keys (独立)                          (v2.0 新增)
faqs (独立)                              (v2.0 新增)
notifications (独立)                     (v2.0 新增)
```

### 表结构

**ai_models** (v2.0 新增)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| name | VARCHAR(100) | 显示名称 |
| provider | VARCHAR(50) | 供应商：mimo/deepseek/openai/anthropic/google/custom |
| model_id | VARCHAR(100) | 模型标识 |
| api_url | VARCHAR(500) | API 端点 |
| api_key | VARCHAR(500) | API Key（加密存储） |
| api_format | VARCHAR(20) | API 格式：openai/anthropic/gemini |
| max_tokens | INT | 最大 token 数，默认 4096 |
| temperature | FLOAT | 温度，默认 0.7 |
| is_preset | BOOLEAN | 是否预置模型 |
| is_active | BOOLEAN | 是否启用 |
| icon | VARCHAR(50) | 图标标识 |
| color | VARCHAR(20) | UI 展示颜色 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**tasks** (v2.0 新增，统一辩论和思考)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| type | VARCHAR(20) | 任务类型：debate/think |
| topic | TEXT | 问题/主题 |
| status | VARCHAR(20) | 状态：pending/running/completed/failed |
| config | JSONB | 任务配置（轮次、参与模型等） |
| result | JSONB | 最终结果 |
| created_at | TIMESTAMP | 创建时间 |
| completed_at | TIMESTAMP | 完成时间 |

**task_messages** (v2.0 新增)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| task_id | UUID, FK → tasks | 所属任务 |
| model_id | UUID, FK → ai_models | 使用的模型 |
| role | VARCHAR(20) | 角色：pro/con/judge/thinker/synthesizer/user |
| round_number | INT | 轮次 |
| content | TEXT | 消息内容 |
| structured | JSONB | 结构化输出（confidence, depth 等） |
| created_at | TIMESTAMP | 创建时间 |

**debates** (v1.0 保留)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| topic | VARCHAR(500) | 辩题 |
| status | VARCHAR(20) | 状态：pending/running/completed/executed |
| created_at | TIMESTAMP | 创建时间 |
| completed_at | TIMESTAMP | 完成时间 |
| verdict | JSONB | 最终裁决 |
| action_plan | JSONB | 执行计划 |

**messages** (v1.0 保留)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| debate_id | UUID, FK → debates | 所属辩论 |
| round_number | INTEGER | 轮次 |
| role | VARCHAR(20) | 角色：pro/con/judge |
| content | TEXT | 消息内容 |
| model_used | VARCHAR(50) | 使用的模型 |
| confidence | FLOAT | 信心度 |

**memories**
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

**executions** (v1.0 保留)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| debate_id | UUID, FK → debates | 所属辩论 |
| status | VARCHAR(20) | 状态：pending/running/success/failed |
| code_generated | TEXT | AI 生成的代码 |
| execution_result | TEXT | 执行结果 |
| error_message | TEXT | 错误信息 |

**user_settings** (v2.0 新增)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| user_id | UUID | 用户 ID |
| language | VARCHAR(10) | 语言，默认 zh |
| theme_mode | VARCHAR(10) | 主题模式：light/dark |
| notifications | BOOLEAN | 通知开关 |
| weekly_digest | BOOLEAN | 周报开关 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**api_keys** (v2.0 新增)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| provider | VARCHAR(50) | 供应商 |
| api_key_enc | TEXT | AES-256 加密存储 |
| key_preview | VARCHAR(30) | 脱敏预览 |
| is_active | BOOLEAN | 是否启用 |
| created_at | TIMESTAMP | 创建时间 |

**faqs** (v2.0 新增)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| question | TEXT | 问题 |
| answer | TEXT | 回答 |
| category | VARCHAR(50) | 分类：debate/think/model/general |
| sort_order | INT | 排序 |

**notifications** (v2.0 新增)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID, PK | 主键 |
| title | VARCHAR(200) | 标题 |
| message | TEXT | 内容 |
| type | VARCHAR(20) | 类型：info/warning/error/success |
| is_read | BOOLEAN | 是否已读 |
| created_at | TIMESTAMP | 创建时间 |

## API 设计

### 当前已实现 API（Express.js server.ts）

| 方法 | 路径 | 说明 | 状态 |
|------|------|------|------|
| GET | /api/health | 健康检查 | ✅ 已实现 |
| POST | /api/debate/next-turn | 辩论轮次生成（Gemini + 模拟降级） | ✅ 已实现 |
| POST | /api/debate/synthesize | 裁判综合裁决（Gemini + 模拟降级） | ✅ 已实现 |
| POST | /api/think/process | 多模型独立思考（Gemini + 模拟降级） | ✅ 已实现 |

### v2.0 目标 API（FastAPI，待实现）

#### 模型管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/models | 获取所有模型 |
| POST | /api/models | 添加模型 |
| PUT | /api/models/{id} | 更新模型 |
| DELETE | /api/models/{id} | 删除模型 |
| POST | /api/models/{id}/toggle | 启用/禁用模型 |
| POST | /api/models/{id}/test | 测试连通性 |

#### 辩论模式

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/debates | 创建辩论 |
| POST | /api/debates/{id}/start | 开始辩论 |
| GET | /api/debates/{id} | 获取辩论详情 |
| POST | /api/debates/{id}/pause | 暂停辩论 |
| POST | /api/debates/{id}/resume | 恢复辩论 |
| POST | /api/debates/{id}/inject | 用户插入引导语 |

#### 独立思考模式

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/thinks | 创建思考任务 |
| POST | /api/thinks/{id}/start | 开始思考 |
| GET | /api/thinks/{id} | 获取思考详情 |
| GET | /api/thinks/{id}/progress | 获取各AI思考进度 |

#### 记忆系统

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/memories | 记忆列表（分页） |
| GET | /api/memories/search?q= | 语义搜索 |
| GET | /api/memories/{id} | 记忆详情 |
| POST | /api/memories | 创建记忆 |
| DELETE | /api/memories/{id} | 删除记忆 |

#### 仪表盘与分析

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/dashboard/stats | 首页统计数据 |
| GET | /api/analytics?period=7d | 分析面板数据 |
| GET | /api/tasks?page=1&limit=20 | 任务历史列表 |
| GET | /api/tasks/{id} | 任务详情（含消息） |

#### 设置与帮助

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/settings | 获取用户设置 |
| PUT | /api/settings | 更新用户设置 |
| PUT | /api/settings/api-keys | 更新 API Key |
| GET | /api/faqs | 获取 FAQ 列表 |

### WebSocket 协议

**辩论/思考进度** — `ws://localhost:8000/ws/task/{task_id}`

```json
// 连接确认
{"type": "connected", "task_id": "...", "message": "已连接到任务房间"}

// 辩论消息（每轮发言）
{"type": "debate_message", "role": "pro", "content": "...", "round_number": 1, "model_used": "mimo", "structured": {"logicalConfidence": 88, "contextualDepth": 85}}

// 思考进度
{"type": "think_progress", "model_id": "...", "model_name": "MIMO", "status": "thinking"}

// 思考完成
{"type": "think_completed", "model_id": "...", "result": {...}}

// 综合裁判开始
{"type": "synthesis_started", "model_name": "Claude Sonnet 4"}

// 任务完成
{"type": "task_completed", "result": {...}}

// 任务失败
{"type": "task_failed", "error": "..."}

// 心跳
{"type": "ping"} → {"type": "pong", "timestamp": "..."}
```

**终端遥测** — `ws://localhost:8000/ws/telemetry`

```json
{"type": "log", "level": "info", "source": "debate-engine", "message": "MIMO 响应完成，耗时 1.2s", "timestamp": "...", "metadata": {"model": "mimo", "latency_ms": 1200}}
```

### 错误响应格式

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

## 安全设计

- **沙箱隔离**: Docker 容器执行代码，无网络、只读文件系统、内存限制
- **API 限流**: 滑动窗口限流器，60 请求/分钟
- **输入验证**: Pydantic 模式验证所有 API 输入
- **错误处理**: 统一错误类型，结构化错误响应
- **API Key 安全**: 后端代理所有 AI 调用，前端不接触完整 Key；AES-256 加密存储
- **JWT 认证**: Bearer Token 认证机制（v2.0）

## 监控体系

- Prometheus + Grafana 监控栈
- 健康检查：GET /api/health
- 遥测 WebSocket：实时推送系统日志
- Grafana Dashboard：14 个面板覆盖辩论数、WebSocket 连接、HTTP 延迟、AI 调用时长等
