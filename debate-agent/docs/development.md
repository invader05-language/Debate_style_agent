# 开发指南

## 项目结构

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
└── scripts/             # 脚本
```

## 开发环境搭建

### 1. 克隆仓库

```bash
git clone https://github.com/invader05-language/Debate_style_agent.git
cd Debate_style_agent
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 安装依赖

```bash
# 后端依赖
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
cd ..
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入 API Keys
```

### 5. 启动开发服务

```bash
# 终端 1: 后端
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 终端 2: 前端
cd frontend
npm start

# 终端 3: 数据库（如果不用 Docker）
docker-compose up -d db redis
```

## 代码规范

### Python

- 遵循 PEP 8
- 使用 type hints
- 使用 `ruff` 进行 linting
- 使用 `black` 格式化代码

```bash
# 检查代码
ruff check .

# 格式化
black .

# 类型检查
mypy .
```

### TypeScript

- 使用 ESLint + Prettier
- 遵循 React 最佳实践
- 使用 TypeScript 严格模式

```bash
cd frontend
npm run lint
npm run format
```

### Commit 规范

使用 Conventional Commits：

```
feat: 添加新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 添加测试
chore: 构建/工具变更
```

## 测试指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_debate.py

# 运行带覆盖率
pytest --cov=. --cov-report=html

# 运行标记的测试
pytest -m unit
pytest -m integration
```

### 编写测试

```python
import pytest
from unittest.mock import AsyncMock

class TestMyFeature:
    """测试我的功能."""

    @pytest.mark.asyncio
    async def test_success_case(self):
        """测试成功场景."""
        # Arrange
        mock_service = AsyncMock()
        mock_service.process.return_value = "success"

        # Act
        result = await my_function(mock_service)

        # Assert
        assert result == "success"
        mock_service.process.assert_called_once()

    @pytest.mark.asyncio
    async def test_error_case(self):
        """测试错误场景."""
        with pytest.raises(ValueError):
            await my_function(invalid_input)
```

### 测试覆盖率

目标：单元测试覆盖率 ≥ 80%

```bash
# 生成覆盖率报告
pytest --cov=. --cov-report=html --cov-report=term-missing

# 查看报告
open htmlcov/index.html
```

## 调试技巧

### 后端调试

```bash
# 启用调试日志
export DEBUG=true
export LOG_LEVEL=DEBUG

# 使用 pdb
import pdb; pdb.set_trace()

# 使用 VS Code 调试器
# 配置 .vscode/launch.json
```

### 前端调试

```bash
# React DevTools
# 浏览器安装 React Developer Tools 扩展

# Redux DevTools（如果使用）
# 浏览器安装 Redux DevTools 扩展
```

### 数据库调试

```bash
# 进入数据库 Shell
make db-shell

# 查看表结构
\d debates
\d messages
\d memories

# 查看数据
SELECT * FROM debates ORDER BY created_at DESC LIMIT 10;
```

### WebSocket 调试

```bash
# 使用 wscat 测试 WebSocket
npm install -g wscat
wscat -c ws://localhost:8000/ws/debate/test-debate-id

# 发送消息
{"type": "ping"}
```

## 常见问题

### 循环导入

如果遇到循环导入问题：
1. 使用 `TYPE_CHECKING` 进行类型提示
2. 使用延迟导入（在函数内导入）
3. 重新组织模块结构

### 异步测试

确保使用 `pytest-asyncio`：
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### 数据库连接池

如果遇到连接池耗尽：
```python
# 调整连接池配置
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30
)
```
