#!/usr/bin/env python3
import argparse, json, os, hashlib, glob, sys
from pathlib import Path

# Ensure repo root importable
sys.path.append(str(Path(__file__).resolve().parents[1]))
from merkle import merkle_root

def chiral_commitment(h_plus_hex: str, h_minus_hex: str) -> str:
    a, b = sorted([bytes.fromhex(h_plus_hex), bytes.fromhex(h_minus_hex)])
    return hashlib.sha256(a + b).hexdigest()

def _find_record_by_n(lane_path: Path, n_target: int):
    if not lane_path.exists():
        return None
    with lane_path.open("rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("n") == n_target:
                return rec
    return None

def read_head_for_lane(lanes, lane_name):
    path = Path(lanes["lanes"][lane_name]["path"])
    if not path.exists() or path.stat().st_size == 0:
        raise SystemExit(f"lane '{lane_name}' has no records; run: scripts/hashhelix_tools.py init --lane {lane_name}")
    with path.open("rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        off = max(0, size - 8192)
        f.seek(off)
        tail = f.read().splitlines()
        last = json.loads(tail[-1].decode())
    return last

def cmd_seal(args):
    lanes = json.load(open("lanes.json"))
    lane_heads = {lane: read_head_for_lane(lanes, lane) for lane in lanes["lanes"]}
    leaves = []
    for _, last in lane_heads.items():
        leaves += [bytes.fromhex(last["h_plus"]), bytes.fromhex(last["h_minus"])]
    root = merkle_root(leaves).hex()
    chiral = {lane: chiral_commitment(last["h_plus"], last["h_minus"]) for lane, last in lane_heads.items()}
    epoch_idx = len(glob.glob("epochs/epoch-*.json")) + 1
    epoch_path = Path(f"epochs/epoch-{epoch_idx:06d}.json")
    epoch = {
        "epoch": epoch_idx,
        "lanes": {k: {"n": v["n"], "h_plus": v["h_plus"], "h_minus": v["h_minus"]} for k, v in lane_heads.items()},
        "merkle_root": root,
        "chiral_commitments": chiral
    }
    epoch_path.parent.mkdir(parents=True, exist_ok=True)
    epoch_path.write_text(json.dumps(epoch, indent=2))
    print(json.dumps({"sealed": epoch_idx, "merkle_root": root, "chiral": chiral}, indent=2))

def cmd_verify(args):
    """
    Verify epochs as immutable snapshots:
      - For each epoch, read stored (n, h_plus, h_minus) per lane.
      - Find the lane record with that exact n.
      - Compare its h_plus/h_minus to the epoch snapshot.
      - Rebuild the epoch's Merkle root from the epoch snapshot values.
    """
    ok = True
    lanes_cfg = json.load(open("lanes.json"))
    for ep_file in glob.glob(args.pattern):
        ep = json.load(open(ep_file))
        leaves = []
        for lane_name, snap in ep["lanes"].items():
            n_expected = snap["n"]; hp_expected = snap["h_plus"]; hm_expected = snap["h_minus"]
            lane_path = Path(lanes_cfg["lanes"][lane_name]["path"])
            rec = _find_record_by_n(lane_path, n_expected)
            if rec is None:
                print(f"[FAIL] {ep_file}: lane {lane_name} has no record with n={n_expected}")
                ok = False
                continue
            if rec.get("h_plus") != hp_expected or rec.get("h_minus") != hm_expected:
                print(f"[FAIL] {ep_file}: lane {lane_name} strand hash mismatch at n={n_expected}")
                ok = False
            leaves += [bytes.fromhex(hp_expected), bytes.fromhex(hm_expected)]
            c_now = chiral_commitment(hp_expected, hm_expected)
            if c_now != ep["chiral_commitments"][lane_name]:
                print(f"[FAIL] {ep_file}: lane {lane_name} chiral commitment mismatch")
                ok = False
        root_now = merkle_root(leaves).hex()
        if root_now != ep["merkle_root"]:
            print(f"[FAIL] {ep_file}: merkle root mismatch")
            ok = False
        else:
            print(f"[OK] {ep_file}")
    if not ok:
        raise SystemExit(1)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("seal");   s1.set_defaults(func=cmd_seal)
    s2 = sub.add_parser("verify"); s2.add_argument("pattern"); s2.set_defaults(func=cmd_verify)
    args = ap.parse_args()
    args.func(args)
