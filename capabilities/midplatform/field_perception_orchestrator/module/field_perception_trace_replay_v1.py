from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Mapping


def _stable_hash(payload: Mapping[str, Any]) -> str:
    blob = json.dumps(payload, ensure_ascii=True, sort_keys=True, default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(blob).hexdigest()


def build_field_perception_trace_replay_v1(
    input_candidate: Mapping[str, Any],
    module_status: str,
    observation_goal: str,
) -> Dict[str, Any]:
    base = {
        "task_id": input_candidate.get("task_id"),
        "task_goal": input_candidate.get("task_goal"),
        "module_status": module_status,
        "observation_goal": observation_goal,
    }
    trace_ref = f"trace_{_stable_hash(base)[:16]}"
    replay_key = f"replay_{_stable_hash({**base, 'trace_ref': trace_ref})[:16]}"
    return {
        "schema_version": "field_perception_trace_replay_v1",
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "deterministic_replay_ready": True,
    }
