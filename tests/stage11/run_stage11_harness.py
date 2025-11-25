"""
Stage 11 — Engine Test Harness Runner

Checks:
1) small-N canonical vector
2) mid-N determinism via prefix-hash repeatability
3) N=1,000,000 drift test (NER compliance)
"""

from __future__ import annotations

import os, sys, time

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from engine.wdtp import wdtp_sequence, wdtp_prefix_hash


CANON_VEC_20 = [1, 2, 1, 4, -4, 2, 5, -6, 6, 1, 11, -11, 13, 9, 4, -13, -4, 12, -7, -10]
CANON_HASH_20 = "075b82498d4ed93704af351af363e2ff05ed20bbb212965974ceb80e7f86a699"


def small_n_check():
    seq20 = wdtp_sequence(20, a1=1)
    assert seq20 == CANON_VEC_20, "small-N vector mismatch"
    h20 = wdtp_prefix_hash(20, 1)
    assert h20 == CANON_HASH_20, "small-N prefix hash mismatch"
    print("small-N check: OK")


def mid_n_determinism_check(n=100_000):
    """
    Determinism check: same run twice => same prefix hash.
    """
    h1 = wdtp_prefix_hash(n, 1)
    h2 = wdtp_prefix_hash(n, 1)
    assert h1 == h2, f"mid-N determinism failed at N={n}"
    print(f"mid-N determinism (N={n}) check: OK")


def drift_1m_check(n=1_000_000):
    """
    NER compliance guard:
    compares two independent runs at high N.
    Any drift indicates LAW-4 violation in an alt engine.
    """
    t0 = time.time()
    h1 = wdtp_prefix_hash(n, 1)
    t1 = time.time()
    h2 = wdtp_prefix_hash(n, 1)
    t2 = time.time()
    assert h1 == h2, f"drift detected at N={n}"
    print(f"N=1M drift check: OK (run1 {t1-t0:.2f}s, run2 {t2-t1:.2f}s)")


def main():
    print("Stage 11 harness starting...\n")
    small_n_check()
    mid_n_determinism_check()
    drift_1m_check()
    print("\nStage 11 harness complete: ALL OK")


if __name__ == "__main__":
    main()
