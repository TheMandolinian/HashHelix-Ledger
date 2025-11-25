BEGIN RUST CONTRACT DOC
Stage 12 — Rust Engine Contract (Stage 10 Interface)
HashHelix Ledger — Deterministic Runtime Equivalence

Author: James Bradley Waresback
Status: Binding for Stage 12 Verification

Purpose

This document defines exactly how the Rust engine must respond to Stage 12 calls so that the Python equivalence harness can verify deterministic parity.

Rust engine must implement the Stage 10 External Engine Contract:
rust_engine --json '{"n": ..., "a_prev": ...}'
Input Format

A single JSON object with two keys:
{
  "n": <integer>,
  "a_prev": <integer>
}
Both values must be integers.


Output Format (Required)
The Rust engine must print only the following JSON:
{
  "a_n": <integer>
}

Nothing else is allowed:

-no logs

-no debugging text

-no warnings

-no prefixes or suffixes

The output must be valid JSON, newline terminated.

Recurrence Requirement
Rust must compute:
phase = (a_prev + π/n) mod 2π
a_n = floor(n * sin(phase)) + 1

Where:

-sin(), π, and mod reduction must follow the Numerical Evaluation Rule (NER)
-arbitrary precision or controlled reduction is acceptable
-drift is forbidden

Determinism Requirement
For every test vector, Rust must match:

-Python reference engine
-WASM engine
-canonical truth tables in /test_vectors/wdtp_vectors.json

Matching is bit-for-bit.

Failure Conditions

Rust must not:

-output anything except valid JSON
-mutate global state
-rely on system time, randomness, or hardware entropy
-skip NER
-perform approximate sine without compensation
-diverge from Python

Any of the above results in Stage 12 failure.


OK Example Output
{"a_n": 57}

FAIL Example Output
a_n=57
**anything else**
logs, warnings, extra fields

END RUST CONTRACT DOC
