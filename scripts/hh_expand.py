#!/usr/bin/env python3

import json
import gzip
import sys
import pathlib

def expand_json_gz(input_path):
    input_path = pathlib.Path(input_path)
    if not input_path.exists():
        print(f"[ERR] File not found: {input_path}")
        sys.exit(1)

    if not input_path.name.endswith(".json.gz"):
        print(f"[WARN] Expected a .json.gz file, got: {input_path.name}")

    # Output path: strip only the .gz
    if input_path.suffix == ".gz":
        output_path = input_path.with_suffix("")  # remove .gz
    else:
        output_path = input_path.with_suffix(".json")

    with gzip.open(input_path, "rb") as gz:
        raw = gz.read()

    # Validate JSON round-trip
    data = json.loads(raw.decode("utf-8"))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, sort_keys=True, separators=(",", ":"))

    print(f"[OK] Expanded → {output_path.name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: hh_expand.py <path_to_json_gz>")
        sys.exit(1)

    expand_json_gz(sys.argv[1])
