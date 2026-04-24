# Bug 修复流水线

> 快速响应 Bug 修复，确保定位准确、修复彻底、不引入新问题

## 流程定义

```yaml
workflow:
  name: bug-fix-pipeline
  version: 1.0.0
  description: Bug 修复专用流水线，快速定位、修复、验证
  agents:
    - pm-dispatcher
    - risk-controller
    - code-developer
    - code-reviewer
    - test-validator
```

## 流程图

```
[Bug 报告]
    │
    ▼
[PM调度Agent] ─── 任务路由 ───▶ [闸门风控Agent] ── 快速评估
                                     │
                                     │ 产出: 风控报告（Bug 定级 + 影响范围）
                                     ▼
                              [开发执行Agent] ── 修复 Bug
                                     │
                                     │ 产出: 修复代码 + 回归测试
                                     │ 门禁: check-code-style + check-security
                                     ▼
                              [代码审查Agent] ── 审查修复
                                     │
                                     │ 产出: 审查报告
                                     │ 门禁: check-review-pass
                                     ▼
                              [测试验收Agent] ── 回归验证
                                     │
                                     │ 产出: 测试报告
                                     │ 门禁: check-test-coverage
                                     ▼
                              [修复完成] ✅
```

## Bug 定级标准

| 等级 | 定义 | 响应时间 | 修复时间 |
|------|------|---------|---------|
| P0 | 线上故障，影响核心功能 | 15 分钟内响应 | 2 小时内修复 |
| P1 | 重要功能异常，影响用户体验 | 1 小时内响应 | 8 小时内修复 |
| P2 | 一般功能问题，有临时规避方案 | 4 小时内响应 | 24 小时内修复 |
| P3 | 轻微问题，不影响正常使用 | 24 小时内响应 | 下一迭代修复 |

## 与全流程的差异

| 方面 | 全流程 | Bug 修复流程 |
|------|--------|-------------|
| 需求分析 | 有 | 跳过（Bug 描述即需求） |
| 方案设计 | 有 | 跳过（修复方案简单直接） |
| 闸门风控 | 有 | 简化（聚焦 Bug 影响评估） |
| 开发执行 | 有 | 有（使用 `skills/fix-bug/`） |
| 代码审查 | 有 | 有（聚焦修复正确性） |
| 测试验收 | 有 | 有（聚焦回归测试） |

## 沉淀要求

- Bug 根因必须归入 `assets/lesson-learned/`
- 同类隐患排查建议归入 `assets/knowledge-base/`
- 更新相关 Rule（如发现新红线）
