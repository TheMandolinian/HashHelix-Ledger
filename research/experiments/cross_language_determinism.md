# Experiment #5 — Cross-Language Determinism Test
HashHelix Research Suite
Status: Active, Multi-Platform Consistency Study

---

## Purpose
This experiment tests whether different programming languages produce *bit-for-bit identical* results for the HashHelix recurrence.

We want to know:

- Does Python match Rust?
- Does Rust match C?
- Does C match JavaScript (V8)?
- Does WASM behave deterministically across browsers or runtimes?
- When divergence occurs, **at which step index does it first appear?**

This determines whether HashHelix requires:

- fixed-point trig,
- integer-only recurrence,
- or strict floating-point contract libraries.

This is one of the most important experiments for long-term ledger determinism.

---

## 1. Recurrence

All languages must compute this *exact* recurrence:

a1 = 1
an = floor(n * sin(a(n-1) + π/n)) + 1


Requirements:

- Use **double precision (64-bit float)** everywhere.
- Use each language’s **default math library sin()**.
- Use identical seed: `a1 = 1`.

---

## 2. Required Languages

Run this experiment in as many as possible:

- **Python 3.10+**
- **Rust (std + libm)**
- **C (math.h)**
- **JavaScript (V8 / Node.js)**
- **WASM (browser + WASI)**
- Optional: **Java**, **Go**, **Swift**, **C#**, **Julia**, **R**

The more, the better.

---

## 3. Test Steps

### 3.1 Compute for several values of N

Run the recurrence to:

- N = 5,000  (quick scan)
- N = 25,000 (structural)
- N = 100,000 (deep drift check)
- N = 200,000+
- Optional: N = 500,000+ (stress)

### 3.2 Record at check-points

For each language, store:

- a_100
- a_500
- a_2,000 
- a_10,000 
- a_25,000 
- a_50,000 
- a_100,000
- last value a_N

Use a simple JSON file:

{
"language": "python",
"N": 100000,
"checkpoints": {
"100": ...,
"500": ...,
"2000": ...,
"10000": ...,
"25000": ...,
"50000": ...,
"100000": ...
},
"final": ...
}

---

## 4. Divergence Analysis

After all results are gathered, analyze:

### 4.1 Match or Diverge?

For each checkpoint k:

- If values match → deterministic
- If values differ → log divergence point

### 4.2 Divergence Onset

Define:

Divergence step = smallest n such that a_n(lang1) ≠ a_n(lang2)


### 4.3 Drift Magnitude

Plot:

- n vs |aₙ(langA) − aₙ(langB)|

Look for:

- small drift → floating-point noise
- large drift → chaotic divergence
- sudden collapse → potential precision bug

---

## 5. Expected Outcomes

Based on chaotic map theory and early tests:

- JS is likely to diverge earliest
- Python + C typically stay close
- Rust libm may drift slightly differently
- WASM often surprises with early sin() deviation

If all languages agree to N ≥ 50,000 → extraordinary and rare.

If they diverge → you know exactly where and why.

This experiment defines the **determinism envelope** of floating-point HashHelix.

---

## 6. Reproducibility Notes

Always record:

- CPU architecture
- OS
- Math library (libm, V8, WASM)
- Compiler flags
- Language version
- N
- Seed (=1)
- Recurrence code snippet

Small changes (compiler flags, JIT warmup, browser type) can change sin() behavior.

---

## 7. Extensions

Future related experiments:

- fixed-point trig implementation
- integer-only approximation
- WASM deterministic sin() module
- multi-lane cross-language drift
- chiral twin determinism tests

Cross-language determinism is mandatory for any on-chain or distributed version of HashHelix.

EOF
