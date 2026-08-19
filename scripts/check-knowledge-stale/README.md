# check-knowledge-stale

Detects stale Repository Map entries by comparing tracked source file hashes with `.harness/wiki-manifest.json`.

```bash
python scripts/check-knowledge-stale/check_knowledge_stale.py .harness/wiki-manifest.json --json
```

Exit codes follow the v2.0.0 gate contract:

| Status | Exit |
| --- | ---: |
| PASS | 0 |
| FAIL | 1 |
| WARN | 2 |
| BLOCK | 3 |

Missing or empty manifest returns `WARN`; changed hashes return `WARN` by default or `FAIL` with `--fail-on-stale`.
