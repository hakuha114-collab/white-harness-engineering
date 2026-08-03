# 使用指南

> 本文档说明如何将 white-harness-engineering 应用到实际 AI 辅助软件开发中。

---

## 一、快速上手（3 分钟）

### 方式 A：用户级技能自动触发（推荐，零配置）

本技能安装为用户级技能（`~/.workbuddy/skills/white-harness-engineering`）后，**在任意工作区对话中意图匹配即自动加载**，无需任何路径配置：

```
打开 CodeBuddy / WorkBuddy
  ↓
进入你的项目工作区
  ↓
直接下达开发任务（如"帮我开发一个登录功能"）
  ↓
AI 自动加载本技能的 Rule 约束与对应子 Skill
```

也可以显式强制加载：

```
请按 Harness Engineering 规范 / Karpathy 四原则执行本次任务，先输出思考文档。
```

### 方式 B：把技能仓库作为工作区打开

将本技能源码仓库作为工作区打开后，AI 能直接读取所有 Rule 和 Skill 文件，适合需要**修改框架本身**（补充红线、扩展子 Skill）的场景。

### 方式 C：跨项目显式引用单个规范文件

在任意项目的对话框中引用技能内的相对路径（以实际安装位置为根）：

```
请按以下规范执行本次任务：
- 编程原则：参考 rules/karpathy-guidelines.md（红线清单）
- 执行细则：参考 skills/karpathy-guidelines/SKILL.md
- 代码规范：参考 rules/coding-standards.md
- 安全规范：参考 rules/security-rules.md
```

---

## 二、核心使用流程

### 完整开发任务（推荐流程）

```
【你】:"我要开发一个用户登录功能，支持手机号+验证码登录"

  ↓  AI 自动执行 Karpathy 原则 Step 1：先思考再编码

【AI】:输出思考文档
  - 假设清单（验证码有效期？错误次数限制？）
  - 多种方案对比（JWT vs Session？）
  - 待确认问题 ← 此时你补充信息

  ↓  你确认后，AI 执行 Step 2-4

【AI】:简洁实现 → 精准修改 → 目标驱动验证
  - 只写必要的代码
  - 每步有验证计划
  - 输出测试 + 代码

  ↓  自动触发代码审查

【AI】:按 review-checklist.md 执行审查
  - 检查 Karpathy 四原则合规性
  - 输出审查报告（MUST/SHOULD/NICE）

  ↓  你确认后进入测试验收

【AI】:按 write-test SKILL 生成测试用例
  - 正常路径 / 边界值 / 异常路径
  - 运行测试，输出覆盖率报告
```

---

## 三、各场景使用方式

### 场景 1：新功能开发

**触发方式**：直接描述需求即可，AI 会自动加载 `skills/create-spec/` 和 `skills/karpathy-guidelines/`

```
我要开发一个 XX 功能：
- 背景：...
- 核心需求：...
- 技术要求：...

请按 Harness Engineering 规范执行，先输出思考文档再编码。
```

**AI 会自动**：
1. 读取 `skills/karpathy-guidelines/SKILL.md` → 执行四原则
2. 读取 `skills/create-spec/SKILL.md` → 输出 SPEC
3. 读取 `rules/coding-standards.md` → 按规范编码
4. 读取 `skills/code-review/SKILL.md` → 自我审查

---

### 场景 2：Bug 修复

```
Bug 描述：
- 现象：...
- 复现步骤：...
- 预期行为：...

请按 fix-bug Skill 执行，先写测试复现再修复。
```

**AI 会按 `skills/fix-bug/SKILL.md` 执行**：
1. 复现问题（输出复现步骤）
2. 根因分析（5-Why 分析）
3. 先写测试复现 Bug
4. 修复代码使测试通过
5. 输出修复报告

---

### 场景 3：代码审查

```
请审查这段代码，按 review-checklist.md 和 karpathy 四原则执行。

[粘贴代码或提供文件路径]
```

**AI 会按 `skills/code-review/SKILL.md` 执行**：
1. 运行 `scripts/check-code-style/` 逻辑检查风格
2. 运行 `scripts/check-security/` 逻辑检查安全
3. 按 Karpathy 四原则检查代码质量
4. 输出分级审查报告（HTML）

---

### 场景 4：重构

```
请重构 src/services/user-service.ts，
按 karpathy 的简洁优先原则执行，
重构前先确认测试覆盖率达标。
```

**AI 会按 `skills/refactor/SKILL.md` 执行**：
1. 先检查测试覆盖率（不足先补测试）
2. 小步重构，每步验证测试通过
3. 只清理自己造成的孤立代码

