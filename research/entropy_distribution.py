# entropy_distribution.py
# HashHelix Stage 3D — Distribution Curve + ASCII Visualization

import json
from pathlib import Path
from collections import Counter


LANE_FILES = [
    "hh_entropy_lane01.txt",
    "hh_entropy_lane02.txt",
    "hh_entropy_lane03.txt",
]

OUT_JSON = "data/entropy_distribution.json"
OUT_ASCII = "data/entropy_distribution_ascii.txt"


def load_all_values():
    """Load all entropy lane integer values."""
    all_vals = []
    for file in LANE_FILES:
        path = Path(file)
        with path.open() as f:
            for line in f:
                try:
                    all_vals.append(int(line.strip()))
                except:
                    pass
    return all_vals


def ascii_plot(counter, *, width=80, top=40):
    """
    Create a crude ASCII histogram for fast pattern inspection.
    Top 40 most frequent values only.
    """
    items = counter.most_common(top)
    max_count = items[0][1]

    lines = []
    for val, count in items:
        bar_len = int((count / max_count) * width)
        bar = "#" * bar_len
        lines.append(f"{val:>8} | {bar} {count}")

    return "\n".join(lines)


def main():
    print("[OK] Loading all values...")
    vals = load_all_values()

    print(f"[OK] Loaded {len(vals):,} total values.")

    counter = Counter(vals)

    # Basic distribution metrics
    distribution = {
        "count": len(vals),
        "unique_values": len(counter),
        "min": min(vals),
        "max": max(vals),
        "mean": sum(vals) / len(vals),
        "top_20": counter.most_common(20),
    }

    # Write JSON
    with open(OUT_JSON, "w") as f:
        json.dump(distribution, f, indent=4)

    print(f"[OK] Distribution JSON written → {OUT_JSON}")

    # ASCII visualization
    ascii_out = ascii_plot(counter)

    with open(OUT_ASCII, "w") as f:
        f.write(ascii_out)

    print(f"[OK] ASCII distribution written → {OUT_ASCII}")
    print("\n--- ASCII Preview (Top 10) ---")
    print("\n".join(ascii_out.split("\n")[:10]))


if __name__ == "__main__":
    main()
