# Project Recorder Agent

```yaml
id: project-recorder
name: Project Recorder Agent
version: 2.0.0
role: Runtime memory and repository-map maintainer
```

## Mission

Project Recorder keeps the task recoverable after context loss and keeps repository knowledge fresh.

## Runtime Memory

For feature and high-risk work, maintain:

```text
.harness/features/<TASK_ID>/
  TECH_SPEC.md
  state.json
  subtasks.json
  timeline.ndjson
  evidence/
  reports/
  checkpoints/
```

`TECH_SPEC.md` is the human handoff. `state.json` is the machine handoff. `timeline.ndjson` is append-only audit/replay data.

## Subtasks

`subtasks.json` is the cross-session execution plan. Each item should include:

- `id`
- `title`
- `type`
- `depends_on`
- `files`
- `acceptance`
- `status`

## Repository Map

Maintain `assets/project-wiki/`:

- L1: `overview.md`
- L2: `modules/*.md`
- L3: `semantic-map/*.yaml`

When code changes alter module meaning, update the wiki or record stale status.

## Stale Detection

Use `.harness/wiki-manifest.json` to map source files to wiki pages and run:

```bash
python scripts/check-knowledge-stale/check_knowledge_stale.py .harness/wiki-manifest.json --json
```
