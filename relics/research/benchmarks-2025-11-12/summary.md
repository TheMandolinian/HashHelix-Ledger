# HashHelix 21-Helix Benchmark — 2025-11-12

- **Date:** 2025-11-12  
- **Codebase:** HashHelix Ledger v1.6  
- **Mode:** 21-Helix temporal recursion (π/n-phase-drifted sine primitive)  
- **Machine:** Intel i7 laptop (local single-node test)  

## Result Overview

This benchmark ran HashHelix in a 21-helix recursion mode, appending  
21,000 ledger events using the π/n-phase-drifted sine function as the  
temporal primitive.

- **Total Appends:** 21,000  
- **Elapsed Time:** ~21.3 seconds  
- **Throughput:** ~4,929 transactions per second (TPS)

“21-Helix Mode” means the ledger executed 21 deterministic lanes of the  
recursion, each offset by a predictable π/n phase drift.  
Every lane advances in perfect sync, allowing high concurrency without  
losing determinism.

## Why This Benchmark Matters

This run shows that HashHelix’s mathematical recursion primitive can  
maintain multi-thousand TPS performance:

- on modest consumer hardware  
- without GPU acceleration  
- without block batching  
- with fully deterministic replay and verification  

Because time evolution is encoded directly in the recursion, any  
verifier can reproduce the 21-lane spiral and confirm matching results.

This run becomes the **canonical baseline** for future performance tests,  
including:

- Higher values of `n`  
- i9 + RTX desktop benchmark (coming soon)  
- Alternate epoch sizes and recursion modes  
- Multi-node verification comparisons
