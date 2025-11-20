#!/usr/bin/env python3
"""
HashHelix Stage 7
Epoch Combiner Tool

Takes a JSON file of lane roots and emits an Epoch Bundle
that conforms to schemas/epoch.schema.json.

Input lane_roots JSON format (example):

[
  {
    "lane_id": 1,
    "h_plus": "hex-hplus-1",
    "h_minus": "hex-hminus-1",
    "merkle_root": "hex-merkle-1"
  },
  {
    "lane_id": 2,
    "h_plus": "hex-hplus-2",
    "h_minus": "hex-hminus-2",
    "merkle_root": "hex-merkle-2"
  }
]
"""

import argparse
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_epoch_bundle(
    singularity_id: str,
    singularity_version: str,
    epoch_index: int,
    author: str,
    version: str,
    lane_roots: list,
) -> dict:
    bundle = {
        "artifact_type": "epoch_bundle",
        "version": version,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "author": author,
        "vault_class": "WARM",
        "singularity_ref": {
            "id": singularity_id,
            "version": singularity_version,
        },
        "epoch_index": epoch_index,
        "lane_roots": lane_roots,
        # integrity will be filled in after serialization
        "integrity": {
            "sha256_epoch_bundle": "",
            "size_bytes": 0,
        },
    }

    # Compute integrity over canonical JSON
    serialized = json.dumps(bundle, sort_keys=True, separators=(",", ":")).encode("utf-8")
    bundle["integrity"]["sha256_epoch_bundle"] = sha256_hex(serialized)
    bundle["integrity"]["size_bytes"] = len(serialized)

    return bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="HashHelix Stage 7 — Epoch Combiner")
    parser.add_argument(
        "--lane-roots",
        required=True,
        help="Path to JSON file containing lane_roots array.",
    )
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
        "--epoch-index",
        required=True,
        type=int,
        help="Epoch index for this bundle.",
    )
    parser.add_argument(
        "--author",
        default="James Bradley Waresback",
        help="Author field for the epoch bundle.",
    )
    parser.add_argument(
        "--version",
        default="v1.7",
        help="Epoch bundle version string, e.g. v1.7",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output path for the epoch bundle JSON.",
    )

    args = parser.parse_args()

    lane_roots_path = Path(args.lane_roots)
    output_path = Path(args.output)

    with lane_roots_path.open("r", encoding="utf-8") as f:
        lane_roots = json.load(f)

    if not isinstance(lane_roots, list):
        raise SystemExit("lane_roots JSON must be a list of lane root objects.")

    bundle = build_epoch_bundle(
        singularity_id=args.singularity_id,
        singularity_version=args.singularity_version,
        epoch_index=args.epoch_index,
        author=args.author,
        version=args.version,
        lane_roots=lane_roots,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, sort_keys=True)

    print(f"[OK] Wrote epoch bundle → {output_path}")


if __name__ == "__main__":
    main()
