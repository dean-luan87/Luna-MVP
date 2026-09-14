from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_api_v1 import (
    run_observation_manager_module_v1,
)


def build_observation_request_candidate_v1(
    input_candidate: Mapping[str, Any],
    vision_request_candidate: Mapping[str, Any],
    model_requirement_candidate: Mapping[str, Any],
    eligible_model_candidates: tuple[Mapping[str, Any], ...],
    result_link_contract: Mapping[str, Any],
) -> Dict[str, Any]:
    request = {
        "observation_request_id": f"obs_req::{input_candidate.get('plan_id')}",
        "source_plan_id": input_candidate.get("plan_id"),
        "vision_request_ref": vision_request_candidate.get("vision_request_id"),
        "model_requirement_ref": model_requirement_candidate.get("requirement_id"),
        "eligible_model_candidate_refs": tuple(
            c.get("model_asset_id") for c in eligible_model_candidates
        ),
        "task_id": input_candidate.get("task_id"),
        "field_snapshot_ref": input_candidate.get("field_snapshot_ref"),
        "information_gap_ref": input_candidate.get("information_gap_ref"),
        "observation_goal": input_candidate.get("observation_goal"),
        "target_region": input_candidate.get("target_region"),
        "expected_evidence_types": tuple(
            input_candidate.get("expected_evidence_types") or ()
        ),
        "temporal_window": input_candidate.get("temporal_window"),
        "priority": input_candidate.get("observation_priority"),
        "result_link_contract": dict(result_link_contract),
        "candidate_only": True,
    }

    obs_payload = {
        "observation_request_id": request["observation_request_id"],
        "request_type": "task_driven",
        "task_id": request["task_id"],
        "task_context": {
            "task_context_ref": f"task_ctx::{request['task_id']}",
            "subject_ref": "field_perception",
        },
        "scene_context": {
            "scene_context_ref": request["field_snapshot_ref"],
            "scene_id": request["field_snapshot_ref"],
        },
        "attention_targets": [request["observation_goal"]],
        "region_hints": [request["target_region"]],
        "vision_requested": True,
        "ocr_requested": "ocr_text"
        in tuple(request.get("expected_evidence_types") or ()),
        "permission_context": dict(input_candidate.get("permission_context") or {}),
        "version_snapshot": dict(input_candidate.get("version_snapshot") or {}),
        "trace_context": dict(input_candidate.get("trace_context") or {}),
    }
    obs_preview = run_observation_manager_module_v1(obs_payload)

    return {
        "observation_request_candidate": request,
        "observation_manager_preview": {
            "module_status": obs_preview.get("module_status"),
            "trace_ref": obs_preview.get("trace_ref"),
            "replay_key": obs_preview.get("replay_key"),
            "rejection_reasons": tuple(obs_preview.get("rejection_reasons") or ()),
        },
    }
