# Executable Graph Runtime

White Harness 2.0 keeps the existing Markdown pipelines as human guidance, but runtime execution is defined by machine-readable graph files:

```text
runtime/graphs/
  trivial.yaml
  normal.yaml
  feature.yaml
  high-risk.yaml
```

Each graph is `G = (V, E, S, P)`:

- `V` Node: agent, gate, checkpoint, fan-in, or human approval node.
- `E` Edge: status-based transitions for `PASS/WARN/FAIL/BLOCK`.
- `S` State: `TaskState` in `.harness/features/<TASK_ID>/state.json`.
- `P` Policy: `rules/policies.yaml` and side-effect approval rules.

## Dynamic Routing

```bash
python scripts/harness_runtime.py route --task-type feature --risk-level normal --changed-files 8
```

Routing chooses:

| Workflow | Use when |
| --- | --- |
| `trivial` | Low-risk docs, typo, tiny config changes. |
| `normal` | Ordinary bug fixes and refactors. |
| `feature` | Multi-file feature work needing TECH_SPEC, subtasks, and fan-out/fan-in verification. |
| `high-risk` | Security, migration, production, destructive, or approval-heavy work. |

## Fan-out / Fan-in

Feature and high-risk graphs fan out after implementation:

```text
implement
  -> style_gate
  -> security_gate
  -> unit_or_coverage_gate
  -> verify/review
```

Each branch writes gate evidence. The graph may only advance when required evidence exists.

## Rollback

`FAIL` follows the edge mapping back to the responsible node. If `rollback_count` exceeds `budget.max_rollbacks`, the runtime sets status to `BLOCKED` and moves to human approval.

## Checkpoint / Resume

Create checkpoints before risky transitions:

```bash
python scripts/harness_runtime.py checkpoint .harness/features/FEAT-001/state.json
```

Resume by reading:

```text
TECH_SPEC.md
state.json
subtasks.json
timeline.ndjson
evidence/
```

Do not resume from chat history alone.
