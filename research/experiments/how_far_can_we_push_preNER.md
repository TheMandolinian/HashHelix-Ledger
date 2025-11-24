# Experiment #4 — “How Far Can We Push Before It Lies?”
HashHelix Research Suite
Status: Active, Fundamental Stress Test

## Purpose
This experiment explores the limits of the recurrence when you push it to very large step counts (n = 100k → 1M+), especially under floating-point arithmetic.

We want to discover:
- Does the sequence remain stable?
- Do floating-point errors accumulate?
- Does any form of periodicity or collapse appear?
- Does the recurrence begin “lying” due to precision loss?
- Do different languages (Python, Rust, JS, C) diverge?

This experiment establishes the **numerical stability envelope** of HashHelix.

---

## 1. Recurrence (Forward Helix Only)

We test the standard lane:


a_1 = 1,\quad
a_n = \left\lfloor n \cdot \sin(a_{n-1} + \pi/n) \right\rfloor + 1


Run this **as far as your machine allows**:
- N = 100,000 (safe)
- N = 500,000 (stress)
- N = 1,000,000+ (danger zone)
- N = 5,000,000+ (requires HPC hardware)

---

## 2. Experiment Variants

### 2.1 Pure Float64 (Default)
Use your language’s built-in double precision `sin()`.

Measure:
- divergence from earlier checkpoints
- drift in average value
- variance vs n
- whether results differ run-to-run (they shouldn’t)

### 2.2 Mixed Precision
Intentionally reduce precision:
- float32 
- fixed-point approximations 
- fast-math trig approximations (CORDIC, Bhaskara, LUT)

Compare the sequences:
- where do they start diverging?
- how quickly does divergence grow?

### 2.3 Cross-Language Determinism Test
Run the same N in:
- Python (float64)
- Rust (libm or std)
- C (math.h)
- JavaScript (double)
- WASM (V8 / WASI)

Record:
- if they match exactly
- if they diverge at step k
- how large the gap becomes

This is crucial for multi-platform determinism.

---

## 3. What To Analyze

### 3.1 Drift
Plot:
- n vs aₙ 
- difference between checkpoints (e.g., every 5k steps)

Look for:
- increasing amplitude
- band formation
- numerical instability

### 3.2 Oscillation / Phase Behavior
Look for:
- envelope curves
- chaotic oscillation patterns
- smooth vs spiky regions

### 3.3 Periodicity Detection
Use:
- short-cycle search (Floyd/Brent)
- modular reductions (aₙ mod m for various m)
- autocorrelation
- FFT frequency analysis

> If any cycle is found → major breakthrough / major vulnerability.

So far, no periodicity found up to ~200k steps.

### 3.4 Cross-Environment Divergence
Document:
- does sequence in Python drift from Rust?
- if so, when and how badly?

This tells us whether we:
- must adopt fixed-point trig 
- or can rely on float64 sine forever.

---

## 4. Reproducibility Notes

Always record:
- OS + CPU + RAM
- language + version
- machine / CPU
- math library (libm, V8, etc.)
- N value
- initial seed
- recurrence form

Floating-point chaos is extremely environment-dependent.

---

## 5. Future Extensions

This experiment leads to:
- fixed-point integer-only HashHelix
- deterministic WASM implementations 
- chiral drift under ultra-high n 
- hardware-accelerated sin() comparison 
- distributed “floating-point divergence maps”

This is one of the most important scientific foundations for HashHelix.

EOF
