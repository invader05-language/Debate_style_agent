# Multi-AI Debate Agent

一个基于多AI协作的辩论系统，让不同AI模型以"辩论赛"模式互相讨论，形成更优方案。

## 功能特性

- **AI 辩论赛模式** - 不同AI针对同一个问题互相挑战，形成对抗性思维
- **三阶段自动化** - 讨论阶段 → 决策阶段 → 执行阶段
- **记忆进化** - 系统记住每次讨论的结论和执行结果，形成知识库
- **多模型支持** - 支持 MIMO、DeepSeek 等多个AI模型

## 技术栈

- **Python 3.11+**
- **AutoGen** - 多Agent协作框架
- **FastAPI** - Web框架
- **PostgreSQL** - 数据库
- **React** - 前端框架
- **WebSocket** - 实时通信

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并填写配置：

```bash
cp .env.example .env
```

### 3. 初始化数据库

```bash
# 创建数据库
createdb debate_agent

# 运行数据库迁移
alembic upgrade head
```

### 4. 运行CLI

```bash
# 开始辩论
python main.py start "设计一个用户登录系统"

# 查看历史
python main.py history

# 查看记忆
python main.py memories
```

## 项目结构

```
debate-agent/
├── main.py                    # CLI 入口
├── config.py                  # 配置管理
├── database.py                # 数据库连接
├── debate/                    # 辩论模块
│   ├── engine.py              # 辩论引擎
│   ├── protocol.py            # 辩论协议
│   └── roles.py               # 角色定义
├── agents/                    # AI模型模块
│   ├── base_agent.py          # 基础Agent
│   ├── mimo_agent.py          # MIMO模型
│   └── deepseek_agent.py      # DeepSeek模型
├── memory/                    # 记忆模块
│   └── store.py               # 记忆存储
├── execution/                 # 执行模块
│   └── executor.py            # 代码执行器
├── prompts/                   # Prompt模板
│   └── templates.py           # 模板定义
└── tests/                     # 测试
    ├── test_debate.py
    ├── test_memory.py
    └── test_executor.py
```

## 开发计划

### Phase 1: CLI MVP (Week 1-2)
- [x] 项目结构搭建
- [x] 辩论引擎核心逻辑
- [x] Agent封装（MIMO/DeepSeek）
- [x] 记忆系统
- [x] CLI界面

### Phase 2: Web Full Stack (Week 3-4)
- [ ] FastAPI后端
- [ ] WebSocket实时通信
- [ ] React前端
- [ ] Redis缓存
- [ ] 集成测试

## 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_debate.py

# 运行测试并生成覆盖率报告
pytest --cov=.
```

## 许可证

MIT License
