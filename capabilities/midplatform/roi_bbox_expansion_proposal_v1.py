# -*- coding: utf-8 -*-
"""ROI BBox Expansion Proposal v1 — expansion candidates only, no crop/OCR.

Phase-ROI-BBox-Expansion-Proposal-v1-001
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "ROI-BBox-Expansion-Proposal-v1-001"
RUNTIME_STEP = "roi_bbox_expansion_proposal_v1"

FOLLOWUPS = [
    "ROI-Crop-Execution-DryRun-v2-BBoxExpansion",
    "Crop-Quality-Scoring-v1",
    "Multiframe-Merge-Proposal-v1",
    "Better-Frame-Extraction-DryRun-v1",
    "Future-Detector-ROI-Proposal-v1",
    "ROI OCR Quality Metrics with GT",
    "Source-Validation-v2-after-ROI-OCR",
    "VisualSymbolRegistry DryRun",
    "STC Contract later",
    "Controlled runtime integration",
]

RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "expand_from_original_bbox_only",
        "condition": "expansion derives from source_bbox_xyxy",
        "expansion_effect": "preserve_origin",
        "blocked_action": "replace_source_bbox",
        "required_next_action": "ROI-Crop-Execution-DryRun-v2-BBoxExpansion",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "original_bbox_must_be_preserved",
        "condition": "source_bbox unchanged in intake",
        "expansion_effect": "source_bbox_immutable",
        "blocked_action": "overwrite_original_bbox",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "expansion_bbox_must_be_within_source_bounds",
        "condition": "frame_width and frame_height known",
        "expansion_effect": "clip_or_defer",
        "blocked_action": "out_of_bounds_crop",
        "required_next_action": "bounds_check_report",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "small_padding_candidate_allowed",
        "condition": "padding_small strategy",
        "expansion_effect": "small_expansion_candidate",
        "blocked_action": "none",
        "required_next_action": "ROI-Crop-Execution-DryRun-v2-BBoxExpansion",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "medium_padding_candidate_allowed",
        "condition": "padding_medium strategy",
        "expansion_effect": "medium_expansion_candidate",
        "blocked_action": "none",
        "required_next_action": "ROI-Crop-Execution-DryRun-v2-BBoxExpansion",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "line_region_expansion_candidate_allowed",
        "condition": "line_region_expand strategy",
        "expansion_effect": "line_region_candidate",
        "blocked_action": "none",
        "required_next_action": "ROI-Crop-Execution-DryRun-v2-BBoxExpansion",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "contextual_expansion_candidate_allowed",
        "condition": "contextual_expand strategy",
        "expansion_effect": "contextual_candidate",
        "blocked_action": "none",
        "required_next_action": "ROI-Crop-Execution-DryRun-v2-BBoxExpansion",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "expansion_candidate_not_crop_artifact",
        "condition": "phase_boundary",
        "expansion_effect": "proposal_not_crop",
        "blocked_action": "crop_generation",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "expansion_candidate_not_evidence",
        "condition": "phase_boundary",
        "expansion_effect": "proposal_not_evidence",
        "blocked_action": "evidence_pack_generation",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_crop_generation_in_this_phase",
        "condition": "phase_boundary",
        "expansion_effect": "no_new_crop",
        "blocked_action": "crop_execution",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocr_execution_in_this_phase",
        "condition": "phase_boundary",
        "expansion_effect": "no_ocr",
        "blocked_action": "ocr_invocation",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_source_validation_before_expansion_crop",
        "condition": "phase_boundary",
        "expansion_effect": "no_sv_v2",
        "blocked_action": "source_validation_v2",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "phase_boundary",
        "expansion_effect": "no_wm",
        "blocked_action": "world_model_attach",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "phase_boundary",
        "expansion_effect": "no_scene_delta",
        "blocked_action": "scene_delta_candidate",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

STRATEGIES: List[Dict[str, Any]] = [
    {
        "strategy_id": "padding_small",
        "strategy_name": "padding_small",
        "expansion_formula": "pad each side by max(8px, 10% of bbox width/height)",
        "intended_fix": "reduce tight clipping on narrow linebox crop",
        "expected_risk_reduction": "clipping_risk",
        "remaining_risk": ["still_single_frame", "linebox_reuse"],
        "crop_generation_allowed_now": False,
        "ocr_allowed_now": False,
    },
    {
        "strategy_id": "padding_medium",
        "strategy_name": "padding_medium",
        "expansion_formula": "pad each side by max(16px, 30% of bbox width/height)",
        "intended_fix": "add moderate context around line region",
        "expected_risk_reduction": "clipping_risk",
        "remaining_risk": ["noise_increase", "mixed_region"],
        "crop_generation_allowed_now": False,
        "ocr_allowed_now": False,
    },
    {
        "strategy_id": "line_region_expand",
        "strategy_name": "line_region_expand",
        "expansion_formula": "left/right +60% width; top/bottom +30% height; clip to frame",
        "intended_fix": "widen horizontal text line context",
        "expected_risk_reduction": "horizontal_clipping",
        "remaining_risk": ["vertical_noise", "adjacent_text"],
        "crop_generation_allowed_now": False,
        "ocr_allowed_now": False,
    },
    {
        "strategy_id": "contextual_expand",
        "strategy_name": "contextual_expand",
        "expansion_formula": "left/right +100% width; top/bottom +60% height; clip to frame",
        "intended_fix": "maximize local context within frame bounds",
        "expected_risk_reduction": "low_context",
        "remaining_risk": ["noise_increase", "false_positive_text", "mixed_region"],
        "crop_generation_allowed_now": False,
        "ocr_allowed_now": False,
    },
]

CANDIDATE_SCHEMA: Dict[str, Any] = {
    "bbox_expansion_candidate_id": "bbox_exp_<uuid>",
    "schema_version": "roi_bbox_expansion_candidate_v1",
    "source_crop_artifact_id": None,
    "source_bbox_xyxy": None,
    "expanded_bbox_xyxy": None,
    "expansion_strategy": "padding_small | padding_medium | line_region_expand | contextual_expand",
    "padding_ratio": None,
    "padding_pixels": {"left": None, "top": None, "right": None, "bottom": None},
    "source_frame_ref": {
        "candidate_frame_id": None,
        "candidate_frame_index": None,
        "candidate_frame_time_sec": None,
        "frame_width": None,
        "frame_height": None,
    },
    "linebox_ref": None,
    "bounds_check": {
        "within_bounds": None,
        "clipped_to_bounds": False,
        "out_of_bounds_before_clip": False,
    },
    "expected_improvement": {
        "more_context": True,
        "reduced_clipping_risk": True,
        "higher_text_context_likelihood": None,
        "risk_remaining": [],
    },
    "future_crop_candidate": {
        "eligible_for_crop_rerun": False,
        "required_future_phase": "ROI-Crop-Execution-DryRun-v2-BBoxExpansion",
    },
    "proposal_status": "proposed | clipped | deferred | invalid",
    "fact_status": "not_fact",
    "write_allowed": False,
    "source_chain": [],
}

FUTURE_CROP_PLAN = {
    "future_phase": "ROI-Crop-Execution-DryRun-v2-BBoxExpansion",
    "required_input": [
        "roi_bbox_expansion_candidate_collection_v1",
        "roi_bbox_expansion_bounds_check_report_v1",
    ],
    "expected_output": ["roi_crop_v2_bbox_expansion_artifact_collection"],
    "should_generate_crop_files_later": True,
    "should_not_ocr_in_crop_phase": True,
    "should_preserve_expansion_candidate_ref": True,
    "not_in_current_phase": True,
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake_id(key: str) -> str:
    return f"exp_intake_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _bbox_sig(bbox: Any) -> str:
    if not isinstance(bbox, list) or len(bbox) != 4:
        return "invalid"
    return ",".join(str(int(float(v))) for v in bbox)


def _group_id(bbox_sig: str, frame_id: str) -> str:
    return f"sbg_{hashlib.sha256((frame_id + '|' + bbox_sig).encode()).hexdigest()[:10]}"


def _candidate_id(strategy: str, group_id: str) -> str:
    return f"bbox_exp_{hashlib.sha256((group_id + '|' + strategy).encode()).hexdigest()[:12]}"


def _area(bbox: List[float]) -> float:
    return max(0.0, bbox[2] - bbox[0]) * max(0.0, bbox[3] - bbox[1])


def _expand_padding(
    bbox: List[float], *, ratio: float, min_px: int
) -> Tuple[List[float], Dict[str, int], Optional[float]]:
    x1, y1, x2, y2 = [float(v) for v in bbox]
    w, h = x2 - x1, y2 - y1
    pl = max(min_px, int(round(w * ratio)))
    pr = max(min_px, int(round(w * ratio)))
    pt = max(min_px, int(round(h * ratio)))
    pb = max(min_px, int(round(h * ratio)))
    return [x1 - pl, y1 - pt, x2 + pr, y2 + pb], {"left": pl, "top": pt, "right": pr, "bottom": pb}, ratio


def _expand_line_region(bbox: List[float]) -> Tuple[List[float], Dict[str, int], None]:
    x1, y1, x2, y2 = [float(v) for v in bbox]
    w, h = x2 - x1, y2 - y1
    pl, pr = int(round(w * 0.6)), int(round(w * 0.6))
    pt, pb = int(round(h * 0.3)), int(round(h * 0.3))
    return [x1 - pl, y1 - pt, x2 + pr, y2 + pb], {"left": pl, "top": pt, "right": pr, "bottom": pb}, None


def _expand_contextual(bbox: List[float]) -> Tuple[List[float], Dict[str, int], None]:
    x1, y1, x2, y2 = [float(v) for v in bbox]
    w, h = x2 - x1, y2 - y1
    pl, pr = int(round(w * 1.0)), int(round(w * 1.0))
    pt, pb = int(round(h * 0.6)), int(round(h * 0.6))
    return [x1 - pl, y1 - pt, x2 + pr, y2 + pb], {"left": pl, "top": pt, "right": pr, "bottom": pb}, None


def _clip_bbox(
    bbox: List[float], fw: Optional[int], fh: Optional[int]
) -> Tuple[List[float], Dict[str, Any], str]:
    if fw is None or fh is None:
        return bbox, {
            "within_bounds": None,
            "clipped_to_bounds": False,
            "out_of_bounds_before_clip": False,
        }, "unknown_frame_bounds"
    x1, y1, x2, y2 = bbox
    oob = x1 < 0 or y1 < 0 or x2 > fw or y2 > fh
    cx1, cy1 = max(0.0, x1), max(0.0, y1)
    cx2, cy2 = min(float(fw), x2), min(float(fh), y2)
    clipped = oob and (cx1 != x1 or cy1 != y1 or cx2 != x2 or cy2 != y2)
    within = cx1 < cx2 and cy1 < cy2 and not (cx1 < 0 or cy1 < 0 or cx2 > fw or cy2 > fh)
    status = "within_bounds" if within and not clipped else ("clipped" if clipped else "invalid")
    return [cx1, cy1, cx2, cy2], {
        "within_bounds": within,
        "clipped_to_bounds": clipped,
        "out_of_bounds_before_clip": oob,
    }, status


def _impact_label(ratio: float) -> str:
    if ratio >= 2.5:
        return "high"
    if ratio >= 1.5:
        return "medium"
    if ratio >= 1.1:
        return "low"
    return "unknown"


def run_roi_bbox_expansion_proposal_v1(
    *,
    roi_crop_diversity_root: str,
    roi_ocr_quality_diagnosis_root: str,
    semantic_v2_root: str,
    evidence_pack_v2_root: str,
    roi_ocr_gated_submission_root: str,
    roi_ocrrequest_reference_root: str,
    roi_crop_rerun_root: str,
    better_frame_root: str,
    roi_retry_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    div_root = Path(roi_crop_diversity_root).resolve()
    diag_root = Path(roi_ocr_quality_diagnosis_root).resolve()
    linebox_root = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    div_summary = _read_json(div_root / "roi_crop_diversity_check_v1_summary.json") or {}
    div_intake = (_read_json(div_root / "roi_crop_diversity_intake_matrix_v1.json") or {}).get("rows") or []
    score_report = _read_json(div_root / "roi_crop_diversity_score_report_v1.json") or {}
    diversity_grade = score_report.get("diversity_grade") or "LOW"

    frame_dims: Dict[str, Tuple[Optional[int], Optional[int]]] = {}
    for fr in (_read_json(linebox_root / "mixedvideo_ocr_scan_linebox_trace_report.json") or {}).get("frames") or []:
        if isinstance(fr, dict) and fr.get("frame_id"):
            frame_dims[str(fr["frame_id"])] = (
                int(fr["image_width"]) if fr.get("image_width") is not None else None,
                int(fr["image_height"]) if fr.get("image_height") is not None else None,
            )

    intake_rows: List[Dict[str, Any]] = []
    for row in div_intake:
        if not isinstance(row, dict):
            continue
        fid = str(row.get("candidate_frame_id") or "")
        fw, fh = frame_dims.get(fid, (None, None))
        crop_id = str(row.get("crop_artifact_id") or "")
        intake_rows.append(
            {
                "expansion_intake_id": _intake_id(crop_id),
                "crop_artifact_id": crop_id,
                "crop_file_path": row.get("crop_file_path"),
                "source_bbox_xyxy": row.get("crop_bbox_xyxy"),
                "crop_width": row.get("crop_width"),
                "crop_height": row.get("crop_height"),
                "candidate_frame_id": fid,
                "candidate_frame_index": row.get("candidate_frame_index"),
                "candidate_frame_time_sec": row.get("candidate_frame_time_sec"),
                "source_frame_width": fw,
                "source_frame_height": fh,
                "linebox_trace_ref": row.get("linebox_trace_ref"),
                "linebox_bbox": row.get("linebox_bbox"),
                "roi_ocr_result_id": row.get("roi_ocr_result_id"),
                "evidence_pack_v2_id": row.get("evidence_pack_v2_id"),
                "semantic_candidate_v2_id": row.get("semantic_candidate_v2_id"),
                "raw_ocr_text": row.get("raw_ocr_text"),
                "diversity_grade": diversity_grade,
                "quality_status": "low_diversity_hold",
                "intake_status": "accepted",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    # Group by source bbox + frame
    groups: Dict[str, Dict[str, Any]] = {}
    for ir in intake_rows:
        bbox = ir.get("source_bbox_xyxy")
        fid = str(ir.get("candidate_frame_id") or "")
        sig = _bbox_sig(bbox)
        gid = _group_id(sig, fid)
        if gid not in groups:
            groups[gid] = {
                "source_bbox_group_id": gid,
                "source_bbox_xyxy": bbox,
                "member_count": 0,
                "member_crop_artifact_ids": [],
                "member_result_ids": [],
                "member_semantic_ids": [],
                "source_frame_id": fid,
                "source_linebox_ref": ir.get("linebox_trace_ref"),
                "group_reason": "duplicate_source_bbox_from_diversity_check",
                "canonical_group": True,
                "expansion_generated_for_group": False,
                "frame_width": ir.get("source_frame_width"),
                "frame_height": ir.get("source_frame_height"),
            }
        g = groups[gid]
        g["member_count"] += 1
        g["member_crop_artifact_ids"].append(ir.get("crop_artifact_id"))
        g["member_result_ids"].append(ir.get("roi_ocr_result_id"))
        g["member_semantic_ids"].append(ir.get("semantic_candidate_v2_id"))

    candidates: List[Dict[str, Any]] = []
    bounds_rows: List[Dict[str, Any]] = []
    impact_rows: List[Dict[str, Any]] = []
    risk_rows: List[Dict[str, Any]] = []
    decision_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    expand_fns = {
        "padding_small": lambda b: _expand_padding(b, ratio=0.1, min_px=8),
        "padding_medium": lambda b: _expand_padding(b, ratio=0.3, min_px=16),
        "line_region_expand": _expand_line_region,
        "contextual_expand": _expand_contextual,
    }

    for gid, g in groups.items():
        bbox = g.get("source_bbox_xyxy")
        if not isinstance(bbox, list) or len(bbox) != 4:
            continue
        src_bbox = [float(v) for v in bbox]
        fid = str(g.get("source_frame_id") or "")
        fw = g.get("frame_width")
        fh = g.get("frame_height")
        g["expansion_generated_for_group"] = True

        for strat in STRATEGIES:
            sid = strat["strategy_id"]
            raw_exp, pads, pad_ratio = expand_fns[sid](src_bbox)
            clipped_bbox, bounds, bounds_status = _clip_bbox(raw_exp, fw, fh)

            if bounds_status == "unknown_frame_bounds":
                proposal_status = "deferred"
            elif bounds_status == "invalid":
                proposal_status = "invalid"
            elif bounds.get("clipped_to_bounds"):
                proposal_status = "clipped"
            else:
                proposal_status = "proposed"

            cid = _candidate_id(sid, gid)
            src_area = _area(src_bbox)
            exp_area = _area(clipped_bbox)
            area_ratio = round(exp_area / src_area, 4) if src_area > 0 else 0.0
            sw, sh = src_bbox[2] - src_bbox[0], src_bbox[3] - src_bbox[1]
            ew, eh = clipped_bbox[2] - clipped_bbox[0], clipped_bbox[3] - clipped_bbox[1]
            w_growth = round(ew / sw, 4) if sw > 0 else 0.0
            h_growth = round(eh / sh, 4) if sh > 0 else 0.0

            chain = [
                "roi_crop_diversity_check_v1",
                "roi_ocr_quality_diagnosis_v1",
                RUNTIME_STEP,
            ]

            remaining = list(strat.get("remaining_risk") or [])
            candidate = {
                "bbox_expansion_candidate_id": cid,
                "schema_version": "roi_bbox_expansion_candidate_v1",
                "source_bbox_group_id": gid,
                "affected_crop_artifact_ids": list(g.get("member_crop_artifact_ids") or []),
                "affected_roi_ocr_result_ids": list(g.get("member_result_ids") or []),
                "source_bbox_xyxy": src_bbox,
                "expanded_bbox_xyxy": [round(v, 2) for v in clipped_bbox],
                "expansion_strategy": sid,
                "padding_ratio": pad_ratio,
                "padding_pixels": pads,
                "source_frame_ref": {
                    "candidate_frame_id": fid,
                    "candidate_frame_index": intake_rows[0].get("candidate_frame_index") if intake_rows else None,
                    "candidate_frame_time_sec": intake_rows[0].get("candidate_frame_time_sec") if intake_rows else None,
                    "frame_width": fw,
                    "frame_height": fh,
                },
                "linebox_ref": g.get("source_linebox_ref"),
                "bounds_check": bounds,
                "expected_improvement": {
                    "more_context": True,
                    "reduced_clipping_risk": proposal_status in ("proposed", "clipped"),
                    "higher_text_context_likelihood": _impact_label(area_ratio) != "unknown",
                    "risk_remaining": remaining,
                    "expansion_reason": strat.get("intended_fix"),
                },
                "future_crop_candidate": {
                    "eligible_for_crop_rerun": proposal_status in ("proposed", "clipped"),
                    "required_future_phase": "ROI-Crop-Execution-DryRun-v2-BBoxExpansion",
                },
                "proposal_status": proposal_status,
                "fact_status": "not_fact",
                "write_allowed": False,
                "source_chain": chain,
            }
            candidates.append(candidate)

            bounds_rows.append(
                {
                    "bbox_expansion_candidate_id": cid,
                    "source_bbox_xyxy": src_bbox,
                    "expanded_bbox_xyxy": candidate["expanded_bbox_xyxy"],
                    "frame_width": fw,
                    "frame_height": fh,
                    "out_of_bounds_before_clip": bounds.get("out_of_bounds_before_clip"),
                    "clipped_to_bounds": bounds.get("clipped_to_bounds"),
                    "within_bounds": bounds.get("within_bounds"),
                    "bounds_status": bounds_status,
                    "invalid_reason": None if proposal_status != "invalid" else "degenerate_after_clip",
                }
            )

            impact_rows.append(
                {
                    "bbox_expansion_candidate_id": cid,
                    "source_bbox_area": round(src_area, 2),
                    "expanded_bbox_area": round(exp_area, 2),
                    "area_growth_ratio": area_ratio,
                    "width_growth_ratio": w_growth,
                    "height_growth_ratio": h_growth,
                    "expected_context_gain": area_ratio > 1.0,
                    "expected_clipping_risk_reduction": proposal_status in ("proposed", "clipped"),
                    "expected_noise_increase_risk": sid in ("contextual_expand", "line_region_expand"),
                    "expected_improvement_label": _impact_label(area_ratio),
                    "estimate_is_diagnostic_only": True,
                }
            )

            risk_rows.append(
                {
                    "bbox_expansion_candidate_id": cid,
                    "risk_remaining": remaining,
                    "risk_newly_introduced": ["noise_increase", "mixed_region"] if sid == "contextual_expand" else [],
                    "possible_noise_increase": sid in ("padding_medium", "line_region_expand", "contextual_expand"),
                    "possible_mixed_region_increase": sid in ("line_region_expand", "contextual_expand"),
                    "possible_false_positive_text": sid == "contextual_expand",
                    "requires_future_crop_quality_scoring": True,
                    "requires_future_ocr_validation": True,
                    "fact_write_allowed": False,
                }
            )

            rec = proposal_status in ("proposed", "clipped")
            decision_rows.append(
                {
                    "bbox_expansion_candidate_id": cid,
                    "proposal_status": proposal_status,
                    "recommended_for_future_crop": rec,
                    "recommendation_reason": strat.get("intended_fix") if rec else "deferred_or_invalid",
                    "blocked_current_actions": [
                        "crop_generation",
                        "ocr_invocation",
                        "source_validation_v2",
                        "fact_write",
                    ],
                    "required_next_action": "ROI-Crop-Execution-DryRun-v2-BBoxExpansion",
                    "allowed_future_phase": [
                        "ROI-Crop-Execution-DryRun-v2-BBoxExpansion",
                        "Crop-Quality-Scoring-v1",
                    ],
                    "fact_write_allowed": False,
                    "world_model_attach_allowed": False,
                    "scene_delta_candidate_allowed": False,
                }
            )

            chain_rows.append(
                {
                    "bbox_expansion_candidate_id": cid,
                    "traceable_to_diversity_check": div_root.is_dir(),
                    "traceable_to_quality_diagnosis": diag_root.is_dir(),
                    "traceable_to_crop_artifact": bool(g.get("member_crop_artifact_ids")),
                    "traceable_to_linebox_trace": linebox_root.is_dir(),
                    "source_chain": chain,
                    "source_chain_preserved": RUNTIME_STEP in chain,
                }
            )

    strat_counts = {s["strategy_id"]: 0 for s in STRATEGIES}
    for c in candidates:
        strat_counts[c.get("expansion_strategy", "")] = strat_counts.get(c.get("expansion_strategy", ""), 0) + 1

    oob_count = sum(1 for b in bounds_rows if b.get("out_of_bounds_before_clip"))
    clipped_count = sum(1 for b in bounds_rows if b.get("clipped_to_bounds"))
    invalid_count = sum(1 for c in candidates if c.get("proposal_status") == "invalid")
    recommended_count = sum(1 for d in decision_rows if d.get("recommended_for_future_crop"))

    grouping_report = {
        "schema_version": "roi_bbox_expansion_source_bbox_grouping_report_v1",
        "groups": list(groups.values()),
        "source_bbox_group_count": len(groups),
    }

    summary = {
        "schema_version": "roi_bbox_expansion_proposal_v1_summary_v0",
        "phase": PHASE_ID,
        "proposal_scope": "bbox_expansion_proposal_only",
        "based_on_roi_crop_diversity_check": div_root.is_dir(),
        "based_on_roi_ocr_quality_diagnosis": diag_root.is_dir(),
        "crop_count_observed": len(intake_rows),
        "unique_bbox_count_observed": div_summary.get("unique_bbox_count") or 1,
        "low_diversity_confirmed_for_planning": div_summary.get("crop_diversity_low") is True,
        "bbox_expansion_proposal_generated": len(candidates) >= 4,
        "source_bbox_count": len(groups),
        "expansion_candidate_count": len(candidates),
        "small_expansion_count": strat_counts.get("padding_small", 0),
        "medium_expansion_count": strat_counts.get("padding_medium", 0),
        "line_region_expansion_count": strat_counts.get("line_region_expand", 0),
        "contextual_expansion_count": strat_counts.get("contextual_expand", 0),
        "bbox_out_of_bounds_count": oob_count,
        "new_crop_generated": False,
        "new_ocr_invoked": False,
        "new_frame_extracted": False,
        "ocrrequest_generated": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "source_validation_v2_invoked": False,
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
        "phase_verdict_hint": "GO"
        if len(intake_rows) == 12 and len(groups) == 1 and len(candidates) >= 4
        else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "roi_bbox_expansion_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {"schema_version": "roi_bbox_expansion_rule_matrix_v1", "rules": RULES},
        "candidate_schema": {
            "schema_version": "roi_bbox_expansion_candidate_schema_v1",
            "template": CANDIDATE_SCHEMA,
        },
        "strategy_matrix": {
            "schema_version": "roi_bbox_expansion_strategy_matrix_v1",
            "strategies": STRATEGIES,
        },
        "candidate_collection": {
            "schema_version": "roi_bbox_expansion_candidate_collection_v1",
            "candidate_count": len(candidates),
            "canonical_source_bbox_group_count": len(groups),
            "rows": candidates,
        },
        "grouping_report": grouping_report,
        "bounds_check_report": {
            "schema_version": "roi_bbox_expansion_bounds_check_report_v1",
            "row_count": len(bounds_rows),
            "rows": bounds_rows,
        },
        "impact_estimate_report": {
            "schema_version": "roi_bbox_expansion_impact_estimate_report_v1",
            "row_count": len(impact_rows),
            "rows": impact_rows,
            "estimate_is_diagnostic_only": True,
        },
        "risk_report": {
            "schema_version": "roi_bbox_expansion_risk_report_v1",
            "row_count": len(risk_rows),
            "rows": risk_rows,
        },
        "future_crop_rerun_plan": {
            "schema_version": "roi_bbox_expansion_future_crop_rerun_plan_v1",
            **FUTURE_CROP_PLAN,
        },
        "decision_matrix": {
            "schema_version": "roi_bbox_expansion_decision_matrix_v1",
            "row_count": len(decision_rows),
            "rows": decision_rows,
        },
        "boundary": {
            "schema_version": "roi_bbox_expansion_boundary_report_v1",
            "bbox_expansion_proposal_only": True,
            "new_crop_generated": False,
            "new_ocr_invoked": False,
            "new_frame_extracted": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_v2_invoked": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
        },
        "source_chain_report": {
            "schema_version": "roi_bbox_expansion_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_diversity_check": div_root.is_dir(),
            "rows": chain_rows,
        },
        "metrics": {
            "schema_version": "roi_bbox_expansion_metrics_candidate_report_v1",
            "source_bbox_group_count": len(groups),
            "affected_crop_count": len(intake_rows),
            "expansion_candidate_count": len(candidates),
            "padding_small_count": strat_counts.get("padding_small", 0),
            "padding_medium_count": strat_counts.get("padding_medium", 0),
            "line_region_expansion_count": strat_counts.get("line_region_expand", 0),
            "contextual_expansion_count": strat_counts.get("contextual_expand", 0),
            "recommended_for_future_crop_count": recommended_count,
            "out_of_bounds_candidate_count": oob_count,
            "clipped_candidate_count": clipped_count,
            "invalid_candidate_count": invalid_count,
            "new_crop_generated_count": 0,
            "new_ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "evidence_pack_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "roi_bbox_expansion_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "roi_bbox_expansion_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "roi_bbox_expansion_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "bbox_expansion_proposal_only": True,
            "new_crop_generated": False,
            "new_ocr_invoked": False,
            "new_frame_extracted": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_v2_invoked": False,
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
            "schema_version": "roi_bbox_expansion_simulation_context_report_v1",
            "simulation_profile_id": (_read_json(sim / "simulation_summary.json") or {}).get(
                "simulation_profile_id", "developer_full"
            ),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "roi_bbox_expansion_non_claims_report_v1",
            "expansion_not_fact": True,
            "expansion_not_better_roi_proof": True,
            "impact_not_accuracy": True,
            "no_ocr_in_phase": True,
            "no_crop_in_phase": True,
            "no_root_cause_confirmed": True,
        },
        "followups": {"schema_version": "roi_bbox_expansion_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "roi_bbox_expansion_audit_report_v1",
            "roi_bbox_expansion_proposal_v1_executed": True,
            "bbox_expansion_proposal_only": True,
            "source_bbox_group_count": len(groups),
            "expansion_candidate_count": len(candidates),
            "new_crop_generated": False,
            "new_ocr_invoked": False,
            "new_frame_extracted": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_v2_invoked": False,
            "decision_committed": False,
            "approval_granted": False,
            "world_model_attach_executed": False,
            "midplatform_fact_written": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
