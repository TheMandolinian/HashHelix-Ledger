nano ORBIT_PORTRAITS.md <<'EOF'
# Orbit Portraits — Single-Lane HashHelix Behavior

**Purpose:**  
Explore how a *single* HashHelix lane behaves over time:
- Does it grow without bound?
- Does it stay in a chaotic band?
- Does it show signs of periodicity?
- How does it “look” when plotted?

This is a **purely mathematical experiment** on the core recurrence.

---

## 1. Recurrence Definition

We use the public HashHelix temporal primitive:

$$
a_1 = 1,\quad
a_n = \left\lfloor n \cdot \sin(a_{n-1} + \pi / n) \right\rfloor + 1
$$

Where:

- $a_n$ is an integer state at step $n$
- $n$ is the step index (starting at 1)
- `sin` is the usual sine function (radians)
- `floor` is the greatest integer ≤ the input

For this experiment, we focus on **one lane**:
- one sequence
- one seed
- no chiral twin yet

---

## 2. Basic Experiment Setup

### 2.1 Parameters

Choose:

- **Seed:** $a_1 = 1$ (default)
- **Length:** 5,000–50,000 steps (start with 5,000)
- **Precision:** use at least `float64` if using floating-point trig

### 2.2 Pseudocode (Language-Agnostic)

a = 1.0
record afor n from 2 to N:
    a = floor( n * sin(a + pi / n) ) + 1
    record a as integer


You can implement this in: Python • Rust • C/C++ • Java • JavaScript • any language with sin, floor, and π

---

## 3. What to Look For

Once you have the sequence $a_n$, analyze:

### 3.1 Growth

Does $|a_n|$ tend to grow, shrink, or stay bounded?

Plot `n vs a_n` and inspect:
- Does it look like a band?
- Does it trend upward?
- Does it oscillate wildly?

### 3.2 Oscillation and Structure

- Do you see repetitive “motifs”?
- Are there visible layers, bands, or envelopes?
- Does the sequence appear chaotic or regular?

### 3.3 Periodicity (Cycles)

Do any exact cycles appear over the sampled window?

You can test for short cycles by checking if:
- any subsequence repeats exactly
- or if $a_n$ returns to an earlier value with the same local context

> So far, HashHelix has behaved like a **chaotic, non-periodic map** in tested ranges (up to n ≥ 100,000), but this experiment lets others confirm or challenge that.

---

## 4. Suggested Plots

Generate one or more of these:

1. **n vs aₙ**  
   Standard time-series plot  
   → x-axis: n y-axis: aₙ

2. **aₙ vs aₙ₊₁**  
   Phase-space style plot  
   → useful for visualizing attractors in chaotic maps

3. **(n mod 360, aₙ mod 100)**  
   Quick way to see “helix-like” structures in a bounded window  
   → gives a visual “fingerprint” of the lane

Any of these can be included in future research/tools/helper scripts.

---

## 5. Reproducibility Notes

To ensure experiments can be reproduced, always specify:

- Language and version (e.g., Python 3.12)
- Math library (e.g., standard `math` in Python)
- Number type (e.g., `float64`)
- Seed and exact recurrence form

If you find something interesting (e.g., apparent cycle, strange pattern):

Record:
- seed
- N (number of steps)
- environment details
- optionally, share a snippet or plot via issue/PR

---

## 6. Future Extensions

This orbit portrait experiment is the foundation for:

- Multi-lane drift experiments
- Chiral twin comparisons (+π/n vs −π/n)
- Entropy and chaos analysis (Lyapunov exponents, NIST tests)
- Fixed-point / integer-only implementations

Those experiments will each get their own file under:  
`research/experiments/`

and may reuse the same basic recurrence and plotting patterns.

EOF
