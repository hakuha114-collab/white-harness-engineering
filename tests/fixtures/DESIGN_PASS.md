# Order Export Design

## Architecture

The feature adds an export controller, an async job service, and a storage adapter.

## Module Boundaries

- Controller owns request validation.
- Service owns job lifecycle and permission checks.
- Storage adapter owns CSV object storage.

## API Contract

- `POST /orders/export` returns `{ "job_id": "..." }`.
- `GET /orders/export/{job_id}` returns the CSV when complete.

## Rollback and Compatibility

The feature is guarded by a config flag and can be disabled without schema rollback.

## Tradeoffs

Async export avoids request timeouts at the cost of delayed download.

## Test Strategy

Unit tests cover job creation, permission checks, and CSV formatting.
