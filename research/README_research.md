# HashHelix Research & Experiments

This folder collects **open scientific experiments, diagnostics, and visualizations**
for the HashHelix temporal engine.

The goal is to make it easy for anyone to:

- Inspect the behavior of the core recurrence
- Reproduce numerical experiments
- Explore chaos, drift, and stability across lanes
- Validate claims about determinism and performance

This directory is **math & science only**. It does **not** contain:

- Tokenomics details
- Business rules
- Pricing models
- Institutional contracts

Those remain private by design. Everything here is safe, open research.

---

## Layout

Planned structure:

- `research/README_research.md`  
  Overview of the research space (this file).

- `research/experiments/`
  - Self-contained experiment guides (what to test, what to look for, how to reproduce).

- `research/tools/` *(planned)*
  - Optional helper scripts for plotting, lane comparison, and diagnostics.

- `research/science_notes/` *(planned)*
  - Background notes on deterministic temporal maps, chaos, and verification ideas.

---

## Core Recurrence (Reference Only)

All experiments in this folder are based on the public HashHelix temporal primitive:

\[
a_1 = 1,\quad
a_n = \left\lfloor n \cdot \sin(a_{n-1} + \pi / n) \right\rfloor + 1
\]

- Each **lane** is a separate instance of this recurrence.
- Experiments vary how long we run, how we seed lanes, and what we visualize.

For chiral extensions, we sometimes consider:

- Forward strand: \( a_n^+ = \lfloor n \cdot \sin(a_{n-1}^+ + \pi / n) \rfloor + 1 \)
- Reverse strand: \( a_n^- = \lfloor n \cdot \sin(a_{n-1}^- - \pi / n) \rfloor + 1 \)

But every experiment file will restate what it needs locally so readers don’t have to chase definitions.

---

## How to Use This Folder

If you’re exploring HashHelix:

1. Start with `research/experiments/orbit_portraits.md`  
   to see how a single lane behaves over time.

2. Follow future experiment guides as they’re added:
   multi-lane drift, chiral behavior, entropy analysis, etc.

3. If you implement the experiments in your own language or environment,
   feel free to open an issue or PR with:
   - plots
   - observations
   - corrections
   - new experiment ideas

This is the **open lab notebook** for the HashHelix engine.
