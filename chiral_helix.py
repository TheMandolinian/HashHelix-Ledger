# chiral_helix.py
import json, hashlib, time
from pathlib import Path
from math import sin, pi
from typing import Optional, List, Dict, Any

# ---- Quantizer (same as single-helix) ----
def q_round(x: float) -> int:
    return int(round(x))

# ---- Spiral with explicit sign (+1 right-handed, -1 left-handed) ----
def spiral(a_prev: int, n: int, sign: int) -> int:
    return q_round(n * sin(a_prev + sign * (pi / n))) + 1

# ---- One-strand step hash ----
def strand_hash(a_n: int, d_n: str, h_prev: bytes) -> bytes:
    # H_n = SHA256( a_n || D_n || H_{n-1} )
    return hashlib.sha256(f"{a_n}|{d_n}".encode() + h_prev).digest()

# ---- Commutative chiral commitment over the two strand heads ----
def chiral_commit(h_plus: bytes, h_minus: bytes) -> str:
    left, right = sorted([h_plus, h_minus])
    return hashlib.sha256(left + right).hexdigest()

class ChiralLedger:
    """
    Dual-helix append-only ledger persisted as JSONL.
    Maintains right-handed (+) and left-handed (-) strands in lockstep.
    """
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.entries: List[Dict[str, Any]] = []
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as f:
                for line in f:
                    self.entries.append(json.loads(line))

        # Genesis state
        if self.entries:
            last = self.entries[-1]
            self.n = last["n"]
            self.a_plus  = last["a_plus"]
            self.a_minus = last["a_minus"]
            self.h_plus  = bytes.fromhex(last["h_plus"])
            self.h_minus = bytes.fromhex(last["h_minus"])
        else:
            self.n = 1
            self.a_plus  = 1
            self.a_minus = 1
            self.h_plus  = b"\x00" * 32
            self.h_minus = b"\x00" * 32

    def append(self, data: str) -> Dict[str, Any]:
        # advance index
        self.n += 1

        # compute next spiral states
        a_plus  = spiral(self.a_plus,  self.n, +1)
        a_minus = spiral(self.a_minus, self.n, -1)

        # hash each strand
        h_plus  = strand_hash(a_plus,  data, self.h_plus)
        h_minus = strand_hash(a_minus, data, self.h_minus)

        entry = {
            "n": self.n,
            "ts": time.time(),
            "data": data,
            "a_plus":  a_plus,
            "a_minus": a_minus,
            "h_plus_prev":  self.h_plus.hex(),
            "h_minus_prev": self.h_minus.hex(),
            "h_plus":  h_plus.hex(),
            "h_minus": h_minus.hex(),
            "commit": chiral_commit(h_plus, h_minus),
        }

        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, separators=(",", ":")) + "\n")

        # advance in-memory state
        self.entries.append(entry)
        self.a_plus, self.a_minus = a_plus, a_minus
        self.h_plus, self.h_minus = h_plus, h_minus
        return entry

    def head(self) -> Optional[Dict[str, Any]]:
        return self.entries[-1] if self.entries else None

    def verify(self) -> bool:
        """
        Recompute both strands from genesis and check:
          - a_± match the stored values
          - h_± link correctly
          - commitment matches chiral_commit(h_plus, h_minus)
        """
        n = 1
        a_plus, a_minus = 1, 1
        h_plus, h_minus = b"\x00"*32, b"\x00"*32

        for e in self.entries:
            n += 1
            a_plus  = spiral(a_plus,  n, +1)
            a_minus = spiral(a_minus, n, -1)
            if a_plus != e["a_plus"] or a_minus != e["a_minus"]:
                return False
            if h_plus.hex() != e["h_plus_prev"] or h_minus.hex() != e["h_minus_prev"]:
                return False
            h_plus  = strand_hash(a_plus,  e["data"], h_plus)
            h_minus = strand_hash(a_minus, e["data"], h_minus)
            if h_plus.hex() != e["h_plus"] or h_minus.hex() != e["h_minus"]:
                return False
            if chiral_commit(h_plus, h_minus) != e["commit"]:
                return False
        return True
