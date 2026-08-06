# White-Harness-Engineering

> **缰绳工程学 —— 让 AI Agent 在研发全流程中稳定、可控、可追溯地落地**

![version](https://img.shields.io/badge/version-1.2.2-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![clients](https://img.shields.io/badge/clients-Codex%20%7C%20WorkBuddy-purple)

> **当前版本：v1.2.2** —— 版本号在 `SKILL.md` frontmatter、`config/harness.yaml`、`CHANGELOG.md` 三处强制同步；每次迭代先写 `CHANGELOG.md` 再提交。完整变更见 [CHANGELOG.md](./CHANGELOG.md)。

## 🎯 项目定位

基于 Harness Engineering 理念搭建的企业级 AI 工程管控底座。覆盖公司全部软件开发环节：

- 📋 **需求分析** → 结构化 SPEC 文档
- 🏗️ **方案设计** → 合规架构方案
- 🚧 **开发执行** → 标准化代码产出
- 🔍 **代码审查** → 全维度质量收口
- 🧪 **测试验收** → 自动化门禁验证
- 📊 **项目管理** → 全链路进度追踪（含项目助手 Agent 按日记录问题与进度，可同步腾讯文档）
- 📐 **开发规范** → 刚性红线约束

## 🧠 核心理念

> **人高位统筹设计全局制度与验收标准，AI全程在既定框架内高效高强度执行落地，全程可控、可追溯、可迭代、可规模化。**

### 与传统 AI 开发模式的本质区别

| 维度 | Vibe Coding（直觉式） | Harness Engineering（缰绳式） |
|------|----------------------|------------------------------|
| 核心理念 | 靠模型随机发挥，直觉驱动 | 制度化管控，缰绳约束 |
| 执行模式 | 单 Agent 全能式、临时会话记忆 | 多 Agent 专业化分工、资产化沉淀 |
| 质量控制 | 靠人临时检查 | Scripts 自动化硬性验收门禁 |
| 流程管理 | 无标准化流程 | Workflow 全链路分级指挥链条 |
| 可追溯性 | 复盘无迹可查 | 全程可控、可追溯、可迭代 |
| 规模化能力 | 难以规模化 | 可规模化、可复用 |

## 🏛️ 七大核心组件

| 组件 | 目录 | 说明 |
|------|------|------|
| **Rule** 刚性工程底线 | `rules/` | 全团队统一遵守的研发红线准则 |
| **Skill** 标准化操作手册 | `skills/` | 高频操作固化成标准流程，一键复用 |
| **Sub Agent** 专业化分工 | `agents/` | 拆分专项职能智能体，各司其职 |
| **Workflow** 分级指挥链 | `workflows/` | Agent 间衔接、流转、回退、交接规则 |
| **Scripts** 自动化验收 | `scripts/` | 每个节点配套校验脚本，达标方可推进 |
| **MCP** 系统外接插座 | `mcp/` | 打通 Git/CI/测试/看板/工单等外部工具 |
| **Assets** 资产化沉淀 | `assets/` | 规范/错题/经验/台账，长效复用迭代 |

## 🤖 八大分级 Agent

> 说明：上文「七大核心组件」指框架的能力组件（Rule/Skill/Agent/Workflow/Scripts/MCP/Assets），此处「八大 Agent」指 Agent 组件内的 8 个专业化角色，两者是不同维度，数量并不矛盾。

| Agent | 目录 | 核心职责 |
|-------|------|----------|
| **PM 调度 Agent** | `agents/pm-dispatcher/` | 全局统筹、任务路由、异常回退、进度兜底 |
| **需求拆解 Agent** | `agents/requirement-analyzer/` | 业务诉求 → 结构化标准 SPEC 文档 |
| **方案设计 Agent** | `agents/solution-designer/` | 需求清单 → 合规架构方案 + 模块拆解 |
| **闸门风控 Agent** | `agents/risk-controller/` | 开发前全维度核验，提前拦阻隐患 |
| **开发执行 Agent** | `agents/code-developer/` | 标准化落地执行，合规编写代码 |
| **代码审查 Agent** | `agents/code-reviewer/` | 全维度校验规范/漏洞/性能/安全 |
| **测试验收 Agent** | `agents/test-validator/` | 功能实测 + 场景兼容 + 边界压测 |
| **项目助手 Agent** | `agents/project-recorder/` | 按日记录问题/进度/遗留，生成进程日志，可同步腾讯文档 |

## 📁 项目结构

```
white-harness-engineering/
├── README.md                    # 项目说明
├── ARCHITECTURE.md              # 架构设计文档
├── SPEC.md                      # 设计规格文档
├── config/
│   ├── harness.yaml             # 全局管控配置
│   └── agents.yaml              # Agent 注册表
├── rules/                       # 刚性工程底线制度
│   ├── coding-standards.md      # 代码规范红线
│   ├── security-rules.md        # 安全合规红线
│   ├── review-checklist.md      # Review 硬性检查项
│   └── prohibited-actions.md    # 禁止操作清单
├── skills/                      # 标准化高频操作手册
│   ├── create-spec/             # 创建 SPEC 文档
│   ├── code-review/             # 代码审查流程
│   ├── write-test/              # 编写测试用例
│   ├── fix-bug/                 # Bug 修复流程
│   ├── refactor/                # 重构流程
│   ├── deploy/                  # 部署流程
│   └── project-setup/           # 项目初始化
├── agents/                      # 专业化分工兵种矩阵
│   ├── pm-dispatcher/           # PM 调度 Agent
│   ├── requirement-analyzer/    # 需求拆解 Agent
│   ├── solution-designer/       # 方案设计 Agent
│   ├── risk-controller/         # 闸门风控 Agent
│   ├── code-developer/          # 开发执行 Agent
│   ├── code-reviewer/           # 代码审查 Agent
│   ├── test-validator/          # 测试验收 Agent
│   └── project-recorder/       # 项目助手 Agent（按日进程日志）
├── workflows/                   # 全链路分级指挥链条
│   ├── full-dev-pipeline.md     # 完整研发流水线
│   ├── bug-fix-pipeline.md      # Bug 修复流水线
│   ├── code-review-pipeline.md  # 代码审查流水线
│   └── hotfix-pipeline.md       # 紧急修复流水线
├── scripts/                     # 自动化硬性验收门禁
│   ├── check-spec/              # SPEC 完整性校验（含已落地的 check_spec.py 真实脚本）
│   ├── check-design/            # 设计文档完整性校验
│   ├── check-risk/              # 风控报告校验
│   ├── check-code-style/        # 代码风格校验
│   ├── check-security/          # 安全合规校验
│   ├── check-test-coverage/     # 测试覆盖率校验
│   └── check-review-pass/       # Review 通过校验
├── mcp/                         # 全域工程系统外接插座
│   ├── git-integration.md       # Git 仓库对接
│   ├── ci-cd-integration.md     # CI/CD 流水线对接
│   ├── project-board.md         # 项目看板对接
│   ├── monitoring.md            # 监控告警对接
│   └── lanhu-mcp.md             # 蓝湖原型对接
└── assets/                      # 资产化沉淀
    ├── dev-map/                 # 全域工程图谱
    ├── knowledge-base/          # 知识库
    ├── lesson-learned/          # 踩坑经验
    └── templates/               # 标准模板库
```

## 📋 报告与产出规范

所有审查 / 评审 / 进程类产出统一以**自包含 HTML** 形式输出（浅色主题、离线可览），便于系统预览与归档；配套 `code-review` 工具支持按项目登记忽略项、动态统计，避免重复检出。报告骨架模板：`assets/templates/report-template.html`。

## 📚 文档分工（避免重复维护）

| 文档 | 定位 | 读者 |
|------|------|------|
| `SKILL.md` | AI 路由入口：何时用、路由表、报告规范 | AI Agent |
| `README.md` | 项目门面：理念、组件、快速开始 | GitHub 访客 |
| `USAGE.md` | 使用者手册：场景化使用方式 | 框架使用者 |
| `SPEC.md` / `ARCHITECTURE.md` | 设计规格与架构 | 框架维护者 |

**单一事实源约定**：意图路由表以 `SKILL.md` 为准；超时/回退数字以 `config/harness.yaml` 为准；Karpathy 原则以 `skills/karpathy-guidelines/SKILL.md` 为准；HTML 报告骨架以 `assets/templates/report-template.html` 为准。其余文档只引用、不复制。

## 🚀 快速开始

### 零门槛落地顺序

按以下标准化步骤逐步搭建，适配各类团队规模：

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 打磨完整可落地设计 SPEC 规格文档 | 统一全员 AI 基准标准 |
| 2 | 补齐项目刚需核心 Rule 红线规则 | 筑牢合规底线 |
| 3 | 梳理高频刚需作业，封装成 Skill 标准库 | 可直接调用 |
| 4 | 单 Agent 不稳定时，拆分多专项 Sub Agent | 提升稳定性 |
| 5 | 跨角色流程衔接复杂后，补充契约文件 | 明确职责 |
| 6 | 规模化阶段，上线 dev-map + 任务看板 | 全局可视 |
| 7 | 需联动外部工具时，接入 MCP 通用接口 | 打通全域系统 |

### 使用方式（支持 Codex / WorkBuddy）

本仓库的 `SKILL.md` 采用 **Open Agent Skills** 通用格式（YAML frontmatter + 渐进式披露），Codex CLI、WorkBuddy、Claude Code、Gemini CLI 等兼容客户端可直接复用，无需改写。

#### 🅰 WorkBuddy（用户级技能，按场景自动触发）

```bash
# 安装到用户级技能目录（所有对话自动可用）
git clone https://github.com/hakuha114-collab/white-harness-engineering.git \
  ~/.workbuddy/skills/white-harness-engineering
```

- 对话中通过 `@skill:white-harness-engineering` 显式引用
- 或在自定义指令里配置「软件研发 / 需求分析 / 代码测试 / 项目管理均使用此技能」，让它按场景自动触发
- 仅对单项目生效时，克隆到 `<项目>/.workbuddy/skills/white-harness-engineering`

#### 🅱 Codex CLI（Open Agent Skills 标准）

```bash
# 方式一：用户级（推荐，所有仓库可用）
git clone https://github.com/hakuha114-collab/white-harness-engineering.git \
  ~/.agents/skills/white-harness-engineering

# 方式二：仓库级（随仓库提交，团队共享）
mkdir -p .agents/skills && git clone https://github.com/hakuha114-collab/white-harness-engineering.git \
  .agents/skills/white-harness-engineering

# 方式三：Skills CLI 一键安装
npx skills add hakuha114-collab/white-harness-engineering -a codex
```

- 触发：在 Codex 会话中输入 `$white-harness-engineering` 显式调用，或描述「写 SPEC / 代码审查 / 修 Bug / 重构」等任务，Codex 按 `SKILL.md` 的 `description` 隐式匹配
- 新装技能后重启 Codex 以加载；`/skills` 可查看已安装技能列表
- 个别技能可在 `~/.codex/config.toml` 中关闭

### 按需裁剪（通用）

- 改 `config/harness.yaml` 适配实际项目管控参数
- 在 `rules/` 补充项目特有的红线规则
- 在 `skills/` 扩展团队高频操作流程
- 在 `agents/` 激活并定制所需 Agent

## 📐 设计原则

1. **制度优先**：先定规则，再执行。AI 必须在既定框架内运行
2. **分而治之**：拒绝全能单 Agent，专业化分工提升稳定性
3. **自动验收**：每个节点有硬性门禁，不靠人临时检查
4. **资产沉淀**：摒弃临时会话记忆，所有产出工程化沉淀
5. **全程追溯**：每个动作、决策、变更都有迹可查
6. **渐进落地**：按标准步骤分步搭建，无需大额成本快速落地

## 📄 参考来源

- [告别AI工程翻车！Harness Engineering：让Agent稳定落地实战全拆解](https://mp.weixin.qq.com/s/D_AxgotNAbdfEBAjp038kg)

## 📜 License

MIT
