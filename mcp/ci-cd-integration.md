# CI/CD 流水线对接

## 对接说明

通过 MCP 协议打通 CI/CD 系统，实现自动构建、部署、流水线状态的双向同步。

## 能力清单

| 能力 | 方向 | 说明 |
|------|------|------|
| 触发构建 | Agent → CI | 提交代码后自动触发 |
| 查询构建状态 | Agent → CI | 查询流水线运行状态 |
| 获取构建日志 | Agent → CI | 获取构建日志用于排查 |
| 取消构建 | Agent → CI | 取消正在运行的流水线 |
| 触发部署 | Agent → CD | 审批通过后触发部署 |
| 查询部署状态 | Agent → CD | 查询部署进度 |
| 回滚部署 | Agent → CD | 部署异常时回滚 |
| 构建状态通知 | CI → Agent | 构建完成/失败通知 |

## 接口定义

### 触发构建

```yaml
endpoint: ci.triggerBuild
method: POST
params:
  - name: branch
    type: string
    required: true
  - name: commit_sha
    type: string
    required: true
  - name: pipeline
    type: string
    default: "default"
response:
  build_id: string
  build_url: string
```

### 查询构建状态

```yaml
endpoint: ci.getBuildStatus
method: GET
params:
  - name: build_id
    type: string
    required: true
response:
  status: enum  # running | success | failed | cancelled
  stages:
    - name: string
      status: enum
      duration: int
  artifacts:
    - name: string
      url: string
```

### 触发部署

```yaml
endpoint: cd.triggerDeploy
method: POST
params:
  - name: build_id
    type: string
    required: true
  - name: environment
    type: enum
    options: [staging, production]
    required: true
  - name: strategy
    type: enum
    options: [rolling, blue_green, canary]
    default: "rolling"
response:
  deploy_id: string
  deploy_url: string
```

## CI 流水线定义

```yaml
pipeline:
  stages:
    - name: lint
      script: npm run lint
      timeout: 5m
      
    - name: test
      script: npm run test:coverage
      timeout: 15m
      
    - name: security
      script: npm run security:check
      timeout: 10m
      
    - name: build
      script: npm run build
      timeout: 10m
      
    - name: deploy-staging
      script: npm run deploy:staging
      timeout: 10m
      when: branch == "develop"
      
    - name: deploy-production
      script: npm run deploy:production
      timeout: 15m
      when: branch == "main"
      approval_required: true
```
