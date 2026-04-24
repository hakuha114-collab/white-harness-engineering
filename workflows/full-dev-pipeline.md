# 完整研发流水线

> 标准「需求 → 设计 → 风控 → 开发 → 审查 → 测试 → 交付」全流程

## 流程定义

```yaml
workflow:
  name: full-dev-pipeline
  version: 1.0.0
  description: 完整研发流水线，覆盖从需求到交付的全链路
  agents:
    - pm-dispatcher
    - requirement-analyzer
    - solution-designer
    - risk-controller
    - code-developer
    - code-reviewer
    - test-validator
```

## 流程图

```
[用户需求]
    │
    ▼
[PM调度Agent] ─── 任务路由 ───▶ [需求拆解Agent]
                                     │
                                     │ 产出: SPEC 文档
                                     │ 门禁: check-spec
                                     ▼
                              [方案设计Agent]
                                     │
                                     │ 产出: 设计文档
                                     │ 门禁: check-design
                                     ▼
                              [闸门风控Agent]
                                     │
                                     │ 产出: 风控报告
                                     │ 门禁: check-risk
                                     ▼
                              [开发执行Agent]
                                     │
                                     │ 产出: 代码 + 单元测试
                                     │ 门禁: check-code-style + check-security
                                     ▼
                              [代码审查Agent]
                                     │
                                     │ 产出: 审查报告
                                     │ 门禁: check-review-pass
                                     ▼
                              [测试验收Agent]
                                     │
                                     │ 产出: 测试报告
                                     │ 门禁: check-test-coverage
                                     ▼
                              [交付完成] ✅
```

## 详细流转规则

### 阶段 1: 需求分析

| 项目 | 说明 |
|------|------|
| 执行 Agent | requirement-analyzer |
| 输入 | 用户原始需求 |
| 产出 | SPEC 文档 |
| 门禁 | `scripts/check-spec/` |
| 通过条件 | SPEC 完整性校验通过 |
| 不通过处理 | 自行修复后重试，最多 3 次 |
| 超时 | 30 分钟 |
| 下一环节 | 方案设计 |

### 阶段 2: 方案设计

| 项目 | 说明 |
|------|------|
| 执行 Agent | solution-designer |
| 输入 | SPEC 文档 |
| 产出 | 设计文档 |
| 门禁 | `scripts/check-design/` |
| 通过条件 | 设计完整性和合规性校验通过 |
| 不通过处理 | 回退需求拆解 Agent |
| 超时 | 60 分钟 |
| 下一环节 | 闸门风控 |

### 阶段 3: 闸门风控

| 项目 | 说明 |
|------|------|
| 执行 Agent | risk-controller |
| 输入 | SPEC + 设计文档 |
| 产出 | 风控报告 |
| 门禁 | `scripts/check-risk/` |
| 通过条件 | 无 L0/L1 级风险 |
| 不通过处理 | 回退方案设计 Agent |
| 超时 | 30 分钟 |
| 下一环节 | 开发执行 |

### 阶段 4: 开发执行

| 项目 | 说明 |
|------|------|
| 执行 Agent | code-developer |
| 输入 | SPEC + 设计文档 + 风控报告 |
| 产出 | 代码 + 单元测试 |
| 门禁 | `scripts/check-code-style/` + `scripts/check-security/` |
| 通过条件 | Lint 通过 + 安全检查通过 + 单元测试通过 |
| 不通过处理 | 自行修复后重试 |
| 超时 | 120 分钟 |
| 下一环节 | 代码审查 |

### 阶段 5: 代码审查

| 项目 | 说明 |
|------|------|
| 执行 Agent | code-reviewer |
| 输入 | 代码 + SPEC |
| 产出 | 审查报告 |
| 门禁 | `scripts/check-review-pass/` |
| 通过条件 | 无 MUST 级问题 |
| 不通过处理 | 回退开发执行 Agent |
| 超时 | 60 分钟 |
| 下一环节 | 测试验收 |

### 阶段 6: 测试验收

| 项目 | 说明 |
|------|------|
| 执行 Agent | test-validator |
| 输入 | 代码 + 审查报告 |
| 产出 | 测试报告 |
| 门禁 | `scripts/check-test-coverage/` |
| 通过条件 | 覆盖率达标 + 功能通过 + 性能达标 |
| 不通过处理 | 回退开发执行 Agent（L1）或方案设计 Agent（L2） |
| 超时 | 90 分钟 |
| 下一环节 | 交付 |

### 阶段 7: 交付

| 项目 | 说明 |
|------|------|
| 执行 Agent | pm-dispatcher |
| 输入 | 全部产出物 |
| 产出 | 交付确认 |
| 操作 | 更新任务状态、归档产出物、沉淀资产 |

## 回退策略

```
回退映射:
  test-validator    → code-developer (L1) / solution-designer (L2) / requirement-analyzer (L3)
  code-reviewer     → code-developer
  code-developer    → risk-controller (L1) / solution-designer (L2)
  risk-controller   → solution-designer
  solution-designer → requirement-analyzer
  requirement-analyzer → pm-dispatcher (请求补充信息)

回退限制:
  - 同一环节回退最多 3 次
  - 超过 3 次自动升级为人工处理
  - L0 级风险直接终止流程
```
