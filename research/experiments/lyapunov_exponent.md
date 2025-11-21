# Experiment #9 — Lyapunov Exponent Estimation
HashHelix Research Suite
Status: Active • Determines Degree of Chaos

## Purpose
The Lyapunov exponent λ measures how quickly nearby trajectories diverge.
If λ > 0 → the system is *chaotic*.
If λ = 0 → borderline chaotic / quasi-periodic.
If λ < 0 → convergent, non-chaotic.

HashHelix appears chaotic, but this experiment quantifies it.

---

## 1. Recurrence

Use the standard recurrence:

\[
a_1 = 1,\quad
a_n = \left\lfloor n \cdot \sin(a_{n-1} + \pi/n) \right\rfloor + 1
\]

And create a *perturbed* version:

\[
b_1 = 2,\quad
b_n = \left\lfloor n \cdot \sin(b_{n-1} + \pi/n) \right\rfloor + 1
\]

The only difference is the seed.

---

## 2. Divergence Tracking

Compute:

\[
d_n = |a_n - b_n|
\]

Track how quickly dₙ grows.

A chaotic system typically shows:

\[
d_n \approx d_0 e^{\lambda n}
\]

Meaning a straight line when plotting:

\[
\log(d_n) \text{ vs } n
\]

---

## 3. Steps to Perform

### 3.1 Generate two sequences
Length:
- N = 10,000 (quick)
- N = 25,000 (recommended)
- N = 50,000+ (deep chaos)

### 3.2 Compute divergence
Record:
- dₙ
- log(dₙ + 1) (to avoid log(0))

### 3.3 Fit a line
Use linear regression on:

- x = array of n values
- y = array of log(dₙ)

Slope = Lyapunov exponent λ.

---

## 4. Expected Results

- **λ > 0** → chaotic (likely)
- **λ ≈ 0** → borderline quasi-periodic
- **λ < 0** → convergent / collapsing (unlikely)

Most early tests show:
- rapid divergence → **chaotic regime**
- periodic re-alignments → **complex attractor behavior**

---

## 5. Visualization Suggestions

Plot:
- n vs dₙ
- n vs log(dₙ)
- linear regression fit
- divergence heatmaps across different seeds

Optional:
- try seeds 1–20
- compare forward and chiral (-π/n) modes

---

## 6. Reproducibility Notes

Record:
- seed pair (e.g., 1 vs 2)
- N value
- CPU / OS
- math library
- float precision
- language/version
- fitting method

Store reports in:

research/lyapunov_reports/


---

## Status
This is Experiment #9 in the HashHelix research suite.
EOF


