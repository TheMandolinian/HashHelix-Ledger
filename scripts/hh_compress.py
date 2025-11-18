#!/usr/bin/env python3

import json
import gzip
import sys
import pathlib

def deterministic_dump(data):
    """
    Deterministic JSON serializer:
    - Sorted keys
    - No extra whitespace
    """
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")

def compress_json(input_path):
    input_path = pathlib.Path(input_path)
    if not input_path.exists():
        print(f"[ERR] File not found: {input_path}")
        sys.exit(1)

    # Output path (same name, but .json.gz)
    output_path = input_path.with_suffix(input_path.suffix + ".gz")

    # Load JSON
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Deterministic bytes
    payload = deterministic_dump(data)

    # GZIP
    with gzip.open(output_path, "wb") as gz:
        gz.write(payload)

    print(f"[OK] Compressed → {output_path.name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: hh_compress.py <path_to_json>")
        sys.exit(1)

    compress_json(sys.argv[1])

