#!/usr/bin/env python3
"""
Singularity Stress Test v0

Runs the HashHelix π/n recursion for multiple lane patterns and
writes raw sequences into hh_tmp/singularity_tests.

This is a *playground* harness – it does NOT mutate the ledger.
"""

import math
import time
from pathlib import Path
from datetime import datetime


def helix_step(prev_a: int, n: int) -> int:
    """
    Canonical HashHelix recurrence:

        a_1 = 1
        a_n = floor(n * sin(a_{n-1} + π/n)) + 1
    """
    return math.floor(n * math.sin(prev_a + math.pi / n)) + 1


def run_lane(lane_id: int, steps: int) -> list[int]:
    """
    Run a single lane for `steps` iterations, returning the whole sequence.
    """
    seq = []
    a = 1  # Singularity v0: proto-core starts at 1
    for n in range(1, steps + 1):
        a = helix_step(a, n)
        seq.append(a)
    return seq


def main() -> None:
    # Where to stash raw outputs (git-ignored)
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    base_dir = Path("hh_tmp") / "singularity_tests" / f"singularity_v0_stress_{ts}"
    base_dir.mkdir(parents=True, exist_ok=True)

    # Lane pattern to play with
    lane_pattern = [1, 3, 7, 9, 12, 15, 18, 21]
    steps = 21000

    print("[SING] Singularity v0 Stress Test")
    print(f"[SING] Output directory: {base_dir}")
    print(f"[SING] Steps per lane: {steps}")
    print(f"[SING] Lane pattern: {lane_pattern}")
    print("")

    for lane in lane_pattern:
        print(f"[SING] Running lane {lane} × {steps} steps...")
        t0 = time.perf_counter()
        seq = run_lane(lane, steps)
        t1 = time.perf_counter()

        # Basic stats
        duration = t1 - t0
        tps = steps / duration if duration > 0 else float("inf")

        # Write raw sequence to text file
        out_file = base_dir / f"lane_{lane}_sequence.txt"
        with out_file.open("w", encoding="utf-8") as f:
            for value in seq:
                f.write(f"{value}\n")

        print(
            f"[SING] lane={lane:2d} done in {duration:7.3f}s "
            f"→ {tps:,.2f} steps/sec; last value = {seq[-1]}"
        )

    print("\n[SING] Stress test complete.")
    print("[SING] You can inspect sequences under:", base_dir)


if __name__ == "__main__":
    main()
