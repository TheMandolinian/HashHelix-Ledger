"""
Stage 4 Master Execution Harness (S4-MEH)

Orchestrates all Stage 4 stability / integrity runs:

  - Runtime Stress
  - Long-Horizon Behavior Tests
  - Verification Pressure Tests
  - Adversarial Scenario Simulations

Guarantees:
  - Deterministic ordering of runs
  - Recurrence is never modified here
  - Past stages are never touched
  - All outputs are mirrored into:
        hh_tmp/stage4_stability/master/
  - A final combined JSON report:
        hh_tmp/stage4_stability/master/stage4_report_*.json
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


# --- Paths & constants -------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

PYTHON_EXE = "python"  # rely on venv / PATH

STAGE4_TMP_ROOT = ROOT / "hh_tmp" / "stage4_stability"
MASTER_OUT_DIR = STAGE4_TMP_ROOT / "master"


@dataclass
class Stage4JobSpec:
    key: str
    label: str
    script: str  # relative to research/
    expected_json: Path  # where the job writes its primary JSON


# NOTE:
# These JSON paths assume each Stage 4 script already writes a canonical
# report into hh_tmp/stage4_stability/<job_key>/...json.
# If the filenames differ, you only need to adjust `expected_json` below
# — no changes to the recurrence or other stages.
JOBS: List[Stage4JobSpec] = [
    Stage4JobSpec(
        key="runtime_stress",
        label="Stage 4 Runtime Stress",
        script="stage4_runtime_stress.py",
        expected_json=STAGE4_TMP_ROOT
        / "runtime_stress"
        / "stage4_runtime_stress_report.json",
    ),
    Stage4JobSpec(
        key="long_horizon",
        label="Stage 4 Long-Horizon Behavior",
        script="stage4_long_horizon.py",
        expected_json=STAGE4_TMP_ROOT
        / "long_horizon"
        / "stage4_long_horizon_plan.json",
    ),
    Stage4JobSpec(
        key="verification_pressure",
        label="Stage 4 Verification Pressure",
        script="stage4_verification_pressure.py",
        expected_json=STAGE4_TMP_ROOT
        / "verification_pressure"
        / "stage4_verification_pressure_report.json",
    ),
    Stage4JobSpec(
        key="adversarial_scenarios",
        label="Stage 4 Adversarial Scenarios",
        script="stage4_adversarial_scenarios.py",
        expected_json=STAGE4_TMP_ROOT
        / "adversarial_scenarios"
        / "stage4_adversarial_report.json",
    ),
]


# --- Harness logic -----------------------------------------------------------


def run_job(job: Stage4JobSpec) -> Dict[str, Any]:
    """
    Run a single Stage 4 script in a deterministic way, load its JSON output,
    and mirror that JSON into the master directory.

    This does NOT alter the recurrence or earlier stages; it only:
      - invokes the existing Stage 4 script
      - reads its JSON file
      - copies structured results into the master summary
    """
    script_path = ROOT / "research" / job.script

    if not script_path.exists():
        raise FileNotFoundError(f"Stage 4 script not found: {script_path}")

    print(f"[S4-MEH] Running {job.label} via {script_path} ...")

    # Deterministic ordering: jobs are run in the order listed in JOBS.
    completed = subprocess.run(
        [PYTHON_EXE, str(script_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    # Ensure the expected JSON file exists after the run
    if not job.expected_json.exists():
        raise FileNotFoundError(
            f"Expected JSON output for {job.label} "
            f"not found at {job.expected_json}"
        )

    # Load the job's native JSON
    with job.expected_json.open("r", encoding="utf-8") as f:
        job_data = json.load(f)

    # Mirror the raw job JSON into the master folder under a stable name
    MASTER_OUT_DIR.mkdir(parents=True, exist_ok=True)
    master_job_json = MASTER_OUT_DIR / f"{job.key}.json"
    with master_job_json.open("w", encoding="utf-8") as f:
        json.dump(job_data, f, indent=2, sort_keys=True)

    print(f"[S4-MEH] {job.label} JSON mirrored → {master_job_json}")

    
       # Convert job dataclass to plain dict, but ensure all paths are strings
    job_info = asdict(job)
    job_info["expected_json"] = str(job.expected_json.relative_to(ROOT))

    return {
        "job": job_info,
        "source_json": str(job.expected_json.relative_to(ROOT)),
        "master_json": str(master_job_json.relative_to(ROOT)),
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "ok": completed.returncode == 0,
    }



def main() -> None:
    """
    Run all Stage 4 jobs and produce a combined stability report JSON
    in hh_tmp/stage4_stability/master/.
    """
    MASTER_OUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    report_path = MASTER_OUT_DIR / f"stage4_report_{timestamp}.json"

    print("[S4-MEH] Starting Stage 4 Master Execution Harness...")
    print(f"[S4-MEH] Master output directory: {MASTER_OUT_DIR}")

    job_summaries: List[Dict[str, Any]] = []

    for job in JOBS:
        summary = run_job(job)
        job_summaries.append(summary)

    combined: Dict[str, Any] = {
        "meta": {
            "kind": "hashhelix_stage4_master_report",
            "timestamp_utc": timestamp,
            "root": str(ROOT),
            "tmp_root": str(STAGE4_TMP_ROOT),
            "master_dir": str(MASTER_OUT_DIR),
            "jobs_count": len(JOBS),
        },
        "jobs": job_summaries,
    }

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, sort_keys=True)

    print(f"[S4-MEH] Combined Stage 4 report written → {report_path}")


if __name__ == "__main__":
    main()
