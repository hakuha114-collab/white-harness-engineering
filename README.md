# White Harness Engineering

> Harness Engineering framework for controllable, traceable, evidence-gated AI software delivery.

![version](https://img.shields.io/badge/version-2.0.0-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![clients](https://img.shields.io/badge/clients-Codex%20%7C%20WorkBuddy-purple)

**Current version: v2.0.0.** Version must stay synchronized in `SKILL.md`, `config/harness.yaml`, and `CHANGELOG.md`.

## What Changed in 2.0

White Harness 2.0 upgrades the original Rule / Skill / Agent / Workflow / Script / MCP / Asset framework into an executable Harness Runtime.

The new core is:

```text
Executable Graph + TaskState + Policy + Evidence Gate + Trace/Replay
```

Key guarantees:

- Executable Graph: `runtime/graphs/*.yaml` defines nodes, edges, rollback, checkpoint/resume, and fan-out/fan-in.
- Unified TaskState: `runtime/schema/task_state.schema.json` defines the machine handoff state.
- Feature Memory: `.harness/features/<TASK_ID>/TECH_SPEC.md`, `state.json`, `subtasks.json`, `timeline.ndjson`.
- Evidence Gate: all main gates emit one JSON schema and enforce `No Evidence, No Pass`.
- Clean-context Reviewer: reviewer cannot inherit developer reasoning or chat history.
- Repository Map: `assets/project-wiki/` provides L1/L2/L3 project knowledge plus stale detection.
- Policy YAML: `rules/policies.yaml` is the machine-readable policy source.
- Dynamic Router: trivial / normal / feature / high-risk graphs are selected by task risk and side effects.
- Human Approval Policy: risky side effects such as commit, push, migration, production deploy, deletion, and secret rotation require approval records.

## Repository Layout

```text
white-harness-engineering/
  SKILL.md
  README.md
  CHANGELOG.md
  RELEASE_NOTES_v2.0.0.md
  config/
    harness.yaml
    router.yaml
    gates.yaml
  runtime/
    gates.py
    graph.py
    state.py
    router.py
    policy.py
    trace.py
    graphs/
    schema/
  rules/
    policies.yaml
    coding-standards.md
    security-rules.md
    review-checklist.md
    prohibited-actions.md
  agents/
    pm-dispatcher/
    risk-controller/
    code-reviewer/
    project-recorder/
  workflows/
    executable-graph.md
    full-dev-pipeline.md
    bug-fix-pipeline.md
    code-review-pipeline.md
    hotfix-pipeline.md
  scripts/
    harness_runtime.py
    self-check.py
    check-spec/
    check-design/
    check-risk/
    check-code-style/
    check-security/
    check-review-pass/
    check-test-coverage/
    check-knowledge-stale/
  assets/
    templates/feature-memory/
    project-wiki/
```

## Runtime Quick Start

Route a task:

```bash
python scripts/harness_runtime.py route --task-type feature --risk-level normal --changed-files 8
```

Create feature memory:

```bash
python scripts/harness_runtime.py init --task-id FEAT-001 --goal "Add order export" --workflow feature
```

Inspect graph transition:

```bash
python scripts/harness_runtime.py next --workflow feature --node implement --status PASS
```

Validate state:

```bash
python scripts/harness_runtime.py validate-state .harness/features/FEAT-001/state.json
```

Replay trace:

```bash
python scripts/harness_runtime.py replay .harness/features/FEAT-001/timeline.ndjson
```

## Gate Quick Start

All gates use the same result contract:

| Status | Exit | Meaning |
| --- | ---: | --- |
| PASS | 0 | Passed with durable evidence. |
| FAIL | 1 | Must roll back and fix. |
| WARN | 2 | Can continue only when policy allows warning carry-forward. |
| BLOCK | 3 | Stop for human intervention. |

Examples:

```bash
python scripts/check-spec/check_spec.py SPEC.md --json
python scripts/check-design/check_design.py DESIGN.md --spec SPEC.md --json
python scripts/check-risk/check_risk.py RISK.md --json
python scripts/check-code-style/check_code_style.py . --json
python scripts/check-security/check_security.py . --json
python scripts/check-review-pass/check_review_pass.py review.md --json
python scripts/check-test-coverage/check_test_coverage.py coverage.json --json
python scripts/check-knowledge-stale/check_knowledge_stale.py .harness/wiki-manifest.json --json
```

## Dynamic Graphs

| Graph | Use when |
| --- | --- |
| `trivial` | Low-risk docs, typo, or tiny config changes. |
| `normal` | Ordinary bug fixes and refactors. |
| `feature` | Multi-file feature work requiring TECH_SPEC, subtasks, and fan-out/fan-in verification. |
| `high-risk` | Security, migration, production, destructive, or approval-heavy work. |

Human-readable pipeline docs remain under `workflows/`. Executable routing is defined by `runtime/graphs/*.yaml`.

## Install

Codex user-level skill:

```bash
git clone https://github.com/hakuha114-collab/white-harness-engineering.git \
  ~/.agents/skills/white-harness-engineering
```

WorkBuddy user-level skill:

```bash
git clone https://github.com/hakuha114-collab/white-harness-engineering.git \
  ~/.workbuddy/skills/white-harness-engineering
```

Codex Skills CLI:

```bash
npx skills add hakuha114-collab/white-harness-engineering -a codex
```

## Verification

Run the repository self-check:

```bash
python scripts/self-check.py
```

This compiles the runtime scripts, runs unit tests, and executes sample gate fixtures.

## Docs

- Runtime: `docs/runtime.md`
- Migration: `docs/migration-v2.md`
- Release notes: `RELEASE_NOTES_v2.0.0.md`
- Executable graph: `workflows/executable-graph.md`

## License

MIT
