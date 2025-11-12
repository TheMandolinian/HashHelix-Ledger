from __future__ import annotations
import hashlib
from typing import List

def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def merkle_root(leaves: List[bytes]) -> bytes:
    if not leaves:
        return sha256(b"")
    layer = [sha256(x) for x in leaves]
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]
            b = layer[i+1] if i+1 < len(layer) else a
            nxt.append(sha256(a + b))
        layer = nxt
    return layer[0]
