# CodeGraph 代码智能对接

## 对接说明

通过本地代码知识图谱（CodeGraph，[@colbymchenry/codegraph](https://www.npmjs.com/package/@colbymchenry/codegraph)）为 Harness 提供**结构级代码理解**能力：用 tree-sitter 把仓库抽成"符号 + 调用边 + 依赖"的图（跨文件、含动态分派），经 MCP 暴露给 Agent。

定位：**代码图（code graph）** ≠ Harness 的 `runtime/graphs`（工作流执行图）。两者维度不同，可并存，不冲突。CodeGraph 补的是"影响面 / 调用链"这类证据，让风控门禁与审查门禁从"口头声明"变成"可查询事实"。

## 与 code-review-graph 的分工（一文读懂选哪个）

另有一张可选图谱 **code-review-graph**（`mcp/code-review-graph.md`），两者互补：

- 输入是**「符号」**（这个东西是什么 / 谁依赖它 / 改它影响谁）→ 用 **CodeGraph**（理解 / 影响面 / 调用链一致性）。
- 输入是**「diff / PR」**（这次改动该查哪些上下文 / 波及哪些流程社区 / 有无大函数坏味道）→ 用 **code-review-graph**（审查对错 / 可视化 / 影响半径）。

一句话：**输入是符号用 CodeGraph，输入是 diff/PR 用 code-review-graph。** 完整选型路由表见 `mcp/code-review-graph.md`。

## 能力清单

| 能力 | MCP 工具 | CLI 等价 | Harness 用途 |
|------|----------|----------|--------------|
| 相关代码 + 调用路径（一句话问） | `codegraph_explore` | `codegraph explore "<query>"` | SPEC / 设计阶段秒定位相关模块 |
| 谁调用了它 | `codegraph_callers` | `codegraph callers <symbol>` | Review Pass 验调用链上游 |
| 它调用了谁 | `codegraph_callees` | `codegraph callees <symbol>` | Review Pass 验调用链下游 |
| 改它的影响面 | `codegraph_impact` | `codegraph impact <symbol>` | **Risk Gate 取波及范围证据（含受影响文件/测试列表）** |

> 注：v1.5.0 实测仅存在上述 4 个 MCP 工具（`explore/callers/callees/impact`）。早期文档提到的 `codegraph_affected`、`codegraph_query` 在本版本未注册，勿写入 `CODEGRAPH_MCP_TOOLS`。

> 默认 MCP 仅暴露 `codegraph_explore`。其余工具需经环境变量 `CODEGRAPH_MCP_TOOLS` 显式启用（见下）。

## 接入方式

### 1) 项目初始化（两端通用）

```bash
cd <your-project>
codegraph init          # 生成 .codegraph/ 并构建全量图，遵守 .gitignore
```

文件监听默认 2s 防抖，改动自动增量同步，索引永不 stale。

### 2) Codex（自动）

```bash
codegraph install       # 自动探测并注入 MCP 到 Codex CLI
```

### 3) WorkBuddy（手动，codegraph install 不探测 WorkBuddy）

在 `~/.workbuddy/mcp.json`（**注意不是 `.mcp.json`**）新增一条 `mcpServers.codegraph`，命令与 `codegraph install` 为 Codex 自动写入的格式一致：

```json
{
  "mcpServers": {
    "codegraph": {
      "command": "codegraph",
      "args": ["serve", "--mcp"],
      "env": {
        "CODEGRAPH_MCP_TOOLS": "explore,callers,callees,impact"
      }
    }
  }
}
```

> 关键：`codegraph` 的 MCP 服务是隐藏子命令 `serve --mcp`（裸 `codegraph` 只会打印 help 并退出，MCP 起不来），故 `args` 必须为 `["serve", "--mcp"]`。WorkBuddy 为避开 PATH 依赖，本机实际生效配置用的是绝对路径 `C:/Users/white/AppData/Local/codegraph/current/bin/codegraph.cmd`（命令不同，args 相同）。

## 使用前置检测（Preflight，必读）

CodeGraph 是可选增强，但"缺失即兜底"不能靠盲目试错。Agent 在调用任何 `codegraph_*` 工具前，**必须先做两步探测**：

1. **服务是否可用**：MCP 工具 `codegraph_explore` 能否被调用（或终端 `codegraph --version` 退出码为 0）。
   - 不可用 → 不调用本页任何工具，改用 Read / Grep / Glob 取证据，并在报告里显式标注「CodeGraph 未接入，已退回内置工具」。
2. **项目是否初始化**：目标项目根（或向上最近一级）是否存在 `.codegraph/` 目录（即跑过 `codegraph init`）。
   - 未初始化 → **不要替用户跑 `codegraph init`**（建索引是用户决定，且大仓首次索引开销高）；改用内置工具，并提示用户：如需 CodeGraph 的影响面 / 调用链证据，请在该项目执行 `codegraph init`。

两步都满足才进入下方「能力清单」；任一不满足则走原有 heuristic，门禁不因缺失而失败。

## 环境变量 / 配置

| 变量 | 作用 | 默认 |
|------|------|------|
| `CODEGRAPH_MCP_TOOLS` | 启用额外 MCP 工具，逗号分隔 | `explore`（仅默认暴露 explore） |
| `CODEGRAPH_WATCH_DEBOUNCE_MS` | 监听防抖窗口 | `2000`（限 100ms–60s） |
| `CODEGRAPH_NO_DAEMON` | 禁用共享后台服务（沙箱/脚本场景） | 未设 |
| `CODEGRAPH_TELEMETRY` / `DO_NOT_TRACK` | 关闭遥测 | `0` / `1` 关闭 |

可选项目配置 `codegraph.json`（项目根）：`exclude` / `include` / `extensions`，零配置即可用。

## 隐私与依赖

- **100% 本地**：后端为本地 SQLite（`.codegraph/codegraph.db`，FTS5，WAL），无 API Key、无外部服务、数据不出机。
- **系统**：Windows / macOS / Linux（x64、arm64）。无需 Node（bundle 安装器自带 Rust 运行时）；`npm i -g` 方式任意 Node 即可；仅 Library API 需 Node 22.5+。
- **不依赖 Git**：无 git 时直接读 `.gitignore` 文件。
- **遥测**：默认收集匿名使用统计（工具/语言用量），**不含**代码、路径、符号名、查询、IP；可 `codegraph telemetry off` 关闭。
- **语言**：20+ 语言（TS/JS/Vue/Svelte/Python/Go/Rust/Java/C#/C/C++/Swift/Kotlin/Scala/PHP/Ruby 等），涵盖主流技术栈。

## 与 Harness 门禁的对应

| Harness 门禁 | 优先使用的 CodeGraph 能力 | 参考文档 |
|--------------|---------------------------|----------|
| Risk Gate（风险门禁） | `codegraph impact` 取影响面（含受影响文件/测试列表） | `agents/risk-controller/AGENT.md` |
| Review Pass（审查门禁） | `codegraph callers` / `codegraph callees` 验调用链一致性 | `agents/code-reviewer/AGENT.md` |
| SPEC / 设计 | `codegraph explore` 定位相关模块 | `skills/create-spec/`、`agents/solution-designer/` |

> 接入为**可选增强**：未安装 CodeGraph 时，门禁按原有 heuristic（人工 grep / 仓库图）执行，不因缺失而失败。
