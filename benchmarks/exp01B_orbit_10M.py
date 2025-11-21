import math
from pathlib import Path
from collections import Counter

# 10,000,000-step orbit portrait stress test
# Optimized for low memory footprint and streaming output

N_STEPS = 10_000_000
LANE_ID = "lane01"
SEED_A1 = 1

results_dir = Path(__file__).parent / "results_exp01B"
results_dir.mkdir(parents=True, exist_ok=True)

summary_path = results_dir / f"exp01B_orbit_{LANE_ID}_summary.txt"

a = SEED_A1

min_val = float("inf")
max_val = float("-inf")

# Frequency sampling (not full histogram)
# Capture every value mod 10,000 for statistical signatures
freq = Counter()

checkpoint_interval = 100_000

with summary_path.open("w") as out:
    out.write(f"Exp #1B — High-N Orbit Portrait Stress Test\n")
    out.write(f"Total steps: {N_STEPS:,}\n")
    out.write(f"Seed: {SEED_A1}\n")
    out.write(f"Lane: {LANE_ID}\n\n")
    out.write("Running...\n")

    for n in range(1, N_STEPS + 1):
        min_val = min(min_val, a)
        max_val = max(max_val, a)

        # sample-based frequency to avoid 10M RAM blowout
        freq[a % 10_000] += 1

        a = math.floor(n * math.sin(a + math.pi / n)) + 1

        if n % checkpoint_interval == 0:
            out.write(f"Reached {n:,}\n")
            out.flush()

    out.write("\n=== FINAL RESULTS ===\n")
    out.write(f"Min: {min_val}\n")
    out.write(f"Max: {max_val}\n")
    out.write(f"Sampled frequency entries: {len(freq)}\n\n")

    out.write("Top 20 sampled values (mod 10k):\n")
    for value, count in freq.most_common(20):
        out.write(f"  {value:6d} → {count}\n")

print("Finished 10M steps.")
print(f"Report saved to: {summary_path}")
