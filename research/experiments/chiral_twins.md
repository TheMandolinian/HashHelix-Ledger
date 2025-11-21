# Chiral Twins — Dual-Helix Mirror Recurrence (+π/n vs −π/n)

**Purpose:** 
Study how the HashHelix recurrence behaves when the phase term is flipped in sign: 
one lane uses +π/n and the other uses −π/n.

This produces a “right-handed” and “left-handed” twin, evolving together but not necessarily matching.
The difference between them is the raw material for:
- chiral commitments 
- integrity detection 
- self-verifying epochs 
- cross-lane comparison 
- time-symmetry studies 

This experiment isolates the core geometric idea of HashHelix chirality.

---

## 1. Recurrence Definitions

**Forward (+) lane:**

a₁⁺ = 1
aₙ⁺ = floor(n · sin(aₙ₋₁⁺ + π/n)) + 1


**Reverse (−) lane:**

a₁⁻ = 1
aₙ⁻ = floor(n · sin(aₙ₋₁⁻ − π/n)) + 1


Both begin with the same seed and diverge from step 2 onward.

---

## 2. Experiment Setup

### 2.1 Choose number of steps
Recommended:

- **N = 5,000** (quick test)
- **N = 25,000** (visible structure)
- **N = 100,000–200,000** (deep chiral drift)

### 2.2 Compute both sequences
Produce arrays:

plus[n] = aₙ⁺
minus[n] = aₙ⁻


---

## 3. What To Analyze

### 3.1 Divergence signal

Compute:

Δ(n) = | aₙ⁺ − aₙ⁻ |


Questions:

- Does Δ(n) explode?
- Does it oscillate?
- Does it remain bounded?
- Does it show periodic “alignment pulses”?

This is the core of geometric integrity checking.

---

## 3.2 Chiral Commitment Signal

Compute:

Cₙ = SHA256( min(aₙ⁺, aₙ⁻) || max(aₙ⁺, aₙ⁻) )


This is the lightweight integrity primitive:
- simple
- deterministic
- collision-resistant
- sensitive to any divergence

Plot:

n vs (Cₙ mod 10⁶)


to visualize commitment variation.

---

## 4. Suggested Plots

### A. Time Series

n vs aₙ⁺
n vs aₙ⁻


Look for symmetric envelopes or drift.

### B. Divergence Plot

n vs Δ(n)


Key indicator of chiral behavior.

### C. Phase Space
Plot:


(aₙ⁺, aₙ⁻)


Scatterplots here often form diagonal bands or chaotic clusters.

---

## 5. Reproducibility Notes

Record:

- math precision
- seed
- step count
- language/runtime
- machine
- implementation details (float64 vs fixed-point)

This helps future research validate the same behavior.

---

## 6. Extensions

Future chiral files will explore:

- chiral commitments over epochs
- twin-strand Merkle trees
- chiral drift heatmaps
- twin-lane fork-choice rules
- “reversible epochs” using backward drift

These will be separate experiments in this folder.

---

## 7. Status

This is Experiment #3 in the HashHelix research suite.

