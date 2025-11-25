"""
HashHelix Stage 11 — Canonical WDTP Reference Engine (Python)

Engine-only. No relic / business logic.
LAW 4 (NER) binding:
    phase = (a_{n-1} + pi/n) mod 2pi
"""

from __future__ import annotations
import math
from typing import Iterator, List, Optional


TAU = math.tau  # 2*pi


def ner_phase(prev_a: int, n: int) -> float:
    """
    Numerical Evaluation Rule (LAW 4):
    Reduce phase mod 2π before sin() to prevent drift.
    """
    # phase_raw = prev_a + pi/n
    phase_raw = prev_a + (math.pi / n)
    # Reduce mod 2π deterministically
    return math.fmod(phase_raw, TAU)


def wdtp_step(prev_a: int, n: int) -> int:
    """
    Single WDTP step.
    a_n = floor(n * sin(phase)) + 1
    with NER-compliant phase reduction.
    """
    if n < 2:
        raise ValueError("n must be >= 2")
    phase = ner_phase(prev_a, n)
    return math.floor(n * math.sin(phase)) + 1


def wdtp_sequence(n_max: int, a1: int = 1) -> List[int]:
    """
    Generate WDTP sequence [a1, a2, ..., a_nmax].
    """
    if n_max < 1:
        raise ValueError("n_max must be >= 1")
    seq = [a1]
    prev = a1
    for n in range(2, n_max + 1):
        prev = wdtp_step(prev, n)
        seq.append(prev)
    return seq


def wdtp_iter(start_n: int = 2, a1: int = 1) -> Iterator[int]:
    """
    Infinite generator of WDTP values starting at a1, yielding a1, a2, ...
    """
    if start_n < 2:
        raise ValueError("start_n must be >= 2")
    prev = a1
    yield prev  # a1
    n = start_n
    while True:
        prev = wdtp_step(prev, n)
        yield prev
        n += 1


def wdtp_prefix_hash(n_max: int, a1: int = 1) -> str:
    """
    Convenience for equivalence tests:
    Returns a stable hex digest of the first n_max terms.
    (SHA-256 of comma-joined ints)
    """
    import hashlib
    seq = wdtp_sequence(n_max, a1=a1)
    blob = ",".join(map(str, seq)).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


if __name__ == "__main__":
    # quick smoke
    print(wdtp_sequence(20))
    print("hash20:", wdtp_prefix_hash(20))

