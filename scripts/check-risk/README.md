# 风控评审校验脚本

## 校验说明

对闸门风控 Agent 产出的风控报告进行校验，确保开发前的风险核验完整、结论明确。

## 校验项

| # | 校验项 | 级别 | 说明 |
|---|--------|------|------|
| 1 | Rule 合规性已逐项核验 | MUST | L0/L1 红线逐条核对并有结论 |
| 2 | 技术可行性已评估 | MUST | 关键技术路径有可行性结论 |
| 3 | 安全合规已检查 | MUST | 按 rules/security-rules.md 逐项核验 |
| 4 | 禁止操作已排查 | MUST | 按 rules/prohibited-actions.md 核验无触碰 |
| 5 | 资源与排期匹配 | SHOULD | 工作量评估与资源约束匹配 |
| 6 | 依赖风险已识别 | SHOULD | 外部依赖、第三方服务风险标注 |
| 7 | 每项风险有应对措施 | MUST | 识别出的风险均有缓解/规避方案 |
| 8 | 结论明确无歧义 | MUST | 通过 / 有条件通过 / 不通过，不允许模糊结论 |

## 校验逻辑

```python
def check_risk(risk_report_path: str, spec_doc_path: str, design_doc_path: str) -> CheckResult:
    """
    风控报告校验

    Returns:
        CheckResult: PASS / WARN / FAIL / BLOCK
    """
    checks = []

    # 1. 检查必需核验维度
    required_dimensions = [
        "Rule合规", "技术可行性", "安全合规", "禁止操作排查", "风险应对"
    ]
    for dim in required_dimensions:
        if not has_section(risk_report_path, dim):
            checks.append(Check(status="FAIL", message=f"缺少必需核验维度: {dim}"))

    # 2. L0 级风险直接 BLOCK
    l0_risks = find_l0_risks(risk_report_path)
    if l0_risks:
        checks.append(Check(status="BLOCK", message=f"发现 L0 级风险: {l0_risks}，终止流程"))
        return CheckResult(status="BLOCK", checks=checks)

    # 3. 风险应对完整性
    risks = parse_risk_list(risk_report_path)
    for risk in risks:
        if not risk.get("mitigation"):
            checks.append(Check(status="FAIL", message=f"风险 '{risk['name']}' 缺少应对措施"))

    # 4. 结论明确性
    if not has_clear_conclusion(risk_report_path):
        checks.append(Check(status="FAIL", message="风控结论不明确"))

    # 5. 判定结果
    if any(c.status == "FAIL" for c in checks):
        return CheckResult(status="FAIL", checks=checks)
    elif any(c.status == "WARN" for c in checks):
        return CheckResult(status="WARN", checks=checks)
    else:
        return CheckResult(status="PASS", checks=checks)
```

## 判定标准

| 结果 | 条件 | 后续动作 |
|------|------|---------|
| PASS | 所有 MUST 和 SHOULD 项通过，无 L0/L1 级风险 | 推进到开发执行 |
| WARN | 所有 MUST 通过，有 SHOULD 未通过 | 标记警告，由 PM 决策 |
| FAIL | 有 MUST 项未通过 | 回退方案设计 Agent 修复 |
| BLOCK | 发现 L0 级风险 | 暂停流水线，人工介入 |
