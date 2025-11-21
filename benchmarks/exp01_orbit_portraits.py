import math
import csv
from collections import Counter
from pathlib import Path

def run_orbit(n_steps: int = 100_000, seed: int = 1, lane_id: str = "lane01"):
    a = seed
    sequence = []

    for n in range(1, n_steps + 1):
        sequence.append(a)
        a = math.floor(n * math.sin(a + math.pi / n)) + 1

    minimum = min(sequence)
    maximum = max(sequence)
    unique_values = len(set(sequence))
    counter = Counter(sequence)
    most_common = counter.most_common(20)

    return {
        "lane_id": lane_id,
        "n_steps": n_steps,
        "seed": seed,
        "sequence": sequence,
        "min": minimum,
        "max": maximum,
        "unique": unique_values,
        "freq": most_common,
    }

def write_csv(results: dict, base_dir: Path):
    base_dir.mkdir(parents=True, exist_ok=True)
    csv_path = base_dir / f"exp01_orbit_{results['lane_id']}_N{results['n_steps']}.csv"

    # open the file, then create a writer on the file handle
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "a_n"])
        for i, value in enumerate(results["sequence"], start=1):
            w.writerow([i, value])

    return csv_path


def write_report(results: dict, base_dir: Path):
    base_dir.mkdir(parents=True, exist_ok=True)
    report_path = base_dir / f"exp01_orbit_{results['lane_id']}_N{results['n_steps']}_report.txt"

    lines = []
    lines.append("HashHelix Experiment #1 — Orbit Portrait (Single Lane)")
    lines.append(f"Lane ID: {results['lane_id']}")
    lines.append(f"Steps (N): {results['n_steps']}")
    lines.append(f"Seed a1: {results['seed']}")
    lines.append("")
    lines.append(f"Min value: {results['min']}")
    lines.append(f"Max value: {results['max']}")
    lines.append(f"Unique values: {results['unique']}")
    lines.append("")
    lines.append("Top 20 most frequent values:")
    for value, count in results["freq"]:
        lines.append(f"  value {value:6d}  →  {count} hits")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path

if __name__ == "__main__":
    N_STEPS = 100_000
    LANE_ID = "lane01"
    SEED_A1 = 1

    results_dir = Path(__file__).parent / "results_exp01"

    print(f"Running Orbit Portrait experiment...")
    print(f"  Lane: {LANE_ID}")
    print(f"  Steps: {N_STEPS}")
    print(f"  Seed: {SEED_A1}")

    results = run_orbit(n_steps=N_STEPS, seed=SEED_A1, lane_id=LANE_ID)

    csv_path = write_csv(results, results_dir)
    report_path = write_report(results, results_dir)

    print("\nDone.")
    print(f"CSV written to:    {csv_path}")
    print(f"Report written to: {report_path}")
    print("\nQuick summary:")
    print(f"  min = {results['min']}")
    print(f"  max = {results['max']}")
    print(f"  unique values = {results['unique']}")
    print("  top 5 most frequent values:")
    for value, count in results['freq'][:5]:
        print(f"    {value:6d}  →  {count} hits")
