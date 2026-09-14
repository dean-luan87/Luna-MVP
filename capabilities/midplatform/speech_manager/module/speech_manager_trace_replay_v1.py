from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Mapping


def _stable_hash(payload: Mapping[str, Any]) -> str:
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(blob).hexdigest()


def build_speech_manager_trace_replay_v1(
    input_candidate: Mapping[str, Any],
    governance: Mapping[str, Any],
    content_candidate: Mapping[str, Any],
    interruption_plan: Mapping[str, Any],
    provider_candidates: Mapping[str, Any],
) -> Dict[str, Any]:
    trace_payload = {
        "request_id": input_candidate.get("request_id"),
        "source_ref": input_candidate.get("source_ref"),
        "priority_level": input_candidate.get("priority_level"),
        "interruption_intent_type": input_candidate.get("interruption_intent_type"),
        "admitted": governance.get("admitted"),
        "normalized_text": content_candidate.get("normalized_text"),
        "selected_action_candidate": interruption_plan.get("selected_action_candidate"),
        "gate_allowed": provider_candidates.get("speech_gate_candidate", {}).get(
            "gate_allowed"
        ),
        "candidate_only": True,
    }
    trace_ref = f"trace_{_stable_hash(trace_payload)[:16]}"
    replay_key = (
        f"replay_{_stable_hash({**trace_payload, 'trace_ref': trace_ref})[:16]}"
    )
    return {
        "schema_version": "speech_manager_trace_replay_v1",
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "trace_payload": trace_payload,
        "trace_present": True,
        "replay_present": True,
        "deterministic_replay_ready": True,
    }
