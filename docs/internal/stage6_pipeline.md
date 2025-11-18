# Stage 6 — Engine-Only Validation & Compression Pipeline

This document describes the Stage 6 engine-only pipeline used to validate and compress
HashHelix lane artifacts. It is an **engineering-facing** description with no business,
tokenomics, or licensing details.

## Scope

Stage 6 locks down:

- Engine-only JSON artifact structure
- Deterministic JSON serialization
- GZIP compression / expansion
- Minimal CI around sample artifacts

Math, recurrence, tokenomics, and business model are defined elsewhere (PDFs).

## Tools

All scripts live in `scripts/`:

- `hh_validate_engine.py`
  - Checks engine artifacts for:
    - Valid JSON
    - Expected structure (soft checks)
    - Absence of business-layer keys (pricing, tokenomics, customers, etc.)

- `hh_compress.py`
  - Input: engine-only JSON file
  - Output: deterministic `*.json.gz` next to the original
  - Uses sorted keys and minimal separators for stable byte output

- `hh_expand.py`
  - Input: `*.json.gz`
  - Output: JSON file with deterministic formatting
  - Confirms the compressed payload is valid JSON

- `hh_bundle_inspect.py`
  - Reads an engine artifact (and optional `.gz`)
  - Prints:
    - Lane (if present)
    - Epoch count (if present)
    - JSON and GZIP sizes
    - SHA-256 of the deterministic JSON bytes

## Sample Artifact

Sample files live under:

- `artifacts/stage6_sample/lane01_artifact.json`
- `artifacts/stage6_sample/lane01_artifact.json.gz` (generated)

These serve as canonical examples for CI and future tooling.

## CI Workflow

GitHub Actions workflow:

- `.github/workflows/validate-stage6.yml`

On each push / PR to `main`:

1. Checkout repo
2. Set up Python 3.12
3. Run:
   - `python scripts/hh_validate_engine.py artifacts/stage6_sample/lane01_artifact.json`
   - `python scripts/hh_compress.py artifacts/stage6_sample/lane01_artifact.json`
   - `python scripts/hh_expand.py artifacts/stage6_sample/lane01_artifact.json.gz`

If any step fails, the job fails.

## Purpose

Stage 6 ensures that:

- Engine artifacts are structurally sane
- There is a deterministic, portable compression format
- CI can repeatedly verify this behavior

With this in place, later stages (business ledger, tokenomics, XRPL integration)
can build on a locked and reproducible engine foundation.
