# research/entropy_fingerprint.py
#
# HashHelix Entropy Fingerprint
#
# Compares the HashHelix entropy lanes to several baseline generators:
#   - Uniform random integers
#   - Normal-distributed integers
#   - Logistic-map chaos (r = 3.99)
#   - SHA-256 derived integers
#
# Output:
#   - data/entropy_fingerprint.json       (machine-friendly summary)
#   - data/entropy_fingerprint_ascii.txt  (human-readable fingerprint)

import json
import math
import random
import hashlib
from typing import Iterable, Dict, Any

# --- Config -----------------------------------------------------------------

LANE_FILES = [
    "hh_entropy_lane01.txt",
    "hh_entropy_lane02.txt",
    "hh_entropy_lane03.txt",
]

OUT_JSON = "data/entropy_fingerprint.json"
OUT_ASCII = "data/entropy_fingerprint_ascii.txt"

# Symmetric buckets around 0, roughly exponential width
BIN_EDGES = [
    -float("inf"),
    -2048,
    -512,
    -128,
    -32,
    32,
    128,
    512,
    2048,
    float("inf"),
]


# --- Streaming statistics helpers -------------------------------------------

def init_stats():
    return {
        "count": 0,
        "mean": 0.0,
        "M2": 0.0,          # for variance
        "min": None,
        "max": None,
        "pos": 0,
        "neg": 0,
        "zero": 0,
        "bins": [0] * (len(BIN_EDGES) - 1),
    }


def update_stats(stats: Dict[str, Any], x: int):
    # Welford's online algorithm for mean / variance
    n = stats["count"] + 1
    delta = x - stats["mean"]
    mean = stats["mean"] + delta / n
    delta2 = x - mean
    M2 = stats["M2"] + delta * delta2

    stats["count"] = n
    stats["mean"] = mean
    stats["M2"] = M2

    if stats["min"] is None or x < stats["min"]:
        stats["min"] = x
    if stats["max"] is None or x > stats["max"]:
        stats["max"] = x

    if x > 0:
        stats["pos"] += 1
    elif x < 0:
        stats["neg"] += 1
    else:
        stats["zero"] += 1

    # binning
    bi = bin_index(x)
    stats["bins"][bi] += 1


def finalize_stats(stats: Dict[str, Any]) -> Dict[str, Any]:
    n = stats["count"]
    if n > 1:
        variance = stats["M2"] / (n - 1)
    else:
        variance = 0.0
    stddev = math.sqrt(variance)

    bins = []
    for i, count in enumerate(stats["bins"]):
        a = BIN_EDGES[i]
        b = BIN_EDGES[i + 1]
        if a == -float("inf"):
            label = f"(-∞, {b})"
        elif b == float("inf"):
            label = f"[{a}, ∞)"
        else:
            label = f"[{a}, {b})"
        bins.append(
            {
                "range": label,
                "count": count,
                "fraction": count / n if n else 0.0,
            }
        )

    return {
        "count": n,
        "min": stats["min"],
        "max": stats["max"],
        "mean": stats["mean"],
        "stddev": stddev,
        "pos_fraction": stats["pos"] / n if n else 0.0,
        "neg_fraction": stats["neg"] / n if n else 0.0,
        "zero_fraction": stats["zero"] / n if n else 0.0,
        "bins": bins,
    }


def bin_index(x: int) -> int:
    # Find which bin [edge[i], edge[i+1]) x falls into
    for i in range(len(BIN_EDGES) - 1):
        if BIN_EDGES[i] <= x < BIN_EDGES[i + 1]:
            return i
    # Fallback (shouldn't happen)
    return len(BIN_EDGES) - 2


def analyze_stream(values: Iterable[int]) -> Dict[str, Any]:
    stats = init_stats()
    for v in values:
        update_stats(stats, v)
    return finalize_stats(stats)


# --- Data sources -----------------------------------------------------------

def iter_hashhelix_values() -> Iterable[int]:
    for path in LANE_FILES:
        try:
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    yield int(line)
        except FileNotFoundError:
            # If a lane is missing, we just skip it
            continue


def iter_uniform(n: int, lo: int, hi: int) -> Iterable[int]:
    for _ in range(n):
        yield random.randint(lo, hi)


def iter_normal(n: int, mu: float, sigma: float) -> Iterable[int]:
    for _ in range(n):
        yield int(round(random.gauss(mu, sigma)))


def iter_logistic(n: int, r: float = 3.99, x0: float = 0.123456) -> Iterable[int]:
    # Classic logistic map on (0,1), then scale to a modest integer range
    x = x0
    scale = 5000
    for _ in range(n):
        x = r * x * (1.0 - x)
        yield int(round((x - 0.5) * 2 * scale))  # roughly [-scale, scale]


