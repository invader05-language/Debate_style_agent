# API 参考文档

## 基础信息

- **基础地址**: `http://localhost:8000`
- **API 前缀**: `/api`
- **WebSocket**: `ws://localhost:8000/ws/debate/{debate_id}`
- **在线文档**: Swagger UI (`/docs`) | ReDoc (`/redoc`)

## 辩论端点

### 创建辩论

```
POST /api/debates
```

**请求体:**
```json
{
  "topic": "JWT vs Session Cookies 哪种更适合移动端认证？"
}
```

**响应 (201):**
```json
{
  "id": "uuid",
  "topic": "JWT vs Session Cookies 哪种更适合移动端认证？",
  "status": "pending",
  "created_at": "2026-06-03T12:00:00"
}
```

**错误:**
- `422`: 主题为空或格式错误

### 获取辩论列表

```
GET /api/debates?page=1&page_size=10
```

**查询参数:**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | int | 1 | 页码 |
| page_size | int | 10 | 每页数量 |

**响应 (200):**
```json
{
  "total": 25,
  "page": 1,
  "page_size": 10,
  "debates": [
    {
      "id": "uuid",
      "topic": "...",
      "status": "completed",
      "created_at": "2026-06-03T12:00:00",
      "completed_at": "2026-06-03T12:05:30"
    }
  ]
}
```

### 获取辩论详情

```
GET /api/debates/{debate_id}
```

**响应 (200):**
```json
{
  "id": "uuid",
  "topic": "...",
  "status": "completed",
  "created_at": "2026-06-03T12:00:00",
  "completed_at": "2026-06-03T12:05:30",
  "verdict": {
    "recommendation": "使用 JWT，因为...",
    "winner": "pro",
    "confidence": 0.85,
    "action_plan": ["步骤1", "步骤2"]
  },
  "messages": [
    {
      "round_number": 1,
      "role": "pro",
      "content": "正方观点...",
      "model_used": "mimo-7b"
    }
  ]
}
```

**错误:**
- `404`: 辩论不存在

### 开始辩论

```
POST /api/debates/{debate_id}/start
```

**响应 (200):**
```json
{
  "id": "uuid",
  "status": "running",
  "message": "辩论已开始"
}
```

**错误:**
- `404`: 辩论不存在
- `400`: 辩论状态不是 pending

## 执行端点

### 生成代码并执行

```
POST /api/debates/{debate_id}/generate-code
```

从辩论的 action_plan 自动生成代码并在沙箱中执行。失败时自动重试（AI 修复）。

**请求体:**
```json
{
  "language": "python",
  "max_retries": 3,
  "use_sandbox": true
}
```

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| language | string | "python" | 编程语言 (python/javascript) |
| max_retries | int | 3 | 最大重试次数 |
| use_sandbox | bool | true | 是否使用 Docker 沙箱 |

**响应 (200):**
```json
{
  "id": "exec-uuid",
  "debate_id": "debate-uuid",
  "status": "pending",
  "message": "代码生成和执行已启动"
}
```

**错误:**
- `404`: 辩论不存在
- `409`: 辩论未完成或无 action_plan

### 直接执行代码

```
POST /api/debates/{debate_id}/execute
```

直接执行辩论的 action_plan（不经过 AI 代码生成）。

**查询参数:**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| use_sandbox | bool | true | 是否使用 Docker 沙箱 |

**响应 (200):**
```json
{
  "id": "exec-uuid",
  "debate_id": "debate-uuid",
  "status": "pending",
  "message": "执行已启动"
}
```

### 获取执行结果

```
GET /api/executions/{execution_id}
```

**响应 (200):**
```json
{
  "id": "exec-uuid",
  "debate_id": "debate-uuid",
  "status": "success",
  "code_generated": "print('你好世界')",
  "execution_result": "你好世界\n",
  "error_message": null,
  "created_at": "2026-06-03T12:06:00",
  "completed_at": "2026-06-03T12:06:02"
}
```

**错误:**
- `404`: 执行记录不存在

### 重试执行

```
POST /api/executions/{execution_id}/retry
```

重试失败或已完成的执行。

**响应 (200):**
```json
{
  "id": "exec-uuid",
  "status": "pending",
  "message": "执行重试已启动"
}
```

