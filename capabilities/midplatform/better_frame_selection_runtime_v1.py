# -*- coding: utf-8 -*-
"""Better Frame Selection Runtime v1 — selection planning only, no decode/crop/OCR.

Phase-Better-Frame-Selection-Runtime-v1-001
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Better-Frame-Selection-Runtime-v1-001"
RUNTIME_STEP = "better_frame_selection_runtime_v1"

SQ_RANK = {"SQ_A": 5, "SQ_B": 4, "SQ_C": 3, "SQ_D": 2, "SQ_E": 1, None: 0}

SELECTION_RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "sq_e_requires_better_source_before_crop",
        "condition": "source_quality_grade==SQ_E",
        "selection_effect": "block_crop_ready",
        "proposed_action": "better_source_or_better_frame_planning",
        "blocked_action": ["immediate_crop", "ocr_request"],
        "required_future_phase": "ROI-Crop-Execution-DryRun-v1-rerun",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "better_frame_required_before_roi_crop",
        "condition": "proposal_type==better_frame_required",
        "selection_effect": "plan_better_frame",
        "proposed_action": "select_existing_or_require_neighbor",
        "blocked_action": ["force_crop"],
        "required_future_phase": "Better-Frame-Extraction-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "null_bbox_requires_future_detector_or_better_frame",
        "condition": "bbox_null",
        "selection_effect": "defer_bbox",
        "proposed_action": "future_detector_or_multiframe",
        "blocked_action": ["fabricate_bbox"],
        "required_future_phase": "Future-Detector-ROI-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "mixed_region_requires_less_mixed_frame",
        "condition": "mixed_region_split",
        "selection_effect": "prefer_lower_mixed_risk_frame",
        "proposed_action": "select_less_mixed_existing_frame",
        "blocked_action": ["semantic_join"],
        "required_future_phase": "ROI-Crop-Execution-DryRun-v1-rerun",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "linebox_exists_but_low_quality_requires_better_frame",
        "condition": "linebox_available and SQ_E",
        "selection_effect": "existing_or_neighbor",
        "proposed_action": "better_frame_from_pool",
        "blocked_action": ["crop_ready_now"],
        "required_future_phase": "Better-Frame-Extraction-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "scan_only_requires_multiframe_or_roi_refinement",
        "condition": "scan_observation_only",
        "selection_effect": "multiframe_or_roi",
        "proposed_action": "multiframe_merge_plan",
        "blocked_action": ["single_frame_fact"],
        "required_future_phase": "Multiframe-Merge-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_new_frame_extraction_in_this_phase",
        "condition": "always",
        "selection_effect": "planning_only",
        "proposed_action": "no_extract",
        "blocked_action": ["new_frame_extracted"],
        "required_future_phase": "Better-Frame-Extraction-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_video_decoding_in_this_phase",
        "condition": "always",
        "selection_effect": "planning_only",
        "proposed_action": "no_decode",
        "blocked_action": ["new_video_decoded"],
        "required_future_phase": "Better-Frame-Extraction-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_crop_execution_in_this_phase",
        "condition": "always",
        "selection_effect": "planning_only",
        "proposed_action": "no_crop",
        "blocked_action": ["roi_crop_executed"],
        "required_future_phase": "ROI-Crop-Execution-DryRun-v1-rerun",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocr_request_generation_in_this_phase",
        "condition": "always",
        "selection_effect": "planning_only",
        "proposed_action": "no_ocr_request",
        "blocked_action": ["ocr_request_generated"],
        "required_future_phase": "ROI-to-OCRRequest-Reference-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocr_execution_in_this_phase",
        "condition": "always",
        "selection_effect": "planning_only",
        "proposed_action": "no_ocr",
        "blocked_action": ["ocr_invoked", "provider_invoked"],
        "required_future_phase": "controlled_runtime",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "always",
        "selection_effect": "planning_only",
        "proposed_action": "no_wm",
        "blocked_action": ["world_model_attach"],
        "required_future_phase": "WorldModel-attach-later",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

FUTURE_PHASES = [
    {
        "future_phase": "Better-Frame-Extraction-DryRun-v1",
        "purpose": "Extract neighboring frames when pool insufficient",
        "required_input": ["better_frame_candidate_collection_v1"],
        "expected_output": ["extracted_frame_refs"],
        "boundary": "extract_only_no_ocr",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Multiframe-Merge-Proposal-v1",
        "purpose": "Merge multi-frame scan for SQ_C video paths",
        "required_input": ["better_frame_neighboring_multiframe_requirement_report_v1"],
        "expected_output": ["multiframe_merge_proposal"],
        "boundary": "proposal_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Future-Detector-ROI-Proposal-v1",
        "purpose": "Detector-based ROI for null-bbox posters",
        "required_input": ["better_frame_candidate_collection_v1"],
        "expected_output": ["detector_roi_proposals"],
        "boundary": "proposal_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "ROI-Crop-Execution-DryRun-v1-rerun",
        "purpose": "Crop from better frame candidates",
        "required_input": ["better_frame_future_roi_crop_readiness_matrix_v1"],
        "expected_output": ["roi_crop_artifact_collection_v1"],
        "boundary": "crop_only_no_ocr",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "ROI-to-OCRRequest-Reference-v1",
        "purpose": "OCRRequest reference from crop artifacts",
        "required_input": ["ROI-Crop-Execution-DryRun-v1-rerun"],
        "expected_output": ["ocr_request_reference_plan"],
        "boundary": "reference_only",
        "not_in_current_phase": True,
    },
]

FOLLOWUPS = [
    "Better-Frame-Extraction-DryRun-v1",
    "Multiframe-Merge-Proposal-v1",
    "Future-Detector-ROI-Proposal-v1",
    "ROI-Crop-Execution-DryRun-v1-rerun",
    "ROI-to-OCRRequest-Reference-v1",
    "OCRRequest Gated Submission from ROI v1",
    "Evidence Pack Adapter v2 ROIRef",
    "Semantic Candidate v2 ROIAware",
    "VisualSymbolRegistry DryRun",
    "STC Contract later",
    "Controlled runtime integration",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _bfid(key: str) -> str:
    return f"bf_{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def _frame_id_from_index(video_id: str, frame_index: int) -> str:
    return f"{video_id}_f{frame_index:06d}"


def _parse_frame_index(frame_id: str) -> Optional[int]:
    m = re.search(r"_f(\d+)$", frame_id or "")
    return int(m.group(1)) if m else None


def _parse_video_id(frame_id: str) -> Optional[str]:
    m = re.match(r"^(.+)_f\d+$", frame_id or "")
    return m.group(1) if m else None


def _vc_from_chain(chain: List[str]) -> Optional[str]:
    for c in chain or []:
        if c.startswith("validation:sv_"):
            return c.split(":", 1)[1]
    return None


def _reasons_for_item(
    *,
    defer_reason: Optional[str],
    ptype: str,
    sq: Optional[str],
    has_bbox: bool,
    has_linebox: bool,
    mixed: bool,
) -> Tuple[List[str], str]:
    reasons: List[str] = []
    if sq == "SQ_E":
        reasons.append("current_frame_sq_e")
    if defer_reason == "null_bbox_deferred" or not has_bbox:
        reasons.append("current_frame_bbox_missing")
    if mixed or ptype == "mixed_region_split":
        reasons.append("current_frame_mixed_regions")
    if ptype == "better_frame_required":
        reasons.append("current_frame_low_quality")
    if has_linebox and sq == "SQ_E":
        reasons.append("linebox_available_but_not_crop_ready")
    if ptype == "future_detector_required":
        reasons.append("future_detector_needed")
    if sq == "SQ_C" and not has_linebox:
        reasons.append("multiframe_needed")
    if not reasons:
        reasons.append("current_frame_low_quality")
    dominant = reasons[0]
    return reasons, dominant


def _pick_better_frame(
    current_frame_id: Optional[str],
    quality_by_index: Dict[int, Dict[str, Any]],
    video_id: str,
) -> Optional[Dict[str, Any]]:
    cur_idx = _parse_frame_index(current_frame_id or "") if current_frame_id else None
    cur_sq = SQ_RANK.get((quality_by_index.get(cur_idx or -1) or {}).get("source_quality_grade"), 0)
    best: Optional[Dict[str, Any]] = None
    best_score = cur_sq
    for idx, row in quality_by_index.items():
        sq = SQ_RANK.get(row.get("source_quality_grade"), 0)
        mixed_risk = str(row.get("mixed_text_region_risk") or "high")
        mixed_penalty = {"low": 0, "medium": 1, "high": 2}.get(mixed_risk, 2)
        score = sq * 10 - mixed_penalty
        if score > best_score * 10:
            best_score = sq
            best = row
    if best and cur_idx is not None and int(best.get("frame_index", -1)) == cur_idx:
        return None
    return best


def run_better_frame_selection_runtime_v1(
    *,
    output_root: str,
    roi_crop_root: str,
    roi_retry_root: str,
    source_validation_root: str,
    mixed_batch_v2_root: str,
    linebox_sq_root: str,
    readability_governance_root: str,
    adapter_v1_root: str,
    review_queue_runtime_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    errs: List[str] = []
    crop_root = Path(roi_crop_root).resolve()
    retry_root = Path(roi_retry_root).resolve()
    sv = Path(source_validation_root).resolve()
    linebox_root = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    crop_intake = {
        r.get("roi_retry_proposal_id"): r
        for r in (_read_json(crop_root / "roi_crop_candidate_intake_matrix_v1.json") or {}).get("rows") or []
        if isinstance(r, dict)
    }
    crop_artifacts = {
        r.get("source_roi_retry_proposal_id"): r
        for r in (_read_json(crop_root / "roi_crop_artifact_collection_v1.json") or {}).get("artifacts") or []
        if isinstance(r, dict)
    }
    deferred_rows = (_read_json(crop_root / "roi_crop_better_frame_deferred_report_v1.json") or {}).get("rows") or []

    proposals = {
        str(p.get("roi_retry_proposal_id")): p
        for p in (_read_json(retry_root / "roi_retry_proposal_collection_v1.json") or {}).get("proposals") or []
        if isinstance(p, dict) and p.get("roi_retry_proposal_id")
    }

    quality_by_index: Dict[int, Dict[str, Any]] = {}
    for row in (_read_json(linebox_root / "mixedvideo_ocr_source_quality_evaluation_matrix.json") or {}).get("rows") or []:
        if isinstance(row, dict) and row.get("frame_index") is not None:
            quality_by_index[int(row["frame_index"])] = row

    linebox_frames: Dict[str, Dict[str, Any]] = {}
    for fr in (_read_json(linebox_root / "mixedvideo_ocr_scan_linebox_trace_report.json") or {}).get("frames") or []:
        if isinstance(fr, dict) and fr.get("frame_id"):
            linebox_frames[str(fr["frame_id"])] = fr

    intake_rows: List[Dict[str, Any]] = []
    candidates: List[Dict[str, Any]] = []
    reason_rows: List[Dict[str, Any]] = []
    existing_rows: List[Dict[str, Any]] = []
    neighbor_rows: List[Dict[str, Any]] = []
    readiness_rows: List[Dict[str, Any]] = []
    routing_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    selected_existing = neighboring_req = multiframe_req = future_detector_req = unavailable = 0
    better_frame_required_count = 0
    crop_rerun_recommended = 0

    video_id_default = "test_video_complex_6m42s"

    for fr in linebox_frames.values():
        fid = str(fr.get("frame_id") or "")
        idx = _parse_frame_index(fid)
        qrow = quality_by_index.get(idx or -1, {})
        sq = qrow.get("source_quality_grade")
        existing_rows.append(
            {
                "source_item_id": fid,
                "existing_frame_ref": fid,
                "linebox_available": fr.get("linebox_available", True),
                "linebox_count": fr.get("text_item_count", 0),
                "source_quality_grade": sq,
                "readability_grade": None,
                "reuse_as_better_frame_candidate": sq in ("SQ_A", "SQ_B") and sq != "SQ_E",
                "reuse_reason": "existing_scan_frame_in_pool"
                if sq in ("SQ_A", "SQ_B", "SQ_D")
                else "sq_e_not_crop_ready",
                "limitations": "not_crop_ready_if_SQ_E" if sq == "SQ_E" else "candidate_only_not_evidence",
            }
        )

    for def_row in deferred_rows:
        if not isinstance(def_row, dict):
            continue
        pid = str(def_row.get("proposal_id") or "")
        prop = proposals.get(pid, {})
        crop_in = crop_intake.get(pid, {})
        crop_art = crop_artifacts.get(pid, {})

        ptype = prop.get("proposal_type") or def_row.get("proposal_type") or ""
        sq = prop.get("source_quality_grade") or crop_in.get("source_quality_grade")
        frame_id = prop.get("frame_id") or crop_in.get("frame_id")
        image_id = prop.get("image_id") or crop_in.get("image_id")
        source_id = prop.get("source_id") or crop_in.get("source_id")
        defer_reason = def_row.get("defer_reason") or crop_in.get("crop_defer_reason")
        bbox = prop.get("proposed_roi_bbox_xyxy")
        lb_refs = prop.get("source_linebox_refs") or crop_in.get("source_linebox_refs") or []
        chain = list(prop.get("source_chain") or [])
        chain.append(RUNTIME_STEP)
        vc_id = _vc_from_chain(prop.get("source_chain") or [])

        if ptype == "better_frame_required" or def_row.get("better_frame_required"):
            better_frame_required_count += 1

        input_id = _bfid(f"in:{pid}")
        intake_rows.append(
            {
                "better_frame_candidate_input_id": input_id,
                "source_roi_retry_proposal_id": pid,
                "source_crop_artifact_id": crop_art.get("crop_artifact_id"),
                "source_validation_candidate_id": vc_id,
                "source_type": prop.get("source_type") or crop_in.get("source_type"),
                "source_id": source_id,
                "frame_id": frame_id,
                "image_id": image_id,
                "proposal_type": ptype,
                "defer_reason": defer_reason,
                "source_quality_grade": sq,
                "readability_grade": prop.get("readability_grade"),
                "linebox_refs": lb_refs,
                "current_bbox_status": "present" if bbox else "null",
                "current_crop_status": crop_art.get("crop_generation_status", "deferred"),
                "intake_status": "accepted",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        reasons, dominant = _reasons_for_item(
            defer_reason=str(defer_reason),
            ptype=ptype,
            sq=sq,
            has_bbox=bool(bbox),
            has_linebox=len(lb_refs) > 0 or (frame_id and frame_id in linebox_frames),
            mixed=ptype == "mixed_region_split",
        )

        candidate_frame_id: Optional[str] = None
        candidate_source = "unavailable"
        selection_status = "deferred"
        expected_read = "unknown"
        crop_readiness = "needs_better_source"
        route = "hold_unavailable"
        target_sq = "SQ_B"
        selection_confidence = 0.3
        future_phase = "Better-Frame-Extraction-DryRun-v1"

        if image_id and not frame_id:
            if defer_reason == "null_bbox_deferred" or not bbox:
                candidate_source = "future_detector_required"
                crop_readiness = "needs_detector"
                route = "require_future_detector"
                future_detector_req += 1
                future_phase = "Future-Detector-ROI-Proposal-v1"
                reasons.append("future_detector_needed")
            else:
                candidate_source = "multiframe_required"
                crop_readiness = "needs_multiframe"
                route = "require_multiframe_merge"
                multiframe_req += 1
                future_phase = "Multiframe-Merge-Proposal-v1"
        elif frame_id and str(frame_id) in linebox_frames:
            vid = _parse_video_id(str(frame_id)) or video_id_default
            better = _pick_better_frame(str(frame_id), quality_by_index, vid)
            if better:
                bidx = int(better["frame_index"])
                candidate_frame_id = _frame_id_from_index(vid, bidx)
                candidate_source = "existing_scan_frame"
                selection_status = "selected_candidate"
                expected_read = "high" if better.get("source_quality_grade") == "SQ_A" else "medium"
                crop_readiness = "ready_later"
                route = "select_existing_frame_candidate"
                target_sq = str(better.get("source_quality_grade") or "SQ_B")
                selection_confidence = 0.75
                selected_existing += 1
                crop_rerun_recommended += 1
                future_phase = "ROI-Crop-Execution-DryRun-v1-rerun"
                reasons.append("existing_pool_higher_sq_frame")
            else:
                candidate_source = "neighboring_frame_required"
                crop_readiness = "needs_better_source"
                route = "require_neighboring_frame_extraction"
                neighboring_req += 1
                future_phase = "Better-Frame-Extraction-DryRun-v1"
                reasons.append("neighboring_frame_needed")
        elif sq == "SQ_C" and ptype == "future_detector_required":
            candidate_source = "multiframe_required"
            crop_readiness = "needs_multiframe"
            route = "require_multiframe_merge"
            multiframe_req += 1
            future_phase = "Multiframe-Merge-Proposal-v1"
        else:
            unavailable += 1
            route = "hold_unavailable"
            crop_readiness = "unavailable"
            reasons.append("source_unavailable")

        if sq == "SQ_E":
            crop_readiness = "needs_better_source" if crop_readiness != "needs_detector" else crop_readiness

        bf_id = _bfid(f"bf:{pid}")
        ts_sec = None
        cidx = _parse_frame_index(candidate_frame_id) if candidate_frame_id else None
        if cidx is not None and cidx in quality_by_index:
            ts_sec = quality_by_index[cidx].get("timestamp_ms")
            if ts_sec is not None:
                ts_sec = float(ts_sec) / 1000.0

        cand = {
            "better_frame_candidate_id": bf_id,
            "schema_version": "better_frame_candidate_v1",
            "source_item_id": source_id,
            "source_type": prop.get("source_type"),
            "current_frame_id": frame_id,
            "candidate_frame_id": candidate_frame_id,
            "candidate_source": candidate_source,
            "candidate_frame_index": cidx,
            "candidate_frame_time_sec": ts_sec,
            "selection_status": selection_status,
            "selection_reason": reasons,
            "expected_readability_improvement": expected_read,
            "expected_roi_crop_readiness": crop_readiness,
            "future_roi_crop_candidate": {
                "bbox_expected": candidate_source == "existing_scan_frame",
                "bbox_source_expected": "linebox_union" if candidate_source == "existing_scan_frame" else None,
                "crop_phase_required": "ROI-Crop-Execution-DryRun-v1-rerun",
            },
            "current_source_quality_grade": sq,
            "target_source_quality_grade": target_sq,
            "linebox_refs": lb_refs,
            "selection_confidence": selection_confidence,
            "required_future_phase": future_phase,
            "blocked_current_actions": [
                "roi_crop_executed",
                "ocr_request_generated",
                "ocr_invoked",
                "new_frame_extracted",
                "new_video_decoded",
            ],
            "new_frame_extracted": False,
            "crop_executed": False,
            "ocr_request_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": chain,
        }
        candidates.append(cand)

        reason_rows.append(
            {
                "item_id": input_id,
                "reasons": reasons,
                "dominant_reason": dominant,
                "selection_status": selection_status,
                "future_action": future_phase,
            }
        )

        if candidate_source == "neighboring_frame_required":
            neighbor_rows.append(
                {
                    "item_id": input_id,
                    "neighboring_frame_required": True,
                    "multiframe_required": False,
                    "reason": dominant,
                    "suggested_temporal_window_sec": 2.0,
                    "suggested_frame_count": 3,
                    "new_frame_extraction_allowed_in_this_phase": False,
                    "required_future_phase": "Better-Frame-Extraction-DryRun-v1",
                }
            )
        if candidate_source == "multiframe_required":
            neighbor_rows.append(
                {
                    "item_id": input_id,
                    "neighboring_frame_required": False,
                    "multiframe_required": True,
                    "reason": dominant,
                    "suggested_temporal_window_sec": 5.0,
                    "suggested_frame_count": 5,
                    "new_frame_extraction_allowed_in_this_phase": False,
                    "required_future_phase": "Multiframe-Merge-Proposal-v1",
                }
            )

        readiness_rows.append(
            {
                "better_frame_candidate_id": bf_id,
                "expected_roi_crop_readiness": crop_readiness,
                "bbox_expected": candidate_source == "existing_scan_frame",
                "bbox_source_expected": "linebox_union"
                if candidate_source == "existing_scan_frame"
                else None,
                "crop_rerun_recommended": selection_status == "selected_candidate",
                "crop_blockers_remaining": ["sq_e_source"] if sq == "SQ_E" else [],
                "required_future_phase": future_phase,
                "ocr_request_allowed_now": False,
                "fact_status": "not_fact",
            }
        )

        routing_rows.append(
            {
                "item_id": input_id,
                "route_decision": route,
                "generated_candidate_ref": bf_id if selection_status == "selected_candidate" else None,
                "required_future_phase": future_phase,
                "blocked_actions": cand["blocked_current_actions"],
                "crop_executed": False,
                "ocr_request_generated": False,
                "provider_invoked": False,
                "fact_status": "not_fact",
            }
        )

        chain_rows.append(
            {
                "better_frame_candidate_id": bf_id,
                "traceable_to_roi_crop_execution": True,
                "traceable_to_roi_retry_proposal": True,
                "traceable_to_source_validation": bool(vc_id),
                "traceable_to_linebox_trace": bool(frame_id and frame_id in linebox_frames),
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

    deferred_count = len(deferred_rows)
    candidate_count = len(candidates)
    selected_count = sum(1 for c in candidates if c.get("selection_status") == "selected_candidate")

    metrics = {
        "schema_version": "better_frame_metrics_candidate_report_v1",
        "deferred_crop_item_count_observed": deferred_count,
        "intake_item_count": len(intake_rows),
        "better_frame_candidate_count": candidate_count,
        "selected_existing_frame_count": selected_count,
        "neighboring_frame_required_count": neighboring_req,
        "multiframe_required_count": multiframe_req,
        "future_detector_required_count": future_detector_req,
        "unavailable_count": unavailable,
        "crop_rerun_recommended_count": crop_rerun_recommended,
        "new_frame_extracted_count": 0,
        "roi_crop_executed_count": 0,
        "ocr_request_generated_count": 0,
        "provider_invoked_count": 0,
        "evidence_pack_generated_count": 0,
        "no_write_boundary_pass_rate": 1.0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    summary = {
        "schema_version": "better_frame_selection_runtime_v1_summary_v0",
        "phase": PHASE_ID,
        "runtime_scope": "better_frame_selection_runtime_only",
        "based_on_roi_crop_execution_dryrun": crop_root.is_dir(),
        "based_on_roi_retry_proposal_runtime": retry_root.is_dir(),
        "based_on_linebox_trace": linebox_root.is_dir(),
        "better_frame_candidate_generated": candidate_count > 0,
        "deferred_crop_item_count_observed": deferred_count,
        "better_frame_required_count_observed": better_frame_required_count,
        "better_frame_candidate_count": candidate_count,
        "selection_planning_only": True,
        "new_video_decoded": False,
        "new_frame_extracted": False,
        "roi_crop_executed": False,
        "ocr_request_generated": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
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
        "phase_verdict_hint": "GO" if candidate_count > 0 and not errs else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    candidate_schema = {
        "schema_version": "better_frame_candidate_schema_v1",
        "template": {
            "better_frame_candidate_id": "bf_<hash>",
            "schema_version": "better_frame_candidate_v1",
            "source_retry_proposal_id": None,
            "source_crop_artifact_id": None,
            "source_frame_ref": None,
            "source_video_ref": None,
            "current_frame_id": None,
            "candidate_frame_id": None,
            "candidate_frame_time_sec": None,
            "candidate_frame_index": None,
            "candidate_source": "existing_scan_frame | neighboring_frame_required | multiframe_required | future_detector_required | unavailable",
            "selection_reason": [],
            "expected_readability_improvement": "high | medium | low | unknown",
            "expected_roi_crop_readiness": "ready_later | needs_detector | needs_multiframe | needs_better_source | unavailable",
            "current_source_quality_grade": None,
            "target_source_quality_grade": None,
            "linebox_refs": [],
            "future_roi_crop_candidate": {
                "bbox_expected": False,
                "bbox_source_expected": None,
                "crop_phase_required": "ROI-Crop-Execution-DryRun-v1-rerun",
            },
            "selection_confidence": None,
            "selection_status": "selected_candidate | deferred | unavailable",
            "new_frame_extracted": False,
            "crop_executed": False,
            "ocr_request_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": [],
        },
        "defaults": {
            "new_frame_extracted": False,
            "crop_executed": False,
            "ocr_request_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "better_frame_candidate_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {
            "schema_version": "better_frame_selection_rule_matrix_v1",
            "rules": SELECTION_RULES,
        },
        "candidate_schema": candidate_schema,
        "candidate_collection": {
            "schema_version": "better_frame_candidate_collection_v1",
            "candidate_count": candidate_count,
            "candidates": candidates,
        },
        "reason_report": {
            "schema_version": "better_frame_selection_reason_report_v1",
            "row_count": len(reason_rows),
            "rows": reason_rows,
        },
        "existing_report": {
            "schema_version": "better_frame_existing_candidate_report_v1",
            "row_count": len(existing_rows),
            "rows": existing_rows,
        },
        "neighbor_report": {
            "schema_version": "better_frame_neighboring_multiframe_requirement_report_v1",
            "row_count": len(neighbor_rows),
            "rows": neighbor_rows,
        },
        "readiness_matrix": {
            "schema_version": "better_frame_future_roi_crop_readiness_matrix_v1",
            "row_count": len(readiness_rows),
            "rows": readiness_rows,
        },
        "routing_matrix": {
            "schema_version": "better_frame_routing_matrix_v1",
            "row_count": len(routing_rows),
            "rows": routing_rows,
        },
        "future_plan": {
            "schema_version": "better_frame_future_execution_plan_v1",
            "phases": FUTURE_PHASES,
        },
        "boundary": {
            "schema_version": "better_frame_boundary_report_v1",
            "better_frame_selection_only": True,
            "new_video_decoded": False,
            "new_frame_extracted": False,
            "roi_crop_executed": False,
            "ocr_request_generated": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
        },
        "source_chain": {
            "schema_version": "better_frame_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_roi_crop_execution": all(r.get("traceable_to_roi_crop_execution") for r in chain_rows),
            "rows": chain_rows,
        },
        "metrics": metrics,
        "benchmark_link": {
            "schema_version": "better_frame_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "better_frame_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "better_frame_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "better_frame_selection_only": True,
            "new_video_decoded": False,
            "new_frame_extracted": False,
            "roi_crop_executed": False,
            "ocr_request_generated": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
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
            "schema_version": "better_frame_simulation_context_report_v1",
            "simulation_profile_id": (_read_json(sim / "simulation_summary.json") or {}).get(
                "simulation_profile_id", "developer_full"
            ),
            "run_model": (_read_json(sim / "simulation_summary.json") or {}).get("run_model", False),
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "better_frame_non_claims_report_v1",
            "no_new_video_decode": True,
            "no_new_frame_extract": True,
            "no_roi_crop": True,
            "no_ocr_request": True,
            "candidate_not_evidence": True,
            "candidate_not_fact": True,
            "not_production_ready": True,
        },
        "followups": {"schema_version": "better_frame_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "better_frame_audit_report_v1",
            "better_frame_selection_runtime_v1_executed": True,
            "better_frame_selection_only": True,
            "better_frame_candidate_generated": candidate_count > 0,
            "new_video_decoded": False,
            "new_frame_extracted": False,
            "roi_crop_executed": False,
            "ocr_request_generated": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
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
        "errs": errs,
    }
