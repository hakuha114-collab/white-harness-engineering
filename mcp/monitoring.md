# 监控告警对接

## 对接说明

通过 MCP 协议打通监控系统，实现运行指标获取、告警通知、性能数据采集。

## 能力清单

| 能力 | 方向 | 说明 |
|------|------|------|
| 查询指标 | Agent → 监控 | 获取运行时指标 |
| 查询告警 | Agent → 监控 | 获取当前告警列表 |
| 确认告警 | Agent → 监控 | 确认已知告警 |
| 创建告警规则 | Agent → 监控 | 为新服务创建监控规则 |
| 告警通知 | 监控 → Agent | 实时告警推送 |
| 性能报告 | 监控 → Agent | 定时性能报告 |

## 接口定义

### 查询指标

```yaml
endpoint: monitoring.queryMetrics
method: POST
params:
  - name: service
    type: string
    required: true
  - name: metrics
    type: string[]
    required: true
    examples: ["cpu_usage", "memory_usage", "request_latency_p99", "error_rate"]
  - name: time_range
    type: object
    properties:
      start: string  # ISO 8601
      end: string    # ISO 8601
  - name: granularity
    type: enum
    options: [1m, 5m, 15m, 1h, 1d]
response:
  metrics:
    - name: string
      values:
        - timestamp: string
          value: number
```

### 查询告警

```yaml
endpoint: monitoring.queryAlerts
method: GET
params:
  - name: service
    type: string
  - name: severity
    type: enum
    options: [critical, warning, info]
  - name: status
    type: enum
    options: [firing, resolved]
response:
  alerts:
    - id: string
      name: string
      severity: string
      status: string
      description: string
      started_at: string
```

## 关键监控指标

| 指标 | 告警阈值 | 说明 |
|------|---------|------|
| CPU 使用率 | > 80% 持续 5min | 服务过载 |
| 内存使用率 | > 85% | 内存泄漏风险 |
| 请求延迟 P99 | > 1s | 性能劣化 |
| 错误率 | > 1% | 服务异常 |
| 磁盘使用率 | > 90% | 存储不足 |
