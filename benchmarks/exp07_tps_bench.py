import time
from hashlib import sha256
import math

# --- WDTP + NER recurrence ---
def wdtp_step(a_prev, n):
    # Numerical Evaluation Rule (NER)
    phase = (a_prev + math.pi / n) % (2 * math.pi)
    return int(n * math.sin(phase)) + 1

# --- HashHelix primitive (public-engine compliant) ---
def helix_hash(prev_hash: bytes, payload: bytes, n: int, a_prev: int):
    # Compute next WDTP value
    a_new = wdtp_step(a_prev, n)

    # Hash: SHA-256(prev_hash || payload || n || a_prev)
    h = sha256()
    h.update(prev_hash)
    h.update(payload)
    h.update(n.to_bytes(8, "big"))
    h.update(a_prev.to_bytes(8, "big"))
    new_hash = h.digest()

    return new_hash, a_new


# ----------------------------------------------------
#  TPS Benchmark (HashHelix Engine)
# ----------------------------------------------------
def benchmark_hashhelix(entries=1_000_000):
    payload = b"sample_experiment_result_42"  # fixed payload for fair comparison
    prev_hash = b"\x00" * 32
    a = 1
    n_start = 2

    start = time.perf_counter()

    for n in range(n_start, n_start + entries):
        prev_hash, a = helix_hash(prev_hash, payload, n, a)

    end = time.perf_counter()

    duration = end - start
    tps = entries / duration

    print("\nHashHelix Core Engine Benchmark")
    print("--------------------------------")
    print(f"Entries processed : {entries:,}")
    print(f"Time taken        : {duration:.6f} seconds")
    print(f"TPS               : {tps:,.0f}")
    print(f"Avg per entry     : {duration/entries*1000:.6f} ms\n")

    return tps


if __name__ == "__main__":
    benchmark_hashhelix(1_000_000)
