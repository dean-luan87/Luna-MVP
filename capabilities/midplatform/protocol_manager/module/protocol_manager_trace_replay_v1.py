from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Mapping


def _stable_hash(payload: Mapping[str, Any]) -> str:
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(blob).hexdigest()


def build_protocol_manager_trace_replay_v1(
    input_candidate: Mapping[str, Any],
    module_status: str,
    compatibility_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    trace_payload = {
        "protocol_request_id": input_candidate.get("protocol_request_id"),
        "operation": input_candidate.get("operation"),
        "protocol_id": input_candidate.get("protocol_id"),
        "module_status": module_status,
        "compatibility_result": compatibility_candidate.get("compatibility_result"),
        "candidate_only": True,
    }
    trace_ref = f"trace_{_stable_hash(trace_payload)[:16]}"
    replay_key = (
        f"replay_{_stable_hash({**trace_payload, 'trace_ref': trace_ref})[:16]}"
    )
    return {
        "schema_version": "protocol_manager_trace_replay_v1",
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "trace_present": True,
        "replay_present": True,
        "deterministic_replay_ready": True,
        "trace_payload": trace_payload,
    }
