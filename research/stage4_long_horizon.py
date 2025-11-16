"""
Stage 4 — Long-Horizon Behavior Harness

This script is responsible for **long-duration** experiments with the existing
HashHelix engine.

Goals:

- Run one or more lanes for large step counts and/or long wall-clock durations.
- Periodically snapshot the state in a human-readable and machine-readable way.
- Observe whether any stability issues appear over time.

Constraints:

- The core recurrence must remain unchanged.
- No prior epochs or relics should be modified.
- All new artifacts should live under:
    hh_tmp/stage4_stability/long_horizon/
"""

from pathlib import Path
import json
import time
import argparse
from typing import Any, Dict


LONG_HORIZON_ROOT = Path("hh_tmp/stage4_stability/long_horizon")


def ensure_directories() -> None:
    LONG_HORIZON_ROOT.mkdir(parents=True, exist_ok=True)


def record_snapshot(metadata: Dict[str, Any]) -> Path:
    """
    Write a snapshot JSON file describing the current long-horizon run state.

    Actual lane state and statistics will be added later.
    """
    ensure_directories()
    timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    out_path = LONG_HORIZON_ROOT / f"long_horizon_snapshot_{timestamp}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    return out_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage 4: Long-horizon behavior harness for HashHelix."
    )
    parser.add_argument(
        "--label",
        default="baseline",
        help="Label for this long-horizon run (e.g., lane01_baseline).",
    )
    parser.add_argument(
        "--target-steps",
        type=int,
        default=1_000_000,
        help="Nominal step target for the long-horizon run.",
    )
    parser.add_argument(
        "--snapshot-interval-steps",
        type=int,
        default=100_000,
        help="Interval (in steps) between snapshots.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # TODO: Replace this placeholder block with real lane stepping logic.
    # For now, just emit an initial scaffolding snapshot.

    metadata = {
        "script": "stage4_long_horizon.py",
        "label": args.label,
        "target_steps": args.target_steps,
        "snapshot_interval_steps": args.snapshot_interval_steps,
        "start_time_unix": time.time(),
        "notes": "Stage 4 long-horizon scaffolding only. Lane evolution TBD.",
    }

    out_path = record_snapshot(metadata)
    print(f"[Stage 4] Long-horizon snapshot written → {out_path}")


if __name__ == "__main__":
    main()
