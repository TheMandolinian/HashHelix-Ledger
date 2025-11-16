# hash_entropy_lanes.py
# Build SHA-256 commitments for the 3 entropy lanes

import hashlib
import json
from pathlib import Path

FILES = [
    "hh_entropy_lane01.txt",
    "hh_entropy_lane02.txt",
    "hh_entropy_lane03.txt",
]

OUT = "data/entropy_commitment.json"


def sha256_file(path: str) -> str:
    """Stream a file and return its SHA-256 hex digest."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    records = []

    # Hash each lane file
    for idx, path in enumerate(FILES, start=1):
        p = Path(path)
        if not p.exists():
            print(f"[ERROR] Missing lane file: {path}")
            return

        digest = sha256_file(path)
        records.append({
            "lane": idx,
            "file": path,
            "sha256": digest,
        })

    # Combined commitment: SHA256 of concatenated lane hashes
    concatenated = "".join(r["sha256"] for r in records).encode("ascii")
    combined = hashlib.sha256(concatenated).hexdigest()

    result = {
        "lanes": records,
        "combined_sha256": combined,
    }

    # Ensure data/ exists
    Path("data").mkdir(exist_ok=True)

    with open(OUT, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[OK] Entropy lane commitments written → {OUT}")
    print(f"Combined commitment: {combined}")
    for r in records:
        print(f"  lane_{r['lane']}: {r['sha256']}")


if __name__ == "__main__":
    main()
