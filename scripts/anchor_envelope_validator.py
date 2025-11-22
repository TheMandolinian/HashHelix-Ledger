#!/usr/bin/env python3
"""
anchor_envelope_validator.py

Validates a Stage 9 Anchor Envelope JSON file against
schemas/anchor_envelope.stage9.json.

Usage:
    python3 scripts/anchor_envelope_validator.py path/to/envelope.json
"""

import json
import sys
from pathlib import Path

import jsonschema
from jsonschema import Draft7Validator


SCHEMA_PATH = Path("schemas/anchor_envelope.stage9.json")


def load_schema(schema_path: Path = SCHEMA_PATH) -> dict:
    """Load and return the Stage 9 anchor envelope schema."""
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    try:
        with schema_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Schema is not valid JSON: {schema_path}\n{e}") from e


def load_json(path: Path) -> dict:
    """Load and return JSON from path."""
    if not path.exists():
        raise FileNotFoundError(f"Envelope file not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Envelope is not valid JSON: {path}\n{e}") from e


def validate_envelope(envelope_path: Path) -> bool:
    """Validate a given envelope JSON file against the Stage 9 schema."""
    schema = load_schema()
    data = load_json(envelope_path)

    # Build validator so we can report *all* errors nicely
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    if errors:
        msg_lines = [f"[ERROR] Envelope failed Stage 9 schema validation: {envelope_path}"]
        for err in errors:
            loc = " -> ".join(map(str, err.path)) if err.path else "(root)"
            msg_lines.append(f"  - At {loc}: {err.message}")
        raise jsonschema.ValidationError("\n".join(msg_lines))

    return True


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] in {"-h", "--help"}:
        print(__doc__.strip())
        return 2  # conventional "usage" exit code

    envelope_path = Path(argv[1])

    try:
        validate_envelope(envelope_path)
        print("[OK] Envelope is valid according to Stage 9 schema.")
        return 0
    except Exception as e:
        print(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
