from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def build_observation_ocr_request_candidate_v1(
    input_candidate: Mapping[str, Any],
    task_context: Mapping[str, Any],
    scene_context: Mapping[str, Any],
    region_plan: Mapping[str, Any],
) -> Dict[str, Any]:
    request_type = str(input_candidate.get("request_type") or "")
    ocr_requested = bool(input_candidate.get("ocr_requested", True))
    if request_type in {"find_text", "read_text", "human_correction_review"}:
        ocr_requested = True
    candidate = {
        "schema_version": "observation_manager_ocr_request_candidate_v1",
        "ocr_request_id": f"ocr_req_{input_candidate.get('observation_request_id')}",
        "task_id": input_candidate.get("task_id"),
        "task_context_ref": task_context.get("task_context_ref"),
        "scene_context_ref": scene_context.get("scene_context_ref"),
        "region_refs": tuple(
            (region_plan.get("region_plan") or {}).get("region_refs") or ()
        ),
        "expected_output": "ocr_evidence",
        "candidate_only": True,
        **not_fact(),
    }
    return {
        "schema_version": "observation_manager_ocr_adapter_v1",
        "ocr_request_candidate": candidate if ocr_requested else None,
        "ocr_request_candidate_present": ocr_requested,
        **not_fact(),
    }
