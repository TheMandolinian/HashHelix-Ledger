# Experiment #8 — Cycle Detection & Periodicity Search
HashHelix Research Suite
Status: Active, Critical Structural Analysis

## Purpose
This experiment attempts to discover whether the HashHelix recurrence ever:

- falls into a true cycle
- enters a near-cycle (quasi-periodic loop)
- collapses into a low-dimensional attractor
- revisits earlier state + step index contexts

If any real periodicity is found, it may reveal:
- structural vulnerabilities
- hidden symmetry
- new mathematical theorems about the recurrence

So far, no periodicity has been observed, but this experiment formalizes the search.

---

## 1. Recurrence

We use the standard forward recurrence:

\[
a_1 = 1, \quad
a_n = \left\lfloor n \cdot \sin(a_{n-1} + \pi/n) \right\rfloor + 1
\]

Generate at least:
- N = 10,000 
- N = 50,000
- N = 100,000
- Optional: N = 250,000–500,000

---

## 2. Exact Cycle Search

We use classic cycle-finding algorithms:

### 2.1 Floyd’s Cycle-Finding (“Tortoise and Hare”)
Algorithm:

t = f(seed)
h = f(f(seed))

while t != h:
t = f(t)
h = f(f(h))


### 2.2 Brent’s Algorithm (More efficient)
Better for very long sequences:

- Adaptive powering
- Fewer evaluations
- Less memory 

These test whether:
\[
a_i = a_j \quad \text{for some } i \neq j
\]

> If found → exact periodicity → publish immediately.

---

## 3. Near-Cycle Search

### 3.1 Windowed Pattern Matching
Check for repeated windows:

[a_n, a_{n+1}, ..., a_{n+k}] == [a_m, a_{m+1}, ..., a_{m+k}]


Values of k:
- 5
- 10
- 20
- 50

### 3.2 Autocorrelation Repeat Peaks
Use autocorrelation function to detect:
- repeating motifs
- partial orbit re-alignments

### 3.3 Modular Periodicity
Compute:
- aₙ mod m
for various m values:
- m = 10, 50, 100
- m = 360 (angular)
- m = 997 (prime modulus)

Look for repeating modular patterns.

---

## 4. Periodicity Red Flags

These patterns may indicate hidden near-cycles:
- sudden collapse into narrow band
- repeated envelopes
- identical small subsequences
- matching aₙ vs aₙ₊₁ values

If anything suspicious appears, document it immediately.

---

## 5. Divergence Verification (Cross-Run)
Run the same test:
- twice in Python
- once in Rust
- once in C

If:
- Python finds a “cycle”
- Rust does **not**
- C does **not**

→ it was floating-point drift, not a true cycle.

True cycles must match across languages with identical recurrence logic.

---

## 6. Reproducibility Notes

Record:

- CPU / OS
- Language + version
- Math library
- N
- Seed (default = 1)
- Cycle-finding method (Floyd / Brent)
- Whether FP errors were mitigated

Store results in:

research/cycle_reports/


---

## 7. Expected Outcomes

Most likely:
- no true cycle
- possible short repeated motifs
- regular modular echoes
- FP-induced pseudo-cycles

If a true cycle is found → it is groundbreaking.

---

## Status
This is Experiment #8 in the HashHelix research suite.

EOF

