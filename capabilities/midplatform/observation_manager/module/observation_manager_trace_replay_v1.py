from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Mapping


def _stable_hash(payload: Mapping[str, Any]) -> str:
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(blob).hexdigest()


def build_observation_manager_trace_replay_v1(
    input_candidate: Mapping[str, Any],
    status_hint: str,
) -> Dict[str, Any]:
    trace_payload = {
        "observation_request_id": input_candidate.get("observation_request_id"),
        "request_type": input_candidate.get("request_type"),
        "task_id": input_candidate.get("task_id"),
        "status_hint": status_hint,
        "candidate_only": True,
    }
    trace_ref = f"trace_{_stable_hash(trace_payload)[:16]}"
    replay_key = (
        f"replay_{_stable_hash({**trace_payload, 'trace_ref': trace_ref})[:16]}"
    )
    return {
        "schema_version": "observation_manager_trace_replay_v1",
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "trace_payload": trace_payload,
        "trace_present": True,
        "replay_present": True,
        "deterministic_replay_ready": True,
    }
