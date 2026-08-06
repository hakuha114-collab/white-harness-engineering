---
name: white-harness-engineering
version: 1.2.2
description: |
  AI 研发全流程工程管控框架（缰绳工程学）。触发：写/审 SPEC、代码审查、写测试、修 Bug、重构、部署、项目初始化，或需强制 AI 开发遵循"先思考再编码、简洁优先、精准修改、目标驱动验证"刚性规范。含刚性 Rule、标准化 Skill、分级 Agent、流水线与门禁脚本。不用于纯问答或闲聊。
agent_created: true
---

# Harness Engineering · AI 工程管控框架

> 人高位统筹设计全局制度与验收标准，AI 全程在既定框架内高效高强度执行落地，全程可控、可追溯、可迭代、可规模化。

本技能将「缰绳工程学」方法论打包为可复用资源。核心思想：**制度优先（先定规则再执行）、分而治之（专业化分工）、自动验收（每节点有硬性门禁）、资产沉淀（工程化复用）、全程追溯**。

## 何时使用

- 启动任何非琐碎的 AI 辅助开发任务（新功能、Bug 修复、重构、API 变更）时，先加载 Rule 约束，遵循 Karpathy 四原则。
- 需要把模糊业务诉求转化为结构化、可量化的 SPEC 文档时 → 用 `skills/create-spec/SKILL.md`。
- 需要规范化代码审查、编写测试、修复 Bug、重构、部署、初始化项目时 → 用对应的子 Skill。
- 需要跑完整研发流水线（需求→设计→风控→开发→审查→测试→交付）或专项流水线（Bug 修复 / 代码审查 / 紧急修复）时 → 用 `workflows/` 下的流水线。
- 需要将 AI 行为约束为 8 个专业兵种（PM 调度、需求拆解、方案设计、闸门风控、开发执行、代码审查、测试验收、项目进程记录）分工协作时 → 参考 `agents/`。
- 需要让 AI 读取蓝湖设计稿 / 原型 / 需求文档 / 切图时 → 先按 `mcp/lanhu-mcp.md` 接入蓝湖 MCP（Lanhu MCP）。

## 目录结构（已随技能一并打包）

```
white-harness-engineering/
├── SKILL.md                  ← 本文件（统一入口）
├── README.md / SPEC.md / ARCHITECTURE.md / USAGE.md   ← 框架总纲
├── config/
│   ├── harness.yaml          ← 全局管控配置
│   └── agents.yaml           ← Agent 注册表
├── rules/                    ← 刚性工程底线（L0-L3 约束体系）
│   ├── karpathy-guidelines.md   ← 编程四原则（总是生效）
│   ├── coding-standards.md      ← 代码规范红线
│   ├── security-rules.md        ← 安全合规红线
│   ├── review-checklist.md      ← Review 硬性检查项
│   └── prohibited-actions.md    ← 禁止操作清单
├── skills/                   ← 标准化高频操作手册（子 Skill）
│   ├── karpathy-guidelines/SKILL.md
│   ├── create-spec/SKILL.md
│   ├── code-review/SKILL.md
│   ├── write-test/SKILL.md
│   ├── fix-bug/SKILL.md
│   ├── refactor/SKILL.md
│   ├── deploy/SKILL.md
│   ├── project-setup/SKILL.md
│   └── repomix/SKILL.md
├── agents/                   ← 八大 Agent 角色定义（七个线性兵种 + 一个侧挂进程记录）
│   ├── pm-dispatcher/AGENT.md
│   ├── requirement-analyzer/AGENT.md
│   ├── solution-designer/AGENT.md
│   ├── risk-controller/AGENT.md
│   ├── code-developer/AGENT.md
│   ├── code-reviewer/AGENT.md
│   ├── test-validator/AGENT.md
│   └── project-recorder/AGENT.md   ← 项目进程记录Agent（侧挂：跨阶段归集问题/待确认/遗留BUG，按日记录并整理整体进度）
├── workflows/                ← 全链路分级指挥链
│   ├── full-dev-pipeline.md
│   ├── bug-fix-pipeline.md
│   ├── code-review-pipeline.md
│   └── hotfix-pipeline.md
├── scripts/                  ← 自动化硬性验收门禁（check-spec 已落地真实脚本，其余为逻辑校验说明）
│   ├── check-spec/  check-design/  check-risk/
│   └── check-code-style/  check-security/  check-review-pass/  check-test-coverage/
├── mcp/                      ← 外部系统接入说明（Git/CI-CD/看板/监控/蓝湖原型）
└── assets/                   ← 资产化沉淀（知识库/错题集/模板/dev-map）
```

