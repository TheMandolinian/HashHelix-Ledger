# Stage 9 — Institutional Anchor Envelope (IAE)

Stage 9 defines the standardized external interface for how institutions
consume, verify, and archive outputs from the HashHelix Engine (Stages 1–8).

The Anchor Envelope (IAE) is a self-contained validation package that includes:

- Lane root
- Epoch bundle hash
- Relic commitment
- Merkle root
- Chiral twin signature
- Complete sequence hash
- ISO 20022 alignment fields
- Institutional signatures
- HH engine signature
- Vault tier declaration

A Stage 9 envelope must be deterministic, reconstructible, and fully verifiable
independent of any private internal system.
