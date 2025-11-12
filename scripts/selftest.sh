#!/usr/bin/env bash
set -euo pipefail

echo "== Step 1: Verify all committed epochs =="
python3 scripts/epoch_tools.py verify "epochs/epoch-*.json"

echo "== Step 2: Compare HEAD chiral vs latest epoch commitment =="
python - <<'PY'
import json,hashlib,glob
lane="default-chiral"
last=json.loads(open("data/chiral_ledger.jsonl","rb").read().splitlines()[-1])
hp,hm=bytes.fromhex(last["h_plus"]),bytes.fromhex(last["h_minus"])
head_c=hashlib.sha256(min(hp,hm)+max(hp,hm)).hexdigest()
latest=sorted(glob.glob("epochs/epoch-*.json"))[-1]
ep=json.load(open(latest))
print("HEAD:", head_c)
print("EPOCH:", ep["chiral_commitments"][lane])
print("MATCH?", head_c==ep["chiral_commitments"][lane])
assert head_c==ep["chiral_commitments"][lane], "HEAD vs EPOCH commitment mismatch"
PY

echo "== Step 3: Fresh clone reproducibility check =="
tmpdir="$(mktemp -d)"
git clone . "$tmpdir/hh_verify" >/dev/null
(
  cd "$tmpdir/hh_verify"
  python3 scripts/epoch_tools.py verify "epochs/epoch-*.json"
)

echo "== Step 4: Tamper test (should FAIL) =="
cp data/chiral_ledger.jsonl "$tmpdir/chiral_ledger.jsonl.bak"
python - <<'PY'
import json,sys
p="data/chiral_ledger.jsonl"
lines=open(p,"rb").read().splitlines()
rec=json.loads(lines[-1])
rec["h_plus"]="0"*64  # corrupt last record
lines[-1]=(json.dumps(rec, separators=(',',':'))+"\n").encode()
open(p,"wb").write(b"\n".join(lines)+b"\n")
print("Corrupted last record in", p)
PY

if python3 scripts/epoch_tools.py verify "epochs/epoch-*.json"; then
  echo "ERROR: tamper test did not fail as expected"; exit 1
else
  echo "✅ Tamper test: FAIL as expected (good)"
fi

echo "== Step 5: Restore ledger file and re-verify =="
mv "$tmpdir/chiral_ledger.jsonl.bak" data/chiral_ledger.jsonl
python3 scripts/epoch_tools.py verify "epochs/epoch-*.json"

echo "== ALL SELFTESTS PASSED =="
