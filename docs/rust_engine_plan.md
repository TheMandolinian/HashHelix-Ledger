
**Must match Python float → floor behavior exactly.**

---

### 2.2 `lane_runtime`
Responsibilities:

- Single-lane generator  
- Multi-lane generator  
- Sequential mode (independent n-counters)  
- Parallel mode (shared n-counter across lanes)  
- Optional interleaved output  

Key detail: no randomness or time-based seeding.

---

### 2.3 `hashing`
Implements all cryptographic logic:

- `sha256_hex`  
- `merkle_root_ints`  
- `merkle_root_hex`  
- `sequence_hash`  
- Chiral commitment logic  

Hash outputs **must match Python byte-for-byte**.

---

### 2.4 `epochs`
Implements WARM vault production:

- Segment lane traces  
- Compute per-epoch Merkle + seq hash  
- Emit JSON (serde_json) using the Stage 7 schema structure  

---

### 2.5 `relics`
Implements COLD vault production:

- Aggregate epoch bundles  
- Compute relic Merkle  
- Compute chiral commitments  
- Produce deterministic JSON  

---

### 2.6 `harness`
Implements Stress Harness v2 in Rust:

- Multi-lane generation  
- Epoch + relic construction  
- Verification  
- Reference-mode: compare Rust output to Python output  

This ensures Rust is **mathematically identical**.

---

## 3. JSON Serialization Rules

Rust engine outputs must:

- Use sorted keys  
- Use standard UTF-8  
- Match Python integer → floating rules  
- Store Merkle as lowercase hex  
- Store IDs with identical naming conventions  

Serde settings:

```rust
serde_json::to_writer_pretty(...)
