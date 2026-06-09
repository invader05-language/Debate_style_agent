# Multi-AI Platform UI 设计规范

> 本文档为前端 UI 实现的完整设计规范，供 UI 设计 AI 或前端开发者参考。
> 基于现有 Tailwind CSS 代码风格，扩展为完整的 v2.0 多 AI 平台。

***

## 一、设计原则

1. **简洁优先** — 界面干净，信息层次分明，不堆砌元素
2. **功能导向** — 每个页面有且仅有一个核心任务
3. **渐进展示** — 复杂信息分层展示，用户按需展开
4. **一致性** — 相同功能使用相同组件，减少认知负担
5. **响应式** — 桌面优先，兼顾平板（≥768px）

***

## 二、设计系统（Design Tokens）

### 2.1 色彩系统

#### 主色调（Brand Colors）

| Token                 | 用途          | Tailwind Class                | Hex       |
| --------------------- | ----------- | ----------------------------- | --------- |
| `brand-primary`       | 主按钮、链接、活跃状态 | `blue-500`                    | `#3B82F6` |
| `brand-primary-hover` | 悬停态         | `blue-600`                    | `#2563EB` |
| `brand-secondary`     | 渐变终点、强调     | `purple-500`                  | `#8B5CF6` |
| `brand-gradient`      | Logo、标题渐变   | `from-blue-500 to-purple-500` | —         |

#### 语义色彩（Semantic Colors）

| Token            | 用途        | Tailwind Class | Hex       |
| ---------------- | --------- | -------------- | --------- |
| `success`        | 成功状态、连接在线 | `green-500`    | `#22C55E` |
| `success-bg`     | 成功背景      | `green-50`     | `#F0FDF4` |
| `success-border` | 成功边框      | `green-200`    | `#BBF7D0` |
| `success-text`   | 成功文字      | `green-700`    | `#15803D` |
| `error`          | 错误状态      | `red-500`      | `#EF4444` |
| `error-bg`       | 错误背景      | `red-50`       | `#FEF2F2` |
| `error-border`   | 错误边框      | `red-200`      | `#FECACA` |
| `error-text`     | 错误文字      | `red-700`      | `#B91C1C` |
| `warning`        | 警告状态      | `yellow-500`   | `#EAB308` |
| `warning-bg`     | 警告背景      | `yellow-50`    | `#FEFCE8` |
| `warning-border` | 警告边框      | `yellow-200`   | `#FEF08A` |
| `warning-text`   | 警告文字      | `yellow-700`   | `#A16207` |
| `info`           | 信息提示      | `blue-500`     | `#3B82F6` |
| `info-bg`        | 信息背景      | `blue-50`      | `#EFF6FF` |

#### 辩论角色色彩（Role Colors）

| 角色                | 背景          | 边框           | 文字           | 头像              |
| ----------------- | ----------- | ------------ | ------------ | --------------- |
| 正方 (Pro)          | `green-50`  | `green-200`  | `green-700`  | `green-500` 背景  |
| 反方 (Con)          | `red-50`    | `red-200`    | `red-700`    | `red-500` 背景    |
| 裁判 (Judge)        | `yellow-50` | `yellow-200` | `yellow-700` | `yellow-500` 背景 |
| 思考者 (Thinker)     | `blue-50`   | `blue-200`   | `blue-700`   | `blue-500` 背景   |
| 综合者 (Synthesizer) | `purple-50` | `purple-200` | `purple-700` | `purple-500` 背景 |

#### 中性色（Neutral）

| Token            | Tailwind Class | Hex       | 用途         |
| ---------------- | -------------- | --------- | ---------- |
| `bg-page`        | `gray-50`      | `#F9FAFB` | 页面背景       |
| `bg-card`        | `white`        | `#FFFFFF` | 卡片背景       |
| `bg-code`        | `gray-900`     | `#111827` | 代码块背景      |
| `border-default` | `gray-200`     | `#E5E7EB` | 默认边框       |
| `border-light`   | `gray-100`     | `#F3F4F6` | 轻边框（分割线）   |
| `text-primary`   | `gray-900`     | `#111827` | 主文字        |
| `text-secondary` | `gray-600`     | `#4B5563` | 次要文字       |
| `text-tertiary`  | `gray-400`     | `#9CA3AF` | 辅助文字（时间戳等） |

### 2.2 字体系统（Typography）

#### 字体族

```css
font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
```

#### 字号层级

| Token       | 大小                 | 行高          | 字重              | 用途          |
| ----------- | ------------------ | ----------- | --------------- | ----------- |
| `heading-1` | `text-2xl` (24px)  | `leading-8` | `font-bold`     | 页面标题        |
| `heading-2` | `text-xl` (20px)   | `leading-7` | `font-semibold` | 区域标题        |
| `heading-3` | `text-lg` (18px)   | `leading-7` | `font-semibold` | 卡片标题        |
| `body`      | `text-sm` (14px)   | `leading-6` | `font-normal`   | 正文内容        |
| `body-lg`   | `text-base` (16px) | `leading-6` | `font-normal`   | 大段阅读文字      |
| `caption`   | `text-xs` (12px)   | `leading-4` | `font-normal`   | 时间戳、标签、辅助信息 |
| `label`     | `text-sm` (14px)   | `leading-5` | `font-medium`   | 表单标签        |
| `code`      | `text-sm` (14px)   | `leading-6` | `font-mono`     | 代码块         |

