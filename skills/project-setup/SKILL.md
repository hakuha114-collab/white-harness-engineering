# Skill: 项目初始化

## 元信息

```yaml
name: project-setup
version: 1.0.0
description: 标准化新项目初始化流程，确保项目结构、工具链、规范一步到位
trigger:
  - "新项目"
  - "项目初始化"
  - "初始化"
  - "搭建项目"
  - "创建工程"
inputs:
  - name: project_name
    type: string
    required: true
    description: 项目名称
  - name: tech_stack
    type: string
    required: true
    description: 技术栈（如: React+TypeScript+Node.js）
  - name: project_type
    type: enum
    required: true
    options: [web, api, mobile, lib, cli, monorepo]
    description: 项目类型
outputs:
  - name: project_structure
    type: directory
    description: 初始化后的项目目录
  - name: setup_report
    type: markdown
    description: 初始化报告
rules:
  - rules/coding-standards.md
  - rules/security-rules.md
scripts:
  - scripts/check-code-style/
```

## 标准执行步骤

### Step 1: 项目规划

- 确认项目类型和技术栈
- 选择项目模板（从 `assets/templates/` 匹配）
- 确认目录结构

### Step 2: 创建项目骨架

标准项目结构：

```
project-name/
├── .github/              # GitHub 配置
│   └── workflows/        # CI/CD 工作流
├── src/                  # 源代码
│   ├── modules/          # 功能模块
│   ├── shared/           # 共享代码
│   └── index.ts          # 入口文件
├── tests/                # 测试代码
│   ├── unit/             # 单元测试
│   ├── integration/      # 集成测试
│   └── e2e/              # 端到端测试
├── docs/                 # 项目文档
│   ├── architecture.md   # 架构文档
│   └── api.md            # API 文档
├── scripts/              # 工具脚本
├── .gitignore
├── .eslintrc             # 或对应的 Lint 配置
├── .prettierrc           # 格式化配置
├── README.md
├── CHANGELOG.md
├── package.json          # 或 pyproject.toml / go.mod
└── tsconfig.json         # TypeScript 项目
```

### Step 3: 配置工具链

| 工具 | 配置 | 说明 |
|------|------|------|
| Lint | ESLint / Pylint / golangci-lint | 代码风格检查 |
| Format | Prettier / Black | 代码格式化 |
| Test | Jest / Pytest / Go Test | 测试框架 |
| CI | GitHub Actions / GitLab CI | 持续集成 |
| Git Hooks | Husky / pre-commit | 提交前检查 |

### Step 4: 配置 Git

- 初始化 Git 仓库
- 配置 `.gitignore`
- 配置分支保护规则
- 创建初始分支结构（main, develop）

### Step 5: 配置安全

- 配置依赖安全扫描
- 配置密钥管理方案
- 配置代码安全扫描

### Step 6: 编写文档

- README.md（项目说明、快速开始）
- CONTRIBUTING.md（贡献指南）
- CHANGELOG.md（变更日志）

### Step 7: 初始化报告

```markdown
# 项目初始化报告

## 项目信息
- 名称: [项目名]
- 类型: [项目类型]
- 技术栈: [技术栈]

## 目录结构
[树形结构]

## 工具链配置
| 工具 | 配置文件 | 说明 |
|------|---------|------|

## Git 配置
- 仓库: [地址]
- 分支策略: [描述]
- 保护规则: [描述]

## 待办事项
- [ ] 补充环境变量配置
- [ ] 接入 CI/CD
- [ ] 配置监控告警
```
