#!/usr/bin/env python3
"""
Stage 12 — Canonical Equivalence Harness
HashHelix Ledger — Multi-Runtime Deterministic Verification
Author: James Bradley Waresback (“The Mandolinian”)
"""

import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime

# ------------------------------------------
# Load canonical test vectors
# ------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
TV_DIR = ROOT / "test_vectors"
REPORT_DIR = ROOT / "reports"

PY_TRUTH = TV_DIR / "wdtp_vectors.json"


# ------------------------------------------
# Python Reference Engine (local compute)
# ------------------------------------------
def run_python_reference(n, a_prev):
    """
    A tiny WDTP+NER reimplementation for spot-verification.
    Python is the ground truth.
    """
    import math
    phase = (a_prev + math.pi / n) % (2 * math.pi)
    return int(math.floor(n * math.sin(phase))) + 1


# ------------------------------------------
# Rust Engine — Stage 10 JSON Contract
# ------------------------------------------
def run_rust_engine(n, a_prev):
    """
    Calls the Rust engine via the Stage 10 external contract:
    rust_engine --json '{"n": ..., "a_prev": ...}'
    """
    payload = json.dumps({"n": n, "a_prev": a_prev})

    try:
        out = subprocess.check_output(
            ["./rust_engine", "--json", payload],
            text=True
        )
        result = json.loads(out)
        return result["a_n"]

    except Exception as e:
        return f"[RUST ERROR] {e}"


# ------------------------------------------
# WASM Engine — Stage 11 Contract
# ------------------------------------------
def run_wasm_engine(n, a_prev):
    """
    Calls WASM export through Stage 11 wrapper.
    Executed via: wasm_runner --n ? --prev ?
    """
    try:
        out = subprocess.check_output(
            ["./wasm_runner", str(n), str(a_prev)],
            text=True
        )
        return int(out.strip())

    except Exception as e:
        return f"[WASM ERROR] {e}"


# ------------------------------------------
# Equivalence Comparison
# ------------------------------------------
def verify_all():
    REPORT_DIR.mkdir(exist_ok=True)

    truth = json.loads(PY_TRUTH.read_text())
    timestamp = datetime.utcnow().isoformat()

    report_path = REPORT_DIR / f"Stage12_report_{timestamp}.txt"
    log = []

    log.append("Stage 12 — Canonical Equivalence Verification Report")
    log.append(f"Timestamp: {timestamp}")
    log.append("--------------------------------------------------------\n")

    failures = 0

    for n_str, entry in truth.items():
        n = int(entry["n"])
        a_prev = entry["a_prev"]
        expected = entry["a_n"]

        # Python
        py_val = run_python_reference(n, a_prev)

        # Rust
        rust_val = run_rust_engine(n, a_prev)

        # WASM
        wasm_val = run_wasm_engine(n, a_prev)

        # Compare
        if py_val != expected:
            failures += 1
            log.append(f"[FAIL] PYTHON MISMATCH @ n={n} py={py_val}, expected={expected}")

        if rust_val != expected:
            failures += 1
            log.append(f"[FAIL] RUST MISMATCH @ n={n} rust={rust_val}, expected={expected}")

        if wasm_val != expected:
            failures += 1
            log.append(f"[FAIL] WASM MISMATCH @ n={n} wasm={wasm_val}, expected={expected}")

        if failures == 0:
            log.append(f"[OK] n={n} all runtimes match")

    if failures == 0:
        log.append("\nALL RUNTIMES ARE CANONICALLY IDENTICAL. STAGE 12 PASSED.\n")
    else:
        log.append(f"\nFAILURES DETECTED: {failures}")
        log.append("STAGE 12 FAILED — Runtimes diverge.\n")

    report_path.write_text("\n".join(log))
    return report_path


# ------------------------------------------
# Main
# ------------------------------------------
def main():
    report = verify_all()
    print(f"[Stage 12] Verification complete.")
    print(f"Report written to: {report}")


if __name__ == "__main__":
    main()
