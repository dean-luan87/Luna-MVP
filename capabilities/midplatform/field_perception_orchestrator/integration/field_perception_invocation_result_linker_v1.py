from __future__ import annotations

from typing import Any, Dict, Mapping


def build_result_link_contract_v1(
    input_candidate: Mapping[str, Any],
    handoff_id: str,
    vision_request_id: str,
    model_requirement_id: str,
    observation_request_id: str,
    trace_ref: str,
    replay_key: str,
) -> Dict[str, Any]:
    return {
        "handoff_id": handoff_id,
        "plan_id": input_candidate.get("plan_id"),
        "vision_request_id": vision_request_id,
        "model_requirement_id": model_requirement_id,
        "observation_request_id": observation_request_id,
        "task_id": input_candidate.get("task_id"),
        "field_snapshot_ref": input_candidate.get("field_snapshot_ref"),
        "information_gap_ref": input_candidate.get("information_gap_ref"),
        "expected_evidence_types": tuple(
            input_candidate.get("expected_evidence_types") or ()
        ),
        "result_return_target": "Observation Manager",
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "candidate_only": True,
    }
