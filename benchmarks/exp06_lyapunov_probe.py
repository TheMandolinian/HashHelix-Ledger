import math
from dataclasses import dataclass


@dataclass
class LyapunovResult:
    steps: int
    delta0: float
    last_delta: float
    collapse_step: int | None
    avg_log_stretch: float | None


def wdtp_step_ner(a_prev: float, n: int) -> float:
    """
    Single WDTP step under the Numerical Evaluation Rule (NER):

        phase_n = (a_prev + pi/n) mod 2*pi
        a_n     = floor(n * sin(phase_n)) + 1

    a_prev is treated as a float but the output is effectively integer.
    """
    phase = (a_prev + math.pi / n) % (2.0 * math.pi)
    return math.floor(n * math.sin(phase)) + 1


def estimate_lyapunov(
    a1: float = 1.0,
    delta0: float = 1e-6,
    N: int = 100_000,
) -> LyapunovResult:
    """
    Two-orbit Lyapunov probe for WDTP + NER.
    """
    a = a1
    a_pert = a1 + delta0

    delta_prev = delta0
    log_stretch_sum = 0.0
    stretch_count = 0
    collapse_step: int | None = None

    for n in range(2, N + 1):
        a = wdtp_step_ner(a, n)
        a_pert = wdtp_step_ner(a_pert, n)

        delta = abs(a_pert - a)

        if delta == 0.0:
            # Trajectories have merged; perturbation fully crushed
            collapse_step = n
            break

        # Local stretching factor and log-accumulation
        stretch = delta / delta_prev
        log_stretch_sum += math.log(stretch)
        stretch_count += 1

        delta_prev = delta

    avg_log_stretch = None
    if stretch_count > 0:
        avg_log_stretch = log_stretch_sum / stretch_count

    return LyapunovResult(
        steps=n,
        delta0=delta0,
        last_delta=delta_prev,
        collapse_step=collapse_step,
        avg_log_stretch=avg_log_stretch,
    )


if __name__ == "__main__":
    result = estimate_lyapunov()

    print("Experiment 6 — Lyapunov Exponent Probe (WDTP + NER)")
    print(f"  initial delta      = {result.delta0:.3e}")
    print(f"  steps simulated    = {result.steps}")
    print(f"  last nonzero delta = {result.last_delta:.3e}")
    print(f"  collapse step      = {result.collapse_step}")
    if result.avg_log_stretch is not None:
        print(f"  avg log(stretch)   = {result.avg_log_stretch:.6f}")
        if result.avg_log_stretch > 0:
            print("  Lyapunov sign      = chaotic (λ > 0)")
        elif result.avg_log_stretch < 0:
            print("  Lyapunov sign      = contracting (λ < 0)")
        else:
            print("  Lyapunov sign      = neutral (λ ≈ 0)")
    else:
        print("  No nonzero separation steps; perturbation collapsed immediately.")
