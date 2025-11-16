# HashHelix — Stage 3: Entropy & Pattern Analysis  
**Version:** Stage 3 Research Dossier  
**Author:** James Bradley Waresback  
**Date:** November 2025

---

## Overview

Stage 3 establishes the first complete **statistical fingerprint** of the HashHelix recurrence.  
The goal is to quantify the dynamical “shape” of HashHelix using:

- Multi-million-step entropy sequences  
- Combined distributions  
- Frequency histograms  
- Baseline comparisons  
- Statistical fingerprints unique to HashHelix  

All results are **fully deterministic** and **reproducible** by any external verifier.

---

# 1. Entropy Lanes (Stage 3A)

Three independent entropy lanes were generated using:

- Initial seed: `a₁ = 1`
- Recurrence: `aₙ = floor(n * sin(aₙ₋₁ + π/n)) + 1`
- Steps per lane: **2,000,000**
- Total values: **6,000,000**

Artifacts:


---

# 2. Combined Distribution (Stage 3B)

Script:


Artifacts:

- `data/entropy_value_histogram.json`
- `data/entropy_distribution.json`
- `data/entropy_distribution_ascii.txt`

Purpose:

- Establish the global distribution shape  
- Detect extreme-value clustering  
- Validate deterministic reproducibility  

---

# 3. Frequency Histogram (Stage 3C)

Script:


Results:

- Top-20 most frequent values  
- No overrepresented integers  
- Broad distribution with heavy tails  
- Near-perfect positive/negative balance  

Supports:  
HashHelix does **not** collapse into cycles within the tested window.

---

# 4. Entropy Distribution Profile (Stage 3D)

Script:


Key results (HashHelix):

- **Mean:** ~343.95  
- **Stddev:** ~817,174  
- **Positive:** 0.500  
- **Negative:** 0.500  
- **Zero:** 0.000  
- **Over 99% of values lie outside ±512**  

HashHelix shows a distinctly heavy-tailed shape unlike:

- Normal (Gaussian) noise  
- Logistic-map chaos  
- SHA-derived pseudo-random values  

---

# 5. Entropy Fingerprint vs Baselines (Stage 3E)

Script:


Artifacts:

- `data/entropy_fingerprint.json`
- `data/entropy_fingerprint_ascii.txt`

Baselines computed:

| Generator | Description |
|----------|-------------|
| **Uniform** | Random integers matching HH’s observed range |
| **Normal** | Gaussian integers matching HH mean/stddev |
| **Logistic-map** | Chaotic x→r x(1–x) values scaled to ints |
| **SHA-256** | Hash-based pseudorandom integers |

## Unique HashHelix Traits

- Perfect sign symmetry  
- Heavy-tail dominance  
- Non-Gaussian bucket occupancy  
- Non-chaotic central mass  
- Distinct from uniform noise  
- Fully reproducible  

Conclusion:  
HashHelix forms a **unique statistical profile** —  
*neither random, nor Gaussian, nor chaotic, nor cryptographically pseudo-random.*

---

# 6. Scientific Significance

### Deterministic Reproducibility  
Any researcher can reproduce sequences exactly from the seed, recurrence, and step count.

### Statistical Distinctness  
HashHelix differs fundamentally from:

- RNGs  
- Gaussian noise  
- Chaotic logistic maps  
- SHA-derived pseudorandom data  

### Heavy-Tailed Entropy  
Wide integer excursions without collapse back into a narrow band.

### Stability Across Lanes  
All entropy lanes converge to the same fingerprint.

---

# 7. Stage 3 Artifact Summary


---

# 8. Next Step — Stage 3G (Merge)

Stage 3 is now ready for PR/merge into the main branch.
