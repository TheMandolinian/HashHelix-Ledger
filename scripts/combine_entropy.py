# combine_entropy.py
# Combine and summarize entropy lanes

import json

FILES = [
    "hh_entropy_lane01.txt",
    "hh_entropy_lane02.txt",
    "hh_entropy_lane03.txt",
]

OUT = "data/entropy_summary.jsonl"


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

    for i, path in enumerate(FILES, start=1):
        data = load_lane(path)
        results[f"lane_{i}"] = compute_stats(data)

    # Write JSON summary
    with open(OUT, "w") as f:
        json.dump(results, f, indent=4)

    print(f"[OK] Summary written → {OUT}\n")

    # Also print to terminal
    for lane, stats in results.items():
        print(f"{lane}:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        print()


if __name__ == "__main__":
    main()
