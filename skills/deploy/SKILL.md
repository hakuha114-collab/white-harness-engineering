<!-- 子资源：由主 SKILL.md 路由引用，不独立注册为技能 -->

# Skill: 部署发布

## 元信息

```yaml
name: deploy
version: 1.0.0
description: 标准化部署发布流程，确保发布安全、可回滚、有监控
trigger:
  - "部署"
  - "发布"
  - "上线"
  - "deploy"
  - "release"
inputs:
  - name: version
    type: string
    required: true
    description: 发布版本号
  - name: changelog
    type: string
    required: true
    description: 变更说明
  - name: environment
    type: enum
    required: true
    options: [staging, production]
    description: 目标环境
outputs:
  - name: deploy_report
    type: html
    description: 部署报告，按主 SKILL.md「报告输出规范」的 HTML 骨架输出
rules:
  - rules/security-rules.md
  - rules/prohibited-actions.md
scripts:
  - scripts/check-security/
```

## 标准执行步骤

### Step 1: 发布前检查

- [ ] 所有测试通过（单元测试 + 集成测试）
- [ ] 代码审查已通过
- [ ] 安全合规检查通过
- [ ] 变更日志已更新
- [ ] 版本号已更新
- [ ] 配置已同步到目标环境
- [ ] 回滚方案已准备

### Step 2: 构建部署包

- 拉取指定版本代码
- 执行构建
- 运行构建后检查
- 生成构建产物校验和

### Step 3: 部署到 Staging

- 部署到预发布环境
- 运行冒烟测试
- 运行回归测试
- 确认功能正常

### Step 4: 部署到 Production

- 灰度发布（先 10% → 50% → 100%）
- 每个阶段观察监控指标
- 发现异常立即回滚

### Step 5: 发布后验证

- [ ] 核心功能可用
- [ ] 监控指标正常
- [ ] 日志无异常错误
- [ ] 性能指标在预期范围

### Step 6: 发布报告

> **按分类模板 `assets/templates/reports/deploy-report.html` 输出的 HTML 文件**（`.html`）。保留以下分区：发布信息、变更内容、部署过程（`<table>` 阶段/时间/状态/备注）、验证结果（冒烟/回归/监控，状态用 .tag 色标）、回滚方案。落盘建议：`reports/deploy-<版本>.html`，并在对话中预览交付。

## ⚠️ 部署红线

- ❌ **禁止** 未经 staging 验证直接部署到生产环境
- ❌ **禁止** 在业务高峰期部署（除非紧急修复）
- ❌ **禁止** 部署后不验证
- ❌ **禁止** 没有回滚方案就部署
