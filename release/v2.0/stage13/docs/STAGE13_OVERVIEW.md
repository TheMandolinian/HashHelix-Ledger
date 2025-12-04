# Stage 13 — Institutional Packaging (HashHelix Public Engine v2.0.0)

This bundle defines the canonical public-engine standard for HashHelix.

- **Version:** v2.0.0
- **Tag:** `v2.0.0-engine`
- **Layer:** Public Engine (LAW-10 compliant)
- **Scope:** Engine-only deterministic core (no business-layer or tokenomics).

## Bundled Artifacts

### 1. Canonical Laws
- `laws/HashHelix_Ledger_Laws_v1.9.41.pdf`  
  The full canonical Ledger Laws document that governs the v2.0.0 engine.

### 2. Whitepaper
- `whitepaper/HashHelix_Ledger_Whitepaper_v1.9.41.pdf`  
  The complete HashHelix ledger whitepaper (v1.9.41), including:
  - WDTP formulation
  - Numerical Evaluation Rule (NER)
  - Locking behavior and periodic compression
  - Engine structure (lanes, epochs, anchors)
  - Legal layer: canonical Ledger Laws inside

### 3. Verification
The Stage 12 cross-runtime equivalence results and test vector outputs
will live under this folder.

### 4. Schemas
JSON schemas for deterministic engine artifacts:
- Root Relics  
- Epoch Bundles  
- Anchor Envelopes  
- Deterministic Objects  

### 5. Engine
Documentation for implementers referencing the canonical engine tag
`v2.0.0-engine`.

## Integrity
The file `checksums.sha256` provides SHA-256 integrity hashes for
canonical stage artifacts.

