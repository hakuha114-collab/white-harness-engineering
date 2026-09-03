# Changelog

## [2.2.0] - 2026-09-03

### Added
- 新增独立工作流 `workflows/git-impact-topology.md`：Git 拉取后一键串联「变更检测（`detect_changes_tool`）→ 影响半径（`get_impact_radius_tool`）→ 受影响流程（`get_affected_flows_tool`）→ 拓扑图（`visualize`）」，产出影响面摘要 + D3 力导向拓扑图 + 高危点清单，并明确红线（本 workflow 不执行任何 git 命令，pull 由用户在其环境完成）
- SKILL.md Intent Routing 新增 `git-impact-topology` 触发项（用户说"Git 影响拓扑 / git-impact-topology"即路由到该 workflow）；Core Files 与 `description` 同步补充触发词
- 版本三处同步 2.1.0 → 2.2.0（Git 拉取后影响面/拓扑一键能力，复用已接入的 code-review-graph MCP 图谱）

## [2.1.0] - 2026-08-19

### Added
- 新增可选审查图谱契约 `mcp/code-review-graph.md`：接入 code-review-graph（[@tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph)，Python 包 v2.3.3），含能力清单（实测 30 个 MCP 工具）、双端接入（WorkBuddy `~/.workbuddy/mcp.json` 6 个按项目根 `cwd` 区分的实例 / Codex `config.toml` 镜像）、Preflight 检测、与 CodeGraph 的选型路由表
- `mcp/codegraph.md` 顶部新增「与 code-review-graph 的分工（一文读懂选哪个）」：输入是符号 → CodeGraph，输入是 diff/PR → code-review-graph
- `agents/code-reviewer/AGENT.md` 的「Required Evidence」补 `get_review_context_tool` / `get_impact_radius_tool` / `get_affected_flows_tool` 审查上下文证据（Preflight 检测后使用），并标注选型路由
- `agents/risk-controller/AGENT.md` 的「Code intelligence」补 code-review-graph 的 `get_impact_radius_tool` 作为 diff/PR 级波及半径补充，标注选型路由
- SKILL.md Core Files 增加 `mcp/codegraph.md` 与 `mcp/code-review-graph.md` 两条可选增强契约
- 版本三处同步 2.0.4 → 2.1.0（双图谱可选能力：CodeGraph 理解 / code-review-graph 审查）

## [2.0.4] - 2026-08-18

### Fixed
- `mcp/codegraph.md` 能力清单与 env 对齐 CodeGraph v1.5.0 真实工具集：移除不存在的 `codegraph_affected` / `codegraph_query`（实测 `tools/list` 仅返回 `explore,callers,callees,impact` 四个），`CODEGRAPH_MCP_TOOLS` 修正为 `explore,callers,callees,impact`（WorkBuddy `mcp.json` 与 Codex `config.toml` 同步修正）

## [2.0.3] - 2026-08-18

### Added
- `mcp/codegraph.md` 新增「使用前置检测（Preflight）」小节：Agent 调用任何 `codegraph_*` 工具前必须先探测（1）MCP 服务是否可用（2）目标项目是否已 `codegraph init`（存在 `.codegraph/`），任一不满足则显式退回 Read/Grep/Glob 并在报告标注，不靠盲目试错
- `agents/risk-controller/AGENT.md` 与 `agents/code-reviewer/AGENT.md` 的「when available」措辞改为先引用 Preflight 检测再使用
- 修正 `mcp/codegraph.md` WorkBuddy 配置示例：MCP 服务实际为隐藏子命令 `serve --mcp`，`args` 须为 `["serve","--mcp"]`（此前 `args: []` 会导致 MCP 起不来）
- 版本三处同步 2.0.2 → 2.0.3（CodeGraph 接入健壮性增强）

## [2.0.2] - 2026-08-18

### Added