### 2.3 间距系统（Spacing）

| Token            | 值                             | 用途      |
| ---------------- | ----------------------------- | ------- |
| `page-padding-x` | `px-4` (16px) / `px-6` (24px) | 页面左右内边距 |
| `section-gap`    | `gap-6` (24px)                | 区域间距    |
| `card-padding`   | `p-4` (16px) / `p-6` (24px)   | 卡片内边距   |
| `element-gap`    | `gap-3` (12px)                | 元素间距    |
| `tight-gap`      | `gap-2` (8px)                 | 紧凑元素间距  |
| `container-max`  | `max-w-7xl` (1280px)          | 最大内容宽度  |

### 2.4 圆角与阴影

| Token           | 值                    | 用途      |
| --------------- | -------------------- | ------- |
| `radius-card`   | `rounded-xl` (12px)  | 卡片圆角    |
| `radius-button` | `rounded-lg` (8px)   | 按钮圆角    |
| `radius-badge`  | `rounded-full`       | 标签/头像圆角 |
| `radius-bubble` | `rounded-2xl` (16px) | 消息气泡圆角  |
| `shadow-sm`     | `shadow-sm`          | 默认卡片阴影  |
| `shadow-hover`  | `hover:shadow-md`    | 卡片悬停阴影  |
| `shadow-modal`  | `shadow-xl`          | 弹窗阴影    |

***

## 三、页面结构

### 3.1 全局布局

