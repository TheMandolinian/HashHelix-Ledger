#!/usr/bin/env python3
"""
HashHelix — Stage 8
Relic Automation Runtime

Takes epoch bundle JSON files (output of epoch_auto.py) and produces:

- N-epoch relic artifacts (COLD vault objects)
- Each relic aggregates multiple epoch bundles
- Deterministic Merkle and chiral commitments

Stage 8 constraints:
- Deterministic and reproducible
- No randomness, no timestamps
- Engine-only
"""

import argparse
import hashlib
import json
from pathlib import Path from typing import Dict, List, Tuple


# ---------- Hash / Merkle helpers ----------

def sha256_bytes(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def sha256_hex_of_strings(values: List[str]) -> str:
    """
    Stable hash over a sequence of strings with '\n' separators.
    """
    h = hashlib.sha256()
    for v in values:
        h.update(v.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def merkle_root_from_hex(values: List[str]) -> str:
    """
    Deterministic Merkle root over hex-encoded hashes.

    - Leaf = bytes.fromhex(v)
    - Pair = SHA256(left || right)
    - Odd node duplicated
    - Empty -> SHA256(b"")
    """
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


# ---------- Core relic construction ----------

def load_epoch_bundles(epoch_dir: Path) -> Dict[int, Dict]:
    """
    Load all epoch_bundle_epXXXX.json files in epoch_dir.

    Returns:
        dict: epoch_index -> bundle_obj
    """
    bundles: Dict[int, Dict] = {}

    for path in sorted(epoch_dir.glob("epoch_bundle_ep*.json")):
        name = path.stem  # e.g. epoch_bundle_ep0001
        # extract XXXX
        parts = name.split("_ep")
        if len(parts) != 2:
            continue
        idx_str = parts[1]
        if not idx_str.isdigit():
            continue
        epoch_index = int(idx_str)

        with path.open("r", encoding="utf-8") as f:
            obj = json.load(f)
        bundles[epoch_index] = obj

    if not bundles:
        raise ValueError(f"No epoch_bundle_epXXXX.json files found in {epoch_dir}")

    return bundles


def build_relics(
    bundles: Dict[int, Dict],
    epochs_per_relic: int,
    max_relics: int,
    out_dir: Path,
) -> None:
    """
    Group epoch bundles into N-epoch relics and emit relic JSON files.
    """
    sorted_epochs = sorted(bundles.keys())
    total_epochs = len(sorted_epochs)

    if total_epochs < epochs_per_relic:
        # Not enough epochs to make even one relic
        return

    # Compute number of relics possible
    num_relics = total_epochs // epochs_per_relic
    if max_relics > 0:
        num_relics = min(num_relics, max_relics)

    for relic_index in range(1, num_relics + 1):
        start_pos = (relic_index - 1) * epochs_per_relic
        end_pos = start_pos + epochs_per_relic
        epoch_slice = sorted_epochs[start_pos:end_pos]

        epoch_start = epoch_slice[0]
        epoch_end = epoch_slice[-1]

        bundle_ids: List[str] = []
        bundle_merkle_roots: List[str] = []
        epoch_entries: List[Dict] = []

        lane_count = None

        for epoch_idx in epoch_slice:
            bundle = bundles[epoch_idx]

            bundle_id = bundle.get("bundle_id", f"epoch-bundle-ep{epoch_idx:04d}")
            bundle_ids.append(bundle_id)

            # lane count and lane merkle roots
            lanes = bundle.get("lanes", [])
            if lane_count is None:
                lane_count = len(lanes)

            lane_merkle_roots = [lane.get("merkle_root", "") for lane in lanes]
            # Merkle root over all lane merkle_roots for this epoch (stable)
            bundle_merkle = merkle_root_from_hex(
                [r for r in lane_merkle_roots if r]
            )
            bundle_merkle_roots.append(bundle_merkle)

            epoch_entries.append(
                {
                    "epoch_index": epoch_idx,
                    "bundle_id": bundle_id,
                    "lane_count": len(lanes),
                    "lane_merkle_roots": lane_merkle_roots,
                    "bundle_merkle_root": bundle_merkle,
                }
            )

        # Aggregate merkle across epoch-level bundle roots
        relic_merkle_root = merkle_root_from_hex(bundle_merkle_roots)

        # Chiral commitments: forward vs reverse order of bundle IDs
        chiral_forward = sha256_hex_of_strings(bundle_ids)
        chiral_reverse = sha256_hex_of_strings(list(reversed(bundle_ids)))

        relic_id = f"relic-ep{epoch_start:04d}-ep{epoch_end:04d}"

        relic_obj = {
            "schema": "https://hashhelix.dev/schemas/relic.schema.json",
            "stage": 8,
            "relic_id": relic_id,
            "relic_index": relic_index,
            "epoch_start": epoch_start,
            "epoch_end": epoch_end,
            "epoch_count": len(epoch_slice),
            "lane_count": lane_count if lane_count is not None else 0,
            "epoch_bundles": epoch_entries,
            "aggregate": {
                "relic_merkle_root": relic_merkle_root,
                "chiral_commitment": {
                    "forward": chiral_forward,
                    "reverse": chiral_reverse,
                },
                "bundle_ids": bundle_ids,
            },
        }

        out_path = out_dir / f"{relic_id}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(relic_obj, f, indent=2, sort_keys=True)


# ---------- CLI ----------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="HashHelix Stage 8 — Automated relic sequence generation."
    )
    parser.add_argument(
        "--epoch-dir",
        type=str,
        default="epochs/stage8_runtime",
        help="Directory containing epoch_bundle_epXXXX.json (default: epochs/stage8_runtime).",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default="relics/stage8_runtime",
        help="Output directory for relic JSON artifacts (default: relics/stage8_runtime).",
    )
    parser.add_argument(
        "--epochs-per-relic",
        type=int,
        required=True,
        help="Number of consecutive epochs per relic (e.g., 10).",
    )
    parser.add_argument(
        "--max-relics",
        type=int,
        default=0,
        help="Maximum relics to generate (0 = all possible).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    epoch_dir = Path(args.epoch_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not epoch_dir.exists():
        raise FileNotFoundError(f"epoch-dir does not exist: {epoch_dir}")

    if args.epochs_per_relic <= 0:
        raise ValueError("epochs-per-relic must be > 0")

    bundles = load_epoch_bundles(epoch_dir)
    build_relics(
        bundles=bundles,
        epochs_per_relic=args.epochs_per_relic,
        max_relics=args.max_relics,
        out_dir=out_dir,
    )


if __name__ == "__main__":
    main()
