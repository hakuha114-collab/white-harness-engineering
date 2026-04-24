# Review 通过校验脚本

## 校验说明

对代码审查 Agent 的审查结果进行校验，确保 Review 流程合规完成。

## 校验项

| # | 校验项 | 级别 | 说明 |
|---|--------|------|------|
| 1 | 审查报告已生成 | MUST | 有完整的 Review 报告 |
| 2 | 无 MUST 级遗留问题 | MUST | 所有 [MUST] 项已关闭 |
| 3 | 审查覆盖率 ≥ 100% | MUST | 所有变更文件已审查 |
| 4 | 安全检查已通过 | MUST | check-security 结果为 PASS |
| 5 | 代码风格检查已通过 | MUST | check-code-style 结果为 PASS |
| 6 | SHOULD 级问题有处理计划 | SHOULD | 遗留的 [SHOULD] 有预期处理时间 |

## 校验逻辑

```python
def check_review_pass(review_report: dict) -> CheckResult:
    checks = []
    
    # 1. 检查审查报告完整性
    if not review_report.get("reviewer"):
        checks.append(Check(status="FAIL", message="审查报告缺少审查人信息"))
    if not review_report.get("conclusion"):
        checks.append(Check(status="FAIL", message="审查报告缺少审查结论"))
    
    # 2. 检查 MUST 级问题
    must_items = [i for i in review_report.get("issues", []) if i["level"] == "MUST"]
    open_must = [i for i in must_items if i["status"] != "resolved"]
    if open_must:
        checks.append(Check(
            status="FAIL", 
            message=f"存在 {len(open_must)} 个未解决的 MUST 级问题"
        ))
    
    # 3. 检查审查覆盖率
    if review_report.get("coverage", 0) < 100:
        checks.append(Check(status="FAIL", message="审查覆盖率未达 100%"))
    
    # 4. 检查前置门禁
    if review_report.get("security_check") != "PASS":
        checks.append(Check(status="FAIL", message="安全检查未通过"))
    if review_report.get("style_check") != "PASS":
        checks.append(Check(status="FAIL", message="代码风格检查未通过"))
    
    return CheckResult(
        status="FAIL" if any(c.status == "FAIL" for c in checks) else "PASS",
        checks=checks
    )
```

## 判定标准

| 结果 | 条件 | 后续动作 |
|------|------|---------|
| PASS | 所有 MUST 项通过 | 推进到测试验收 |
| FAIL | 有 MUST 项未通过 | 回退开发执行 Agent 修复 |
