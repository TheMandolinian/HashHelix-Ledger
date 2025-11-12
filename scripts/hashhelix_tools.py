#!/usr/bin/env python3
import hashlib, json, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SHARDS = ROOT / "shards"
GENESIS_MANIFEST = SHARDS / "genesis" / "artifacts" / "manifest.sha256"
RESEARCH_DIR = SHARDS / "research"

def git_head():
    try:
        return subprocess.check_output(["git","rev-parse","HEAD"], cwd=ROOT).decode().strip()
    except Exception:
        return None

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def read_kv(path: Path):
    d = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                d[k.strip()] = v.strip()
    return d

def build_summary():
    summary = {
        "project": "HashHelix Ledger",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo_head": git_head(),
        "genesis": None,
        "research": []
    }

    # Genesis
    if GENESIS_MANIFEST.exists():
        summary["genesis"] = {
            "manifest_path": str(GENESIS_MANIFEST.relative_to(ROOT)),
            "manifest_sha256": file_sha256(GENESIS_MANIFEST)
        }

    # Research shards
    if RESEARCH_DIR.exists():
        for shard in sorted(RESEARCH_DIR.glob("*")):
            art = shard / "artifacts"
            if not art.exists():
                continue
            manifest = art / "manifest.sha256"
            chiral = art / "chiral_link.sha256"
            files = [p.name for p in art.glob("*.pdf")]
            entry = {
                "slug": shard.name,
                "artifacts_path": str(art.relative_to(ROOT)),
                "files": files,
                "manifest": {
                    "path": str(manifest.relative_to(ROOT)) if manifest.exists() else None,
                    "sha256": file_sha256(manifest) if manifest.exists() else None,
                    "size": manifest.stat().st_size if manifest.exists() else None
                },
                "chiral_link": None
            }
            if chiral.exists():
                kv = read_kv(chiral)
                entry["chiral_link"] = {
                    "path": str(chiral.relative_to(ROOT)),
                    "left": kv.get("left"),
                    "right": kv.get("right"),
                    "commitment": kv.get("commitment")
                }
            summary["research"].append(entry)

    out = ROOT / "ledger_summary.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"✅ Wrote {out}")
    return 0

def verify_all():
    ok = True
    if not GENESIS_MANIFEST.exists():
        print("❌ Missing genesis manifest:", GENESIS_MANIFEST)
        return 1

    for shard in sorted(RESEARCH_DIR.glob("*")) if RESEARCH_DIR.exists() else []:
        art = shard / "artifacts"
        chiral = art / "chiral_link.sha256"
        manifest_r = art / "manifest.sha256"
        if not (chiral.exists() and manifest_r.exists()):
            continue
        kv = read_kv(chiral)
        g = GENESIS_MANIFEST.read_bytes()
        r = manifest_r.read_bytes()
        left = hashlib.sha256(g + r).hexdigest()
        right = hashlib.sha256(r + g).hexdigest()
        commit = hashlib.sha256(min(left, right).encode() + max(left, right).encode()).hexdigest()
        shard_ok = (kv.get("left")==left and kv.get("right")==right and kv.get("commitment")==commit)
        status = "✅" if shard_ok else "❌"
        print(f"{status} {shard.name} chiral commitment")
        ok = ok and shard_ok

    print("Overall:", "✅ Verified" if ok else "❌ Mismatch")
    return 0 if ok else 1

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "build-summary":
        sys.exit(build_summary())
    if cmd == "verify":
        sys.exit(verify_all())
    print("Usage:")
    print("  python3 scripts/hashhelix_tools.py build-summary")
    print("  python3 scripts/hashhelix_tools.py verify")
    sys.exit(1)

if __name__ == "__main__":
    main()
