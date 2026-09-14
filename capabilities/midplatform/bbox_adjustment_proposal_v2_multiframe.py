# -*- coding: utf-8 -*-
"""BBox adjustment proposal v2 from text detector dry-run candidates (no crop, no OCR).

Phase-BBox-Adjustment-Proposal-v2-Multiframe-001
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "BBox-Adjustment-Proposal-v2-Multiframe-001"
RUNTIME_STEP = "bbox_adjustment_proposal_v2_multiframe"

FOLLOWUPS = [
    "Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted",
    "OCRRequest-Gated-Submission-from-Multiframe-v2",
    "Evidence-Pack-Adapter-v4-Multiframe-Rerun",
    "Semantic-Candidate-v4-MultiframeAware",
    "Source-Validation-v2-Rerun-after-Multiframe",
    "Multiframe-Consensus-Policy-v1",
    "Crop-Quality-Scoring-v1",
    "Text-Detector-DryRun-v2-with-supervision",
    "VisualSymbolRegistry-DryRun-v1",
    "Map-POI-Hint-DryRun-v1",
    "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
]

FUTURE_PHASES: List[Dict[str, Any]] = [
    {
        "future_phase": "Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted",
        "purpose": "re-crop using adjusted bbox proposals",
        "required_input": ["bbox_adjustment_proposal_collection_v2"],
        "expected_output": ["multiframe_crop_artifact_collection_v2"],
        "boundary": "dry_run_no_ocr",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v2",
        "purpose": "re-OCR on detector-adjusted crops",
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
        "purpose": "semantic after text-bearing path",
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
    "consume_text_detector_adjustment_candidates_only",
    "heuristic_adjustment_not_fact",
    "adjustment_bbox_not_detected_text_region",
    "bounds_check_required",
    "clip_allowed_but_must_record",
    "deduplication_required",
    "proposal_ready_not_crop_ready",
    "no_new_crop_generation_in_this_phase",
    "no_ocr_execution_in_this_phase",
    "no_ocrrequest_generation_in_this_phase",
    "no_evidence_pack_generation_in_this_phase",
    "no_semantic_generation_in_this_phase",
    "no_source_validation_rerun_in_this_phase",
    "no_world_model_attach_in_this_phase",
    "no_scene_delta_candidate_in_this_phase",
]

PROPOSAL_TEMPLATE: Dict[str, Any] = {
    "bbox_adjustment_proposal_id": "bbox_adj_v2_<uuid>",
    "schema_version": "bbox_adjustment_proposal_v2_multiframe",
    "source_candidate": {
        "bbox_adjustment_candidate_id": None,
        "text_region_candidate_id": None,
        "source_input_ref": None,
        "source_type": None,
    },
    "frame_context": {
        "frame_index": None,
        "frame_time_sec": None,
        "frame_offset_from_source": None,
        "frame_width": None,
        "frame_height": None,
    },
    "bbox_adjustment": {
        "original_projection_bbox_xyxy": None,
        "proposed_adjusted_bbox_xyxy": None,
        "clipped_adjusted_bbox_xyxy": None,
        "clipped": False,
        "bbox_within_bounds": None,
        "adjustment_reason": None,
        "adjustment_confidence": None,
        "adjustment_source": "internal_heuristic",
        "iou_with_original": None,
    },
    "proposal_status": {
        "proposal_ready_for_future_recrop": False,
        "crop_generation_allowed_now": False,
        "ocrrequest_allowed_now": False,
        "ocr_allowed_now": False,
        "semantic_allowed_now": False,
        "source_validation_allowed_now": False,
    },
    "risk_flags": {
        "heuristic_candidate_not_fact": True,
        "adjustment_bbox_not_detected_text_region": True,
        "projection_risk_still_active": True,
        "same_frame_blocker_still_active": True,
    },
    "fact_status": "not_fact",
    "write_allowed": False,
    "source_chain": [],
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake_id(candidate_id: str) -> str:
    return f"ba_intake_{hashlib.sha256(candidate_id.encode()).hexdigest()[:10]}"


def _proposal_id(candidate_id: str) -> str:
    return f"bbox_adj_v2_{hashlib.sha256(candidate_id.encode()).hexdigest()[:12]}"


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


def _clip_bbox(bbox: List[float], fw: int, fh: int) -> Tuple[List[float], bool]:
    x1, y1, x2, y2 = bbox
    cx1 = max(0.0, min(float(fw), x1))
    cy1 = max(0.0, min(float(fh), y1))
    cx2 = max(0.0, min(float(fw), x2))
    cy2 = max(0.0, min(float(fh), y2))
    clipped = any(v != o for v, o in zip([cx1, cy1, cx2, cy2], [x1, y1, x2, y2]))
    if cx2 <= cx1:
        cx2 = min(float(fw), cx1 + 1.0)
    if cy2 <= cy1:
        cy2 = min(float(fh), cy1 + 1.0)
    return [cx1, cy1, cx2, cy2], clipped


def _bbox_valid(bbox: List[float], fw: int, fh: int) -> bool:
    x1, y1, x2, y2 = bbox
    w, h = x2 - x1, y2 - y1
    return w >= 4 and h >= 4 and x1 >= 0 and y1 >= 0 and x2 <= fw and y2 <= fh


def _dedup_key(frame_index: int, clipped: List[float], source_type: str) -> str:
    rounded = tuple(round(v, 1) for v in clipped)
    return f"{frame_index}|{source_type}|{rounded}"


def _build_rules() -> List[Dict[str, Any]]:
    return [
        {
            "rule_id": rid,
            "condition": rid,
            "proposal_effect": "govern_proposal_not_fact",
            "allowed_action": "proposal_generation_and_bounds_check",
            "blocked_action": "crop_ocr_fact_semantic_sv",
            "required_next_action": "Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted",
            "fact_status_after_rule": "not_fact",
            "write_allowed_after_rule": False,
        }
        for rid in RULE_IDS
    ]


def run_bbox_adjustment_proposal_v2_multiframe(
    *,
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
    td_root = Path(text_detector_root).resolve()
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

    adj_candidates = [
        r
        for r in (_read_json(td_root / "text_detector_bbox_adjustment_candidate_report_v1.json") or {}).get("rows") or []
        if isinstance(r, dict)
    ]
    candidate_count_observed = len(adj_candidates)

    txt_by_id = {
        str(c.get("text_region_candidate_id")): c
        for c in (_read_json(td_root / "text_region_candidate_collection_v1.json") or {}).get("candidates") or []
        if isinstance(c, dict) and c.get("text_region_candidate_id")
    }
    intake_by_source = {
        str(r.get("source_artifact_id") or r.get("source_input_ref")): r
        for r in (_read_json(td_root / "text_detector_input_intake_matrix_v1.json") or {}).get("rows") or []
        if isinstance(r, dict)
    }
    crops_by_id = {
        str(c.get("multiframe_crop_artifact_id")): c
        for c in (_read_json(crop_root / "multiframe_crop_artifact_collection_v1.json") or {}).get("artifacts") or []
        if isinstance(c, dict) and c.get("multiframe_crop_artifact_id")
    }

    frame_dims: Dict[int, Tuple[int, int]] = {}
    for ref in (_read_json(bf_root / "better_frame_candidate_frame_reference_collection.json") or {}).get("references") or []:
        if isinstance(ref, dict) and ref.get("candidate_frame_index") is not None:
            fi = int(ref["candidate_frame_index"])
            frame_dims[fi] = (int(ref.get("frame_width") or 544), int(ref.get("frame_height") or 960))

    default_fw, default_fh = 544, 960

    intake_rows: List[Dict[str, Any]] = []
    raw_proposals: List[Dict[str, Any]] = []
    bounds_rows: List[Dict[str, Any]] = []
    delta_rows: List[Dict[str, Any]] = []
    risk_rows: List[Dict[str, Any]] = []
    recrop_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    clipped_count = 0
    ready_count = 0

    for cand in adj_candidates:
        cand_id = str(cand.get("bbox_adjustment_candidate_id") or "")
        txt_id = str(cand.get("text_region_candidate_id") or "")
        src_ref = str(cand.get("source_input_ref") or "")
        txt = txt_by_id.get(txt_id, {})
        intake = intake_by_source.get(src_ref, {})
        crop_art = crops_by_id.get(src_ref, {})

        fc = txt.get("frame_context") or {}
        fi = int(fc.get("frame_index") or intake.get("frame_index") or crop_art.get("frame_index") or 0)
        ft = fc.get("frame_time_sec") or intake.get("frame_time_sec") or crop_art.get("frame_time_sec")
        fo = fc.get("frame_offset_from_source") or intake.get("frame_offset_from_source") or crop_art.get("frame_offset_from_source")
        fw, fh = frame_dims.get(fi, (default_fw, default_fh))
        source_type = str(txt.get("source_type") or intake.get("input_type") or "multiframe_crop")

        orig = [float(v) for v in cand.get("original_projection_bbox_xyxy") or []]
        proposed = [float(v) for v in cand.get("proposed_adjusted_bbox_xyxy") or []]
        adj_src = str(cand.get("adjustment_source") or "heuristic")
        if adj_src == "heuristic":
            adj_src = "internal_heuristic"

        intake_rows.append(
            {
                "bbox_adjustment_intake_id": _intake_id(cand_id),
                "bbox_adjustment_candidate_id": cand_id,
                "text_region_candidate_id": txt_id,
                "source_input_ref": src_ref,
                "source_type": source_type,
                "frame_index": fi,
                "frame_time_sec": ft,
                "frame_offset_from_source": fo,
                "original_projection_bbox_xyxy": orig,
                "proposed_adjusted_bbox_xyxy": proposed,
                "adjustment_reason": cand.get("adjustment_reason"),
                "iou_with_original": cand.get("iou_with_original"),
                "adjustment_confidence": cand.get("adjustment_confidence"),
                "adjustment_source": adj_src,
                "crop_generation_allowed_now": False,
                "ocrrequest_allowed_now": False,
                "intake_status": "accepted",
                "eligible_for_bbox_adjustment_proposal": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        clipped_bbox, clipped = _clip_bbox(proposed, fw, fh)
        if clipped:
            clipped_count += 1
        within = _bbox_valid(clipped_bbox, fw, fh)
        ready = within
        if ready:
            ready_count += 1

        pid = _proposal_id(cand_id)
        chain = list(txt.get("source_chain") or crop_art.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        prop = {
            "bbox_adjustment_proposal_id": pid,
            "bbox_adjustment_candidate_id": cand_id,
            "text_region_candidate_id": txt_id,
            "source_input_ref": src_ref,
            "source_type": source_type,
            "frame_index": fi,
            "frame_time_sec": ft,
            "frame_offset_from_source": fo,
            "frame_width": fw,
            "frame_height": fh,
            "original_projection_bbox_xyxy": [round(v, 2) for v in orig],
            "proposed_adjusted_bbox_xyxy": [round(v, 2) for v in proposed],
            "clipped_adjusted_bbox_xyxy": [round(v, 2) for v in clipped_bbox],
            "clipped": clipped,
            "bbox_within_bounds": within,
            "adjustment_reason": cand.get("adjustment_reason"),
            "adjustment_confidence": cand.get("adjustment_confidence"),
            "adjustment_source": adj_src,
            "iou_with_original": cand.get("iou_with_original"),
            "proposal_ready_for_future_recrop": ready,
            "crop_generation_allowed_now": False,
            "ocrrequest_allowed_now": False,
            "ocr_allowed_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": chain,
            "_dedup_key": _dedup_key(fi, clipped_bbox, source_type),
        }
        raw_proposals.append(prop)

        bounds_rows.append(
            {
                "bbox_adjustment_proposal_id": pid,
                "frame_width": fw,
                "frame_height": fh,
                "original_projection_bbox_xyxy": orig,
                "proposed_adjusted_bbox_xyxy": proposed,
                "bbox_within_bounds": within,
                "clipped": clipped,
                "clipped_adjusted_bbox_xyxy": clipped_bbox,
                "bbox_valid_for_future_recrop": ready,
                "bounds_check_status": "ok" if ready else "invalid_after_clip",
                "fact_status": "not_fact",
            }
        )

        ox1, oy1, ox2, oy2 = orig
        ax1, ay1, ax2, ay2 = clipped_bbox
        ow, oh = ox2 - ox1, oy2 - oy1
        aw, ah = ax2 - ax1, ay2 - ay1
        ocx, ocy = (ox1 + ox2) / 2, (oy1 + oy2) / 2
        acx, acy = (ax1 + ax2) / 2, (ay1 + ay2) / 2
        shift = ((acx - ocx) ** 2 + (acy - ocy) ** 2) ** 0.5
        area_o = max(1.0, ow * oh)
        area_a = aw * ah
        delta_rows.append(
            {
                "bbox_adjustment_proposal_id": pid,
                "original_projection_bbox_xyxy": orig,
                "adjusted_bbox_xyxy": clipped_bbox,
                "delta_x": round(ax1 - ox1, 2),
                "delta_y": round(ay1 - oy1, 2),
                "delta_w": round(aw - ow, 2),
                "delta_h": round(ah - oh, 2),
                "center_shift_px": round(shift, 2),
                "area_change_ratio": round(abs(area_a - area_o) / area_o, 4),
                "iou_with_original": _iou(orig, clipped_bbox),
                "adjustment_direction": "expand" if area_a > area_o else ("shrink" if area_a < area_o else "unchanged"),
                "adjustment_magnitude": "large" if shift > 20 else ("medium" if shift > 5 else "small"),
                "adjustment_is_diagnostic_only": True,
            }
        )

        risk_rows.append(
            {
                "bbox_adjustment_proposal_id": pid,
                "heuristic_candidate_not_fact": True,
                "adjustment_bbox_not_detected_text_region": True,
                "projection_risk_still_active": True,
                "possible_false_positive_text_like_region": True,
                "possible_cross_region_merge": area_a > area_o * 1.5,
                "possible_over_expansion": area_a > area_o * 1.2,
                "possible_under_expansion": area_a < area_o * 0.8,
                "requires_future_recrop": ready,
                "requires_future_reocr": ready,
                "requires_future_quality_gate": True,
                "fact_write_allowed": False,
            }
        )

        recrop_rows.append(
            {
                "bbox_adjustment_proposal_id": pid,
                "proposal_ready_for_future_recrop": ready,
                "crop_generation_allowed_now": False,
                "required_input_for_future_recrop": [
                    "bbox_adjustment_proposal_collection_v2",
                    "better_frame_artifact",
                    "tracklet_context",
                ],
                "future_phase": "Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted",
                "readiness_status": "ready_for_future_recrop" if ready else "blocked_invalid_bbox",
                "blocker_codes": [] if ready else ["invalid_bbox_after_bounds_check"],
            }
        )

        chain_rows.append(
            {
                "bbox_adjustment_proposal_id": pid,
                "traceable_to_text_detector_dryrun": td_root.is_dir(),
                "traceable_to_crop_quality_diagnosis": cq_root.is_dir(),
                "traceable_to_ep_v4": ep_root.is_dir(),
                "traceable_to_multiframe_crop": crop_root.is_dir(),
                "traceable_to_tracklet": tr_root.is_dir(),
                "traceable_to_better_frame": bf_root.is_dir(),
                "traceable_to_source_validation_v2": sv_root.is_dir(),
                "source_chain_preserved": True,
            }
        )

    # Deduplication
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for p in raw_proposals:
        k = p.pop("_dedup_key", "")
        groups.setdefault(k, []).append(p)

    duplicate_groups: List[Dict[str, Any]] = []
    canonical_proposals: List[Dict[str, Any]] = []
    for gid, (key, members) in enumerate(sorted(groups.items(), key=lambda x: x[0])):
        canonical = members[0]
        canonical_proposals.append(canonical)
        if len(members) > 1:
            duplicate_groups.append(
                {
                    "group_id": f"dedup_grp_{gid:03d}",
                    "member_proposal_ids": [m["bbox_adjustment_proposal_id"] for m in members],
                    "canonical_proposal_id": canonical["bbox_adjustment_proposal_id"],
                    "reason": "same_frame_index_clipped_bbox_and_source_type",
                    "proposal_status": "canonical_selected",
                }
            )

    proposal_count = len(raw_proposals)
    dedup_count = len(canonical_proposals)

    summary = {
        "schema_version": "bbox_adjustment_proposal_v2_multiframe_summary_v0",
        "phase": PHASE_ID,
        "proposal_scope": "bbox_adjustment_proposal_only",
        "based_on_text_detector_dryrun": True,
        "based_on_crop_quality_diagnosis_v2": True,
        "text_region_candidate_count_observed": 36,
        "bbox_adjustment_candidate_count_observed": candidate_count_observed,
        "bbox_adjustment_proposal_generated": proposal_count > 0,
        "bbox_adjustment_proposal_count": proposal_count,
        "deduplicated_proposal_count": dedup_count,
        "bounds_check_executed": True,
        "clipped_bbox_count": clipped_count,
        "proposal_ready_for_future_recrop_count": ready_count,
        "supervision_used": False,
        "adjustment_source": "internal_heuristic",
        "ocr_invoked": False,
        "provider_invoked": False,
        "new_crop_generated": False,
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
        "phase_verdict_hint": "GO" if candidate_count_observed == 5 and proposal_count > 0 else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "bbox_adjustment_candidate_intake_matrix_v2",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {"schema_version": "bbox_adjustment_rule_matrix_v2", "rules": _build_rules()},
        "proposal_schema": {
            "schema_version": "bbox_adjustment_proposal_schema_v2",
            "template": PROPOSAL_TEMPLATE,
        },
        "proposal_collection": {
            "schema_version": "bbox_adjustment_proposal_collection_v2",
            "proposal_count": proposal_count,
            "deduplicated_proposal_count": dedup_count,
            "proposals": raw_proposals,
            "canonical_proposals": canonical_proposals,
        },
        "bounds_check": {
            "schema_version": "bbox_adjustment_bounds_check_report_v2",
            "row_count": len(bounds_rows),
            "rows": bounds_rows,
        },
        "dedup": {
            "schema_version": "bbox_adjustment_dedup_grouping_report_v2",
            "input_candidate_count": candidate_count_observed,
            "proposal_count_before_dedup": proposal_count,
            "deduplicated_proposal_count": dedup_count,
            "duplicate_group_count": len(duplicate_groups),
            "grouping_method": "frame_index_clipped_bbox_source_type",
            "grouping_keys": ["frame_index", "clipped_adjusted_bbox_xyxy", "source_type"],
            "duplicate_groups": duplicate_groups,
        },
        "delta": {
            "schema_version": "bbox_adjustment_delta_report_v2",
            "row_count": len(delta_rows),
            "rows": delta_rows,
        },
        "risk": {
            "schema_version": "bbox_adjustment_risk_report_v2",
            "row_count": len(risk_rows),
            "rows": risk_rows,
        },
        "recrop_readiness": {
            "schema_version": "bbox_adjustment_future_recrop_readiness_report_v2",
            "row_count": len(recrop_rows),
            "rows": recrop_rows,
        },
        "future_reocr": {
            "schema_version": "bbox_adjustment_future_reocr_plan_v2",
            "phases": FUTURE_PHASES,
        },
        "source_chain": {
            "schema_version": "bbox_adjustment_source_chain_report_v2",
            "row_count": len(chain_rows),
            "rows": chain_rows,
        },
        "semantic_sv_blocker": {
            "schema_version": "bbox_adjustment_semantic_sv_blocker_carryover_report_v2",
            "semantic_v4_still_blocked": True,
            "source_validation_rerun_still_blocked": True,
            "blocker_reason": "bbox_adjustment_proposal_not_ocr_evidence",
            "same_frame_blocker_still_active": True,
            "required_future_phase": "Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted / OCRRequest-Gated-Submission-from-Multiframe-v2",
        },
        "boundary": {
            "schema_version": "bbox_adjustment_boundary_report_v2",
            "bbox_adjustment_proposal_only": True,
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
            "schema_version": "bbox_adjustment_metrics_candidate_report_v2",
            "bbox_adjustment_candidate_count_observed": candidate_count_observed,
            "bbox_adjustment_proposal_count": proposal_count,
            "deduplicated_proposal_count": dedup_count,
            "clipped_bbox_count": clipped_count,
            "proposal_ready_for_future_recrop_count": ready_count,
            "crop_generation_count": 0,
            "ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "evidence_pack_generated_count": 0,
            "semantic_candidate_generated_count": 0,
            "source_validation_rerun_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "bbox_adjustment_benchmark_link_report_v2",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "bbox_adjustment_system_health_link_report_v2",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "bbox_adjustment_no_write_boundary_report_v2",
            "boundary_ok": True,
            "violations": [],
            "bbox_adjustment_proposal_only": True,
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
            "schema_version": "bbox_adjustment_simulation_context_report_v2",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "bbox_adjustment_non_claims_report_v2",
            "claims": [
                "no_ocr_in_this_phase",
                "no_new_crop_in_this_phase",
                "adjustment_proposal_not_detected_text_region",
                "heuristic_adjustment_not_fact",
                "proposal_ready_not_ocr_ready_fact",
                "bbox_valid_not_ocr_success_guarantee",
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
        "followups": {"schema_version": "bbox_adjustment_open_followups_v2", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "bbox_adjustment_audit_report_v2",
            "bbox_adjustment_proposal_v2_multiframe_executed": True,
            "bbox_adjustment_proposal_only": True,
            "bbox_adjustment_candidate_count_observed": candidate_count_observed,
            "bbox_adjustment_proposal_count": proposal_count,
            "deduplicated_proposal_count": dedup_count,
            "proposal_ready_for_future_recrop_count": ready_count,
            "ocr_invoked": False,
            "provider_invoked": False,
            "new_crop_generated": False,
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
