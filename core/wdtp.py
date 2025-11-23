"""
core/wdtp.py
Canonical Waresback Deterministic Temporal Primitive (WDTP)
with Numerical Evaluation Rule (NER) enforcement.

LAW 4 — Numerical Evaluation Rule (binding):
phase = (a_prev + π/n) mod 2π
a_n   = floor(n * sin(phase)) + 1
"""

from __future__ import annotations
import math
from typing import Union

Number = Union[int, float]

TAU = 2.0 * math.pi  # 2π

def wdtp_next(a_prev: int, n: int) -> int:
    """
    Compute next WDTP term with NER enforced.

    Args:
        a_prev: previous integer state a_{n-1}
        n: step index (n >= 1)

    Returns:
        a_n as int
    """
    # NER: reduce phase modulo 2π before sin evaluation
    phase = (a_prev + (math.pi / n)) % TAU
    return math.floor(n * math.sin(phase)) + 1


def wdtp_next_chiral(a_prev: int, n: int, sign: int = +1) -> int:
    """
    Chiral twin version (for ± helices) with NER enforced.

    sign = +1 for forward helix, -1 for reverse helix.
    """
    phase = (a_prev + sign * (math.pi / n)) % TAU
    return math.floor(n * math.sin(phase)) + 1
