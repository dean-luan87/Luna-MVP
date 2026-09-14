from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Mapping


def _stable_hash(payload: Mapping[str, Any]) -> str:
    blob = json.dumps(payload, ensure_ascii=True, sort_keys=True, default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(blob).hexdigest()


def build_visual_handoff_trace_replay_v1(
    input_candidate: Mapping[str, Any],
    integration_status: str,
) -> Dict[str, Any]:
    base = {
        "handoff_request_id": input_candidate.get("handoff_request_id"),
        "plan_id": input_candidate.get("plan_id"),
        "task_id": input_candidate.get("task_id"),
        "field_snapshot_ref": input_candidate.get("field_snapshot_ref"),
        "information_gap_ref": input_candidate.get("information_gap_ref"),
        "observation_goal": input_candidate.get("observation_goal"),
        "integration_status": integration_status,
    }
    trace_ref = f"trace_{_stable_hash(base)[:16]}"
    replay_key = f"replay_{_stable_hash({**base, 'trace_ref': trace_ref})[:16]}"
    return {
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "deterministic_replay_ready": True,
    }