```
┌─────────────────────────────────────────────────────────────┐
│  Header (sticky top-0, bg-white, border-b border-gray-100)  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Logo + 标题     [导航链接1] [导航链接2] ...    [设置] │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Main Content (max-w-7xl mx-auto px-4/6 py-6)              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                                                      │   │
│  │                 页面内容区域                          │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

#### Header 规范

- **高度**: `h-16` (64px)
- **背景**: `bg-white`
- **底部边框**: `border-b border-gray-100`
- **定位**: `sticky top-0 z-50`
- **Logo**: 蓝紫渐变图标 (`from-blue-500 to-purple-500`)，`w-8 h-8 rounded-lg`
- **标题**: "Multi-AI Platform"，`text-lg font-semibold text-gray-900`
- **副标题**: "AI 辩论协作系统"，`text-xs text-gray-500`
- **导航**: 水平链接，`text-sm`，当前页 `text-blue-600 font-medium`，其他 `text-gray-600 hover:text-gray-900`

#### 导航项

| 名称   | 路由            | 图标建议                    |
| ---- | ------------- | ----------------------- |
| 首页   | `/`           | HomeIcon                |
| 辩论   | `/debate/new` | ChatBubbleLeftRightIcon |
| 独立思考 | `/think/new`  | LightBulbIcon           |
| 模型管理 | `/models`     | CpuChipIcon             |
| 历史记录 | `/history`    | ClockIcon               |
| 记忆库  | `/memories`   | ArchiveBoxIcon          |

***

## 四、页面设计

### 4.1 首页（Dashboard）

**路由**: `/`

**功能**: 快速入口 + 最近活动概览

**布局**:

```
┌─────────────────────────────────────────────────────────┐
│  欢迎语 "你好，开始你的 AI 协作之旅"                      │
│  subtitle: "选择一种模式开始"                             │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐             │
│  │  🎯 AI 辩论模式   │  │  💡 独立思考模式  │             │
│  │                  │  │                  │             │
│  │  多个AI针对问题   │  │  多个AI独立分析   │             │
│  │  互相辩论挑战    │  │  综合裁判汇总    │             │
│  │                  │  │                  │             │
│  │  [开始辩论 →]    │  │  [开始思考 →]    │             │
│  └──────────────────┘  └──────────────────┘             │
├─────────────────────────────────────────────────────────┤
│  最近活动                                                │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 辩论: 用户登录方案  │ 已完成 │ 2小时前 │ [查看]  │    │
│  │ 思考: 架构选型分析  │ 进行中 │ 5分钟前 │ [查看]  │    │
│  │ 辩论: 数据库设计    │ 已完成 │ 昨天    │ [查看]  │    │
│  └─────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│  模型状态                                                │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐           │
│  │ MIMO   │ │DeepSeek│ │ Claude │ │ GPT-4o │           │
│  │ ● 在线  │ │ ● 在线  │ │ ○ 离线  │ │ ○ 离线  │           │
│  └────────┘ └────────┘ └────────┘ └────────┘           │
└─────────────────────────────────────────────────────────┘
```

**模式选择卡片规范**:

- 容器: `grid grid-cols-1 md:grid-cols-2 gap-6`
- 卡片: `bg-white rounded-xl p-6 shadow-sm hover:shadow-md cursor-pointer transition-all border border-gray-100`
- 标题: `text-lg font-semibold text-gray-900`
- 描述: `text-sm text-gray-600 mt-2`
- 按钮: `mt-4 text-sm font-medium text-blue-600 hover:text-blue-700`

**最近活动列表规范**:

- 容器: `bg-white rounded-xl shadow-sm border border-gray-100`
- 每行: `flex items-center justify-between px-4 py-3 border-b border-gray-50 hover:bg-gray-50`
- 状态标签: `rounded-full px-2 py-0.5 text-xs font-medium`
  - 已完成: `bg-green-50 text-green-700`
  - 进行中: `bg-blue-50 text-blue-700`
  - 失败: `bg-red-50 text-red-700`

**模型状态卡片规范**:

- 容器: `grid grid-cols-2 md:grid-cols-4 gap-3`
- 卡片: `bg-white rounded-lg p-3 border border-gray-100 text-center`
- 在线指示: `w-2 h-2 rounded-full bg-green-500 inline-block`
- 离线指示: `w-2 h-2 rounded-full bg-gray-300 inline-block`

***

### 4.2 辩论页面（Debate Page）

**路由**: `/debate/new`（新建），`/debate/:id`（进行中/结果）

**功能**: 创建辩论任务 → 实时观看辩论 → 查看结果 → 确认执行

**布局 — 创建阶段**:

```
┌─────────────────────────────────────────────────────────┐
│  🎯 创建辩论任务                                         │
├─────────────────────────────────────────────────────────┤
│  辩论主题                                                │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 输入你想讨论的问题...                              │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  选择模型                                                │
│  正方: [MIMO v2.5 Pro ▼]   反方: [DeepSeek V4 ▼]       │
│  裁判: [Claude Sonnet 4 ▼]                              │
│                                                         │
│  辩论设置                                                │
│  轮次: [3] 轮    (slider: 1-10)                          │
│                                                         │
│  [开始辩论]                                              │
└─────────────────────────────────────────────────────────┘
```

**布局 — 进行中阶段**:

```
┌─────────────────────────────────────────────────────────┐
│  状态栏: ● WebSocket 已连接 │ 状态: 辩论进行中           │
├─────────────────────────────────────────────────────────┤
│  RoundProgress: [●1] ─── [●2] ─── [○3]                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ── 第 1 轮 ──                                          │
│                                                         │
│  ┌─ 正方 (MIMO) ──────────────────────┐                 │
│  │ A  我认为应该使用 JWT...            │                 │
│  │    置信度: ████████░░ 80%           │                 │
│  └────────────────────────────────────┘                 │
│                                                         │
│           ┌─ 反方 (DeepSeek) ──────────────────────┐    │
│           │ B  我不同意，Session 更安全...           │    │
│           │    置信度: ███████░░░ 70%               │    │
│           └────────────────────────────────────────┘    │
│                                                         │
│  ── 第 2 轮 ──                                          │
│  ...                                                    │
│                                                         │
│  ┌─ 裁判 (Claude) ─────────────────────┐                │
│  │ J  综合双方观点，我建议...            │                │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ⏳ AI 正在思考... ● ● ●                                │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  用户引导（可折叠）                                       │
│  ┌─────────────────────────────────────┐ [发送引导语]   │
│  │ 输入引导语来影响辩论方向...           │                │
│  └─────────────────────────────────────┘                │
│  [暂停辩论]                                              │
└─────────────────────────────────────────────────────────┘
```

**布局 — 结果阶段**:

```
┌─────────────────────────────────────────────────────────┐
│  ✅ 辩论完成                                             │
├─────────────────────────────────────────────────────────┤
│  VerdictCard                                             │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 🏆 正方获胜                                      │    │
│  │ 推荐方案: 使用 JWT + Refresh Token 方案           │    │
│  │ 置信度: █████████░ 85%                           │    │
│  │                                                  │    │
│  │ 执行计划:                                        │    │
│  │ 1. 安装 jsonwebtoken 依赖                        │    │
│  │ 2. 创建 JWT 中间件                               │    │
│  │ 3. 实现 Token 刷新机制                           │    │
│  │ 4. 编写单元测试                                  │    │
│  │                                                  │    │
│  │ [确认执行]  [重新辩论]                            │    │
│  └─────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│  ExecutionPanel（点击"确认执行"后出现）                    │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 执行状态: 运行中                                  │    │
│  │ ┌──────────────────────────────────────────┐    │    │
│  │ │ $ npm install jsonwebtoken               │    │    │
│  │ │ added 3 packages in 2s                   │    │    │
│  │ │ $ node src/middleware/jwt.js              │    │    │
│  │ │ ✅ All tests passed                       │    │    │
│  │ └──────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**组件规范**:

**主题输入框**:

- 容器: `bg-white rounded-xl p-6 shadow-sm border border-gray-100`
- 标签: `text-sm font-medium text-gray-700 mb-2`
- 输入框: `w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm placeholder-gray-400`
- 最小高度: `min-h-[80px]`（textarea）

**模型选择器**:

- 每个角色一行: `flex items-center gap-3`
- 标签宽度固定: `w-16 text-sm font-medium text-gray-700`
- 下拉框: `flex-1 px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white`

**轮次滑块**:

