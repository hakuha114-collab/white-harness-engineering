# White Harness Engineering

> **缰绳工程学 —— 让 AI Agent 在研发全流程中稳定、可控、可追溯地落地**
>
> v2.0 起，框架从「文档驱动」升级为「可执行的 Harness Runtime」：规则不再只是写在 Markdown 里的约定，而是由真实脚本与状态机强制执行。

![version](https://img.shields.io/badge/version-2.0.1-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![clients](https://img.shields.io/badge/clients-Codex%20%7C%20WorkBuddy-purple)

> **当前版本：v2.0.1** —— 版本号在 `SKILL.md` frontmatter、`config/harness.yaml`、`CHANGELOG.md` 三处强制同步；每次迭代先写 `CHANGELOG.md` 再提交。完整变更见 [CHANGELOG.md](./CHANGELOG.md)，2.0 发布说明见 [RELEASE_NOTES_v2.0.0.md](./RELEASE_NOTES_v2.0.0.md)。

## 🎯 项目定位

基于 Harness Engineering 理念搭建的企业级 AI 工程管控底座，覆盖软件开发全部环节：

- 📋 **需求分析** → 结构化 SPEC 文档（机器可校验）
- 🏗️ **方案设计** → 合规架构方案
- 🚧 **开发执行** → 标准化代码产出
- 🔍 **代码审查** → 全维度质量收口（净上下文审查，不继承开发推理）
- 🧪 **测试验收** → 自动化门禁验证（No Evidence, No Pass）
- 📊 **项目管理** → 全链路进度追踪（项目助手按日记录，可同步腾讯文档）
- 📐 **开发规范** → 刚性红线约束（Markdown 判据 + policies.yaml 机器策略）

## 🧠 核心理念

> **人高位统筹设计全局制度与验收标准，AI 全程在既定框架内高效高强度执行落地，全程可控、可追溯、可迭代、可规模化。**

### 与传统 AI 开发模式的本质区别

| 维度 | Vibe Coding（直觉式） | Harness Engineering（缰绳式） |
|------|----------------------|------------------------------|
| 核心理念 | 靠模型随机发挥，直觉驱动 | 制度化管控，缰绳约束 |
| 执行模式 | 单 Agent 全能式、临时会话记忆 | 多 Agent 专业化分工、资产化沉淀 |
| 质量控制 | 靠人临时检查 | 证据门禁硬性验收（无证据不通过） |
| 流程管理 | 无标准化流程 | 可执行图（Executable Graph）分级指挥 |
| 可追溯性 | 复盘无迹可查 | Trace/Replay 全程留痕可回放 |
| 规模化能力 | 难以规模化 | 可规模化、可复用 |

## 🚀 v2.0 变更（文档驱动 → 可执行运行时）

2.0 在原有「Rule / Skill / Agent / Workflow / Script / MCP / Asset」七大组件之上，新增可执行内核：

```text
可执行图（Executable Graph） + 统一任务状态（TaskState） + 策略（Policy YAML） + 证据门禁（Evidence Gate） + 留痕回放（Trace/Replay）
```

关键能力：

- **可执行图**：`runtime/graphs/*.yaml` 定义节点、边、回退、检查点续跑、扇出/扇入
- **统一 TaskState**：`runtime/schema/task_state.schema.json` 定义 Agent 间机器交接状态
- **Feature 记忆**：`.harness/features/<TASK_ID>/` 下沉淀 `TECH_SPEC.md`、`state.json`、`subtasks.json`、`timeline.ndjson`
- **证据门禁**：所有主门禁输出统一 JSON 契约，强制执行 **No Evidence, No Pass**
- **净上下文审查**：Reviewer 不得继承 Developer 的推理过程与会话历史
- **仓库地图**：`assets/project-wiki/` 提供 L1/L2/L3 项目知识与过期检测
- **策略即代码**：`rules/policies.yaml` 为机器可读策略源（含人工审批策略）
- **动态路由**：按任务风险与副作用自动选择 trivial / normal / feature / high-risk 图
- **人工审批策略**：commit、push、迁移、生产部署、删除、密钥轮换等风险副作用须留审批记录

## 🏛️ 核心组件（1.x 七大组件 + 2.0 执行内核）

| 组件 | 目录 | 说明 |
|------|------|------|
| **Rule** 刚性工程底线 | `rules/` | 研发红线判据（Markdown）+ 机器策略（policies.yaml） |
| **Skill** 标准化操作手册 | `skills/` | 高频操作固化成标准流程，一键复用 |
| **Sub Agent** 专业化分工 | `agents/` | 拆分专项职能智能体，各司其职 |
| **Workflow** 分级指挥链 | `workflows/` | 人类可读的流程指引（执行路由以 runtime/graphs 为准） |
| **Scripts** 自动化验收 | `scripts/` | 每个节点配套真实校验脚本，达标方可推进 |
| **MCP** 系统外接插座 | `mcp/` | 打通 Git/CI/测试/看板/工单等外部工具（契约蓝图） |
| **Assets** 资产化沉淀 | `assets/` | 规范/错题/经验/模板/项目wiki，长效复用迭代 |
| **Runtime** 可执行内核（2.0 新增） | `runtime/` | 图执行、状态、路由、策略、留痕回放 |

## 🤖 八大分级 Agent

| Agent | 目录 | 核心职责 |
|-------|------|----------|
| **PM 调度 Agent** | `agents/pm-dispatcher/` | 全局统筹、任务路由、异常回退、进度兜底 |
| **需求拆解 Agent** | `agents/requirement-analyzer/` | 业务诉求 → 结构化标准 SPEC 文档 |
| **方案设计 Agent** | `agents/solution-designer/` | 需求清单 → 合规架构方案 + 模块拆解 |
| **闸门风控 Agent** | `agents/risk-controller/` | 开发前全维度核验，提前拦阻隐患 |
| **开发执行 Agent** | `agents/code-developer/` | 标准化落地执行，合规编写代码 |
| **代码审查 Agent** | `agents/code-reviewer/` | 全维度校验（净上下文，不继承开发推理） |
| **测试验收 Agent** | `agents/test-validator/` | 功能实测 + 场景兼容 + 边界压测 |
| **项目助手 Agent** | `agents/project-recorder/` | 按日记录问题/进度/遗留，可同步腾讯文档 |

## 📁 项目结构

```text
white-harness-engineering/
├── SKILL.md                     # AI 路由入口（何时用、路由表、报告规范）
├── README.md                    # 项目门面（本文件）
├── ARCHITECTURE.md              # 架构设计文档
├── SPEC.md                      # 设计规格文档
├── USAGE.md                     # 使用者手册
├── CHANGELOG.md                 # 版本演进
├── RELEASE_NOTES_v2.0.0.md      # 2.0 发布说明
├── config/                      # 机器可读配置
│   ├── harness.yaml             # 全局管控配置
│   ├── router.yaml              # 动态路由配置
│   └── gates.yaml               # 门禁配置
├── runtime/                     # 可执行运行时（2.0 核心）
│   ├── gates.py                 # 证据门禁引擎
│   ├── graph.py / state.py      # 图执行 / 任务状态
│   ├── router.py / policy.py    # 动态路由 / 策略
│   ├── trace.py                 # 留痕回放
│   ├── graphs/                  # trivial/normal/feature/high-risk 图定义
│   └── schema/                  # task_state.schema.json
├── rules/                       # 刚性工程底线
│   ├── policies.yaml            # 机器可读策略源（2.0 新增）
│   ├── coding-standards.md      # 代码规范红线（判据式 SSOT）
│   ├── security-rules.md        # 安全合规红线（判据式 SSOT）
│   ├── review-checklist.md      # Review 硬性检查项
│   └── prohibited-actions.md    # 禁止操作分级索引
├── skills/                      # 标准化高频操作手册
│   ├── create-spec/  code-review/  write-test/  fix-bug/
│   ├── refactor/  deploy/  project-setup/  repomix/
│   └── karpathy-guidelines/
├── agents/                      # 八大专业化 Agent（见上表）
├── workflows/                   # 流程指引（人类可读）
│   ├── executable-graph.md      # 可执行图说明（2.0 新增）
│   └── full-dev / bug-fix / code-review / hotfix 四条流水线
├── scripts/                     # 真实校验脚本（2.0 全部落地）
│   ├── harness_runtime.py       # 运行时 CLI（route/init/next/validate/replay）
│   ├── self-check.py            # 仓库自检
│   └── check-spec/ check-design/ check-risk/ check-code-style/
│       check-security/ check-review-pass/ check-test-coverage/
│       check-knowledge-stale/
├── mcp/                         # 外接系统契约蓝图（Git/CI/看板/监控/蓝湖）
├── assets/                      # 资产化沉淀
│   ├── templates/               # 报告模板（10 类分类模板）+ feature-memory 模板
│   ├── project-wiki/            # 仓库地图 L1/L2/L3 + 语义映射（2.0 新增）
│   └── knowledge-base/ lesson-learned/ dev-map/
├── docs/                        # runtime.md / migration-v2.md（2.0 新增）
└── tests/                       # 单元测试 + 门禁 fixtures（2.0 新增）
```

## ⚡ Runtime 快速上手（2.0）

```bash
# 任务路由：按类型/风险/改动面选择执行图
python scripts/harness_runtime.py route --task-type feature --risk-level normal --changed-files 8

# 创建 Feature 记忆
python scripts/harness_runtime.py init --task-id FEAT-001 --goal "新增订单导出" --workflow feature

# 查看图流转（下一节点）
python scripts/harness_runtime.py next --workflow feature --node implement --status PASS

# 校验任务状态
python scripts/harness_runtime.py validate-state .harness/features/FEAT-001/state.json

# 回放执行留痕
python scripts/harness_runtime.py replay .harness/features/FEAT-001/timeline.ndjson
```

## 🚦 门禁快速上手

所有门禁使用统一结果契约：

| 状态 | 退出码 | 含义 |
|------|-------|------|
| PASS | 0 | 通过，且有持久化证据 |
| FAIL | 1 | 必须回退修复 |
| WARN | 2 | 仅当策略允许警告携带时可推进 |
| BLOCK | 3 | 暂停，等待人工介入 |

```bash
python scripts/check-spec/check_spec.py SPEC.md --json
python scripts/check-design/check_design.py DESIGN.md --spec SPEC.md --json
python scripts/check-risk/check_risk.py RISK.md --json
python scripts/check-code-style/check_code_style.py . --json
python scripts/check-security/check_security.py . --json
python scripts/check-review-pass/check_review_pass.py review.md --json
python scripts/check-test-coverage/check_test_coverage.py coverage.json --json
python scripts/check-knowledge-stale/check_knowledge_stale.py .harness/wiki-manifest.json --json
```

## 🧭 动态图路由

| 图 | 适用场景 |
|----|---------|
| `trivial` | 低风险文档、错别字、微小配置改动 |
| `normal` | 常规 Bug 修复与重构 |
| `feature` | 多文件特性开发，需 TECH_SPEC、子任务拆分、扇出/扇入验证 |
| `high-risk` | 安全、迁移、生产、破坏性操作或需审批的工作 |

人类可读的流程文档保留在 `workflows/`；可执行路由以 `runtime/graphs/*.yaml` 为准。

## 📦 安装与使用（Codex / WorkBuddy 双客户端）

本仓库 `SKILL.md` 采用 **Open Agent Skills** 通用格式（YAML frontmatter + 渐进式披露），Codex CLI、WorkBuddy、Claude Code、Gemini CLI 等兼容客户端可直接复用。

### 🅰 WorkBuddy（用户级技能，按场景自动触发）

```bash
git clone https://github.com/hakuha114-collab/white-harness-engineering.git \
  ~/.workbuddy/skills/white-harness-engineering
```

- 对话中通过 `@skill:white-harness-engineering` 显式引用
- 或在自定义指令里配置「软件研发 / 需求分析 / 代码测试 / 项目管理均使用此技能」，按场景自动触发
- 仅对单项目生效时，克隆到 `<项目>/.workbuddy/skills/white-harness-engineering`

### 🅱 Codex CLI（Open Agent Skills 标准）

```bash
# 用户级（推荐，所有仓库可用）
git clone https://github.com/hakuha114-collab/white-harness-engineering.git \
  ~/.agents/skills/white-harness-engineering

# 或 Skills CLI 一键安装
npx skills add hakuha114-collab/white-harness-engineering -a codex
```

- 触发：会话中输入 `$white-harness-engineering` 显式调用，或描述「写 SPEC / 代码审查 / 修 Bug / 重构」等任务隐式匹配
- 新装技能后重启 Codex 加载；`/skills` 查看已安装列表

## ✅ 验证

```bash
python scripts/self-check.py
```

编译运行时脚本、跑单元测试、执行门禁样例 fixtures，全过即仓库健康。

## 📋 报告与产出规范

所有审查 / 评审 / 进程类产出统一以**自包含 HTML** 输出（浅色主题、离线可览），分类模板见 `assets/templates/reports/`（代码审查/覆盖率/测试/Bug修复/重构/部署/初始化/风控/验收/代码库分析 10 类）。

## 📚 文档分工与单一事实源

| 文档 | 定位 | 读者 |
|------|------|------|
| `SKILL.md` | AI 路由入口：何时用、路由表、报告规范 | AI Agent |
| `README.md` | 项目门面：理念、组件、快速开始 | GitHub 访客 |
| `USAGE.md` | 使用者手册：场景化使用方式 | 框架使用者 |
| `docs/runtime.md` / `docs/migration-v2.md` | 运行时细节与 1.x→2.0 迁移 | 框架维护者 |

**单一事实源约定**：意图路由以 `SKILL.md` 为准；管控参数以 `config/harness.yaml` 为准；可执行路由以 `runtime/graphs/*.yaml` 为准；策略以 `rules/policies.yaml` 为准；红线判据以 `rules/security-rules.md` / `rules/coding-standards.md` 为准；HTML 报告骨架以 `assets/templates/report-template.html` 为准。

## 📐 设计原则

1. **制度优先**：先定规则，再执行；规则尽量机器可执行
2. **分而治之**：拒绝全能单 Agent，专业化分工提升稳定性
3. **证据验收**：No Evidence, No Pass，不靠人临时检查
4. **资产沉淀**：摒弃临时会话记忆，所有产出工程化沉淀
5. **全程追溯**：Trace/Replay，每个动作、决策、变更都有迹可查
6. **渐进落地**：按标准步骤分步搭建，无需大额成本快速落地

## 📄 参考来源

- [告别AI工程翻车！Harness Engineering：让Agent稳定落地实战全拆解](https://mp.weixin.qq.com/s/D_AxgotNAbdfEBAjp038kg)

## 📜 License

MIT
