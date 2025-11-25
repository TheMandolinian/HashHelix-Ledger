# Stage 11 — Canonical Engine Export Layer  
**HashHelix Public Engine Layer — WDTP Reference Export**  
**Author:** James Bradley Waresback  
**Status:** Completed (Engine-Only)

---

## 0. Purpose
Stage 11 defines the **canonical WDTP engine interface** and exports it across:
- Python (reference implementation)
- Rust (NER-compliant skeleton)
- WASM (language-neutral interface)
- Test harness and equivalence suite

This stage **does not touch relics, vaults, anchors, tokenomics, or business logic.**  
Engine-only.

---

## 1. WDTP Recurrence (Immutable)
\[
a_1 = 1,\quad
a_n = \lfloor n\cdot\sin(\phi_n)\rfloor + 1
\]

Where:
\[
\phi_n = (a_{n-1} + \pi/n)\bmod 2\pi
\]

### LAW 4 — Numerical Evaluation Rule (NER)
All implementations **must** reduce the phase modulo \(2\pi\) before applying `sin()`:

\[
\phi_n = (prev\_a + \pi/n) \bmod 2\pi
\]

Without NER: WDTP drifts  
With NER: WDTP is deterministic forever

---

## 2. Canonical Python Engine  
**File:** `engine/wdtp.py`

Implements:
- `ner_phase(prev_a, n)`
- `wdtp_step(prev_a, n)`
- `wdtp_sequence(n_max, a1=1)`
- `wdtp_iter(start_n=2, a1=1)`
- `wdtp_prefix_hash(n_max, a1=1)`

Python is the **reference truth** for all future engines.

**Canonical first-20 vector:**

[1, 2, 1, 4, -4, 2, 5, -6, 6, 1,
11, -11, 13, 9, 4, -13, -4, 12, -7, -10]

**Prefix hash (n=20):**

075b82498d4ed93704af351af363e2ff05ed20bbb212965974ceb80e7f86a699


---

## 3. Rust Engine Skeleton (NER-Compliant)
**File:** `engine/rust/wdtp.rs`

Exports:
- `ner_phase(prev_a, n)`
- `wdtp_step(prev_a, n)`
- `wdtp_sequence(n_max, a1)`
- `WdtpIter` infinite iterator

Rust must return:
- Identical values to Python for all \(n\)
- Identical prefix-hashes
- No drift at N=1,000,000

---

## 4. WASM Export Layer  
Defines the minimal WebAssembly interface so any platform can verify WDTP:

Exports:
- `wasm_wdtp_step(prev_a, n)`
- `wasm_wdtp_sequence(n_max, a1)` → `Int32Array`
- `free(pointer)`

JS Glue Contract:
```js
import init, { wasm_wdtp_step, wasm_wdtp_sequence } from "./wdtp_wasm.js";
await init();

// Example usage:
const x = wasm_wdtp_step(1, 2);          
const seq20 = wasm_wdtp_sequence(20, 1); 

Rules:
- JS may **not** compute sin() or recurrence logic.  
  (All logic MUST remain in Rust → WASM.)
- JS only handles integer outputs.

---

## 5. Cross-Language Equivalence Contract
**File:** `tests/stage11/replay_equivalence.py`

All alternate engines (Rust, WASM, hardware) must match Python on:

### 5.1 Small-N Sequence Check  

[1, 2, 1, 4, -4, 2, 5, -6, 6, 1,
11, -11, 13, 9, 4, -13, -4, 12, -7, -10]


### 5.2 Prefix-Hash Parity  
Engines must match Python prefix-hashes at:
- N = 20  
- N = 1,000  
- N = 100,000  

### 5.3 NER Drift Test (Critical)
Engines must match Python at:
- N = 1,000,000

A mismatch = NER violation.

---

## 6. Stage 11 Harness
**File:** `tests/stage11/run_stage11_harness.py`

Runs:
1. Small-N vector test  
2. Mid-N determinism (100k)  
3. 1M drift test  

Sample output:

small-N check: OK
mid-N determinism (N=100000) check: OK
N=1M drift check: OK
Stage 11 harness complete: ALL OK


---

## 7. Definition of Done
- [x] Python canonical engine  
- [x] Rust skeleton  
- [x] WASM export design  
- [x] Cross-language equivalence suite  
- [x] Drift test at N=1M passes  
- [x] `engine_api.md` published  
- [x] Merged into main  
- [x] No business-layer changes  

**Stage 11 is complete.**

---

## 8. Next Stage  
Proceed to **Stage 12 — Engine Compliance Suite & Public Verification Pack**  
(Target version: **v1.9.43**)

This will produce:
- Official WDTP test vectors  
- Compliance suite  
- CI matrix  
- Institutional verification guide  