- 使用 `<input type="range">`，自定义样式
- 当前值显示: `text-lg font-semibold text-blue-600`
- 范围标签: `text-xs text-gray-400`

**开始按钮**:

- `w-full py-3 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg transition-colors shadow-sm`

**连接状态栏**:

- `flex items-center gap-2 px-4 py-2 bg-gray-50 rounded-lg text-xs`
- 在线: `w-2 h-2 rounded-full bg-green-500 animate-pulse`
- 离线: `w-2 h-2 rounded-full bg-red-400`

**用户引导区**:

- 可折叠容器，默认收起
- 输入框: `flex-1 px-3 py-2 border border-gray-200 rounded-lg text-sm`
- 发送按钮: `px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm`
- 暂停按钮: `px-4 py-2 bg-yellow-50 hover:bg-yellow-100 text-yellow-700 border border-yellow-200 rounded-lg text-sm`

***

### 4.3 独立思考页面（Think Page）

**路由**: `/think/new`（新建），`/think/:id`（进行中/结果）

**功能**: 多 AI 独立分析同一问题 → 综合裁判汇总

**布局 — 创建阶段**:

```
┌─────────────────────────────────────────────────────────┐
│  💡 创建独立思考任务                                      │
├─────────────────────────────────────────────────────────┤
│  问题描述                                                │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 输入你想让 AI 分析的问题...                        │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  选择思考者（至少2个）                                    │
│  ☑ MIMO v2.5 Pro    ☑ DeepSeek V4                      │
│  ☐ Claude Sonnet 4  ☐ GPT-4o                           │
│                                                         │
│  综合裁判                                                │
│  [Claude Sonnet 4 ▼] （从未参与思考的模型中选择）          │
│                                                         │
│  [开始思考]                                              │
└─────────────────────────────────────────────────────────┘
```

**布局 — 进行中阶段**:

```
┌─────────────────────────────────────────────────────────┐
│  阶段 1/2: 独立思考中                                     │
├─────────────────────────────────────────────────────────┤
│  进度指示器                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ MIMO     │  │ DeepSeek │  │ Claude   │              │
│  │ ⏳ 思考中 │  │ ✅ 已完成 │  │ ⏳ 思考中 │              │
│  │ ● ● ●   │  │          │  │ ● ● ●   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
├─────────────────────────────────────────────────────────┤
│  各 AI 思考结果（实时流式展示，逐个出现）                    │
│                                                         │
│  ┌─ MIMO v2.5 Pro ─────────────────────────┐            │
│  │ 分析: ...                               │            │
│  │ 优点: 1. ... 2. ...                     │            │
│  │ 缺点: 1. ... 2. ...                     │            │
│  │ 建议: ...                               │            │
│  │ 置信度: ████████░░ 80%                   │            │
│  │ 关键洞察: ...                            │            │
│  └─────────────────────────────────────────┘            │
│                                                         │
│  ┌─ DeepSeek V4 ───────────────────────────┐            │
│  │ ...                                     │            │
│  └─────────────────────────────────────────┘            │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  阶段 2/2: 综合决策                                       │
│  ┌─ 裁判: Claude Sonnet 4 ─────────────────┐            │
│  │ ⏳ 综合分析中...                          │            │
│  └─────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────┘
```

**布局 — 结果阶段**:

```
┌─────────────────────────────────────────────────────────┐
│  ✅ 思考完成                                             │
├─────────────────────────────────────────────────────────┤
│  综合结果 (SynthesisCard)                                │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 🧠 综合分析 — Claude Sonnet 4                    │    │
│  │                                                  │    │
│  │ 总结: 综合所有分析后...                           │    │
│  │                                                  │    │
│  │ ✅ 共识点:                                       │    │
│  │ • 所有AI都认为应使用微服务架构                    │    │
│  │ • 所有AI都建议先做MVP                            │    │
│  │                                                  │    │
│  │ ⚠️ 分歧点:                                       │    │
│  │ • MIMO建议REST，DeepSeek建议GraphQL              │    │
│  │ • 数据库选择存在分歧                              │    │
│  │                                                  │    │
│  │ 最终建议: ...                                    │    │
│  │ 置信度: █████████░ 90%                           │    │
│  │                                                  │    │
│  │ 执行计划:                                        │    │
│  │ 1. ...                                          │    │
│  │ 2. ...                                          │    │
│  │ 3. ...                                          │    │
│  │                                                  │    │
│  │ 最佳洞察: "..." — 来自 DeepSeek V4               │    │
│  │                                                  │    │
│  │ [确认执行]  [重新思考]                            │    │
│  └─────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│  各 AI 独立思考详情（可折叠展开）                          │
│  [▸ MIMO v2.5 Pro 的分析]                               │
│  [▸ DeepSeek V4 的分析]                                 │
└─────────────────────────────────────────────────────────┘
```

**思考者卡片规范**:

