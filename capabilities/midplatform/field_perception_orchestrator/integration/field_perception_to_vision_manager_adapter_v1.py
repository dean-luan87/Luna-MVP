from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.vision_manager.module.vision_manager_module_api_v1 import (
    run_vision_manager_module_api_v1,
)


def build_vision_request_candidate_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    request = {
        "vision_request_id": f"vision_req::{input_candidate.get('plan_id')}",
        "source_plan_id": input_candidate.get("plan_id"),
        "task_id": input_candidate.get("task_id"),
        "field_snapshot_ref": input_candidate.get("field_snapshot_ref"),
        "information_gap_ref": input_candidate.get("information_gap_ref"),
        "observation_goal": input_candidate.get("observation_goal"),
        "requested_capabilities": tuple(
            input_candidate.get("requested_visual_capabilities") or ()
        ),
        "target_region": input_candidate.get("target_region"),
        "target_entity_types": tuple(input_candidate.get("target_entity_types") or ()),
        "resolution_level": input_candidate.get("resolution_level"),
        "temporal_window": input_candidate.get("temporal_window"),
        "priority": input_candidate.get("observation_priority"),
        "confidence_requirement": input_candidate.get("confidence_requirement"),
        "expected_evidence_types": tuple(
            input_candidate.get("expected_evidence_types") or ()
        ),
        "candidate_only": True,
    }

    vm_payload = {
        "request_id": request["vision_request_id"],
        "capability": "luna.vision_manager",
        "observation_request": "observe_task_target_area",
        "attention_target": request["target_region"] or "global",
        "frame_quality": "good",
        "model_test_lens": "default",
        "ownership_ok": True,
        "version_snapshot": dict(input_candidate.get("version_snapshot") or {}),
        "trace_context": dict(input_candidate.get("trace_context") or {}),
    }
    vm_preview = run_vision_manager_module_api_v1(vm_payload)
    return {
        "vision_request_candidate": request,
        "vision_manager_preview": {
            "module_status": vm_preview.get("module_status"),
            "rejection_reasons": tuple(vm_preview.get("rejection_reasons") or ()),
            "trace_ref": vm_preview.get("trace_ref"),
            "replay_key": vm_preview.get("replay_key"),
        },
    }
