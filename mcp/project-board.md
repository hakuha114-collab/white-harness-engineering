# 项目看板对接

## 对接说明

通过 MCP 协议打通项目看板系统（Jira/飞书/Tapd 等），实现任务状态、进度追踪的双向同步。

## 能力清单

| 能力 | 方向 | 说明 |
|------|------|------|
| 创建任务 | Agent → 看板 | 自动创建开发任务 |
| 更新任务状态 | Agent ↔ 看板 | 同步任务进度 |
| 查询任务 | Agent → 看板 | 查询任务详情和列表 |
| 添加评论 | Agent → 看板 | 自动添加进展评论 |
| 关联代码 | Agent → 看板 | 关联 PR/Commit 到任务 |
| 状态变更通知 | 看板 → Agent | 任务状态变更通知 |

## 接口定义

### 创建任务

```yaml
endpoint: board.createTask
method: POST
params:
  - name: title
    type: string
    required: true
  - name: description
    type: string
  - name: type
    type: enum
    options: [story, bug, task, subtask]
  - name: priority
    type: enum
    options: [P0, P1, P2, P3]
  - name: assignee
    type: string
  - name: labels
    type: string[]
response:
  task_id: string
  task_url: string
```

### 更新任务状态

```yaml
endpoint: board.updateTaskStatus
method: PUT
params:
  - name: task_id
    type: string
    required: true
  - name: status
    type: enum
    options: [todo, in_progress, in_review, done, blocked]
  - name: comment
    type: string
response:
  updated: boolean
```

## 状态映射

| Harness 状态 | 看板状态 |
|-------------|---------|
| 任务创建 | todo |
| Agent 开始执行 | in_progress |
| 代码审查中 | in_review |
| 测试验收中 | in_review |
| 交付完成 | done |
| 阻塞/回退 | blocked |
