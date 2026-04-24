# Skill: 编写测试用例

## 元信息

```yaml
name: write-test
version: 1.0.0
description: 为功能代码编写结构化测试用例，确保功能正确性和边界覆盖
trigger:
  - "写测试"
  - "测试用例"
  - "单元测试"
  - "测试覆盖"
  - "写 UT"
inputs:
  - name: source_path
    type: string
    required: true
    description: 待测试的源代码路径
  - name: spec_doc
    type: string
    required: false
    description: 关联的 SPEC 文档（用于提取验收标准）
outputs:
  - name: test_file
    type: code
    description: 测试代码文件
  - name: coverage_report
    type: markdown
    description: 覆盖率报告
rules:
  - rules/coding-standards.md
scripts:
  - scripts/check-test-coverage/
```

## 标准执行步骤

### Step 1: 分析源代码

- 读取源代码，识别所有公共函数/方法
- 分析每个函数的输入输出
- 识别边界条件和异常路径

### Step 2: 提取测试场景

| 测试类型 | 说明 | 覆盖目标 |
|---------|------|---------|
| 正常路径 | 标准输入 → 预期输出 | 核心功能验证 |
| 边界值 | 空值、零值、最大值、最小值 | 边界条件 |
| 异常路径 | 非法输入、异常抛出 | 错误处理 |
| 并发场景 | 竞态条件、资源冲突 | 并发安全 |
| 性能测试 | 大数据量、高频调用 | 性能基线 |

### Step 3: 编写测试代码

遵循命名规范：
```
test_[函数名]_[场景]_[预期结果]

例: test_getUser_whenIdIsNull_shouldThrowException
    test_calculateTotal_withDiscount_shouldReturnDiscountedPrice
```

### Step 4: 运行测试

- 执行所有测试用例
- 确认全部通过
- 生成覆盖率报告

### Step 5: 提交验收

运行 `scripts/check-test-coverage/` 校验覆盖率是否达标。

### 覆盖率标准

| 模块类型 | 行覆盖率 | 分支覆盖率 |
|---------|---------|-----------|
| 核心业务逻辑 | ≥ 80% | ≥ 70% |
| 通用工具类 | ≥ 90% | ≥ 80% |
| API 控制器 | ≥ 70% | ≥ 60% |
| 配置/常量 | ≥ 50% | — |
