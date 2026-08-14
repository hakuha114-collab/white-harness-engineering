---
name: white-harness-engineering
version: 2.0.1
description: AI 研发全流程工程管控框架。触发：写/审 SPEC、代码审查、写测试、修 Bug、重构、部署、项目初始化，或需强制 AI 开发遵循先思考再编码、简洁优先、精准修改、目标驱动验证。v2.0.0 增加 Executable Graph、TaskState、Evidence Gate、Clean-context Reviewer、Policy YAML 和项目记忆。
agent_created: true
---

# White Harness Engineering

White Harness Engineering 是面向 AI 软件研发的管控技能。v2.0.0 的核心定位是：

```text
Skill-driven + Graph-orchestrated + State-persistent + Evidence-gated Agent Runtime
```

## When To Use

Use this skill for:

- SPEC / requirements analysis.
- Solution design.
- Risk review.
- Code implementation.
- Code review.
- Test and coverage validation.
- Bug fix, refactor, deploy, project setup.
- Any task that needs durable state, graph rollback, evidence gates, or clean-context review.

Do not use it for casual Q&A that does not touch software delivery or project management.

## Required v2 Runtime Rules

1. Use `scripts/harness_runtime.py route` to choose `trivial`, `normal`, `feature`, or `high-risk` graph when task risk is not obvious.
2. For feature and high-risk work, create feature memory before implementation:

```bash
python scripts/harness_runtime.py init --task-id <TASK_ID> --goal "<GOAL>" --workflow feature
```

3. Treat `state.json` as the machine handoff object. Do not use chat history as the state source.
4. Treat `TECH_SPEC.md` and `subtasks.json` as cross-session memory.
5. Run gates through executable scripts and keep their JSON evidence.
6. Enforce `No Evidence, No Pass`.
7. Reviewer must run in clean context and may only read spec, diff, tests, evidence, rules, policies, and relevant code.
8. Side effects covered by `rules/policies.yaml` require approval records before execution.

## Core Files

```text
config/harness.yaml                 Runtime configuration
config/router.yaml                  Dynamic routing policy
config/gates.yaml                   Gate registry and rollback mapping
runtime/graphs/*.yaml               Executable graphs
runtime/schema/task_state.schema.json
rules/policies.yaml                 Machine-readable policy source
scripts/harness_runtime.py          Runtime CLI
scripts/check-*/                    Evidence gate scripts
assets/templates/feature-memory/    TECH_SPEC, subtasks, state templates
assets/project-wiki/                L1/L2/L3 repository map
```

## Gate Contract

| Status | Exit | Meaning |
| --- | ---: | --- |
| PASS | 0 | Passed with durable evidence. |
| FAIL | 1 | Roll back and fix. |
| WARN | 2 | Continue only when policy allows. |
| BLOCK | 3 | Stop for human approval. |

## Intent Routing

| User intent | Use |
| --- | --- |
| Write SPEC / requirements | `skills/create-spec/SKILL.md`, `scripts/check-spec/check_spec.py` |
| Design feature | `agents/solution-designer/`, `scripts/check-design/check_design.py` |
| Risk / approval / side effect | `agents/risk-controller/`, `rules/policies.yaml`, `scripts/check-risk/check_risk.py` |
| Implement code | `agents/code-developer/`, selected runtime graph |
| Review code | `agents/code-reviewer/`, clean-context policy, `scripts/check-review-pass/check_review_pass.py` |
| Write or validate tests | `skills/write-test/SKILL.md`, `scripts/check-test-coverage/check_test_coverage.py` |
| Maintain project memory | `agents/project-recorder/`, `.harness/features/<TASK_ID>/`, `assets/project-wiki/` |

## Verification

Before release or handoff, run:

```bash
python scripts/self-check.py
```

## Version Management

Keep these synchronized:

- `SKILL.md` frontmatter `version`
- `config/harness.yaml` `harness.version`
- newest `CHANGELOG.md` entry
