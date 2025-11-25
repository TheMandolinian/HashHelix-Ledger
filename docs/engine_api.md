# Stage 11 — Canonical Engine Export Layer
**HashHelix Public Engine — WDTP Reference API**
**Status:** Draft (Stage 11)

---

## 0. Scope (Engine-Only)
This document defines the **public, canonical WDTP engine interface** across languages.

Included:
- Canonical Python binding (reference implementation)
- Rust skeleton (NER-compliant)
- WASM export design
- Optional C header

Excluded (explicitly out of scope):
- Business ledger logic
- Relic / vault / anchor / tokenomics logic
- Any private-layer interfaces

---

## 1. WDTP Recurrence (Immutable)
WDTP is **not redesigned here**. This stage exports it.

\[
a_1 = 1,\quad
a_n = \lfloor n \cdot \sin(\phi_n) \rfloor + 1
\]

Where:

\[
\phi_n = (a_{n-1} + \pi/n)\ \bmod\ 2\pi
\]

**LAW 4 (NER) is binding:** phase reduction mod \(2\pi\) is mandatory in all languages.

---

## 2. Canonical Python API

**File:** `/engine/wdtp.py`  
This is the *reference implementation* all other languages must match.

### 2.1 Constants
- `TAU = math.tau`  
  Canonical value for \(2\pi\).

### 2.2 Functions

#### `ner_phase(prev_a: int, n: int) -> float`
Computes NER-reduced phase:

\[
\phi_n = (prev\_a + \pi/n) \bmod 2\pi
\]

Rules:
- `n` MUST be `>= 2`
- Uses `fmod(phase_raw, TAU)` for deterministic reduction.

#### `wdtp_step(prev_a: int, n: int) -> int`
Single recurrence step:

\[
a_n = \lfloor n \cdot \sin(\phi_n) \rfloor + 1
\]

Rules:
- `n` MUST be `>= 2`
- MUST call `ner_phase()` before `sin()`.

#### `wdtp_sequence(n_max: int, a1: int = 1) -> List[int]`
Generates finite sequence:

\[
[a_1, a_2, \dots, a_{n\_max}]
\]

Rules:
- `n_max >= 1`
- Default seed `a1 = 1`.

#### `wdtp_iter(start_n: int = 2, a1: int = 1) -> Iterator[int]`
Infinite generator yielding:

\[
a_1, a_2, a_3, \dots
\]

Rules:
- `start_n >= 2`
- Default seed `a1 = 1`.

#### `wdtp_prefix_hash(n_max: int, a1: int = 1) -> str`
Equivalence-test helper.  
Returns SHA-256 hex digest of the first `n_max` terms, comma-joined UTF-8.

Purpose:
- Used to compare Python ↔ Rust ↔ WASM replay determinism.

### 2.3 Canonical Test Vector (small-N)
First 20 terms (seed `a1=1`):

`[1, 2, 1, 4, -4, 2, 5, -6, 6, 1, 11, -11, 13, 9, 4, -13, -4, 12, -7, -10]`

Prefix hash (n_max=20):

`075b82498d4ed93704af351af363e2ff05ed20bbb212965974ceb80e7f86a699`


## 3. Rust Engine Skeleton API (NER-Compliant)

**File:** `/engine/rust/wdtp.rs`  
This is a **Stage 11 skeleton** meant to be compiled into a Rust crate later.  
Its semantics MUST match the canonical Python reference exactly.

### 3.1 Constants
- `TAU: f64 = 2π`  
  Canonical modulus value.

### 3.2 Functions

#### `ner_phase(prev_a: i64, n: u64) -> f64`
Computes NER-reduced phase:

\[
\phi_n = (prev\_a + \pi/n) \bmod 2\pi
\]

Rules:
- `n >= 2`
- MUST use Euclidean modulus: `rem_euclid(TAU)`.

#### `wdtp_step(prev_a: i64, n: u64) -> i64`
Single recurrence step:

