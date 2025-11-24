import math
import time
from pathlib import Path

"""
Experiment 3b / Exp01B — High-N Orbit Stress Test (NER Truth Mode)

This script runs the WDTP recurrence under the Numerical Evaluation Rule (NER)
in a low-overhead "truth mode" configuration:

    a_1 = 1
    a_n = floor(n * sin(theta_n)) + 1
    theta_n = (a_{n-1} + pi/n) mod 2*pi

- No heavy instrumentation
- No entropy windows
- No rolling deques
- No per-step logging
- Minimal file output (header, sparse checkpoints, final summary)

Use this as the canonical high-N runner for:
- NER stability checks
- Cross-language replay tests
- Cross-hardware determinism checks
"""

# ===== Configuration =====

N_STEPS = 1_000_000_000  # Adjust to 50_000_000 or higher for full stress runs
LANE_ID = "lane01"
SEED_A1 = 1

results_dir = Path(__file__).parent / "results_exp01B"
results_dir.mkdir(parents=True, exist_ok=True)

summary_path = results_dir / f"exp01B_orbit1B_{LANE_ID}_summary.txt"


def run_truth_mode():
    a = SEED_A1

    # Track basic stats (cheap, not "heavy instrumentation")
    min_val = a
    max_val = a

    checkpoint_interval = 10_000_000  # print every 1M steps

    start_time = time.perf_counter()

    with summary_path.open("w") as out:
        out.write("Exp #1B / Experiment 3b — High-N Orbit Stress Test (NER Truth Mode)\n")
        out.write(f"Total steps: {N_STEPS:,}\n")
        out.write(f"Seed (a1): {SEED_A1}\n")
        out.write(f"Lane: {LANE_ID}\n\n")
        out.write("Recurrence (NER): a_n = floor(n * sin(theta_n)) + 1, "
                  "theta_n = (a_{n-1} + pi/n) mod 2*pi\n\n")
        out.write("Running...\n")
        out.flush()

        for n in range(1, N_STEPS + 1):
            # Update simple stats
            if a < min_val:
                min_val = a
            if a > max_val:
                max_val = a

            # NER-compliant phase update
            phase = (a + math.pi / n) % (2.0 * math.pi)
            a = math.floor(n * math.sin(phase)) + 1

            if n % checkpoint_interval == 0:
                out.write(f"Reached {n:,} steps, a_n = {a}\n")
                out.flush()

        elapsed = time.perf_counter() - start_time

        out.write("\n=== FINAL RESULTS ===\n")
        out.write(f"Final n: {N_STEPS:,}\n")
        out.write(f"Final a_n: {a}\n")
        out.write(f"Min a_n observed: {min_val}\n")
        out.write(f"Max a_n observed: {max_val}\n")
        out.write(f"Elapsed time (seconds): {elapsed:.3f}\n")

        end_ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n=== NER Truth-Mode High-N Run Complete ===")
    print(f"Timestamp       : {end_ts}")
    print(f"Steps (N)       : {N_STEPS:,}")
    print(f"Final a_n       : {a}")
    print(f"Min a_n         : {min_val}")
    print(f"Max a_n         : {max_val}")
    print(f"Elapsed (sec)   : {elapsed:.3f}")
    print(f"Summary written : {summary_path}")
    print("==========================================\n")


if __name__ == "__main__":
    run_truth_mode()

