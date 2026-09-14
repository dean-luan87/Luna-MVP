from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

from capabilities.midplatform.vision_manager.module.vision_manager_trace_replay_v1 import (
    build_vision_trace_replay_v1,
)
from capabilities.vision.schemas.vision_event import VisionEvent
from capabilities.midplatform.vision_recognition_evidence_readonly_ingest_candidate_v0 import (
    roi_type_from_roi_id_v0,
)

ALLOWED_OBSERVATION_REQUESTS = {
    "observe_forward_path",
    "observe_signage_area",
    "observe_task_target_area",
    "observe_safety_risk",
    "observe_readable_region",
}


def _frame_quality_status(frame_quality: str) -> str:
    value = str(frame_quality or "").strip().lower()
    if value in {"good", "ok", "clear"}:
        return "good"
    if value in {"insufficient", "low", "blurred", "dark"}:
        return "insufficient"
    return "unknown"


def _attention_plan(attention_target: str, admitted: bool) -> Dict[str, Any]:
    target = str(attention_target or "").strip()
    return {
        "plan_id": f"attention_plan_{target or 'none'}",
        "target": target,
        "active": bool(target) and admitted,
        "candidate_only": True,
        "action_allowed": False,
    }


def _roi_region_candidates(
    request_id: str, attention_target: str
) -> Tuple[Tuple[Dict[str, Any], ...], Tuple[Dict[str, Any], ...]]:
    roi_id = f"{request_id}_upper_sign_roi"
    roi = {
        "roi_id": roi_id,
        "roi_type": roi_type_from_roi_id_v0(roi_id),
        "attention_target": attention_target,
        "candidate_only": True,
        "runtime_allowed": False,
    }
    region = {
        "region_id": f"region_{request_id}",
        "region_type": "surface_candidate",
        "source_roi_id": roi_id,
        "candidate_only": True,
        "runtime_allowed": False,
    }
    return (roi,), (region,)


def _detection_candidates(
    request_id: str, attention_target: str
) -> Tuple[Dict[str, Any], ...]:
    event = VisionEvent(
        event_id=f"det_evt_{request_id}",
        timestamp=0.0,
        source="vision_manager_module_v1",
        provider_name="vision_stub",
        model_name="candidate_detector",
        event_type="detection",
        confidence=0.7,
        frame_id=request_id,
        metadata={"attention_target": attention_target, "candidate_only": True},
    )
    return (
        {
            "candidate_id": f"det_cand_{request_id}",
            "event": event.__dict__,
            "normalized": True,
            "candidate_only": True,
        },
    )


