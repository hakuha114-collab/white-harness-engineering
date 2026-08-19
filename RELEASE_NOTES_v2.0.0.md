# White Harness Engineering v2.0.0

## Summary

v2.0.0 upgrades White Harness Engineering from a document-driven AI engineering framework into an executable Harness Runtime.

The core architecture is now:

```text
Executable Graph + TaskState + Policy YAML + Evidence Gate + Trace/Replay
```

## Major Changes

- Added executable runtime modules under `runtime/`.
- Added graph definitions for `trivial`, `normal`, `feature`, and `high-risk` workflows.
- Added `TaskState` schema and feature-level task memory.
- Added evidence-based gate engine with one result schema and exit-code contract.
- Added real gate wrappers for all main check directories.
- Added clean-context reviewer policy.
- Added machine-readable `rules/policies.yaml`.
- Added Repository Map L1/L2/L3 and knowledge stale detector.
- Added runtime CLI, self-check script, unit tests, fixtures, and migration docs.

## Migration Notes

- `config/harness.yaml` is now machine-readable JSON-compatible YAML.
- Store feature work under `.harness/features/<TASK_ID>/`.
- Store gate JSON outputs under the feature `evidence/` directory.
- Use `scripts/harness_runtime.py route` to select the graph instead of manually choosing one fixed pipeline.
- Keep existing Markdown workflows for human guidance, but use `runtime/graphs/*.yaml` for executable transitions.

## Compatibility

The existing seven-part framework remains:

```text
Rule / Skill / Agent / Workflow / Script / MCP / Asset
```

v2.0.0 adds Runtime, State, Evidence, and Policy execution around that framework without adding unnecessary new agents.

## Verification

Run:

```bash
python scripts/self-check.py
```
