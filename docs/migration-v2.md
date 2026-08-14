# Migration to v2.0.0

## What Changed

- `config/harness.yaml` is now machine-readable JSON-compatible YAML.
- `rules/policies.yaml` is the machine-readable policy source.
- `runtime/` contains executable graph, state, policy, trace, router, and gate code.
- Main gate directories now contain real Python wrappers.
- Feature work now persists state under `.harness/features/<TASK_ID>/`.
- Repository knowledge is organized as L1/L2/L3 under `assets/project-wiki/`.

## Compatibility

The existing Rule, Skill, Agent, Workflow, Script, MCP, and Asset layout remains intact. Markdown workflows remain useful for human-readable guidance, but executable routing now comes from `runtime/graphs/*.yaml`.

## Required Team Change

For feature and high-risk work, create task memory first:

```bash
python scripts/harness_runtime.py init --task-id FEAT-001 --goal "Describe goal" --workflow feature
```

For gate results, use JSON output and store it under the feature evidence directory:

```bash
python scripts/check-security/check_security.py . --json --output .harness/features/FEAT-001/evidence/security.json
```
