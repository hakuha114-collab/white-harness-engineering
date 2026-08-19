# White Harness 2.0 Runtime

White Harness 2.0 upgrades the repository from a prompt-and-document framework to an executable runtime:

- Executable Graph: `runtime/graphs/*.yaml` defines Node, Edge, State, and Policy flow.
- TaskState: `runtime/schema/task_state.schema.json` defines the durable handoff object.
- Feature Memory: `.harness/features/<TASK_ID>/TECH_SPEC.md`, `state.json`, `subtasks.json`, `timeline.ndjson`.
- Evidence Gate: all gate scripts emit one JSON result schema and enforce `No Evidence, No Pass`.
- Clean Review: reviewer input is limited to spec, diff, tests, evidence, rules, and policies.
- Trace/Replay: `timeline.ndjson` is append-only and replayable by `scripts/harness_runtime.py replay`.

## Runtime CLI

```bash
python scripts/harness_runtime.py route --task-type feature --risk-level normal --changed-files 8
python scripts/harness_runtime.py init --task-id FEAT-001 --goal "Add export" --workflow feature
python scripts/harness_runtime.py next --workflow feature --node implement --status PASS
python scripts/harness_runtime.py validate-state .harness/features/FEAT-001/state.json
python scripts/harness_runtime.py replay .harness/features/FEAT-001/timeline.ndjson
```

## Gate CLI

```bash
python scripts/check-spec/check_spec.py SPEC.md --json
python scripts/check-design/check_design.py DESIGN.md --spec SPEC.md --json
python scripts/check-risk/check_risk.py RISK.md --json
python scripts/check-code-style/check_code_style.py . --json
python scripts/check-security/check_security.py . --json
python scripts/check-review-pass/check_review_pass.py review.md --json
python scripts/check-test-coverage/check_test_coverage.py coverage.json --json
```

## Exit Codes

| Status | Exit | Meaning |
| --- | ---: | --- |
| PASS | 0 | Gate passed with evidence. |
| FAIL | 1 | Must fix and roll back to the mapped node. |
| WARN | 2 | May continue only when policy allows warning carry-forward. |
| BLOCK | 3 | Stop for human intervention. |
