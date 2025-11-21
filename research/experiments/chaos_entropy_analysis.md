# Chaos & Entropy Analysis — Statistical Fingerprinting of HashHelix

**Purpose:**  
Determine whether the HashHelix recurrence behaves like:
- a chaotic dynamical system,
- a high-entropy pseudorandom generator,
- an aperiodic map with structure,
- or some hybrid category unique to temporal spirals.

This experiment analyzes the statistical properties of the sequence aₙ over large N.

---

## 1. Recurrence Under Study

We analyze the standard forward recurrence:

a₁ = 1
aₙ = floor(n · sin(aₙ₋₁ + π/n)) + 1


This function is:
- non-linear  
- time-dependent  
- phase-shifted  
- integer-quantized  

These are classic ingredients for chaotic or quasi-chaotic behavior.

---

## 2. Experiment Setup

### 2.1 Choose long sequences
Recommended:

- **N = 50,000** (quick)
- **N = 250,000** (good)
- **N = 1,000,000+** (deep statistical analysis)

### 2.2 Precision & environment
Record:
- language (Python, Rust, C, etc.)
- numeric precision (float64 recommended)
- hardware
- OS and math library

---

## 3. Statistical Tests

Run the following analyses over the values `{aₙ}`:

### 3.1 Distribution Histogram

Plot:
- histogram of aₙ values
- running mean
- running variance

Look for:
- heavy tails  
- multimodal clusters  
- stable envelopes or oscillatory bands  

### 3.2 Entropy Estimate

Compute approximate Shannon entropy:

H = − Σ p(x) log₂ p(x)


over the normalized histogram.

Compare:
- early N vs late N
- fixed windows vs full-sequence

### 3.3 Autocorrelation

Compute lag-k autocorrelation:

corr(k) = corr(aₙ, aₙ₊ₖ)


for k = 1, 2, 5, 10, 50, 100.

Chaotic systems → fast decorrelation  
Periodic systems → strong repeated patterns

### 3.4 FFT Spectrum

FFT on `(aₙ − mean)` detects:
- periodicity  
- quasi-periodic bands  
- chaotic broadband noise  

Look for:
- sharp spikes (periodic)
- diffuse noise (chaotic)
- mixed patterns (quasi-chaotic)

### 3.5 Lyapunov-Like Divergence (Approximate)

Construct a nearby sequence:

b₁ = a₁ = 1
b₂ = a₂ + 1 # extremely tiny artificial perturbation


Run:

δₙ = |aₙ − bₙ|


Plot log(δₙ) vs n.

If it fits: 

log δₙ ≈ λn


Then λ > 0 suggests chaotic divergence.

---

## 4. Periodicity Tests

This detects whether HashHelix ever “locks” into cycles.

### 4.1 Floyd Cycle-Finding (Tortoise & Hare)

Perform for several windows:
- n ∈ [1…50k]
- n ∈ [100k…200k]
- n ∈ [500k…1M]

A true cycle would show:

aᵢ = aⱼ and the following k steps match

### 4.2 Sliding Window Hashes

Hash consecutive windows:

H(n) = SHA256( aₙ … aₙ₊₂₅₅ )


If any H(n) repeats → likely periodic structure.

So far, no cycles have been found in any known tests.

---

## 5. Plot Suite (Recommended Outputs)

### A. Distribution Plot  
Value frequencies across N.

### B. Time Series  
n vs aₙ  
Shows envelopes, drift, or chaotic banding.

### C. Autocorrelation Graph  
Decorrelates quickly → chaotic  
Decorrelates slowly → structured

### D. FFT Spectrum  
Sharp lines → periodic  
Broadband → chaotic  
Mixed → quasi-chaotic

### E. Divergence Graph (Lyapunov)  
log δₙ vs n  
Slope → approximate λ

---

## 6. Reporting Structure (for reproducibility)

If a contributor runs this test, they should report:

- N (sequence length)
- seed used
- hardware
- OS
- language/runtime 
- math precision  
- key findings:
  - entropy value  
  - autocorrelation decay  
  - presence/absence of periodicity  
  - FFT character  
  - divergence behavior  

This ensures the scientific community can reproduce and inspect results.

---

## 7. Status

This is **Experiment #4** in the HashHelix research suite.

Subsequent experiments will extend this into:
- fixed-point arithmetic
- integer-only CORDIC models
- precision sensitivity
- adversarial perturbation testing


