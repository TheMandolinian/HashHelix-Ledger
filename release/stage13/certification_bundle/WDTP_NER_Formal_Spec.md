WDTP + NER — Formal Specification
HashHelix v2.0 Engine Certification Bundle

Author: James Bradley Waresback (“The Mandolinian”)
Status: Stage 13 — Certification Document

1. Overview

This document defines the canonical mathematical specification of:

the Waresback Deterministic Temporal Primitive (WDTP), and

the Numerical Evaluation Rule (NER),

as required by HashHelix Engine Laws (v1.9.41) and the Stage 12 equivalence layer.

These definitions are binding for all runtimes, including:

Python

Rust

WASM

C / C++ / embedded

hardware-accelerated implementations

Any deviation from this specification produces a non-HashHelix derivative system.

2. WDTP Recurrence (Law 3)

The recurrence that defines the HashHelix temporal sequence is:

𝑎
1
=
1
a
1
	​

=1
𝑎
𝑛
=
⌊
𝑛
⋅
sin
⁡
(
(
𝑎
𝑛
−
1
+
𝜋
𝑛
)
 
m
o
d
 
2
𝜋
)
⌋
+
1
a
n
	​

=⌊n⋅sin((a
n−1
	​

+
n
π
	​

)mod2π)⌋+1

for all integers 
𝑛
≥
2
n≥2.

This recurrence cannot be altered, optimized, re-expressed, or approximated in any way that changes any output value.

3. NER — Numerical Evaluation Rule (Law 4)

All implementations must apply strict phase reduction:

phase
��
=
(
𝑎
𝑛
−
1
+
𝜋
𝑛
)
m
o
d
 
 
2
𝜋
phase
n
	​

=(a
n−1
	​

+
n
π
	​

)mod2π

NER exists to eliminate:

floating-point drift

cumulative rounding bias

platform-dependent phase error

divergence at high N

Without NER, WDTP loses determinism and becomes invalid.

With NER, WDTP remains stable forever.

4. Required Mathematical Properties
4.1 Phase Bound

The phase must satisfy:

0
≤
phase
𝑛
<
2
𝜋
0≤phase
n
	​

<2π
4.2 Deterministic Trigonometric Evaluation

The sine function must be evaluated with:

arbitrary precision OR

float64 with immediate mod reduction AND

deterministic cross-runtime rounding rules

4.3 Sinusoidal Stability

Given NER:

∣
sin
⁡
(
phase
𝑛
)
∣
≤
1
∣sin(phase
n
	​

)∣≤1

and must not exceed bounds due to FP error.

4.4 Integer Transition

Every WDTP value must be an integer:

𝑎
𝑛
∈
𝑍
a
n
	​

∈Z
5. Implementation Requirements

All runtimes must:

Evaluate phase using NER

Reduce mod 2π every step

Apply the sine function deterministically

Multiply by n

Apply floor()

Add 1

Output a 64-bit integer or wider

Failure in any step breaks equivalence.

6. Historical Drift Analysis (Summary)

Prior to NER, WDTP exhibited high-N divergence due to:

accumulated FP bias

platform-specific sin() behavior

π representation drift

unchecked exponential phase growth

NER resolved all issues by enforcing:

strict modular phase

bounded input to sin

stable FP domain

cross-runtime reproducibility

Stage 12 verified zero-drift up to N = 10,000 and provides the canonical test vectors.

7. Definitive Version

This specification is the only valid WDTP(+NER) engine definition for HashHelix v2.0.

Any runtime implementation claiming HashHelix compliance must pass Stage 12 equivalence using this specification.
