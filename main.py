# main.py
import argparse
from ledger import Ledger
from chiral_helix import ChiralLedger

def main():
    parser = argparse.ArgumentParser(description="HashHelix ledger CLI")
    parser.add_argument("--mode", choices=["single", "chiral"], default="single",
                        help="single-helix or dual-helix (chiral)")
    parser.add_argument("--file", help="path to ledger file (auto-creates on first use)")
    parser.add_argument("--append", help="append a new record with this string")
    parser.add_argument("--head", action="store_true", help="print the current head")
    parser.add_argument("--verify", action="store_true", help="verify full ledger integrity")
    args = parser.parse_args()

    # choose defaults by mode if file not provided
    file_path = args.file or ("data/ledger.jsonl" if args.mode == "single"
                              else "data/chiral_ledger.jsonl")

    if args.mode == "single":
        lg = Ledger(file_path)
    else:
        lg = ChiralLedger(file_path)

    if args.append:
        e = lg.append(args.append)
        print("APPENDED:", e)

    if args.head:
        print("HEAD:", lg.head())

    if args.verify:
        print("VERIFY:", lg.verify())

if __name__ == "__main__":
    main()
