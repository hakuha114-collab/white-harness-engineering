# Skill: 代码审查

## 元信息

```yaml
name: code-review
version: 1.0.0
description: 全维度校验代码规范、逻辑漏洞、性能隐患、安全bug，做好技术质量收口
trigger:
  - "代码审查"
  - "code review"
  - "review"
  - "PR 审查"
  - "代码检查"
inputs:
  - name: pr_url
    type: string
    required: true
    description: PR 地址或变更文件路径
  - name: spec_doc
    type: string
    required: false
    description: 关联的 SPEC 文档路径
outputs:
  - name: review_report
    type: markdown
    description: Review 报告（含问题清单和改进建议）
rules:
  - rules/coding-standards.md
  - rules/security-rules.md
  - rules/review-checklist.md
  - rules/prohibited-actions.md
scripts:
  - scripts/check-code-style/
  - scripts/check-security/
  - scripts/check-review-pass/
```

## 标准执行步骤

### Step 1: 加载上下文

- 读取 PR 变更内容
- 读取关联的 SPEC 文档（如有）
- 加载 Review 检查清单：`rules/review-checklist.md`

### Step 2: 自动化检查

运行自动化脚本：

1. `scripts/check-code-style/` — 代码风格校验
2. `scripts/check-security/` — 安全合规校验

### Step 3: 人工级 Review

按 `rules/review-checklist.md` 逐项审查：

| 维度 | 检查项 |
|------|--------|
| 功能正确性 | 逻辑正确、边界处理、异常处理 |
| 代码质量 | 可读性、可维护性、DRY、SOLID |
| 安全合规 | 注入风险、认证授权、数据安全 |
| 测试覆盖 | 单元测试、边界测试、异常测试 |
| 架构一致 | 分层正确、依赖方向、模块边界 |

### Step 4: 生成 Review 报告

```markdown
# Code Review 报告

## 基本信息
- PR: [链接]
- 审查人: [Agent ID]
- 审查时间: [时间]

## 审查结论: [通过 / 不通过 / 有条件通过]

## 问题清单

### [MUST] 必须修改
| # | 文件 | 行号 | 问题描述 | 修改建议 |
|---|------|------|---------|---------|

### [SHOULD] 建议修改
| # | 文件 | 行号 | 问题描述 | 修改建议 |
|---|------|------|---------|---------|

### [NICE] 可选优化
| # | 文件 | 行号 | 优化建议 |
|---|------|------|---------|

## 亮点
- [值得肯定的做法]
```

### Step 5: 判定与流转

- **通过**: 无 MUST 项 → 移交测试验收 Agent
- **不通过**: 有 MUST 项 → 回退开发执行 Agent，附修改建议
- **有条件通过**: 仅有 SHOULD/NICE 项 → 标记后推进，由 PM 决策

### Step 6: 沉淀

- 共性问题归入 `assets/lesson-learned/`
- 好的做法归入 `assets/knowledge-base/`
