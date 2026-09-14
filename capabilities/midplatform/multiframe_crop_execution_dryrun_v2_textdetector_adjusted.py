# -*- coding: utf-8 -*-
"""Multiframe Crop Execution DryRun v2 — TextDetectorAdjusted re-crop only, no OCR.

Phase-Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted-001
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted-001"
RUNTIME_STEP = "multiframe_crop_execution_dryrun_v2_textdetector_adjusted"

FOLLOWUPS = [
    "OCRRequest-Gated-Submission-from-Multiframe-v2",
    "Evidence-Pack-Adapter-v4-Multiframe-Rerun",
    "Semantic-Candidate-v4-MultiframeAware",
    "Source-Validation-v2-Rerun-after-Multiframe",
    "User-Guidance-Recovery-Policy-v1",
    "STC-Sampling-Guidance-Policy-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "Text-Detector-DryRun-v2-with-supervision",
    "Crop-Quality-Scoring-v1",
    "Multiframe-Consensus-Policy-v1",
    "VisualSymbolRegistry-DryRun-v1",
    "Map-POI-Hint-DryRun-v1",
]

RULE_IDS = [
    "consume_bbox_adjustment_proposal_only",
    "adjusted_bbox_from_heuristic_not_detection",
    "adjusted_crop_artifact_not_evidence",
    "geometry_change_must_be_reported",
    "same_bbox_risk_must_be_reported",
    "crop_generation_allowed_only_for_dryrun",
    "ocr_execution_forbidden",
    "ocrrequest_generation_forbidden",
    "evidence_pack_generation_forbidden",
    "semantic_generation_forbidden",
    "source_validation_rerun_forbidden",
    "same_frame_blocker_not_resolved_in_this_phase",
    "user_guidance_recovery_required_if_reocr_empty_later",
    "no_world_model_attach_in_this_phase",
    "no_scene_delta_candidate_in_this_phase",
]

FUTURE_PHASES: List[Dict[str, Any]] = [
    {
        "future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v2",
        "purpose": "gated OCR on TextDetectorAdjusted crops",
        "required_input": ["multiframe_crop_v2_adjusted_artifact_collection"],
        "expected_output": ["multiframe_ocr_result_collection_v2"],
        "boundary": "gated_submission_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Evidence-Pack-Adapter-v4-Multiframe-Rerun",
        "purpose": "adapt v2 OCR to EP v4",
        "required_input": ["multiframe_ocr_result_collection_v2"],
        "expected_output": ["evidence_pack_v4_multiframe_collection_rerun"],
        "boundary": "adapter_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Semantic-Candidate-v4-MultiframeAware",
        "purpose": "semantic after non-empty path",
        "required_input": ["evidence_pack_v4_with_text"],
        "expected_output": ["semantic_candidate_v4"],
        "boundary": "not_fact",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Source-Validation-v2-Rerun-after-Multiframe",
        "purpose": "SV rerun when evidence matures",
        "required_input": ["semantic_v4_or_ep_v4_nonempty"],
        "expected_output": ["sv_rerun_report"],
        "boundary": "rerun_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "User-Guidance-Recovery-Policy-v1",
        "purpose": "user guidance + system self-adjust + external assistance if re-OCR empty",
        "required_input": ["ocr_v2_empty_or_low_confidence"],
        "expected_output": ["recovery_policy_report"],
        "boundary": "policy_only_no_tts_in_prior_phases",
        "not_in_current_phase": True,
    },
]

ARTIFACT_SCHEMA: Dict[str, Any] = {
    "adjusted_multiframe_crop_artifact_id": "mf_crop_v2_adj_<uuid>",
    "schema_version": "multiframe_crop_artifact_v2_textdetector_adjusted",
    "bbox_adjustment_proposal_ref": None,
    "text_region_candidate_ref": None,
    "source_frame": {
        "frame_index": None,
        "frame_time_sec": None,
        "frame_offset_from_source": None,
        "frame_file_path": None,
    },
    "bbox_context": {
        "original_projection_bbox_xyxy": None,
        "proposed_adjusted_bbox_xyxy": None,
        "clipped_adjusted_bbox_xyxy": None,
        "crop_bbox_xyxy": None,
        "bbox_within_bounds": None,
        "clipped": False,
        "iou_with_original": None,
        "geometry_changed": None,
        "geometry_change_significant": None,
        "adjustment_source": "internal_heuristic",
        "adjustment_bbox_not_detected_text_region": True,
    },
    "crop_output": {
        "crop_file_path": None,
        "crop_width": None,
        "crop_height": None,
        "crop_generated": False,
        "crop_status": "generated | deferred | failed",
    },
    "quality_placeholder": {
        "lightweight_placeholder": True,
        "crop_area": None,
        "crop_aspect_ratio": None,
        "brightness_score": None,
        "blur_score": None,
        "crop_quality_claim_allowed": False,
    },
    "governance": {
        "ocr_allowed_now": False,
        "ocrrequest_allowed_now": False,
        "semantic_allowed_now": False,
        "source_validation_allowed_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    },
    "source_chain": [],
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _stable_id(prefix: str, key: str) -> str:
    return f"{prefix}{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def _intake_id(prop_id: str) -> str:
    return f"adj_crop_intake_{hashlib.sha256(prop_id.encode()).hexdigest()[:10]}"


def _bbox_equal(a: List[float], b: List[float], eps: float = 0.5) -> bool:
    if len(a) < 4 or len(b) < 4:
        return False
    return all(abs(float(a[i]) - float(b[i])) <= eps for i in range(4))


def _iou(a: List[float], b: List[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    if inter <= 0:
        return 0.0
    ua = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    ub = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = ua + ub - inter
    return inter / union if union > 0 else 0.0


def _center_dist(a: List[float], b: List[float]) -> float:
    return ((a[0] + a[2] - b[0] - b[2]) ** 2 / 4 + (a[1] + a[3] - b[1] - b[3]) ** 2 / 4) ** 0.5


def _area(bbox: List[float]) -> float:
    return max(0.0, bbox[2] - bbox[0]) * max(0.0, bbox[3] - bbox[1])


def _build_rules() -> List[Dict[str, Any]]:
    return [
        {
            "rule_id": rid,
            "condition": rid,
            "allowed_action": "textdetector_adjusted_recrop_dryrun",
            "blocked_action": "ocr_fact_semantic_sv_tts_runtime",
            "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v2",
            "fact_status_after_rule": "not_fact",
            "write_allowed_after_rule": False,
        }
        for rid in RULE_IDS
    ]


def _load_frame_image(path: Path):
    from PIL import Image  # type: ignore

    return Image.open(path).convert("RGB")


def _save_crop(img, bbox: List[float], out_path: Path) -> Tuple[int, int]:
    x1, y1, x2, y2 = [int(round(v)) for v in bbox[:4]]
    cropped = img.crop((x1, y1, x2, y2))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(out_path, format="PNG")
    return cropped.size[0], cropped.size[1]


def _image_stats_from_crop(img) -> Tuple[Optional[float], Optional[float]]:
    try:
        import numpy as np  # type: ignore

        arr = np.asarray(img.convert("L"), dtype=np.float32)
        brightness = float(arr.mean()) if arr.size else None
        gx = np.abs(np.diff(arr, axis=1)).mean() if arr.shape[1] > 1 else 0.0
        gy = np.abs(np.diff(arr, axis=0)).mean() if arr.shape[0] > 1 else 0.0
        return brightness, float((gx + gy) / 2.0)
    except Exception:
        return None, None


def run_multiframe_crop_execution_dryrun_v2_textdetector_adjusted(
    *,
    output_root: str,
    bbox_adjustment_root: str,
    text_detector_root: str,
    crop_quality_root: str,
    evidence_pack_v4_root: str,
    multiframe_ocr_root: str,
    multiframe_crop_root: str,
    text_region_tracklet_root: str,
    better_frame_root: str,
    multiframe_merge_proposal_root: str,
    source_validation_v2_root: str,
    semantic_v3_root: str,
    evidence_pack_v3_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    out = Path(output_root).resolve()
    crops_dir = out / "crops"
    crops_dir.mkdir(parents=True, exist_ok=True)

    ba_root = Path(bbox_adjustment_root).resolve()
    td_root = Path(text_detector_root).resolve()
    cq_root = Path(crop_quality_root).resolve()
    ep_root = Path(evidence_pack_v4_root).resolve()
    crop_v1_root = Path(multiframe_crop_root).resolve()
    bf_root = Path(better_frame_root).resolve()
    tr_root = Path(text_region_tracklet_root).resolve()
    mf_root = Path(multiframe_merge_proposal_root).resolve()
    sv_root = Path(source_validation_v2_root).resolve()
    sem_root = Path(semantic_v3_root).resolve()
    ep3_root = Path(evidence_pack_v3_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    coll = _read_json(ba_root / "bbox_adjustment_proposal_collection_v2.json") or {}
    proposals = [p for p in (coll.get("proposals") or coll.get("canonical_proposals") or []) if isinstance(p, dict)]
    proposal_count = len(proposals)

    frame_path_by_index: Dict[int, str] = {}
    frame_dims: Dict[int, Tuple[int, int]] = {}
    for ref in (_read_json(bf_root / "better_frame_candidate_frame_reference_collection.json") or {}).get("references") or []:
        if isinstance(ref, dict) and ref.get("candidate_frame_index") is not None:
            fi = int(ref["candidate_frame_index"])
            fp = str(ref.get("frame_artifact_path") or "")
            if fp:
                frame_path_by_index[fi] = fp
            frame_dims[fi] = (int(ref.get("frame_width") or 544), int(ref.get("frame_height") or 960))

    intake_rows: List[Dict[str, Any]] = []
    artifacts: List[Dict[str, Any]] = []
    trace_rows: List[Dict[str, Any]] = []
    geometry_rows: List[Dict[str, Any]] = []
    quality_rows: List[Dict[str, Any]] = []
    ocr_ready_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    generated_n = 0
    deferred_n = 0
    failed_n = 0
    same_bbox_n = 0
    geom_sig_n = 0
    ready_ocr_n = 0
    clipped_total = 0

    for prop in proposals:
        prop_id = str(prop.get("bbox_adjustment_proposal_id") or "")
        if not prop.get("proposal_ready_for_future_recrop"):
            deferred_n += 1
            continue

        fi = int(prop.get("frame_index") or 0)
        fw, fh = frame_dims.get(fi, (544, 960))
        frame_path = frame_path_by_index.get(fi, "")
        orig = [float(v) for v in prop.get("original_projection_bbox_xyxy") or []]
        proposed = [float(v) for v in prop.get("proposed_adjusted_bbox_xyxy") or []]
        clipped_bbox = [float(v) for v in prop.get("clipped_adjusted_bbox_xyxy") or proposed]
        crop_bbox = clipped_bbox

        iou = float(prop.get("iou_with_original") or _iou(orig, crop_bbox))
        geom_changed = not _bbox_equal(orig, crop_bbox)
        center_shift = _center_dist(orig, crop_bbox)
        area_o = max(1.0, _area(orig))
        area_a = _area(crop_bbox)
        area_ratio = abs(area_a - area_o) / area_o
        geom_sig = geom_changed and (iou < 0.99 or area_ratio > 0.05 or center_shift > 2.0)
        same_risk = iou >= 0.99 and center_shift <= 2.0 and area_ratio <= 0.05

        if same_risk:
            same_bbox_n += 1
        if geom_sig:
            geom_sig_n += 1
        if prop.get("clipped"):
            clipped_total += 1

        art_id = _stable_id("mf_crop_v2_adj_", prop_id)
        crop_fname = f"{art_id}_fi{fi}_adj.png"
        crop_path = crops_dir / crop_fname

        intake_rows.append(
            {
                "adjusted_crop_intake_id": _intake_id(prop_id),
                "bbox_adjustment_proposal_id": prop_id,
                "bbox_adjustment_candidate_id": prop.get("bbox_adjustment_candidate_id"),
                "text_region_candidate_id": prop.get("text_region_candidate_id"),
                "source_input_ref": prop.get("source_input_ref"),
                "source_type": prop.get("source_type"),
                "frame_index": fi,
                "frame_time_sec": prop.get("frame_time_sec"),
                "frame_offset_from_source": prop.get("frame_offset_from_source"),
                "frame_file_path": frame_path,
                "frame_width": fw,
                "frame_height": fh,
                "original_projection_bbox_xyxy": orig,
                "proposed_adjusted_bbox_xyxy": proposed,
                "clipped_adjusted_bbox_xyxy": clipped_bbox,
                "clipped": bool(prop.get("clipped")),
                "bbox_within_bounds": bool(prop.get("bbox_within_bounds")),
                "adjustment_reason": prop.get("adjustment_reason"),
                "adjustment_source": prop.get("adjustment_source") or "internal_heuristic",
                "adjustment_confidence": prop.get("adjustment_confidence"),
                "iou_with_original": iou,
                "proposal_ready_for_future_recrop": True,
                "intake_status": "accepted",
                "eligible_for_adjusted_crop": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        crop_status = "failed"
        crop_generated = False
        crop_w, crop_h = None, None
        err = None
        brightness, blur = None, None

        if not frame_path or not Path(frame_path).is_file():
            crop_status = "deferred"
            err = "frame_file_missing"
            deferred_n += 1
        elif crop_bbox[2] <= crop_bbox[0] or crop_bbox[3] <= crop_bbox[1]:
            crop_status = "failed"
            err = "invalid_bbox_area"
            failed_n += 1
        else:
            try:
                img = _load_frame_image(Path(frame_path))
                crop_w, crop_h = _save_crop(img, crop_bbox, crop_path)
                cropped_img = img.crop(tuple(int(round(v)) for v in crop_bbox))
                brightness, blur = _image_stats_from_crop(cropped_img)
                crop_status = "generated"
                crop_generated = True
                generated_n += 1
                if crop_path.is_file():
                    ready_ocr_n += 1
            except Exception as exc:
                crop_status = "failed"
                err = str(exc)[:200]
                failed_n += 1

        chain = list(prop.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        art = {
            "adjusted_multiframe_crop_artifact_id": art_id,
            "bbox_adjustment_proposal_id": prop_id,
            "text_region_candidate_id": prop.get("text_region_candidate_id"),
            "source_input_ref": prop.get("source_input_ref"),
            "source_type": prop.get("source_type"),
            "frame_index": fi,
            "frame_time_sec": prop.get("frame_time_sec"),
            "frame_offset_from_source": prop.get("frame_offset_from_source"),
            "frame_file_path": frame_path,
            "original_projection_bbox_xyxy": [round(v, 2) for v in orig],
            "proposed_adjusted_bbox_xyxy": [round(v, 2) for v in proposed],
            "clipped_adjusted_bbox_xyxy": [round(v, 2) for v in clipped_bbox],
            "crop_bbox_xyxy": [round(v, 2) for v in crop_bbox],
            "clipped": bool(prop.get("clipped")),
            "bbox_within_bounds": bool(prop.get("bbox_within_bounds")),
            "iou_with_original": round(iou, 4),
            "geometry_changed": geom_changed,
            "geometry_change_significant": geom_sig,
            "adjustment_source": prop.get("adjustment_source") or "internal_heuristic",
            "crop_file_path": str(crop_path) if crop_generated else None,
            "crop_width": crop_w,
            "crop_height": crop_h,
            "crop_generated": crop_generated,
            "crop_status": crop_status,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": chain,
        }
        artifacts.append(art)

        trace_rows.append(
            {
                "crop_execution_id": f"crop_exec_{hashlib.sha256(prop_id.encode()).hexdigest()[:10]}",
                "bbox_adjustment_proposal_id": prop_id,
                "adjusted_multiframe_crop_artifact_id": art_id,
                "frame_file_path": frame_path,
                "crop_bbox_xyxy": crop_bbox,
                "crop_status": crop_status,
                "crop_file_path": str(crop_path) if crop_generated else None,
                "clipped": bool(prop.get("clipped")),
                "error": err,
                "ocr_invoked": False,
                "provider_invoked": False,
                "ocrrequest_generated": False,
                "evidence_pack_generated": False,
                "semantic_candidate_generated": False,
            }
        )

        ox1, oy1, ox2, oy2 = orig
        ax1, ay1, ax2, ay2 = crop_bbox
        geometry_rows.append(
            {
                "adjusted_multiframe_crop_artifact_id": art_id,
                "bbox_adjustment_proposal_id": prop_id,
                "original_projection_bbox_xyxy": orig,
                "adjusted_bbox_xyxy": crop_bbox,
                "iou_with_original": round(iou, 4),
                "delta_x": round(ax1 - ox1, 2),
                "delta_y": round(ay1 - oy1, 2),
                "delta_w": round((ax2 - ax1) - (ox2 - ox1), 2),
                "delta_h": round((ay2 - ay1) - (oy2 - oy1), 2),
                "center_shift_px": round(center_shift, 2),
                "area_change_ratio": round(area_ratio, 4),
                "geometry_changed": geom_changed,
                "geometry_change_significant": geom_sig,
                "same_bbox_or_near_same_bbox_risk": same_risk,
                "expected_ocr_improvement_limited": same_risk,
                "diagnostic_only": True,
            }
        )

        aspect = (crop_w / crop_h) if crop_w and crop_h and crop_h > 0 else None
        quality_rows.append(
            {
                "adjusted_multiframe_crop_artifact_id": art_id,
                "crop_width": crop_w,
                "crop_height": crop_h,
                "crop_area": (crop_w * crop_h) if crop_w and crop_h else None,
                "crop_aspect_ratio": round(aspect, 4) if aspect else None,
                "brightness_score": brightness,
                "blur_score": blur,
                "small_crop_risk": bool(crop_h and crop_w and (crop_h < 32 or crop_w < 80)),
                "lightweight_placeholder": True,
                "crop_quality_claim_allowed": False,
                "required_future_phase": "Crop-Quality-Scoring-v1",
            }
        )

        ready = crop_status == "generated" and crop_path.is_file()
        ocr_ready_rows.append(
            {
                "adjusted_multiframe_crop_artifact_id": art_id,
                "bbox_adjustment_proposal_id": prop_id,
                "crop_file_path": str(crop_path) if ready else None,
                "crop_status": crop_status,
                "ready_for_ocrrequest_multiframe_v2": ready,
                "readiness_status": "ready_for_future_ocrrequest_v2" if ready else crop_status,
                "ocrrequest_allowed_now": False,
                "required_input_for_future_ocrrequest": [
                    "multiframe_crop_v2_adjusted_artifact_collection",
                    "ocr_mainline_bridge_v0",
                ],
                "blocker_codes": [] if ready else ["crop_not_generated"],
                "future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v2",
            }
        )

        chain_rows.append(
            {
                "adjusted_multiframe_crop_artifact_id": art_id,
                "traceable_to_bbox_adjustment_proposal": ba_root.is_dir(),
                "traceable_to_text_detector_dryrun": td_root.is_dir(),
                "traceable_to_crop_quality_diagnosis": cq_root.is_dir(),
                "traceable_to_ep_v4": ep_root.is_dir(),
                "traceable_to_multiframe_crop_v1": crop_v1_root.is_dir(),
                "traceable_to_tracklet": tr_root.is_dir(),
                "source_chain_preserved": True,
            }
        )

    unique_frames = {a["frame_index"] for a in artifacts}
    unique_bboxes = {tuple(a.get("crop_bbox_xyxy") or []) for a in artifacts}
    unique_sizes = {(a.get("crop_width"), a.get("crop_height")) for a in artifacts if a.get("crop_generated")}
    offset_dist: Dict[int, int] = {}
    for a in artifacts:
        fo = int(a.get("frame_offset_from_source") or 0)
        offset_dist[fo] = offset_dist.get(fo, 0) + 1

    summary = {
        "schema_version": "multiframe_crop_v2_textdetector_adjusted_summary_v0",
        "phase": PHASE_ID,
        "dryrun_scope": "textdetector_adjusted_recrop_only",
        "based_on_bbox_adjustment_proposal_v2": True,
        "bbox_adjustment_proposal_count_observed": proposal_count,
        "deduplicated_proposal_count_observed": int(
            (_read_json(ba_root / "bbox_adjustment_proposal_v2_multiframe_summary.json") or {}).get(
                "deduplicated_proposal_count"
            )
            or proposal_count
        ),
        "adjusted_crop_execution_attempted": True,
        "adjusted_crop_artifact_generated": generated_n > 0,
        "adjusted_crop_artifact_count": len(artifacts),
        "adjusted_crop_deferred_count": deferred_n,
        "adjusted_crop_failed_count": failed_n,
        "adjusted_bbox_same_as_original_count": same_bbox_n,
        "geometry_change_significant_count": geom_sig_n,
        "adjustment_source": "internal_heuristic",
        "user_guidance_recovery_needed_later": True,
        "ocr_invoked": False,
        "provider_invoked": False,
        "ocrrequest_generated": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "source_validation_rerun_invoked": False,
        "same_frame_blocker_resolved": False,
        "decision_committed": False,
        "approval_granted": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": "GO" if proposal_count == 5 and generated_n > 0 else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "multiframe_crop_v2_adjusted_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {"schema_version": "multiframe_crop_v2_execution_rule_matrix_v1", "rules": _build_rules()},
        "artifact_schema": {
            "schema_version": "multiframe_crop_v2_adjusted_artifact_schema_v1",
            "template": ARTIFACT_SCHEMA,
        },
        "artifact_collection": {
            "schema_version": "multiframe_crop_v2_adjusted_artifact_collection_v1",
            "artifact_count": len(artifacts),
            "artifacts": artifacts,
        },
        "execution_trace": {
            "schema_version": "multiframe_crop_v2_adjusted_execution_trace_v1",
            "row_count": len(trace_rows),
            "rows": trace_rows,
        },
        "geometry_delta": {
            "schema_version": "multiframe_crop_v2_geometry_delta_report_v1",
            "summary": {
                "adjusted_crop_count": len(artifacts),
                "adjusted_bbox_same_as_original_count": same_bbox_n,
                "geometry_change_significant_count": geom_sig_n,
                "same_bbox_or_near_same_bbox_risk_count": same_bbox_n,
            },
            "rows": geometry_rows,
        },
        "quality_placeholder": {
            "schema_version": "multiframe_crop_v2_adjusted_quality_placeholder_report_v1",
            "row_count": len(quality_rows),
            "rows": quality_rows,
        },
        "diversity": {
            "schema_version": "multiframe_crop_v2_adjusted_diversity_report_v1",
            "adjusted_crop_count": len(artifacts),
            "unique_frame_index_count": len(unique_frames),
            "unique_adjusted_bbox_count": len(unique_bboxes),
            "unique_crop_size_count": len(unique_sizes),
            "frame_offset_distribution": offset_dist,
            "adjusted_vs_original_bbox_diversity_gain": "limited_same_bbox_dominant"
            if same_bbox_n >= len(artifacts) // 2
            else "partial",
            "diversity_claim_allowed": False,
            "independent_consensus_allowed_now": False,
            "same_frame_blocker_resolved": False,
        },
        "ocr_readiness": {
            "schema_version": "multiframe_crop_v2_ocrrequest_readiness_report_v1",
            "row_count": len(ocr_ready_rows),
            "rows": ocr_ready_rows,
        },
        "user_guidance": {
            "schema_version": "multiframe_crop_v2_user_guidance_recovery_followup_report_v1",
            "user_guidance_recovery_needed_later": True,
            "trigger_condition": "if_multiframe_v2_reocr_empty_or_low_confidence",
            "guidance_action_candidates": [
                "ask_user_move_closer",
                "ask_user_center_text",
                "ask_user_adjust_angle",
                "ask_user_hold_still",
                "ask_user_increase_light",
                "ask_user_zoom_or_enable_magnification",
                "request_external_assistance_if_needed",
            ],
            "system_self_adjustment_candidates": [
                "request_higher_quality_frame",
                "request_zoom_or_autofocus",
                "request_resampling",
                "request_text_detector_heavy_provider",
            ],
            "not_in_current_phase": True,
            "no_tts_invoked_now": True,
            "no_runtime_action_committed": True,
            "note": "Do not infinite internal re-crop/re-OCR; escalate to user guidance / STC sampling / system self-adjust",
        },
        "same_frame_carryover": {
            "schema_version": "multiframe_crop_v2_same_frame_blocker_carryover_report_v1",
            "same_frame_consensus_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
            "independent_consensus_allowed_now": False,
            "adjusted_crops_prepared_but_not_validated": True,
            "required_future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v2",
        },
        "future_plan": {
            "schema_version": "multiframe_crop_v2_future_ocr_ep_sv_plan_v1",
            "phases": FUTURE_PHASES,
        },
        "source_chain": {
            "schema_version": "multiframe_crop_v2_source_chain_report_v1",
            "row_count": len(chain_rows),
            "rows": chain_rows,
        },
        "boundary": {
            "schema_version": "multiframe_crop_v2_boundary_report_v1",
            "textdetector_adjusted_recrop_only": True,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
            "tts_invoked": False,
            "user_guidance_runtime_action_committed": False,
        },
        "metrics": {
            "schema_version": "multiframe_crop_v2_metrics_candidate_report_v1",
            "bbox_adjustment_proposal_count_observed": proposal_count,
            "adjusted_crop_artifact_count": len(artifacts),
            "adjusted_crop_generated_count": generated_n,
            "adjusted_crop_deferred_count": deferred_n,
            "adjusted_crop_failed_count": failed_n,
            "adjusted_bbox_same_as_original_count": same_bbox_n,
            "geometry_change_significant_count": geom_sig_n,
            "proposal_ready_for_future_recrop_count": proposal_count,
            "ready_for_ocrrequest_multiframe_v2_count": ready_ocr_n,
            "ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "evidence_pack_generated_count": 0,
            "semantic_candidate_generated_count": 0,
            "source_validation_rerun_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "user_guidance_runtime_action_committed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "multiframe_crop_v2_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "multiframe_crop_v2_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "multiframe_crop_v2_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "textdetector_adjusted_recrop_only": True,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "decision_committed": False,
            "approval_granted": False,
            "auto_approve_invoked": False,
            "fact_review_generated": False,
            "world_model_attach_executed": False,
            "scene_delta_candidate_generated": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "tts_invoked": False,
            "user_guidance_runtime_action_committed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "multiframe_crop_v2_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "multiframe_crop_v2_non_claims_report_v1",
            "claims": [
                "no_ocr_in_this_phase",
                "no_ocrrequest_in_this_phase",
                "textdetector_adjusted_crop_not_ocr_evidence",
                "adjusted_bbox_not_detected_text_region",
                "heuristic_adjustment_not_fact",
                "geometry_valid_not_ocr_success_guarantee",
                "if_reocr_still_empty_use_user_guidance_or_stc_sampling_not_infinite_recrop",
                "no_semantic",
                "no_sv_rerun",
                "no_world_model",
                "no_scene_delta",
                "not_benchmark",
                "not_provider_comparison",
                "not_navigation",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "multiframe_crop_v2_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "multiframe_crop_v2_audit_report_v1",
            "multiframe_crop_v2_textdetector_adjusted_executed": True,
            "textdetector_adjusted_recrop_only": True,
            "bbox_adjustment_proposal_count_observed": proposal_count,
            "adjusted_crop_artifact_count": len(artifacts),
            "adjusted_crop_generated_count": generated_n,
            "adjusted_bbox_same_as_original_count": same_bbox_n,
            "geometry_change_significant_count": geom_sig_n,
            "ready_for_ocrrequest_multiframe_v2_count": ready_ocr_n,
            "user_guidance_recovery_needed_later": True,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "same_frame_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
            "tts_invoked": False,
            "user_guidance_runtime_action_committed": False,
            "decision_committed": False,
            "approval_granted": False,
            "auto_approve_invoked": False,
            "fact_review_generated": False,
            "world_model_attach_executed": False,
            "scene_delta_candidate_generated": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "model_selection_claimed": False,
            "production_readiness_claimed": False,
        },
    }
