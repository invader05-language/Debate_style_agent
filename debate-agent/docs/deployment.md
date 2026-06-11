# 部署指南

## Docker 部署（推荐）

### 前置条件

- Docker Engine 20.10+
- Docker Compose v2.0+
- MIMO API Key
- DeepSeek API Key

### 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 必填
MIMO_API_KEY=your_mimo_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key

# 可选
MIMO_API_URL=https://api.mimo.com/v1
DEEPSEEK_API_URL=https://api.deepseek.com/v1
DEBUG=false
LOG_LEVEL=INFO
```

### 启动服务

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend

# 检查状态
docker-compose ps
```

### 验证部署

```bash
# 检查后端健康
curl http://localhost:8000/health

# 检查前端
curl http://localhost:3000

# 检查 API 文档
open http://localhost:8000/docs
```

## 手动部署

### Python 环境准备

```bash
# Python 3.11+
python --version

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### PostgreSQL 安装配置

```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# 创建数据库
sudo -u postgres psql
CREATE DATABASE debate_agent;
CREATE USER debate_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE debate_user TO debate_agent;
\q

# 启用 pgvector 扩展
sudo -u postgres psql -d debate_agent -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### 数据库迁移（Alembic）

使用 Alembic 管理数据库 schema：

```bash
# 升级到最新版本
python scripts/migrate.py upgrade

# 查看当前版本
python scripts/migrate.py current

# 查看迁移历史
python scripts/migrate.py history

# 降级到指定版本
python scripts/migrate.py downgrade <revision>

# 检查是否有待执行的迁移
python scripts/migrate.py check
```

迁移文件位于 `alembic/versions/`，初始迁移创建以下表：
- `users` - 用户认证表
- `debates` - 辩论记录表
- `messages` - 辩论消息表
- `memories` - 记忆存储表（含 pgvector embedding）
- `executions` - 代码执行记录表

### Redis 安装配置

```bash
# Ubuntu/Debian
sudo apt install redis-server

# 启动 Redis
sudo systemctl start redis
sudo systemctl enable redis

# 测试连接
redis-cli ping
```

### 应用启动

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

## 生产环境建议

### Nginx 反向代理

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

### HTTPS 配置

```bash
# 使用 Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 日志收集

```bash
# 查看结构化日志
docker-compose logs -f backend | jq .

# 日志轮转（logrotate）
sudo vim /etc/logrotate.d/debate-agent
```

### 监控告警

项目内置 Prometheus + Grafana 监控栈：

```bash
# 启动监控服务
docker-compose up -d prometheus grafana redis-exporter

# 访问 Grafana
open http://localhost:3001
# 默认账号: admin / admin
```

- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001` (自动配置 Prometheus 数据源)
- Redis Exporter: `http://localhost:9121`
- 指标端点: `GET /metrics`
- 健康检查: `GET /health` (含 Redis 连接状态和延迟)

Grafana Dashboard 自动加载，包含 14 个面板：
- 活跃辩论数、WebSocket 连接数
- HTTP 请求速率、p95 延迟
- AI Agent 请求时长、降级事件
- 记忆搜索速率、缓存命中率
- 代码执行统计、限流命中

### 备份策略

```bash
# 数据库备份
pg_dump -U postgres debate_agent > backup_$(date +%Y%m%d).sql

# 恢复
psql -U postgres debate_agent < backup_20260603.sql
```

## 常见部署问题

### 数据库连接失败

检查 PostgreSQL 是否运行：
```bash
sudo systemctl status postgresql
pg_isready -h localhost -p 5432
```

### Redis 连接失败

检查 Redis 是否运行：
```bash
sudo systemctl status redis
redis-cli ping
```

### 端口被占用

```bash
# 查看端口占用
lsof -i :8000
lsof -i :3000

# 杀死进程
kill -9 <PID>
```

### Docker 构建失败

```bash
# 清理缓存
docker-compose build --no-cache

# 清理所有容器
docker-compose down -v
```

### Alembic 迁移失败

```bash
# 查看当前数据库版本
python scripts/migrate.py current

# 手动修复后标记为最新
python scripts/migrate.py upgrade head

# 回滚并重新执行
python scripts/migrate.py downgrade -1
python scripts/migrate.py upgrade
```
