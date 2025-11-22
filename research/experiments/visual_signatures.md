nano research/experiments/visual_signatures.md <<'EOF'
# Experiment #2 — Visual Signatures of HashHelix
HashHelix Research Suite
Status: Active, Visualization-Based Structural Study

## Purpose
This experiment explores how HashHelix *looks* when projected into 2D visual spaces.
The goal is to discover recognizable structure, chaos, symmetry, and drift patterns.

These visual signatures help:
- identify characteristic “helix fingerprints”
- detect anomalies (periodicity, collapse, drift)
- compare different languages / precisions / seeds
- generate intuitive insight into the underlying dynamics

This experiment does **not** require huge N.
Most plots work beautifully with N = 5k–50k.

---

## 1. Recurrence

Use the standard forward recurrence:

\[
a_1 = 1,\quad
a_n = \left\lfloor n \cdot \sin(a_{n-1} + \pi/n) \right\rfloor + 1
\]

Compute at least:
- N = 5,000
- N = 10,000
- N = 25,000
(You may go higher if you want deeper structure.)

---

## 2. Visual Experiments

### 2.1 Time Series Plot  
**Plot:**
n vs aₙ 

This reveals:
- envelopes
- band structures
- oscillatory regions
- chaotic dispersion

It is the simplest and most diagnostic graph.

---

### 2.2 Phase-Space Plot  
**Plot:**
(aₙ, aₙ₊₁)

Often used in chaotic map analysis (logistic map, Henon map).

Look for:
- diagonal line clustering
- fan structures
- chaotic scattering
- bands / voids

These indicate whether HashHelix behaves like a strange attractor.

---

### 2.3 Modular Spiral Projection  
**Plot:**
(n mod 360, aₙ mod 100)

This is the “helix fingerprint” plot.

It visually compresses the sequence into:
- a circular angular dimension
- a radial band space

Look for:
- spiral arms
- star-like rays
- dense chaotic blooms

These patterns often persist across seeds and languages.

---

### 2.4 Delta Plot  
**Plot:**
n vs (aₙ₊₁ − aₙ)

This shows:
- local volatility
- high-frequency oscillation
- drift-to-chaos transitions

If the delta distribution begins clustering heavily, this may indicate precision collapse.

---

### 2.5 Chiral Separation Visualization  
(Optional if dual helix is computed)

**Plot:**
n vs |aₙ⁺ − aₙ⁻|

This reveals:
- whether chiral strands diverge
- periodic re-alignments
- chaotic sensitivity differences

Even small differences amplify over long n.

---

## 3. What to Look For

### 3.1 Structure  
Does the data form:
- smooth arcs?
- thick chaotic clouds?
- discrete bands?
- quasi-periodic lattices?

### 3.2 Repeating Motifs  
Look specifically for:
- “feathered” arcs
- diagonal streaks
- concentric shells
- star patterns

These indicate deep underlying structure.

### 3.3 Irregularities  
Sudden flattening or collapse may indicate:
- float precision limits
- implementation drift
- non-chaotic regime transitions

---

## 4. Reproducibility Notes

Record:
- N value
- seed
- language/runtime
- plot type
- math precision used (float64, float32, fixed-point)
- machine + CPU

Small changes can radically affect the look of chaotic projections.

---

## 5. Extensions

Future visualization tools may include:
- animated lane evolution
- chiral split animations
- 3D spiral embeddings
- cross-language visual drift comparisons
- “HashHelix fractal atlas” collections 

Visual signature analysis is one of the best tools for discovering hidden behavior, attractors, or stability regions.

---

## Status
This is Experiment #6 in the HashHelix research suite.
EOF
