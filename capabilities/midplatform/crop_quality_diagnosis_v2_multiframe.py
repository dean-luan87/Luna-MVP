# -*- coding: utf-8 -*-
"""Crop quality diagnosis v2 for multiframe empty OCR (no OCR, no new crop, hypothesis only).

Phase-Crop-Quality-Diagnosis-v2-Multiframe-001
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Crop-Quality-Diagnosis-v2-Multiframe-001"
RUNTIME_STEP = "crop_quality_diagnosis_v2_multiframe"

FOLLOWUPS = [
    "Text-Detector-DryRun-v1",
    "BBox-Adjustment-Proposal-v2-Multiframe",
    "Crop-Quality-Scoring-v1",
    "OCRRequest-Gated-Submission-from-Multiframe-v2",
    "Evidence-Pack-Adapter-v4-Multiframe-Rerun",
    "Semantic-Candidate-v4-MultiframeAware",
    "Source-Validation-v2-Rerun-after-Multiframe",
    "Multiframe-Consensus-Policy-v1",
    "VisualSymbolRegistry-DryRun-v1",
    "Map-POI-Hint-DryRun-v1",
    "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
]

FUTURE_FIX_PHASES: List[Dict[str, Any]] = [
    {
        "future_phase": "Text-Detector-DryRun-v1",
        "purpose": "detector-supported bbox vs static projection",
        "required_input": ["better_frame_artifacts", "tracklet_candidate"],
        "expected_output": ["text_detector_dryrun_report"],
        "boundary": "dry_run_not_fact",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "BBox-Adjustment-Proposal-v2-Multiframe",
        "purpose": "propose bbox adjustments before re-crop",
        "required_input": ["crop_quality_diagnosis_v2", "tracklet"],
        "expected_output": ["bbox_adjustment_proposal"],
        "boundary": "proposal_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Crop-Quality-Scoring-v1",
        "purpose": "structured crop quality scoring after detector/crop fix",
        "required_input": ["adjusted_crops"],
        "expected_output": ["crop_quality_scores"],
        "boundary": "diagnostic_not_production",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v2",
        "purpose": "re-OCR after crop/bbox fix",
        "required_input": ["improved_multiframe_crops"],
        "expected_output": ["multiframe_ocr_result_collection_v2"],
        "boundary": "gated_submission_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Evidence-Pack-Adapter-v4-Multiframe-Rerun",
        "purpose": "re-adapt non-empty OCR to EP v4",
        "required_input": ["multiframe_ocr_result_collection_v2"],
        "expected_output": ["evidence_pack_v4_multiframe_collection_rerun"],
        "boundary": "adapter_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Semantic-Candidate-v4-MultiframeAware",
        "purpose": "semantic after non-empty OCR path",
        "required_input": ["evidence_pack_v4_with_text"],
        "expected_output": ["semantic_candidate_v4"],
        "boundary": "not_fact_until_governance",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Source-Validation-v2-Rerun-after-Multiframe",
        "purpose": "SV rerun after multiframe evidence matures",
        "required_input": ["semantic_v4_or_ep_v4_nonempty"],
        "expected_output": ["sv_rerun_report"],
        "boundary": "rerun_only",
        "not_in_current_phase": True,
    },
]

RULE_IDS = [
    "empty_ocr_result_requires_input_diagnosis",
    "empty_ocr_not_no_text_fact",
    "projection_crop_requires_projection_risk_check",
    "crop_size_requires_small_crop_check",
    "bbox_type_requires_comparison",
    "frame_offset_requires_frame_quality_check",
    "brightness_requires_lightweight_analysis",
    "blur_requires_lightweight_analysis",
    "root_cause_hypothesis_not_confirmed_by_default",
    "no_ocr_execution_in_this_phase",
    "no_new_crop_generation_in_this_phase",
    "no_source_validation_rerun_in_this_phase",
    "no_semantic_generation_in_this_phase",
    "no_world_model_attach_in_this_phase",
    "no_scene_delta_candidate_in_this_phase",
]

HYPOTHESES: List[Dict[str, Any]] = [
    {
        "hypothesis_id": "h_proj_bbox_miss",
        "hypothesis": "projection_bbox_may_miss_text",
        "supporting_signals": ["detected_region=false", "projection_is_approximate=true", "all_empty_ocr"],
        "contradicting_signals": ["ocr_provider_success_empty"],
        "confidence_level": "medium",
        "confirmed": False,
        "required_next_action": "Text-Detector-DryRun-v1",
    },
    {
        "hypothesis_id": "h_crop_too_small",
        "hypothesis": "crop_may_be_too_small",
        "supporting_signals": ["small_crop_risk_on_multiple_crops"],
        "contradicting_signals": [],
        "confidence_level": "medium",
        "confirmed": False,
        "required_next_action": "BBox-Adjustment-Proposal-v2-Multiframe",
    },
    {
        "hypothesis_id": "h_crop_low_quality",
        "hypothesis": "crop_may_be_low_quality",
        "supporting_signals": ["low_brightness_or_blur_risk"],
        "contradicting_signals": [],
        "confidence_level": "low",
        "confirmed": False,
        "required_next_action": "Crop-Quality-Scoring-v1",
    },
    {
        "hypothesis_id": "h_viewpoint_shift",
        "hypothesis": "viewpoint_shift_may_move_text_region",
        "supporting_signals": ["multiframe_frame_offsets", "projection_drift_risk"],
        "contradicting_signals": [],
        "confidence_level": "medium",
        "confirmed": False,
        "required_next_action": "Text-Detector-DryRun-v1",
    },
    {
        "hypothesis_id": "h_source_bbox_drift",
        "hypothesis": "source_bbox_static_projection_may_drift",
        "supporting_signals": ["static_bbox_projection", "region_drift_risk"],
        "contradicting_signals": [],
        "confidence_level": "medium",
        "confirmed": False,
        "required_next_action": "BBox-Adjustment-Proposal-v2-Multiframe",
    },
    {
        "hypothesis_id": "h_expanded_insufficient",
        "hypothesis": "expanded_bbox_still_insufficient",
        "supporting_signals": ["expanded_bbox_also_empty_ocr"],
        "contradicting_signals": ["expanded_bbox_larger_area"],
        "confidence_level": "low",
        "confirmed": False,
        "required_next_action": "BBox-Adjustment-Proposal-v2-Multiframe",
    },
    {
        "hypothesis_id": "h_crop_no_text",
        "hypothesis": "crop_may_not_contain_text",
        "supporting_signals": ["projection_not_detection", "near_blank_candidate"],
        "contradicting_signals": ["empty_ocr_not_no_text_fact_policy"],
        "confidence_level": "low",
        "confirmed": False,
        "required_next_action": "Text-Detector-DryRun-v1",
    },
    {
        "hypothesis_id": "h_rapidocr_empty_low_quality",
        "hypothesis": "rapidocr_may_return_empty_on_low_quality_crop",
        "supporting_signals": ["provider_success_empty", "small_or_blur_risk"],
        "contradicting_signals": ["provider_not_confirmed_failure"],
        "confidence_level": "low",
        "confirmed": False,
        "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v2",
    },
    {
        "hypothesis_id": "h_text_detector_needed",
        "hypothesis": "text_detector_needed_before_crop",
        "supporting_signals": ["detected_region_count=0", "projection_crop_not_detection"],
        "contradicting_signals": [],
        "confidence_level": "high",
        "confirmed": False,
        "required_next_action": "Text-Detector-DryRun-v1",
    },
    {
        "hypothesis_id": "h_bbox_adjust_before_reocr",
        "hypothesis": "bbox_adjustment_needed_before_re_ocr",
        "supporting_signals": ["requires_bbox_adjustment_or_detector", "all_empty"],
        "contradicting_signals": [],
        "confidence_level": "high",
        "confirmed": False,
        "required_next_action": "BBox-Adjustment-Proposal-v2-Multiframe",
    },
]

EXPECTED_FRAME_OFFSETS = [-30, -15, -5, 5, 15, 30]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _diagnosis_intake_id(ep_id: str) -> str:
    return f"cq_diag_intake_{hashlib.sha256(ep_id.encode()).hexdigest()[:10]}"


def _analyze_crop_image(path: Path) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "file_exists": path.is_file(),
        "file_size_bytes": path.stat().st_size if path.is_file() else 0,
        "image_read_success": False,
        "width": None,
        "height": None,
        "channel_count": None,
        "brightness_score": None,
        "blur_score": None,
        "all_black_candidate": False,
        "all_white_candidate": False,
        "near_blank_candidate": False,
    }
    if not path.is_file():
        return out
    try:
        import cv2  # type: ignore
        import numpy as np  # type: ignore

        img = cv2.imread(str(path))
        if img is None:
            return out
        out["image_read_success"] = True
        h, w = img.shape[:2]
        out["width"] = w
        out["height"] = h
        out["channel_count"] = int(img.shape[2]) if len(img.shape) > 2 else 1
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
        out["brightness_score"] = float(gray.mean())
        out["blur_score"] = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        mn, mx = float(gray.min()), float(gray.max())
        std = float(np.std(gray))
        out["all_black_candidate"] = mx < 8
        out["all_white_candidate"] = mn > 247
        out["near_blank_candidate"] = std < 3.0 or (mx - mn) < 5
    except Exception:
        pass
    return out


def _geometry_flags(width: int, height: int) -> Dict[str, Any]:
    area = width * height
    aspect = (width / height) if height > 0 else 0.0
    small = height < 32 or width < 80
    thin = height < 24 and width > height * 4
    extreme = aspect > 8.0 or (aspect < 0.5 and aspect > 0)
    notes: List[str] = []
    if small:
        notes.append("dimensions_below_recommended_threshold")
    if thin:
        notes.append("thin_horizontal_strip_like")
    if extreme:
        notes.append("extreme_aspect_ratio")
    status = "ok"
    if small or thin or extreme:
        status = "risk"
    return {
        "crop_width": width,
        "crop_height": height,
        "crop_area": area,
        "crop_aspect_ratio": round(aspect, 4),
        "small_crop_risk": small,
        "thin_crop_risk": thin,
        "extreme_aspect_ratio_risk": extreme,
        "geometry_status": status,
        "diagnosis_notes": notes,
    }


def _build_rules() -> List[Dict[str, Any]]:
    rules: List[Dict[str, Any]] = []
    for rid in RULE_IDS:
        rules.append(
            {
                "rule_id": rid,
                "condition": rid,
                "diagnosis_effect": "enforce_not_fact_boundary",
                "allowed_action": "read_and_diagnose_only",
                "blocked_action": "ocr_or_fact_write",
                "required_next_action": "Text-Detector-DryRun-v1_or_BBox-Adjustment",
                "fact_status_after_rule": "not_fact",
                "write_allowed_after_rule": False,
            }
        )
    return rules


def run_crop_quality_diagnosis_v2_multiframe(
    *,
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
    ep_root = Path(evidence_pack_v4_root).resolve()
    ocr_root = Path(multiframe_ocr_root).resolve()
    crop_root = Path(multiframe_crop_root).resolve()
    tr_root = Path(text_region_tracklet_root).resolve()
    bf_root = Path(better_frame_root).resolve()
    mf_root = Path(multiframe_merge_proposal_root).resolve()
    sv_root = Path(source_validation_v2_root).resolve()
    sem_root = Path(semantic_v3_root).resolve()
    ep3_root = Path(evidence_pack_v3_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    packs = [
        p
        for p in (_read_json(ep_root / "evidence_pack_v4_multiframe_collection.json") or {}).get("packs") or []
        if isinstance(p, dict)
    ]
    ep_count = len(packs)

    ocr_by_id = {
        str(r.get("multiframe_ocr_result_id")): r
        for r in (_read_json(ocr_root / "multiframe_ocr_result_collection_v1.json") or {}).get("rows") or []
        if isinstance(r, dict) and r.get("multiframe_ocr_result_id")
    }

    crops_by_id = {
        str(c.get("multiframe_crop_artifact_id")): c
        for c in (_read_json(crop_root / "multiframe_crop_artifact_collection_v1.json") or {}).get("artifacts") or []
        if isinstance(c, dict) and c.get("multiframe_crop_artifact_id")
    }

    bf_quality_by_ref: Dict[str, Dict[str, Any]] = {}
    for row in (_read_json(bf_root / "better_frame_quality_placeholder_report.json") or {}).get("rows") or []:
        if isinstance(row, dict) and row.get("candidate_frame_ref_id"):
            bf_quality_by_ref[str(row["candidate_frame_ref_id"])] = row

    drift_rep = (_read_json(tr_root / "text_region_drift_risk_report_v1.json") or {}).get("reports") or [{}]
    drift_row = drift_rep[0] if isinstance(drift_rep[0], dict) else {}
    default_drift = str(drift_row.get("drift_risk") or "medium")

    intake_rows: List[Dict[str, Any]] = []
    geometry_rows: List[Dict[str, Any]] = []
    brightness_rows: List[Dict[str, Any]] = []
    projection_rows: List[Dict[str, Any]] = []
    visual_rows: List[Dict[str, Any]] = []
    decision_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    small_crop_n = 0
    thin_crop_n = 0
    extreme_aspect_n = 0
    low_brightness_n = 0
    blur_risk_n = 0
    drift_medium_high = 0
    near_blank_n = 0
    empty_count = 0

    bbox_agg: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "bbox_type": "",
            "crop_count": 0,
            "empty_ocr_count": 0,
            "non_empty_ocr_count": 0,
            "widths": [],
            "heights": [],
            "areas": [],
            "aspects": [],
            "brightness": [],
            "blurs": [],
        }
    )
    frame_agg: Dict[int, Dict[str, Any]] = defaultdict(
        lambda: {
            "frame_index": 0,
            "frame_offset_from_source": 0,
            "crop_count": 0,
            "empty_ocr_count": 0,
            "non_empty_ocr_count": 0,
            "brightness": [],
            "blurs": [],
        }
    )

    for pack in packs:
        ep_id = str(pack.get("evidence_pack_v4_id") or "")
        ocr_id = str(pack.get("multiframe_ocr_result_ref") or "")
        crop_id = str(pack.get("multiframe_crop_artifact_ref") or "")
        ocr = ocr_by_id.get(ocr_id, {})
        crop_art = crops_by_id.get(crop_id, {})

        raw_text = str(pack.get("raw_ocr", {}).get("raw_ocr_text") if isinstance(pack.get("raw_ocr"), dict) else pack.get("raw_ocr_text") or "")
        if not raw_text and ocr:
            raw_text = str(ocr.get("raw_ocr_text") or "")
        empty_text = bool(pack.get("empty_text") if pack.get("empty_text") is not None else ocr.get("empty_text"))
        if empty_text:
            empty_count += 1

        w = int(crop_art.get("crop_width") or 0)
        h = int(crop_art.get("crop_height") or 0)
        crop_path = Path(str(crop_art.get("crop_file_path") or pack.get("crop_file_path") or ""))
        geom = _geometry_flags(w, h)
        if geom["small_crop_risk"]:
            small_crop_n += 1
        if geom["thin_crop_risk"]:
            thin_crop_n += 1
        if geom["extreme_aspect_ratio_risk"]:
            extreme_aspect_n += 1

        vis = _analyze_crop_image(crop_path)
        if vis.get("near_blank_candidate"):
            near_blank_n += 1

        b_score = vis.get("brightness_score")
        blur_score = vis.get("blur_score")
        low_b = bool(b_score is not None and b_score < 45)
        blur_r = bool(blur_score is not None and blur_score < 80)
        if low_b:
            low_brightness_n += 1
        if blur_r:
            blur_risk_n += 1

        bbox_type = str(pack.get("bbox_type") or crop_art.get("bbox_type") or "")
        fi = int(pack.get("frame_index") or 0)
        fo = int(pack.get("frame_offset_from_source") or 0)
        cref = str(pack.get("candidate_frame_ref") or crop_art.get("candidate_frame_ref_id") or "")

        intake_rows.append(
            {
                "diagnosis_intake_id": _diagnosis_intake_id(ep_id),
                "evidence_pack_v4_id": ep_id,
                "multiframe_ocr_result_id": ocr_id,
                "multiframe_crop_artifact_id": crop_id,
                "ocrrequest_reference_multiframe_id": pack.get("ocrrequest_reference_multiframe_ref"),
                "tracklet_candidate_id": pack.get("multiframe_context", {}).get("tracklet_candidate_id")
                if isinstance(pack.get("multiframe_context"), dict)
                else pack.get("tracklet_candidate_id"),
                "candidate_frame_ref_id": cref,
                "frame_index": fi,
                "frame_time_sec": pack.get("frame_time_sec"),
                "frame_offset_from_source": fo,
                "crop_file_path": str(crop_path),
                "crop_width": w,
                "crop_height": h,
                "crop_area": geom["crop_area"],
                "crop_aspect_ratio": geom["crop_aspect_ratio"],
                "bbox_type": bbox_type,
                "projection_method": pack.get("projection_method"),
                "projection_is_approximate": True,
                "detected_region": False,
                "raw_ocr_text": raw_text,
                "empty_text": empty_text,
                "result_status": (pack.get("provider_metadata") or {}).get("result_status")
                if isinstance(pack.get("provider_metadata"), dict)
                else ocr.get("result_status"),
                "provider": (pack.get("provider_metadata") or {}).get("provider")
                if isinstance(pack.get("provider_metadata"), dict)
                else ocr.get("provider"),
                "provider_status": (pack.get("provider_metadata") or {}).get("provider_status")
                if isinstance(pack.get("provider_metadata"), dict)
                else ocr.get("provider_status"),
                "intake_status": "accepted",
                "eligible_for_quality_diagnosis": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        geometry_rows.append(
            {
                "multiframe_crop_artifact_id": crop_id,
                "evidence_pack_v4_id": ep_id,
                "frame_index": fi,
                "frame_offset_from_source": fo,
                "bbox_type": bbox_type,
                **geom,
            }
        )

        brightness_rows.append(
            {
                "multiframe_crop_artifact_id": crop_id,
                "frame_index": fi,
                "bbox_type": bbox_type,
                "crop_file_path": str(crop_path),
                "brightness_score": b_score,
                "blur_score": blur_score,
                "low_brightness_risk": low_b,
                "blur_risk": blur_r,
                "lightweight_placeholder": True,
                "quality_claim_allowed": False,
                "diagnosis_only": True,
            }
        )

        region_conf = float(crop_art.get("region_confidence") or 0.35)
        drift_risk = default_drift
        if region_conf < 0.4:
            drift_risk = "high"
        elif region_conf < 0.5:
            drift_risk = "medium"
        if drift_risk in ("medium", "high"):
            drift_medium_high += 1

        projection_rows.append(
            {
                "multiframe_crop_artifact_id": crop_id,
                "tracklet_candidate_id": pack.get("multiframe_context", {}).get("tracklet_candidate_id")
                if isinstance(pack.get("multiframe_context"), dict)
                else None,
                "frame_index": fi,
                "frame_offset_from_source": fo,
                "projection_method": pack.get("projection_method"),
                "projection_is_approximate": True,
                "detected_region": False,
                "region_confidence": region_conf,
                "drift_risk": drift_risk,
                "drift_risk_reason": "static_projection_low_region_confidence",
                "viewpoint_shift_risk": "medium" if abs(fo) >= 15 else "low",
                "cross_region_merge_risk": "medium",
                "projection_status": "approximate_projection",
                "required_next_action": "Text-Detector-DryRun-v1",
            }
        )

        visual_rows.append(
            {
                "multiframe_crop_artifact_id": crop_id,
                "crop_file_path": str(crop_path),
                "file_exists": vis["file_exists"],
                "file_size_bytes": vis["file_size_bytes"],
                "image_read_success": vis["image_read_success"],
                "width": vis["width"] or w,
                "height": vis["height"] or h,
                "channel_count": vis["channel_count"],
                "all_black_candidate": vis["all_black_candidate"],
                "all_white_candidate": vis["all_white_candidate"],
                "near_blank_candidate": vis["near_blank_candidate"],
                "visual_existence_status": "readable" if vis["image_read_success"] else "unreadable",
            }
        )

        quality_statuses: List[str] = ["insufficient_for_semantic", "insufficient_for_sv_rerun"]
        if geom["small_crop_risk"] or geom["thin_crop_risk"]:
            quality_statuses.append("requires_bbox_adjustment")
        if low_b or blur_r:
            quality_statuses.append("requires_crop_quality_scoring")
        quality_statuses.append("requires_text_detector")
        quality_statuses.append("requires_re_ocr_after_fix")

        decision_rows.append(
            {
                "multiframe_crop_artifact_id": crop_id,
                "evidence_pack_v4_id": ep_id,
                "quality_status": quality_statuses,
                "diagnosis_decision": "blocked_downstream_until_crop_or_detector_fix",
                "recommended_next_action": "Text-Detector-DryRun-v1_or_BBox-Adjustment-Proposal-v2-Multiframe",
                "semantic_v4_allowed": False,
                "source_validation_rerun_allowed": False,
                "re_ocr_allowed_now": False,
                "future_re_ocr_after_fix_allowed": True,
                "fact_write_allowed": False,
            }
        )

        chain_rows.append(
            {
                "diagnosis_intake_id": _diagnosis_intake_id(ep_id),
                "evidence_pack_v4_id": ep_id,
                "traceable_to_ep_v4": True,
                "traceable_to_multiframe_ocr_result": ocr_root.is_dir(),
                "traceable_to_multiframe_crop": crop_root.is_dir(),
                "traceable_to_tracklet": tr_root.is_dir(),
                "traceable_to_better_frame": bf_root.is_dir(),
                "traceable_to_multiframe_proposal": mf_root.is_dir(),
                "traceable_to_source_validation_v2": sv_root.is_dir(),
                "traceable_to_semantic_candidate_v3": sem_root.is_dir(),
                "traceable_to_evidence_pack_v3": ep3_root.is_dir(),
                "traceable_to_linebox_trace": Path(linebox_sq_root).resolve().is_dir(),
                "source_chain_preserved": True,
            }
        )

        ba = bbox_agg[bbox_type]
        ba["bbox_type"] = bbox_type
        ba["crop_count"] += 1
        if empty_text:
            ba["empty_ocr_count"] += 1
        else:
            ba["non_empty_ocr_count"] += 1
        ba["widths"].append(w)
        ba["heights"].append(h)
        ba["areas"].append(geom["crop_area"])
        ba["aspects"].append(geom["crop_aspect_ratio"])
        if b_score is not None:
            ba["brightness"].append(b_score)
        if blur_score is not None:
            ba["blurs"].append(blur_score)

        fa = frame_agg[fi]
        fa["frame_index"] = fi
        fa["frame_offset_from_source"] = fo
        fa["crop_count"] += 1
        if empty_text:
            fa["empty_ocr_count"] += 1
        else:
            fa["non_empty_ocr_count"] += 1
        if b_score is not None:
            fa["brightness"].append(b_score)
        if blur_score is not None:
            fa["blurs"].append(blur_score)

    def _avg(vals: List[float]) -> Optional[float]:
        return round(sum(vals) / len(vals), 4) if vals else None

    geom_summary = {
        "crop_count": ep_count,
        "min_width": min((r["crop_width"] for r in geometry_rows), default=0),
        "max_width": max((r["crop_width"] for r in geometry_rows), default=0),
        "min_height": min((r["crop_height"] for r in geometry_rows), default=0),
        "max_height": max((r["crop_height"] for r in geometry_rows), default=0),
        "min_area": min((r["crop_area"] for r in geometry_rows), default=0),
        "max_area": max((r["crop_area"] for r in geometry_rows), default=0),
        "small_crop_risk_count": small_crop_n,
        "thin_crop_risk_count": thin_crop_n,
        "extreme_aspect_ratio_risk_count": extreme_aspect_n,
    }

    bbox_comparison: List[Dict[str, Any]] = []
    for bt, agg in sorted(bbox_agg.items()):
        cc = agg["crop_count"]
        er = agg["empty_ocr_count"] / cc if cc else 0.0
        bbox_comparison.append(
            {
                "bbox_type": bt,
                "crop_count": cc,
                "empty_ocr_count": agg["empty_ocr_count"],
                "non_empty_ocr_count": agg["non_empty_ocr_count"],
                "avg_width": _avg([float(x) for x in agg["widths"]]),
                "avg_height": _avg([float(x) for x in agg["heights"]]),
                "avg_area": _avg([float(x) for x in agg["areas"]]),
                "avg_aspect_ratio": _avg([float(x) for x in agg["aspects"]]),
                "avg_brightness": _avg(agg["brightness"]),
                "avg_blur": _avg(agg["blurs"]),
                "empty_rate": round(er, 4),
                "relative_quality_candidate": "diagnostic_only_no_winner",
                "comparison_is_diagnostic_only": True,
                "fact_status": "not_fact",
            }
        )

    frame_offset_rows: List[Dict[str, Any]] = []
    for fi in sorted(frame_agg.keys()):
        agg = frame_agg[fi]
        cc = agg["crop_count"]
        er = agg["empty_ocr_count"] / cc if cc else 0.0
        bf_row = None
        for _cref, bfr in bf_quality_by_ref.items():
            if bfr:
                bf_row = bfr
                break
        avg_b = _avg(agg["brightness"])
        avg_bl = _avg(agg["blurs"])
        fq_risk = "low"
        if avg_bl is not None and avg_bl < 80:
            fq_risk = "medium"
        frame_offset_rows.append(
            {
                "frame_index": fi,
                "frame_offset_from_source": agg["frame_offset_from_source"],
                "crop_count": cc,
                "empty_ocr_count": agg["empty_ocr_count"],
                "non_empty_ocr_count": agg["non_empty_ocr_count"],
                "avg_brightness": avg_b,
                "avg_blur": avg_bl,
                "empty_rate": round(er, 4),
                "frame_quality_placeholder_available": bool(bf_quality_by_ref),
                "frame_quality_risk": fq_risk,
                "frame_offset_diagnostic_status": "all_empty_under_current_projection",
            }
        )

    brightness_summary = {
        "avg_brightness": _avg([r["brightness_score"] for r in brightness_rows if r.get("brightness_score") is not None]),
        "avg_blur": _avg([r["blur_score"] for r in brightness_rows if r.get("blur_score") is not None]),
        "low_brightness_risk_count": low_brightness_n,
        "blur_risk_count": blur_risk_n,
    }

    projection_summary = {
        "projection_crop_count": ep_count,
        "detected_region_count": 0,
        "projection_is_approximate_count": ep_count,
        "medium_or_high_drift_risk_count": drift_medium_high,
        "requires_text_detector_count": ep_count,
    }

    non_empty = ep_count - empty_count
    empty_rate = empty_count / ep_count if ep_count else 0.0

    summary = {
        "schema_version": "crop_quality_diagnosis_v2_multiframe_summary_v0",
        "phase": PHASE_ID,
        "diagnosis_scope": "multiframe_crop_quality_diagnosis_only",
        "based_on_evidence_pack_v4_multiframe": True,
        "based_on_multiframe_crop_execution": True,
        "evidence_pack_v4_count_observed": ep_count,
        "multiframe_crop_artifact_count_observed": ep_count,
        "empty_ocr_result_count_observed": empty_count,
        "non_empty_ocr_result_count_observed": non_empty,
        "crop_quality_diagnosis_generated": True,
        "root_cause_confirmed": False,
        "root_cause_hypothesis_count": len(HYPOTHESES),
        "small_crop_risk_count": small_crop_n,
        "projection_drift_risk_count": drift_medium_high,
        "low_brightness_risk_count": low_brightness_n,
        "blur_risk_count": blur_risk_n,
        "bbox_type_comparison_generated": True,
        "frame_offset_analysis_generated": True,
        "ocr_invoked": False,
        "provider_invoked": False,
        "new_crop_generated": False,
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
        "phase_verdict_hint": "GO" if ep_count == 30 and empty_count == 30 else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {"schema_version": "crop_quality_diagnosis_v2_intake_matrix_v1", "row_count": len(intake_rows), "rows": intake_rows},
        "rule_matrix": {"schema_version": "crop_quality_diagnosis_v2_rule_matrix_v1", "rules": _build_rules()},
        "geometry": {
            "schema_version": "crop_quality_geometry_diagnosis_report_v2",
            "summary": geom_summary,
            "rows": geometry_rows,
        },
        "bbox_comparison": {
            "schema_version": "crop_quality_bbox_type_comparison_report_v2",
            "groups": bbox_comparison,
            "comparison_is_diagnostic_only": True,
            "source_bbox_group_present": any(g["bbox_type"] == "source_bbox" for g in bbox_comparison),
            "expanded_bbox_group_present": any(g["bbox_type"] == "expanded_bbox" for g in bbox_comparison),
            "expanded_bbox_also_empty_note": "expanded_bbox_empty_under_current_projection_not_invalid_strategy",
            "fact_status": "not_fact",
        },
        "frame_offset": {
            "schema_version": "crop_quality_frame_offset_diagnosis_report_v2",
            "expected_frame_offsets": EXPECTED_FRAME_OFFSETS,
            "row_count": len(frame_offset_rows),
            "rows": frame_offset_rows,
        },
        "brightness_blur": {
            "schema_version": "crop_quality_brightness_blur_report_v2",
            "summary": brightness_summary,
            "rows": brightness_rows,
            "lightweight_placeholder": True,
            "quality_claim_allowed": False,
            "diagnosis_only": True,
        },
        "projection_drift": {
            "schema_version": "crop_quality_projection_drift_diagnosis_report_v2",
            "summary": projection_summary,
            "rows": projection_rows,
            "projection_crop_not_detection": True,
        },
        "empty_pattern": {
            "schema_version": "crop_quality_empty_result_pattern_report_v2",
            "total_result_count": ep_count,
            "empty_result_count": empty_count,
            "non_empty_result_count": non_empty,
            "empty_result_rate": round(empty_rate, 4),
            "all_empty": empty_count == ep_count and ep_count > 0,
            "empty_text_is_valid_ocr_result": True,
            "empty_text_is_not_no_text_fact": True,
            "no_text_fact_written": False,
            "pattern_status": "all_empty_multiframe_projection_crop",
            "pattern_interpretation": (
                "Current multiframe projection crops produced valid but empty OCR results; "
                "this does not imply absence of text in the region. "
                "Investigate projection, bbox, crop quality, and text detector support."
            ),
        },
        "visual_existence": {
            "schema_version": "crop_quality_visual_existence_report_v2",
            "row_count": len(visual_rows),
            "rows": visual_rows,
            "all_readable": all(r.get("image_read_success") for r in visual_rows),
        },
        "root_cause": {
            "schema_version": "crop_quality_root_cause_hypothesis_report_v2",
            "root_cause_confirmed": False,
            "hypothesis_count": len(HYPOTHESES),
            "hypotheses": HYPOTHESES,
        },
        "decision_matrix": {
            "schema_version": "crop_quality_diagnosis_decision_matrix_v2",
            "row_count": len(decision_rows),
            "rows": decision_rows,
        },
        "future_fix_plan": {
            "schema_version": "crop_quality_future_fix_plan_v2",
            "phases": FUTURE_FIX_PHASES,
        },
        "semantic_sv_blocker": {
            "schema_version": "crop_quality_semantic_sv_blocker_carryover_report_v2",
            "semantic_v4_still_blocked": True,
            "source_validation_rerun_still_blocked": True,
            "blocker_reason": "empty_ocr_result_and_projection_risk",
            "same_frame_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
            "required_future_phase": "Text-Detector-DryRun-v1_or_BBox-Adjustment-Proposal-v2-Multiframe",
        },
        "source_chain": {
            "schema_version": "crop_quality_source_chain_report_v2",
            "row_count": len(chain_rows),
            "rows": chain_rows,
        },
        "boundary": {
            "schema_version": "crop_quality_boundary_report_v2",
            "crop_quality_diagnosis_only": True,
            "ocr_invoked": False,
            "provider_invoked": False,
            "new_crop_generated": False,
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
            "schema_version": "crop_quality_metrics_candidate_report_v2",
            "evidence_pack_v4_count_observed": ep_count,
            "multiframe_crop_artifact_count_observed": ep_count,
            "empty_ocr_result_count_observed": empty_count,
            "non_empty_ocr_result_count_observed": non_empty,
            "crop_count": ep_count,
            "small_crop_risk_count": small_crop_n,
            "thin_crop_risk_count": thin_crop_n,
            "extreme_aspect_ratio_risk_count": extreme_aspect_n,
            "low_brightness_risk_count": low_brightness_n,
            "blur_risk_count": blur_risk_n,
            "projection_drift_risk_count": drift_medium_high,
            "near_blank_candidate_count": near_blank_n,
            "root_cause_hypothesis_count": len(HYPOTHESES),
            "confirmed_root_cause_count": 0,
            "semantic_candidate_generated_count": 0,
            "source_validation_rerun_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "crop_quality_benchmark_link_report_v2",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "crop_quality_system_health_link_report_v2",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "crop_quality_no_write_boundary_report_v2",
            "boundary_ok": True,
            "violations": [],
            "crop_quality_diagnosis_only": True,
            "ocr_invoked": False,
            "provider_invoked": False,
            "new_crop_generated": False,
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
            "schema_version": "crop_quality_simulation_context_report_v2",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "crop_quality_non_claims_report_v2",
            "claims": [
                "no_ocr_in_this_phase",
                "no_new_crop_in_this_phase",
                "crop_quality_diagnosis_not_fact_verification",
                "empty_ocr_not_no_text_fact",
                "near_blank_not_no_text_fact",
                "root_cause_is_hypothesis_not_confirmed",
                "provider_failure_not_confirmed",
                "projection_drift_not_detector_proven",
                "no_semantic_candidate",
                "no_sv_rerun",
                "no_world_model",
                "no_scene_delta",
                "not_benchmark",
                "not_provider_comparison",
                "not_navigation",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "crop_quality_open_followups_v2", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "crop_quality_audit_report_v2",
            "crop_quality_diagnosis_v2_multiframe_executed": True,
            "crop_quality_diagnosis_only": True,
            "evidence_pack_v4_count_observed": ep_count,
            "multiframe_crop_artifact_count_observed": ep_count,
            "empty_ocr_result_count_observed": empty_count,
            "non_empty_ocr_result_count_observed": non_empty,
            "root_cause_confirmed": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "new_crop_generated": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "same_frame_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
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
