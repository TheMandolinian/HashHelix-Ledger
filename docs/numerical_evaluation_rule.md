### Numerical Evaluation Rule (NER) — LAW 4 (Binding, 2025)

HashHelix’s temporal primitive (WDTP) is mathematically periodic in its sine argument.  
However, at extremely large recurrence indices, floating-point phase accumulation causes cross-platform drift unless the phase is normalized before evaluation.

To preserve bit-for-bit determinism forever, HashHelix adopts the Numerical Evaluation Rule (NER) as a binding law.

**WDTP (unchanged):**  
- Seed: a₁ = 1  
- Recurrence (n ≥ 2):  
  aₙ = ⌊ n · sin(aₙ₋₁ + π/n) ⌋ + 1

**NER requirement:**  
Before any sin() call, the phase must be reduced modulo 2π:

phase = (aₙ₋₁ + π/n) mod 2π  
aₙ = ⌊ n · sin(phase) ⌋ + 1

This rule does not alter WDTP mathematics.  
It standardizes evaluation to eliminate meaningless full-rotation accumulation that exceeds floating-point precision.

**Implications:**
- WDTP remains deterministic at arbitrarily large N  
- Outputs are identical across CPU architectures, compilers, FPUs, and math libraries  
- Cross-language implementations (Python, Rust, C, WASM, hardware) remain replay-equivalent forever  

NER is mandatory for all public-engine computations starting with Whitepaper v1.9.4.
