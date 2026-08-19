# Project Wiki

White Harness 2.0 uses a three-level repository map so agents read the smallest useful context first.

## L1 Overview

`overview.md` explains product boundaries, top-level architecture, and module index.

## L2 Module Maps

`modules/*.md` maps each major module to entry points, ownership, APIs, data stores, tests, and known risks.

## L3 Semantic Maps

`semantic-map/*.yaml` connects business terms, APIs, UI components, data tables, and code symbols.

## Freshness

Track source-to-wiki hashes in `.harness/wiki-manifest.json` and run:

```bash
python scripts/check-knowledge-stale/check_knowledge_stale.py .harness/wiki-manifest.json --json
```

The gate returns `WARN` when a tracked source hash changes and the wiki needs refresh.
