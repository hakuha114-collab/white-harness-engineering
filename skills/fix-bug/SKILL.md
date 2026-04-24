# Skill: Bug 修复

## 元信息

```yaml
name: fix-bug
version: 1.0.0
description: 标准化 Bug 修复流程，确保问题定位准确、修复彻底、不引入新问题
trigger:
  - "修 Bug"
  - "Bug 修复"
  - "修复问题"
  - "fix bug"
  - "问题排查"
inputs:
  - name: bug_description
    type: string
    required: true
    description: Bug 描述（现象、复现步骤、预期行为）
  - name: bug_id
    type: string
    required: false
    description: Bug 工单编号
outputs:
  - name: fix_code
    type: code
    description: 修复代码
  - name: regression_test
    type: code
    description: 回归测试代码
  - name: fix_report
    type: markdown
    description: 修复报告
rules:
  - rules/coding-standards.md
  - rules/security-rules.md
scripts:
  - scripts/check-code-style/
  - scripts/check-security/
  - scripts/check-test-coverage/
```

## 标准执行步骤

### Step 1: 问题复现

- 按 Bug 描述复现问题
- 确认复现条件（环境、数据、操作步骤）
- 记录复现过程

### Step 2: 根因分析

- 定位问题根因（不是表面现象）
- 分析影响范围
- 识别是否有同类隐患

使用 5-Why 分析法深挖根因：

```
现象 → 为什么？→ 原因1 → 为什么？→ 原因2 → ... → 根因
```

### Step 3: 修复方案

- 设计修复方案（不只修补表面，要解决根因）
- 评估修复影响范围
- 确认不引入新问题

### Step 4: 编写修复代码

- 实现修复
- 编写回归测试（先写测试，再修复，TDD 方式）
- 确认所有测试通过

### Step 5: 自检

- [ ] 根因已解决（非表面修补）
- [ ] 回归测试已通过
- [ ] 无新增 Lint 告警
- [ ] 无安全合规问题
- [ ] 修复不影响其他功能

### Step 6: 生成修复报告

```markdown
# Bug 修复报告

## Bug 信息
- Bug ID: [编号]
- 严重程度: [P0/P1/P2/P3]
- 影响范围: [描述]

## 根因分析
- 现象: [描述]
- 根因: [描述]
- 分析过程: [5-Why 记录]

## 修复方案
- 修复方式: [描述]
- 影响范围: [描述]
- 风险评估: [描述]

## 验证结果
- 回归测试: [通过/不通过]
- 原有测试: [通过/不通过]
- 手动验证: [通过/不通过]
```

### Step 7: 沉淀

- Bug 根因归入 `assets/lesson-learned/`
- 同类隐患排查建议归入 `assets/knowledge-base/`
