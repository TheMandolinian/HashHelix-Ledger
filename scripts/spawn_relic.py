#!/usr/bin/env python3
"""
HashHelix Stage 7
Temporal Relic Spawner

Combines one or more Epoch Bundles into a Temporal Relic
that conforms to schemas/relic.schema.json.

Usage example:

python scripts/spawn_relic.py \
  --singularity-id SINGULARITY_0001 \
  --singularity-version v1.7 \
  --start-epoch 0 \
  --end-epoch 9 \
  --epoch-files artifacts/epochs/epoch_*.json \
  --label "Stage 7 Demo Relic" \
  --institution "HashHelix Labs" \
  --output artifacts/stage7_sample/relic_demo.json
"""

import argparse
import glob
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_epoch_bundles(patterns: List[str]) -> List[Dict[str, Any]]:
    files: List[Path] = []
    for pattern in patterns:
        for p in glob.glob(pattern):
            files.append(Path(p))

    if not files:
        raise SystemExit("No epoch bundle files matched the given --epoch-files patterns.")

    bundles = []
    for p in sorted(files):
        with p.open("r", encoding="utf-8") as f:
            bundles.append(json.load(f))
    return bundles


def build_relic(
    singularity_id: str,
    singularity_version: str,
    start_epoch: int,
    end_epoch: int,
    author: str,
    version: str,
    epoch_bundles: List[Dict[str, Any]],
    label: str | None,
    description: str | None,
    institution: str | None,
) -> dict:
    # Collect lanes across all epochs
    lane_ids = set()
    epoch_hashes: List[str] = []
    lane_concat_parts: List[str] = []

    for bundle in epoch_bundles:
        epoch_hash = bundle.get("integrity", {}).get("sha256_epoch_bundle", "")
        epoch_hashes.append(epoch_hash)

        for lr in bundle.get("lane_roots", []):
            lane_id = lr.get("lane_id")
            if lane_id is not None:
                lane_ids.add(int(lane_id))
            lane_concat_parts.append(
                f"{bundle.get('epoch_index')}|{lr.get('lane_id')}|{lr.get('h_plus')}|{lr.get('h_minus')}|{lr.get('merkle_root')}"
            )

    lanes_list = sorted(lane_ids)

    # Chiral commitments derived from lane roots
    lane_concat = "|".join(lane_concat_parts).encode("utf-8")
    h_plus = sha256_hex(b"plus|" + lane_concat)
    h_minus = sha256_hex(b"minus|" + lane_concat)

    # Simple Merkle-like root over epoch hashes
    merkle_seed = "|".join(epoch_hashes).encode("utf-8")
    merkle_root = sha256_hex(b"merkle|" + merkle_seed)

    relic = {
        "artifact_type": "temporal_relic",
        "version": version,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "author": author,
        "vault_class": "COLD",
        "singularity_ref": {
            "id": singularity_id,
            "version": singularity_version,
        },
        "epoch_range": {
            "start_epoch": start_epoch,
            "end_epoch": end_epoch,
        },
        "lanes": lanes_list,
        "chiral_commitment": {
            "h_plus": h_plus,
            "h_minus": h_minus,
        },
        "merkle": {
            "scheme": "sha256-merkle-v1",
            "root": merkle_root,
        },
        # integrity will be filled after serialization
        "integrity": {
            "sha256_bundle": "",
            "size_bytes": 0,
        },
        "metadata": {},
    }

    # Optional metadata
    if label:
        relic["metadata"]["label"] = label
    if description:
        relic["metadata"]["description"] = description
    if institution:
        relic["metadata"]["institution"] = institution

    # Compute integrity over canonical JSON
    serialized = json.dumps(relic, sort_keys=True, separators=(",", ":")).encode("utf-8")
    relic["integrity"]["sha256_bundle"] = sha256_hex(serialized)
    relic["integrity"]["size_bytes"] = len(serialized)

    return relic


def main() -> None:
    parser = argparse.ArgumentParser(description="HashHelix Stage 7 — Temporal Relic Spawner")
    parser.add_argument(
        "--singularity-id",
        required=True,
        help="Opaque ID or hash of the Singularity Artifact.",
    )
    parser.add_argument(
        "--singularity-version",
        required=True,
        help="Singularity version, e.g. v1.7",
    )
    parser.add_argument(
        "--start-epoch",
        required=True,
        type=int,
        help="Start epoch (inclusive).",
    )
    parser.add_argument(
        "--end-epoch",
        required=True,
        type=int,
        help="End epoch (inclusive).",
    )
    parser.add_argument(
        "--epoch-files",
        required=True,
        nargs="+",
        help="One or more glob patterns or explicit paths to epoch bundle JSON files.",
    )
    parser.add_argument(
        "--author",
        default="James Bradley Waresback",
        help="Author field for the relic.",
    )
    parser.add_argument(
        "--version",
        default="v1.7",
        help="Relic version string, e.g. v1.7",
    )
    parser.add_argument(
        "--label",
        help="Optional human-readable label for the relic.",
    )
    parser.add_argument(
        "--description",
        help="Optional description.",
    )
    parser.add_argument(
        "--institution",
        help="Optional institution name.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output path for the relic JSON.",
    )

    args = parser.parse_args()

    if args.end_epoch < args.start_epoch:
        raise SystemExit("end_epoch must be >= start_epoch")

    epoch_bundles = load_epoch_bundles(args.epoch_files)

    relic = build_relic(
        singularity_id=args.singularity_id,
        singularity_version=args.singularity_version,
        start_epoch=args.start_epoch,
        end_epoch=args.end_epoch,
        author=args.author,
        version=args.version,
        epoch_bundles=epoch_bundles,
        label=args.label,
        description=args.description,
        institution=args.institution,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(relic, f, indent=2, sort_keys=True)

    print(f"[OK] Wrote Temporal Relic → {output_path}")


if __name__ == "__main__":
    main()
