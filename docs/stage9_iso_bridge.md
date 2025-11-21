# Stage 9 — ISO 20022 Bridge

HashHelix does not replace ISO 20022. 
It provides a deterministic mapping for institutions that already use ISO.

Mapping rules:

- `MsgId` ← envelope_id
- `CreDtTm` ← engine_timestamp
- `RgltryRptg` ← institution category (optional)
- `SplmtryData` ← hh_engine_commitment

This mapping is optional, non-binding, and used for interoperability only.
