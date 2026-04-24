# 安全合规校验脚本

## 校验说明

对代码进行安全合规校验，确保不违反 L0/L1 级安全红线。

## 校验工具

| 工具 | 用途 | 扫描范围 |
|------|------|---------|
| SAST | 静态代码安全扫描 | 源代码 |
| 依赖扫描 | 第三方依赖漏洞扫描 | package.json / requirements.txt |
| 密钥扫描 | 硬编码密钥检测 | 全部文件 |
| 敏感信息扫描 | 日志中敏感信息检测 | 全部文件 |

## L0 级检查项（绝对禁止，违反即终止）

| # | 检查项 | 检测方式 |
|---|--------|---------|
| 1 | 硬编码密钥/密码/Token | 正则匹配 + entropy 检测 |
| 2 | 日志中打印敏感信息 | 模式匹配 |
| 3 | 使用 eval/exec 执行动态代码 | AST 分析 |
| 4 | SQL 语句拼接 | AST 分析 |
| 5 | 未参数化的数据库查询 | AST 分析 |
| 6 | 用户输入未校验 | 数据流分析 |

## L1 级检查项（强制禁止，违反即回退）

| # | 检查项 | 检测方式 |
|---|--------|---------|
| 1 | HTTP 通信（应使用 HTTPS） | URL 模式匹配 |
| 2 | 未认证的 API 接口 | 注解/装饰器分析 |
| 3 | 密码明文存储 | 数据流分析 |
| 4 | 缺少 CORS 配置 | 配置文件检查 |
| 5 | 文件上传未校验 | 代码模式匹配 |

## 依赖安全扫描

```bash
# Node.js
npm audit --json > security-report.json

# Python
safety check --json > security-report.json
pip-audit --format json > security-report.json

# Java
mvn org.owasp:dependency-check:check

# Go
nancy sleuth < go.sum
```

## 密钥扫描

```bash
# 使用 detect-secrets 或 trufflehog
detect-secrets scan --all-files --json > secrets-report.json
trufflehog filesystem ./src --json > secrets-report.json
```

## 判定标准

| 结果 | 条件 | 后续动作 |
|------|------|---------|
| PASS | 0 个 L0/L1 级问题 | 推进到代码审查 |
| FAIL | 有 L0 级问题 | 立即终止，必须修复 |
| FAIL | 有 L1 级问题 | 回退开发执行 Agent 修复 |
