# -*- coding: utf-8 -*-
"""Object persistence candidate builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def build_object_persistence_candidates(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    tracks: List[Dict[str, Any]],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Build ObjectPersistenceCandidate from track sequences."""
    overrides = case_overrides or {}
    if raw_output.get("_blocked"):
        return []

    results: List[Dict[str, Any]] = []
    for track in tracks:
        bbox_seq = track.get("bbox_sequence") or []
        obs_count = overrides.get("observation_count", len(bbox_seq))
        lifecycle = track.get("lifecycle_status", "unknown")
        identity_switch_risk = track.get("_identity_switch_risk", overrides.get("identity_switch_risk", "low"))
        short_track = obs_count < 2 or overrides.get("short_track") is True

        if lifecycle == "lost":
            persistence_status = "short_lived_candidate"
            persistence_conf = "low"
            identity_stability = "unstable"
        elif short_track:
            persistence_status = "short_lived_candidate"
            persistence_conf = "low"
            identity_stability = "unstable"
        elif identity_switch_risk in ("high", "severe"):
            persistence_status = "unstable_candidate"
            persistence_conf = "medium"
            identity_stability = "unstable"
        elif obs_count >= 3:
            persistence_status = "persistent_candidate"
            persistence_conf = "medium" if obs_count < 5 else "medium"
            identity_stability = "stable" if identity_switch_risk == "low" else "unstable"
        else:
            persistence_status = "unknown"
            persistence_conf = "low"
            identity_stability = "unknown"

        if persistence_conf == "high" and obs_count < 3:
            persistence_conf = "medium"

        persist_id = f"opc_{uuid.uuid4().hex[:12]}"
        ts_range = track.get("timestamp_range") or {}
        results.append({
            "object_persistence_candidate_id": persist_id,
            "source_track_ref": track.get("object_track_candidate_id"),
            "source_object_observation_refs": track.get("source_object_observation_refs") or [],
            "candidate_entity_key": f"entity_{track.get('track_id', persist_id)}",
            "persistence_status": persistence_status,
            "observation_count": obs_count,
            "first_seen_at": ts_range.get("start"),
            "last_seen_at": ts_range.get("end"),
            "persistence_confidence": persistence_conf,
            "identity_stability": identity_stability,
            "conflict_refs": overrides.get("conflict_refs") or [],
            "warning_codes": track.get("warning_codes") or [],
            "missing_information": track.get("missing_information") or [],
            "source_refs": [track.get("object_track_candidate_id"), adapter_input.get("adapter_input_id")],
            "evidence_refs": [adapter_input.get("model_ref")],
            "traceability_refs": list(track.get("traceability_refs") or []) + [persist_id],
            "candidate_only": True,
        })
    return results
