# 代码风格校验脚本

## 校验说明

对开发执行 Agent 产出的代码进行风格校验，确保符合团队编码规范。

## 支持的语言及工具

| 语言 | Lint 工具 | 配置文件 |
|------|---------|---------|
| TypeScript/JavaScript | ESLint + Prettier | `.eslintrc`, `.prettierrc` |
| Python | Pylint + Black + isort | `pyproject.toml` |
| Java | Checkstyle + SpotBugs | `checkstyle.xml` |
| Go | golangci-lint | `.golangci.yml` |

## 校验项

### 通用检查

| # | 校验项 | 级别 |
|---|--------|------|
| 1 | 命名规范（参照 `rules/coding-standards.md`） | MUST |
| 2 | 函数长度 ≤ 50 行 | SHOULD |
| 3 | 文件长度 ≤ 500 行 | SHOULD |
| 4 | 无调试代码残留 | MUST |
| 5 | 无注释掉的代码 | MUST |
| 6 | 无 TODO/FIXME/HACK 标记 | WARN |
| 7 | 导入排序规范 | SHOULD |

### 代码质量检查

| # | 校验项 | 级别 |
|---|--------|------|
| 1 | 无重复代码块 | SHOULD |
| 2 | 圈复杂度 ≤ 10 | SHOULD |
| 3 | 嵌套层级 ≤ 3 | MUST |
| 4 | 函数参数 ≤ 5 | SHOULD |
| 5 | 无未使用的变量/导入 | MUST |

## 校验逻辑

```bash
# TypeScript/JavaScript 项目
npx eslint src/ --format json --output-file lint-report.json
npx prettier --check src/

# Python 项目
pylint src/ --output-format=json > lint-report.json
black --check src/
isort --check src/

# Java 项目
mvn checkstyle:check
mvn spotbugs:check

# Go 项目
golangci-lint run ./... --out-format=json > lint-report.json
```

## 判定标准

| 结果 | 条件 | 后续动作 |
|------|------|---------|
| PASS | 0 error, 0 warning | 推进到代码审查 |
| WARN | 0 error, 有 warning | 标记警告，推进到代码审查 |
| FAIL | 有 error | 回退开发执行 Agent 修复 |
