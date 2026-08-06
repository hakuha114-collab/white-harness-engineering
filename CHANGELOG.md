# Changelog

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