## 使用方式

### 1. 任何编码任务：先加载 Rule，遵循 Karpathy 四原则

读取并执行 `rules/karpathy-guidelines.md` 与 `skills/karpathy-guidelines/SKILL.md` 的四原则：

1. **先思考再编码** —— 写代码前必须输出思考文档（假设清单 / 多种解读 / 权衡分析 / 最简方案 / 待确认问题）；有歧义先向用户确认。
2. **简洁优先** —— 只实现被要求的功能，杜绝未被请求的抽象与"灵活性"。
3. **精准修改** —— diff 中只含请求相关的变更，不包含任何"顺手改进"。
4. **目标驱动验证** —— 每个步骤都有明确验证方式（测试先行或成功标准明确）。

编码时同时遵守 `rules/coding-standards.md`、`rules/security-rules.md`、`rules/prohibited-actions.md`。

### 2. 按用户意图路由到对应子 Skill

| 用户说的话 | 读取并遵循 |
|-----------|-----------|
| "新需求 / 写 SPEC / 需求分析" | `skills/create-spec/SKILL.md` + `assets/templates/spec-template.md` |
| "代码审查 / review / PR 审查" | `skills/code-review/SKILL.md` + `rules/review-checklist.md` |
| "写测试 / 单元测试 / 测试用例" | `skills/write-test/SKILL.md` |
| "修 Bug / Bug 修复" | `skills/fix-bug/SKILL.md`（先写测试复现再修复） |
| "重构 / 优化代码" | `skills/refactor/SKILL.md`（先确认测试覆盖率） |
| "部署 / 发布" | `skills/deploy/SKILL.md` |
| "初始化项目 / 搭建工程" | `skills/project-setup/SKILL.md` |
| （任何编码任务） | `skills/karpathy-guidelines/SKILL.md` ← 总是生效 |

### 3. 跑流水线（多 Agent 协作）

根据任务类型读取对应 Workflow，按其中的阶段、门禁与回退策略执行：

- `workflows/full-dev-pipeline.md` —— 完整研发流水线（需求→设计→风控→开发→审查→测试→交付）。
- `workflows/bug-fix-pipeline.md` —— Bug 修复流水线。
- `workflows/code-review-pipeline.md` —— 代码审查流水线。
- `workflows/hotfix-pipeline.md` —— 紧急修复流水线。

每个阶段结束必须运行对应门禁校验（`scripts/`），结果分四级：**PASS（通过）/ WARN（标记后推进）/ FAIL（回退修复）/ BLOCK（暂停，人工介入）**。任一阶段不通过按 `workflows/full-dev-pipeline.md` 的回退映射回退到对应 Agent。

### 4. 跨项目引用

本技能安装为用户级技能后，在任意工作区对话中只要意图匹配即自动触发；也可显式要求"按 Harness Engineering 规范 / Karpathy 四原则执行本次任务"来强制加载。

## 报告输出规范（全局 · 强制）

**所有「报告类」产出必须且只能以 HTML 文件形式交付**，不再输出 Markdown 报告。这是框架级硬性约定，目的是让审查 / 测试 / 部署 / 重构 / 修复 / 初始化 / 风控等报告在 WorkBuddy 内置预览面板中"开箱即看、可交互、可分享"，并支撑门禁横幅、分级色标、问题-修改方案两列等可视化结构。

### 适用范围

- **必须 HTML（报告类）**：名称含 `Report` / `报告` 的产出，包括：
  `review_report`(代码审查)、`coverage_report`(覆盖率)、`deploy_report`(部署)、`refactor_report`(重构)、`test_results`(测试验证结果)、`fix_report`(Bug 修复)、`setup_report`(项目初始化)、`repomix` 分析报告、风控报告、测试验收报告等。
- **保持 Markdown（过程文档，非报告）**：`thinking_doc`(思考文档)、`verification_plan`(验证计划)、`spec_doc`(SPEC)、`design_doc`(设计文档) 等中间过程文档，仍用 Markdown。

