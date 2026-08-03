# 设计文档校验脚本

## 校验说明

对方案设计 Agent 产出的设计文档进行完整性与合规性校验，确保方案可进入风控评审。

## 校验项

| # | 校验项 | 级别 | 说明 |
|---|--------|------|------|
| 1 | 设计目标与 SPEC 对齐 | MUST | 每个功能点都有对应设计覆盖 |
| 2 | 架构分层明确 | MUST | 模块划分、职责边界、依赖方向清晰 |
| 3 | 技术选型有依据 | MUST | 关键技术选型给出理由与备选对比 |
| 4 | 接口契约已定义 | MUST | 模块间接口有明确的输入/输出定义 |
| 5 | 数据模型已定义 | SHOULD | 核心实体、字段、关系明确 |
| 6 | 非功能设计已覆盖 | SHOULD | 性能、安全、降级、兼容性设计 |
| 7 | 风险点已标注 | MUST | 技术风险与不确定性显式标注 |
| 8 | 无超出 SPEC 的设计 | SHOULD | 不存在 SPEC 之外的过度设计 |

## 校验逻辑

```python
def check_design(design_doc_path: str, spec_doc_path: str) -> CheckResult:
    """
    设计文档完整性校验

    Returns:
        CheckResult: PASS / WARN / FAIL
    """
    checks = []

    # 1. 检查必需章节
    required_sections = [
        "设计目标", "架构设计", "模块划分",
        "接口定义", "技术选型", "风险标注"
    ]
    for section in required_sections:
        if not has_section(design_doc_path, section):
            checks.append(Check(status="FAIL", message=f"缺少必需章节: {section}"))

    # 2. SPEC 功能覆盖检查
    spec_features = parse_feature_list(spec_doc_path)
    for feature in spec_features:
        if not is_covered_by_design(design_doc_path, feature):
            checks.append(Check(status="FAIL", message=f"SPEC 功能 '{feature['name']}' 无对应设计"))

    # 3. 过度设计检查
    design_modules = parse_module_list(design_doc_path)
    for module in design_modules:
        if not traceable_to_spec(spec_doc_path, module):
            checks.append(Check(status="WARN", message=f"模块 '{module['name']}' 无法追溯到 SPEC，疑似过度设计"))

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
| PASS | 所有 MUST 和 SHOULD 项通过 | 推进到闸门风控 |
| WARN | 所有 MUST 通过，有 SHOULD 未通过 | 标记警告，由 PM 决策 |
| FAIL | 有 MUST 项未通过 | 回退方案设计 Agent 修复 |
