#!/usr/bin/env python3
"""
HashHelix — Stage 8
Epoch Automation Runtime

Takes lane trace files (from lane_runtime.py) and produces:

- Per-lane epoch artifacts (JSON)
- Per-epoch bundles referencing all lanes

Properties:
- Deterministic and reproducible
- No timestamps, no randomness
- WARM vault output only (epochs)
"""

import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Tuple


# ---------- Merkle Helpers ----------

def sha256_bytes(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def merkle_root_from_ints(values: List[int]) -> str:
    """
    Deterministic Merkle root:
    - Leaf = SHA256(str(v).encode('utf-8'))
    - Pair = SHA256(left || right)
    - Odd node duplicated at end of layer
    - Empty sequence → SHA256(b"")
    """
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
                right = left  # duplicate last if odd
            next_layer.append(sha256_bytes(left + right))
        layer = next_layer
    return layer[0].hex()


def sequence_hash_from_ints(values: List[int]) -> str:
    """
    Stable sequence hash:
    - SHA256 over decimal values with '\n' separators.
    """
    h = hashlib.sha256()
    for v in values:
        h.update(str(v).encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


# ---------- Core Epoch Logic ----------

def load_lane_values(lane_path: Path) -> List[int]:
    values: List[int] = []
    with lane_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            values.append(int(line))
    return values


def compute_epoch_stats(segment: List[int]) -> Dict[str, float]:
    if not segment:
        return {
            "min": 0,
            "max": 0,
            "mean": 0.0,
        }
    mn = min(segment)
    mx = max(segment)
    mean = sum(segment) / float(len(segment))
    return {
        "min": mn,
        "max": mx,
        "mean": mean,
    }


def generate_epochs_for_lane(
    lane_id: int,
    values: List[int],
    epoch_length: int,
    max_epochs: int,
    out_dir: Path,
) -> List[Tuple[int, Dict]]:
    """
    Slice a lane into fixed-length epochs and emit JSON files.

    Returns:
        List of (epoch_index, summary_dict) for bundle construction.
    """
    summaries: List[Tuple[int, Dict]] = []

    total_steps = len(values)
    if total_steps < epoch_length:
        # Not enough steps to form even one epoch → no output for this lane.
        return summaries

    num_epochs = total_steps // epoch_length
    if max_epochs > 0:
        num_epochs = min(num_epochs, max_epochs)

    for epoch_index in range(1, num_epochs + 1):
        start_idx = (epoch_index - 1) * epoch_length
        end_idx = start_idx + epoch_length
        segment = values[start_idx:end_idx]

        start_step = start_idx + 1
        end_step = end_idx

        merkle = merkle_root_from_ints(segment)
        seq_hash = sequence_hash_from_ints(segment)
        stats = compute_epoch_stats(segment)

        epoch_id = f"epoch-lane{lane_id:02d}-ep{epoch_index:04d}"

        epoch_obj = {
            # Stage 7 / Epoch schema alignment
            "schema": "https://hashhelix.dev/schemas/epoch.stage5.json",
            "stage": 8,
            "epoch_id": epoch_id,
            "lane_id": lane_id,
            "epoch_index": epoch_index,
            "start_step": start_step,
            "end_step": end_step,
            "step_count": len(segment),
            "merkle_root": merkle,
            "sequence_hash": seq_hash,
            "stats": stats,
        }

        epoch_filename = f"epoch_lane{lane_id:02d}_ep{epoch_index:04d}.json"
        epoch_path = out_dir / epoch_filename
        with epoch_path.open("w", encoding="utf-8") as f:
            json.dump(epoch_obj, f, indent=2, sort_keys=True)

        summaries.append(
            (
                epoch_index,
                {
                    "lane_id": lane_id,
                    "epoch_id": epoch_id,
                    "merkle_root": merkle,
                    "sequence_hash": seq_hash,
                },
            )
        )

    return summaries


def build_epoch_bundles(
    epoch_summaries: Dict[int, List[Dict]],
    out_dir: Path,
) -> None:
    """
    For each epoch_index, emit a bundle JSON listing all lane epochs.
    """
    for epoch_index in sorted(epoch_summaries.keys()):
        lanes = epoch_summaries[epoch_index]
        bundle_id = f"epoch-bundle-ep{epoch_index:04d}"

        bundle_obj = {
            "schema": "https://hashhelix.dev/schemas/hashBundle.stage6.json",
            "stage": 8,
            "bundle_id": bundle_id,
            "bundle_type": "epoch_bundle",
            "epoch_index": epoch_index,
            "lane_count": len(lanes),
            "lanes": lanes,
        }

        bundle_filename = f"epoch_bundle_ep{epoch_index:04d}.json"
        bundle_path = out_dir / bundle_filename
        with bundle_path.open("w", encoding="utf-8") as f:
            json.dump(bundle_obj, f, indent=2, sort_keys=True)


# ---------- CLI ----------

def autodetect_lanes(lane_dir: Path) -> List[int]:
    lane_ids: List[int] = []
    for path in sorted(lane_dir.glob("lane*.txt")):
        name = path.stem  # e.g., lane01
        if not name.startswith("lane"):
            continue
        suffix = name[4:]
        if not suffix.isdigit():
            continue
        lane_ids.append(int(suffix))
    return sorted(lane_ids)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="HashHelix Stage 8 — Automated epoch production."
    )
    parser.add_argument(
        "--lane-dir",
        type=str,
        default="data/runtime/lanes",
        help="Directory containing laneXX.txt traces (default: data/runtime/lanes).",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default="epochs/stage8_runtime",
        help="Output directory for epoch JSON artifacts (default: epochs/stage8_runtime).",
    )
    parser.add_argument(
        "--lanes",
        type=int,
        default=0,
        help=(
            "Number of lanes to process. "
            "If 0, autodetect lane*.txt in lane-dir (default: 0)."
        ),
    )
    parser.add_argument(
        "--epoch-length",
        type=int,
        required=True,
        help="Number of steps per epoch (e.g., 100000).",
    )
    parser.add_argument(
        "--max-epochs",
        type=int,
        default=0,
        help="Maximum epochs per lane (0 = all possible).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    lane_dir = Path(args.lane_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not lane_dir.exists():
        raise FileNotFoundError(f"lane-dir does not exist: {lane_dir}")

    if args.epoch_length <= 0:
        raise ValueError("epoch-length must be > 0")

    # Lane discovery
    if args.lanes > 0:
        lane_ids = list(range(1, args.lanes + 1))
    else:
        lane_ids = autodetect_lanes(lane_dir)

    if not lane_ids:
        raise ValueError("No lanes found to process.")

    epoch_summaries: Dict[int, List[Dict]] = {}

    for lane_id in lane_ids:
        lane_path = lane_dir / f"lane{lane_id:02d}.txt"
        if not lane_path.exists():
            # Strict: fail if a requested lane is missing.
            raise FileNotFoundError(f"Missing lane trace: {lane_path}")

        values = load_lane_values(lane_path)
        summaries = generate_epochs_for_lane(
            lane_id=lane_id,
            values=values,
            epoch_length=args.epoch_length,
            max_epochs=args.max_epochs,
            out_dir=out_dir,
        )

        for epoch_index, summary in summaries:
            epoch_summaries.setdefault(epoch_index, []).append(summary)

    # Build per-epoch bundles
    build_epoch_bundles(epoch_summaries, out_dir)


if __name__ == "__main__":
    main()