- 容器: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4`
- 卡片: `bg-white rounded-xl p-4 shadow-sm border border-gray-100`
- 状态指示:
  - 等待中: 灰色图标 + "等待中"
  - 思考中: 蓝色脉冲图标 + "思考中" + 跳动点动画
  - 已完成: 绿色勾号 + "已完成"
- 结果区域: `text-sm text-gray-700 leading-relaxed`
- 结构化字段标签: `text-xs font-medium text-gray-500 uppercase tracking-wide`

**SynthesisCard 规范**:

- 容器: `bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden`
- 头部: `bg-gradient-to-r from-purple-500 to-blue-500 px-6 py-4 text-white`
  - 标题: `text-lg font-semibold`
  - 副标题: `text-sm opacity-90`
- 内容区: `p-6 space-y-4`
- 共识/分歧标签:
  - 共识: `inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-green-50 text-green-700 text-xs`
  - 分歧: `inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-yellow-50 text-yellow-700 text-xs`
- 置信度条: `h-2 bg-gray-100 rounded-full overflow-hidden`
  - 填充: `h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full`
- 最佳洞察: `p-3 bg-blue-50 rounded-lg border border-blue-100 text-sm text-blue-800 italic`

***

### 4.4 模型管理页面（Models Page）

**路由**: `/models`

**功能**: 添加、编辑、删除、测试 AI 模型配置

**布局**:

```
┌─────────────────────────────────────────────────────────┐
│  AI 模型管理                              [+ 添加模型]    │
├─────────────────────────────────────────────────────────┤
│  预置模型                                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ MIMO     │ │ DeepSeek │ │ Claude   │ │ GPT-4o   │   │
│  │ V2.5 Pro │ │ V4       │ │ Sonnet 4 │ │          │   │
│  │          │ │          │ │          │ │          │   │
│  │ OpenAI   │ │ OpenAI   │ │Anthropic │ │ OpenAI   │   │
│  │ ● 已启用  │ │ ● 已启用  │ │ ○ 已禁用 │ │ ○ 已禁用 │   │
│  │          │ │          │ │          │ │          │   │
│  │[测试连接] │ │[测试连接] │ │[启用]    │ │[启用]    │   │
│  │[编辑]    │ │[编辑]    │ │[编辑]    │ │[编辑]    │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│                                                         │
│  ┌──────────┐                                          │
│  │ Gemini   │                                          │
│  │ 2.5 Pro  │                                          │
│  │ Gemini   │                                          │
│  │ ○ 已禁用  │                                          │
│  │[启用]    │                                          │
│  │[编辑]    │                                          │
│  └──────────┘                                          │
├─────────────────────────────────────────────────────────┤
│  自定义模型                                [+ 添加模型]   │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 暂无自定义模型，点击右上角添加                      │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**模型卡片规范**:

- 容器: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4`
- 卡片: `bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow`
- 模型名称: `text-base font-semibold text-gray-900`
- 供应商: `text-xs text-gray-500 mt-0.5`
- API格式标签: `inline-block px-2 py-0.5 rounded bg-gray-100 text-xs text-gray-600 mt-2`
- 状态开关: 使用 toggle 组件
  - 启用: `bg-green-500`
  - 禁用: `bg-gray-300`
- 测试连接按钮: `text-xs text-blue-600 hover:text-blue-700`
  - 测试中: 转圈动画 + "测试中..."
  - 成功: 绿色勾号 + "连接成功"
  - 失败: 红色叉号 + "连接失败"
- 编辑按钮: `text-xs text-gray-500 hover:text-gray-700`
- 删除按钮: `text-xs text-red-500 hover:text-red-700`（预置模型不显示）

**添加/编辑模型弹窗（Modal）**:

```
┌─────────────────────────────────────────────┐
│  添加 AI 模型                        [✕]    │
├─────────────────────────────────────────────┤
│                                             │
│  模型名称 *                                  │
│  [________________]                         │
│                                             │
│  供应商 *                                    │
│  [________________]                         │
│                                             │
│  模型标识 *                                  │
│  [________________]                         │
│                                             │
│  API 地址 *                                 │
│  [________________]                         │
│                                             │
│  API Key *                                  │
│  [________________] [👁 显示/隐藏]           │
│                                             │
│  API 格式                                   │
│  (●) OpenAI  ( ) Anthropic  ( ) Gemini     │
│                                             │
│  高级设置（可折叠）                           │
│  ├─ 最大 Token: [4096]                      │
│  └─ Temperature: [0.7]                      │
│                                             │
│         [取消]  [保存]                       │
└─────────────────────────────────────────────┘
```

**弹窗规范**:

- 背景遮罩: `fixed inset-0 bg-black/50 z-50`
- 弹窗: `bg-white rounded-xl shadow-xl max-w-lg w-full mx-4`
- 头部: `px-6 py-4 border-b border-gray-100`
- 内容: `px-6 py-4 space-y-4`
- 底部: `px-6 py-4 border-t border-gray-100 flex justify-end gap-3`
- 表单输入: `w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent`
- 标签: `text-sm font-medium text-gray-700 mb-1`
- 必填标记: `text-red-500`

***

### 4.5 历史记录页面（History Page）

**路由**: `/history`

**功能**: 查看所有历史辩论和思考任务

**布局**:

```
┌─────────────────────────────────────────────────────────┐
│  历史记录                                                │
│                                                         │
│  筛选: [全部 ▼] [辩论] [思考]    搜索: [____________]    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 🎯 用户登录方案设计          │ 辩论 │ 已完成     │    │
│  │    正方: MIMO vs 反方: DeepSeek │ 3轮 │ 2小时前   │    │
│  │    [查看详情]  [重新辩论]     │      │           │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ 💡 微服务架构选型            │ 思考 │ 已完成     │    │
│  │    思考者: MIMO, DeepSeek    │ 裁判: Claude    │    │
│  │    [查看详情]  [重新思考]     │      │ 昨天      │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ 🎯 数据库设计方案            │ 辩论 │ 进行中     │    │
│  │    正方: Claude vs 反方: MIMO │ 2/3 │ 5分钟前   │    │
│  │    [继续查看]                 │      │           │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  加载更多...                                            │
└─────────────────────────────────────────────────────────┘
```

**历史记录卡片规范**:

- 容器: `space-y-3`
- 卡片: `bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer`
- 标题: `text-base font-semibold text-gray-900`
- 类型标签:
  - 辩论: `px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 text-xs`
  - 思考: `px-2 py-0.5 rounded-full bg-purple-50 text-purple-700 text-xs`
- 状态标签: 同首页活动列表
- 元信息: `text-xs text-gray-500`
- 操作按钮: `text-sm text-blue-600 hover:text-blue-700`
- 分页: 底部"加载更多"按钮或无限滚动

***

### 4.6 记忆库页面（Memory Page）

**路由**: `/memories`

**功能**: 查看和管理系统积累的知识记忆

**布局**:

```
┌─────────────────────────────────────────────────────────┐
│  记忆库                                    [导出记忆]    │
│                                                         │
│  搜索: [____________]    标签筛选: [认证] [安全] [×]     │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 📝 JWT vs Session 认证方案                       │    │
│  │    2026-06-03 │ 置信度: 90% │ 来源: 辩论         │    │
│  │    结论: JWT更适合分布式系统                      │    │
│  │    标签: [认证] [安全] [JWT]                     │    │
│  │    经验教训:                                    │    │
│  │    • JWT更适合分布式系统                         │    │
│  │    • Session需要额外存储                         │    │
│  │    [查看详情]  [删除]                            │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ 📝 微服务通信方案选择                             │    │
│  │    2026-06-02 │ 置信度: 85% │ 来源: 思考         │    │
│  │    结论: gRPC适合内部通信，REST适合外部API        │    │
│  │    标签: [微服务] [通信] [gRPC]                  │    │
│  │    [查看详情]  [删除]                            │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**记忆卡片规范**:

