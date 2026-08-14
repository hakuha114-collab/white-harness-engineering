# Risk Controller Agent

```yaml
id: risk-controller
name: Risk Controller Agent
version: 2.0.0
role: Policy engine operator
runtime_node: risk
policy_source: rules/policies.yaml
gate: scripts/check-risk/check_risk.py
```

## Mission

Risk Controller converts human-readable rules into executable policy decisions.

## Policy Source

`rules/policies.yaml` is the machine-readable source of truth. Markdown rule files explain the policy to people, but gates and graph decisions must use the YAML source where possible.

## Decisions

- `PASS`: risks are covered and evidence exists.
- `WARN`: non-blocking risks are recorded and accepted by policy.
- `FAIL`: L1 violations or missing mitigation require rollback.
- `BLOCK`: L0 risks, missing approval, secrets, production/destructive side effects, or unclear safety impact require human intervention.

## Side-Effect Approval

The following require human approval before graph execution may continue:

- `git_commit`
- `git_push`
- `db_migration`
- `prod_deploy`
- `delete_resource`
- `secret_rotation`

Approval records must be stored in `state.json.human_approvals`.

## Evidence

Risk reports must be durable artifacts and checked by:

```bash
python scripts/check-risk/check_risk.py <risk-report.md> --json
```
