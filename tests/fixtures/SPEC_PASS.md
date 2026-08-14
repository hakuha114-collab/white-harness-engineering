# Order Export SPEC

## Overview

Users need a batch order export flow for operations reporting.

## Goals

Export selected orders as CSV without blocking the order list page.

## Success Metrics

- Export jobs start within 2 seconds for 95% of requests.
- CSV generation succeeds for at least 99% of jobs under 10,000 rows.

## Functional Scope

- P0: create export job.
- P0: download completed CSV.
- P1: show export history.

## Acceptance Criteria

- Given 500 selected orders, the job returns an id within 2 seconds.
- Given a completed job, CSV download returns HTTP 200.

## Risks and Assumptions

- Large exports may need async worker capacity.
- Existing order permission checks are reused.