- 容器: `space-y-3`
- 卡片: `bg-white rounded-xl p-4 shadow-sm border border-gray-100`
- 标题: `text-base font-semibold text-gray-900`
- 元信息行: `flex items-center gap-3 text-xs text-gray-500`
- 置信度条: 同 SynthesisCard 的置信度条样式
- 标签: `inline-flex items-center px-2 py-0.5 rounded-full bg-gray-100 text-xs text-gray-600`
- 经验教训: `text-sm text-gray-600 mt-2 pl-4 border-l-2 border-gray-200`
- 操作按钮: `text-xs text-gray-500 hover:text-gray-700`

***

## 五、通用组件规范

### 5.1 消息气泡（MessageBubble）

用于辩论模式中展示各方发言。

```
正方 (左对齐):
┌────────────────────────────────────────┐
│ [A] MIMO v2.5 Pro         正方        │
│                                         │
│ 我认为应该使用 JWT 方案，因为...        │
│                                         │
│ 置信度: ████████░░ 80%                  │
│                         10:30           │
└────────────────────────────────────────┘

反方 (右对齐):
                    ┌────────────────────────────────────────┐
                    │              反方  DeepSeek V4 [B]      │
                    │                                         │
                    │ 我不同意，Session 方案更安全，因为...    │
                    │                                         │
                    │ 置信度: ███████░░░ 70%                  │
                    │ 10:31                                   │
                    └────────────────────────────────────────┘
```

**规范**:

- 正方: 左对齐，`max-w-[80%]`
- 反方/裁判: 右对齐，`max-w-[80%]`
- 气泡: `rounded-2xl shadow-sm`
- 头像: `w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold`
- 名称: `text-sm font-medium`
- 角色标签: `text-xs px-1.5 py-0.5 rounded`
- 内容: `text-sm leading-relaxed mt-2`
- 置信度条: `mt-3 h-1.5 bg-gray-100 rounded-full`
- 时间戳: `text-xs text-gray-400 mt-2`

### 5.2 进度步骤条（RoundProgress）

```
  ● 已完成 ─────── ● 已完成 ─────── ○ 进行中 ─────── ○ 等待
   第1轮            第2轮            第3轮            第4轮
```

**规范**:

- 容器: `flex items-center justify-between`
- 圆点: `w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium`
  - 已完成: `bg-green-500 text-white` + 勾号图标
  - 进行中: `bg-blue-500 text-white` + 脉冲动画 `animate-pulse`
  - 等待: `bg-gray-200 text-gray-500`
- 连接线: `flex-1 h-0.5 mx-2`
  - 已完成段: `bg-green-500`
  - 进行中段: `bg-gradient-to-r from-green-500 to-blue-500`
  - 等待段: `bg-gray-200`
