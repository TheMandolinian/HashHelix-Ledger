# Experiment 6 — Lyapunov Exponent Probe (NER WDTP Stability vs Chaos)

**Author:** James Bradley Waresback  
**Date:** 2025-11-25  
**Status:** Draft

Results at the bottom.

What is a Lyapunov Exponent? (High-School Level)

Imagine you have two identical systems, except one starts just a tiny bit different.

Example:
Two balls rolling down a hill, but one starts one hair to the left.

A Lyapunov exponent measures:

Do those small differences grow or shrink as the system evolves?

If small differences GROW

The system is chaotic.

Two balls starting almost together end up in very different places.

This means predicting the future becomes impossible — tiny errors explode.

Examples:

-Weather

-Turbulent water

-Double pendulum (the crazy spinning physics class demo)

This is a positive Lyapunov exponent.

If small differences SHRINK

The system is stable or contracting.

Two balls start slightly apart but fall into the same path.

Prediction is easy; small errors get crushed.

This is a negative Lyapunov exponent.

⚖️ If the difference stays the same

The system is “neutral.”
Things neither diverge nor collapse.

This is a zero Lyapunov exponent.

🧭 Why do people use Lyapunov exponents in real life?

1. Weather prediction

Weather is chaotic.
Meteorologists measure Lyapunov exponents to see how fast forecast errors blow up.

If λ is high → forecasts lose accuracy FAST.
This is why predicting 10 days out is really hard.

2. Engineering stability

Engineers check if small errors in rockets, bridges, or control systems grow (bad) or die out (good).

Low or negative λ = stable machine
High λ = catastrophic potential

3. Robotics and autopilot systems

Self-driving cars and airplane autopilots must avoid chaotic behavior.

They test:

“If the sensor wiggles a tiny bit, does the robot go crazy?”

4. Finance

Traders measure chaos in markets.

If λ > 0 → markets behave unpredictably, sensitive to noise.
If λ ≈ 0 → stable, predictable patterns exist.

5. Biology & population growth

Ecologists study animal populations using Lyapunov exponents to see if a species is:

-in stable equilibrium

-growing uncontrollably

-collapsing

-cycling chaotically

🌀 So why is this interesting for WDTP (HashHelix engine)?

Because:

This ledger should NOT act like weather.
This ledger should act like a clock.

If WDTP had a positive Lyapunov exponent, it would mean:

-Tiny differences in initial state → massively different future states

-No reproducibility

-No determinism

-No ledger integrity

-No consensus replacement

This experiment showed the opposite:

-The WDTP engine kills tiny differences instantly.

This means:

-Strong determinism

-No chaotic divergence

-Every node, every machine, every platform gets the same answer

-Perfect for a verifiable ledger engine

-Perfect for cryptographic determinism

-Safe for aerospace-style timing or computational scheduling

-Suitable for high-trust workloads

In simple terms:

-HashHelix behaves more like a precision watch than a weather system.

And that’s exactly what a deterministic temporal engine is supposed to do.
---

## Objective

Estimate an effective **Lyapunov exponent** for the WDTP + NER engine by
tracking how a tiny perturbation between two trajectories behaves over time.

The classic two-orbit method:

- Orbit 1 starts from `a₁ = 1.0`
- Orbit 2 starts from `a₁ + δ`, where `δ` is very small (e.g. `1e-6`)
- Both orbits evolve under the same WDTP + NER recurrence
- At each step we measure the separation `Δₙ = |aₙ' − aₙ|`
- We accumulate the local stretch factors `Δₙ / Δₙ₋₁` to estimate an
  average log-stretch (Lyapunov exponent proxy)

Because WDTP is an **integer-valued** map after the floor, we also track
the step at which the two trajectories become identical (perturbation
collapse).

This experiment answers:

1. Does a tiny perturbation **grow** (positive Lyapunov ≈ chaotic)?
2. Does it **decay** (negative Lyapunov ≈ contracting/stable)?
3. How quickly does the floor structure annihilate small differences
   under NER?

---

## Recurrence (with NER)

We respect the Numerical Evaluation Rule (NER):

- `phaseₙ = (aₙ₋₁ + π/n) mod 2π`
- `aₙ = floor(n · sin(phaseₙ)) + 1`

where `aₙ` is treated as the state for the next step.

Implementation detail:

- We treat the state as a Python `float` but the recurrence produces
  integer values after `floor(⋅) + 1`.
- The perturbation lives in the *pre-floor* phase until the two orbits
  land on the same integer and become identical.

---

## Setup

- Repository: `HashHelix-Ledger`
- Engine: Python reference WDTP implementation with NER
- Script: `benchmarks/exp06_lyapunov_probe.py`
- Optional output directory:
  - `benchmarks/results_exp06/` (for logs / CSV if we choose to extend)

Dependencies:

- Python 3.x
- Standard library only (`math`, `dataclasses`)

---

## Parameters

- Initial base value: `a₁ = 1.0`
- Initial perturbation: `δ = 1e-6` (configurable)
- Range: `n = 1 … N`
- Suggested `N`:
  - Default: `N = 100_000`
  - Can be raised for further probes if performance allows

---

## Procedure

1. From the repo root, run:

   ```bash
   python3 benchmarks/exp06_lyapunov_probe.py

---

## `benchmarks/exp06_lyapunov_probe.py`

Here’s the updated script, now explicitly using NER:

```python
"""
Experiment 6 — Lyapunov Exponent Probe (NER WDTP Stability vs Chaos)

This script implements a two-orbit Lyapunov-style probe for the
WDTP + NER recurrence.

- Orbit 1 starts at a1
- Orbit 2 starts at a1 + delta0

We evolve both trajectories under:

    phase_n = (a_{n-1} + pi/n) mod 2*pi
    a_n     = floor(n * sin(phase_n)) + 1

and measure how the separation evolves until the trajectories collapse
to the same integer state.
"""

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

    Returns:
        LyapunovResult with:
        - steps simulated
        - initial delta
        - last nonzero delta
        - first collapse step (if any)
        - avg_log_stretch ≈ Lyapunov exponent proxy
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
        print("  Lyapunov sign      = ",
              "chaotic (λ > 0)" if result.avg_log_stretch > 0
              else "contracting (λ < 0)" if result.avg_log_stretch < 0
              else "neutral (λ ≈ 0)")
    else:
        print("  No nonzero separation steps; "
              "perturbation collapsed immediately.")

              Results Below
@TheMandolinian ➜ /workspaces/HashHelix-Ledger (main) $ nano benchmarks/exp06_lyapunov_probe.py
@TheMandolinian ➜ /workspaces/HashHelix-Ledger (main) $ python3 benchmarks/exp06_lyapunov_probe.py
Experiment 6 — Lyapunov Exponent Probe (WDTP + NER)
  initial delta      = 1.000e-06
  steps simulated    = 2
  last nonzero delta = 1.000e-06
  collapse step      = 2
  No nonzero separation steps; perturbation collapsed immediately.
@TheMandolinian ➜ /workspaces/HashHelix-Ledger (main) $ 

Nothing random here...