\[
a_n = \lfloor n \cdot \sin(\phi_n) \rfloor + 1
\]

Rules:
- `n >= 2`
- MUST call `ner_phase()` before `sin()`.

#### `wdtp_sequence(n_max: u64, a1: i64) -> Vec<i64>`
Generates finite sequence:

\[
[a_1, a_2, \dots, a_{n\_max}]
\]

Rules:
- `n_max >= 1`
- Default seed in tests is `a1 = 1`.

### 3.3 Iterator

#### `WdtpIter`
Infinite iterator yielding:

\[
a_1, a_2, a_3, \dots
\]

Rules:
- First yield is `a1`
- Subsequent yields use `wdtp_step(prev, n)`.

### 3.4 Canonical Test Vector
Rust unit tests MUST include the canonical 20-term vector and match Python exactly.

Vector:
`[1, 2, 1, 4, -4, 2, 5, -6, 6, 1, 11, -11, 13, 9, 4, -13, -4, 12, -7, -10]`


## 4. WASM Export API

The WASM layer provides a **minimal, deterministic, language-neutral interface** for WDTP.  
It is NOT a full Rust crate — only an export surface for external runtimes (Node, Bun, Go, Python via wasm3, JS engines, etc.).

**Implementation rule:**  
The WASM module MUST wrap the Rust skeleton code from Section 3 without alteration.

---

### 4.1 Exported Functions (Final, Canonical)

#### `wdtp_step(prev_a: i32, n: i32) -> i32`
Direct wrapper over Rust `wdtp_step`.  
Rules:
- `n >= 2`
- Uses Rust’s NER reduction (rem_euclid)

#### `wdtp_sequence(n_max: i32, a1: i32) -> pointer`
Returns a pointer to a WASM memory block containing **i32[]** of length `n_max`.

Memory layout (little-endian):


## 5. Optional C Header
(TBD)

---

## 6. Cross-Language Replay Equivalence Tests

**Canonical rule:** Python (`/engine/wdtp.py`) is the *reference truth*.  
Rust and WASM exports MUST match Python term-for-term.

**Harness file:** `/tests/stage11/replay_equivalence.py`

### 6.1 Equivalence Dimensions

1. **Small-N sequence vector**
   - Engines MUST reproduce the canonical first-20 terms exactly.

2. **Prefix-hash parity**
   - Engines MUST match Python SHA-256 prefix hashes at:
     - N = 20
     - N = 1,000
     - N = 100,000

3. **NER drift compliance**
   - Engines MUST match Python at:
     - N = 1,000,000
   - Any divergence indicates missing/incorrect LAW-4 phase reduction.

### 6.2 Canonical Vector & Hash
Vector (N=20):

`[1, 2, 1, 4, -4, 2, 5, -6, 6, 1, 11, -11, 13, 9, 4, -13, -4, 12, -7, -10]`

Prefix hash (N=20):

`075b82498d4ed93704af351af363e2ff05ed20bbb212965974ceb80e7f86a699`


## 7. Stage 11 Test Harness

Stage 11 ships a Python-led harness to validate canonical determinism and NER compliance.

### 7.1 Files
- **Equivalence contract:** `/tests/stage11/replay_equivalence.py`
- **Harness runner:** `/tests/stage11/run_stage11_harness.py`

### 7.2 Required Checks

1. **Small-N sequence checks**
   - Verifies the canonical first-20 vector and its prefix hash.

2. **Mid-N determinism check**
   - Recomputes prefix hash at N=100,000 twice.
   - Hashes MUST match.

3. **N=1,000,000 drift test**
   - High-N repeatability check.
   - Any mismatch indicates non-NER evaluation in an alternate engine.

### 7.3 Pass Condition
Stage 11 is considered valid when:
- Harness passes on Python canonical engine, and
- Rust + WASM engines (when wired) pass the equivalence harness without drift.

