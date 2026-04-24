# 知识库

> 团队技术知识沉淀，支持 Agent 检索和复用

## 知识分类

### 编程原则（核心）

- **[Karpathy 编程四原则](./principles/karpathy-guidelines.md)** — 先思考再编码、简洁优先、精准修改、目标驱动执行
  - 来源：[andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)（80.8k Stars）
  - 适用：所有 AI 辅助开发场景
  - 关联规则：`rules/karpathy-guidelines.md`

### 架构设计

- [微服务架构最佳实践](./architecture/microservice.md)
- [前端工程化方案](./architecture/frontend.md)
- [数据库设计规范](./architecture/database.md)

### 开发规范

- [API 设计规范](./dev/api-design.md)
- [错误处理规范](./dev/error-handling.md)
- [日志规范](./dev/logging.md)
- [配置管理规范](./dev/configuration.md)

### 技术选型

- [前端框架选型指南](./tech-stack/frontend.md)
- [后端框架选型指南](./tech-stack/backend.md)
- [数据库选型指南](./tech-stack/database.md)
- [消息队列选型指南](./tech-stack/mq.md)

### 最佳实践

- [代码审查最佳实践](./best-practices/code-review.md)
- [测试策略最佳实践](./best-practices/testing.md)
- [CI/CD 最佳实践](./best-practices/ci-cd.md)
- [安全开发最佳实践](./best-practices/security.md)

## 使用方式

1. Agent 在执行任务前，检索知识库获取相关规范和最佳实践
2. 审查 Agent 发现好的做法时，归入知识库
3. 定期整理和更新知识库内容

## 贡献方式

- 代码审查中发现好的实践 → 提交到 `best-practices/`
- 新技术选型决策 → 记录到 `tech-stack/`
- 架构设计评审 → 沉淀到 `architecture/`
