import time
import csv
from core.wdtp import wdtp_next
import os
from datetime import datetime

# -----------------------------------------------------
# HashHelix Synthetic Benchmark (v1.7)
# -----------------------------------------------------

def sine_recursion(n, steps):
    """NER-compliant π/n-phase sine recursion (synthetic benchmark)."""
    a = 1  # synthetic state, same starting point as WDTP’s a₁ = 1
    for k in range(2, steps + 2):
        a = wdtp_next(a, k)
    return a


def run_lane(n, steps):
    """Benchmark a single lane."""
    start = time.time()
    sine_recursion(n, steps)
    end = time.time()
    return end - start


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    print("\n[HH BENCH] HashHelix Synthetic Benchmark v1.7")
    steps = 21000  # match your 21-helix benchmark size
    lane_counts = [1, 3, 7, 9, 12, 15, 18, 21]  # progressive scaling

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outdir = f"benchmarks/{timestamp}"
    ensure_dir(outdir)

    results = []

    for lanes in lane_counts:
        print(f"[BENCH] Running {lanes} lanes × {steps} steps...")

        start_block = time.time()
        for _ in range(lanes):
            run_lane(lanes, steps)
        end_block = time.time()

        elapsed = end_block - start_block
        tps = (lanes * steps) / elapsed

        print(f" → {tps:.2f} TPS")

        results.append({
            "lanes": lanes,
            "steps": steps,
            "elapsed_sec": elapsed,
            "tps": tps
        })

    # Write CSV
    csvpath = os.path.join(outdir, "benchmark_results.csv")
    with open(csvpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["lanes", "steps", "elapsed_sec", "tps"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    print(f"\n[WRITE] Benchmark results saved → {csvpath}")
    print("[DONE] Synthetic HashHelix benchmark complete.\n")


if __name__ == "__main__":
    main()
