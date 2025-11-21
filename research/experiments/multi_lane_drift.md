# Multi-Lane Drift — Sensitivity & Divergence in HashHelix

**Purpose:**  
Explore how *multiple* HashHelix lanes evolve when started from similar but distinct initial seeds.  
This experiment reveals sensitivity to initial conditions, divergence rates, and whether the lanes
ever realign or drift apart forever.

This is the first “parallel universe” experiment for HashHelix.

---

## 1. Recurrence (per lane)

Each lane follows the standard HashHelix recurrence:

a₁ = seed
aₙ = floor(n · sin(aₙ₋₁ + π/n)) + 1


All lanes use the same update rule, but:

- **Lane 1** starts with seed = 1  
- **Lane 2** starts with seed = 2  
- **Lane 3** starts with seed = 3  
- …and so on.

Each lane becomes a separate deterministic universe.

---

## 2. Experiment Setup

### 2.1 Choose number of lanes

Try:

- **3 lanes** (minimum meaningful drift)
- **5 lanes** (good odd-number majority set)
- **16 lanes** (raw hardware scaling)
- **21 lanes** (HashHelix’s classic chiral window)

### 2.2 Choose number of steps

Recommended:

- **N = 10,000** for quick results  
- **N = 50,000** for visible structure  
- **N = 100,000–500,000** for deep drift studies

### 2.3 Generate sequences

Each lane outputs a sequence:

Lane 1 → a₁(n)
Lane 2 → a₂(n)
Lane 3 → a₃(n)
...
Lane k → aₖ(n)


Store them or plot them as needed.

---

## 3. What To Look For

### 3.1 Drift between lanes

Define drift between lanes i and j:

drift(i,j,n) = | aᵢ(n) − aⱼ(n) |


Questions:

- Does `drift(i,j,n)` grow linearly?  
- Does it grow exponentially?  
- Does it remain bounded?  
- Do some lanes repeatedly “re-sync” at random points?

This shows whether HashHelix is *Lyapunov-chaotic*, *chaotic-but-bounded*, or *weakly diverging*.

### 3.2 Lane Clustering

Plot lanes overlayed:

- Do some lanes cluster together?  
- Do some remain permanently separated?  
- Do any lanes mirror each other?

Lane clustering can reveal hidden symmetries.

### 3.3 Sensitivity to seeds

Compare lanes that start with:

- seeds 1 and 2  
- seeds 1 and 100  
- seeds 1 and 9999  

Does tiny vs huge initial separation matter after 100k steps?

---

## 4. Suggested Plots

### A. Time Series

n vs a₁(n), a₂(n), a₃(n), …


See whether lanes diverge into colored bands.

### B. Drift Over Time

Plot:

n vs drift(L₁,L₂,n)
n vs drift(L₁,L₃,n)
n vs drift(L₂,L₃,n)


This reveals divergence rates.

### C. Lane Difference Map

Plot:

(aᵢ(n), aⱼ(n))


A chaotic scatterplot signals complex relationships.

---

## 5. Reproducibility Notes

Record:

- number of lanes  
- seeds  
- N  
- math precision  
- language/runtime  
- CPU used  

HashHelix is deterministic — so if two people run this experiment with identical parameters and identical compute rules, they must get identical results.

---

## 6. Extensions

Future drift experiments may incorporate:

- lane re-seeding  
- chiral twins per lane  
- checkpoint comparison  
- integer-only sin() approximations  
- drift heatmaps  
- cross-lane Merkle commitments  

These will appear in future files in this directory.

---

## 7. Status

This file is part of the live HashHelix research experiment suite.