---

## 四、Rules 如何生效

### 自动生效（推荐）

作为用户级技能安装后，意图匹配时 AI 自动读取：

```
rules/karpathy-guidelines.md → 编码前红线检查（细则见 skills/karpathy-guidelines/）
rules/coding-standards.md    → 编码时自动遵守
rules/security-rules.md      → 编码时自动检查
rules/review-checklist.md    → 审查时自动核对
rules/prohibited-actions.md  → 自动规避禁止操作
```

### 手动引用（强制加载）

在任何对话框中显式要求：

```
请按 Karpathy 四原则执行本次任务，先输出思考文档。
```

---

## 五、Skills 如何触发

Skills 通过关键词自动触发，无需手动调用。**路由对应关系以主入口 `SKILL.md`「按用户意图路由到对应子 Skill」表为唯一事实源**，摘要如下：

| 你说的话 | 自动触发的 Skill |
|-----------|---------------------|
| "新需求 / 写 SPEC / 需求分析" | `skills/create-spec/` |
| "代码审查 / review / PR 审查" | `skills/code-review/` |
| "写测试 / 单元测试 / 测试用例" | `skills/write-test/` |
| "修 Bug / Bug 修复" | `skills/fix-bug/` |
| "重构 / 优化代码" | `skills/refactor/` |
| "部署 / 发布" | `skills/deploy/` |
| "初始化项目 / 搭建工程" | `skills/project-setup/` |
| （任何编码任务） | `skills/karpathy-guidelines/` ← 总是生效 |

---

## 六、Workflows 如何使用

Workflows 是流程蓝图，AI 按其中的定义执行多步骤任务：

### 使用完整研发流水线

```
按 workflows/full-dev-pipeline.md 执行以下需求：
[需求描述]
```

AI 会按流水线定义依次执行：
`需求拆解 → 方案设计 → 风控评估 → 开发执行 → 代码审查 → 测试验收`

每个环节完成后自动校验门禁，不通过则回退。

---

## 七、门禁校验如何工作

门禁是"关卡"，AI 在每个环节结束时自动运行校验：

```
开发执行完成
  ↓
AI 自动运行 check-code-style 逻辑（对照 rules/coding-standards.md）
AI 自动运行 check-security 逻辑（对照 rules/security-rules.md）
  ↓
全部通过 → 进入代码审查
有 MUST 级问题 → 自动修复或提示你确认
```

**门禁分两级实现**：
- **可执行脚本**：`scripts/check-spec/check_spec.py` 已落地为真实 Python 脚本，可直接运行机器校验；
- **逻辑校验**：其余门禁当前为 AI 读规则后自查（各 `scripts/check-*/README.md` 描述了校验项与伪代码），后续可同样升级为真实脚本（接入 ESLint、pytest 等工具）。

---

## 八、推荐的工作区配置

### 单工作区模式（推荐，默认）

```
CodeBuddy / WorkBuddy 工作区 = 你的项目目录
  ↓
技能作为用户级技能自动生效，无需额外配置
```

### 双工作区模式（需要修改框架本身时）

```
工作区 1：本技能源码仓库（规范库）
工作区 2：你的实际项目（开发目录）
  ↓
AI 可以同时读取两个工作区的文件
```

---

## 九、效果检查清单

使用本框架后，你应该能看到这些改善：

- [ ] AI 在编码前会先输出思考文档（假设、权衡、方案对比）
- [ ] 代码 diff 干净，没有无关的"顺手改进"
- [ ] 代码简洁，没有过度抽象
- [ ] 每个任务都有验证计划（测试先行或成功标准明确）
- [ ] 代码审查报告有分级（MUST/SHOULD/NICE）
- [ ] 门禁不通过时 AI 会自动修复而非跳过

---

## 十、后续升级路径

| 阶段 | 做什么 | 效果 |
|------|--------|------|
| 现在 | 用 `.md` 规范约束 AI + check-spec 真实脚本 | AI 读规则后自查，SPEC 门禁已机器化，75% 效果 |
| 下一步 | 其余 Scripts 落地为真实可执行脚本（ESLint 配置、pytest 等） | 自动化校验，90% 效果 |
| 再下一步 | 搭建 Orchestrator 引擎，自动调度 Agent 和门禁 | 全自动流水线，100% 效果 |

---

**快速开始**：进入任意项目工作区 → 输入"按 Karpathy 四原则帮我开发一个 XX 功能，先输出思考文档" → 开始体验。
