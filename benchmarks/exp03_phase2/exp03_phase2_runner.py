#!/usr/bin/env python3
"""
Experiment 3 — Phase 2 (Rev-E, Scientific Truth Mode)
HashHelix — WDTP Deterministic Core Recurrence Test
Numerical Evaluation Rule (NER) strictly enforced.

This experiment measures ONLY:
• True residue-lock onset (aₙ ≡ 209 mod 210)
• Post-lock survival
• Final summary for whitepaper reproducibility

Zero diagnostics, zero guessed thresholds, zero drift tests.
Pure recurrence. Pure truth.
"""

import math
import json
import csv
import os
import time

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
OUTPUT_DIR          = "benchmarks/exp03_phase2"
N_TARGET_FAST       = 50_000_000
MODULUS             = 210
EXPECTED_RESIDUE    = 209
CHECKPOINT_INTERVAL = 1_000_000

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# WDTP recurrence — CANONICAL form with mandatory mod 2π (NER)
# ----------------------------------------------------------------------
def next_a(n: int, a_prev: float) -> int:
    """
    WDTP:
        a₁ = 1
        aₙ = floor(n * sin((aₙ₋₁ + π/n) mod 2π)) + 1
    """
    phase = (a_prev + math.pi / n) % (2 * math.pi)
    return math.floor(n * math.sin(phase)) + 1

# ----------------------------------------------------------------------
# Phase 2 — Fast Mode (50M)
# ----------------------------------------------------------------------
def run_fast_mode():
    print("Rev-E: Scientific Truth Mode — Running to 50,000,000…")
    start = time.time()

    a = 1.0
    n = 1
    lock_onset = None
    violations_after_lock = 0

    checkpoints = []

    while n < N_TARGET_FAST:
        n += 1
        a = float(next_a(n, a))
        residue = int(a) % MODULUS

        # -------------------------------
        # RESIDUE-LOCK DETECTION LOGIC
        # -------------------------------
        if lock_onset is None:
            if residue == EXPECTED_RESIDUE:
                lock_onset = n
                print(f"*** LOCK ONSET at n={n:,} (a_n={int(a)}) ***")
        else:
            if residue != EXPECTED_RESIDUE:
                violations_after_lock += 1

        # -------------------------------
        # CHECKPOINT LOGGING
        # -------------------------------
        if n % CHECKPOINT_INTERVAL == 0:
            status = (
                f"locked since {lock_onset}"
                if lock_onset
                else "pre-lock"
            )
            print(f"checkpoint n={n:,} | a_n={int(a):,} | r={residue} | {status} | post-lock viol={violations_after_lock:,}")

            checkpoints.append((n, int(a), residue))

    elapsed = time.time() - start
    print(f"\nRev-E Complete in {elapsed:.1f}s")

    # -------------------------------
    # FINAL SUMMARY
    # -------------------------------
    summary = {
        "final_n": n,
        "lock_onset_n": lock_onset,
        "violations_after_lock": violations_after_lock,
        "transient_lock_duration": (n - lock_onset) if lock_onset else None,
        "elapsed_seconds": round(elapsed, 1),
    }

    with open(f"{OUTPUT_DIR}/revE_transient_locking_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    with open(f"{OUTPUT_DIR}/revE_checkpoints.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "a_n", "residue"])
        w.writerows(checkpoints)

    print("\n=== REV-E SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print("======================")

    print("\nRev-E completed successfully.")
    return summary

# ----------------------------------------------------------------------

if __name__ == "__main__":
    run_fast_mode()

