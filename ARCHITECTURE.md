# Architecture

White Harness Engineering v2.0.0 is an executable AI engineering runtime built around the existing Harness assets.

## Layers

```text
User Intent
  -> PM Dispatcher / Dynamic Router
  -> Executable Graph
  -> Agent Node or Gate Node
  -> TaskState
  -> Evidence
  -> Policy Decision
  -> Trace / Replay
```

## Core Runtime Components

| Component | Path | Purpose |
| --- | --- | --- |
| Router | `runtime/router.py`, `config/router.yaml` | Select `trivial`, `normal`, `feature`, or `high-risk`. |
| Graph | `runtime/graph.py`, `runtime/graphs/*.yaml` | Define nodes, edges, rollback, checkpoint, fan-out/fan-in. |
| State | `runtime/state.py`, `runtime/schema/task_state.schema.json` | Persist cross-agent machine state. |
| Policy | `runtime/policy.py`, `rules/policies.yaml` | Evaluate rule levels and side-effect approvals. |
| Gate | `runtime/gates.py`, `scripts/check-*/` | Produce evidence-based PASS/WARN/FAIL/BLOCK results. |
| Trace | `runtime/trace.py` | Append and replay `timeline.ndjson`. |

## Graph Model

Each graph is `G = (V, E, S, P)`:

- `V`: agent, gate, merge, checkpoint, or human approval nodes.
- `E`: conditional transitions by gate status.
- `S`: `TaskState` stored in `.harness/features/<TASK_ID>/state.json`.
- `P`: policy rules from `rules/policies.yaml`.

## State Model

`TaskState` is the only machine handoff contract. It stores:

- task id and goal
- selected workflow and current node
- artifacts and evidence
- subtasks
- rollback count
- human approvals
- budget
- audit pointers

## Evidence Model

Gates cannot return `PASS` without durable evidence. Evidence can be a spec, design doc, report, diff, coverage file, scan output, or another stored artifact with hash metadata.

## Clean-context Review

The reviewer is isolated from Developer reasoning and chat history. It receives only:

- spec and acceptance criteria
- diff and relevant code
- test and gate evidence
- rules and policies
- repository map entries

## Compatibility

The original Rule / Skill / Agent / Workflow / Script / MCP / Asset framework remains intact. v2.0.0 adds Runtime, State, Evidence, and Policy execution around it.
