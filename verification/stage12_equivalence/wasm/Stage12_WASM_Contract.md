BEGIN WASM CONTRACT DOC
Stage 12 — WASM Engine Contract (Stage 11 Interface)
HashHelix Ledger — Deterministic Runtime Equivalence

Author: James Bradley Waresback
Status: Binding for Stage 12 Verification

Purpose

This document defines exactly how the WASM runtime must behave for Stage 12 multi-runtime determinism verification.

The WASM engine is executed via the Stage 11 wrapper:

wasm_runner <n> <a_prev>

wasm_runner must call the WASM module with these two integers.

Input
Two positional integers:

n a_prev

Example:

wasm_runner 300 147

Output (Required)
WASM must output only:

<integer>

No JSON.
No extra text.
Just the number.

Example:

57

Recurrence Rule
WASM must compute:

phase = (a_prev + π/n) mod 2π
a_n = floor(n * sin(phase)) + 1

With strict NER:

-phase reduced mod 2π
-deterministic trig evaluation
-no floating-point drift allowed

Determinism Requirements

WASM output must match:
-Python reference
-Rust engine
-canonical test vectors

Matching is:
bit-for-bit identical

Forbidden Behaviors

-printing logs
-printing multiple lines
-returning floats
-any nondeterministic behavior
-using system entropy, timers, threads

OK Example Output

251

FAIL Example Output

Result = 251
[251]
251.0
anything else

END WASM CONTRACT DOC
