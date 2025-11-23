Dropdown HASHHELIX LEDGER LAWS — FULL CANONICAL VERSION (v1.9.41) 
The Mandolinian Edition — 2025 Revision 
Includes the Numerical Evaluation Rule (NER), Transient Locking Findings, and updated 
terminology. 11/22/2025 9:45pm ct 


LAW 1 — The Root Artifact is the Source of All Deterministic Computation 
Every HashHelix computation originates from a single immutable Root Artifact, which defines: 
• the recurrence seed, 
• the canonical π definition, 
• the engine’s deterministic constraints. 
No Temporal Relic, Vault, or Lane may override the Root Artifact. 


LAW 2 — Temporal Relics Are the Only Valid Containers of Computation 
All engine outputs must be serialized into Temporal Relics, which hold: 
• the recurrence outputs, 
• lane metadata, 
• chiral commitments, 
• sealing proofs. 
A Relic is the unit of truth in HashHelix. 


LAW 3 — Deterministic Recurrence Governs All Lanes 
The HashHelix engine is defined exclusively by the WDTP recurrence: 

a₁ = 1aₙ = ⌊ n · sin( a_{n-1} + π/n  mod  2π ) ⌋ + 1    (for n ≥ 2)


No fork, variant, or optimization may alter this recurrence without becoming a non-HashHelix 
derivative system. 


LAW 4 — The Numerical Evaluation Rule (NER) (New 2025) 
WDTP must be evaluated with: 
NER Requirement 

p𝐡𝐚𝐬𝐞 = (𝒂𝒏−𝟏 +𝝅/𝒏)𝐦𝐨𝐝 𝟐𝝅 

This is mandatory for all implementations (FP, HP, Rust, C, or hardware). 
Without NER, WDTP drifts due to floating-point decay. 
With NER, WDTP is mathematically deterministic forever. 
This is now binding law. 


LAW 5 — Chiral Lane Structure Is Immutable 
Every lane operates as a left/right chiral pair. 
A valid Helix must contain: 
• Lane L0 (left) 
• Lane R0 (right) 
• Defined chiral commitments between them 
A lane without a chiral twin is invalid and cannot host Relics. 


LAW 6 — Epoch Bundles Provide Verifiability 
Temporal Relics must be grouped into sequential Epoch Bundles, each containing: 
• ordered residue traces, 
• deterministic phase summaries, 
• sealed metadata blocks. 
Epochs allow parallel validation without scanning entire Relics. 


LAW 7 — Deterministic Compression Is Required 
All Relic data must be compressible via a deterministic, lossless compressor. 
If two nodes compress the same Relic and get different bytes, the Relic is invalid. 


LAW 8 — Vault Classes Define Access and Cost 
HashHelix distinguishes between: 
• HOT Vaults — high-frequency, short-term computation 
• WARM Vaults — mid-term analytical storage 
• COLD Vaults — deep archive and institutional anchoring 
Each vault obeys strict retention and access rules. 


LAW 9 — Public Engine, Private Economy 
The WDTP recurrence is permissively licensed and public. 
Temporal Relics, Vault policies, and commercial use of the engine economy are not public. 
Tokenomics = stopped disclosures. 
The economy is private-layer only. 


LAW 10 — Institutional Anchor Envelopes Must Seal Deterministically 
Institutions anchoring data into HashHelix must: 
• use Relics, 
• follow vault-tier rules, 
• adhere to deterministic sealing, 
• retain chiral proof integrity. 
A broken seal invalidates the anchored data. 


LAW 11 — The Engine and Economy Must Remain Strictly Separate 
No ledger rule may allow commercial actions to influence the recurrence. 
No fee, token, or financial layer may modify lane computation. 
The engine is sacred. 


LAW 12 — HashHelix Is the Internet of Verification 
HashHelix is not: 
• a blockchain, 
• a DAG, 
• a validator-based consensus system. 
It is a deterministic temporal computation engine whose purpose is to provide: 
• verifiable time, 
• verifiable sequence, 
• verifiable mathematical truth. 
This law defines the philosophical foundation of the system. 


END OF FULL CANONICAL LAWS (v1.9.4) 
HASHHELIX LEDGER LAWS — COMPACT HEADER VERSION 
(For README.md, project headers, and file footers.) 


LAW 1 — Root Artifact governs all truth. 
LAW 2 — Temporal Relics are the only containers of valid computation. 
LAW 3 — WDTP is the immutable recurrence. 
LAW 4 — NER Required: phase must be reduced mod 2π every step. 
LAW 5 — Lanes are chiral, paired, and immutable. 
LAW 6 — Epoch Bundles provide deterministic validation. 
LAW 7 — Compression must be deterministic. 
LAW 8 — Vault classes define computation vs storage. 
LAW 9 — Engine public, economy private. 
LAW 10 — Anchor envelopes must seal deterministically. 
LAW 11 — Engine and economy must remain separate. 
LAW 12 — HashHelix = The Internet of Verification.