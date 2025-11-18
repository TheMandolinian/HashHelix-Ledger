# ================================================================
# HashHelix Ledger — ENGINE ONLY
# Stage 6: Runtime sealing for lane artifacts and engine bundles.
#
# PUBLIC ENGINE ONLY:
# - No Singularity Artifact logic
# - No Temporal Relic lifecycle
# - No vault (HOT/WARM/COLD) semantics
# - No business / economic fields
# ================================================================

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List


# -----------------------------
# Canonical serialization & hash
# -----------------------------


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


# -----------------------------
# Lane artifact (engine-only)
# -----------------------------


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

    body: Dict[str, Any] = {
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


# -----------------------------
# Bundle (engine-only .hhl)
# -----------------------------


def build_engine_bundle(
    *,
    lane_artifacts: List[Dict[str, Any]],
    bundle_id: str,
    engine: str = "HashHelix-Ledger",
    engine_version: str = "v1.6",
    engine_commit: str | None = None,
    created_at: str | None = None,
) -> Dict[str, Any]:
    """
    Build a Stage 6 engine-only bundle (.hhl) that matches
    schemas/hashBundle.stage6.json.

    NOTE: bundle_hash is computed over the bundle *without* the `seal`
    field, then the seal is attached. This keeps the seal from
    self-referential hashing.
    """
    if created_at is None:
        created_at = (
            datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )

    bundle_core: Dict[str, Any] = {
        "bundle_format": "hhl.bundle",
        "stage": 6,
        "engine": engine,
        "engine_version": engine_version,
        "bundle_id": bundle_id,
        "created_at": created_at,
        "lane_artifacts": lane_artifacts,
    }

    if engine_commit is not None:
        bundle_core["engine_commit"] = engine_commit

    # Canonicalize the core (no seal) and hash it
    canonical = canonical_serialize(bundle_core)
    bundle_hash = sha256_hex(canonical)

    seal: Dict[str, Any] = {
        "hash_function": "sha256",
        "canonicalization": "RFC8785",
        "bundle_hash": bundle_hash,
        # "lanes_root" can be added later if/when you define that aggregate.
    }

    bundle: Dict[str, Any] = dict(bundle_core)
    bundle["seal"] = seal
    return bundle


def write_sample_bundle() -> None:
    """
    Load the existing Stage 6 sample lane artifact and wrap it
    into a single-lane .hhl bundle.
    """
    artifact_path = Path("artifacts/stage6_sample/lane01_artifact.json")
    if not artifact_path.exists():
        raise SystemExit(
            f"[ERROR] Missing lane artifact: {artifact_path}. "
            "Run the lane generator first or restore the sample."
        )

    with artifact_path.open("r", encoding="utf-8") as f:
        lane_artifact = json.load(f)

    bundle = build_engine_bundle(
        lane_artifacts=[lane_artifact],
        bundle_id="stage6-lane01-sample",
        engine="HashHelix-Ledger",
        engine_version="v1.6-dev",
        # engine_commit can be plumbed from `git rev-parse` later if desired.
    )

    out_path = Path("artifacts/stage6_sample/lane01.hhl.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, sort_keys=True)

    print(f"[OK] Loaded lane artifact → {artifact_path}")
    print(f"[OK] Wrote Stage 6 bundle → {out_path}")


if __name__ == "__main__":
    write_sample_bundle()