def iter_sha256_ints(n: int) -> Iterable[int]:
    # Derive pseudorandom integers from SHA-256 of sequential seeds
    for i in range(n):
        h = hashlib.sha256(str(i).encode("utf-8")).digest()
        # Use first 4 bytes as signed 32-bit int
        raw = int.from_bytes(h[:4], byteorder="big", signed=True)
        yield raw


# --- ASCII helpers ----------------------------------------------------------

def make_ascii_section(label: str, stats: Dict[str, Any], bar_width: int = 60) -> str:
    lines = []
    lines.append(f"=== {label} ===")
    lines.append(
        f"n={stats['count']}, mean={stats['mean']:.6f}, stddev={stats['stddev']:.6f}, "
        f"pos={stats['pos_fraction']:.3f}, neg={stats['neg_fraction']:.3f}, zero={stats['zero_fraction']:.3f}"
    )
    lines.append("bins:")
    # Find max bin fraction for scaling
    max_frac = max((b["fraction"] for b in stats["bins"]), default=0.0)
    for b in stats["bins"]:
        frac = b["fraction"]
        if max_frac > 0:
            k = int(round(frac / max_frac * bar_width))
        else:
            k = 0
        bar = "#" * k
        lines.append(f"{b['range']:>12} | {bar} {frac:.4f}")
    lines.append("")  # blank line
    return "\n".join(lines)


# --- Main -------------------------------------------------------------------

def main():
    print("[OK] Building HashHelix entropy fingerprint…")

    # 1) Analyze the real HashHelix entropy lanes
    print("[*] Reading HashHelix entropy lanes…")
    hh_stats = analyze_stream(iter_hashhelix_values())
    total_n = hh_stats["count"]
    if total_n == 0:
        raise SystemExit("No entropy values found in hh_entropy_lane*.txt")

    print(f"[OK] HashHelix values: n={total_n}, mean={hh_stats['mean']:.6f}, stddev={hh_stats['stddev']:.6f}")

    # Decide sample size for baselines (keep it reasonable)
    baseline_n = min(200_000, total_n)
    lo = hh_stats["min"]
    hi = hh_stats["max"]
    mu = hh_stats["mean"]
    sigma = hh_stats["stddev"] or 1.0  # avoid zero

    print(f"[*] Using n={baseline_n} for baseline generators, range≈[{lo}, {hi}], mu≈{mu:.3f}, sigma≈{sigma:.3f}")

    # 2) Baseline distributions
    print("[*] Generating uniform baseline…")
    uniform_stats = analyze_stream(iter_uniform(baseline_n, lo, hi))

    print("[*] Generating normal baseline…")
    normal_stats = analyze_stream(iter_normal(baseline_n, mu, sigma))

    print("[*] Generating logistic-map baseline…")
    logistic_stats = analyze_stream(iter_logistic(baseline_n))

    print("[*] Generating SHA-256-derived baseline…")
    sha_stats = analyze_stream(iter_sha256_ints(baseline_n))

    # 3) Assemble fingerprint
    fingerprint = {
        "description": "HashHelix entropy fingerprint vs several baseline generators.",
        "bin_edges": BIN_EDGES,
        "distributions": {
            "hashhelix_entropy": hh_stats,
            "uniform_int": uniform_stats,
            "normal_int": normal_stats,
            "logistic_map": logistic_stats,
            "sha256_int": sha_stats,
        },
    }

    # 4) Write JSON
    with open(OUT_JSON, "w") as f:
        json.dump(fingerprint, f, indent=2)
    print(f"[OK] Fingerprint JSON written → {OUT_JSON}")

    # 5) Write ASCII report
    sections = []
    sections.append(make_ascii_section("HashHelix entropy", hh_stats))
    sections.append(make_ascii_section("Uniform int", uniform_stats))
    sections.append(make_ascii_section("Normal int", normal_stats))
    sections.append(make_ascii_section("Logistic map", logistic_stats))
    sections.append(make_ascii_section("SHA-256 int", sha_stats))

    ascii_report = "\n".join(sections)
    with open(OUT_ASCII, "w") as f:
        f.write(ascii_report)
    print(f"[OK] ASCII fingerprint written → {OUT_ASCII}")

    # Also print a short preview to the terminal
    print("\n--- ASCII Fingerprint (HashHelix vs baselines, first few lines) ---")
    for line in ascii_report.splitlines()[:25]:
        print(line)


if __name__ == "__main__":
    main()
