# -*- coding: utf-8 -*-
"""Vision frame input governance v0 — gate frames before ROI / recognition (no ML)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


GOVERNANCE_MATRIX_SCHEMA = "vision_frame_input_governance_matrix_v0"
CANDIDATE_SCHEMA_VERSION = "vision_frame_input_candidate_v0"


def _safe_int(v: Any, default: int = 0) -> int:
    if v is None:
        return default
    return int(v)


def load_vision_frame_traces_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if isinstance(o, dict):
            rows.append(o)
    return rows


def _image_dimensions_v0(image_ref: str) -> Tuple[int, int]:
    p = Path(image_ref)
    if not p.is_file():
        return 0, 0
    try:
        from PIL import Image  # type: ignore

        with Image.open(p) as im:
            w, h = im.size
            return int(w), int(h)
    except Exception:
        return 0, 0


def evaluate_single_frame_governance_v0(
    *,
    trace: Dict[str, Any],
    registry_width: int,
    registry_height: int,
    max_edge: int = 8192,
    min_edge: int = 8,
) -> Dict[str, Any]:
    """Return one governance row + STCM/performance placeholder fields."""
    frame_id = str(trace.get("frame_id") or "")
    frame_index = _safe_int(trace.get("frame_index"))
    image_ref = str(trace.get("image_ref") or "")
    iw, ih = _image_dimensions_v0(image_ref)
    if iw <= 0 or ih <= 0:
        iw, ih = registry_width, registry_height

    reject_codes: List[str] = []
    img_path = Path(image_ref)
    if not image_ref.strip():
        reject_codes.append("missing_image_ref")
    elif not img_path.is_file():
        reject_codes.append("image_file_missing")

    normalization_required = False
    recommended_strategy = "use_as_is"
    if iw > max_edge or ih > max_edge:
        normalization_required = True
        recommended_strategy = "resize"
    elif iw < min_edge or ih < min_edge:
        recommended_strategy = "reject"
        reject_codes.append("dimensions_below_minimum")

    hard_reject = bool(
        {"missing_image_ref", "image_file_missing", "dimensions_below_minimum"} & set(reject_codes)
    )
    frame_accepted = not hard_reject

    anchor = trace.get("stcm_anchor") if isinstance(trace.get("stcm_anchor"), dict) else {}
    observed = _safe_int(anchor.get("observed_at_ms"), trace.get("timestamp_ms"))
    valid_until = anchor.get("valid_until_ms")

    stcm_deadline_hint = valid_until
    frame_validity_hint = "valid_in_offline_eval_buffer_v0"
    performance_budget_hint = "performance_controller_not_wired_placeholder_v0"
    degradation_reason_codes: List[str] = []
    if not frame_accepted:
        degradation_reason_codes.append("frame_not_accepted_for_roi_pipeline")
    if normalization_required:
        degradation_reason_codes.append("resize_recommended_before_roi")

    keyframe_candidate = frame_index % 4 == 0

    return {
        "frame_id": frame_id,
        "frame_index": frame_index,
        "image_ref": image_ref,
        "width": iw,
        "height": ih,
        "frame_accepted": frame_accepted,
        "reject_reason_codes": reject_codes,
        "normalization_required": normalization_required,
        "recommended_strategy": recommended_strategy,
        "eligible_for_roi_proposal": bool(frame_accepted),
        "eligible_for_recognition": False,
        "stcm_deadline_hint": stcm_deadline_hint,
        "frame_validity_hint": frame_validity_hint,
        "performance_budget_hint": performance_budget_hint,
        "degradation_reason_codes": degradation_reason_codes,
        "keyframe_candidate": keyframe_candidate,
    }


def build_vision_frame_input_governance_audit_v0() -> Dict[str, Any]:
    return {
        "schema": "vision_frame_input_governance_audit_v0",
        "frame_input_governance_executed": True,
        "real_camera_invoked": False,
        "yolo_invoked": False,
        "ocr_invoked": False,
        "vlm_invoked": False,
        "supervision_mainline_invoked": False,
        "vision_recognition_provider_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
    }


def run_vision_frame_input_governance_v0(trace_root: Path, output_root: Path) -> Dict[str, Any]:
    trace_root = Path(trace_root).resolve()
    output_root = Path(output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    reg = json.loads((trace_root / "vision_stream_registry.json").read_text(encoding="utf-8"))
    traces = load_vision_frame_traces_jsonl(trace_root / "vision_frame_trace.jsonl")
    rw = _safe_int(reg.get("width"), 640)
    rh = _safe_int(reg.get("height"), 480)
    stream_id = str(reg.get("stream_id") or "")

    matrix_rows: List[Dict[str, Any]] = []
    for tr in sorted(traces, key=lambda t: _safe_int(t.get("frame_index"))):
        matrix_rows.append(evaluate_single_frame_governance_v0(trace=tr, registry_width=rw, registry_height=rh))

    total_frames = len(matrix_rows)
    accepted_frames = sum(1 for r in matrix_rows if r.get("frame_accepted"))
    rejected_frames = total_frames - accepted_frames
    normalization_required_count = sum(1 for r in matrix_rows if r.get("normalization_required"))
    keyframe_candidate_count = sum(1 for r in matrix_rows if r.get("keyframe_candidate"))
    eligible_for_roi = sum(1 for r in matrix_rows if r.get("eligible_for_roi_proposal"))
    eligible_for_recognition_count = 0

    summary = {
        "schema": "vision_frame_input_governance_summary_v0",
        "phase": "Phase-Vision-Frame-Input-Governance-001",
        "frame_trace_root": str(trace_root),
        "stream_id": stream_id,
        "total_frames": total_frames,
        "accepted_frames": accepted_frames,
        "rejected_frames": rejected_frames,
        "normalization_required_count": normalization_required_count,
        "keyframe_candidate_count": keyframe_candidate_count,
        "eligible_for_roi_proposal_count": eligible_for_roi,
        "eligible_for_recognition_count": eligible_for_recognition_count,
        "stcm_deadline_hint_global": None,
        "frame_validity_hint_global": "offline_trace_aligned_v0",
        "performance_budget_hint_global": "performance_controller_not_wired_placeholder_v0",
        "degradation_reason_codes_global": [],
    }

    frames_candidate: List[Dict[str, Any]] = []
    for r in matrix_rows:
        if not r.get("frame_accepted"):
            continue
        frames_candidate.append(
            {
                "frame_id": str(r.get("frame_id") or ""),
                "image_ref": str(r.get("image_ref") or ""),
                "input_status": "accepted",
                "recommended_next_stage": "roi_proposal_stub",
            }
        )

    candidate = {
        "schema_version": CANDIDATE_SCHEMA_VERSION,
        "stream_id": stream_id,
        "source_trace_root": str(trace_root),
        "candidate_scope": "input_governance_only",
        "frames": frames_candidate,
        "forbidden_next_stages": [
            "vision_recognition_provider",
            "navigation_decision",
            "midplatform_fact_write",
        ],
    }

    matrix = {"schema": GOVERNANCE_MATRIX_SCHEMA, "rows": matrix_rows}
    audit = build_vision_frame_input_governance_audit_v0()

    return {
        "summary": summary,
        "matrix": matrix,
        "candidate": candidate,
        "audit": audit,
    }
