# 测试覆盖率校验脚本

## 校验说明

对测试验收 Agent 的产出进行覆盖率校验，确保测试充分性达标。

## 覆盖率标准

| 模块类型 | 行覆盖率 | 分支覆盖率 | 函数覆盖率 |
|---------|---------|-----------|-----------|
| 核心业务逻辑 | ≥ 80% | ≥ 70% | ≥ 90% |
| 通用工具类 | ≥ 90% | ≥ 80% | ≥ 95% |
| API 控制器 | ≥ 70% | ≥ 60% | ≥ 80% |
| 配置/常量 | ≥ 50% | — | — |

## 校验项

| # | 校验项 | 级别 |
|---|--------|------|
| 1 | 核心模块行覆盖率达标 | MUST |
| 2 | 核心模块分支覆盖率达标 | MUST |
| 3 | 所有测试通过 | MUST |
| 4 | 无跳过的测试 | SHOULD |
| 5 | 测试命名规范 | SHOULD |
| 6 | 测试独立性（无外部依赖） | MUST |

## 覆盖率检测命令

```bash
# TypeScript/JavaScript
npx jest --coverage --coverageReporters=json-summary --coverageReporters=lcov

# Python
pytest --cov=src --cov-report=json --cov-report=term-missing --cov-fail-under=80

# Java
mvn jacoco:report

# Go
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
```

## 报告格式

```json
{
  "summary": {
    "lines": { "total": 1000, "covered": 850, "percentage": 85.0 },
    "branches": { "total": 200, "covered": 150, "percentage": 75.0 },
    "functions": { "total": 100, "covered": 92, "percentage": 92.0 }
  },
  "modules": [
    {
      "name": "core",
      "lines": { "percentage": 88.5 },
      "branches": { "percentage": 76.2 },
      "status": "PASS"
    }
  ],
  "uncovered_files": ["src/utils/legacy.ts"],
  "status": "PASS"
}
```

## 判定标准

| 结果 | 条件 | 后续动作 |
|------|------|---------|
| PASS | 所有 MUST 项通过 | 交付完成 |
| WARN | MUST 通过但有 SHOULD 未通过 | 标记后推进，后续迭代补充 |
| FAIL | 有 MUST 项未通过 | 回退开发执行 Agent 补充测试 |
