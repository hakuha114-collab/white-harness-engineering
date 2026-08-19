# code-review-graph 审查图谱对接（含与 CodeGraph 选型路由）

## 对接说明

通过本地**审查知识图谱**（code-review-graph，[@tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph)，Python 包 `code-review-graph`）为 Harness 提供 **diff/PR 级的审查上下文与影响半径**：用 tree-sitter 把仓库建成"实体 + 调用/数据流 + 社区"的多层图（持久化在 `.code-review-graph/`），经 MCP 暴露 ~30 个工具给 Agent，并内置 D3 力导向图可视化（`visualize` 命令）。

定位：**审查图谱（review graph）** 与 CodeGraph 的**代码图（code graph）** 是互补的两张图，不是替代：

- **CodeGraph**：输入是「符号」，回答"这个东西是什么、谁依赖它、改它影响谁"——偏**理解 / 影响面 / 跨文件调用链一致性**。
- **code-review-graph**：输入是「diff / PR」，回答"这次改动该查哪些上下文、波及哪些流程/社区、有哪些大函数/坏味道"——偏**审查对错 / 可视化 / 影响半径**。

两者都可选、都 100% 本地、都不依赖 Git；可并存，互不冲突。

## 能力清单（实测，v2.3.3，MCP `tools/list` 返回 30 个）

| 用途 | MCP 工具（节选） | Harness 用途 |
|------|------------------|--------------|
| 取一次 diff/PR 的审查上下文 | `get_review_context_tool` | Review Pass 直接喂审查背景 |
| 改动的波及半径 | `get_impact_radius_tool` | **Risk Gate 取波及范围证据** |
| 变更影响检测 | `detect_changes_tool` | 提交前 diff 分析 |
| 受影响的业务流程 | `get_affected_flows_tool` / `list_flows_tool` / `get_flow_tool` | Review Pass 验流程是否被破 |
| 受影响的知识社区 | `list_communities_tool` / `get_community_tool` / `get_architecture_overview_tool` | 架构一致性 |
| 语义检索实体 | `semantic_search_nodes_tool` / `query_graph_tool` / `traverse_graph_tool` | SPEC/设计定位 |
| 大函数 / 坏味道 | `find_large_functions_tool` | Review Pass 圈复杂度 |
| 图构建/后处理 | `build_or_update_graph_tool` / `run_postprocess_tool` / `embed_graph_tool` | 首次/增量建索引 |

> 完整 30 工具见 `tools/list`；本表列出与门禁最相关的子集。

## 接入方式

### 1) 环境前置（已在本机修好依赖）

```text
Python 3.10 (miniforge3)
pip install code-review-graph==2.3.3
依赖：mcp>=1.x, fastmcp, anyio>=4.5, typing_extensions, annotated_types, pydantic, pywin32(Windows)
Windows 注意：pywin32 需跑 `pywin32_postinstall.py -install` 并手写 `pywin32.pth`（win32/win32\lib/Pythonwin）才能 import pywintypes
```

### 2) 项目初始化（两端通用，建索引是用户决定）

```bash
cd <your-project>
python -m code_review_graph build      # 生成 .code-review-graph/ 全量图（首次开销高）
# 或增量：python -m code_review_graph update
```

### 3) WorkBuddy（手动，`~/.workbuddy/mcp.json`）

本机已写入 6 个按项目根 `cwd` 区分的实例（与 Codex `config.toml` 对齐）：

```json
{
  "mcpServers": {
    "code-review-graph": {
      "command": "C:/Users/white/miniforge3/python.exe",
      "args": ["-m", "code_review_graph", "serve"],
      "cwd": "E:/code/smarlink-JLHW",
      "type": "stdio"
    }
  }
}
```

其余 5 个实例：`code-review-graph-overseas-fleet` / `-southafrica` / `-ai-bi` / `-intl-ops` / `-intl-fe-southafrica`，`args` 相同，仅 `cwd` 换成各自项目根。选哪个实例由"当前工作目录落在哪个项目"决定（WorkBuddy 按 `cwd` 拉起对应仓库的图谱）。

### 4) 按需裁剪工具

`serve` 支持 `--tools`（`CRG_TOOLS` 环境变量兜底）逗号分隔白名单；未列出则从服务端移除。默认全部 30 个可用，一般无需裁剪。

## 使用前置检测（Preflight，必读）

code-review-graph 是可选增强，"缺失即兜底"不能靠盲目试错。Agent 在调用任何 `code_review_graph_*` 工具前**必须先做两步探测**：

1. **服务是否可用**：MCP 工具 `get_review_context_tool` 能否被调用（`tools/list` 含它）。
   - 不可用 → 不调用本页任何工具，改用 Read / Grep / Glob 取证据，报告显式标注「code-review-graph 未接入，已退回内置工具」。
2. **项目是否索引**：目标项目根（或向上最近一级）是否存在 `.code-review-graph/` 目录（即跑过 `build`）。
   - 未索引 → **不要替用户跑 `build`**（大仓首次建图开销高，且是用户决定）；改用 Read/Grep 或 CodeGraph（若已 init），并提示用户：如需审查图谱的上下文/影响半径证据，请在该项目执行 `python -m code_review_graph build`。

两步都满足才进入上方「能力清单」；任一不满足则走原有 heuristic，门禁不因缺失而失败。

## 选型路由：什么时候用 code-review-graph，什么时候用 CodeGraph

| 你的输入 / 问题 | 用哪个 | 为什么 |
|----------------|--------|--------|
| "帮我审查这个 diff / 这个 PR" | **code-review-graph** | 它吃 diff/PR，直接给审查上下文与影响半径 |
| "这次改动波及哪些流程/社区？" | **code-review-graph** | `get_affected_flows_tool` / `list_communities_tool` |
| "这个函数是不是太大/有坏味道？" | **code-review-graph** | `find_large_functions_tool` |
| "这个符号是谁、谁调用它、改它影响谁？" | **CodeGraph** | `explore` / `callers` / `callees` / `impact` 专为符号级理解 |
| "Review Pass 验调用链一致性" | **CodeGraph** | `callers`/`callees` 验 diff 的调用边是否符合意图 |
| "Risk Gate 取影响面（文件/测试列表）" | **CodeGraph** 优先，`code-review-graph` 补充 | 两者都行；CodeGraph 的 `impact` 含受影响测试清单，code-review-graph 的 `get_impact_radius_tool` 给波及半径 |
| "SPEC/设计 阶段定位相关模块" | **CodeGraph**（`explore`）或 code-review-graph（`semantic_search_nodes_tool`） | 二选一皆可，按已接入情况 |

**一句话**：输入是「符号」→ CodeGraph；输入是「diff/PR」→ code-review-graph。

## 与 Harness 门禁的对应

| Harness 门禁 | 优先工具 | 参考文档 |
|--------------|----------|----------|
| Review Pass（审查门禁） | `get_review_context_tool` / `get_impact_radius_tool` / `get_affected_flows_tool`；调用链一致性仍用 CodeGraph `callers`/`callees` | `agents/code-reviewer/AGENT.md`、`mcp/codegraph.md` |
| Risk Gate（风险门禁） | `get_impact_radius_tool`（波及半径）+ CodeGraph `impact`（影响面/测试清单） | `agents/risk-controller/AGENT.md`、`mcp/codegraph.md` |
| SPEC / 设计 | `semantic_search_nodes_tool` / `query_graph_tool` | `skills/create-spec/`、`agents/solution-designer/` |

> 接入为**可选增强**：未安装 code-review-graph 时，门禁按原有 heuristic 执行，不因缺失而失败。
