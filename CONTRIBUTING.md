# Contributing to Multi-AI Debate Agent

感谢你对本项目的关注！以下是参与贡献的指南。

## 开发环境搭建

```bash
# 克隆仓库
git clone https://github.com/invader05-language/Debate_style_agent.git
cd Debate_style_agent

# 后端依赖
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
cd ..

# 启动数据库
docker-compose up -d postgres redis

# 数据库迁移
python scripts/migrate.py upgrade

# 启动开发服务器
uvicorn backend.main:app --reload
```

## 代码规范

### Python

- 遵循 PEP 8 规范
- 使用 type hints
- 异步函数使用 `async/await`
- 使用 `logging` 模块记录日志，不要用 `print`

### TypeScript / React

- 使用 TypeScript 严格模式
- 组件使用函数式组件 + Hooks
- 样式使用 Tailwind CSS
- 遵循 ESLint 规则

## 提交规范

使用 Conventional Commits 格式：

```
<type>(<scope>): <description>

[optional body]
[optional footer]
```

类型：
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具链

示例：
```
feat(memory): add pgvector semantic search
fix(websocket): handle broken connections gracefully
docs(readme): update API endpoint table
```

## 分支策略

- `master`: 稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `fix/*`: 修复分支

## 测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_debate.py

# 运行带覆盖率的测试
pytest --cov=backend --cov=agents --cov=debate

# 前端测试
cd frontend
npm test
```

## Pull Request 流程

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### PR 要求

- 描述清楚改了什么、为什么改
- 关联相关 Issue
- 确保所有测试通过
- 更新相关文档
- 保持 PR 范围小而聚焦

## 报告 Bug

使用 Issue 模板报告 Bug，包含：
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（OS, Python 版本, Node 版本）

## 功能建议

欢迎通过 Issue 提出功能建议，请说明：
- 使用场景
- 预期行为
- 可能的实现方案

## 代码审查

所有代码都需要经过审查才能合并。审查关注点：
- 代码正确性
- 测试覆盖
- 性能影响
- 安全考虑
- 代码风格一致性

## 许可证

贡献即表示你同意你的代码以 MIT 许可证发布。
