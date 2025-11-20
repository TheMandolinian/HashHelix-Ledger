import json
import jsonschema
from jsonschema import validate

def load_schema():
    with open("schemas/anchor_envelope.stage9.json", "r") as f:
        return json.load(f)

def validate_envelope(path):
    schema = load_schema()
    with open(path, "r") as f:
        data = json.load(f)
    validate(instance=data, schema=schema)
    return True

if __name__ == "__main__":
    import sys
    try:
        result = validate_envelope(sys.argv[1])
        print("[OK] Envelope is valid according to Stage 9 schema.")
    except Exception as e:
        print("[ERROR]", e)

