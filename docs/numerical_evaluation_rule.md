# Numerical Evaluation Rule (NER)
**Binding Engine Law — LAW 4 (v1.9.4)**

## Purpose
The Numerical Evaluation Rule (NER) guarantees that the Waresback Deterministic Temporal Primitive (WDTP) remains
bit-for-bit deterministic across:

- extremely large N (high-step execution)
- different CPUs / math libraries
- different languages (Python, Rust, C, FP, WASM, hardware)
- long-running institutional deployments

Without NER, floating-point phase drift accumulates in the sine argument, leading to cross-machine divergence.

## Canonical WDTP Recurrence (unchanged)
WDTP is defined as:

- **Seed:** `a₁ = 1`  
- **Recurrence (n ≥ 2):**
  
  \[
  a_n = \left\lfloor n \cdot \sin(a_{n-1} + \pi/n) \right\rfloor + 1
  \]

**NER does not modify this mathematics.**  
NER only standardizes how the sine argument is evaluated.

## LAW 4 — Numerical Evaluation Rule (NER)
Before any `sin()` call, the phase **must** be reduced modulo `2π`:

\[
\text{phase} = (a_{n-1} + \pi/n) \bmod 2\pi
\]

\[
a_n = \left\lfloor n \cdot \sin(\text{phase}) \right\rfloor + 1
\]

### Canonical reference implementation (Python)

```python
phase = (a_prev + math.pi / n) % (2.0 * math.pi)
a_n = math.floor(n * math.sin(phase)) + 1
