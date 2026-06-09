# API 使用示例

## 基础信息

- 基础 URL: `http://localhost:8000`
- 认证: Bearer Token (JWT)
- Content-Type: `application/json`

## 认证

### 注册用户

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

响应 (201):
```json
{
  "id": "uuid",
  "username": "testuser",
  "email": "test@example.com",
  "created_at": "2026-06-04T12:00:00"
}
```

### 登录

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

响应 (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 使用 Token 访问受保护端点

```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

## 辩论 API

### 创建辩论

```bash
curl -X POST http://localhost:8000/api/debates \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "JWT vs Session Cookies for authentication"
  }'
```

响应 (201):
```json
{
  "id": "debate-uuid",
  "topic": "JWT vs Session Cookies for authentication",
  "status": "pending",
  "created_at": "2026-06-04T12:00:00"
}
```

### 获取辩论列表

```bash
curl "http://localhost:8000/api/debates?page=1&page_size=10"
```

响应 (200):
```json
{
  "debates": [
    {
      "id": "debate-uuid",
      "topic": "JWT vs Session Cookies",
      "status": "completed",
      "created_at": "2026-06-04T12:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

### 获取辩论详情

```bash
curl http://localhost:8000/api/debates/debate-uuid
```

响应 (200):
```json
{
  "id": "debate-uuid",
  "topic": "JWT vs Session Cookies",
  "status": "completed",
  "messages": [
    {
      "round_number": 1,
      "role": "pro",
      "content": "JWT 支持跨域认证...",
      "model_used": "mimo"
    }
  ],
  "verdict": {
    "recommendation": "建议使用 JWT",
    "winner": "pro",
    "confidence": 0.85,
    "action_plan": ["实现 JWT 中间件", "添加 token 刷新"]
  }
}
```

### 开始辩论

```bash
curl -X POST http://localhost:8000/api/debates/debate-uuid/start
```

响应 (200): 辩论开始，通过 WebSocket 推送实时消息。

### 生成代码并执行

```bash
curl -X POST http://localhost:8000/api/debates/debate-uuid/generate-code \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python"
  }'
```

响应 (202):
```json
{
  "execution_id": "exec-uuid",
  "status": "pending",
  "message": "代码生成任务已提交"
}
```

### 获取执行结果

```bash
curl http://localhost:8000/api/executions/exec-uuid
```

响应 (200):
```json
{
  "id": "exec-uuid",
  "debate_id": "debate-uuid",
  "status": "success",
  "code_generated": "import jwt\n...",
  "execution_result": "JWT middleware implemented successfully",
  "created_at": "2026-06-04T12:00:00"
}
```

### 重试失败的执行

```bash
curl -X POST http://localhost:8000/api/executions/exec-uuid/retry
```

## 记忆 API

### 搜索记忆（语义搜索）

```bash
curl "http://localhost:8000/api/memories/search?q=JWT+authentication&use_semantic=true"
```

响应 (200):
```json
[
  {
    "id": "mem-uuid",
    "topic": "JWT authentication",
    "debate_summary": "JWT won the debate for distributed systems",
    "outcome": "Implemented JWT with refresh tokens",
    "confidence": 0.9,
    "tags": ["auth", "jwt"],
    "lessons_learned": ["JWT is stateless", "Use refresh tokens"],
    "similarity": 0.92
  }
]
```

### 获取记忆列表

```bash
curl "http://localhost:8000/api/memories?page=1&page_size=20"
```

### 创建记忆

```bash
curl -X POST http://localhost:8000/api/memories \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "REST API design patterns",
    "debate_summary": "REST won for CRUD-heavy applications",
    "outcome": "Implemented RESTful API",
    "confidence": 0.85,
    "tags": ["api", "rest", "design"],
    "lessons_learned": ["Use proper HTTP methods", "Version your API"]
  }'
```

### 生成 embedding

```bash
curl -X POST http://localhost:8000/api/memories/mem-uuid/generate-embedding
```

### 批量生成 embedding

```bash
curl -X POST http://localhost:8000/api/memories/generate-all-embeddings
```

## WebSocket

### 连接辩论实时消息

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/debate/debate-uuid');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case 'debate_message':
      console.log(`[${data.role}] ${data.content}`);
      break;
    case 'status_update':
      console.log(`Status: ${data.status}`);
      break;
    case 'verdict':
      console.log('Verdict:', data.verdict);
      break;
  }
};
```

消息类型：

```json
// 辩论消息
{
  "type": "debate_message",
  "role": "pro",
  "content": "JWT 的优势在于...",
  "round_number": 1,
  "model_used": "mimo"
}

// 状态更新
{
  "type": "status_update",
  "status": "running",
  "message": "正在进行第 2 轮辩论"
}

// 裁决结果
{
  "type": "verdict",
  "verdict": {
    "recommendation": "建议使用 JWT",
    "winner": "pro",
    "confidence": 0.85
  }
}
```

## 错误响应

所有错误响应格式：

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "retryable": true,
    "request_id": "uuid"
  }
}
```

常见错误码：

| HTTP 状态码 | 错误码 | 说明 |
|------------|--------|------|
| 400 | VALIDATION_ERROR | 请求参数验证失败 |
| 401 | UNAUTHORIZED | 未认证 |
| 404 | NOT_FOUND | 资源不存在 |
| 409 | CONFLICT | 状态冲突（如辩论已在运行） |
| 429 | RATE_LIMIT_EXCEEDED | 请求过于频繁 |
| 500 | INTERNAL_ERROR | 服务器内部错误 |

## 限流

- 全局默认: 60 请求/分钟
- 辩论创建: 30 请求/分钟
- 代码执行: 10 请求/分钟
- 记忆搜索: 60 请求/分钟

响应头：
```
X-RateLimit-Remaining: 59
X-RateLimit-Limit: 60
```
