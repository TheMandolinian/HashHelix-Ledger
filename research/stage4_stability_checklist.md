# Stage 4 — Stability & Integrity Checklist

This is a practical to-do list for Stage 4.  
Check items off as code, logs, and writeups are completed.

---

## A. Runtime Stress (Short, Intense Runs)

- [ ] Define initial runtime stress profiles:
  - [ ] Single-lane high-speed appends
  - [ ] Multi-lane concurrent appends
  - [ ] Heavy log-writing scenarios
- [ ] Implement `research/stage4_runtime_stress.py` scaffolding
- [ ] Decide what gets logged to:
  - [ ] `hh_tmp/stage4_stability/runtime_stress/`
- [ ] Run first small-scale stress tests
- [ ] Capture initial observations in a short note or comment block

---

## B. Long-Horizon Experiments

- [ ] Decide on long-horizon targets:
  - [ ] Step counts (e.g., N ranges)
  - [ ] Wall-clock durations (e.g., hours/days)
- [ ] Implement `research/stage4_long_horizon.py` scaffolding
- [ ] Design periodic snapshots:
  - [ ] Where snapshots are stored
  - [ ] What summary stats are recorded (non-math, descriptive)
- [ ] Run at least one long-horizon test
- [ ] Record behavior and any anomalies in:
  - [ ] `hh_tmp/stage4_stability/long_horizon/`
  - [ ] A short written summary

---

## C. Verification Pressure Tests

- [ ] Enumerate verification scenarios:
  - [ ] Complete data — “happy path”
  - [ ] Missing epochs or files
  - [ ] Truncated or corrupted logs
- [ ] Implement `research/stage4_verification_pressure.py` scaffolding
- [ ] Define expected outcomes for each scenario in human language
- [ ] Run tests against existing epochs / logs
- [ ] Document:
  - [ ] What the verification layer detects reliably
  - [ ] Any blind spots or confusing behaviors

---

## D. Adversarial Scenarios

- [ ] Brainstorm “what if someone tries THIS?” list:
  - [ ] Editing existing files between runs
  - [ ] Reordering lines or records
  - [ ] Injecting extra entries
- [ ] Implement `research/stage4_adversarial_scenarios.py` scaffolding
- [ ] Create sample tampered artifacts in:
  - [ ] `hh_tmp/stage4_stability/adversarial/`
- [ ] Observe which tampering attempts are:
  - [ ] Immediately detected
  - [ ] Subtle but detectable
  - [ ] Need stronger defenses or better tooling

---

## E. Logging & Artifact Hygiene

- [ ] Decide logging format for Stage 4 (JSON lines, text summaries, or both)
- [ ] Add simple run metadata:
  - [ ] Timestamp
  - [ ] Script name
  - [ ] Parameters for the run
- [ ] Ensure all Stage 4 scripts:
  - [ ] Can run without modifying prior data or epochs
  - [ ] Fail safely if directories are missing
  - [ ] Are documented in their top-level docstrings

---

## F. Documentation & Wrap-Up

- [ ] Update this checklist as items evolve
- [ ] Summarize Stage 4 findings in:
  - [ ] `research/stage4_stability_overview.md` (final section)
  - [ ] Any benchmark notes under `benchmarks/`
- [ ] Decide which Stage 4 artifacts become:
  - [ ] Permanent “relics”
  - [ ] Temporary scratch data
