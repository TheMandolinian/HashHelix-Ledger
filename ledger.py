import json, hashlib, time
from pathlib import Path
from math import sin, pi
from typing import Optional, List, Dict, Any

def q_round(x: float) -> int:
    return int(round(x))

def spiral(a_prev: int, n: int, sign: int = +1, quantizer=q_round) -> int:
    return quantizer(n * sin(a_prev + sign * (pi / n))) + 1

def helix_hash(a_n: int, d_n: str, h_prev: bytes) -> bytes:
    return hashlib.sha256(f"{a_n}|{d_n}".encode() + h_prev).digest()

class Ledger:
    """Single-helix append-only ledger persisted as JSONL."""
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.entries: List[Dict[str, Any]] = []
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as f:
                for line in f:
                    self.entries.append(json.loads(line))
        # genesis state
        self.a = self.entries[-1]["a"] if self.entries else 1
        self.n = self.entries[-1]["n"] if self.entries else 1
        self.h = bytes.fromhex(self.entries[-1]["h"]) if self.entries else b"\x00"*32

    def append(self, data: str) -> Dict[str, Any]:
        self.n += 1
        a_n = spiral(self.a, self.n, sign=+1, quantizer=q_round)
        h_n = helix_hash(a_n, data, self.h)
        entry = {
            "n": self.n,
            "ts": time.time(),
            "a": a_n,
            "data": data,
            "h_prev": self.h.hex(),
            "h": h_n.hex(),
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, separators=(",", ":")) + "\n")
        self.entries.append(entry)
        self.a, self.h = a_n, h_n
        return entry

    def head(self) -> Optional[Dict[str, Any]]:
        return self.entries[-1] if self.entries else None

    def verify(self) -> bool:
        """Recompute the chain from genesis and confirm every hash links."""
        a, h = 1, b"\x00"*32
        n = 1
        for e in self.entries:
            n += 1
            a = spiral(a, n, sign=+1, quantizer=q_round)
            if a != e["a"]:
                return False
            if h.hex() != e["h_prev"]:
                return False
            h = helix_hash(a, e["data"], h)
            if h.hex() != e["h"]:
                return False
        return True
