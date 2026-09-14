from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Mapping


def _stable_hash(payload: Mapping[str, Any]) -> str:
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(blob).hexdigest()


def build_permission_and_admission_trace_replay_v1(
    input_candidate: Mapping[str, Any],
    eligibility: Mapping[str, Any],
) -> Dict[str, Any]:
    trace_payload = {
        "request_id": input_candidate.get("request_id"),
        "request_type": input_candidate.get("request_type"),
        "subject_ref": input_candidate.get("subject_ref"),
        "resource_ref": input_candidate.get("resource_ref"),
        "requested_authority": input_candidate.get("requested_authority"),
        "requested_operation": input_candidate.get("requested_operation"),
        "admission_status": eligibility.get("admission_status"),
        "rejection_reasons": tuple(eligibility.get("rejection_reasons") or ()),
        "candidate_only": True,
    }
    trace_ref = f"trace_{_stable_hash(trace_payload)[:16]}"
    replay_key = (
        f"replay_{_stable_hash({**trace_payload, 'trace_ref': trace_ref})[:16]}"
    )
    return {
        "schema_version": "permission_and_admission_trace_replay_v1",
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "trace_payload": trace_payload,
        "trace_present": True,
        "replay_present": True,
        "deterministic_replay_ready": True,
    }
