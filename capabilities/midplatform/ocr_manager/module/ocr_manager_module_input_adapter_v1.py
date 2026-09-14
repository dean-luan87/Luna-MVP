from __future__ import annotations

from typing import Any, Dict, Mapping


def adapt_ocr_manager_input_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    request_id = str(payload.get("request_id") or "").strip()
    source_ref = str(payload.get("source_ref") or "").strip()
    frame_ref = str(payload.get("frame_ref") or "").strip()
    request_type = str(payload.get("request_type") or "task_ocr_request").strip()
    source_kind = str(payload.get("source_kind") or "synthetic_fixture").strip()

    image_candidate = (
        payload.get("image_candidate")
        if isinstance(payload.get("image_candidate"), dict)
        else {}
    )
    visual_regions = (
        payload.get("visual_region_candidates")
        if isinstance(payload.get("visual_region_candidates"), list)
        else []
    )
    poster_regions = (
        payload.get("poster_region_candidates")
        if isinstance(payload.get("poster_region_candidates"), list)
        else []
    )
    task_ocr_request = (
        payload.get("task_ocr_request")
        if isinstance(payload.get("task_ocr_request"), dict)
        else {}
    )
    human_correction_input = (
        payload.get("human_correction_input")
        if isinstance(payload.get("human_correction_input"), list)
        else []
    )
    synthetic_fixture = (
        payload.get("synthetic_integration_fixture")
        if isinstance(payload.get("synthetic_integration_fixture"), dict)
        else {}
    )
    crossmodal_context = (
        payload.get("crossmodal_context")
        if isinstance(payload.get("crossmodal_context"), dict)
        else {}
    )

    rejection_reasons = []
    if not request_id:
        rejection_reasons.append("missing_request_id")
    if not source_ref:
        rejection_reasons.append("missing_source_ref")
    if not frame_ref:
        rejection_reasons.append("missing_frame_ref")

    image_path = str(image_candidate.get("image_path") or "")
    if image_path.startswith("/") and source_kind != "synthetic_fixture":
        rejection_reasons.append("unguarded_real_file_path")
    if bool(payload.get("camera_runtime_requested")):
        rejection_reasons.append("camera_runtime_forbidden")
    if bool(payload.get("fact_write_requested")):
        rejection_reasons.append("fact_write_forbidden")
    if bool(payload.get("action_execution_requested")):
        rejection_reasons.append("action_execution_forbidden")

    return {
        "request_id": request_id or "none",
        "source_ref": source_ref,
        "frame_ref": frame_ref,
        "request_type": request_type,
        "source_kind": source_kind,
        "image_candidate": image_candidate,
        "region_candidates": tuple(list(visual_regions) + list(poster_regions)),
        "task_ocr_request": task_ocr_request,
        "human_correction_input": tuple(human_correction_input),
        "synthetic_integration_fixture": synthetic_fixture,
        "crossmodal_context": crossmodal_context,
        "input_valid": len(rejection_reasons) == 0,
        "rejection_reasons": tuple(rejection_reasons),
    }