- 新增可选代码智能契约 `mcp/codegraph.md`：接入本地代码知识图谱 CodeGraph（[@colbymchenry/codegraph](https://www.npmjs.com/package/@colbymchenry/codegraph)），含能力清单、MCP 工具启用（`CODEGRAPH_MCP_TOOLS`）、双端接入（Codex `codegraph install` 自动 / WorkBuddy 手动 `~/.workbuddy/mcp.json`）、隐私与依赖、与门禁的对应关系
- Risk Gate 文档 `agents/risk-controller/AGENT.md` 增加证据指引：优先用 `codegraph impact` 取影响面、`codegraph affected` 取必跑测试
- Review Pass 文档 `agents/code-reviewer/AGENT.md` 增加证据指引：优先用 `codegraph callers` / `codegraph callees` 验证调用链一致性
- 版本三处同步 2.0.1 → 2.0.2（可选能力新增）

## [2.0.1] - 2026-08-14

### Changed

- README 全面中文化：保留 1.x 整体介绍（项目定位/核心理念/Vibe vs Harness 对比/七大组件/八大 Agent/设计原则/文档分工），合并 v2.0 变更说明（Runtime/TaskState/Evidence Gate/动态路由/人工审批策略），目录树补齐英文版遗漏的 `skills/`、`mcp/` 与全部 8 个 Agent
- 版本三处同步 2.0.0 → 2.0.1（文档修订号）

## [2.0.0] - 2026-08-14

### Added

- Executable Harness Runtime in `runtime/` with graph loading, dynamic routing, TaskState helpers, policy helpers, trace/replay, and evidence-based gates.
- Machine-readable graph definitions for `trivial`, `normal`, `feature`, and `high-risk` workflows, including rollback, checkpoint/resume, and feature fan-out/fan-in.
- Unified `TaskState` schema at `runtime/schema/task_state.schema.json`.
- Feature memory layout and templates for `TECH_SPEC.md`, `subtasks.json`, `state.json`, evidence, reports, checkpoints, and timeline.
- `rules/policies.yaml` as the machine-readable policy source, including side-effect approval policy.
- Real executable gate wrappers for spec, design, risk, code style, security, review pass, test coverage, and knowledge stale checks.
- Repository Map L1/L2/L3 structure under `assets/project-wiki/` plus stale detector.
- Runtime docs, migration docs, release notes, unit tests, fixtures, and `scripts/self-check.py`.

### Changed

- Upgraded `config/harness.yaml` from a human explanation file to machine-readable JSON-compatible YAML.
- Updated `README.md` and `SKILL.md` for v2.0.0 Runtime usage.
- Updated PM Dispatcher, Risk Controller, Code Reviewer, and Project Recorder agent docs for runtime responsibilities.
- Reviewer policy now explicitly forbids inheriting Developer reasoning or chat history.

### Compatibility

- Existing Rule / Skill / Agent / Workflow / Script / MCP / Asset layout remains intact.
- Existing Markdown workflows remain human guidance; executable routing is now in `runtime/graphs/*.yaml`.

本文件记录 white-harness-engineering 的版本演进，遵循「全程追溯」原则。

## [1.2.2] - 2026-08-06

### 优化（减法审计落地，对照《模型越来越强，harness 该留下什么？》）

- rules 去重：`prohibited-actions.md` 改为分级索引，具体红线以 `security-rules.md` / `coding-standards.md` 为 SSOT，消除逐条双写漂移（A1/A2）
- 沉降工具层：`security-rules.md` / `coding-standards.md` 顶部明确「以 `scripts/check-security` / `check-code-style` 为准，违反即拦截」，指令层不再重复列清单（D1/D2）
- 穷举禁令改判据：命名法改为引用语言官方 style guide；函数/类/文件尺寸、依赖、结构复杂度改为可读性/单一职责判据；保留「禁止直推 main」与 commit 意图判据（B3/B5/B6/F1）
- 删 L0 公开知识：基础安全常识（HTTPS/密码加密/参数化查询）与命名风格法收敛为判据，不再逐条复述（F2）
- 示例→接口：review-checklist 安全/性能项改为判据+引用 SSOT；project-recorder 记录 schema 由完整样例改为字段枚举；ARCHITECTURE 的 yaml 示例标注为「参考性」（C1/C2/C3）
- 删冗余安全条目：容器/网络/最小权限/RBAC/Session 等平台默认或 L0 常识收敛为判据（E1-E4）
- README 版本标注补同步（V1，此前漏改）

## [1.2.1] - 2026-08-04

### 优化

- 精简 `SKILL.md` 的 `description`（281 字 → 150 字，降约 47%），触发词前置并补充「何时不触发」边界，提升 Codex 等兼容客户端的隐式匹配准确率与渐进式披露（progressive disclosure）效率
- README 顶部补版本徽章（version / license / clients）与版本三处同步说明，并打 `v1.2.0` 标签，使版本号在 GitHub Tags/Releases 可见
- README「使用方式」由 CodeBuddy 改为 Codex + WorkBuddy 双客户端安装与触发（Codex 走 `~/.agents/skills/` 或 `npx skills add`）

## [1.2.0] - 2026-08-03

### 新增

- 10 类报告的分类 HTML 模板（`assets/templates/reports/`）：代码审查 / 覆盖率 / 测试验证结果 / Bug 修复 / 重构 / 部署 / 项目初始化 / 风控 / 测试验收 / 代码库分析（repomix），全部基于统一骨架、预置分区结构
- 主 SKILL.md 报告规范增加「报告类型 → 模板文件」映射表；各子 Skill 的报告步骤改为直接引用对应分类模板
- 版本管理机制：SKILL.md frontmatter 增加 `version` 字段，与 `config/harness.yaml`、`CHANGELOG.md` 三处强制同步；新增「版本管理（维护者约定）」章节（SemVer 规则）

## [1.1.0] - 2026-08-03

### 修复（一致性缺陷）

- 补齐流水线引用但缺失的门禁：`scripts/check-design/` 与 `scripts/check-risk/`（校验项表 + 伪代码 + 判定标准）
- Karpathy 四原则三处副本 SSOT 化：`skills/karpathy-guidelines/SKILL.md` 为唯一事实源，`rules/` 版改为红线清单，`assets/knowledge-base/principles/` 版改为索引指针
- 修正 `pm-dispatcher` 路由表与主 SKILL.md 的矛盾：修 Bug → bug-fix-pipeline（code-developer + fix-bug skill）；重构默认走轻量 refactor 路径，仅架构级重构升级为 full-dev-pipeline
- USAGE.md 移除过时的 `F:\code\...` 硬编码路径，改为用户级技能自动触发为第一使用方式

### 优化

- HTML 报告骨架从主 SKILL.md 抽离为 `assets/templates/report-template.html`，SKILL.md 仅保留规范要点与模板引用
- `scripts/check-spec/check_spec.py` 落地为真实可执行 Python 脚本（stdlib only，exit 0/1/2 对应 PASS/FAIL/WARN，支持 --json）
- 子 Skill 头部统一：移除非标准 `disable: true` frontmatter，改为统一注释（repomix 补齐）
- 流水线超时数字单一源化：各阶段超时统一引用 `config/harness.yaml` timeout_overrides
- `assets/lesson-learned/` 补充强制落盘规范（`YYYY-MM-DD-问题关键词.md` + 索引表），fix-bug / code-review 沉淀步骤同步具体化
- SPEC.md 非功能量化指标标注生效阶段；README 补充「七大组件 vs 八大 Agent」说明；USAGE.md「效查清单」勘误为「效果检查清单」

## [1.0.0] - 2026-04

- 首次发布：Rule / Skill / Agent / Workflow / Scripts / MCP / Assets 七大组件与八分级 Agent 体系
