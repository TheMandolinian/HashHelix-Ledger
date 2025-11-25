#!/usr/bin/env python3
"""
Stage 12 — Canonical Test Vector Generator
HashHelix Ledger — WDTP + NER Deterministic Truth Tables
Author: James Bradley Waresback (“The Mandolinian”)
"""

import json
import math
import hashlib
from pathlib import Path

# -------------------------------
# NER Phase Reduction
# -------------------------------
def wdtp_step(a_prev, n):
    """
    WDTP recurrence with strict NER:
    a[n] = floor( n * sin( (a[n-1] + π/n) mod 2π ) ) + 1
    """
    phase = (a_prev + math.pi / n) % (2 * math.pi)
    return int(math.floor(n * math.sin(phase))) + 1


# -------------------------------
# Test Vector Builder
# -------------------------------
def build_vectors(N=10000, lanes=[1, 2, 4, 21]):
    """
    Generate canonical WDTP(+NER) sequences and SHA-256 transitions.
    """
    vectors = {}

    # Initial seed
    a_prev = 1

    for n in range(1, N + 1):
        a_n = wdtp_step(a_prev, n)

        # SHA-256 transition state over tuple
        state_tuple = f"{n}|{a_prev}|{a_n}".encode()
        sha = hashlib.sha256(state_tuple).hexdigest()

        vectors[n] = {
            "n": n,
            "a_prev": a_prev,
            "a_n": a_n,
            "sha256": sha,
        }

        a_prev = a_n

    # Lane configurations (simple deterministic slicing)
    lane_outputs = {}
    for L in lanes:
        step = max(1, N // L)
        lane_outputs[str(L)] = [
            vectors[i]["a_n"] for i in range(1, N + 1, step)
        ]

    return vectors, lane_outputs


# -------------------------------
# JSON Serialization (Stage 5/6/7 Schema)
# -------------------------------
def write_json(vectors, lane_outputs, outdir):
    outdir.mkdir(parents=True, exist_ok=True)

    truth_file = outdir / "wdtp_vectors.json"
    lanes_file = outdir / "lane_vectors.json"

    print(f"[Stage 12] Writing {truth_file}")
    truth_file.write_text(json.dumps(vectors, indent=2))

    print(f"[Stage 12] Writing {lanes_file}")
    lanes_file.write_text(json.dumps(lane_outputs, indent=2))


# -------------------------------
# Main
# -------------------------------
def main():
    root = Path(__file__).resolve().parent.parent / "test_vectors"
    vectors, lane_outputs = build_vectors()
    write_json(vectors, lane_outputs, root)
    print("[Stage 12] Test vector generation complete.")


if __name__ == "__main__":
    main()
