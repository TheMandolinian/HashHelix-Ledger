# Experiment #10 — Fixed-Point / Integer-Only Deterministic Recurrence
HashHelix Research Suite
Status: Critical • Enables Exact Determinism Across Platforms

## Purpose
This experiment replaces floating-point `sin()` with **deterministic fixed-point arithmetic** so that:
- every computer
- every CPU architecture
- every language
- every runtime

produces **bit-identical HashHelix sequences**.

Floating-point chaos is good for research —
but unacceptable for a production engine or ledger binding.

This experiment tests whether a fixed-point version:
- matches float64 for small n
- diverges gracefully
- introduces bias or collapse
- remains chaotic
- stays stable under high n

This is the foundation of the production HashHelix Engine.

---

## 1. Recurrence (Baseline Float64)

Reference version:

\[
a_1 = 1,\quad
a_n = \lfloor n \cdot \sin(a_{n-1} + \pi/n) \rfloor + 1
\]

This version is **NOT deterministic across languages**,
but used as the ground truth for comparison.

---

## 2. Fixed-Point Versions to Test

### 2.1 CORDIC (Integer Rotation Method)
Pros:
- exact determinism
- pure integer operations
- hardware-friendly
- portable to WASM

Cons:
- slower
- requires bit-precision tuning

### 2.2 Bhaskara Approximation (Fast, Simple)
Formula:

\[
\sin(x) \approx \frac{16x(\pi - x)}{5\pi^2 - 4x(\pi - x)}
\]

Convert all terms to integer fixed-point (e.g., Q16.16).

Pros:
- very fast
- decent accuracy

Cons:
- slightly biased near peaks

### 2.3 LUT (Lookup Table)
Use a **precomputed table** of sin values at fixed resolution.

Pros:
- deterministic
- extremely fast

Cons:
- memory tradeoff
- resolution limits

---

## 3. Fixed-Point Recurrence to Evaluate

Choose a fixed-point scaling, recommended:

- **Q16.16** (32-bit integer)
- or **Q24.8** (if performance matters)

Implement:

\[
x = a_{n-1} + (\pi / n)
\]

Convert x to fixed-point, then compute sin(x) using:
- CORDIC
- Bhaskara
- LUT
(or all three)

Then compute:

\[
a_n^{fp} = \left\lfloor n \cdot \text{sin\_fixed}(x) \right\rfloor + 1
\]

---

## 4. Comparison Metrics

For each N:

- N = 1,000
- N = 5,000
- N = 25,000
- N = 100,000

Record:

### 4.1 Local Difference
\[
d_n = |a_n^{float} - a_n^{fp}|
\]

### 4.2 Drift Behavior
Plot:
- n vs dₙ
- n vs log(dₙ + 1)

### 4.3 Global Structure
Compare:
- phase-space plots
- modular spiral plots 
- oscillation envelopes

### 4.4 Stability
Look for:
- collapse
- bias
- periodicity artifacts

These are red flags.

---

## 5. Divergence Threshold

Define the **Divergence Point**:

\[
k = \min \{ n : a_n^{float} \neq a_n^{fp} \}
\]

Record k for each method:
- CORDIC
- Bhaskara
- LUT

This tells us:
- which method is most accurate
- which method best preserves chaos
- which method is viable for production

---

## 6. Reproducibility Notes

Record:
- method used (CORDIC/Bhaskara/LUT)
- scaling (Q16.16, etc.)
- math library
- CPU/OS
- language 
- N 
- divergence point
- final aₙ^{fp}

Store results in:

research/fixed_point_reports/


---

## 7. Expected Outcomes

Likely:

- some divergence will occur
- Bhaskara is fast but drifts earlier
- CORDIC is closest but slower
- LUT is stable but resolution-sensitive

Ideal goal:
- choose a fixed-point design where drift is slow
- structure is preserved
- no collapse
- high performance

This experiment is required before building the **HashHelix Engine v2**.

---

## Status
This is Experiment #10 in the HashHelix research suite — the final core experiment.

EOF

