# Experiment #4 — “How Far Can We Push Before It Lies?” (NER Edition)
HashHelix Research Suite 
Status: Active — NER-Compliant High-N Stress Framework

---

## Purpose
This experiment measures the numerical stability of the WDTP recurrence *under the Numerical Evaluation Rule (NER)* at very large step counts (N = 1M → 100M+).

**Before NER**, the recurrence was vulnerable to floating-point decay, phase drift, and cross-language divergence.

**With NER**, the sequence becomes mathematically deterministic and suitable for:

- Cross-hardware determinism tests 
- Cross-language replay (Python → Rust → WASM) 
- High-N stress behavior 
- Pathology detection 
- Scientific reproducibility 

This experiment establishes the **NER stability envelope** for HashHelix.

---

## 1. Recurrence (NER-Compliant)

The recurrence is:

\[
a_1 = 1,\qquad
a_n = \left\lfloor n \cdot \sin(\theta_n) \right\rfloor + 1
\]

Where the phase is evaluated with:

\[
\theta_n = (a_{n-1} + \pi/n) \bmod 2\pi
\]

This equation is **LAW 4 — The Numerical Evaluation Rule (NER)**.

NER prevents long-range drift and ensures *mathematical invariance* across:

- languages 
- OS 
- CPU architectures 
- different floating-point implementations 

---

## 2. Execution Modes

To avoid catastrophic slowdowns observed in earlier experiments, the modern NER engine uses two modes.

### **2.1 Truth Mode (Rev-E)**
Engine-only recurrence. No instrumentation.

- No entropy windows 
- No rolling deques 
- No per-step logging 
- No pathology detectors firing in loop 
- No file writes except final summary 

Used for:
- High-N stress tests (10M → 100M → 500M → 1B) 
- Determinism verification 
- Replay equivalence (Python, Rust, WASM) 

Performance:
- **50M steps in ~25 seconds** on standard hardware 
- Linear time complexity, minimal memory

Truth Mode produces the *ground-truth WDTP sequence*.

---

### **2.2 Instrumentation Mode**
Same recurrence, but with analysis tools enabled:

- Shannon entropy windows 
- Entropy collapse detectors 
- Drift monitors 
- Oscillation/phase analysis 
- Pathology signatures 
- Rolling statistics 
- Diagnostic log files 

Used for:
- Scientific characterization 
- Visual signatures 
- Detecting anomalies 
- Entropy decay or clustering 

Performance:
- Significantly slower (10×–500× depending on tools) 
- Not used for high-N final values 

---

## 3. What To Analyze

### **3.1 Determinism**
Truth Mode must produce *identical* outputs for:

- multiple runs 
- different Python versions 
- different OS 
- different CPUs 
- Rust → WASM → Python cross-checks 

Any deviation indicates:
- an implementation violation 
- a floating-point inconsistency 
- or a NER failure 

---

### **3.2 Stability & Pathologies**
Check for:

- boundary clustering 
- phase-flip storms 
- unexpected flattening 
- anomalous growth events 
- oscillation bands 
- entropy collapse 

These should appear **only** in Instrumentation Mode visualizations.

---

### **3.3 Entropy & Complexity**
In Instrumentation Mode:

- sliding entropy 
- autocorrelation 
- FFT signatures 
- variation density 
- “burst regions” 

All help characterize WDTP behavior, but do **not** affect truth mode output.

---

## 4. Performance History & Fix

Early versions (pre-NER, pre-mode-split):

- 5M steps → 10–15 minutes 
- 50M steps → 1+ hour 

Main causes:
- enormous entropy windows 
- rolling deques over 1M+ entries 
- per-iteration file writes 
- constant pathology detector triggers 
- logging every iteration 
- no separation between truth vs instrumentation 

**Fix:** fully separate Truth Mode and Instrumentation Mode.

Result:
- **50M steps in ~25 seconds** 
- stable output across hardware 
- reproducible final values 

---

## 5. Cross-Language Determinism Roadmap

Truth Mode outputs at fixed checkpoints will be validated in:

- Python (canonical)
- Rust (NER-compliant, libm or sleef)
- WASM (deterministic fp mode)
- C / C++ (libm)
- Possibly CUDA or FPGA later

Checkpoints:
- N = 1M 
- N = 10M 
- N = 50M 
- N = 100M 

Exact agreement is required.

---

## 6. Files for This Experiment (NER Edition)

Truth Mode runner: 
- `/benchmarks/exp01B_orbit_10M.py` (to be upgraded for Exp 3b)

Instrumentation Mode tools: 
- `/research/experiments/entropy_diagnostics.md`
- `/research/experiments/chaos_entropy_analysis.md`
- `/research/experiments/visual_signatures.md`

This document you are reading serves as the **official NER edition** of Experiment #4.

---

## 7. Status

- Old (pre-NER) version preserved at 
  `how_far_can_we_push_preNER.md` 
- This file now represents the **modern, NER-compliant, Rev-E** version
- Linked directly to:
  - Experiment 3b 
  - Stability and pathologies research 
  - Stage 10 engine binding 
  - Stage 11 canonical API export 

---

END OF FILE

