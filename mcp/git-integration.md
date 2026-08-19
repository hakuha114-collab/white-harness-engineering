# Git 仓库对接

## 对接说明

通过 MCP 协议打通 Git 代码仓库，实现代码托管、PR 管理、分支策略的双向同步。

## 能力清单

| 能力 | 方向 | 说明 |
|------|------|------|
| 创建分支 | Agent → Git | 按分支策略创建功能分支 |
| 提交代码 | Agent → Git | 提交代码变更 |
| 创建 PR | Agent → Git | 创建 Pull Request |
| Review PR | Agent ↔ Git | 审查 PR，提交 Review 意见 |
| 合并代码 | Agent → Git | Review 通过后合并 |
| 获取变更 | Git → Agent | 监听代码变更事件 |
| 获取分支列表 | Git → Agent | 查询分支信息 |
| 获取 Commit 历史 | Git → Agent | 查询提交历史 |

## 接口定义

### 创建分支

```yaml
endpoint: git.createBranch
method: POST
params:
  - name: branch_name
    type: string
    required: true
    pattern: "^(feature|bugfix|hotfix|release)/.+"
  - name: base_branch
    type: string
    default: "develop"
response:
  branch_url: string
```

### 创建 PR

```yaml
endpoint: git.createPullRequest
method: POST
params:
  - name: title
    type: string
    required: true
  - name: source_branch
    type: string
    required: true
  - name: target_branch
    type: string
    default: "develop"
  - name: description
    type: string
  - name: reviewers
    type: string[]
response:
  pr_url: string
  pr_number: int
```

### 提交 Review

```yaml
endpoint: git.submitReview
method: POST
params:
  - name: pr_number
    type: int
    required: true
  - name: body
    type: string
    required: true
  - name: event
    type: enum
    options: [APPROVE, REQUEST_CHANGES, COMMENT]
response:
  review_id: string
```

## 分支策略

```
main (生产)
  │
  ├── develop (开发)
  │     │
  │     ├── feature/xxx (功能分支)
  │     ├── bugfix/xxx (修复分支)
  │     └── refactor/xxx (重构分支)
  │
  └── hotfix/xxx (紧急修复，从 main 拉取)
```

## 事件监听

```yaml
events:
  - name: push
    description: 代码推送事件
    trigger: 任何分支有新提交
    
  - name: pull_request
    description: PR 事件
    trigger: PR 创建/更新/合并
    
  - name: review
    description: Review 事件
    trigger: Review 提交/更新
```
