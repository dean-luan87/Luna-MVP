from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Mapping


def _stable_hash(payload: Mapping[str, Any]) -> str:
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(blob).hexdigest()


def build_system_maintenance_trace_replay_v1(
    input_candidate: Mapping[str, Any],
    module_status: str,
    primary_capability_candidate: str,
) -> Dict[str, Any]:
    trace_payload = {
        "maintenance_request_id": input_candidate.get("maintenance_request_id"),
        "anomaly_type": input_candidate.get("anomaly_type"),
        "source_capability_id": input_candidate.get("source_capability_id"),
        "primary_capability_candidate": primary_capability_candidate,
        "module_status": module_status,
        "runtime_mode": input_candidate.get("runtime_mode"),
    }
    trace_ref = f"trace_{_stable_hash(trace_payload)[:16]}"
    replay_key = (
        f"replay_{_stable_hash({**trace_payload, 'trace_ref': trace_ref})[:16]}"
    )
    return {
        "schema_version": "system_maintenance_trace_replay_v1",
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "trace_present": True,
        "replay_present": True,
        "deterministic_replay_ready": True,
    }
