# HashHelix Ledger — Stage 7 Design
## Singularity → Epoch → Relic & Engine Lockdown

**Author:** James Bradley Waresback
**Branch:** `stage7-business-ledger`
**Stage:** 7

---

## 1. Stage 7 Goals

Stage 7 hardens HashHelix from a prototype into a sealed, deterministic public engine with a clear artifact pipeline:

- **HOT:** Singularity Artifact (root engine)
- **WARM:** Epoch Bundles (lane/epoch checkpoints)
- **COLD:** Temporal Relics (token-safe, frozen bundles)

At the same time, Stage 7 draws a hard line between:

- **Public engine layer** — fully open, auditable, and deterministic.
 — TO v1.4, business rules, pricing, and institutional onboarding.

The public engine can verify Temporal Relics, but it never exposes or depends on private economic state.

---

## 2. Artifact Classes & Vault Tiers

### 2.1 Singularity Artifact (HOT)

The **Singularity Artifact** is the canonical, engine-only root object.

Key properties:

- `artifact_type = "singularity"`
- `vault_class = "HOT"`
- Holds the deterministic recurrence description:
  - `seed = 1`
  - `formula = "a(n) = floor(n * sin(a(n-1) + π/n)) + 1"`
- Defines lane and epoch parameters:
  - maximum lanes
  - epoch length
- Chiral flag:
  - `chiral.enabled = true`
- Integrity root:
  - `integrity.sha256_root`

The Singularity is never tokenized. It is the canonical reference for every derived Epoch Bundle and Temporal Relic.

---

### 2.2 Epoch Bundle (WARM)

The **Epoch Bundle** is the WARM vault checkpoint that sits between the engine runtime and cold storage.

Key properties:

- `artifact_type = "epoch_bundle"`
- `vault_class = "WARM"`
- `singularity_ref` links to the HOT Singularity (id + version).
- `epoch_index` identifies which epoch this bundle represents.
- `lane_roots[]` holds, per lane:
  - `lane_id`
  - `h_plus`
  - `h_minus`
  - `merkle_root`
- `integrity.sha256_epoch_bundle` and `size_bytes` seal the bundle.

WARM epochs are produced by the engine as it runs. They can be archived, recomputed, or combined into COLD relics.

---

### 2.3 Temporal Relic (COLD)

The **Temporal Relic** is the token-safe, externally-anchorable, COLD vault artifact.

Key properties:

- `artifact_type = "temporal_relic"`
- `vault_class = "COLD"`
- `singularity_ref` ties back to the HOT engine.
- `epoch_range.start_epoch` / `end_epoch` define coverage.
- `lanes[]` lists all lane IDs included.
- `chiral_commitment`:
  - `h_plus`
  - `h_minus`
- `merkle.scheme = "sha256-merkle-v1"`
- `merkle.root` seals all included epochs.
- `integrity.sha256_bundle` and `size_bytes` seal the relic itself.
- Optional `metadata` (label, description, institution) is human-facing only.

Temporal Relics are safe to tokenize because they are frozen views of computation. They cannot change the engine; the engine verifies them.

---

## 3. Engine vs Economy Separation

### 3.1 Public Engine Layer

Public, open-source layer includes:

- Recurrence and chiral definition.
- Singularity / Epoch / Relic schemas.
- Epoch and relic tooling:
  - `scripts/epoch_combine.py`
  - `scripts/spawn_relic.py`
- CI workflows:
  - `validate-stage7.yml` for schema and vault enforcement.
- Artifact lineage rules and anti-fork checks.

This layer is designed for verifiability, reproducibility, and external audit.

### 3.2 Private Economy Layer

The private layer includes:

- Business layer v1.4 details (distribution, pricing, incentives).
- Business logic for relic issuance and institutional onboarding.
- Any mapping of relics to financial products or obligations.
- Operational policies (SLAs, hosting agreements, licensing).

The rule of Stage 7:

The engine can verify *what happened in time*, but not *what it is worth*.

---

## 4. Tooling: From Lanes to Relics

### 4.1 `epoch_combine.py`

Responsible for:

- Reading a JSON file of `lane_roots` entries.
- Constructing a WARM Epoch Bundle object that conforms to `epoch.schema.json`.
- Filling `integrity.sha256_epoch_bundle` and `size_bytes`.
- Writing the resulting bundle to an artifacts directory.

Conceptually:

1. Lanes produce strand commitments and Merkle roots.
2. Epoch combiner packages them into a single WARM checkpoint.

### 4.2 `spawn_relic.py`

Responsible for:

- Loading one or more Epoch Bundles (by glob pattern or explicit paths).
- Computing chiral commitments over all lane/epoch contributions.
- Computing a Merkle-like root over epoch hashes.
- Producing a COLD Temporal Relic that conforms to `relic.schema.json`.
- Filling `integrity.sha256_bundle` and `size_bytes`.

Conceptually:

1. Select an epoch range and the associated bundles.
2. Combine them into a single, frozen, COLD relic.
3. Use the HOT engine to verify relic integrity at any time.

---

## 5. CI: Stage 7 Validation

The `validate-stage7.yml` workflow enforces:

- All Stage 7 schemas are valid JSON Schema 2020-12.
- No nested `schemas/schemas` directories.
- Vault class constants:
  - Singularity → HOT
  - Epoch → WARM
  - Relic → COLD

This ensures that future changes cannot accidentally weaken the stage boundaries or leak private economics into the public engine.

---

## 6. Rust and Future Implementations

The Stage 7 design is language-agnostic:

- JSON schemas define the public artifact contract.
- The recurrence and chiral rules are mathematical, not Python-specific.
- Tools in `scripts/` are a reference implementation.

A Rust engine can:

- Reimplement the recurrence and epoch/relic logic.
- Use the same schemas for input/output.
- Produce identical artifacts and integrity hashes.

Stage 7’s role is to make this portability natural and verifiable.

---

## 7. Summary

Stage 7 completes three things:

1. A clear artifact hierarchy:
   - HOT Singularity → WARM Epoch → COLD Relic.
2. A hard separation between public engine and private economy.
3. Tooling and CI that enforce these rules over time.

From here, further stages can focus on performance, integrations, and institutional workflows without changing the core temporal engine.
