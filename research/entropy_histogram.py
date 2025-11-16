# entropy_histogram.py
# Histogram analysis for HH entropy lanes

from collections import Counter
from pathlib import Path
import json

# Input lanes — same naming as before
FILES = [
    "hh_entropy_lane01.txt",
    "hh_entropy_lane02.txt",
    "hh_entropy_lane03.txt",
]

OUT = "data/entropy_value_histogram.json"

def load_values(path):
    """Load integers from a lane file."""
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                yield int(line)

def main():
    counter = Counter()

    # accumulate all values across all lanes
    for filename in FILES:
        p = Path(filename)
        if not p.exists():
            print(f"[WARN] Missing: {filename}")
            continue

        for v in load_values(p):
            counter[v] += 1

    # Summary
    print(f"[OK] Loaded {sum(counter.values()):,} values across lanes.")

    # 20 most common values
    top20 = counter.most_common(20)

    print("\nTop 20 value frequencies:")
    for val, cnt in top20:
        print(f"  {val:>7} → {cnt:,}")

    # Write JSON
    data = {
        "total_values": sum(counter.values()),
        "unique_values": len(counter),
        "top20": top20,
    }

    with open(OUT, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n[OK] Histogram written → {OUT}")

if __name__ == "__main__":
    main()
