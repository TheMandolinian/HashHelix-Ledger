"""
Stage 11 — Cross-Language Replay Equivalence Harness (Python-led)

Contract:
...
"""

from __future__ import annotations

# Insert bootstrap *below* future import:
import os, sys
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import importlib
from dataclasses import dataclass
from typing import Callable, List, Optional

from engine.wdtp import wdtp_sequence, wdtp_prefix_hash


CANON_VEC_20 = [1, 2, 1, 4, -4, 2, 5, -6, 6, 1, 11, -11, 13, 9, 4, -13, -4, 12, -7, -10]
CANON_HASH_20 = "075b82498d4ed93704af351af363e2ff05ed20bbb212965974ceb80e7f86a699"


@dataclass
class EngineAdapter:
    name: str
    sequence_fn: Callable[[int, int], List[int]]  # (n_max, a1) -> list[int]
    prefix_hash_fn: Callable[[int, int], str]     # (n_max, a1) -> hex str


def python_adapter() -> EngineAdapter:
    return EngineAdapter(
        name="python",
        sequence_fn=lambda n_max, a1: wdtp_sequence(n_max, a1=a1),
        prefix_hash_fn=lambda n_max, a1: wdtp_prefix_hash(n_max, a1=a1),
    )


def try_load_rust_adapter() -> Optional[EngineAdapter]:
    """
    Stub: expects a future python-callable Rust binding module:
        engine.rust_bindings with:
            rust_wdtp_sequence(n_max:int, a1:int)->list[int]
            rust_wdtp_prefix_hash(n_max:int, a1:int)->str
    """
    try:
        m = importlib.import_module("engine.rust_bindings")
        return EngineAdapter(
            name="rust",
            sequence_fn=m.rust_wdtp_sequence,
            prefix_hash_fn=m.rust_wdtp_prefix_hash,
        )
    except Exception:
        return None


def try_load_wasm_adapter() -> Optional[EngineAdapter]:
    """
    Stub: expects a future wasm runner module:
        engine.wasm_runner with:
            wasm_wdtp_sequence(n_max:int, a1:int)->list[int]
            wasm_wdtp_prefix_hash(n_max:int, a1:int)->str
    """
    try:
        m = importlib.import_module("engine.wasm_runner")
        return EngineAdapter(
            name="wasm",
            sequence_fn=m.wasm_wdtp_sequence,
            prefix_hash_fn=m.wasm_wdtp_prefix_hash,
        )
    except Exception:
        return None


def assert_small_vector(adapter: EngineAdapter):
    seq20 = adapter.sequence_fn(20, 1)
    assert seq20 == CANON_VEC_20, f"{adapter.name} small-N vector mismatch"


def assert_prefix_hashes(adapter: EngineAdapter):
    ns = [20, 1_000, 100_000]
    for n in ns:
        h = adapter.prefix_hash_fn(n, 1)
        h_py = wdtp_prefix_hash(n, 1)
        assert h == h_py, f"{adapter.name} prefix hash mismatch at N={n}"


def assert_drift_1m(adapter: EngineAdapter):
    """
    Determinism / drift test.
    Adapter MUST match Python at N=1,000,000.
    (This is the LAW 4 / NER compliance check.)
    """
    n = 1_000_000
    h = adapter.prefix_hash_fn(n, 1)
    h_py = wdtp_prefix_hash(n, 1)
    assert h == h_py, f"{adapter.name} drift mismatch at N={n}"


def run_all():
    adapters = [python_adapter()]

    rust = try_load_rust_adapter()
    wasm = try_load_wasm_adapter()
    if rust: adapters.append(rust)
    if wasm: adapters.append(wasm)

    # Always validate canonical constants first
    assert wdtp_sequence(20, a1=1) == CANON_VEC_20, "python canonical vector changed"
    assert wdtp_prefix_hash(20, 1) == CANON_HASH_20, "python canonical hash changed"

    for ad in adapters:
        print(f"== {ad.name} ==")
        assert_small_vector(ad)
        assert_prefix_hashes(ad)
        # drift check only if non-python (python is definitionally canonical)
        if ad.name != "python":
            assert_drift_1m(ad)
        print("OK")

    print("\nAll Stage 11 equivalence checks passed.")


if __name__ == "__main__":
    run_all()
