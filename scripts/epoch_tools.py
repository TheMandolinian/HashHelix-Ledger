#!/usr/bin/env python3
import argparse, json, os, hashlib, glob, sys
from pathlib import Path

# Ensure repo root is importable no matter where we run from
sys.path.append(str(Path(__file__).resolve().parents[1]))

from merkle import merkle_root
# sha256_hex not strictly needed here; kept if you extend later
def chiral_commitment(h_plus_hex: str, h_minus_hex: str) -> str:
    a, b = sorted([bytes.fromhex(h_plus_hex), bytes.fromhex(h_minus_hex)])
    return hashlib.sha256(a + b).hexdigest()

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
    for lane, last in lane_heads.items():
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
    ok = True
    for ep_file in glob.glob(args.pattern):
        ep = json.load(open(ep_file))
        lanes = json.load(open("lanes.json"))
        leaves = []
        for lane in ep["lanes"]:
            last = read_head_for_lane(lanes, lane)
            if last["n"] != ep["lanes"][lane]["n"]:
                print(f"[FAIL] {ep_file}: lane {lane} n mismatch (have {last['n']} expected {ep['lanes'][lane]['n']})")
                ok = False
            leaves += [bytes.fromhex(last["h_plus"]), bytes.fromhex(last["h_minus"])]
            c_now = chiral_commitment(last["h_plus"], last["h_minus"])
            if c_now != ep["chiral_commitments"][lane]:
                print(f"[FAIL] {ep_file}: lane {lane} chiral commitment mismatch")
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
