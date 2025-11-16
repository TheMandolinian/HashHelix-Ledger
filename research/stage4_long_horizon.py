"""
Stage 4 — Long-Horizon Behavior Plan

This script is responsible for defining and recording **long-duration**
or high-step-count experiments against the HashHelix engine.

Goals (engineering-facing):

- Describe a set of long-horizon test plans (not the math, just the runs).
- Keep the description deterministic and reproducible.
- Emit a canonical JSON plan that the Stage 4 Master Execution Harness (S4-MEH)
  can reference and mirror.

This script:
- MUST NOT change the core recurrence.
- MUST NOT modify prior stages or historical data.
- SHOULD write all scratch artifacts under:
    hh_tmp/stage4_stability/long_horizon/
"""

from pathlib import Path
import json
import time
import argparse
from typing import Any, Dict, List


LONG_HORIZON_ROOT = Path("hh_tmp/stage4_stability/long_horizon")


def ensure_directories() -> None:
    """Ensure that the Stage 4 long-horizon directories exist."""
    LONG_HORIZON_ROOT.mkdir(parents=True, exist_ok=True)


def write_long_horizon_plan(plan: Dict[str, Any]) -> Path:
    """
    Write the canonical Stage 4 long-horizon plan JSON expected by S4-MEH.
    """
    ensure_directories()

    out_path = LONG_HORIZON_ROOT / "stage4_long_horizon_plan.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)

    print(f"[Stage 4] Long-horizon plan JSON written → {out_path}")
    return out_path


def parse_args() -> argparse.Namespace:
    """
    Parse CLI arguments for the long-horizon planner.

    These arguments describe *how many* long runs and their rough sizes,
    but they do not run the engine themselves.
    """
    parser = argparse.ArgumentParser(
        description="Stage 4: Long-horizon behavior planning for HashHelix."
    )
    parser.add_argument(
        "--profiles",
        nargs="+",
        default=["baseline_1M", "baseline_10M"],
        help="Named long-horizon profiles (e.g., baseline_1M, baseline_10M).",
    )
    parser.add_argument(
        "--lanes",
        type=int,
        default=3,
        help="Number of lanes to include in each long-horizon profile.",
    )
    return parser.parse_args()


def build_plan(profiles: List[str], lanes: int) -> Dict[str, Any]:
    """
    Construct a deterministic long-horizon test plan.

    This is purely descriptive metadata — it tells downstream tools
    what to run, but does not perform the runs itself.
    """
    timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())

    # Simple, descriptive entries for now. We can refine later without
    # changing the overall structure expected by the master harness.
    runs: List[Dict[str, Any]] = []
    for name in profiles:
        runs.append(
            {
                "profile": name,
                "lanes": lanes,
                "notes": "Long-horizon profile definition only; engine wiring occurs in a later stage.",
            }
        )

    plan: Dict[str, Any] = {
        "script": "stage4_long_horizon.py",
        "generated_at_local": timestamp,
        "profiles": profiles,
        "lanes": lanes,
        "runs": runs,
        "status": "plan-defined",
    }
    return plan


def main() -> None:
    args = parse_args()
    plan = build_plan(args.profiles, args.lanes)
    write_long_horizon_plan(plan)


if __name__ == "__main__":
    main()
