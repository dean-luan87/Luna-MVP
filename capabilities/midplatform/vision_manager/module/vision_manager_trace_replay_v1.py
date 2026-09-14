from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


def build_vision_trace_replay_v1(
    *,
    request_id: str,
    capability: str,
    module_status: str,
    model_handoff_candidate: Dict[str, Any],
) -> Dict[str, str]:
    payload = {
        "request_id": request_id,
        "capability": capability,
        "module_status": module_status,
        "model_candidate_id": str(model_handoff_candidate.get("candidate_id") or ""),
    }
    stable = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    digest = hashlib.sha256(stable.encode("utf-8")).hexdigest()
    return {
        "trace_ref": f"vision_trace_v1_{digest[:24]}",
        "replay_key": f"vision_replay_v1_{digest[24:48]}",
    }
