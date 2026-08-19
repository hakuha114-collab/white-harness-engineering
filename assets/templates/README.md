# 标准模板库

> 提供各类标准模板，Agent 可直接引用

## 模板列表

| 模板 | 文件 | 使用场景 |
|------|------|---------|
| SPEC 文档模板 | `spec-template.md` | 需求拆解 Agent（验收标准须量化，可被 `scripts/check-spec/check_spec.py` 机器校验） |
| HTML 报告通用骨架 | `report-template.html` | 所有报告类产出的基础骨架 |
| 代码审查报告模板 | `reports/review-report.html` | code-review |
| 覆盖率报告模板 | `reports/coverage-report.html` | write-test |
| 测试验证结果模板 | `reports/test-results.html` | refactor / write-test |
| Bug 修复报告模板 | `reports/fix-report.html` | fix-bug |
| 重构报告模板 | `reports/refactor-report.html` | refactor |
| 部署报告模板 | `reports/deploy-report.html` | deploy |
| 项目初始化报告模板 | `reports/setup-report.html` | project-setup |
| 风控报告模板 | `reports/risk-report.html` | risk-controller |
| 测试验收报告模板 | `reports/acceptance-report.html` | test-validator |
| 代码库分析报告模板 | `reports/repomix-report.html` | repomix |

## 模板使用规范

1. Agent 产出文档时，必须基于对应模板
2. 模板中的必填项不可省略
3. 可根据项目特点扩展模板字段
4. 新增/重命名模板时，必须同步更新本表与主 `SKILL.md` 的「报告类型 → 模板文件」映射表
