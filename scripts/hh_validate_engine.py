#!/usr/bin/env python3

import json
import sys
import pathlib

# Keys that should NOT appear in engine-only artifacts
FORBIDDEN_BUSINESS_KEYS = {
    "pricing",
    "prices",
    "licensing",
    "license",
    "customer",
    "customers",
    "xrpl",
    "xlm",
    "nft",
    "royalties",
    "revenue",
}

def validate_engine_file(path):
    path = pathlib.Path(path)

    if not path.exists():
        print(f"[ERR] File not found: {path}")
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERR] JSON parse failed for {path}: {e}")
        return False

    if not isinstance(data, dict):
        print(f"[ERR] Top-level JSON must be an object: {path}")
        return False

    # Simple sanity: must look like an engine artifact
    top_keys = set(data.keys())
    required_like = {"lane", "epochs"}  # soft expectation, not hard schema

    if not required_like & top_keys:
        print(f"[WARN] {path} does not contain typical engine keys (lane/epochs).")

    # Business-layer guard: no forbidden keys anywhere in the tree
    def walk(obj, prefix=""):
        problems = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                full = f"{prefix}.{k}" if prefix else k
                if k.lower() in FORBIDDEN_BUSINESS_KEYS:
                    problems.append(full)
                problems.extend(walk(v, full))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                full = f"{prefix}[{i}]"
                problems.extend(walk(v, full))
        return problems

    bad_paths = walk(data)

    if bad_paths:
        print(f"[ERR] Forbidden business keys found in {path}:")
        for p in bad_paths:
            print(f"  - {p}")
        return False

    print(f"[OK] Engine-only validation passed: {path}")
    return True


def main(argv):
    if len(argv) < 2:
        print("Usage: hh_validate_engine.py <path1.json> [path2.json ...]")
        return 1

    ok = True
    for p in argv[1:]:
        if not validate_engine_file(p):
            ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