- 标签: `text-xs text-gray-500 mt-1`

### 5.3 裁定卡片（VerdictCard）

**规范**:

- 容器: `bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden`
- 头部渐变:
  - 正方获胜: `bg-gradient-to-r from-green-500 to-emerald-500`
  - 反方获胜: `bg-gradient-to-r from-red-500 to-orange-500`
  - 平局: `bg-gradient-to-r from-gray-500 to-gray-600`
- 头部内容: `px-6 py-4 text-white`
  - 获胜者: `text-lg font-bold`
  - 副标题: `text-sm opacity-90`
- 内容区: `p-6 space-y-4`
- 推荐方案: `text-sm text-gray-700 leading-relaxed`
- 置信度: 同前
- 执行计划: `space-y-2`
  - 每步: `flex items-start gap-2`
  - 序号: `w-5 h-5 rounded-full bg-blue-100 text-blue-600 text-xs flex items-center justify-center flex-shrink-0 mt-0.5`
  - 内容: `text-sm text-gray-700`
- 操作按钮区: `flex gap-3 mt-6`
  - 确认执行: `px-6 py-2.5 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg transition-colors`
  - 重新辩论: `px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition-colors`

### 5.4 执行面板（ExecutionPanel）

**规范**:

- 容器: `bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden`
- 头部: 根据状态变色
  - 等待: `bg-gray-50`
  - 运行中: `bg-blue-50`
  - 成功: `bg-green-50`
  - 失败: `bg-red-50`
- 代码区: `bg-gray-900 p-4 font-mono text-sm text-green-400 overflow-x-auto max-h-96 overflow-y-auto`
- 错误区: `bg-red-50 p-4 text-sm text-red-700 border-t border-red-100`

### 5.5 按钮系统

| 类型        | 样式                                                                                     | 用途    |
| --------- | -------------------------------------------------------------------------------------- | ----- |
| Primary   | `bg-blue-500 hover:bg-blue-600 text-white rounded-lg px-4 py-2 text-sm font-medium`    | 主操作   |
| Secondary | `bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg px-4 py-2 text-sm font-medium` | 次要操作  |
| Danger    | `bg-red-500 hover:bg-red-600 text-white rounded-lg px-4 py-2 text-sm font-medium`      | 危险操作  |
| Ghost     | `hover:bg-gray-100 text-gray-600 rounded-lg px-4 py-2 text-sm font-medium`             | 轻量操作  |
| Link      | `text-blue-600 hover:text-blue-700 text-sm font-medium`                                | 链接式按钮 |
| Icon      | `p-2 rounded-lg hover:bg-gray-100 text-gray-500`                                       | 图标按钮  |

### 5.6 表单元素

**输入框**:

- 默认: `w-full px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent`
- 错误: `border-red-300 focus:ring-red-500`
- 禁用: `bg-gray-50 text-gray-400 cursor-not-allowed`
- 占位符: `placeholder-gray-400`

**下拉框**:

- 同输入框样式 + `appearance-none bg-[url('chevron-down.svg')] bg-no-repeat bg-[right_8px_center]`

**复选框**:

- `w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500`

**开关（Toggle）**:

- 关闭: `bg-gray-300`
- 开启: `bg-green-500`
- 滑块: `w-4 h-4 bg-white rounded-full shadow-sm`

### 5.7 标签与徽章

| 类型 | 样式                                                              |
| -- | --------------------------------------------------------------- |
| 默认 | `px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 text-xs`    |
| 蓝色 | `px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 text-xs`     |
| 绿色 | `px-2 py-0.5 rounded-full bg-green-50 text-green-700 text-xs`   |
| 红色 | `px-2 py-0.5 rounded-full bg-red-50 text-red-700 text-xs`       |
| 黄色 | `px-2 py-0.5 rounded-full bg-yellow-50 text-yellow-700 text-xs` |
| 紫色 | `px-2 py-0.5 rounded-full bg-purple-50 text-purple-700 text-xs` |

### 5.8 空状态

```
┌─────────────────────────────────────────────────┐
│                                                  │
│           📭                                     │
│                                                  │
│     暂无数据                                      │
│     开始你的第一次辩论吧                           │
│                                                  │
│         [开始辩论]                                │
│                                                  │
└─────────────────────────────────────────────────┘
```

**规范**:

- 容器: `flex flex-col items-center justify-center py-16`
- 图标: `text-4xl mb-4`
- 标题: `text-lg font-medium text-gray-900 mb-1`
- 描述: `text-sm text-gray-500 mb-4`
- 操作按钮: Primary 按钮样式

***

## 六、动画规范

### 6.1 已有动画（保留）

```css
/* 淡入上移 — 消息出现 */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 左滑入 — 正方消息 */
@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}

/* 右滑入 — 反方/裁判消息 */
@keyframes slideInRight {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}

/* 脉冲环 — 进行中指示器 */
@keyframes pulse-ring {
  0% { transform: scale(0.8); opacity: 1; }
  100% { transform: scale(1.4); opacity: 0; }
}

/* 跳动点 — AI 思考中 */
@keyframes bounce-dot {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
```

