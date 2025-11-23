# scripts/anchor_envelope_validator.py
# Stage 9 anchor envelope validator (engine-only)

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

from jsonschema import Draft202012Validator


SCHEMA_PATH = Path("schemas/anchor_envelope.stage9.json")


def load_schema() -> Dict[str, Any]:
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema not found: {SCHEMA_PATH}")
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    # Ensure schema itself is valid
    Draft202012Validator.check_schema(schema)
    return schema


def validate_envelope(envelope_path: Path) -> None:
    if not envelope_path.exists():
        raise FileNotFoundError(f"Envelope file not found: {envelope_path}")

    schema = load_schema()
    with envelope_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    if errors:
        msg_lines = ["[ERROR] Envelope failed Stage 9 schema validation:"]
        for e in errors:
            loc = ".".join([str(p) for p in e.path]) or "(root)"
            msg_lines.append(f" - At {loc}: {e.message}")
        raise ValueError("\n".join(msg_lines))


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python scripts/anchor_envelope_validator.py <path_to_envelope.json>")
        return 2

    envelope_path = Path(argv[1])

    try:
        validate_envelope(envelope_path)
        print("[OK] Envelope is valid according to Stage 9 schema.")
        return 0
    except Exception as e:
        print(str(e))
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
