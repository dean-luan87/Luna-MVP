from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Mapping


def _stable_hash(payload: Mapping[str, Any]) -> str:
    text = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def build_trace_and_replay_v1(
    *,
    request_id: str,
    required_capability: str,
    module_status: str,
    selected_model_candidate: Mapping[str, Any],
    trace_context: Mapping[str, Any],
) -> Dict[str, str]:
    base = {
        "request_id": request_id,
        "required_capability": required_capability,
        "module_status": module_status,
        "selected_model_id": str(selected_model_candidate.get("model_id", "")),
        "trace_context": dict(trace_context),
    }
    digest = _stable_hash(base)
    return {
        "trace_ref": f"trace:model_manager:{request_id}:{digest}",
        "replay_key": f"replay:model_manager:{digest}",
    }
