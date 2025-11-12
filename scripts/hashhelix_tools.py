#!/usr/bin/env python3
import argparse, json, math, time, os, hashlib
from pathlib import Path

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def spiral_next(a_prev: int, n: int, sign: int) -> int:
    # sign=+1 => +pi/n ; sign=-1 => -pi/n
    return math.floor(n * math.sin(a_prev + sign * math.pi / n)) + 1

def chiral_step(prev_plus, prev_minus, n, data_bytes, h_prev_plus_hex, h_prev_minus_hex):
    a_plus = spiral_next(prev_plus, n, +1)
    a_minus = spiral_next(prev_minus, n, -1)
    # Hn± = SHA256( spiral(a_{n-1},n) || Dn || H_{n-1} )
    h_plus = sha256_hex(
        (str(a_plus).encode() + data_bytes + bytes.fromhex(h_prev_plus_hex))
        if h_prev_plus_hex else (str(a_plus).encode() + data_bytes)
    )
    h_minus = sha256_hex(
        (str(a_minus).encode() + data_bytes + bytes.fromhex(h_prev_minus_hex))
        if h_prev_minus_hex else (str(a_minus).encode() + data_bytes)
    )
    return a_plus, a_minus, h_plus, h_minus

def lane_path(lanes_json, lane):
    return lanes_json["lanes"][lane]["path"]

def load_head(path: Path):
    if not path.exists() or path.stat().st_size == 0:
        return 0, 1, 1, "", "", None
    with path.open("rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        # read last line
        off = max(0, size - 8192)
        f.seek(off)
        tail = f.read().splitlines()
        last = json.loads(tail[-1].decode())
    return last["n"], last["a_plus"], last["a_minus"], last["h_plus"], last["h_minus"], last

def append_record(path: Path, rec: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("ab") as f:
        line = (json.dumps(rec, separators=(",", ":")) + "\n").encode()
        f.write(line)

def cmd_append(args):
    lanes = json.load(open("lanes.json"))
    lane = args.lane
    p = Path(lane_path(lanes, lane))
    n_prev, a_prev_plus, a_prev_minus, h_prev_plus, h_prev_minus, _ = load_head(p)
    n = n_prev + 1
    data_bytes = args.data.encode()
    a_plus, a_minus, h_plus, h_minus = chiral_step(a_prev_plus, a_prev_minus, n, data_bytes, h_prev_plus, h_prev_minus)
    rec = {
        "n": n,
        "ts": int(time.time()),
        "data": args.data,
        "a_plus": a_plus,
        "a_minus": a_minus,
        "h_plus": h_plus,
        "h_minus": h_minus,
        "prev_h_plus": h_prev_plus,
        "prev_h_minus": h_prev_minus
    }
    append_record(p, rec)
    print(json.dumps({"lane": lane, "n": n, "h_plus": h_plus, "h_minus": h_minus}, indent=2))

def cmd_head(args):
    lanes = json.load(open("lanes.json"))
    p = Path(lane_path(lanes, args.lane))
    n, ap, am, hp, hm, rec = load_head(p)
    if rec is None:
        print(json.dumps({"lane": args.lane, "empty": True}, indent=2))
    else:
        print(json.dumps({"lane": args.lane, "n": n, "h_plus": hp, "h_minus": hm}, indent=2))

def cmd_init(args):
    # seed lane with one record if empty
    lanes = json.load(open("lanes.json"))
    p = Path(lane_path(lanes, args.lane))
    _, _, _, _, _, rec = load_head(p)
    if rec is None:
        # first record uses a1=1 for both strands; n=1
        a1 = 1
        data = "genesis"
        h_plus = sha256_hex(str(a1).encode() + data.encode())
        h_minus = sha256_hex(str(a1).encode() + data.encode())
        rec = {
            "n": 1,
            "ts": int(time.time()),
            "data": data,
            "a_plus": a1,
            "a_minus": a1,
            "h_plus": h_plus,
            "h_minus": h_minus,
            "prev_h_plus": "",
            "prev_h_minus": ""
        }
        append_record(p, rec)
        print(json.dumps({"lane": args.lane, "initialized": True, "h_plus": h_plus, "h_minus": h_minus}, indent=2))
    else:
        print(json.dumps({"lane": args.lane, "initialized": False, "message": "already has records"}, indent=2))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s0 = sub.add_parser("init")
    s0.add_argument("--lane", default="default-chiral")
    s0.set_defaults(func=cmd_init)
    s1 = sub.add_parser("append")
    s1.add_argument("--lane", default="default-chiral")
    s1.add_argument("--data", default="{}")
    s1.set_defaults(func=cmd_append)
    s2 = sub.add_parser("head")
    s2.add_argument("--lane", default="default-chiral")
    s2.set_defaults(func=cmd_head)
    args = ap.parse_args()
    args.func(args)
