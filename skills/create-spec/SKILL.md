# Skill: 创建 SPEC 文档

## 元信息

```yaml
name: create-spec
version: 1.0.0
description: 将模糊业务诉求转化为结构化、可落地、可量化的标准技术 SPEC 文档
trigger:
  - "新需求"
  - "需求分析"
  - "写 SPEC"
  - "需求文档"
  - "产品需求"
inputs:
  - name: requirement
    type: string
    required: true
    description: 业务方的原始诉求描述
  - name: context
    type: object
    required: false
    description: 补充上下文（业务背景、技术约束等）
outputs:
  - name: spec_doc
    type: markdown
    path: assets/templates/spec-template.md
    description: 结构化 SPEC 文档
rules:
  - rules/coding-standards.md
  - rules/security-rules.md
scripts:
  - scripts/check-spec/
```

## 标准执行步骤

### Step 1: 需求理解

- 仔细阅读原始诉求，识别核心业务目标
- 标记模糊、有歧义的表述
- 列出需要进一步确认的问题清单

### Step 2: 需求拆解

- 将大需求拆解为独立的功能模块
- 识别功能依赖关系
- 标注优先级（P0/P1/P2）

### Step 3: 结构化文档输出

按以下模板输出 SPEC 文档：

```markdown
# [需求名称] - 设计规格文档

## 1. 需求概述
### 1.1 业务背景
### 1.2 核心目标
### 1.3 成功指标（可量化）

## 2. 功能规格
### 2.1 功能列表
| 功能 | 描述 | 优先级 | 验收标准 |
### 2.2 用户故事
### 2.3 业务流程图

## 3. 非功能规格
### 3.1 性能要求
### 3.2 安全要求
### 3.3 兼容性要求

## 4. 技术约束
### 4.1 技术栈
### 4.2 依赖服务
### 4.3 环境要求

## 5. 验收标准
### 5.1 功能验收
### 5.2 性能验收
### 5.3 安全验收

## 6. 风险与假设
### 6.1 已知风险
### 6.2 前置假设

## 7. 里程碑
| 阶段 | 内容 | 预期时间 |
```

### Step 4: 自检

- [ ] 所有功能点都有对应的验收标准
- [ ] 成功指标可量化、可验证
- [ ] 无歧义表述
- [ ] 风险和假设已明确标注

### Step 5: 提交验收

运行 `scripts/check-spec/` 进行 SPEC 完整性校验，通过后移交方案设计 Agent。
