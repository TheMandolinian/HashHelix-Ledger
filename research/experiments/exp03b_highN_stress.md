# Experiment 3b — High-N Stress Test & NER Verification  
HashHelix Research Suite 
Status: Active — Phase 2 (“Will it blow up at scale?”)

---

## Purpose  
Experiment 3b evaluates **numerical stability, determinism, and pathological behavior** of the WDTP recurrence **after the adoption of NER (Numerical Evaluation Rule)**.

This experiment directly answers the question:

> **“How far can the system be pushed before it lies?”**

Using both Truth Mode and Instrumentation Mode, we measure whether the recurrence remains stable, deterministic, and drift-free up to **10M → 50M → 100M → 500M steps**, and eventually **1B** on capable hardware.

This is the experiment that validates the **mathematical correctness** of the HashHelix Engine.

---

## 1. Recurrence Under Test (NER-Compliant)

\[
a_1 = 1,\qquad
a_n = \left\lfloor n \cdot \sin(\theta_n) \right\rfloor + 1
\]

Where the phase is defined by LAW 4 — NER:

\[
\theta_n = (a_{n-1} + \pi/n) \bmod 2\pi
\]

**NER is mandatory.** 
Without phase-modulo at every iteration, drift appears beyond ~500k steps.

---

## 2. Execution Modes

To avoid catastrophic slowdowns, Experiment 3b is executed in two distinct modes.

### **2.1 Truth Mode (Rev-E)**  
Pure recurrence. 
No instrumentation. 
No entropy. 
No drift detectors. 
No file writes inside the loop. 
No rolling windows. 

Used for: 
- 1M → 500M → 1B step stress tests 
- Python → Rust → WASM replay equivalence 
- Hardware stability and reproducibility 
- Cross-language determinism 

Performance: 
- **50M steps in ~25 seconds** on modest hardware 
- Linear memory footprint 
- Zero drift under NER

Truth Mode generates the ground-truth WDTP sequence.

---

### **2.2 Instrumentation Mode**  
Same recurrence, but with analysis features enabled:

- Shannon entropy (sliding or block-based) 
- Drift & divergence detectors 
- Oscillation patterns 
- Pathology signatures 
- Rolling statistical windows 
- Visual signature data export 
- Periodicity scanning 
- FFT analysis 

Used for: 
- scientific research 
- visual characterization 
- anomaly detection 
- identifying numerical “stress regions” 

Instrumentation Mode is **not** used to determine final WDTP values due to heavy overhead.

---

## 3. Target N Values

Truth Mode: 
- **N = 1,000,000** (baseline) 
- **N = 10,000,000** 
- **N = 50,000,000** 
- **N = 100,000,000** 
- **N = 500,000,000** (stretch goal) 
- **N = 1,000,000,000** (HPC only)

Instrumentation Mode: 
- Run up to 1M–5M only (due to heavy processing) 

---

## 4. Stability & Pathology Checklist

Experiment 3b monitors for:

### **4.1 Drift**  
- Any deviation from known checkpoints 
- Cross-run nondeterminism 
- Python vs Python mismatch 
Drift is **not allowed** under NER.

### **4.2 Phase Behavior**  
- Stability of (aₙ₋₁ + π/n) mod 2π 
- Boundary clustering 
- Unexpected phase transitions 

### **4.3 Pathological Regions**  
- phase-flip storms 
- unexpected value plateaus 
- anomalous growth events 
- entropy collapse zones 

### **4.4 Cross-Hardware Divergence**  
Truth Mode must match: 
- Windows 
- macOS 
- Linux 
- ARM vs Intel 
- cloud machines 

### **4.5 Cross-Language Replay**  
Truth Mode must produce identical results with: 
- Python (canonical) 
- Rust (NER engine) 
- WASM (deterministic FP) 
- C / libm 

Replay failure = engine violation.

---

## 5. Logging, Output & Checkpoints

Truth Mode logs: 
- N reached 
- a[n] final value 
- sparse checkpoints (optional: N/100, N/10) 
- runtime 
- hardware info 

Instrumentation Mode logs: 
- entropy windows 
- oscillation metrics 
- statistical signatures 
- any pathology detections 
- optional CSV series 

---

## 6. Expected Results (NER Behavior)

Under correct NER implementation:

