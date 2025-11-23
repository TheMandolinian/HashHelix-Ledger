# HashHelix Engine & Ledger Laws — v1.9.4 (Public Engine Layer)
Created by James Bradley Waresback — “The Mandolinian” 
Status: **Binding and Immutable** for all public-engine implementations.

These laws define the non-negotiable behavior of the HashHelix deterministic temporal engine.
They apply to **all** languages, runtimes, and institutional deployments.

---

## LAW 1 — WDTP Is the Sole Temporal Primitive
HashHelix state evolution is governed only by the Waresback Deterministic Temporal Primitive (WDTP):

- Seed: `a₁ = 1`
- Recurrence (n ≥ 2):

\[
a_n = \left\lfloor n \cdot \sin(a_{n-1} + \pi/n) \right\rfloor + 1
\]

No alternative primitives, shortcuts, or probabilistic variants are permitted in the public engine.

---

## LAW 2 — Deterministic Recurrence Equals Time
“Time” in HashHelix is not a clock. 
It is the **deterministic recurrence index** `n`, advanced strictly by WDTP evaluation.

All epoching, lane growth, ordering, and verification rely on recurrence time.

---

## LAW 3 — Temporal Relics Are the Containers of Truth
Temporal Relics are the unified computation containers of HashHelix.

A Relic may contain:
- lane roots
- epoch bundles
- chiral twin heads
- Merkle checkpoints
- metadata necessary for deterministic replay

Relics must be reproducible forever from public engine rules.

---

## LAW 4 — Numerical Evaluation Rule (NER) (New 2025)
Before any `sin()` call, WDTP **must** reduce phase mod `2π`:

\[
\text{phase} = (a_{n-1} + \pi/n) \bmod 2\pi
\]

\[
a_n = \left\lfloor n \cdot \sin(\text{phase}) \right\rfloor + 1
\]

NER is mandatory for all implementations (FP, HP, Rust, C, WASM, or hardware).

Without NER, WDTP drifts due to floating-point decay. 
With NER, WDTP remains mathematically deterministic forever.

---

## LAW 5 — Lanes / Epochs / Merkle Are Structural Time Layers
HashHelix structures recurrence time into:

- **Lanes**: independent deterministic strands
- **Epochs**: fixed-window bundles of recurrence time
- **Merkle checkpoints**: deterministic integrity boundaries

These layers are structural only; they do not alter WDTP mathematics.

---

## LAW 6 — Chiral Twins Must Remain Commit-Commutative
If chiral twin lanes are used, the + and − strands must be evaluated with identical NER rules and combined via a commutative chiral commitment.

Order of +/− strand hashing must not affect final commitment.

---

## LAW 7 — Deterministic Ledger Objects Only
Every public-engine artifact must be derivable from:
- previous deterministic state
- WDTP evolution
- declared inputs

No randomness, system time, external entropy, or nondeterministic ordering is permitted in public engine objects.

---

## LAW 8 — Deterministic Compression Is Allowed, Loss Is Not
Compression may be applied **only** if it preserves full deterministic replay.

Compression must be:
- stable across machines
- verifiable from the public engine
- incapable of changing WDTP outputs

Lossy compression is forbidden.

---

## LAW 9 — Vault Classes Define Storage Tiers, Not Truth
Vaults are storage tiers for Relics:

- **HOT** — active/reference execution tier
- **WARM** — institutional storage tier
- **COLD** — archival / NFT-like tier

Vault placement never changes truth, only availability and policy.

---

## LAW 10 — Public Engine vs. Private Economy Separation
The WDTP engine, its laws, and all public verification rules are **public and immutable**.

Private layers (tokenomics, contracts, licensing, pricing, institutional onboarding) are **not part of the public engine**.

**Tokenomics = stopped disclosures** in public docs.

---

## LAW 11 — HashHelix Is the Internet of Verification
HashHelix is not a blockchain, DAG, or probabilistic consensus network.

It is a deterministic temporal computation engine whose outputs serve as permanent verification objects.

Any marketing, implementation, or integration must preserve this definition.

---

# Change Control
These laws are binding as of **v1.9.4**. 
Future versions may add laws, but **no public law may be weakened or contradicted**.
