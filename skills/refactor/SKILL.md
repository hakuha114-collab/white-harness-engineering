# Skill: 代码重构

## 元信息

```yaml
name: refactor
version: 1.0.0
description: 标准化代码重构流程，确保重构安全、渐进、可验证
trigger:
  - "重构"
  - "代码重构"
  - "优化代码"
  - "refactor"
  - "改善代码结构"
inputs:
  - name: target_path
    type: string
    required: true
    description: 待重构的代码路径
  - name: refactor_goal
    type: string
    required: true
    description: 重构目标（性能优化/可读性/可维护性/架构调整）
outputs:
  - name: refactored_code
    type: code
    description: 重构后的代码
  - name: test_results
    type: markdown
    description: 测试验证结果
  - name: refactor_report
    type: markdown
    description: 重构报告
rules:
  - rules/coding-standards.md
scripts:
  - scripts/check-code-style/
  - scripts/check-test-coverage/
```

## 标准执行步骤

### Step 1: 重构前准备

- ⚠️ **确认有足够测试覆盖**（核心逻辑 ≥ 80%）
- 运行现有测试，确认全部通过（基线）
- 记录当前性能指标（如涉及性能优化）

### Step 2: 分析重构范围

- 识别待重构模块的依赖关系
- 标记影响范围
- 评估重构风险

### Step 3: 小步重构

遵循 **小步前进、持续验证** 原则：

1. 每次只做一个小改动
2. 每次改动后立即运行测试
3. 测试通过后再做下一个改动

常用重构手法：
- 提取函数/方法
- 提取变量/常量
- 重命名（变量/函数/类）
- 移动函数/类
- 简化条件表达式
- 消除重复代码
- 替换临时变量
- 引入参数对象

### Step 4: 验证

- 所有原有测试通过
- 新增必要的测试
- 代码风格检查通过
- 性能指标无退化（或已改善）

### Step 5: 重构报告

```markdown
# 重构报告

## 重构目标
[描述]

## 重构范围
- 文件: [列表]
- 影响模块: [列表]

## 重构手法
| 步骤 | 手法 | 说明 |
|------|------|------|

## 验证结果
- 原有测试: [全部通过]
- 新增测试: [数量及通过情况]
- 代码风格: [通过/告警]
- 性能变化: [无变化/提升X%/退化X%]
```

## ⚠️ 重构红线

- ❌ **禁止** 在没有测试覆盖的情况下重构
- ❌ **禁止** 重构和功能修改同时进行
- ❌ **禁止** 一次重构跨越多个模块
- ❌ **禁止** 跳过测试验证直接提交
