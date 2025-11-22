import os
import math
import csv
import matplotlib.pyplot as plt

# ============================================================
#  Experiment #2 — Visual Signatures
#
#  Generates:
#     1. Time-Series Plot
#     2. Phase-Space Plot (a_n vs a_{n+1})
#     3. Modular Signature Plots (mod 2,3,5,7,10)
#     4. CSV output of the entire sequence
#
#  Output folder:
#       benchmarks/results_exp02/
# ============================================================


# -----------------------------
#  Recurrence Function
# -----------------------------
def hashhelix_step(n, prev):
    """Compute the next a_n using the HashHelix recurrence."""
    return math.floor(n * math.sin(prev + math.pi / n)) + 1


# -----------------------------
#  Generate Sequence
# -----------------------------
def generate_sequence(N=100000, a1=1):
    seq = [0] * (N + 1)
    seq[1] = a1

    for n in range(2, N + 1):
        seq[n] = hashhelix_step(n, seq[n - 1])

    return seq


# -----------------------------
#  Save CSV
# -----------------------------
def save_csv(seq, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "a_n"])
        for i in range(1, len(seq)):
            writer.writerow([i, seq[i]])


# -----------------------------
#  Plot Helpers
# -----------------------------
def plot_time_series(seq, outpath):
    plt.figure(figsize=(12, 4))
    plt.plot(seq[1:], linewidth=0.7)
    plt.title("HashHelix — Time Series Signature")
    plt.xlabel("n")
    plt.ylabel("a_n")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_phase_space(seq, outpath):
    plt.figure(figsize=(6, 6))
    plt.scatter(seq[1:-1], seq[2:], s=1)
    plt.title("HashHelix — Phase Space (a_n vs a_{n+1})")
    plt.xlabel("a_n")
    plt.ylabel("a_{n+1}")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_modular(seq, out_folder, mods):
    for m in mods:
        plt.figure(figsize=(12, 3))
        mod_values = [x % m for x in seq[1:]]
        plt.plot(mod_values, linewidth=0.5)
        plt.title(f"HashHelix — Modular Signature (mod {m})")
        plt.xlabel("n")
        plt.ylabel(f"a_n mod {m}")
        plt.tight_layout()
        plt.savefig(os.path.join(out_folder, f"mod_{m}.png"))
        plt.close()


# -----------------------------
#  Main Runner
# -----------------------------
def run_experiment():
    results_dir = "benchmarks/results_exp02"
    os.makedirs(results_dir, exist_ok=True)

    N = 100000
    a1 = 1

    print(f"Running Experiment #2 (Visual Signatures) with N={N} ...")
    seq = generate_sequence(N=N, a1=a1)

    # Save CSV
    csv_path = os.path.join(results_dir, "exp02_sequence.csv")
    print("Saving CSV...")
    save_csv(seq, csv_path)

    # Time Series
    print("Generating time-series plot...")
    plot_time_series(seq, os.path.join(results_dir, "time_series.png"))

    # Phase Space
    print("Generating phase-space plot...")
    plot_phase_space(seq, os.path.join(results_dir, "phase_space.png"))

    # Modular Plots
    print("Generating modular signature plots...")
    mods = [2, 3, 5, 7, 10]
    plot_modular(seq, results_dir, mods)

    print("Experiment #2 complete.")
    print(f"Results saved to: {results_dir}")


# -----------------------------
#  Execute
# -----------------------------
if __name__ == "__main__":
    run_experiment()

