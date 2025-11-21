# Experiment #7 — Entropy & Randomness Diagnostics
HashHelix Research Suite
Status: Active, Statistical & Chaos Analysis

## Purpose
This experiment determines whether the HashHelix temporal sequence behaves like:

- a chaotic map
- a pseudo-random generator
- a structured oscillatory system
- or something entirely unique

We analyze **entropy**, **autocorrelation**, **frequency spectrum**, and **randomness qualities** of the core recurrence.

This is essential for:
- cryptographic safety
- fork-choice predictability
- scientific reproducibility
- identifying hidden periodicity
- validating the recurrence as a high-quality PoT engine

---

## 1. Sequence Generation

Use the forward recurrence:

\[
a_1 = 1,\quad
a_n = \left\lfloor n \cdot \sin(a_{n-1} + \pi/n) \right\rfloor + 1
\]

Generate sequences of length:

- **N = 100,000**
- **N = 500,000**
- **N = 2,000,000** (if CPU permits)

Save raw integer output to:

hh_entropy_lane01.txt

Format:
One integer per line.

(Already supported via previous tools/scripts.)

---

## 2. Diagnostics to Perform

### 2.1 Shannon Entropy (H)
Compute:

\[
H = -\sum p_i \log_2 p_i
\]

Where \(p_i\) is the frequency of each integer modulo an appropriate bin size.

Check:
- Does entropy stay high?
- Do specific bands dominate?
- Are there forbidden states?

---

### 2.2 NIST SP 800-22 Tests (Optional)
Tests include:
- monobit
- runs
- poker
- approximate entropy
- linear complexity
- serial tests
- FFT test

We only need ~10–20 tests for a first-pass scan.

HashHelix is **not** a PRNG — but randomness properties matter for PoT fairness.

---

### 2.3 Autocorrelation Function
Compute:

\[
C(k) = \sum_{n} a_n \cdot a_{n+k}
\]

Plot C(k) across lag values k.

Look for:
- rapid decay (chaotic)
- persistent peaks (periodicity)
- long-range structure (non-random but non-periodic)

---

### 2.4 FFT Frequency Spectrum
Apply FFT to:

- raw aₙ
- Δaₙ = aₙ₊₁ − aₙ
- aₙ mod m (for various m)

Look for:
- dominant frequencies
- harmonic structure
- spectral flattening
- fractal noise profiles

A smooth, noise-like FFT → chaotic behavior.
Sharp spikes → periodic or quasi-periodic structure.

---

### 2.5 Histogram & Value Distribution
Plot histogram of:

- aₙ mod 100
- aₙ mod 360
- Δaₙ

Look for:
- preferred residues
- clustering
- uniformity vs bias

---

## 3. What to Look For

### 3.1 Signs of Chaos
- high entropy
- rapidly decaying autocorrelation
- broadband FFT spectrum
- sensitivity to initial conditions
- divergence across implementations/languages

### 3.2 Signs of Hidden Periodicity
- repeating FFT peaks
- autocorrelation spikes
- modular repetition patterns

> If periodicity is discovered → publish immediately; it would be huge.

### 3.3 Signs of Float Drift Effects
At large N:
- bias toward certain residues
- collapse of distribution
- short repeating windows
- loss of amplitude 

---

## 4. Reproducibility Notes

For all submitted reports, record:

- CPU / OS
- N value
- language/runtime
- math library
- sequence file name
- time to compute
- entropy accuracy

Keep results in:

research/entropy_reports/


(each user/computer gets its own file)

---

## 5. Extensions

This experiment is the base for:

- Lyapunov exponent estimation
- Chiral entropy comparisons
- Multi-lane entropy divergence
- Fixed-point vs floating entropy comparison
- “Entropy maps” across seed space

Entropy diagnostics are required to classify HashHelix in chaos theory terms.

---

## Status
This is Experiment #7 in the HashHelix research suite.
EOF

