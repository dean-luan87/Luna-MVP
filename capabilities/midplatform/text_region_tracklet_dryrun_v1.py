# -*- coding: utf-8 -*-
"""Text Region Tracklet DryRun v1 — projection-based tracklet candidate only, no OCR/detector.

Phase-Text-Region-Tracklet-DryRun-v1-001
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Text-Region-Tracklet-DryRun-v1-001"
RUNTIME_STEP = "text_region_tracklet_dryrun_v1"

FOLLOWUPS = [
    "Multiframe-Crop-Execution-DryRun-v1",
    "OCRRequest-Gated-Submission-from-Multiframe-v1",
    "Evidence-Pack-Adapter-v4-Multiframe",
    "Semantic-Candidate-v4-MultiframeAware",
    "Source-Validation-v2-Rerun-after-Multiframe",
    "Text-Detector-DryRun-v1",
    "Frame-Quality-Scoring-v1",
    "VisualSymbolRegistry-DryRun-v1",
    "Map-POI-Hint-DryRun-v1",
    "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
    "STC Contract later",
    "Controlled runtime integration",
]

RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "consume_better_frame_artifacts_only",
        "condition": "better_frame_artifact_collection present",
        "allowed_action": "artifact_intake_and_tracklet_candidate",
        "blocked_action": "fabricate_frame_artifact",
        "required_next_action": "Multiframe-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "approximate_bbox_projection_allowed",
        "condition": "static_bbox_projection within planned frames",
        "allowed_action": "projected_region_matrix",
        "blocked_action": "detector_output_claim",
        "required_next_action": "Multiframe-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "detector_invocation_forbidden",
        "condition": "phase_boundary",
        "allowed_action": "projection_only",
        "blocked_action": "object_detector_invocation",
        "required_next_action": "Text-Detector-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "text_detector_invocation_forbidden",
        "condition": "phase_boundary",
        "allowed_action": "projection_only",
        "blocked_action": "text_detector_invocation",
        "required_next_action": "Text-Detector-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "ocr_execution_forbidden",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "ocr_invocation",
        "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "crop_generation_forbidden",
        "condition": "phase_boundary",
        "allowed_action": "crop_readiness_plan",
        "blocked_action": "crop_generation",
        "required_next_action": "Multiframe-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "tracklet_candidate_not_fact",
        "condition": "always",
        "allowed_action": "tracklet_dryrun_artifacts",
        "blocked_action": "fact_write",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "bbox_continuity_not_entity_confirmation",
        "condition": "continuity_metrics present",
        "allowed_action": "continuity_report",
        "blocked_action": "entity_confirmation",
        "required_next_action": "Source-Validation-v2-Rerun-after-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "same_region_continuity_not_independent_consensus",
        "condition": "same_region_projection",
        "allowed_action": "tracklet_candidate_only",
        "blocked_action": "independent_consensus",
        "required_next_action": "Source-Validation-v2-Rerun-after-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "same_frame_blocker_not_resolved_in_this_phase",
        "condition": "always",
        "allowed_action": "blocker_carryover",
        "blocked_action": "same_frame_blocker_resolve",
        "required_next_action": "Multiframe-Crop-Execution-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_source_validation_rerun_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "source_validation_rerun",
        "required_next_action": "Source-Validation-v2-Rerun-after-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "world_model_attach",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "scene_delta_candidate",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

FUTURE_PHASES = [
    {
        "future_phase": "Multiframe-Crop-Execution-DryRun-v1",
        "purpose": "generate multiframe crops from projected regions",
        "required_input": ["text_region_tracklet_candidate_collection", "better_frame_artifact_collection"],
        "expected_output": "multiframe_crop_artifact_collection",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "purpose": "gated OCR for multiframe crops",
        "required_input": ["multiframe_crop_artifact_collection"],
        "expected_output": "multiframe_ocr_result_refs",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Evidence-Pack-Adapter-v4-Multiframe",
        "purpose": "adapt multiframe OCR to evidence packs",
        "required_input": ["multiframe_ocr_result_refs"],
        "expected_output": "evidence_pack_v4_multiframe_collection",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Semantic-Candidate-v4-MultiframeAware",
        "purpose": "semantic candidates aware of multiframe context",
        "required_input": ["evidence_pack_v4_multiframe_collection"],
        "expected_output": "semantic_candidate_v4_collection",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Source-Validation-v2-Rerun-after-Multiframe",
        "purpose": "re-evaluate validation with multiframe tracklet evidence",
        "required_input": ["tracklet_candidate_collection", "multiframe_ocr_results"],
        "expected_output": "validation_rerun_report",
        "not_in_current_phase": True,
    },
]

TRACKLET_SCHEMA: Dict[str, Any] = {
    "tracklet_candidate_id": "tr_tracklet_<uuid>",
    "schema_version": "text_region_tracklet_candidate_v1",
    "multiframe_candidate_region_id": None,
    "tracking_target": "bank_like_text_region",
    "source_frame": {
        "source_frame_id": None,
        "source_frame_index": None,
        "source_frame_time_sec": None,
    },
    "frame_sequence": [],
    "region_projection_method": "static_bbox_projection | approximate_bbox_projection",
    "source_bbox_xyxy": None,
    "expanded_bbox_set": [],
    "projected_regions": [],
    "continuity_metrics": {
        "frame_coverage_ratio": None,
        "bbox_continuity_score": None,
        "region_drift_risk": None,
        "scale_variation_hint": None,
        "viewpoint_shift_hint": None,
    },
    "quality_context": {
        "frame_quality_placeholder_used": True,
        "quality_claim_allowed": False,
    },
    "tracklet_status": "candidate_only",
    "tracklet_created_now": False,
    "ocr_allowed_in_this_phase": False,
    "crop_allowed_in_this_phase": False,
    "fact_status": "not_fact",
    "write_allowed": False,
    "source_chain": [],
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _tracklet_id(region_id: str) -> str:
    return f"tr_tracklet_{hashlib.sha256(region_id.encode()).hexdigest()[:12]}"


def _intake_id(artifact_id: str) -> str:
    return f"trk_intake_{hashlib.sha256(artifact_id.encode()).hexdigest()[:12]}"


def _drift_risk_from_offsets(offsets: List[int], blur_scores: List[Optional[float]]) -> Tuple[str, List[str]]:
    reasons: List[str] = []
    max_abs = max(abs(o) for o in offsets) if offsets else 0
    if max_abs >= 25:
        reasons.append("large_temporal_offset_from_source")
    if max_abs >= 15:
        reasons.append("viewpoint_shift_possible")
    low_blur = [b for b in blur_scores if b is not None and b < 500]
    if len(low_blur) >= 2:
        reasons.append("low_blur_placeholder_on_multiple_frames")
    if not reasons:
        reasons.append("static_projection_only_moderate_offset")
    if max_abs >= 25 or len(low_blur) >= 2:
        return "medium", reasons
    return "low", reasons


def run_text_region_tracklet_dryrun_v1(
    *,
    better_frame_root: str,
    multiframe_merge_proposal_root: str,
    source_validation_v2_root: str,
    semantic_v3_root: str,
    evidence_pack_v3_root: str,
    ocrrequest_gated_submission_v2_root: str,
    roi_ocrrequest_reference_v2_root: str,
    roi_crop_v2_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    bf_root = Path(better_frame_root).resolve()
    mf_root = Path(multiframe_merge_proposal_root).resolve()
    sv_root = Path(source_validation_v2_root).resolve()
    sem_root = Path(semantic_v3_root).resolve()
    ep_root = Path(evidence_pack_v3_root).resolve()
    linebox = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    bf_summary = _read_json(bf_root / "better_frame_extraction_dryrun_v1_summary.json") or {}
    artifacts_doc = _read_json(bf_root / "better_frame_artifact_collection.json") or {}
    refs_doc = _read_json(bf_root / "better_frame_candidate_frame_reference_collection.json") or {}
    quality_doc = _read_json(bf_root / "better_frame_quality_placeholder_report.json") or {}
    region_coll = _read_json(mf_root / "multiframe_candidate_region_collection_v1.json") or {}

    ref_by_id = {
        str(r.get("candidate_frame_ref_id")): r
        for r in (refs_doc.get("references") or [])
        if isinstance(r, dict)
    }
    quality_by_ref = {
        str(q.get("candidate_frame_ref_id")): q
        for q in (quality_doc.get("rows") or [])
        if isinstance(q, dict)
    }

    regions = [r for r in (region_coll.get("regions") or []) if isinstance(r, dict)]
    region = regions[0] if regions else {}
    region_id = str(region.get("multiframe_candidate_region_id") or "mf_region_unknown")
    source_frame_id = str(region.get("source_frame_id") or bf_summary.get("source_frame_id") or "")
    source_frame_index = int(region.get("source_frame_index") or bf_summary.get("source_frame_index") or 1620)
    source_frame_time_sec = float(region.get("source_frame_time_sec") or bf_summary.get("source_frame_time_sec") or 54.022)
    source_bbox = list(region.get("source_bbox_xyxy") or [292.0, 367.0, 381.0, 395.0])
    expanded_bbox_set = list(region.get("expanded_bbox_set") or [])

    generated_arts = [
        a
        for a in (artifacts_doc.get("artifacts") or [])
        if isinstance(a, dict) and a.get("frame_materialization_status") == "generated"
    ]
    generated_arts.sort(key=lambda x: int(x.get("frame_index") or 0))

    intake_rows: List[Dict[str, Any]] = []
    missing_files: List[str] = []
    for art in generated_arts:
        fp = str(art.get("frame_file_path") or "")
        ref_id = str(art.get("candidate_frame_ref_id") or "")
        ref = ref_by_id.get(ref_id, {})
        q = quality_by_ref.get(ref_id, {})
        if fp and not Path(fp).is_file():
            missing_files.append(fp)
        intake_rows.append(
            {
                "tracklet_frame_intake_id": _intake_id(str(art.get("frame_artifact_id") or ref_id)),
                "frame_artifact_id": art.get("frame_artifact_id"),
                "candidate_frame_ref_id": ref_id,
                "frame_index": art.get("frame_index"),
                "frame_time_sec": art.get("frame_time_sec"),
                "frame_offset_from_source": art.get("frame_offset_from_source"),
                "frame_file_path": fp,
                "frame_width": art.get("frame_width"),
                "frame_height": art.get("frame_height"),
                "frame_materialization_status": art.get("frame_materialization_status"),
                "quality_placeholder_ref": q.get("blur_score") is not None or ref.get("quality_placeholder"),
                "region_hint_ref": ref.get("region_hint"),
                "intake_status": "accepted" if fp and Path(fp).is_file() else "rejected_missing_file",
                "eligible_for_tracklet_dryrun": bool(fp and Path(fp).is_file()),
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    eligible_arts = [a for a in generated_arts if Path(str(a.get("frame_file_path") or "")).is_file()]
    frame_count = len(eligible_arts)

    tracklet_id = _tracklet_id(region_id)
    frame_sequence: List[Dict[str, Any]] = []
    projected_regions: List[Dict[str, Any]] = []
    projected_matrix_rows: List[Dict[str, Any]] = []
    quality_carryover_rows: List[Dict[str, Any]] = []
    offsets: List[int] = []
    blur_scores: List[Optional[float]] = []

    for art in eligible_arts:
        ref_id = str(art.get("candidate_frame_ref_id") or "")
        ref = ref_by_id.get(ref_id, {})
        qrow = quality_by_ref.get(ref_id, {})
        offset = int(art.get("frame_offset_from_source") or 0)
        offsets.append(offset)
        blur = qrow.get("blur_score") or (ref.get("quality_placeholder") or {}).get("blur_score")
        blur_scores.append(float(blur) if blur is not None else None)

        frame_sequence.append(
            {
                "candidate_frame_ref_id": ref_id,
                "frame_artifact_id": art.get("frame_artifact_id"),
                "frame_index": art.get("frame_index"),
                "frame_time_sec": art.get("frame_time_sec"),
                "frame_offset_from_source": offset,
                "frame_file_path": art.get("frame_file_path"),
            }
        )

        proj_source = list(source_bbox)
        proj_expanded = [list(b) for b in expanded_bbox_set]
        projected_regions.append(
            {
                "candidate_frame_ref_id": ref_id,
                "frame_index": art.get("frame_index"),
                "projection_method": "static_bbox_projection",
                "source_bbox_xyxy": proj_source,
                "expanded_bbox_set": proj_expanded,
                "projection_is_approximate": True,
                "detected_region": False,
            }
        )

        for eb in expanded_bbox_set:
            projected_matrix_rows.append(
                {
                    "tracklet_candidate_id": tracklet_id,
                    "candidate_frame_ref_id": ref_id,
                    "frame_artifact_id": art.get("frame_artifact_id"),
                    "frame_index": art.get("frame_index"),
                    "frame_time_sec": art.get("frame_time_sec"),
                    "frame_offset_from_source": offset,
                    "projection_method": "static_bbox_projection",
                    "source_bbox_xyxy": proj_source,
                    "projected_bbox_xyxy": list(eb),
                    "expanded_bbox_candidates": proj_expanded,
                    "projection_is_approximate": True,
                    "detected_region": False,
                    "detector_invoked": False,
                    "text_detector_invoked": False,
                    "region_confidence": 0.35,
                    "projection_status": "projected_hint_not_detection",
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )
        projected_matrix_rows.append(
            {
                "tracklet_candidate_id": tracklet_id,
                "candidate_frame_ref_id": ref_id,
                "frame_artifact_id": art.get("frame_artifact_id"),
                "frame_index": art.get("frame_index"),
                "frame_time_sec": art.get("frame_time_sec"),
                "frame_offset_from_source": offset,
                "projection_method": "static_bbox_projection",
                "source_bbox_xyxy": proj_source,
                "projected_bbox_xyxy": proj_source,
                "expanded_bbox_candidates": proj_expanded,
                "projection_is_approximate": True,
                "detected_region": False,
                "detector_invoked": False,
                "text_detector_invoked": False,
                "region_confidence": 0.4,
                "projection_status": "projected_hint_not_detection",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        quality_carryover_rows.append(
            {
                "candidate_frame_ref_id": ref_id,
                "frame_artifact_id": art.get("frame_artifact_id"),
                "blur_score": blur,
                "brightness_score": qrow.get("brightness_score")
                or (ref.get("quality_placeholder") or {}).get("brightness_score"),
                "lightweight_placeholder": True,
                "frame_quality_claim_allowed": False,
                "quality_context_used_for_planning_only": True,
                "required_future_phase": "Frame-Quality-Scoring-v1",
            }
        )

    projected_region_count = len(projected_matrix_rows)
    frame_expected = 6
    coverage_ratio = round(frame_count / frame_expected, 4) if frame_expected else 0.0
    drift_risk, drift_reasons = _drift_risk_from_offsets(offsets, blur_scores)

    continuity_score = 1.0 if frame_count == frame_expected else round(frame_count / max(frame_expected, 1), 4)
    continuity_score = min(continuity_score, 0.85)
    continuity_score = round(continuity_score * 0.7, 4)

    source_chain = [
        "better_frame_extraction_dryrun_v1",
        "multiframe_merge_proposal_v1",
        "source_validation_v2_after_ep_v3",
        "semantic_candidate_v3_bbox_expansion_aware",
        "evidence_pack_adapter_v3_bbox_expansion",
        "mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0",
    ]

    tracklet_candidate = {
        "tracklet_candidate_id": tracklet_id,
        "multiframe_candidate_region_id": region_id,
        "tracking_target": "bank_like_text_region",
        "source_frame_id": source_frame_id,
        "source_frame_index": source_frame_index,
        "source_frame_time_sec": source_frame_time_sec,
        "frame_sequence": frame_sequence,
        "source_bbox_xyxy": source_bbox,
        "expanded_bbox_set": expanded_bbox_set,
        "projected_regions": projected_regions,
        "region_projection_method": "static_bbox_projection",
        "projection_is_approximate": True,
        "detector_invoked": False,
        "text_detector_invoked": False,
        "tracklet_created_now": False,
        "tracklet_status": "candidate_only",
        "continuity_metrics": {
            "frame_coverage_ratio": coverage_ratio,
            "bbox_continuity_score": continuity_score,
            "region_drift_risk": drift_risk,
            "scale_variation_hint": "static_projection_assumes_constant_scale",
            "viewpoint_shift_hint": "moderate_if_large_offset",
        },
        "fact_status": "not_fact",
        "write_allowed": False,
        "source_chain": source_chain,
    }

    coverage_report = {
        "tracklet_candidate_id": tracklet_id,
        "frame_count_expected": frame_expected,
        "frame_count_available": frame_count,
        "frame_count_with_projection": frame_count,
        "missing_frame_count": max(0, frame_expected - frame_count),
        "frame_coverage_ratio": coverage_ratio,
        "coverage_status": "full" if frame_count >= frame_expected else "partial",
        "coverage_is_candidate_only": True,
        "fact_write_allowed": False,
    }

    continuity_report = {
        "tracklet_candidate_id": tracklet_id,
        "source_bbox_xyxy": source_bbox,
        "projected_bbox_count": projected_region_count,
        "bbox_continuity_score": continuity_score,
        "continuity_method": "static_bbox_projection_identity",
        "continuity_is_projection_based": True,
        "continuity_not_detection_based": True,
        "continuity_not_entity_confirmation": True,
        "same_region_continuity_not_independent_consensus": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    drift_report = {
        "tracklet_candidate_id": tracklet_id,
        "drift_risk": drift_risk,
        "drift_risk_reasons": drift_reasons,
        "viewpoint_shift_risk": max_abs_offset >= 15 if (max_abs_offset := max(abs(o) for o in offsets) if offsets else 0) else False,
        "scale_change_risk": False,
        "occlusion_change_risk": True,
        "motion_blur_risk": any(b is not None and b < 500 for b in blur_scores),
        "cross_region_merge_risk": True,
        "requires_future_detection_or_quality_gate": True,
        "required_next_action": "Text-Detector-DryRun-v1;Frame-Quality-Scoring-v1",
    }

    ready_for_crop = frame_count >= 6 and not missing_files
    crop_readiness = {
        "tracklet_candidate_id": tracklet_id,
        "ready_for_multiframe_crop_dryrun": ready_for_crop,
        "readiness_status": "ready_for_crop_dryrun" if ready_for_crop else "blocked_missing_artifacts",
        "crop_allowed_now": False,
        "required_input_for_future_crop": [
            "better_frame_artifact_collection",
            "text_region_projected_region_matrix_v1",
            "expanded_bbox_set",
        ],
        "blocker_codes": [] if ready_for_crop else ["missing_frame_artifact"],
        "future_phase": "Multiframe-Crop-Execution-DryRun-v1",
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    summary = {
        "schema_version": "text_region_tracklet_dryrun_v1_summary_v0",
        "phase": PHASE_ID,
        "dryrun_scope": "text_region_tracklet_dryrun_only",
        "based_on_better_frame_extraction": bf_root.is_dir(),
        "based_on_multiframe_merge_proposal": mf_root.is_dir(),
        "candidate_frame_reference_count_observed": bf_summary.get("candidate_frame_reference_count", 6),
        "frame_artifact_count_observed": len(generated_arts),
        "multiframe_candidate_region_count_observed": region_coll.get("region_count", 1),
        "tracklet_candidate_generated": True,
        "tracklet_candidate_count": 1,
        "tracklet_created_now": False,
        "region_projection_executed": True,
        "detector_invoked": False,
        "text_detector_invoked": False,
        "vision_model_invoked": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "crop_generated": False,
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
        "phase_verdict_hint": "GO"
        if frame_count >= 6 and len(missing_files) == 0
        else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "artifact_intake": {
            "schema_version": "tracklet_better_frame_artifact_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {"schema_version": "text_region_tracklet_rule_matrix_v1", "rules": RULES},
        "tracklet_schema": {
            "schema_version": "text_region_tracklet_candidate_schema_v1",
            "template": TRACKLET_SCHEMA,
        },
        "tracklet_collection": {
            "schema_version": "text_region_tracklet_candidate_collection_v1",
            "tracklet_candidate_count": 1,
            "candidates": [tracklet_candidate],
        },
        "projected_matrix": {
            "schema_version": "text_region_projected_region_matrix_v1",
            "row_count": projected_region_count,
            "rows": projected_matrix_rows,
        },
        "frame_coverage": {
            "schema_version": "text_region_tracklet_frame_coverage_report_v1",
            "reports": [coverage_report],
        },
        "bbox_continuity": {
            "schema_version": "text_region_bbox_continuity_report_v1",
            "reports": [continuity_report],
        },
        "drift_risk": {
            "schema_version": "text_region_drift_risk_report_v1",
            "reports": [drift_report],
        },
        "quality_carryover": {
            "schema_version": "text_region_quality_context_carryover_report_v1",
            "row_count": len(quality_carryover_rows),
            "rows": quality_carryover_rows,
        },
        "crop_readiness": {
            "schema_version": "text_region_tracklet_crop_readiness_report_v1",
            "reports": [crop_readiness],
        },
        "same_frame_carryover": {
            "schema_version": "text_region_tracklet_same_frame_blocker_carryover_report_v1",
            "same_frame_consensus_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
            "independent_consensus_allowed_now": False,
            "tracklet_candidate_prepared_but_not_validated": True,
            "required_future_phase": "Multiframe-Crop-Execution-DryRun-v1",
        },
        "future_crop_plan": {
            "schema_version": "text_region_future_multiframe_crop_plan_v1",
            "phases": FUTURE_PHASES,
        },
        "source_chain_report": {
            "schema_version": "text_region_tracklet_source_chain_report_v1",
            "tracklet_candidate_id": tracklet_id,
            "traceable_to_better_frame_extraction": bf_root.is_dir(),
            "traceable_to_multiframe_proposal": mf_root.is_dir(),
            "traceable_to_source_validation_v2": sv_root.is_dir(),
            "traceable_to_semantic_candidate_v3": sem_root.is_dir(),
            "traceable_to_evidence_pack_v3": ep_root.is_dir(),
            "traceable_to_linebox_trace": linebox.is_dir(),
            "source_chain_preserved": True,
            "source_chain": source_chain,
        },
        "boundary": {
            "schema_version": "text_region_tracklet_boundary_report_v1",
            "text_region_tracklet_dryrun_only": True,
            "detector_invoked": False,
            "text_detector_invoked": False,
            "vision_model_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "crop_generated": False,
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
            "schema_version": "text_region_tracklet_metrics_candidate_report_v1",
            "frame_artifact_count_observed": len(generated_arts),
            "tracklet_candidate_count": 1,
            "projected_region_count": projected_region_count,
            "frame_coverage_ratio": coverage_ratio,
            "tracklet_created_now_count": 0,
            "detector_invoked_count": 0,
            "text_detector_invoked_count": 0,
            "ocr_invoked_count": 0,
            "crop_generated_count": 0,
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
            "schema_version": "text_region_tracklet_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "text_region_tracklet_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "text_region_tracklet_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "text_region_tracklet_dryrun_only": True,
            "detector_invoked": False,
            "text_detector_invoked": False,
            "vision_model_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "crop_generated": False,
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
            "schema_version": "text_region_tracklet_simulation_context_report_v1",
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
            "schema_version": "text_region_tracklet_non_claims_report_v1",
            "no_ocr_in_phase": True,
            "no_detector": True,
            "no_crop": True,
            "no_ocrrequest": True,
            "projected_not_detected": True,
            "tracklet_candidate_not_real_tracklet": True,
            "bbox_continuity_not_entity_confirmation": True,
            "same_region_not_independent_consensus": True,
            "same_frame_blocker_not_resolved": True,
            "no_source_validation_rerun": True,
            "no_world_model": True,
            "no_scene_delta": True,
            "no_benchmark_claim": True,
            "no_provider_comparison": True,
            "no_navigation_ready": True,
            "no_production_ready": True,
        },
        "followups": {"schema_version": "text_region_tracklet_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "text_region_tracklet_audit_report_v1",
            "text_region_tracklet_dryrun_v1_executed": True,
            "text_region_tracklet_dryrun_only": True,
            "frame_artifact_count_observed": len(generated_arts),
            "tracklet_candidate_count": 1,
            "projected_region_count": projected_region_count,
            "tracklet_created_now": False,
            "detector_invoked": False,
            "text_detector_invoked": False,
            "vision_model_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "crop_generated": False,
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
