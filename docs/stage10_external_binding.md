# Stage 10 — External Engine Binding  
**HashHelix Ledger — Engine Contract Specification**  
**Author:** James Bradley Waresback  
**Status:** Draft (Stage 10 Lane)

---

## 1. Purpose

Stage 10 establishes a **universal engine contract** so that any external runtime  
(Rust, C, CUDA, FPGA, WASM, or distributed cluster) can execute HashHelix lanes,  
epochs, and relics *without modifying the ledger repository*.  

The contract is:

- **Language-agnostic**
- **CLI-based (Stage 10)**
- **JSON in / JSON out**
- Fully compatible with:
  - Stage 5: Lane / Epoch / Relic schemas  
  - Stage 6: Seal helper & bundle rules  
  - Stage 7: Master Validator pipeline  
  - Stage 9: Anchor Envelope ingestion  

This file does **not** describe Rust/FI implementations.  
It defines **what an engine must do** to be considered compliant.

---

## 2. Engine Invocation Contract (CLI Mode)

A compliant engine **must** be runnable as a CLI binary or script:


engine_binary --manifest path/to/engine_binding.stage10.json
--input path/to/input.json
--output path/to/output.json


### 2.1 Required Flags

| Flag        | Description |
|-------------|-------------|
| `--manifest` | Path to engine binding manifest (stage10 schema) |
| `--input`    | Lane manifest / epoch request / relic request |
| `--output`   | File path the engine must write its JSON results to |

### 2.2 Exit Codes

| Code | Meaning |
|------|---------|
| `0`  | Success, output conforms to schema |
| `1`  | Input file missing or invalid |
| `2`  | Manifest invalid or unsupported feature |
| `3`  | Engine internal error |
| `4`  | Output failed schema validation |

All compliant engines must use these codes.

---

## 3. Input Specification

The engine may be invoked on one of the following input types:

### 3.1 Lane Generation Request  
Uses:  
- `lane-metadata.stage5.json`  
- Lane seed, nStart, nEnd

### 3.2 Epoch Bundle Request  
Uses:  
- `lane-artifact.stage5.json`  
- Range of n that constitutes one epoch

### 3.3 Relic Bundle Request  
Uses:  
- `hashBundle.stage5.json`

All JSON input fed into the engine must be **unmodified Stage 5/6/7 JSON**.

---

## 4. Output Specification

A compliant engine must emit:

- **Lane artifact JSON** (for lane requests)  
- **Epoch bundle JSON** (for epoch requests)  
- **Relic bundle JSON** (for relic requests)

And it must follow:

- Stage 5 structural rules  
- Stage 6 sealing rules  
- Stage 7 master-validator compatibility  

The master validator will treat the output the same whether it comes  
from Python, Rust, or another runtime.

---

## 5. Reference Engine (Stage 10 Python Shim)

A minimal reference engine is provided in:

scripts/engine_binding_ref.py


This shim:

- Reads the manifest  
- Loads input JSON  
- Executes the Stage 1–3 recurrence using the Python primitive  
- Generates a tiny example epoch  
- Emits valid Stage 5/6/7 output  
- Returns exit code 0 on success  

This script acts as **the canonical example** that future Rust/C engines  
must exactly replicate.

---

## 6. Engine Binding Manifest (Stage 10)

The schema in:

schemas/engine_binding.stage10.json


Defines:

- `engineId`  
- `version`  
- `binaryPath`  
- `apiMode` = `"cli"`  
- `inputSpec` / `outputSpec`  
- Optional performance hints (threads, GPUs, lanes supported)

This allows the ledger to declare which engine produced which artifact.

---

## 7. Modes

### 7.1 Batch Mode (Stage 10)  
Simple offline operation.  
Engine runs once, produces JSON, exits.

### 7.2 Streaming Mode (Future Stage)  
Possible future extension to stream n-values to stdout or pipe.  
Stage 10 documents only the concept, not the implementation.

---

## 8. Validation Pipeline

Stage 10 adds a CI workflow:

.github/workflows/validate-stage10.yml


This workflow:

1. Installs Python 3.11  
2. Loads the Stage 10 manifest  
3. Runs the reference shim  
4. Validates output with Stage 7 master validator  
5. Fails if any part of the engine contract is broken  

This ensures external engines plug cleanly into the HashHelix architecture.

---

## 9. Completion Criteria

Stage 10 is complete when:

- [ ] Design doc (this file) is added  
- [ ] Schema is added  
- [ ] Reference shim is added  
- [ ] Sample binding artifact is added  
- [ ] CI workflow passes  
- [ ] PR is merged cleanly  

Once complete, Stage 11 may begin.


