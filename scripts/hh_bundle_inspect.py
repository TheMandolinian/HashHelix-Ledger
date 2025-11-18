#!/usr/bin/env python3

import json
import gzip
import hashlib
import pathlib
import sys
import os


def deterministic_bytes(data):
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")


def inspect_bundle(json_path):
    json_path = pathlib.Path(json_path)

    if not json_path.exists():
        print(f"[ERR] File not found: {json_path}")
        sys.exit(1)

    # Load JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Deterministic bytes
    dbytes = deterministic_bytes(data)
    sha = hashlib.sha256(dbytes).hexdigest()

    # Check for gzip companion
    gz_path = json_path.with_suffix(json_path.suffix + ".gz")
    has_gz = gz_path.exists()

    # Sizes
    size_json = os.path.getsize(json_path)
    size_gz = os.path.getsize(gz_path) if has_gz else None

    # Extract expected info if present
    lane = data.get("lane", None)
    epochs = data.get("epochs", [])
    epoch_count = len(epochs) if isinstance(epochs, list) else 0

    print("=== Stage 6 Artifact Inspector ===")
    print(f"File:         {json_path.name}")
    print(f"Lane:         {lane}")
    print(f"Epochs:       {epoch_count}")
    print(f"JSON Size:    {size_json} bytes")
    if has_gz:
        print(f"GZIP Size:    {size_gz} bytes")
    else:
        print("GZIP Size:    (not found)")
    print(f"SHA-256:      {sha}")
    print("==================================")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: hh_bundle_inspect.py <path_to_json>")
        sys.exit(1)

    inspect_bundle(sys.argv[1])
