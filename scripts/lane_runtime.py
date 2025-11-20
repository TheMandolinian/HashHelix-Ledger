#!/usr/bin/env python3
"""
HashHelix — Stage 8
Lane Runtime Generator

Purpose:
- Deterministic recurrence execution
- Multi-lane generation
- Sequential and simulated-parallel modes
- Raw lane traces only (one integer per line)
- No timestamps, no randomness → bit-for-bit reproducible
"""

import argparse
import math
from pathlib import Path


def hh_step(prev_a: int, n: int) -> int:
    """
    HashHelix Temporal Primitive (HTP) step function.

    a_1 = seed (integer)
    a_n = floor(n * sin(a_{n-1} + pi / n)) + 1
    """
    return math.floor(n * math.sin(prev_a + math.pi / n)) + 1


def generate_lane_sequential(
    lane_id: int,
    steps: int,
    seed: int,
    out_dir: Path,
) -> None:
    """
    Generate a single lane in sequential mode:
    - n counts from 1..steps for this lane only
    - Output: one integer per line
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    lane_path = out_dir / f"lane{lane_id:02d}.txt"

    a = int(seed)
    with lane_path.open("w", encoding="utf-8") as f:
        # n = 1
        f.write(f"{a}\n")
        # n = 2..steps
        for n in range(2, steps + 1):
            a = hh_step(a, n)
            f.write(f"{a}\n")


def generate_lanes_sequential(
    lanes: int,
    steps: int,
    seed: int,
    seed_stride: int,
    out_dir: Path,
) -> None:
    """
    Sequential multi-lane:
    - Each lane runs independently from n=1..steps
    - Lane k uses seed = seed + (k-1)*seed_stride
    """
    for lane_id in range(1, lanes + 1):
        lane_seed = seed + (lane_id - 1) * seed_stride
        generate_lane_sequential(
            lane_id=lane_id,
            steps=steps,
            seed=lane_seed,
            out_dir=out_dir,
        )


def generate_lanes_parallel(
    lanes: int,
    steps: int,
    seed: int,
    seed_stride: int,
    out_dir: Path,
    write_interleaved: bool = True,
) -> None:
    """
    Simulated parallel multi-lane:
    - All lanes advance in lockstep with the same n (global step index).
    - For each n, every lane takes one step.
    - Produces:
        - laneXX.txt for each lane
        - (optional) lanes_interleaved.txt with: n, lane_id, value
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    # Initialize per-lane state
    lane_states = []
    lane_files = []
    for lane_id in range(1, lanes + 1):
        lane_seed = seed + (lane_id - 1) * seed_stride
        lane_states.append(int(lane_seed))
        lane_path = out_dir / f"lane{lane_id:02d}.txt"
        lane_files.append(lane_path.open("w", encoding="utf-8"))

    interleaved_file = None
    if write_interleaved:
        interleaved_path = out_dir / "lanes_interleaved.txt"
        interleaved_file = interleaved_path.open("w", encoding="utf-8")

    try:
        # n = 1
        n = 1
        for lane_id in range(1, lanes + 1):
            a = lane_states[lane_id - 1]
            lane_files[lane_id - 1].write(f"{a}\n")
            if interleaved_file is not None:
                interleaved_file.write(f"{n},{lane_id},{a}\n")

        # n = 2..steps
        for n in range(2, steps + 1):
            for lane_id in range(1, lanes + 1):
                idx = lane_id - 1
                prev_a = lane_states[idx]
                a = hh_step(prev_a, n)
                lane_states[idx] = a
                lane_files[idx].write(f"{a}\n")
                if interleaved_file is not None:
                    interleaved_file.write(f"{n},{lane_id},{a}\n")

    finally:
        for f in lane_files:
            f.close()
        if interleaved_file is not None:
            interleaved_file.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "HashHelix Stage 8 — Lane Runtime\n"
            "Deterministic lane sequence generator."
        )
    )
    parser.add_argument(
        "--lanes",
        type=int,
        default=1,
        help="Number of lanes to generate (default: 1).",
    )
    parser.add_argument(
        "--steps",
        type=int,
        required=True,
        help="Number of steps per lane (n from 1..steps).",
    )
    parser.add_argument(
        "--mode",
        choices=["sequential", "parallel"],
        default="sequential",
        help="Generation mode (default: sequential).",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default="data/runtime/lanes",
        help="Output directory for lane traces (default: data/runtime/lanes).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=1,
        help="Base seed a_1 for lane 1 (default: 1).",
    )
    parser.add_argument(
        "--seed-stride",
        type=int,
        default=0,
        help=(
            "Per-lane seed increment. "
            "Lane k uses seed + (k-1)*seed_stride (default: 0)."
        ),
    )
    parser.add_argument(
        "--no-interleaved",
        action="store_true",
        help="Disable lanes_interleaved.txt in parallel mode.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)

    if args.lanes < 1:
        raise ValueError("lanes must be >= 1")
    if args.steps < 1:
        raise ValueError("steps must be >= 1")

    if args.mode == "sequential":
        generate_lanes_sequential(
            lanes=args.lanes,
            steps=args.steps,
            seed=args.seed,
            seed_stride=args.seed_stride,
            out_dir=out_dir,
        )
    else:
        generate_lanes_parallel(
            lanes=args.lanes,
            steps=args.steps,
            seed=args.seed,
            seed_stride=args.seed_stride,
            out_dir=out_dir,
            write_interleaved=not args.no_interleaved,
        )


if __name__ == "__main__":
    main()
