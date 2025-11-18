# ================================================================
# HashHelix Ledger — ENGINE ONLY
# Runtime sealing for lane outputs.
#
# NOTE:
# - No Singularity Artifact logic
# - No Temporal Relic lifecycle
# - No vault (HOT/WARM/COLD) semantics
# ================================================================

import json
import hashlib
from typing import Any, Dict


def canonical_serialize(obj: Dict[str, Any]) -> bytes:
    """
    Canonical JSON serialization:
    - UTF-8
    - sorted keys
    - no extra whitespace
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_lane_artifact(
    *,
    lane_id: int,
    height: int,
    chiral_plus: str,
    chiral_minus: str,
    metadata: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Build an engine-only lane artifact:
    - laneId
    - height (sequence length)
    - chiral commitments
    - metadata (engine-safe only)
    """
    if metadata is None:
        metadata = {}

    body = {
        "version": "6.0-engine",
        "laneId": lane_id,
        "height": height,
        "chiral": {
            "h_plus": chiral_plus,
            "h_minus": chiral_minus,
        },
        "metadata": metadata,
    }

    serialized = canonical_serialize(body)
    digest = sha256_hex(serialized)

    return {
        "artifactKind": "laneArtifact",
        "artifactVersion": "6.0",
        "digest": digest,
        "body": body,
    }
import pathlib


def write_lane_artifact_json(path: str, artifact: Dict[str, Any]) -> None:
    """
    Write a lane artifact to disk as canonical JSON.
    This is engine-only: no private ledger, no Relic semantics.
    """
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(artifact, f, sort_keys=True, indent=2)


if __name__ == "__main__":
    # Simple demo: build a fake lane artifact and write it out.
    lane_id = 1
    height = 10000  # pretend this lane ran 10k steps

    # Placeholder chiral commitments for now.
    # Later we will wire these to real chiral_helix outputs.
    h_plus = "0" * 64
    h_minus = "f" * 64

    artifact = build_lane_artifact(
        lane_id=lane_id,
        height=height,
        chiral_plus=h_plus,
        chiral_minus=h_minus,
        metadata={"stage": 6, "profile": "sample"},
    )

    output_path = "artifacts/stage6_sample/lane01_artifact.json"
    write_lane_artifact_json(output_path, artifact)
    print(f"[OK] Wrote lane artifact → {output_path}")
