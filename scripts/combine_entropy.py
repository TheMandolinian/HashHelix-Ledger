# combine_entropy.py
# Combine and summarize entropy lanes (soft-skip missing files)

import json
from pathlib import Path

FILES = [
    "hh_entropy_lane01.txt",
    "hh_entropy_lane02.txt",
    "hh_entropy_lane03.txt",
]

OUT = "data/entropy_summary.json"


def load_lane(path):
    """Load a lane text file → list of integers."""
    with open(path, "r") as f:
        return [int(x.strip()) for x in f.readlines()]


def compute_stats(values):
    """Compute basic statistics for a lane."""
    return {
        "length": len(values),
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / len(values),
    }


def main():
    results = {}
    missing = []

    for i, path in enumerate(FILES, start=1):
        p = Path(path)

        if not p.exists():
            missing.append(path)
            print(f"[WARN] Missing entropy lane → {path}")
            continue

        try:
            data = load_lane(p)
        except Exception as e:
            print(f"[WARN] Could not read {path}: {e}")
            missing.append(path)
            continue

        results[f"lane_{i}"] = compute_stats(data)

    # If no lanes exist at all, write a minimal safe file
    Path("data").mkdir(exist_ok=True)
    if not results:
        summary = {
            "lanes": {},
            "note": "No entropy lanes found. Summary not computed.",
            "missing": missing,
        }
        with open(OUT, "w") as f:
            json.dump(summary, f, indent=4)
        print(f"[OK] Minimal summary written → {OUT}")
        return 0

    # Normal case → write stats summary
    summary = {
        "lanes": results,
        "missing": missing,
    }

    with open(OUT, "w") as f:
        json.dump(summary, f, indent=4)

    print(f"[OK] Summary written → {OUT}\n")

    # Also print to terminal
    for lane, stats in results.items():
        print(f"{lane}:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        print()

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main() or 0)

