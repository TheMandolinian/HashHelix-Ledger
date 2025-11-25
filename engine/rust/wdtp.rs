//! HashHelix Stage 11 — WDTP Rust Skeleton (NER-Compliant)
//! Engine-only. No business / relic logic.
//! LAW 4 (NER) binding:
//!   phase = (a_{n-1} + PI/n) mod 2PI

use std::f64::consts::PI;

pub const TAU: f64 = std::f64::consts::TAU; // 2π

/// Numerical Evaluation Rule (LAW 4):
/// Reduce phase mod 2π before sin() to prevent drift.
pub fn ner_phase(prev_a: i64, n: u64) -> f64 {
    if n < 2 {
        panic!("n must be >= 2");
    }
    let phase_raw = (prev_a as f64) + (PI / (n as f64));
    // Deterministic reduction mod 2π
    phase_raw.rem_euclid(TAU)
}

/// Single WDTP step.
/// a_n = floor(n * sin(phase)) + 1
pub fn wdtp_step(prev_a: i64, n: u64) -> i64 {
    if n < 2 {
        panic!("n must be >= 2");
    }
    let phase = ner_phase(prev_a, n);
    ((n as f64) * phase.sin()).floor() as i64 + 1
}

/// Generate WDTP sequence [a1, a2, ..., a_nmax].
pub fn wdtp_sequence(n_max: u64, a1: i64) -> Vec<i64> {
    if n_max < 1 {
        panic!("n_max must be >= 1");
    }
    let mut seq: Vec<i64> = Vec::with_capacity(n_max as usize);
    seq.push(a1);
    let mut prev = a1;
    for n in 2..=n_max {
        prev = wdtp_step(prev, n);
        seq.push(prev);
    }
    seq
}

/// Iterator over WDTP values (infinite).
pub struct WdtpIter {
    n: u64,
    prev: i64,
}

impl WdtpIter {
    pub fn new(a1: i64) -> Self {
        Self { n: 2, prev: a1 }
    }
}

impl Iterator for WdtpIter {
    type Item = i64;

    fn next(&mut self) -> Option<Self::Item> {
        if self.n == 2 {
            // first yield is a1
            self.n += 1;
            return Some(self.prev);
        }
        self.prev = wdtp_step(self.prev, self.n);
        self.n += 1;
        Some(self.prev)
    }
}

/*
Optional equivalence helper (add sha2 crate later):

pub fn wdtp_prefix_hash(n_max: u64, a1: i64) -> String {
    use sha2::{Digest, Sha256};
    let seq = wdtp_sequence(n_max, a1);
    let blob = seq.iter()
        .map(|v| v.to_string())
        .collect::<Vec<_>>()
        .join(",");
    let mut hasher = Sha256::new();
    hasher.update(blob.as_bytes());
    format!("{:x}", hasher.finalize())
}
*/

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn small_n_vector_matches_python() {
        let seq20 = wdtp_sequence(20, 1);
        let expected: Vec<i64> = vec![
            1, 2, 1, 4, -4, 2, 5, -6, 6, 1,
            11, -11, 13, 9, 4, -13, -4, 12, -7, -10
        ];
        assert_eq!(seq20, expected);
    }
}
