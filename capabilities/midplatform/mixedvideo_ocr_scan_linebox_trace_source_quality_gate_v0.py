# -*- coding: utf-8 -*-
"""P0 video scan linebox trace + OCR source quality gate.

Phase-MixedVideo-OCR-Scan-LineBox-Trace-SourceQualityGate-001
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "MixedVideo-OCR-Scan-LineBox-Trace-SourceQualityGate-001"
P0_VIDEO_ID = "test_video_complex_6m42s"
SCAN_STEP = "mixedvideo_scan_linebox_trace"
GATE_STEP = "ocr_source_quality_gate"

BRAND_PAT = re.compile(r"HOKA|GAP|NIKE|SALE{2,}|andSTORE", re.I)
PUBLIC_PAT = re.compile(r"禁烟|NO\s*SMO?KING|出口|EXIT", re.I)
BANK_PAT = re.compile(r"银行|Bank|建设", re.I)


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _parse_ocr_rows(result: Any) -> Tuple[str, List[Dict[str, Any]], float]:
    items: List[Dict[str, Any]] = []
    scores: List[float] = []
    if not result:
        return "", items, 0.0
    for i, row in enumerate(result):
        if not isinstance(row, (list, tuple)) or len(row) < 2:
            continue
        box = row[0]
        text = str(row[1] or "").strip()
        conf = float(row[2]) if len(row) >= 3 and row[2] is not None else None
        if conf is not None:
            scores.append(conf)
        polygon: List[Any] = []
        bbox = [None, None, None, None]
        if isinstance(box, (list, tuple)):
            if len(box) == 4 and all(isinstance(x, (int, float)) for x in box):
                bbox = [float(x) for x in box]
            else:
                for pt in box:
                    if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                        polygon.append([float(pt[0]), float(pt[1])])
                if polygon:
                    xs = [p[0] for p in polygon]
                    ys = [p[1] for p in polygon]
                    bbox = [min(xs), min(ys), max(xs), max(ys)]
        x1, y1, x2, y2 = bbox
        bbox_xywh = None
        if all(v is not None for v in bbox):
            bbox_xywh = [x1, y1, x2 - x1, y2 - y1]
        items.append(
            {
                "line_index": i,
                "text": text,
                "confidence": conf,
                "bbox_xyxy": bbox,
                "bbox_xywh": bbox_xywh,
                "polygon": polygon,
                "text_source": "scan_full_frame_ocr",
            }
        )
    parts = [it["text"] for it in items if it.get("text")]
    joined = " | ".join(parts) if len(parts) > 1 else " ".join(parts)
    avg = sum(scores) / len(scores) if scores else 0.0
    return joined.strip(), items, avg


def _centroid(bbox: List[Any]) -> Optional[Tuple[float, float]]:
    if not bbox or len(bbox) != 4 or any(x is None for x in bbox):
        return None
    x1, y1, x2, y2 = [float(x) for x in bbox]
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def _count_regions(items: List[Dict[str, Any]], img_w: float, img_h: float) -> int:
    cents = []
    for it in items:
        c = _centroid(it.get("bbox_xyxy") or [])
        if c:
            cents.append(c)
    if len(cents) <= 1:
        return len(cents)
    # cluster: split by horizontal thirds
    bands = set()
    for cx, cy in cents:
        band = int(min(2, max(0, cx / max(img_w, 1) * 3)))
        vband = int(min(2, max(0, cy / max(img_h, 1) * 3)))
        bands.add((band, vband))
    return max(1, len(bands))


def _spread_score(items: List[Dict[str, Any]], img_w: float, img_h: float) -> float:
    cents = [_centroid(it.get("bbox_xyxy") or []) for it in items]
    cents = [c for c in cents if c]
    if len(cents) < 2:
        return 0.0
    max_d = 0.0
    for i, a in enumerate(cents):
        for b in cents[i + 1 :]:
            d = math.hypot(a[0] - b[0], img_w or 1) + math.hypot(a[1] - b[1], img_h or 1)
            max_d = max(max_d, d / max(img_w + img_h, 1))
    return min(1.0, max_d)


def _heuristic_quality(
    preview: str,
    items: List[Dict[str, Any]],
    avg_conf: float,
    img_w: int,
    img_h: int,
    linebox_available: bool,
) -> Dict[str, Any]:
    n = len(items)
    regions = _count_regions(items, float(img_w), float(img_h)) if linebox_available else 0
    spread = _spread_score(items, float(img_w), float(img_h)) if linebox_available else 0.5
    mixed_risk = "high" if regions >= 3 or spread > 0.35 or "|" in preview and n >= 4 else "medium" if regions >= 2 else "low"
    brand_like = bool(BRAND_PAT.search(preview)) or any(len((it.get("text") or "")) <= 5 and (it.get("text") or "").isupper() for it in items)
    public_like = bool(PUBLIC_PAT.search(preview))
    bank_like = bool(BANK_PAT.search(preview))

    motion_blur = "high" if avg_conf < 0.45 and n > 0 else "medium" if avg_conf < 0.65 else "low"
    occlusion = "medium" if n > 0 and avg_conf < 0.55 else "low"
    compression = "medium" if n > 8 and avg_conf < 0.7 else "low"
    text_size = "small" if linebox_available and items and all(
        (it.get("bbox_xyxy") or [0, 0, 0, 0])[2] - (it.get("bbox_xyxy") or [0, 0, 0, 0])[0] < img_w * 0.08 for it in items
    ) else "medium"
    full_frame_noise = "high" if n >= 8 and mixed_risk == "high" else "medium" if n >= 5 else "low"
    view_angle = "medium"
    frontality = "medium" if avg_conf >= 0.7 else "low"
    crop_spec = "low"
    stability = "medium"
    distance = "medium" if text_size == "small" else "near"
    lighting = "medium"
    contrast = round(avg_conf, 3) if n else None
    logo_sym = "high" if brand_like and n <= 3 else "medium" if brand_like else "low"
    pf_sem = "high" if public_like else "low"

    # grade
    if not linebox_available or n == 0:
        grade, gate = "SQ_E", "reject_as_unreadable_or_mixed"
        action = "require_linebox_trace"
    elif brand_like and regions >= 2:
        grade, gate = "SQ_D", "route_to_visual_symbol"
        action = "route_logo_to_visual_symbol"
    elif mixed_risk == "high" or (regions >= 3 and "|" in preview):
        grade, gate = "SQ_E", "reject_as_unreadable_or_mixed"
        action = "generate_roi_crop_before_pack"
    elif mixed_risk == "medium" or regions >= 2:
        grade, gate = "SQ_C", "require_roi_crop"
        action = "generate_roi_crop_before_pack"
    elif public_like and avg_conf >= 0.5:
        grade, gate = "SQ_B", "accept_as_partial_evidence"
        action = "public_facility_semantic_first"
    elif avg_conf >= 0.75 and regions == 1:
        grade, gate = "SQ_A", "accept_for_ocr_evidence"
        action = "roi_ocr_then_evidence_pack"
    else:
        grade, gate = "SQ_B", "accept_as_partial_evidence"
        action = "require_roi_crop"

    return {
        "view_angle_quality": view_angle,
        "text_frontality": frontality,
        "occlusion_level": occlusion,
        "motion_blur_level": motion_blur,
        "compression_artifact_level": compression,
        "text_size_level": text_size,
        "distance_level": distance,
        "lighting_quality": lighting,
        "contrast_score": contrast,
        "frame_stability": stability,
        "crop_specificity": crop_spec,
        "mixed_text_region_risk": mixed_risk,
        "full_frame_noise_risk": full_frame_noise,
        "logo_visual_symbol_likelihood": logo_sym,
        "public_facility_semantic_likelihood": pf_sem,
        "dominant_region_count": regions,
        "source_quality_grade": grade,
        "gate_decision": gate,
        "required_next_action": action,
        "brand_like": brand_like,
        "public_like": public_like,
        "bank_like": bank_like,
    }


def _ocr_frame(
    frame: Any,
    max_width: int,
    ocr: Any,
    cv2: Any,
) -> Tuple[List[Dict[str, Any]], int, int, str, bool, Optional[str]]:
    h, w = frame.shape[:2]
    if w > max_width:
        sc = max_width / w
        frame = cv2.resize(frame, (int(w * sc), int(h * sc)))
        h, w = frame.shape[:2]
    result, _ = ocr(frame)
    preview, items, _ = _parse_ocr_rows(result)
    if not items:
        return [], w, h, preview, False, "ocr_no_line_boxes"
    for it in items:
        it["readability_grade_candidate"] = "B" if (it.get("confidence") or 0) >= 0.7 else "C"
        it["quality_flags"] = ["scan_full_frame", "not_fact"]
        it["source_chain"] = [SCAN_STEP, "rapidocr_lightweight", GATE_STEP]
    return items, w, h, preview, True, None


def _rescan_selected_frames_sequential(
    video_path: Path,
    frame_indices: List[int],
    max_width: int,
    ocr: Any,
    cv2: Any,
) -> Dict[int, Tuple[List[Dict[str, Any]], int, int, str, bool, Optional[str]]]:
    """Sequential decode until max target frame; avoids broken CAP_PROP_POS_FRAMES on some codecs."""
    targets = set(frame_indices)
    if not targets:
        return {}
    max_idx = max(targets)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return {fi: ([], 0, 0, "", False, "video_open_failed") for fi in frame_indices}
    out: Dict[int, Tuple[List[Dict[str, Any]], int, int, str, bool, Optional[str]]] = {}
    idx = 0
    while idx <= max_idx:
        ok, frame = cap.read()
        if not ok or frame is None:
            break
        if idx in targets:
            out[idx] = _ocr_frame(frame, max_width, ocr, cv2)
        idx += 1
    cap.release()
    for fi in frame_indices:
        if fi not in out:
            out[fi] = ([], 0, 0, "", False, "frame_not_reached_in_sequential_read")
    return out


def run_mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0(
    *,
    output_root: str,
    mixed_batch_root: str,
    readability_governance_root: str,
    evidence_pack_contract_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    p0_video_path: str,
    rescan_p0: bool = True,
    max_video_width: int = 1280,
) -> Tuple[Any, ...]:
    errs: List[str] = []
    out = Path(output_root).resolve()
    batch = Path(mixed_batch_root).resolve()
    p0_path = Path(p0_video_path).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    plan_doc = _read_json(batch / "mixed_video_selected_text_bearing_frame_plan.json") or {}
    pack_doc = _read_json(batch / "mixed_ocr_evidence_pack_collection.json") or {}
    selected = [f for f in (plan_doc.get("selected_frames") or []) if isinstance(f, dict)]

    pack_by_frame: Dict[int, Dict[str, Any]] = {}
    for p in pack_doc.get("packs") or []:
        if not isinstance(p, dict):
            continue
        src = p.get("source") or {}
        if src.get("source_type") != "video_frame_roi":
            continue
        fi = (p.get("temporal_coordinates") or {}).get("frame_index")
        if fi is not None:
            pack_by_frame[int(fi)] = p

    video_loaded = p0_path.is_file()
    ocr_scan_invoked = False
    ocr = cv2 = None
    if rescan_p0 and video_loaded:
        try:
            import cv2 as _cv2  # type: ignore
            from rapidocr_onnxruntime import RapidOCR  # type: ignore

            cv2 = _cv2
            ocr = RapidOCR()
            ocr_scan_invoked = True
        except ImportError as e:
            errs.append(str(e))

    trace_frames: List[Dict[str, Any]] = []
    plan_updates: List[Dict[str, Any]] = []
    eval_rows: List[Dict[str, Any]] = []
    consistency_rows: List[Dict[str, Any]] = []

    rescan_results: Dict[int, Tuple[List[Dict[str, Any]], int, int, str, bool, Optional[str]]] = {}
    if ocr_scan_invoked and ocr and cv2:
        indices = [int(sf.get("frame_index") or 0) for sf in selected]
        rescan_results = _rescan_selected_frames_sequential(p0_path, indices, max_video_width, ocr, cv2)

    for sf in selected:
        fi = int(sf.get("frame_index") or 0)
        ts_ms = int(sf.get("timestamp_ms") or 0)
        ts_sec = float(sf.get("timestamp_sec") or 0)
        frame_id = f"{P0_VIDEO_ID}_f{fi:06d}"
        original_preview = str(sf.get("ocr_preview") or "")
        items: List[Dict[str, Any]] = []
        img_w, img_h = 0, 0
        display_preview = original_preview
        linebox_available = False
        missing_reason: Optional[str] = None

        if fi in rescan_results:
            items, img_w, img_h, display_preview, linebox_available, missing_reason = rescan_results[fi]
            if not linebox_available and original_preview:
                display_preview = original_preview
                missing_reason = missing_reason or "rescan_empty_use_plan_preview_only"
        elif ocr_scan_invoked:
            missing_reason = "frame_rescan_missing"
        else:
            missing_reason = "ocr_rescan_not_invoked"

        source_chain = [SCAN_STEP, "rapidocr_lightweight", GATE_STEP, "mixed_batch_plan_ref"]
        avg_conf = 0.0
        if items:
            confs = [float(it["confidence"]) for it in items if it.get("confidence") is not None]
            avg_conf = sum(confs) / len(confs) if confs else 0.0

        q = _heuristic_quality(display_preview, items, avg_conf, img_w or 544, img_h or 960, linebox_available)
        regions = q["dominant_region_count"]
        possible_mixed = regions >= 2 or q["mixed_text_region_risk"] in ("high", "medium") or "SALE" in display_preview.upper()

        trace_frames.append(
            {
                "video_id": P0_VIDEO_ID,
                "video_path": str(p0_path),
                "frame_id": frame_id,
                "frame_index": fi,
                "timestamp_ms": ts_ms,
                "video_time_sec": ts_sec,
                "image_width": img_w or None,
                "image_height": img_h or None,
                "ocr_preview": display_preview,
                "display_text_only": not linebox_available,
                "linebox_available": linebox_available,
                "missing_reason": missing_reason,
                "text_items": items,
                "text_item_count": len(items),
                "source_chain": source_chain,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        plan_updates.append(
            {
                "frame_plan_id": sf.get("frame_plan_id"),
                "video_id": P0_VIDEO_ID,
                "frame_index": fi,
                "timestamp_ms": ts_ms,
                "video_time_sec": ts_sec,
                "original_ocr_preview": original_preview,
                "selected_text_items": items,
                "linebox_available": linebox_available,
                "selected_text_item_count": len(items),
                "dominant_text_region_count": regions,
                "possible_mixed_regions": possible_mixed,
                "scan_quality_grade": q["source_quality_grade"],
                "source_quality_gate_decision": q["gate_decision"],
                "missing_reason": missing_reason,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        eval_rows.append(
            {
                "frame_plan_id": sf.get("frame_plan_id"),
                "frame_index": fi,
                "timestamp_ms": ts_ms,
                "original_ocr_preview": original_preview,
                "linebox_available": linebox_available,
                "text_item_count": len(items),
                **{k: q[k] for k in q if k not in ("gate_decision", "required_next_action", "brand_like", "public_like", "bank_like")},
                "gate_decision": q["gate_decision"],
                "required_next_action": q["required_next_action"],
            }
        )

        pack = pack_by_frame.get(fi)
        pack_exists = pack is not None
        pack_text = str((pack.get("raw_ocr") or {}).get("raw_ocr_text") or "") if pack else ""
        pack_empty = (pack.get("raw_ocr") or {}).get("empty_text", True) if pack else True
        scan_has_text = bool(original_preview.strip()) or len(items) > 0

        if not pack_exists:
            status, reason, fix = "scan_has_text_pack_missing", "pack_not_generated_for_frame", "generate_roi_crop_before_pack"
        elif scan_has_text and pack_empty:
            if possible_mixed:
                status, reason, fix = "scan_mixed_regions_pack_empty", "mixed_text_regions", "generate_roi_crop_before_pack"
            else:
                status, reason, fix = "scan_has_text_pack_empty", "full_frame_reocr_instability", "use_scan_text_items_as_scan_observation_only"
        elif not linebox_available:
            status, reason, fix = "scan_linebox_missing", "require_linebox_trace", "require_linebox_trace"
        elif scan_has_text and pack_text:
            status, reason, fix = "scan_and_pack_consistent", None, "roi_ocr_then_evidence_pack"
        else:
            status, reason, fix = "scan_has_text_pack_empty", "frame_decode_difference", "use_best_frame_resample"

        consistency_rows.append(
            {
                "frame_id": frame_id,
                "frame_index": fi,
                "timestamp_ms": ts_ms,
                "scan_ocr_preview": original_preview,
                "scan_display_preview": display_preview,
                "scan_text_item_count": len(items),
                "linebox_available": linebox_available,
                "pack_exists": pack_exists,
                "pack_raw_ocr_text": pack_text,
                "pack_empty_text": pack_empty,
                "consistency_status": status,
                "mismatch_reason_candidate": reason,
                "recommended_fix": fix,
            }
        )

    linebox_trace_report = {
        "schema_version": "mixedvideo_ocr_scan_linebox_trace_report_v0",
        "video_id": P0_VIDEO_ID,
        "selected_frame_count": len(trace_frames),
        "linebox_available_count": sum(1 for t in trace_frames if t.get("linebox_available")),
        "linebox_missing_count": sum(1 for t in trace_frames if not t.get("linebox_available")),
        "frames": trace_frames,
    }

    plan_update_doc = {
        "schema_version": "mixedvideo_selected_frame_linebox_plan_update_v0",
        "selected_frame_count": len(plan_updates),
        "possible_mixed_regions_count": sum(1 for p in plan_updates if p.get("possible_mixed_regions")),
        "frames": plan_updates,
    }

    gate_policy = {
        "schema_version": "mixedvideo_ocr_source_quality_gate_policy_v0",
        "architecture_principle": "OCR failure may stem from input source quality; govern input before changing provider.",
        "quality_factors": [
            "view_angle_quality",
            "text_frontality",
            "occlusion_level",
            "motion_blur_level",
            "compression_artifact_level",
            "text_size_level",
            "distance_level",
            "lighting_quality",
            "contrast_score",
            "frame_stability",
            "crop_specificity",
            "mixed_text_region_risk",
            "full_frame_noise_risk",
            "logo_visual_symbol_likelihood",
            "public_facility_semantic_likelihood",
        ],
        "grades": {
            "SQ_A": {
                "source_quality_grade": "SQ_A",
                "criteria": "High quality: frontal, clear, low occlusion, single text region",
                "ocr_scan_allowed": True,
                "ocr_evidence_allowed": True,
                "requires_roi_crop": False,
                "requires_multiframe": False,
                "route_to_visual_symbol": False,
                "route_to_public_facility_semantic": False,
                "evidence_confidence_cap": 0.85,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            "SQ_B": {
                "source_quality_grade": "SQ_B",
                "criteria": "Usable but unstable; OCR allowed, evidence partial_or_uncertain",
                "ocr_scan_allowed": True,
                "ocr_evidence_allowed": True,
                "requires_roi_crop": False,
                "requires_multiframe": False,
                "route_to_visual_symbol": False,
                "route_to_public_facility_semantic": False,
                "evidence_confidence_cap": 0.65,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            "SQ_C": {
                "source_quality_grade": "SQ_C",
                "criteria": "Low quality; scan ok, evidence needs ROI crop or multiframe",
                "ocr_scan_allowed": True,
                "ocr_evidence_allowed": False,
                "requires_roi_crop": True,
                "requires_multiframe": True,
                "route_to_visual_symbol": False,
                "route_to_public_facility_semantic": False,
                "evidence_confidence_cap": 0.45,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            "SQ_D": {
                "source_quality_grade": "SQ_D",
                "criteria": "Logo/brand/graphic; route to VisualSymbolEvidence",
                "ocr_scan_allowed": True,
                "ocr_evidence_allowed": False,
                "requires_roi_crop": True,
                "requires_multiframe": False,
                "route_to_visual_symbol": True,
                "route_to_public_facility_semantic": False,
                "evidence_confidence_cap": 0.35,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            "SQ_E": {
                "source_quality_grade": "SQ_E",
                "criteria": "Unreadable or severely mixed; no OCR evidence",
                "ocr_scan_allowed": True,
                "ocr_evidence_allowed": False,
                "requires_roi_crop": True,
                "requires_multiframe": True,
                "route_to_visual_symbol": False,
                "route_to_public_facility_semantic": False,
                "evidence_confidence_cap": 0.0,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
        },
    }

    eval_matrix = {
        "schema_version": "mixedvideo_ocr_source_quality_evaluation_matrix_v0",
        "row_count": len(eval_rows),
        "rows": eval_rows,
    }

    consistency_report = {
        "schema_version": "mixedvideo_scan_vs_pack_consistency_report_v0",
        "row_count": len(consistency_rows),
        "scan_has_text_pack_empty_count": sum(1 for r in consistency_rows if r.get("consistency_status") == "scan_has_text_pack_empty"),
        "scan_has_text_pack_missing_count": sum(1 for r in consistency_rows if r.get("consistency_status") == "scan_has_text_pack_missing"),
        "scan_mixed_regions_pack_empty_count": sum(1 for r in consistency_rows if r.get("consistency_status") == "scan_mixed_regions_pack_empty"),
        "rows": consistency_rows,
    }

    full_frame_risk = {
        "schema_version": "mixedvideo_full_frame_ocr_risk_report_v0",
        "risks": {
            "multiple_text_regions_joined": True,
            "background_ads_pollution": True,
            "signboard_and_logo_mixed": True,
            "far_text_noise": True,
            "moving_frame_blur": True,
            "semantic_candidate_contamination": True,
            "no_reliable_entity_boundary": True,
        },
        "full_frame_ocr_allowed_for_scan": True,
        "full_frame_ocr_allowed_for_fact": False,
        "full_frame_ocr_allowed_for_world_model": False,
        "roi_crop_required_before_evidence": True,
        "semantic_candidate_from_full_frame_requires_review": True,
        "notes": "Full-frame OCR joins multiple signboards; not suitable as fact-grade evidence without ROI crop.",
    }

    roi_types = [
        ("signboard_roi", "multiple_signboards_or_mixed_preview", "signboard_ttl_policy_later"),
        ("bank_sign_roi", "bank_or_construction_bank_text", "source_validation_required"),
        ("brand_logo_roi", "HOKA_GAP_short_uppercase_logo", "visual_symbol_registry_later"),
        ("poster_notice_roi", "promo_poster_or_date_range", "poster_ttl_policy_later"),
        ("public_rule_roi", "no_smoking_or_exit_rule", "public_facility_semantic_first"),
        ("public_facility_sign_roi", "station_wayfinding_restroom", "public_facility_semantic_first"),
        ("doorplate_roi", "unit_floor_label", "source_validation_required"),
        ("traffic_sign_roi", "traffic_or_warning_sign", "warning_sign_governance"),
    ]
    roi_plan = {
        "schema_version": "mixedvideo_ocr_roi_crop_requirement_plan_v0",
        "roi_type_count": len(roi_types),
        "items": [
            {
                "roi_type": rt,
                "trigger_condition": cond,
                "required_before_ocr_evidence": True,
                "crop_quality_requirements": "minimal_occlusion, readable_text_frontality, stable_frame",
                "expected_output": "roi_cropped_ocr_text_items_with_bbox",
                "governance_route": route,
                "rejection_conditions": ["mixed_full_frame_only", "empty_crop", "logo_only_without_registry"],
            }
            for rt, cond, route in roi_types
        ],
    }

    scan_obs_policy = {
        "schema_version": "mixedvideo_scan_observation_vs_evidence_policy_v0",
        "scan_observation_allowed": True,
        "scan_observation_fact_status": "not_fact",
        "scan_observation_write_allowed": False,
        "roi_ocr_required_for_evidence_pack": True,
        "full_frame_scan_not_fact": True,
        "world_model_attach_from_scan_allowed": False,
        "ocr_preview_for_frame_selection_only": True,
        "linebox_trace_is_scan_observation_evidence": True,
        "low_quality_same_weight_as_high_quality_forbidden": True,
    }

    ep_recs = [
        ("ep_rec_001", "ocr_text_evidence_pack_v0", "scan_observation_ref", "Preserve scan layer when pack re-OCR empty", True),
        ("ep_rec_002", "ocr_text_evidence_pack_v0", "scan_text_items_ref", "Line-level scan items for traceability", True),
        ("ep_rec_003", "ocr_text_evidence_pack_v0", "source_quality_grade", "Gate low-quality inputs", True),
        ("ep_rec_004", "ocr_text_evidence_pack_v0", "scan_vs_pack_consistency_status", "Explain scan/pack mismatch", True),
        ("ep_rec_005", "ocr_text_evidence_pack_v0", "roi_ocr_priority", "ROI OCR pack outranks full-frame scan pack", True),
    ]
    ep_update = {
        "schema_version": "mixedvideo_ocr_evidence_pack_update_recommendation_v0",
        "recommendations": [
            {
                "recommendation_id": rid,
                "target_schema": schema,
                "field_to_add": field,
                "reason": reason,
                "required_for_next_phase": req,
                "write_allowed": False,
            }
            for rid, schema, field, reason, req in ep_recs
        ],
    }

    sem_guard = {
        "schema_version": "mixedvideo_semantic_candidate_guard_update_plan_v0",
        "rules": [
            "SQ_C_or_SQ_E: no strong entity candidate",
            "possible_mixed_regions: no single entity meaning",
            "high logo_visual_symbol_likelihood: route visual symbol",
            "high public_facility_semantic_likelihood: semantic-first",
            "scan_vs_pack mismatch: semantic_candidate uncertain",
            "full_frame ocr_preview only: no WorldModel attach candidate",
        ],
        "no_strong_entity_when_mixed_regions": True,
        "write_allowed": False,
    }

    grade_dist = Counter(r.get("source_quality_grade") for r in eval_rows)
    gate_dist = Counter(r.get("gate_decision") for r in eval_rows)
    metrics = {
        "schema_version": "mixedvideo_ocr_scan_linebox_quality_metrics_candidate_report_v0",
        "selected_frame_count": len(selected),
        "linebox_available_count": sum(1 for t in trace_frames if t.get("linebox_available")),
        "linebox_missing_count": sum(1 for t in trace_frames if not t.get("linebox_available")),
        "scan_has_text_pack_empty_count": consistency_report["scan_has_text_pack_empty_count"],
        "scan_has_text_pack_missing_count": consistency_report["scan_has_text_pack_missing_count"],
        "possible_mixed_regions_count": plan_update_doc["possible_mixed_regions_count"],
        "source_quality_grade_distribution": dict(grade_dist),
        "gate_decision_distribution": dict(gate_dist),
        "require_roi_crop_count": sum(1 for r in eval_rows if r.get("gate_decision") == "require_roi_crop"),
        "route_to_visual_symbol_count": sum(1 for r in eval_rows if r.get("gate_decision") == "route_to_visual_symbol"),
        "reject_as_unreadable_or_mixed_count": sum(
            1 for r in eval_rows if r.get("gate_decision") == "reject_as_unreadable_or_mixed"
        ),
        "accept_for_ocr_evidence_count": sum(1 for r in eval_rows if r.get("gate_decision") == "accept_for_ocr_evidence"),
        "no_write_boundary_pass_rate": 1.0,
        "can_feed_future_t1_collector": True,
        "benchmark_score_generated": False,
    }

    benchmark_link = {
        "schema_version": "mixedvideo_ocr_scan_linebox_quality_benchmark_link_report_v0",
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "can_feed_future_t1_collector": True,
        "current_phase_collects_t2": False,
        "ground_truth_available": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": "mixedvideo_ocr_scan_linebox_quality_system_health_link_report_v0",
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    boundary = {
        "schema_version": "mixedvideo_ocr_scan_linebox_quality_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "scan_trace_update_only": True,
        "source_quality_gate_only": True,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "production_readiness_claimed": False,
    }

    sim_sm = _read_json(sim / "simulation_summary.json") or {}
    sim_report = {
        "schema_version": "mixedvideo_ocr_scan_linebox_quality_simulation_context_report_v0",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "mixedvideo_ocr_scan_linebox_quality_non_claims_report_v0",
        "not_ocr_accuracy_evaluation": True,
        "not_benchmark": True,
        "not_provider_comparison": True,
        "not_fact_write": True,
        "not_world_model_attach": True,
        "not_scene_delta_readiness": True,
        "not_navigation": True,
        "not_production_ocr": True,
        "linebox_trace_is_scan_observation_only": True,
        "source_quality_grade_is_heuristic": True,
    }

    followups = {
        "schema_version": "mixedvideo_ocr_scan_linebox_quality_open_followups_v0",
        "items": [
            "ROI Crop Proposal for selected text-bearing frames",
            "ROI-to-OCR Reference for selected frame crops",
            "OCRRequest Gated Submission with source_quality_grade",
            "Evidence Pack Adapter v1 with scan_observation_ref",
            "Semantic Candidate guard v1",
            "VisualSymbolRegistry integration",
            "PublicFacility semantic-first extension",
            "Ground Truth Annotation Schema",
            "Benchmark T2 collector",
            "SystemHealth provider runtime dry-run",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": "mixedvideo_ocr_scan_linebox_quality_audit_v0",
        "mixedvideo_ocr_scan_linebox_trace_quality_gate_executed": True,
        "scan_trace_update_only": True,
        "source_quality_gate_only": True,
        "video_loaded": video_loaded,
        "ocr_scan_invoked": ocr_scan_invoked,
        "evidence_pack_updated": False,
        "semantic_candidate_updated": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "model_selection_claimed": False,
        "production_readiness_claimed": False,
    }

    summary = {
        "schema_version": "mixedvideo_ocr_scan_linebox_trace_quality_gate_summary_v0",
        "phase": PHASE_ID,
        "phase_scope": "scan_trace_and_source_quality_gate_only",
        "based_on_mixed_batch_smoke": batch.is_dir(),
        "based_on_readability_governance": Path(readability_governance_root).is_dir(),
        "based_on_evidence_pack_contract": Path(evidence_pack_contract_root).is_dir(),
        "linebox_trace_defined": True,
        "source_quality_gate_defined": True,
        "scan_vs_pack_consistency_defined": True,
        "p0_video_rescan_allowed": rescan_p0,
        "video_loaded": video_loaded,
        "ocr_scan_invoked": ocr_scan_invoked,
        "evidence_pack_updated": False,
        "semantic_candidate_updated": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": "GO" if not errs and len(selected) >= 10 else "CONDITIONAL_GO",
        "linebox_available_count": metrics["linebox_available_count"],
        "selected_frame_count": len(selected),
    }
    if errs:
        summary["errors"] = errs

    return (
        summary,
        linebox_trace_report,
        plan_update_doc,
        gate_policy,
        eval_matrix,
        consistency_report,
        full_frame_risk,
        roi_plan,
        scan_obs_policy,
        ep_update,
        sem_guard,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    )