**错误:**
- `404`: 执行记录不存在
- `400`: 状态不是 failed/success

### 获取辩论的执行记录

```
GET /api/debates/{debate_id}/executions
```

**响应 (200):**
```json
[
  {
    "id": "exec-uuid",
    "debate_id": "debate-uuid",
    "status": "success",
    "code_generated": "...",
    "execution_result": "...",
    "error_message": null,
    "created_at": "2026-06-03T12:06:00",
    "completed_at": "2026-06-03T12:06:02"
  }
]
```

## 记忆端点

### 搜索记忆

```
GET /api/memories/search?q=JWT&limit=5
```

**查询参数:**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| q | string | (必填) | 搜索关键词 |
| limit | int | 10 | 返回数量上限 |

**响应 (200):**
```json
[
  {
    "id": "mem-uuid",
    "topic": "JWT vs Session",
    "debate_summary": "关于认证方式的辩论...",
    "outcome": "推荐使用 JWT",
    "confidence": 0.85,
    "tags": ["JWT", "认证", "安全"],
    "lessons_learned": ["JWT 无状态更利于扩展"],
    "created_at": "2026-06-03T10:00:00"
  }
]
```

### 获取记忆详情

```
GET /api/memories/{memory_id}
```

**响应 (200):**
```json
{
  "id": "mem-uuid",
  "topic": "JWT vs Session",
  "debate_summary": "关于认证方式的辩论...",
  "outcome": "推荐使用 JWT",
  "confidence": 0.85,
  "tags": ["JWT", "认证", "安全"],
  "lessons_learned": ["JWT 无状态更利于扩展"],
  "created_at": "2026-06-03T10:00:00"
}
```

**错误:**
- `404`: 记忆不存在

### 获取记忆列表

```
GET /api/memories?page=1&page_size=10
```

## 系统端点

### 健康检查

```
GET /health
```

**响应 (200):**
```json
{
  "status": "healthy"
}
```

### 根路径

```
GET /
```

**响应 (200):**
```json
{
  "message": "Multi-AI Debate Agent API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

## WebSocket 协议

### 连接地址

```
ws://localhost:8000/ws/debate/{debate_id}
```

### 消息类型

**连接确认:**
```json
{
  "type": "connected",
  "debate_id": "uuid",
  "message": "已连接到辩论房间",
  "timestamp": "2026-06-03T12:00:00"
}
```

**辩论消息 (每轮发言):**
```json
{
  "type": "debate_message",
  "debate_id": "uuid",
  "role": "pro",
  "content": "正方观点详细内容...",
  "round_number": 1,
  "model_used": "mimo-7b",
  "timestamp": "2026-06-03T12:01:00"
}
```

**状态更新:**
```json
{
  "type": "status_update",
  "debate_id": "uuid",
  "status": "completed",
  "message": "辩论已完成",
  "timestamp": "2026-06-03T12:05:30"
}
```

**最终裁决:**
```json
{
  "type": "verdict",
  "debate_id": "uuid",
  "verdict": {
    "recommendation": "推荐使用 JWT...",
    "winner": "pro",
    "confidence": 0.85,
    "key_arguments": ["无状态", "跨域友好"],
    "action_plan": ["步骤1", "步骤2"],
    "lessons_learned": ["JWT 需注意刷新机制"]
  },
  "timestamp": "2026-06-03T12:05:30"
}
```

**心跳:**
```json
// 客户端发送
{"type": "ping"}

// 服务端响应
{"type": "pong", "timestamp": "2026-06-03T12:00:30"}
```

**错误 (JSON 解析失败):**
```json
{
  "type": "error",
  "message": "无效的 JSON 格式"
}
```

## 错误响应格式

所有错误遵循统一格式：

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

### 常见错误码

| HTTP 状态码 | 错误码 | 说明 |
|------------|--------|------|
| 400 | BAD_REQUEST | 请求参数错误 |
| 404 | NOT_FOUND | 资源不存在 |
| 409 | CONFLICT | 状态冲突（如辩论未完成） |
| 422 | VALIDATION_ERROR | 请求体验证失败 |
| 429 | RATE_LIMITED | 请求过于频繁 (60次/分钟) |
| 500 | INTERNAL_ERROR | 服务器内部错误 |
