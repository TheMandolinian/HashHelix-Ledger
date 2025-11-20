#!/usr/bin/env python3
"""
HashHelix — Stage 8
Stress Harness v2

Pipeline:
  lane_runtime.py  → lane traces
  epoch_auto.py    → WARM epochs + bundles
  relic_auto.py    → COLD relics

Checks:
  - Lane length / coverage
  - Epoch JSON vs lane traces (Merkle + seq hash)
  - Relic aggregate + chiral commitments
  - Optional corruption test (in-memory, no disk damage)

All deterministic, no randomness, no timestamps.
"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


# ---------- Shared hashing helpers ----------

def sha256_bytes(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def merkle_root_from_ints(values: List[int]) -> str:
    if not values:
        return hashlib.sha256(b"").hexdigest()
    layer = [sha256_bytes(str(v).encode("utf-8")) for v in values]
    while len(layer) > 1:
        next_layer: List[bytes] = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            if i + 1 < len(layer):
                right = layer[i + 1]
            else:
                right = left
            next_layer.append(sha256_bytes(left + right))
        layer = next_layer
    return layer[0].hex()


def sequence_hash_from_ints(values: List[int]) -> str:
    h = hashlib.sha256()
    for v in values:
        h.update(str(v).encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def merkle_root_from_hex(values: List[str]) -> str:
    if not values:
        return hashlib.sha256(b"").hexdigest()
    layer = [bytes.fromhex(v) for v in values]
    while len(layer) > 1:
        next_layer: List[bytes] = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            if i + 1 < len(layer):
                right = layer[i + 1]
            else:
                right = left
            next_layer.append(sha256_bytes(left + right))
        layer = next_layer
    return layer[0].hex()


def sha256_hex_of_strings(values: List[str]) -> str:
    h = hashlib.sha256()
    for v in values:
        h.update(v.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


# ---------- Utility ----------

def run_cmd(args: List[str]) -> None:
    print(f"[CMD] {' '.join(args)}")
    subprocess.run(args, check=True)


def load_lane_values(path: Path) -> List[int]:
    vals: List[int] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            vals.append(int(line))
    return vals


# ---------- Verification ----------

def verify_lane_lengths(lane_dir: Path, lanes: int, steps: int) -> None:
    print("[CHECK] Lane lengths")
    for lane_id in range(1, lanes + 1):
        lane_path = lane_dir / f"lane{lane_id:02d}.txt"
        if not lane_path.exists():
            raise AssertionError(f"Missing lane file: {lane_path}")
        count = sum(1 for _ in lane_path.open("r", encoding="utf-8"))
        if count != steps:
            raise AssertionError(
                f"Lane {lane_id}: expected {steps} steps, found {count}"
            )
    print("[OK] Lane lengths verified")


def verify_epochs_against_lanes(
    lane_dir: Path,
    epoch_dir: Path,
    lanes: int,
    epoch_length: int,
) -> None:
    print("[CHECK] Epochs vs lane traces")
    for lane_id in range(1, lanes + 1):
        lane_path = lane_dir / f"lane{lane_id:02d}.txt"
        lane_values = load_lane_values(lane_path)

        epoch_paths = sorted(
            epoch_dir.glob(f"epoch_lane{lane_id:02d}_ep*.json")
        )
        if not epoch_paths:
            raise AssertionError(f"No epochs for lane {lane_id}")

        for ep_path in epoch_paths:
            with ep_path.open("r", encoding="utf-8") as f:
                obj = json.load(f)

            start_step = obj["start_step"]
            end_step = obj["end_step"]
            step_count = obj["step_count"]
            merkle = obj["merkle_root"]
            seq_hash = obj["sequence_hash"]

            if end_step - start_step + 1 != step_count:
                raise AssertionError(
                    f"{ep_path}: inconsistent step range vs count"
                )
            if step_count != epoch_length:
                raise AssertionError(
                    f"{ep_path}: expected epoch_length={epoch_length}, "
                    f"found {step_count}"
                )

            # slice is 0-based, inclusive start, exclusive end
            segment = lane_values[start_step - 1:end_step]
            if len(segment) != step_count:
                raise AssertionError(
                    f"{ep_path}: segment length mismatch ({len(segment)})"
                )

            m2 = merkle_root_from_ints(segment)
            if m2 != merkle:
                raise AssertionError(
                    f"{ep_path}: merkle mismatch\n"
                    f"  stored : {merkle}\n"
                    f"  recomputed: {m2}"
                )

            s2 = sequence_hash_from_ints(segment)
            if s2 != seq_hash:
                raise AssertionError(
                    f"{ep_path}: sequence_hash mismatch\n"
                    f"  stored : {seq_hash}\n"
                    f"  recomputed: {s2}"
                )

    print("[OK] Epochs consistent with lane traces")


def verify_relics(relic_dir: Path) -> None:
    print("[CHECK] Relic aggregates + chiral commitments")

    relic_paths = sorted(relic_dir.glob("relic-ep*.json"))
    if not relic_paths:
        raise AssertionError(f"No relics found in {relic_dir}")

    for path in relic_paths:
        with path.open("r", encoding="utf-8") as f:
            relic = json.load(f)
        _verify_single_relic(relic, label=str(path))

    print("[OK] All relics verified")


def _verify_single_relic(relic: Dict, label: str = "<in-memory>") -> None:
    epoch_entries = relic.get("epoch_bundles", [])
    bundle_ids: List[str] = []
    bundle_merkle_roots: List[str] = []

    for entry in epoch_entries:
        bundle_id = entry["bundle_id"]
        lane_merkle_roots = entry["lane_merkle_roots"]
        bundle_merkle_root = entry["bundle_merkle_root"]

        # recompute bundle_merkle_root from lane_merkle_roots
        expected_bundle = merkle_root_from_hex(lane_merkle_roots)
        if expected_bundle != bundle_merkle_root:
            raise AssertionError(
                f"{label}: bundle_merkle_root mismatch for {bundle_id}\n"
                f"  stored : {bundle_merkle_root}\n"
                f"  recomputed: {expected_bundle}"
            )

        bundle_ids.append(bundle_id)
        bundle_merkle_roots.append(bundle_merkle_root)

    # aggregate relic merkle
    expected_relic_merkle = merkle_root_from_hex(bundle_merkle_roots)
    stored_relic_merkle = (
        relic.get("aggregate", {})
        .get("relic_merkle_root")
    )
    if expected_relic_merkle != stored_relic_merkle:
        raise AssertionError(
            f"{label}: relic_merkle_root mismatch\n"
            f"  stored : {stored_relic_merkle}\n"
            f"  recomputed: {expected_relic_merkle}"
        )

    # chiral commitments
    agg = relic.get("aggregate", {})
    chiral = agg.get("chiral_commitment", {})
    forward = chiral.get("forward")
    reverse = chiral.get("reverse")

    expected_forward = sha256_hex_of_strings(bundle_ids)
    expected_reverse = sha256_hex_of_strings(list(reversed(bundle_ids)))

    if forward != expected_forward:
        raise AssertionError(
            f"{label}: chiral forward mismatch\n"
            f"  stored : {forward}\n"
            f"  recomputed: {expected_forward}"
        )
    if reverse != expected_reverse:
        raise AssertionError(
            f"{label}: chiral reverse mismatch\n"
            f"  stored : {reverse}\n"
            f"  recomputed: {expected_reverse}"
        )


def corruption_test_one_relic(relic_dir: Path) -> None:
    """
    In-memory corruption test:
      - Load one relic
      - Tamper with first bundle_id
      - Expect verification to fail
    """
    relic_paths = sorted(relic_dir.glob("relic-ep*.json"))
    if not relic_paths:
        print("[SKIP] No relics for corruption test")
        return

    path = relic_paths[0]
    with path.open("r", encoding="utf-8") as f:
        relic = json.load(f)

    print(f"[TEST] Corruption check using {path}")

    # Deep copy via json round-trip
    corrupted = json.loads(json.dumps(relic))

    if not corrupted["epoch_bundles"]:
        print("[SKIP] No epoch_bundles in relic")
        return

    corrupted["epoch_bundles"][0]["bundle_id"] += "-CORRUPTED"

    try:
        _verify_single_relic(corrupted, label=f"{path} (corrupted)")
    except AssertionError as e:
        print("[OK] Corruption detected as expected:")
        print(f"      {e}")
    else:
        raise AssertionError(
            "Corruption test FAILED: tampering went undetected"
        )


# ---------- Orchestration ----------

def run_pipeline(args: argparse.Namespace) -> None:
    lane_dir = Path("data/runtime/stress_v2/lanes")
    epoch_dir = Path("epochs/stage8_stress_v2")
    relic_dir = Path("relics/stage8_stress_v2")

    lane_dir.mkdir(parents=True, exist_ok=True)
    epoch_dir.mkdir(parents=True, exist_ok=True)
    relic_dir.mkdir(parents=True, exist_ok=True)

    # 1) Lanes
    run_cmd([
        "python", "scripts/lane_runtime.py",
        "--steps", str(args.steps),
        "--lanes", str(args.lanes),
        "--mode", args.mode,
        "--out-dir", str(lane_dir),
    ])

    # 2) Epochs
    run_cmd([
        "python", "scripts/epoch_auto.py",
        "--lane-dir", str(lane_dir),
        "--out-dir", str(epoch_dir),
        "--epoch-length", str(args.epoch_length),
        "--lanes", str(args.lanes),
    ])

    # 3) Relics
    run_cmd([
        "python", "scripts/relic_auto.py",
        "--epoch-dir", str(epoch_dir),
        "--out-dir", str(relic_dir),
        "--epochs-per-relic", str(args.epochs_per_relic),
    ])

    # 4) Verification
    verify_lane_lengths(lane_dir, args.lanes, args.steps)
    verify_epochs_against_lanes(lane_dir, epoch_dir, args.lanes, args.epoch_length)
    verify_relics(relic_dir)

    if args.corruption_test:
        corruption_test_one_relic(relic_dir)

    print("[DONE] Stress Harness v2 completed successfully")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="HashHelix Stage 8 — Stress Harness v2"
    )
    p.add_argument(
        "--lanes",
        type=int,
        default=4,
        help="Number of lanes (default: 4).",
    )
    p.add_argument(
        "--steps",
        type=int,
        default=1_000_000,
        help="Steps per lane (default: 1,000,000).",
    )
    p.add_argument(
        "--mode",
        choices=["sequential", "parallel"],
        default="parallel",
        help="Lane runtime mode (default: parallel).",
    )
    p.add_argument(
        "--epoch-length",
        type=int,
        default=100_000,
        help="Steps per epoch (default: 100,000).",
    )
    p.add_argument(
        "--epochs-per-relic",
        type=int,
        default=10,
        help="Epochs per relic (default: 10).",
    )
    p.add_argument(
        "--corruption-test",
        action="store_true",
        help="Enable in-memory corruption detection test.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    try:
        run_pipeline(args)
    except Exception as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
