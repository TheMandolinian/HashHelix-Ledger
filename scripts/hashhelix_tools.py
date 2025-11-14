#!/usr/bin/env python3
import argparse, json, math, time, os, hashlib, struct
from pathlib import Path

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def spiral_next(a_prev: int, n: int, phase: float) -> int:
    return int(n * math.sin(a_prev + phase)) + 1

def lane_path(lane: str) -> Path:
    lanes = json.loads(open("lanes.json").read())["lanes"]
    return Path(lanes[lane]["path"])

def cmd_init(args):
    lanes = json.loads(open("lanes.json").read())["lanes"]
    lane = lanes[args.lane]
    path = Path(lane["path"])
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        print(json.dumps({"lane": args.lane, "initialized": False, "message": "already exists"}))
    else:
        path.write_text(json.dumps({"lane": args.lane, "n": 0, "h": "0"*64}) + "\n")
        print(json.dumps({"lane": args.lane, "initialized": True}))

def cmd_append(args):
    data = args.data.encode()
    data_bytes = data if len(data) <= 256 else hashlib.sha256(data).digest()
    lanes = json.loads(open("lanes.json").read())["lanes"]
    lane_config = lanes[args.lane]
    path = Path(lane_config["path"])
    lines = path.read_text().splitlines()
    last = json.loads(lines[-1]) if lines else {"n": 0, "h": "0"*64}
    n = last["n"] + 1
    h_prev = last["h"]
    a_prev = last.get("a", 1)

    num_helices = lane_config.get("helices", 2)
    phases = [i * 2 * math.pi / num_helices for i in range(num_helices)]

    record = {"n": n, "data": args.data, "helices": num_helices}
    a = a_prev
    h = h_prev.encode()
    for i, phase in enumerate(phases):
        a = spiral_next(a, n, phase)
        h = sha256_hex(struct.pack(">Q", a) + data_bytes + h.encode())
        record[f"a_helix_{i}"] = a
        record[f"h_helix_{i}"] = h

    path.write_text(path.read_text() + json.dumps(record, separators=(',', ':')) + "\n")
    print(json.dumps({"lane": args.lane, "n": n, "h": h, "helices": num_helices}))

def cmd_head(args):
    path = lane_path(args.lane)
    lines = path.read_text().splitlines()
    if not lines:
        print(json.dumps({"lane": args.lane, "n": 0, "h": "0"*64}))
        return
    last = json.loads(lines[-1])
    print(json.dumps({"lane": args.lane, "n": last["n"], "h": last[f"h_helix_{last['helices']-1}"]}))

parser = argparse.ArgumentParser()
sub = parser.add_subparsers()
init = sub.add_parser("init")
init.add_argument("--lane", required=True)
init.set_defaults(func=cmd_init)
append = sub.add_parser("append")
append.add_argument("--lane", required=True)
append.add_argument("--data", required=True)
append.set_defaults(func=cmd_append)
head = sub.add_parser("head")
head.add_argument("--lane", required=True)
head.set_defaults(func=cmd_head)

args = parser.parse_args()
args.func(args)
