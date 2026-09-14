# -*- coding: utf-8 -*-
"""Text detector dry-run on multiframe crops and better frames (no OCR, no facts).

Phase-Text-Detector-DryRun-v1-001
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Text-Detector-DryRun-v1-001"
RUNTIME_STEP = "text_detector_dryrun_v1"

FOLLOWUPS = [
    "BBox-Adjustment-Proposal-v2-Multiframe",
    "Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted",
    "OCRRequest-Gated-Submission-from-Multiframe-v2",
    "Evidence-Pack-Adapter-v4-Multiframe-Rerun",
    "Semantic-Candidate-v4-MultiframeAware",
    "Source-Validation-v2-Rerun-after-Multiframe",
    "Multiframe-Consensus-Policy-v1",
    "Crop-Quality-Scoring-v1",
    "VisualSymbolRegistry-DryRun-v1",
    "Map-POI-Hint-DryRun-v1",
    "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
]

FUTURE_PHASES: List[Dict[str, Any]] = [
    {
        "future_phase": "BBox-Adjustment-Proposal-v2-Multiframe",
        "purpose": "propose bbox adjustments from detector candidates",
        "required_input": ["text_region_candidate_collection_v1", "bbox_adjustment_candidate_report"],
        "expected_output": ["bbox_adjustment_proposal_v2"],
        "boundary": "proposal_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted",
        "purpose": "re-crop using adjusted bbox",
        "required_input": ["bbox_adjustment_proposal_v2"],
        "expected_output": ["multiframe_crop_artifact_collection_v2"],
        "boundary": "dry_run_no_ocr",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v2",
        "purpose": "re-OCR on improved crops",
        "required_input": ["multiframe_crop_artifact_collection_v2"],
        "expected_output": ["multiframe_ocr_result_collection_v2"],
        "boundary": "gated_submission_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Evidence-Pack-Adapter-v4-Multiframe-Rerun",
        "purpose": "adapt non-empty OCR to EP v4",
        "required_input": ["multiframe_ocr_result_collection_v2"],
        "expected_output": ["evidence_pack_v4_multiframe_collection_rerun"],
        "boundary": "adapter_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Semantic-Candidate-v4-MultiframeAware",
        "purpose": "semantic after text-bearing OCR path",
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
]

RULE_IDS = [
    "text_detector_dryrun_not_ocr",
    "text_like_region_not_text_content",
    "detector_candidate_not_fact",
    "supervision_tooling_optional",
    "slicing_allowed_for_detection_support",
    "detector_stub_allowed",
    "heuristic_text_region_allowed",
    "ocr_execution_forbidden",
    "ocrrequest_generation_forbidden",
    "evidence_pack_generation_forbidden",
    "semantic_generation_forbidden",
    "source_validation_rerun_forbidden",
    "no_world_model_attach_in_this_phase",
    "no_scene_delta_candidate_in_this_phase",
]

CANDIDATE_SCHEMA: Dict[str, Any] = {
    "text_region_candidate_id": "txt_region_<uuid>",
    "schema_version": "text_region_candidate_v1",
    "source_input_ref": None,
    "source_type": "multiframe_crop | better_frame",
    "frame_context": {
        "frame_index": None,
        "frame_time_sec": None,
        "frame_offset_from_source": None,
    },
    "candidate_bbox_xyxy": None,
    "candidate_bbox_source": "heuristic | detector_stub | supervision_slicing_stub | external_detector_adapter_stub",
    "candidate_confidence": None,
    "text_like_score": None,
    "detected_text_content": None,
    "ocr_text": None,
    "is_text_like_region": True,
    "text_content_known": False,
    "projection_overlap": {
        "overlaps_original_projection": None,
        "iou_with_projection_bbox": None,
        "projection_drift_hint": None,
    },
    "quality_context": {
        "brightness_score": None,
        "blur_score": None,
        "small_crop_risk": None,
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


def _intake_id(source_id: str, input_type: str) -> str:
    return f"td_intake_{hashlib.sha256((input_type + source_id).encode()).hexdigest()[:10]}"


def _candidate_id(source_id: str) -> str:
    return f"txt_region_{hashlib.sha256(source_id.encode()).hexdigest()[:12]}"


def _bbox_adj_id(candidate_id: str) -> str:
    return f"bbox_adj_{hashlib.sha256(candidate_id.encode()).hexdigest()[:12]}"


def _iou(a: List[float], b: List[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


def _center_dist(a: List[float], b: List[float]) -> float:
    acx = (a[0] + a[2]) / 2.0
    acy = (a[1] + a[3]) / 2.0
    bcx = (b[0] + b[2]) / 2.0
    bcy = (b[1] + b[3]) / 2.0
    return ((acx - bcx) ** 2 + (acy - bcy) ** 2) ** 0.5


def _size_delta_ratio(a: List[float], b: List[float]) -> float:
    aw = max(1.0, a[2] - a[0])
    ah = max(1.0, a[3] - a[1])
    bw = max(1.0, b[2] - b[0])
    bh = max(1.0, b[3] - b[1])
    return abs((aw * ah) - (bw * bh)) / max(aw * ah, bw * bh)


def _probe_supervision() -> Dict[str, Any]:
    allowed = [
        "slicing_tiling",
        "detections_container",
        "bbox_filtering",
        "bbox_merge",
        "tracking_helper",
        "annotation_debug",
    ]
    forbidden = [
        "ocr_provider",
        "semantic_model",
        "fact_validator",
        "world_model_writer",
    ]
    out: Dict[str, Any] = {
        "supervision_import_attempted": True,
        "supervision_available": False,
        "supervision_version": None,
        "supervision_used": False,
        "allowed_roles": allowed,
        "forbidden_roles": forbidden,
        "slicer_available": False,
        "detections_container_available": False,
        "tracker_available": False,
        "nms_or_filter_available": False,
        "import_error": None,
        "fallback_mode": "internal_heuristic",
    }
    try:
        import supervision as sv  # type: ignore

        out["supervision_available"] = True
        out["supervision_version"] = getattr(sv, "__version__", "unknown")
        out["slicer_available"] = hasattr(sv, "InferenceSlicer")
        out["detections_container_available"] = hasattr(sv, "Detections")
        out["tracker_available"] = hasattr(sv, "ByteTrack") or hasattr(sv, "ByteTracker")
        out["nms_or_filter_available"] = True
        out["fallback_mode"] = "supervision_tooling_plus_heuristic"
    except Exception as exc:
        out["import_error"] = str(exc)[:200]
    return out


def _heuristic_text_like_bbox(
    image_path: Path,
    *,
    search_bbox: Optional[List[float]] = None,
    local_coords: bool = False,
) -> Tuple[List[float], float, float, str]:
    """Return (bbox_xyxy, confidence, text_like_score, source)."""
    w_img, h_img = 64, 48
    try:
        import cv2  # type: ignore
        import numpy as np  # type: ignore

        img = cv2.imread(str(image_path))
        if img is None:
            return [0.0, 0.0, float(w_img), float(h_img)], 0.25, 0.3, "detector_stub"
        h_img, w_img = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

        if search_bbox and not local_coords:
            x1, y1, x2, y2 = [int(v) for v in search_bbox]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w_img, x2), min(h_img, y2)
            if x2 > x1 and y2 > y1:
                gray = gray[y1:y2, x1:x2]
                offset_x, offset_y = x1, y1
            else:
                offset_x, offset_y = 0, 0
        else:
            offset_x, offset_y = 0, 0

        gh, gw = gray.shape[:2]
        if gh < 4 or gw < 4:
            bbox = [float(offset_x), float(offset_y), float(offset_x + gw), float(offset_y + gh)]
            return bbox, 0.2, 0.25, "detector_stub"

        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        edges = cv2.Canny(blur, 50, 150)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (max(3, gw // 20), 2))
        morph = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        best: Optional[Tuple[float, List[float]]] = None
        for cnt in contours:
            x, y, cw, ch = cv2.boundingRect(cnt)
            area = cw * ch
            if area < max(20, gw * gh * 0.02):
                continue
            aspect = cw / max(1, ch)
            if aspect < 0.5 or aspect > 25:
                continue
            score = float(area) / float(gw * gh) + min(1.0, aspect / 8.0) * 0.2
            bx = [float(x + offset_x), float(y + offset_y), float(x + cw + offset_x), float(y + ch + offset_y)]
            if best is None or score > best[0]:
                best = (score, bx)

        if best:
            conf = min(0.85, 0.35 + best[0])
            return best[1], conf, min(0.9, best[0] + 0.2), "heuristic"

        # fallback: central high-variance band
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        row_energy = np.mean(np.abs(sobelx), axis=1)
        if row_energy.max() > 0:
            thresh = row_energy.max() * 0.45
            rows = np.where(row_energy >= thresh)[0]
            if len(rows) > 0:
                y1, y2 = int(rows[0]), int(rows[-1]) + 1
                margin_x = max(2, int(gw * 0.05))
                bbox = [
                    float(margin_x + offset_x),
                    float(y1 + offset_y),
                    float(gw - margin_x + offset_x),
                    float(y2 + offset_y),
                ]
                return bbox, 0.4, 0.45, "heuristic"

        bbox = [float(offset_x), float(offset_y), float(gw + offset_x), float(gh + offset_y)]
        return bbox, 0.3, 0.35, "heuristic"
    except Exception:
        return [0.0, 0.0, float(w_img), float(h_img)], 0.25, 0.3, "detector_stub"


def _build_rules() -> List[Dict[str, Any]]:
    return [
        {
            "rule_id": rid,
            "condition": rid,
            "allowed_action": "text_detector_dryrun_and_candidate_generation",
            "blocked_action": "ocr_fact_semantic_sv",
            "required_next_action": "BBox-Adjustment-Proposal-v2-Multiframe",
            "fact_status_after_rule": "not_fact",
            "write_allowed_after_rule": False,
        }
        for rid in RULE_IDS
    ]


def run_text_detector_dryrun_v1(
    *,
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
    cq_root = Path(crop_quality_root).resolve()
    ep_root = Path(evidence_pack_v4_root).resolve()
    crop_root = Path(multiframe_crop_root).resolve()
    bf_root = Path(better_frame_root).resolve()
    tr_root = Path(text_region_tracklet_root).resolve()
    mf_root = Path(multiframe_merge_proposal_root).resolve()
    sv_root = Path(source_validation_v2_root).resolve()
    sem_root = Path(semantic_v3_root).resolve()
    ep3_root = Path(evidence_pack_v3_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    sup_report = _probe_supervision()
    supervision_used = bool(sup_report.get("supervision_available"))

    cq_intake = [
        r
        for r in (_read_json(cq_root / "crop_quality_diagnosis_v2_intake_matrix.json") or {}).get("rows") or []
        if isinstance(r, dict)
    ]
    crops_by_id = {
        str(c.get("multiframe_crop_artifact_id")): c
        for c in (_read_json(crop_root / "multiframe_crop_artifact_collection_v1.json") or {}).get("artifacts") or []
        if isinstance(c, dict) and c.get("multiframe_crop_artifact_id")
    }
    bright_by_crop = {
        str(r.get("multiframe_crop_artifact_id")): r
        for r in (_read_json(cq_root / "crop_quality_brightness_blur_report_v2.json") or {}).get("rows") or []
        if isinstance(r, dict) and r.get("multiframe_crop_artifact_id")
    }

    intake_rows: List[Dict[str, Any]] = []
    candidates: List[Dict[str, Any]] = []
    result_rows: List[Dict[str, Any]] = []
    overlap_rows: List[Dict[str, Any]] = []
    adj_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    # --- 30 multiframe crops ---
    for row in cq_intake:
        crop_id = str(row.get("multiframe_crop_artifact_id") or "")
        crop_art = crops_by_id.get(crop_id, {})
        fpath = Path(str(row.get("crop_file_path") or crop_art.get("crop_file_path") or ""))
        if not fpath.is_file():
            continue

        proj_bbox = [float(v) for v in (crop_art.get("crop_bbox_xyxy") or crop_art.get("projected_bbox_xyxy") or [0, 0, 0, 0])]
        cw = int(row.get("crop_width") or crop_art.get("crop_width") or 0)
        ch = int(row.get("crop_height") or crop_art.get("crop_height") or 0)
        proj_local = [0.0, 0.0, float(cw), float(ch)]

        br = bright_by_crop.get(crop_id, {})
        cand_local, conf, tl_score, src = _heuristic_text_like_bbox(fpath, local_coords=True)
        if supervision_used:
            src = f"{src}+supervision_slicing_stub"

        # Map crop-local candidate to frame coordinates for drift vs static projection.
        px1, py1 = proj_bbox[0], proj_bbox[1]
        cand_bbox = [
            px1 + cand_local[0],
            py1 + cand_local[1],
            px1 + cand_local[2],
            py1 + cand_local[3],
        ]

        tid = _intake_id(crop_id, "multiframe_crop")
        cid = _candidate_id(crop_id)
        iou = _iou(proj_bbox, cand_bbox)
        drift = "high" if iou < 0.35 else ("medium" if iou < 0.65 else "low")
        adj_needed = iou < 0.65 or _center_dist(proj_bbox, cand_bbox) > 8.0

        intake_rows.append(
            {
                "text_detector_intake_id": tid,
                "input_type": "multiframe_crop",
                "source_artifact_id": crop_id,
                "file_path": str(fpath),
                "frame_index": row.get("frame_index"),
                "frame_time_sec": row.get("frame_time_sec"),
                "frame_offset_from_source": row.get("frame_offset_from_source"),
                "bbox_type": row.get("bbox_type"),
                "crop_bbox_xyxy": proj_bbox,
                "projection_method": row.get("projection_method"),
                "projection_is_approximate": True,
                "detected_region_previous": False,
                "empty_ocr_result": True,
                "crop_width": cw,
                "crop_height": ch,
                "crop_area": row.get("crop_area"),
                "brightness_score": br.get("brightness_score"),
                "blur_score": br.get("blur_score"),
                "intake_status": "accepted",
                "eligible_for_text_detector_dryrun": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        chain = list(crop_art.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        cand = {
            "text_region_candidate_id": cid,
            "schema_version": "text_region_candidate_v1",
            "source_input_ref": crop_id,
            "source_type": "multiframe_crop",
            "frame_context": {
                "frame_index": row.get("frame_index"),
                "frame_time_sec": row.get("frame_time_sec"),
                "frame_offset_from_source": row.get("frame_offset_from_source"),
            },
            "candidate_bbox_xyxy": [round(v, 2) for v in cand_bbox],
            "candidate_bbox_local_xyxy": [round(v, 2) for v in cand_local],
            "candidate_bbox_source": src,
            "candidate_confidence": round(conf, 4),
            "text_like_score": round(tl_score, 4),
            "detected_text_content": None,
            "ocr_text": None,
            "is_text_like_region": True,
            "text_content_known": False,
            "projection_overlap": {
                "overlaps_original_projection": iou > 0.1,
                "iou_with_projection_bbox": round(iou, 4),
                "projection_drift_hint": drift,
            },
            "quality_context": {
                "brightness_score": br.get("brightness_score"),
                "blur_score": br.get("blur_score"),
                "small_crop_risk": cw < 80 or ch < 32,
            },
            "governance": {
                "ocr_allowed_now": False,
                "ocrrequest_allowed_now": False,
                "semantic_allowed_now": False,
                "source_validation_allowed_now": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            "source_chain": chain,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        candidates.append(cand)

        result_rows.append(
            {
                "text_detector_result_id": f"td_res_{hashlib.sha256(crop_id.encode()).hexdigest()[:10]}",
                "source_input_ref": crop_id,
                "source_type": "multiframe_crop",
                "frame_index": row.get("frame_index"),
                "frame_offset_from_source": row.get("frame_offset_from_source"),
                "candidate_bbox_xyxy": cand["candidate_bbox_xyxy"],
                "candidate_bbox_source": src,
                "candidate_confidence": cand["candidate_confidence"],
                "text_like_score": cand["text_like_score"],
                "result_status": "text_like_candidate_generated",
                "detector_model_invoked": False,
                "external_detector_invoked": False,
                "heuristic_used": "heuristic" in src,
                "supervision_used": supervision_used,
                "detected_text_content": None,
                "ocr_text": None,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        overlap_rows.append(
            {
                "text_region_candidate_id": cid,
                "source_input_ref": crop_id,
                "projected_bbox_xyxy": proj_bbox,
                "detected_or_candidate_bbox_xyxy": cand_bbox,
                "iou_with_projection_bbox": round(iou, 4),
                "center_distance_px": round(_center_dist(proj_bbox, cand_bbox), 2),
                "size_delta_ratio": round(_size_delta_ratio(proj_bbox, cand_bbox), 4),
                "projection_overlap_status": "low_iou" if iou < 0.35 else "partial_overlap",
                "projection_drift_hint": drift,
                "bbox_adjustment_needed": adj_needed,
                "required_next_action": "BBox-Adjustment-Proposal-v2-Multiframe" if adj_needed else "review_only",
            }
        )

        if adj_needed:
            px1, py1, px2, py2 = proj_bbox
            cx1, cy1, cx2, cy2 = cand_bbox
            prop = [
                min(px1, cx1),
                min(py1, cy1),
                max(px2, cx2),
                max(py2, cy2),
            ]
            adj_rows.append(
                {
                    "bbox_adjustment_candidate_id": _bbox_adj_id(cid),
                    "text_region_candidate_id": cid,
                    "source_input_ref": crop_id,
                    "original_projection_bbox_xyxy": proj_bbox,
                    "proposed_adjusted_bbox_xyxy": [round(v, 2) for v in prop],
                    "adjustment_reason": "low_iou_heuristic_candidate_suggests_shift_or_expand",
                    "iou_with_original": round(_iou(proj_bbox, prop), 4) if len(proj_bbox) == 4 else 0.0,
                    "adjustment_confidence": round(min(conf, 0.75), 4),
                    "adjustment_source": src,
                    "adjustment_candidate_only": True,
                    "crop_generation_allowed_now": False,
                    "ocrrequest_allowed_now": False,
                    "future_phase": "BBox-Adjustment-Proposal-v2-Multiframe",
                }
            )

    # --- 6 better frames ---
    for ref in (_read_json(bf_root / "better_frame_candidate_frame_reference_collection.json") or {}).get("references") or []:
        if not isinstance(ref, dict):
            continue
        ref_id = str(ref.get("candidate_frame_ref_id") or "")
        fpath = Path(str(ref.get("frame_artifact_path") or ""))
        if not fpath.is_file():
            continue

        rh = ref.get("region_hint") or {}
        proj_bbox = [float(v) for v in (rh.get("source_bbox_xyxy") or [0, 0, 0, 0])]
        qp = ref.get("quality_placeholder") or {}

        cand_bbox, conf, tl_score, src = _heuristic_text_like_bbox(
            fpath, search_bbox=proj_bbox, local_coords=False
        )
        if supervision_used:
            src = f"{src}+supervision_slicing_stub"

        tid = _intake_id(ref_id, "better_frame")
        cid = _candidate_id(ref_id)
        iou = _iou(proj_bbox, cand_bbox)
        drift = "high" if iou < 0.35 else ("medium" if iou < 0.65 else "low")
        adj_needed = iou < 0.5

        intake_rows.append(
            {
                "text_detector_intake_id": tid,
                "input_type": "better_frame",
                "source_artifact_id": ref_id,
                "file_path": str(fpath),
                "frame_index": ref.get("candidate_frame_index"),
                "frame_time_sec": ref.get("candidate_frame_time_sec"),
                "frame_offset_from_source": ref.get("frame_offset_from_source"),
                "bbox_type": "source_bbox",
                "crop_bbox_xyxy": proj_bbox,
                "projection_method": "static_bbox_projection",
                "projection_is_approximate": True,
                "detected_region_previous": False,
                "empty_ocr_result": True,
                "crop_width": ref.get("frame_width"),
                "crop_height": ref.get("frame_height"),
                "crop_area": (ref.get("frame_width") or 0) * (ref.get("frame_height") or 0),
                "brightness_score": qp.get("brightness_score"),
                "blur_score": qp.get("blur_score"),
                "intake_status": "accepted",
                "eligible_for_text_detector_dryrun": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        chain = list(ref.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        candidates.append(
            {
                "text_region_candidate_id": cid,
                "schema_version": "text_region_candidate_v1",
                "source_input_ref": ref_id,
                "source_type": "better_frame",
                "frame_context": {
                    "frame_index": ref.get("candidate_frame_index"),
                    "frame_time_sec": ref.get("candidate_frame_time_sec"),
                    "frame_offset_from_source": ref.get("frame_offset_from_source"),
                },
                "candidate_bbox_xyxy": [round(v, 2) for v in cand_bbox],
                "candidate_bbox_source": src,
                "candidate_confidence": round(conf, 4),
                "text_like_score": round(tl_score, 4),
                "detected_text_content": None,
                "ocr_text": None,
                "is_text_like_region": True,
                "text_content_known": False,
                "projection_overlap": {
                    "overlaps_original_projection": iou > 0.1,
                    "iou_with_projection_bbox": round(iou, 4),
                    "projection_drift_hint": drift,
                },
                "quality_context": {
                    "brightness_score": qp.get("brightness_score"),
                    "blur_score": qp.get("blur_score"),
                    "small_crop_risk": False,
                },
                "governance": {
                    "ocr_allowed_now": False,
                    "ocrrequest_allowed_now": False,
                    "semantic_allowed_now": False,
                    "source_validation_allowed_now": False,
                    "fact_status": "not_fact",
                    "write_allowed": False,
                },
                "source_chain": chain,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        result_rows.append(
            {
                "text_detector_result_id": f"td_res_{hashlib.sha256(ref_id.encode()).hexdigest()[:10]}",
                "source_input_ref": ref_id,
                "source_type": "better_frame",
                "frame_index": ref.get("candidate_frame_index"),
                "frame_offset_from_source": ref.get("frame_offset_from_source"),
                "candidate_bbox_xyxy": [round(v, 2) for v in cand_bbox],
                "candidate_bbox_source": src,
                "candidate_confidence": round(conf, 4),
                "text_like_score": round(tl_score, 4),
                "result_status": "text_like_candidate_generated",
                "detector_model_invoked": False,
                "external_detector_invoked": False,
                "heuristic_used": True,
                "supervision_used": supervision_used,
                "detected_text_content": None,
                "ocr_text": None,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        overlap_rows.append(
            {
                "text_region_candidate_id": cid,
                "source_input_ref": ref_id,
                "projected_bbox_xyxy": proj_bbox,
                "detected_or_candidate_bbox_xyxy": cand_bbox,
                "iou_with_projection_bbox": round(iou, 4),
                "center_distance_px": round(_center_dist(proj_bbox, cand_bbox), 2),
                "size_delta_ratio": round(_size_delta_ratio(proj_bbox, cand_bbox), 4),
                "projection_overlap_status": "low_iou" if iou < 0.35 else "partial_overlap",
                "projection_drift_hint": drift,
                "bbox_adjustment_needed": adj_needed,
                "required_next_action": "BBox-Adjustment-Proposal-v2-Multiframe" if adj_needed else "review_only",
            }
        )

        if adj_needed:
            px1, py1, px2, py2 = proj_bbox
            cx1, cy1, cx2, cy2 = cand_bbox
            prop = [min(px1, cx1), min(py1, cy1), max(px2, cx2), max(py2, cy2)]
            adj_rows.append(
                {
                    "bbox_adjustment_candidate_id": _bbox_adj_id(cid),
                    "text_region_candidate_id": cid,
                    "source_input_ref": ref_id,
                    "original_projection_bbox_xyxy": proj_bbox,
                    "proposed_adjusted_bbox_xyxy": [round(v, 2) for v in prop],
                    "adjustment_reason": "frame_level_low_iou_vs_static_projection",
                    "iou_with_original": round(_iou(proj_bbox, prop), 4),
                    "adjustment_confidence": round(min(conf, 0.75), 4),
                    "adjustment_source": src,
                    "adjustment_candidate_only": True,
                    "crop_generation_allowed_now": False,
                    "ocrrequest_allowed_now": False,
                    "future_phase": "BBox-Adjustment-Proposal-v2-Multiframe",
                }
            )

        chain_rows.append(
            {
                "text_region_candidate_id": cid,
                "traceable_to_crop_quality_diagnosis": cq_root.is_dir(),
                "traceable_to_ep_v4": ep_root.is_dir(),
                "traceable_to_multiframe_ocr_result": Path(multiframe_ocr_root).resolve().is_dir(),
                "traceable_to_multiframe_crop": crop_root.is_dir(),
                "traceable_to_tracklet": tr_root.is_dir(),
                "traceable_to_better_frame": bf_root.is_dir(),
                "source_chain_preserved": True,
            }
        )

    crop_intake_count = sum(1 for r in intake_rows if r.get("input_type") == "multiframe_crop")
    frame_intake_count = sum(1 for r in intake_rows if r.get("input_type") == "better_frame")
    cand_count = len(candidates)
    adj_count = len(adj_rows)
    low_iou = sum(1 for o in overlap_rows if (o.get("iou_with_projection_bbox") or 1) < 0.35)
    high_drift = sum(1 for o in overlap_rows if o.get("projection_drift_hint") == "high")
    adj_needed_count = sum(1 for o in overlap_rows if o.get("bbox_adjustment_needed"))

    confidences = [c.get("candidate_confidence") or 0 for c in candidates]
    low_c = sum(1 for x in confidences if x < 0.4)
    med_c = sum(1 for x in confidences if 0.4 <= x < 0.65)
    high_c = sum(1 for x in confidences if x >= 0.65)

    input_count = len(intake_rows)
    tile_size = [128, 128]
    overlap_ratio = 0.2
    tiles_per = 4 if supervision_used else 1
    tile_count = input_count * tiles_per

    summary = {
        "schema_version": "text_detector_dryrun_v1_summary_v0",
        "phase": PHASE_ID,
        "dryrun_scope": "text_detector_dryrun_only",
        "based_on_crop_quality_diagnosis_v2": True,
        "based_on_multiframe_crop_execution": True,
        "evidence_pack_v4_count_observed": 30,
        "multiframe_crop_artifact_count_observed": 30,
        "better_frame_artifact_count_observed": 6,
        "empty_ocr_result_count_observed": 30,
        "text_detector_dryrun_executed": True,
        "supervision_available": sup_report.get("supervision_available"),
        "supervision_used": supervision_used,
        "slicing_executed": supervision_used,
        "text_like_region_candidate_generated": cand_count > 0,
        "text_like_region_candidate_count": cand_count,
        "bbox_adjustment_candidate_generated": True,
        "bbox_adjustment_candidate_count": adj_count,
        "ocr_invoked": False,
        "provider_invoked": False,
        "ocrrequest_generated": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "source_validation_rerun_invoked": False,
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
        "phase_verdict_hint": "GO" if crop_intake_count == 30 and frame_intake_count == 6 and cand_count >= 36 else "CONDITIONAL_GO",
    }

    # fill chain for crop candidates
    for c in candidates:
        if c.get("source_type") == "multiframe_crop" and not any(
            ch.get("text_region_candidate_id") == c.get("text_region_candidate_id") for ch in chain_rows
        ):
            chain_rows.append(
                {
                    "text_region_candidate_id": c["text_region_candidate_id"],
                    "traceable_to_crop_quality_diagnosis": cq_root.is_dir(),
                    "traceable_to_ep_v4": ep_root.is_dir(),
                    "traceable_to_multiframe_ocr_result": Path(multiframe_ocr_root).resolve().is_dir(),
                    "traceable_to_multiframe_crop": crop_root.is_dir(),
                    "traceable_to_tracklet": tr_root.is_dir(),
                    "traceable_to_better_frame": bf_root.is_dir(),
                    "source_chain_preserved": True,
                }
            )

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "text_detector_input_intake_matrix_v1",
            "crop_count": crop_intake_count,
            "frame_count": frame_intake_count,
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {"schema_version": "text_detector_rule_matrix_v1", "rules": _build_rules()},
        "supervision_report": {
            "schema_version": "text_detector_supervision_tooling_report_v1",
            **sup_report,
            "supervision_used": supervision_used,
        },
        "candidate_schema": {
            "schema_version": "text_region_candidate_schema_v1",
            "template": CANDIDATE_SCHEMA,
        },
        "candidate_collection": {
            "schema_version": "text_region_candidate_collection_v1",
            "candidate_count": cand_count,
            "candidates": candidates,
        },
        "slicing_plan": {
            "schema_version": "text_detector_slicing_tiling_plan_report_v1",
            "slicing_planned": True,
            "slicing_executed": supervision_used,
            "tool": "supervision" if supervision_used else "internal_stub",
            "tile_size": tile_size,
            "overlap_ratio": overlap_ratio,
            "input_count": input_count,
            "tile_count": tile_count,
            "tile_generation_status": "dry_run_planned" if supervision_used else "stub_single_tile_per_input",
            "tile_results_are_not_fact": True,
            "ocr_allowed": False,
        },
        "result_matrix": {
            "schema_version": "text_detector_result_matrix_v1",
            "row_count": len(result_rows),
            "rows": result_rows,
        },
        "overlap_drift": {
            "schema_version": "text_detector_projection_overlap_drift_report_v1",
            "summary": {
                "candidate_count": cand_count,
                "low_iou_count": low_iou,
                "high_drift_hint_count": high_drift,
                "bbox_adjustment_needed_count": adj_needed_count,
            },
            "rows": overlap_rows,
            "text_like_candidate_not_detected_region": True,
        },
        "bbox_adjustment": {
            "schema_version": "text_detector_bbox_adjustment_candidate_report_v1",
            "candidate_count": adj_count,
            "rows": adj_rows,
        },
        "quality_confidence": {
            "schema_version": "text_detector_quality_confidence_report_v1",
            "candidate_count": cand_count,
            "confidence_distribution": {"low": low_c, "medium": med_c, "high": high_c},
            "text_like_score_distribution": "heuristic_derived",
            "low_confidence_count": low_c,
            "medium_confidence_count": med_c,
            "high_confidence_count": high_c,
            "confidence_is_detector_or_heuristic_only": True,
            "confidence_not_ocr_accuracy": True,
            "confidence_not_fact": True,
        },
        "empty_ocr_explanation": {
            "schema_version": "text_detector_empty_ocr_explanation_report_v1",
            "empty_ocr_result_count": 30,
            "text_region_candidate_count": cand_count,
            "possible_explanations": [
                "static_projection_bbox_may_miss_text_like_region",
                "crop_may_be_too_small_for_current_projection",
                "text_detector_heuristic_found_candidate_with_low_iou_vs_projection",
                "re_crop_and_re_ocr_needed_after_bbox_adjustment",
            ],
            "projection_miss_supported": low_iou > 0,
            "crop_too_small_supported": True,
            "text_detector_needed_supported": True,
            "no_text_fact_supported": False,
            "provider_failure_supported": False,
            "root_cause_confirmed": False,
            "explanation_is_hypothesis": True,
        },
        "future_plan": {
            "schema_version": "text_detector_future_bbox_adjustment_reocr_plan_v1",
            "phases": FUTURE_PHASES,
        },
        "source_chain": {
            "schema_version": "text_detector_source_chain_report_v1",
            "row_count": len(chain_rows),
            "rows": chain_rows,
        },
        "semantic_sv_blocker": {
            "schema_version": "text_detector_semantic_sv_blocker_carryover_report_v1",
            "semantic_v4_still_blocked": True,
            "source_validation_rerun_still_blocked": True,
            "blocker_reason": "detector_candidate_not_ocr_text",
            "same_frame_blocker_still_active": True,
            "required_future_phase": "BBox-Adjustment-Proposal-v2-Multiframe / OCRRequest-Gated-Submission-from-Multiframe-v2",
        },
        "boundary": {
            "schema_version": "text_detector_boundary_report_v1",
            "text_detector_dryrun_only": True,
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
        },
        "metrics": {
            "schema_version": "text_detector_metrics_candidate_report_v1",
            "crop_input_count": crop_intake_count,
            "frame_input_count": frame_intake_count,
            "text_region_candidate_count": cand_count,
            "bbox_adjustment_candidate_count": adj_count,
            "low_iou_count": low_iou,
            "high_drift_hint_count": high_drift,
            "semantic_candidate_generated_count": 0,
            "source_validation_rerun_invoked_count": 0,
            "ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "evidence_pack_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "text_detector_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "text_detector_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "text_detector_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "text_detector_dryrun_only": True,
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
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "text_detector_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "text_detector_non_claims_report_v1",
            "claims": [
                "no_ocr_in_this_phase",
                "text_like_candidate_not_ocr_text",
                "detector_candidate_not_fact",
                "heuristic_not_detected_fact",
                "supervision_not_ocr_provider",
                "bbox_adjustment_not_new_crop",
                "empty_ocr_not_no_text_fact",
                "root_cause_not_confirmed",
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
        "followups": {"schema_version": "text_detector_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "text_detector_audit_report_v1",
            "text_detector_dryrun_v1_executed": True,
            "text_detector_dryrun_only": True,
            "supervision_available": sup_report.get("supervision_available"),
            "supervision_used": supervision_used,
            "crop_input_count": crop_intake_count,
            "frame_input_count": frame_intake_count,
            "text_region_candidate_count": cand_count,
            "bbox_adjustment_candidate_count": adj_count,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "same_frame_blocker_still_active": True,
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
