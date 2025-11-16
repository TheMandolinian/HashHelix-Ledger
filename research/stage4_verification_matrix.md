# Stage 4 — Verification & Adversarial Scenario Matrix

This matrix describes the high-level verification and adversarial scenarios  
for the Stability & Integrity Phase.

It is intentionally non-mathematical and focuses on behavior, expectations,  
and where artifacts are written.

---

## Table Legend

- **Scenario ID** — Short handle for referencing the scenario.
- **Category** — Runtime Stress / Long-Horizon / Verification / Adversarial.
- **Description** — What we are doing in plain language.
- **Inputs** — Which lanes, epochs, or files are involved.
- **Expected Evidence of Integrity** — What “success” looks like.
- **Artifacts** — Where logs, JSON, and notes are stored.

---

## Scenario Matrix

| Scenario ID | Category       | Description                                                | Inputs                                      | Expected Evidence of Integrity                                                | Artifacts Path                                                 |
|------------|----------------|------------------------------------------------------------|---------------------------------------------|-------------------------------------------------------------------------------|----------------------------------------------------------------|
| S4-RS-01   | Runtime Stress | Short, intense multi-lane run with heavy logging          | Existing lane configs; fresh temp logs      | No crashes; consistent lane progression; logs complete and readable          | `hh_tmp/stage4_stability/runtime_stress/`                      |
| S4-RS-02   | Runtime Stress | Single-lane “max speed” run with minimal logging          | Single lane config                          | Stable run; no partial writes; run metadata captured                         | `hh_tmp/stage4_stability/runtime_stress/`                      |
| S4-LH-01   | Long-Horizon   | Extended single-lane run over large N                     | Chosen lane; previously verified epochs     | Clean checkpoints; no drift in index tracking; snapshots line up with epochs | `hh_tmp/stage4_stability/long_horizon/`                        |
| S4-LH-02   | Long-Horizon   | Multi-lane long-horizon run with periodic snapshots       | Multiple lanes; epoch combiner              | Each snapshot verifies; no missing epochs; cross-lane linkage remains sound  | `hh_tmp/stage4_stability/long_horizon/`                        |
| S4-VP-01   | Verification   | Replay verification using complete, untampered data       | Historical epochs and logs                  | All checks pass; no unexpected warnings or errors                            | `hh_tmp/stage4_stability/verification_pressure/`               |
| S4-VP-02   | Verification   | Verification with a deliberately missing epoch file       | Ledger minus one epoch                      | Verification flags the missing piece clearly and quickly                     | `hh_tmp/stage4_stability/verification_pressure/`               |
| S4-VP-03   | Verification   | Verification with a truncated log                         | One log file manually shortened             | Verification detects inconsistency and reports it without crashing           | `hh_tmp/stage4_stability/verification_pressure/`               |
| S4-AD-01   | Adversarial    | Tampered record ordering inside an existing epoch         | Copy of an epoch with lines reordered       | Verification fails the epoch and explains that ordering is inconsistent      | `hh_tmp/stage4_stability/adversarial/`                         |
| S4-AD-02   | Adversarial    | Inserted extra records into a historical log              | Modified copy of a log file                 | Verification detects additional entries and refuses to accept the log        | `hh_tmp/stage4_stability/adversarial/`                         |
| S4-AD-03   | Adversarial    | Overwritten hash or state fields in a prior record        | Manually edited epoch or lane file          | Verification detects mismatch vs recomputed values                           | `hh_tmp/stage4_stability/adversarial/`                         |

---

## Notes

- This matrix is a **living document**.  
  You can add, remove, or refine scenarios as Stage 4 evolves.

- Actual implementations for each scenario will live in:
  - `research/stage4_runtime_stress.py`
  - `research/stage4_long_horizon.py`
  - `research/stage4_verification_pressure.py`
  - `research/stage4_adversarial_scenarios.py`

- The core recurrence and prior stages remain unchanged.  
  All scenarios operate on existing ledger rules and data.