def run_vision_manager_module_v1(request: Mapping[str, Any]) -> Dict[str, Any]:
    request_id = str(request.get("request_id") or "").strip()
    capability = str(request.get("capability") or "").strip()
    observation_request = str(request.get("observation_request") or "").strip()
    attention_target = str(request.get("attention_target") or "").strip()
    frame_quality = str(request.get("frame_quality") or "").strip()
    model_test_lens = str(request.get("model_test_lens") or "").strip()
    ownership_ok = bool(request.get("ownership_ok", True))
    version_snapshot = (
        request.get("version_snapshot")
        if isinstance(request.get("version_snapshot"), dict)
        else {}
    )

    rejection_reasons = []
    input_valid = True
    if not request_id:
        rejection_reasons.append("missing_request_id")
        input_valid = False
    if not capability:
        rejection_reasons.append("missing_capability")
        input_valid = False
    if not version_snapshot:
        rejection_reasons.append("missing_version_snapshot")
        input_valid = False

    admitted_visual_input = (
        input_valid and observation_request in ALLOWED_OBSERVATION_REQUESTS
    )
    if input_valid and not admitted_visual_input:
        rejection_reasons.append("invalid_observation_request")

    quality_status = _frame_quality_status(frame_quality)
    attention_plan = _attention_plan(attention_target, admitted_visual_input)
    roi_candidates, region_candidates = _roi_region_candidates(
        request_id or "none", attention_target
    )

    model_capability_request = {
        "request_id": f"model_cap_req_{request_id or 'none'}",
        "capability": "luna.model_manager",
        "model_test_lens": model_test_lens or "default",
        "candidate_only": True,
        "runtime_allowed": False,
    }

    model_handoff_candidate: Dict[str, Any] = {}
    if (
        admitted_visual_input
        and quality_status == "good"
        and attention_plan["active"]
        and ownership_ok
    ):
        model_handoff_candidate = {
            "candidate_id": f"model_handoff_{request_id}",
            "target_capability": "luna.model_manager",
            "handoff_ready": True,
            "candidate_only": True,
            "runtime_allowed": False,
        }

    if model_test_lens == "blocked":
        model_handoff_candidate = {}
        rejection_reasons.append("model_handoff_blocked")

    detection_candidates = (
        _detection_candidates(request_id or "none", attention_target)
        if admitted_visual_input
        else tuple()
    )
    segmentation_candidates = (
        (
            {
                "candidate_id": f"seg_cand_{request_id or 'none'}",
                "normalized": True,
                "candidate_only": True,
                "runtime_allowed": False,
            },
        )
        if admitted_visual_input
        else tuple()
    )
    tracking_candidates = (
        (
            {
                "candidate_id": f"trk_cand_{request_id or 'none'}",
                "normalized": True,
                "candidate_only": True,
                "runtime_allowed": False,
            },
        )
        if admitted_visual_input
        else tuple()
    )

    scene_evidence_candidates = (
        (
            {
                "candidate_id": f"scene_evd_{request_id or 'none'}",
                "source_refs": [c.get("candidate_id") for c in detection_candidates],
                "candidate_only": True,
            },
        )
        if admitted_visual_input
        else tuple()
    )

    composed_visual_evidence = {
        "evidence_id": f"visual_evd_pack_{request_id or 'none'}",
        "detection_count": len(detection_candidates),
        "segmentation_count": len(segmentation_candidates),
        "tracking_count": len(tracking_candidates),
        "candidate_only": True,
        "fact_status": "not_fact",
    }

    correction_candidates = tuple()
    if quality_status == "insufficient":
        correction_candidates = (
            {
                "candidate_id": f"correction_{request_id or 'none'}",
                "type": "human_correction",
                "suggestion": "hold_still_or_recenter",
                "candidate_only": True,
            },
        )

    degradation_plan = {
        "plan_id": f"degrade_{request_id or 'none'}",
        "degraded": quality_status != "good" or not bool(model_handoff_candidate),
        "reason_codes": tuple(rejection_reasons),
        "candidate_only": True,
    }

    if not input_valid:
        module_status = "invalid_observation_request"
    elif quality_status == "insufficient":
        module_status = "frame_quality_insufficient"
    elif not attention_plan["active"]:
        module_status = "no_attention_target"
    elif model_test_lens == "blocked":
        module_status = "model_handoff_blocked"
    elif not ownership_ok:
        module_status = "ownership_blocked"
    elif not model_handoff_candidate:
        module_status = "degraded_without_model"
    elif correction_candidates:
        module_status = "human_correction_candidate"
    else:
        module_status = "ready"

    diagnostics = {
        "input_valid": input_valid,
        "observation_request": observation_request,
        "ownership_ok": ownership_ok,
        "boundary_ok": True,
        "candidate_only": True,
    }

    trace = build_vision_trace_replay_v1(
        request_id=request_id or "none",
        capability=capability or "luna.vision_manager",
        module_status=module_status,
        model_handoff_candidate=model_handoff_candidate,
    )

    return {
        "module_status": module_status,
        "admitted_visual_input": admitted_visual_input,
        "frame_quality_status": quality_status,
        "attention_plan": attention_plan,
        "roi_candidates": roi_candidates,
        "region_candidates": region_candidates,
        "model_capability_request": model_capability_request,
        "model_handoff_candidate": model_handoff_candidate,
        "detection_candidates": detection_candidates,
        "segmentation_candidates": segmentation_candidates,
        "tracking_candidates": tracking_candidates,
        "scene_evidence_candidates": scene_evidence_candidates,
        "composed_visual_evidence": composed_visual_evidence,
        "correction_candidates": correction_candidates,
        "degradation_plan": degradation_plan,
        "diagnostics": diagnostics,
        "rejection_reasons": tuple(rejection_reasons),
        "trace_ref": trace["trace_ref"],
        "replay_key": trace["replay_key"],
        "camera_invoked": False,
        "visual_model_invoked": False,
        "ocr_provider_invoked": False,
        "segmentation_runtime_invoked": False,
        "tracking_runtime_invoked": False,
        "world_model_written": False,
        "memory_written": False,
        "fact_written": False,
        "navigation_action_triggered": False,
        "production_runtime_executed": False,
    }