### 6.2 页面过渡

- 页面切换: `transition-opacity duration-200`
- 卡片出现: `animate-fadeInUp` (stagger 每个卡片延迟 50ms)
- 弹窗: 背景遮罩 `transition-opacity`，弹窗 `transition-all duration-200 scale-95 → scale-100`

### 6.3 交互反馈

- 按钮点击: `active:scale-[0.98]`（微缩放）
- 卡片悬停: `hover:shadow-md transition-shadow duration-200`
- 输入框聚焦: `focus:ring-2 focus:ring-blue-500 transition-shadow`

***

## 七、响应式断点

| 断点   | 宽度      | 布局调整             |
| ---- | ------- | ---------------- |
| `sm` | ≥640px  | 2列卡片网格           |
| `md` | ≥768px  | 导航水平排列，侧边栏       |
| `lg` | ≥1024px | 3列卡片网格           |
| `xl` | ≥1280px | 4列卡片网格，max-w-7xl |

**移动端适配**（<768px）:

- 导航折叠为汉堡菜单
- 卡片单列排列
- 辩论气泡 `max-w-[95%]`
- 模型选择器改为下拉菜单
- 弹窗全屏显示

***

## 八、图标建议

使用 Heroicons（Tailwind 官方图标库）或 Lucide React：

| 用途   | 图标名                       |
| ---- | ------------------------- |
| 首页   | `HomeIcon`                |
| 辩论   | `ChatBubbleLeftRightIcon` |
| 思考   | `LightBulbIcon`           |
| 模型   | `CpuChipIcon`             |
| 历史   | `ClockIcon`               |
| 记忆   | `ArchiveBoxIcon`          |
| 设置   | `Cog6ToothIcon`           |
| 搜索   | `MagnifyingGlassIcon`     |
| 添加   | `PlusIcon`                |
| 删除   | `TrashIcon`               |
| 编辑   | `PencilIcon`              |
| 测试连接 | `SignalIcon`              |
| 暂停   | `PauseIcon`               |
| 恢复   | `PlayIcon`                |
| 导出   | `ArrowDownTrayIcon`       |
| 展开   | `ChevronDownIcon`         |
| 收起   | `ChevronUpIcon`           |
| 成功   | `CheckCircleIcon`         |
| 失败   | `XCircleIcon`             |
| 警告   | `ExclamationTriangleIcon` |
| 信息   | `InformationCircleIcon`   |

***

## 九、代码规范

### 9.1 Tailwind 配置扩展

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#3B82F6',
          secondary: '#8B5CF6',
        }
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.3s ease-out',
        'slide-in-left': 'slideInLeft 0.3s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'pulse-ring': 'pulse-ring 1.5s cubic-bezier(0.215, 0.61, 0.355, 1) infinite',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInLeft: {
          '0%': { opacity: '0', transform: 'translateX(-20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
      },
    },
  },
}
```

### 9.2 组件文件结构

```
src/
├── components/
│   ├── common/              # 通用组件
│   │   ├── Button.tsx
│   │   ├── Badge.tsx
│   │   ├── Modal.tsx
│   │   ├── Toggle.tsx
│   │   ├── EmptyState.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── ConfidenceBar.tsx
│   ├── debate/              # 辩论相关
│   │   ├── MessageBubble.tsx
│   │   ├── VerdictCard.tsx
│   │   ├── RoundProgress.tsx
│   │   ├── ExecutionPanel.tsx
│   │   ├── DebateView.tsx
│   │   └── UserGuideInput.tsx
│   ├── think/               # 独立思考相关
│   │   ├── ThinkerCard.tsx
│   │   ├── ThinkProgress.tsx
│   │   ├── SynthesisCard.tsx
│   │   └── ThinkResult.tsx
│   ├── models/              # 模型管理相关
│   │   ├── ModelCard.tsx
│   │   ├── ModelForm.tsx
│   │   └── ModelTestStatus.tsx
│   └── layout/              # 布局组件
│       ├── Header.tsx
│       ├── Navigation.tsx
│       └── PageContainer.tsx
├── pages/
│   ├── DashboardPage.tsx
│   ├── DebatePage.tsx
│   ├── ThinkPage.tsx
│   ├── ModelsPage.tsx
│   ├── HistoryPage.tsx
│   └── MemoryPage.tsx
├── hooks/                   # 自定义 Hooks
│   ├── useWebSocket.ts
│   ├── useDebate.ts
│   ├── useThink.ts
│   └── useModels.ts
├── types/                   # TypeScript 类型
│   ├── debate.ts
│   ├── think.ts
│   ├── model.ts
│   └── memory.ts
└── utils/
    ├── api.ts
    └── constants.ts
```

***

## 十、无障碍（Accessibility）

- 所有交互元素支持键盘导航（Tab、Enter、Escape）
- 颜色对比度 ≥ 4.5:1（WCAG AA）
- 图标按钮必须有 `aria-label`
- 状态变化使用 `aria-live` 区域通知屏幕阅读器
- 表单输入必须关联 `<label>`
- 弹窗打开时焦点自动移入，关闭时焦点返回触发元素

