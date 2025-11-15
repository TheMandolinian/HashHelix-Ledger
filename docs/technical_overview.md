# HashHelix: A High-Performance Proof-of-Time Primitive

## 1. Core Recurrence

\[
a_1 = 1, \quad
a_n = \left\lfloor n \cdot \sin(a_{n-1} + \pi/n) \right\rfloor + 1
\]

- **Sequential per lane**: each step depends on the previous one.
- **Parallel across lanes**: independent recurrences can be run concurrently.
- **Measured throughput**:  
  - ≈ **8.24M steps/sec** (synthetic peak, 3 lanes)  
  - ≈ **8.1M steps/sec** (7–15 lanes)  
  - ≈ **3.4M steps/sec** (full multi-core “blast” benchmark)

HashHelix behaves like a CPU-bound temporal primitive: a deterministic “time engine”
rather than a blockchain or DAG.

---

## 2. Sequentiality and Verification

Per lane, HashHelix is strictly sequential:

- You cannot compute \(a_n\) without \(a_{n-1}\).
- Each lane is similar to a Verifiable Delay Function (VDF) or Proof-of-History (PoH) chain.

### 2.1 Evaluation and Verification

Current model:

- **Evaluation cost:** \(O(n)\)  
- **Verification cost:** also \(O(n)\) via full recomputation

This is acceptable for **Proof-of-Time (PoT)** use cases where
wall-clock timing and hardware cost are part of the trust model.

Planned enhancement:

- Introduce **sparse checkpoints** (e.g., every \(2^{16}\) steps) and commit them in a Merkle tree.
- This enables **\(O(\log n)\)** audit paths for partial verification.

---

## 3. Chiral Mode (Dual Helix)

Forward helix:

\[
a_n^+ = \left\lfloor n \cdot \sin(a_{n-1}^+ + \pi/n) \right\rfloor + 1
\]

Reverse helix:

\[
a_n^- = \left\lfloor n \cdot \sin(a_{n-1}^- - \pi/n) \right\rfloor + 1
\]

Chiral commitment:

\[
C_n = \text{SHA-256}\big(\min(a_n^+, a_n^-) \,\|\, \max(a_n^+, a_n^-)\big)
\]

Chiral mode provides:

- **Tamper evidence**: divergence between helices is detectable.
- **Integrity checking**: dual evolution acts as a redundant consistency layer.
- Not a full proof-of-computation, but a useful integrity primitive.

---

## 4. Security Considerations

Initial assumptions:

- No known shortcut to compute \(a_n\) without iterating the recurrence.
- Per-lane computation is **sequential**, while lanes remain independent.
- Arithmetic-based (no embedded cryptographic hash), so analysis focuses on:
  - orbit behavior
  - entropy
  - potential cycles or attractors

Open questions and work in progress:

- **Entropy analysis** of long sequences (e.g., 2M-step lane samples).
- **Cycle detection** and orbit density.
- **Replacement of floating-point `sin` with fixed-point or integer approximations** for strict determinism.
- **Checkpoint-based verification** for sublinear audit costs.

---

## 5. Intended Use Cases

HashHelix is designed as a **temporal primitive**, not a full ledger.

Target applications include:

- **Proof-of-Time layer** for fair transaction ordering and anti-MEV systems.
- **Deterministic AI lineage**, where model updates are bound to a reproducible temporal index.
- **Scientific recordkeeping**, enabling replayable experiments over a deterministic time-base.
- **Anchoring to external ledgers** (e.g., XRPL/XLM) using HashHelix lanes as high-resolution clocks.
- **Temporal compression and integrity**, via chiral commitments and sparse checkpoints.

---

## 6. Summary

- HashHelix is a **high-speed arithmetic Proof-of-Time primitive**.
- It achieves **multi-million steps per second** on consumer hardware.
- It offers **strong per-lane sequentiality** with fully parallel lanes.
- Chiral mode and checkpointing provide a path to **tamper evidence** and **sublinear verification**.
- Ongoing work focuses on **entropy analysis, fixed-point determinism, and formal security modeling**.
