Developer Onboarding Guide — HashHelix v2.0 Engine
Deterministic Runtime Implementation Manual

Author: James Bradley Waresback (“The Mandolinian”)
Status: Stage 13 — Developer Package
Engine Version: v1.9.44 (Final Pre-Release)

1. Introduction

Welcome to the HashHelix Engine development ecosystem.

This guide provides all information needed to implement a compliant runtime in:

Rust

WASM

C / C++

embedded / hardware

any deterministic target environment

HashHelix is not a blockchain.
It is a deterministic temporal computation engine whose correctness depends on:

strict recurrence rules

strict NER application

strict JSON schema compliance

strict cross-runtime equivalence

Breaking any of these breaks the engine.

2. Engine Summary

The HashHelix engine is governed by:

WDTP Recurrence
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
/
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

+π/n)mod2π)⌋+1
NER (Numerical Evaluation Rule)
phase
=
(
𝑎
𝑛
−
1
+
𝜋
/
𝑛
)
m
o
d
 
 
2
��
phase=(a
n−1
	​

+π/n)mod2π

Python is the canonical reference implementation.
All other runtimes must match it exactly.

3. Required Reading Before Implementation

A new developer must read:

WDTP + NER Formal Spec

Drift Elimination Proof

Equivalence Proof Summary

Chiral & Epoch Architecture Summary

Schema Compliance Summary

Stage 10 External Engine Contract

Stage 11 WASM Engine Contract

These documents define the engine boundaries.

4. Stage 10 — Rust Engine Contract Summary

Rust engines must:

Accept JSON input:

{"n": <int>, "a_prev": <int>}


Output only:

{"a_n": <int>}


Avoid:

debug logs

printing multiple fields

nondeterministic metadata

environment-dependent behavior

Apply WDTP+NER exactly.

Rust must pass Stage 12 equivalence tests.

5. Stage 11 — WASM Engine Contract Summary

WASM engines must:

Take two positional integers:

wasm_runner <n> <a_prev>


Output a single integer, with no formatting:

57


Use deterministic math and strict NER.

Produce identical results to Python and Rust.

6. Stage 12 — Equivalence Layer Summary

Before merging any runtime into main, developers must:

Run the equivalence harness:

python3 verification/stage12_equivalence/python/equivalence_harness.py


Confirm PASS on:

recurrence values

SHA-256 transitions

lane behavior

epoch bundle integrity

Any mismatch = rejection.

7. Implementation Warnings
❌ Forbidden:

skipping mod 2π

approximating sin() without bounds

using random seeds

modifying schema structure

generating nondeterministic compression

logging to stdout

using floating-point libraries with nonstandard rounding

✔ Required:

deterministic FP or arbitrary precision

strict recurrence

exact JSON matches

unit tests using canonical vectors

8. Developer Checklist

Before submitting runtime code:

✔ NER implemented
✔ sin() deterministic in [0, 2π)
✔ Stage 12 vector match verified
✔ JSON contract compliance validated
✔ No debug/log noise
✔ Compression deterministic
✔ Chiral lane and epoch rules respected

If all checks pass → Runtime is HashHelix-compliant.

9. Contact File for Future Maintainers

Included in this directory:

Stage 10 contract

Stage 11 WASM contract

Stage 12 harness guide

Canonical test vectors path

New developers must follow these strictly.

END