### HTML 报告硬性要求

1. **自包含**：单个 `.html` 文件，内联 `<style>`，**不引用任何外部 CSS/JS/CDN/字体**，可双击离线打开。
2. **浅色主题适配 IDE**：白底深字，颜色变量明确定义（见模板文件），状态/分级用色标区分。
3. **必备结构**（顺序）：
   - `<h1>` 报告标题 + 基本信息（任务 / 版本 / 时间 / 执行 Agent）；
   - **结论横幅** `.banner`：通过=绿 / 不通过=红 / 有条件通过=黄，文案与门禁一致；
   - 分级 / 状态 **色标标签** `.tag`：MUST/SHOULD/NICE 与 PASS/WARN/FAIL/BLOCK 用不同底色；
   - 主体用 `<table>` 呈现（问题清单、验证结果、变更内容等），复杂项用「问题 | 修改方案」两列网格。
4. 报告文件建议落盘到仓库 `deliverables/` 或对应 skill 的 `reports/` 目录，并在对话中通过预览交付。

### 统一 HTML 报告骨架与分类模板

- **通用骨架**：`assets/templates/report-template.html`（任何报告均可基于它填充，勿在主文档内联维护副本）。
- **分类模板**（`assets/templates/reports/` 下，已预置分区结构，生成报告时优先读取对应模板替换占位）：

| 报告类型 | 模板文件 | 产出方 |
|---------|---------|--------|
| 代码审查报告 review_report | `reports/review-report.html` | code-review |
| 覆盖率报告 coverage_report | `reports/coverage-report.html` | write-test |
| 测试验证结果 test_results | `reports/test-results.html` | refactor / write-test |
| Bug 修复报告 fix_report | `reports/fix-report.html` | fix-bug |
| 重构报告 refactor_report | `reports/refactor-report.html` | refactor |
| 部署报告 deploy_report | `reports/deploy-report.html` | deploy |
| 项目初始化报告 setup_report | `reports/setup-report.html` | project-setup |
| 风控报告 | `reports/risk-report.html` | risk-controller |
| 测试验收报告 | `reports/acceptance-report.html` | test-validator |
| 代码库分析报告（repomix） | `reports/repomix-report.html` | repomix |

各子 Skill 在「生成 XXX 报告」步骤只需声明"按对应分类模板输出"，并保留原结构分区（基本信息 / 结论 / 问题清单 / 验证结果等），不再使用 ` ```markdown ` 报告模板。

## 约束层级（Rule 体系）

- **L0 法律合规红线**：数据隐私 / 安全漏洞 / 知识产权，违反即终止。
- **L1 工程规范红线**：代码风格 / 架构规范 / 测试覆盖，违反即回退。
- **L2 团队最佳实践**：设计模式 / 性能 / 可维护性，偏离需说明。
- **L3 项目特定约定**：命名 / 目录结构 / 工具选择，灵活调整。

## 设计原则

1. 制度优先：先定规则，再执行，AI 必须在既定框架内运行。
2. 分而治之：拒绝全能单 Agent，专业化分工提升稳定性。
3. 自动验收：每个节点有硬性门禁，不靠人临时检查。
4. 资产沉淀：摒弃临时会话记忆，所有产出工程化沉淀到 `assets/`。
5. 全程追溯：每个动作、决策、变更都有迹可查。
6. 渐进落地：按标准步骤分步搭建，无需大额成本快速落地。

## 版本管理（维护者约定）

- 版本号采用语义化版本（SemVer）：`主版本.次版本.修订号`。规则/门禁变更 → 次版本；模板/文档/勘误 → 修订号；架构级调整 → 主版本。
- **三处版本号必须同步**：本文件 frontmatter 的 `version`、`config/harness.yaml` 的 `harness.version`、`CHANGELOG.md` 最新条目。
- 每次迭代升级必须先在 `CHANGELOG.md` 追加条目（日期 + 变更清单），再提交推送。

## 参考来源

- 框架原文与详细说明见 `README.md`、`SPEC.md`、`ARCHITECTURE.md`、`USAGE.md`。
- 核心理念参考：[告别AI工程翻车！Harness Engineering：让Agent稳定落地实战全拆解](https://mp.weixin.qq.com/s/D_AxgotNAbdfEBAjp038kg)
