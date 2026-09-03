# Git 影响面与拓扑工作流（git-impact-topology）

> 一键串联：Git 拉取后「变更检测 → 影响半径 → 受影响流程 → 拓扑图」

## 红线（必读）

本 workflow **不执行任何 git 命令**（不 pull / 不 diff / 不 commit / 不 push）。
- pull 由用户在其开发环境完成（白波本地红线：绝不在本机做 git 操作）。
- 检测基于「用户提供的 pull 前基准 SHA（BASE）」对比当前 working tree。
- 若用户无法提供 BASE，则默认对比 `HEAD` 与 working tree，并在报告中显式标注「未提供 BASE，使用 HEAD vs working tree」。

## 适用场景

- 用户说："用 white-harness-engineering 跑 git 影响拓扑" / "git-impact-topology" / "拉取后影响范围" / "生成变更拓扑图"。
- 已在本地 `git pull` 到最新，想知道：这次改动涉及哪些部分、波及哪些范围、影响的拓扑长什么样。

## 流程定义

```yaml
workflow:
  name: git-impact-topology
  version: 1.0.0
  description: Git 拉取后一键串联变更检测→影响半径→受影响流程→拓扑图
  agents:
    - risk-controller
    - code-reviewer
  mcp:
    - code-review-graph   # 已接入：detect_changes_tool / get_impact_radius_tool / get_affected_flows_tool / visualize
```

## 流程图

```text
[用户在外部 pull 到最新, 记录 BASE = pull 前 commit SHA]
        │
        ▼
[Preflight] code-review-graph 服务可用?  项目已 build(.code-review-graph/)?
        │  ├─ 任一否 → 兜底 Read/Grep/Glob + 提示用户 build
        ▼  │
[变更检测] detect_changes_tool(base=BASE) ──▶ 本次 diff 的实体/文件清单
        │
        ▼
[影响半径] get_impact_radius_tool ──▶ 波及的实体/社区半径
        │
        ▼
[受影响流程] get_affected_flows_tool ──▶ 被破坏风险最高的业务流程
        │
        ▼
[拓扑图] visualize --mode full --serve ──▶ 浏览器打开 D3 力导向图
        │
        ▼
[产出] 影响面摘要 + 拓扑图链接 + 高危点清单 (No Evidence, No Pass)
```

## 步骤

### 0) Preflight（必做，缺失即兜底）

1. **服务可用**：MCP `tools/list` 是否含 `get_review_context_tool`（code-review-graph 实例已按当前 `cwd` 拉起）。
   - 否 → 不调用本页任何 `code_review_graph_*` 工具，改用 Read / Grep / Glob 取证据，报告标注「code-review-graph 未接入，已退回内置工具」。
2. **项目已索引**：当前项目根（或向上最近一级）是否存在 `.code-review-graph/` 目录（即跑过 `build`）。
   - 否 → **不要替用户跑 `build`**（大仓首次建图开销高，且是用户决定）；改用 Read/Grep 或 CodeGraph（若已 init），并提示用户：如需审查图谱的上下文/影响半径证据，请在该项目执行 `python -m code_review_graph build` 后再来。

两步都满足才进入下方步骤；任一不满足则走原有 heuristic，门禁不因缺失而失败。

### 1) 变更检测（detect_changes_tool）

- 输入：BASE（pull 前 commit SHA / 分支 / 标签；缺省对比 `HEAD` vs working tree）。
- 输出：本次变更涉及的实体（函数/类/方法）、改动文件清单、增删行概要。
- 工具参数键名以 MCP `tools/list` 实际 schema 为准（常见为 `base` / `revision`），不要臆测。

### 2) 影响半径（get_impact_radius_tool）

- 输入：步骤 1 的变更实体。
- 输出：波及半径（N 跳内的依赖者、受影响知识社区）。
- 用途：作为 **Risk Gate 的波及范围证据**。

### 3) 受影响流程（get_affected_flows_tool）

- 输出：可能被破坏的业务流程（flow）清单 + 风险排序。
- 用途：作为 **Review Pass 的「流程是否被破」证据**。

### 4) 拓扑图（visualize）

- 命令：`python -m code_review_graph visualize --mode full --serve`（或 MCP 等价工具），生成 D3 力导向图并在浏览器打开。
- 该图即用户要的「影响拓扑图」：节点 = 实体，边 = 调用/数据流，颜色 = 社区归属。

### 5) 产出

- **影响面摘要**（markdown）：变更实体数 / 波及半径 / 高危流程 Top N。
- **拓扑图链接**：local server 或导出 HTML。
- **高危点清单**：大函数、跨社区耦合、被破坏风险高的流程 → 交给 Risk Gate / Review Pass 处置。
- 门禁原则：**No Evidence, No Pass**——缺拓扑/影响半径证据则标注 BLOCK 并交人工。

## 双端触发

- **WorkBuddy**：已接入 6 个按 `cwd` 区分的 `code-review-graph-*` MCP 实例（含 `-ai-bi` / `-overseas-fleet` / `-southafrica` / `-intl-ops` / `-intl-fe-southafrica` 等）。按当前工作目录自动选对应仓库实例。
- **Codex**：`config.toml` 镜像同 6 实例。说「git-impact-topology」即路由到本 workflow。

## 与门禁对应

| Harness 门禁 | 本 workflow 提供 |
|--------------|------------------|
| Risk Gate（风险门禁） | `get_impact_radius_tool` 波及半径 + 高危流程清单 |
| Review Pass（审查门禁） | `get_affected_flows_tool` 流程破坏证据 + `visualize` 拓扑图 |

> 可选增强：code-review-graph 未接入时，门禁按原有 heuristic（Read/Grep/CodeGraph）执行，不因缺失而失败。详见 `mcp/code-review-graph.md` 的 Preflight 与选型路由。
