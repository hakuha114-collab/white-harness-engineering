# Skill: Karpathy 编程规范

## 元信息

```yaml
name: karpathy-guidelines
version: 1.0.0
description: |
  基于 Andrej Karpathy 对 LLM 编程三大致命问题的观察，提炼的四大约束原则：
  先思考再编码、简洁优先、精准修改、目标驱动执行。
  适用于所有 AI 辅助开发场景，减少错误假设、过度复杂化和附带破坏。
trigger:
  - "开发"
  - "写代码"
  - "编码"
  - "修Bug"
  - "重构"
  - "添加功能"
  - "实现需求"
  - "code"
  - "develop"
  - "implement"
  - "编程规范"
  - "karpathy"
inputs:
  - name: task_description
    type: string
    required: true
    description: 任务描述
  - name: code_context
    type: string
    required: false
    description: 待修改的代码路径或上下文
outputs:
  - name: thinking_doc
    type: markdown
    description: 思考文档（假设、权衡、方案对比）
  - name: code_output
    type: code
    description: 代码产出
  - name: verification_plan
    type: markdown
    description: 验证计划
rules:
  - rules/karpathy-guidelines.md
  - rules/coding-standards.md
  - rules/security-rules.md
scripts:
  - scripts/check-code-style/
  - scripts/check-review-pass/
```

## 标准执行步骤

### Step 1: 先思考再编码 (Think Before Coding)

在写任何代码之前，**必须**输出思考文档：

```markdown
# 思考文档

## 任务理解
[用自己的话复述任务，确认理解正确]

## 假设清单
| # | 假设 | 确信度 | 需要确认？ |
|---|------|--------|-----------|
| 1 | ... | 高/中/低 | 是/否 |

## 多种解读
[如果存在多种理解，列出每种解读及对应方案]

## 权衡分析
| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|

## 最简方案
[选择最简单的方案，说明理由]

## 待确认问题
[列出需要用户确认的问题]
```

**决策规则**：
- 如果有"需确认"的假设 → **停止**，先向用户确认
- 如果有多种解读 → **呈现所有选项**，请用户选择
- 如果有更简单的方案 → **提出来**，说明理由

### Step 2: 简洁实现 (Simplicity First)

确认方案后，按最简方式实现：

**检查清单**（编码时自检）：
- [ ] 只实现被要求的功能，不多不少
- [ ] 没有未被请求的抽象
- [ ] 没有未被请求的"灵活性"
- [ ] 没有不可能发生的错误处理
- [ ] 代码行数是否可以更少？如果是，简化

**复杂度检查**：
```
问自己：一个高级工程师会说这过度复杂了吗？
  → 是：简化
  → 否：继续
```

### Step 3: 精准修改 (Surgical Changes)

如果修改现有代码：

**修改前检查**：
- [ ] 列出所有需要修改的文件和行
- [ ] 每处修改都能追溯到用户请求
- [ ] 不包含任何"顺手改进"

**修改后检查**：
- [ ] diff 中只有请求相关的变更
- [ ] 没有风格漂移（引号、命名、间距与原代码一致）
- [ ] 自己产生的孤立代码已清理
- [ ] 原有的死代码未触碰（只提了一下）

### Step 4: 目标驱动验证 (Goal-Driven Execution)

定义成功标准并验证：

```markdown
# 验证计划

## 成功标准
| # | 标准 | 验证方式 | 结果 |
|---|------|---------|------|
| 1 | ... | [测试/检查] | ⬜ |

## 执行步骤
1. [步骤] → 验证: [检查方式]
2. [步骤] → 验证: [检查方式]
3. [步骤] → 验证: [检查方式]
```

**验证规则**：
- 每个步骤都有明确的验证方式
- 修改代码 → 先写测试复现问题 → 修复 → 确认测试通过
- 重构代码 → 确认重构前后测试都通过
- 新功能 → 写测试定义预期行为 → 实现 → 确认测试通过

## 反模式速查

| 原则 | ❌ 反模式 | ✅ 正确做法 |
|------|---------|-----------|
| 先思考 | 默默假设格式/字段/范围 | 明确列出假设，请求澄清 |
| 简洁优先 | 用策略模式做单一折扣计算 | 只用一个函数，直到真正需要复杂度 |
| 精准修改 | 修 Bug 时顺手改引号风格 | 只修改解决问题的那几行 |
| 目标驱动 | "我会审查并改进代码" | "写测试复现 Bug → 使其通过 → 验证无回归" |

## 示例

### 示例 1：简洁优先 — 折扣计算

**用户**: "添加计算折扣的函数"

❌ **过度复杂化**:
```python
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: ...

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float, config: DiscountConfig): ...
    def calculate(self, amount: float) -> float: ...

class FixedDiscount(DiscountStrategy):
    def __init__(self, fixed_amount: float, config: DiscountConfig): ...
    def calculate(self, amount: float) -> float: ...

class DiscountCalculator:
    def __init__(self, strategy: DiscountStrategy): ...
    def apply(self, amount: float) -> float: ...
```

✅ **简洁实现**:
```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)
```

> 仅当真正需要多种折扣类型时才重构。

### 示例 2：精准修改 — 修 Bug

**用户**: "修复空邮箱导致验证器崩溃的 bug"

❌ **附带修改**:
- 修复了空邮箱处理 ✓
- "改进"了邮箱验证正则 ✗
- 添加了用户名验证 ✗
- 修改了注释 ✗
- 加了 docstring ✗

✅ **精准修改**:
- 只修复空邮箱处理的那几行代码
- 其他一律不动

### 示例 3：目标驱动 — 添加限流

**用户**: "给 API 添加限流"

❌ **一次性大实现**: 300 行完整方案，无验证步骤

✅ **分步验证**:
```
1. 基本内存限流（单端点）→ 验证: 测试限流触发
2. 提取为中间件（所有端点）→ 验证: 测试中间件生效
3. 添加 Redis 后端（多服务器）→ 验证: 测试分布式限流
4. 添加配置（每端点不同限流）→ 验证: 测试差异化配置
```

## 适用范围

- **严格适用**: 非琐碎的开发任务（新功能、Bug修复、重构、API变更）
- **灵活适用**: 简单任务（错别字修复、明显一行修改）可自行判断
- **不适用**: 纯文档修改、配置调整（不需要思考文档和验证计划）
