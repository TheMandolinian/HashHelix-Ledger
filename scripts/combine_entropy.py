# scripts/combine_entropy.py
# Combine and summarize entropy lanes (engine-only)

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any

FILES = [
    "hh_entropy_lane01.txt",
    "hh_entropy_lane02.txt",
    "hh_entropy_lane03.txt",
]

OUT = Path("data/entropy_summary.jsonl")


def load_lane(path: Path) -> List[int]:
    """Load a lane text file -> list of integers. Soft-skip if missing."""
    if not path.exists():
        print(f"[WARN] Missing entropy lane file: {path}")
        return []
    values: List[int] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                values.append(int(line))
            except ValueError:
                print(f"[WARN] Non-integer line in {path}: {line!r}")
    return values


def compute_stats(values: List[int]) -> Dict[str, Any]:
    """Compute basic statistics for a lane. Handles empty lanes."""
    if not values:
        return {"length": 0, "min": None, "max": None, "mean": None}
    return {
        "length": len(values),
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / len(values),
    }


def main() -> int:
    results: Dict[str, Any] = {}

    for i, rel_path in enumerate(FILES, start=1):
        path = Path(rel_path)
        lane_values = load_lane(path)
        results[f"lane_{i}"] = compute_stats(lane_values)

    OUT.parent.mkdir(parents=True, exist_ok=True)

    # JSONL output: one object per line.
    with OUT.open("w", encoding="utf-8") as f:
        f.write(json.dumps(results) + "\n")

    print(f"[OK] Summary written -> {OUT}")
    for lane, stats in results.items():
        print(f"{lane}: {stats}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
