#!/usr/bin/env python3
import hashlib, shutil, subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
SHARDS = ROOT / "shards"
RESEARCH = SHARDS / "research"
GENESIS = SHARDS / "genesis" / "artifacts" / "manifest.sha256"

def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def new_slug():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    v = input("Enter new version tag (e.g. v1.6): ").strip()
    name = input("Enter shard title (e.g. symmetry): ").strip().replace(" ","-")
    return f"{today}-{name}-{v}"

def main():
    slug = new_slug()
    shard_dir = RESEARCH / slug / "artifacts"
    shard_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Created shard folder: {shard_dir}")

    pdf_path = input("Path to new PDF (relative or absolute): ").strip()
    pdf = Path(pdf_path).resolve()
    if not pdf.exists():
        print("❌ PDF not found."); return
    shutil.copy(pdf, shard_dir / pdf.name)
    print(f"📄 Copied {pdf.name}")

    # Manifest
    m = shard_dir / "manifest.sha256"
    m.write_text(f"sha256={sha256_file(shard_dir / pdf.name)}\n")
    print("🧮 Generated manifest.")

    # Chiral link
    left = hashlib.sha256(GENESIS.read_bytes() + m.read_bytes()).hexdigest()
    right = hashlib.sha256(m.read_bytes() + GENESIS.read_bytes()).hexdigest()
    commit = hashlib.sha256(min(left,right).encode() + max(left,right).encode()).hexdigest()
    c = shard_dir / "chiral_link.sha256"
    c.write_text(f"left={left}\nright={right}\ncommitment={commit}\n")
    print("🔗 Created chiral link.")

    subprocess.run(["git","add",str(shard_dir)])
    subprocess.run(["git","commit","-m",f"Add research shard {slug}"])
    subprocess.run(["git","push","origin","main"])
    subprocess.run(["python3","scripts/hashhelix_tools.py","build-summary"])
    subprocess.run(["git","add","ledger_summary.json"])
    subprocess.run(["git","commit","-m",f"Update ledger summary for {slug}"])
    subprocess.run(["git","push","origin","main"])
    print("\n✅ Shard added and ledger updated successfully.\n")

if __name__ == "__main__":
    main()
