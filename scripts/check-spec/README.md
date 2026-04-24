# SPEC 完整性校验脚本

## 校验说明

对需求拆解 Agent 产出的 SPEC 文档进行完整性校验，确保文档达到可交付标准。

## 校验项

| # | 校验项 | 级别 | 说明 |
|---|--------|------|------|
| 1 | 需求概述完整 | MUST | 包含背景、目标、成功指标 |
| 2 | 功能列表完整 | MUST | 每个功能有描述和优先级 |
| 3 | 验收标准可量化 | MUST | 每个功能有量化验收标准 |
| 4 | 非功能需求已明确 | SHOULD | 性能、安全、兼容性 |
| 5 | 技术约束已标注 | SHOULD | 技术栈、依赖、环境 |
| 6 | 风险和假设已识别 | SHOULD | 已知风险和前置假设 |
| 7 | 无歧义表述 | MUST | 不得有模糊/多义表述 |
| 8 | 成功指标可验证 | MUST | 指标可被客观验证 |

## 校验逻辑

```python
def check_spec(spec_doc_path: str) -> CheckResult:
    """
    SPEC 完整性校验
    
    Returns:
        CheckResult: PASS / WARN / FAIL
    """
    checks = []
    
    # 1. 检查必需章节
    required_sections = [
        "需求概述", "核心目标", "成功指标",
        "功能规格", "功能列表",
        "验收标准",
        "风险与假设"
    ]
    for section in required_sections:
        if not has_section(spec_doc_path, section):
            checks.append(Check(status="FAIL", message=f"缺少必需章节: {section}"))
    
    # 2. 检查功能列表格式
    features = parse_feature_list(spec_doc_path)
    for feature in features:
        if not feature.get("acceptance_criteria"):
            checks.append(Check(status="FAIL", message=f"功能 '{feature['name']}' 缺少量化验收标准"))
        if not feature.get("priority"):
            checks.append(Check(status="WARN", message=f"功能 '{feature['name']}' 缺少优先级标注"))
    
    # 3. 检查歧义表述
    ambiguous_patterns = ["可能", "大概", "也许", "尽量", "适当", "等", "相关"]
    ambiguities = find_patterns(spec_doc_path, ambiguous_patterns)
    if ambiguities:
        checks.append(Check(status="WARN", message=f"发现可能歧义的表述: {ambiguities}"))
    
    # 4. 判定结果
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
| PASS | 所有 MUST 和 SHOULD 项通过 | 推进到方案设计 |
| WARN | 所有 MUST 通过，有 SHOULD 未通过 | 标记警告，由 PM 决策 |
| FAIL | 有 MUST 项未通过 | 回退需求拆解 Agent 修复 |