- **Drift = 0** 
- **Cross-run difference = 0** 
- **Cross-hardware difference = 0** 
- **Cross-language difference = 0** 

The system should not “lie” at any N, regardless of scale.

Without NER, divergence begins around: 
- ~300k–600k depending on hardware. 
This experiment verifies that NER fully eliminates that decay.

---

## 7. File Locations & Code

High-N truth-mode runner lives in:

```
/benchmarks/exp01B_orbit_10M.py
```

This file will be upgraded and re-tagged for Experiments 3a/3b.

Instrumentation Mode tools live in:

```
/research/experiments/entropy_diagnostics.md
/research/experiments/visual_signatures.md
/research/experiments/chaos_entropy_analysis.md
```

Experiment 3b links **directly** to Stage 10 and Stage 11.

---

## 8. Status

Experiment 3b is now the **canonical** large-scale stability test for the NER-compliant HashHelix Engine.

- Experiment 3a = Phase-Space Signature 
- **Experiment 3b = High-N Stress & NER Verification** 
- Experiment 4 = “How Far Can We Push Before It Lies?” (NER Edition)

---

---

## 9. Recorded Checkpoints (Python, Codespaces)

### 9.1 Local Run #1 — N = 10,000,000 (Truth Mode, NER)

- Timestamp (UTC): 2025-11-24 01:05:01
- Environment: GitHub Codespaces (HashHelix-Ledger main)
- Language: Python (NER truth-mode runner)
- Script: `benchmarks/exp01B_orbit_10M.py`
- Steps N: 10,000,000
- Final a_n: -4,035,155
- Min a_n observed: -9,999,032
- Max a_n observed: 9,999,312
- Elapsed time: 3.260 seconds
- Mode: Truth Mode (no entropy / no heavy instrumentation)

### 9.2 Local Run #2 — N = 50,000,000 (Truth Mode, NER)

- Timestamp (UTC): 2025-11-24 01:14:26
- Environment: GitHub Codespaces (HashHelix-Ledger main)
- Language: Python (NER truth-mode runner)
- Script: `benchmarks/exp01B_orbit_50M.py`
- Steps N: 50,000,000
- Final a_n: 28,099,265
- Min a_n observed: -49,998,740
- Max a_n observed: 49,998,962
- Elapsed time: 17.220 seconds
- Mode: Truth Mode (no entropy / no heavy instrumentation)

### 9.3 Local Run #3 — N = 100,000,000 (Truth Mode, NER)

- Timestamp (UTC): 2025-11-24 01:20:36
- Environment: GitHub Codespaces (HashHelix-Ledger main)
- Language: Python (NER truth-mode runner)
- Script: `benchmarks/exp01B_orbit_100M.py`
- Steps N: 100,000,000
- Final a_n: 96,395,114
- Min a_n observed: -99,999,782
- Max a_n observed: 99,999,573
- Elapsed time: 33.053 seconds
- Mode: Truth Mode (no entropy / no heavy instrumentation)

### 9.4 Local Run #4 — N = 1,000,000,000 (Truth Mode, NER)

- Timestamp (UTC): 2025-11-24 01:36:45
- Environment: GitHub Codespaces (HashHelix-Ledger main)
- Language: Python (NER truth-mode runner)
- Script: `benchmarks/exp01B_orbit_1B.py`
- Steps N: 1,000,000,000
- Final a_n: -713,750,954
- Min a_n observed: -999,999,538
- Max a_n observed: 999,998,777
- Elapsed time: 322.977 seconds
- Mode: Truth Mode (no entropy / no heavy instrumentation)
- Notes: 1B-scale determinism holds under NER with linear runtime scaling.

### 9.5 Local Run #5 — N = 1,000,000,000 (Truth Mode, NER) — Repeat Verification

- Timestamp (UTC): 2025-11-24 01:49:54
- Environment: GitHub Codespaces (HashHelix-Ledger main)
- Language: Python (NER truth-mode runner)
- Script: `benchmarks/exp01B_orbit_1B.py`
- Steps N: 1,000,000,000
- Final a_n: -713,750,954  (identical to Run #4)
- Min a_n observed: -999,999,538
- Max a_n observed: 999,998,777
- Elapsed time: 324.506 seconds
- Mode: Truth Mode (NER)
- Notes: Absolute determinism confirmed at 1B steps across repeated runs.


END OF FILE
