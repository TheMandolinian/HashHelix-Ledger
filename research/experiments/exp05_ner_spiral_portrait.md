# Experiment 5 — NER Spiral Portrait (WDTP Stability Snapshot)

**Author:** James Bradley Waresback  
**Date:** 2025-11-12  
**Status:** Draft

---

## Objective

Generate a visual “orbit portrait” of the WDTP sequence under the
Numerical Evaluation Rule (NER):

> phase = (a_{n-1} + π/n) mod 2π

This plot should be directly comparable to the original `spiral.png`
(pre-NER) to visually confirm that:

1. The global triangular envelope of WDTP is preserved under NER.
2. The phase-jitter artifacts along the upper edge become cleaner and
   more stable at high *n*.
3. The sequence continues to exhibit no visible short cycles or chaotic
   blow-up over the tested range.

---

## Setup

- Repository: `HashHelix-Ledger`
- Engine: Python reference WDTP implementation with NER
- Output: `spiral_ner.png` in the repo root
- Dependencies:
  - Python 3.x
  - `matplotlib` (for quick plotting)

---

## Parameters

- Initial value: `a₁ = 1`
- Recurrence with NER:

  - `phaseₙ = (aₙ₋₁ + π/n) mod 2π`
  - `aₙ = floor(n · sin(phaseₙ)) + 1`

- Range: `n = 1 … N`
- Suggested `N`: 500,000 (adjust as needed for performance)

---

## Procedure

1. Run the benchmark script:

   ```bash
   python "benchmarks/Experiment 5 — NER Spiral Portrait.py"
