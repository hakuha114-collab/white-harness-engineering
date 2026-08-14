# Usage

## 1. Route The Task

```bash
python scripts/harness_runtime.py route --task-type feature --risk-level normal --changed-files 8
```

Use the result to select one graph:

- `trivial`
- `normal`
- `feature`
- `high-risk`

## 2. Create Task Memory

For feature and high-risk work:

```bash
python scripts/harness_runtime.py init --task-id FEAT-001 --goal "Add order export" --workflow feature
```

This creates:

```text
.harness/features/FEAT-001/
  TECH_SPEC.md
  state.json
  subtasks.json
  timeline.ndjson
  evidence/
  reports/
  checkpoints/
```

## 3. Run Gates

Store JSON evidence under the feature directory:

```bash
python scripts/check-spec/check_spec.py SPEC.md \
  --json --output .harness/features/FEAT-001/evidence/spec.json
```

```bash
python scripts/check-security/check_security.py . \
  --json --output .harness/features/FEAT-001/evidence/security.json
```

## 4. Follow Exit Codes

| Status | Exit | Action |
| --- | ---: | --- |
| PASS | 0 | Continue to next graph node. |
| FAIL | 1 | Roll back to mapped node and fix. |
| WARN | 2 | Continue only if policy allows. |
| BLOCK | 3 | Stop for human approval. |

## 5. Review In Clean Context

The reviewer must not read Developer reasoning or chat history. Provide only:

- SPEC / TECH_SPEC
- diff and relevant code
- tests and evidence
- rules and policies
- repository map entries

## 6. Replay Or Resume

```bash
python scripts/harness_runtime.py validate-state .harness/features/FEAT-001/state.json
python scripts/harness_runtime.py replay .harness/features/FEAT-001/timeline.ndjson
```

Resume from `TECH_SPEC.md`, `state.json`, `subtasks.json`, and evidence, not from chat history alone.

## 7. Verify The Framework

```bash
python scripts/self-check.py
```
