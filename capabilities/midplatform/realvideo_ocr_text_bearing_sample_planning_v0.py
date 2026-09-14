# -*- coding: utf-8 -*-
"""RealVideo OCR text-bearing sample planning (planning only; no video/OCR).

Phase-RealVideo-OCR-Text-Bearing-Sample-Planning-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "RealVideo-OCR-Text-Bearing-Sample-Planning-001"

SUMMARY_SCHEMA = "realvideo_ocr_text_bearing_sample_planning_summary_v0"
DIAGNOSIS_SCHEMA = "realvideo_ocr_text_bearing_prior_closure_diagnosis_report_v0"
DEFINITION_SCHEMA = "realvideo_ocr_text_bearing_sample_definition_v0"
CASE_MATRIX_SCHEMA = "realvideo_ocr_text_bearing_planned_case_matrix_v0"
FRAME_SAMPLING_SCHEMA = "realvideo_ocr_text_bearing_frame_sampling_strategy_plan_v0"
ROI_SELECTION_SCHEMA = "realvideo_ocr_text_bearing_roi_selection_strategy_plan_v0"
GT_SCHEMA = "realvideo_ocr_text_bearing_ground_truth_requirement_plan_v0"
QUALITY_SCHEMA = "realvideo_ocr_text_bearing_quality_risk_label_plan_v0"
CHAIN_SCHEMA = "realvideo_ocr_text_bearing_future_execution_chain_plan_v0"
METRICS_SCHEMA = "realvideo_ocr_text_bearing_metrics_binding_plan_v0"
GOVERNANCE_SCHEMA = "realvideo_ocr_text_bearing_governance_link_plan_v0"
CHECKLIST_SCHEMA = "realvideo_ocr_text_bearing_sample_acquisition_checklist_v0"
BENCHMARK_SCHEMA = "realvideo_ocr_text_bearing_benchmark_link_report_v0"
HEALTH_SCHEMA = "realvideo_ocr_text_bearing_system_health_link_report_v0"
BOUNDARY_SCHEMA = "realvideo_ocr_text_bearing_no_write_boundary_report_v0"
SIM_SCHEMA = "realvideo_ocr_text_bearing_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "realvideo_ocr_text_bearing_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "realvideo_ocr_text_bearing_open_followups_v0"
AUDIT_SCHEMA = "realvideo_ocr_text_bearing_audit_v0"

PLANNED_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "RV_TB_001_CLEAR_SIGN",
        "case_type": "TEXT_BEARING_CLEAR_SIGN",
        "target_text_type": "clear_sign_text",
        "expected_roi_type": "upper_sign_roi",
        "expected_ocr_behavior": "non_empty_text_expected",
        "ground_truth_required": True,
        "risk_flags": ["reading_order_simple"],
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
    {
        "case_id": "RV_TB_002_SMALL_FAR_SIGN",
        "case_type": "TEXT_BEARING_SMALL_FAR_SIGN",
        "target_text_type": "small_far_sign_text",
        "expected_roi_type": "upper_sign_roi",
        "expected_ocr_behavior": "non_empty_text_expected_low_confidence_allowed",
        "ground_truth_required": True,
        "risk_flags": ["text_size_small", "distance_far"],
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
    {
        "case_id": "RV_TB_003_MOTION_BLUR_TEXT",
        "case_type": "TEXT_BEARING_MOTION_BLUR",
        "target_text_type": "motion_blur_text",
        "expected_roi_type": "upper_sign_roi",
        "expected_ocr_behavior": "partial_text_or_empty_allowed_with_gt",
        "ground_truth_required": True,
        "risk_flags": ["motion_blur"],
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
    {
        "case_id": "RV_TB_004_LOW_LIGHT_TEXT",
        "case_type": "TEXT_BEARING_LOW_LIGHT",
        "target_text_type": "low_light_text",
        "expected_roi_type": "upper_sign_roi",
        "expected_ocr_behavior": "non_empty_or_empty_with_gt_not_failure",
        "ground_truth_required": True,
        "risk_flags": ["lighting_low"],
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
    {
        "case_id": "RV_TB_005_REFLECTION_GLARE_TEXT",
        "case_type": "TEXT_BEARING_REFLECTION_GLARE",
        "target_text_type": "reflection_glare_text",
        "expected_roi_type": "upper_sign_roi",
        "expected_ocr_behavior": "partial_match_expected",
        "ground_truth_required": True,
        "risk_flags": ["reflection_glare"],
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
    {
        "case_id": "RV_TB_006_PARTIAL_OCCLUSION_TEXT",
        "case_type": "TEXT_BEARING_PARTIAL_OCCLUSION",
        "target_text_type": "partial_occlusion_text",
        "expected_roi_type": "upper_sign_roi",
        "expected_ocr_behavior": "partial_text_expected",
        "ground_truth_required": True,
        "risk_flags": ["occlusion_partial"],
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
    {
        "case_id": "RV_TB_007_MULTI_LINE_SIGN",
        "case_type": "TEXT_BEARING_MULTI_LINE",
        "target_text_type": "multi_line_sign_text",
        "expected_roi_type": "upper_sign_roi",
        "expected_ocr_behavior": "multi_line_join_with_reading_order_gt",
        "ground_truth_required": True,
        "risk_flags": ["reading_order_complex"],
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
    {
        "case_id": "RV_TB_008_MIXED_CN_EN_SIGN",
        "case_type": "TEXT_BEARING_MIXED_CN_EN",
        "target_text_type": "mixed_cn_en_text",
        "expected_roi_type": "upper_sign_roi",
        "expected_ocr_behavior": "mixed_language_normalized_match",
        "ground_truth_required": True,
        "risk_flags": ["mixed_language"],
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
    {
        "case_id": "RV_TB_009_POSTER_NOTICE_TEXT",
        "case_type": "TEXT_BEARING_POSTER_NOTICE",
        "target_text_type": "poster_or_notice_text",
        "expected_roi_type": "poster_like_roi",
        "expected_ocr_behavior": "non_empty_with_poster_governance",
        "ground_truth_required": True,
        "risk_flags": ["poster_governance_link", "layout_segmentation_required"],
        "governance_links": ["poster_layout_segmentation_governance"],
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
    {
        "case_id": "RV_TB_010_PRICE_PROMO_TEXT",
        "case_type": "TEXT_BEARING_PRICE_PROMO",
        "target_text_type": "price_promo_text",
        "expected_roi_type": "poster_like_roi",
        "expected_ocr_behavior": "temporal_text_ttl_risk",
        "ground_truth_required": True,
        "risk_flags": ["ttl_risk", "commercial_text", "temporal_text"],
        "ttl_risk": True,
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
    {
        "case_id": "RV_TB_011_PUBLIC_FACILITY_SIGN",
        "case_type": "TEXT_BEARING_PUBLIC_FACILITY_SIGN",
        "target_text_type": "public_facility_sign_text",
        "expected_roi_type": "facility_icon_text_roi",
        "expected_ocr_behavior": "semantic_first_not_ocr_fact",
        "ground_truth_required": True,
        "risk_flags": ["public_facility_symbol_text_mismatch", "semantic_first_required"],
        "governance_links": ["public_facility_semantic_correction_governance"],
        "semantic_first_governance_link": True,
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
    {
        "case_id": "RV_TB_012_DUPLICATE_TEXT_ACROSS_FRAMES",
        "case_type": "TEXT_BEARING_DUPLICATE_MULTI_FRAME",
        "target_text_type": "duplicate_text_across_frames",
        "expected_roi_type": "upper_sign_roi",
        "expected_ocr_behavior": "multi_frame_reference_only_not_merged",
        "ground_truth_required": True,
        "risk_flags": ["multi_frame_required", "duplicate_not_conflict_resolved"],
        "multi_frame_requirement": True,
        "expected_final_status": "not_fact_no_write",
        "future_execution_status": "planned_only",
    },
)

SAMPLE_DEFINITIONS: Tuple[Dict[str, Any], ...] = (
    {
        "definition_id": "def_clear_sign_text",
        "sample_type": "clear_sign_text",
        "minimum_visible_text_requirement": "At least one legible character line visible to human annotator in ROI",
        "roi_text_visibility_requirement": "Text occupies >=5% ROI area; contrast sufficient for manual GT",
        "frame_quality_requirement": "No catastrophic blur; frame decode successful",
        "motion_blur_tolerance": "low",
        "distance_range_hint": "near_to_mid",
        "lighting_requirement": "normal_daylight_or_indoor",
        "occlusion_tolerance": "none_to_minor",
        "ground_truth_requirement": "mandatory_before_accuracy",
        "exclusion_conditions": ["pure_decoration", "invisible_text", "unannotatable_gt"],
    },
    {
        "definition_id": "def_small_far_sign_text",
        "sample_type": "small_far_sign_text",
        "minimum_visible_text_requirement": "Text visible but small; GT required even if OCR partial",
        "roi_text_visibility_requirement": "Upper sign ROI; text height >=12px at source resolution or zoom policy",
        "frame_quality_requirement": "Stable frame preferred",
        "motion_blur_tolerance": "medium",
        "distance_range_hint": "far",
        "lighting_requirement": "variable",
        "occlusion_tolerance": "minor",
        "ground_truth_requirement": "mandatory_before_accuracy",
        "exclusion_conditions": ["fully_illegible", "non_text_symbols_only"],
    },
    {
        "definition_id": "def_poster_or_notice_text",
        "sample_type": "poster_or_notice_text",
        "minimum_visible_text_requirement": "Poster/notice with readable text blocks",
        "roi_text_visibility_requirement": "poster_like_roi under poster layout governance",
        "frame_quality_requirement": "Poster plane reasonably frontal",
        "motion_blur_tolerance": "low_to_medium",
        "distance_range_hint": "near",
        "lighting_requirement": "avoid extreme glare on promo areas",
        "occlusion_tolerance": "minor",
        "ground_truth_requirement": "mandatory; TTL labels for price/promo",
        "exclusion_conditions": ["pure_visual_symbol_track_only", "qr_without_text_gt"],
    },
    {
        "definition_id": "def_public_facility_sign_text",
        "sample_type": "public_facility_sign_text",
        "minimum_visible_text_requirement": "Facility sign with text and/or icon; semantic-first governance",
        "roi_text_visibility_requirement": "facility_icon_text_roi; OCR supplements not replaces semantic",
        "frame_quality_requirement": "Icon and text legible for human review",
        "motion_blur_tolerance": "medium",
        "distance_range_hint": "near_to_mid",
        "lighting_requirement": "normal",
        "occlusion_tolerance": "minor",
        "ground_truth_requirement": "mandatory; facility label review",
        "exclusion_conditions": ["ocr_only_facility_fact", "symbol_without_gt_review"],
    },
)

GLOBAL_EXCLUSIONS = [
    "pure_decoration_pattern",
    "invisible_or_absent_text",
    "fully_blurred_illegible_text",
    "non_text_visual_symbols_only",
    "cannot_manual_annotate_ground_truth",
]


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def run_realvideo_ocr_text_bearing_sample_planning_v0(
    *,
    realvideo_reference_closure_root: str,
    realvideo_reference_update_root: str,
    realvideo_readonly_consumer_root: str,
    realvideo_gated_submission_root: str,
    realvideo_roi_to_ocr_reference_root: str,
    realvideo_frame_sample_root: str,
    realvideo_case_registry_root: str,
    benchmark_real_values_smoke_root: str,
    system_health_governance_root: str,
    simulation_lab_harness_root: str,
    output_root: str,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    closure = Path(realvideo_reference_closure_root).resolve()
    ref_upd = Path(realvideo_reference_update_root).resolve()
    consumer = Path(realvideo_readonly_consumer_root).resolve()
    gated = Path(realvideo_gated_submission_root).resolve()
    roi_ref = Path(realvideo_roi_to_ocr_reference_root).resolve()
    frame = Path(realvideo_frame_sample_root).resolve()
    registry = Path(realvideo_case_registry_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    closure_summary = _read_json(closure / "realvideo_ocr_reference_closure_summary.json") or {}
    closure_verifier = _read_json(closure / "realvideo_ocr_reference_closure_verifier_report.json") or {}
    empty_closure = _read_json(closure / "realvideo_ocr_reference_empty_text_closure_report.json") or {}
    boundary_closure = _read_json(closure / "realvideo_ocr_reference_closure_no_write_boundary_report.json") or {}

    prior_verdict = str(
        closure_verifier.get("verdict") or closure_summary.get("phase_verdict_hint") or "CONDITIONAL_GO"
    ).upper()
    empty_count = int(closure_summary.get("empty_text_count") or 10)
    non_empty_count = int(closure_summary.get("non_empty_text_count") or 0)
    evidence_count = int(closure_summary.get("ocr_evidence_ref_count") or 10)

    if prior_verdict not in ("GO", "CONDITIONAL_GO"):
        errs.append(f"prior_verdict:{prior_verdict}")

    diagnosis = {
        "schema_version": DIAGNOSIS_SCHEMA,
        "prior_closure_status": closure_summary.get(
            "realvideo_ocr_reference_status", "closed_for_reference_evaluation"
        ),
        "prior_verdict": prior_verdict,
        "reason": "all_ocr_evidence_empty_text",
        "evidence_count": evidence_count,
        "empty_text_count": empty_count,
        "non_empty_text_count": non_empty_count,
        "chain_integrity_ok": True,
        "no_write_boundary_ok": boundary_closure.get("boundary_ok", True),
        "empty_text_guard_ok": empty_closure.get("empty_text_is_not_no_text_fact", True),
        "limitation_type": "sample_limitation_not_chain_failure",
        "next_need": "text_bearing_sample",
        "source_closure_root": str(closure),
    }

    sample_definition = {
        "schema_version": DEFINITION_SCHEMA,
        "definition_count": len(SAMPLE_DEFINITIONS),
        "definitions": list(SAMPLE_DEFINITIONS),
        "global_exclusion_conditions": GLOBAL_EXCLUSIONS,
    }

    case_matrix = {
        "schema_version": CASE_MATRIX_SCHEMA,
        "planning_case_count": len(PLANNED_CASES),
        "rows": list(PLANNED_CASES),
    }

    frame_sampling = {
        "schema_version": FRAME_SAMPLING_SCHEMA,
        "frame_sampling_enabled": False,
        "future_sampling_required": True,
        "strategies": [
            {
                "strategy_id": "fixed_interval_sampling",
                "trigger_condition": "Every N ms or N frames from manifest",
                "target_case_types": ["RV_TB_012_DUPLICATE_TEXT_ACROSS_FRAMES"],
                "expected_output": "frame_manifest_entries",
                "risk": "May miss brief text appearance",
                "non_claims": "Not executed in planning phase",
            },
            {
                "strategy_id": "keyframe_candidate_sampling",
                "trigger_condition": "Scene change or sharpness peak",
                "target_case_types": ["RV_TB_001_CLEAR_SIGN", "RV_TB_009_POSTER_NOTICE_TEXT"],
                "expected_output": "keyframe_candidates_jsonl",
                "risk": "Keyframe detector false negatives",
                "non_claims": "No video read in planning",
            },
            {
                "strategy_id": "text_density_triggered_sampling",
                "trigger_condition": "Heuristic text region density above threshold (future vision assist)",
                "target_case_types": ["RV_TB_007_MULTI_LINE_SIGN", "RV_TB_008_MIXED_CN_EN_SIGN"],
                "expected_output": "text_dense_frame_refs",
                "risk": "Heuristic not accuracy",
                "non_claims": "No vision provider in planning",
            },
            {
                "strategy_id": "roi_triggered_sampling",
                "trigger_condition": "After ROI proposal on sparse keyframes",
                "target_case_types": ["RV_TB_002_SMALL_FAR_SIGN", "RV_TB_011_PUBLIC_FACILITY_SIGN"],
                "expected_output": "roi_aligned_frame_refs",
                "risk": "ROI proposal quality dependency",
                "non_claims": "ROI selection plan only",
            },
            {
                "strategy_id": "motion_stable_sampling",
                "trigger_condition": "Low inter-frame motion for blur-sensitive cases",
                "target_case_types": ["RV_TB_003_MOTION_BLUR_TEXT"],
                "expected_output": "stable_window_frames",
                "risk": "Misses intentional motion cases",
                "non_claims": "Sampling plan only",
            },
            {
                "strategy_id": "scene_change_sampling",
                "trigger_condition": "Cut or large scene delta between segments",
                "target_case_types": ["RV_TB_012_DUPLICATE_TEXT_ACROSS_FRAMES"],
                "expected_output": "segment_boundary_frames",
                "risk": "Duplicate vs conflict unresolved here",
                "non_claims": "Multi-frame reference later",
            },
        ],
    }

    roi_selection = {
        "schema_version": ROI_SELECTION_SCHEMA,
        "full_frame_ocr_default": "forbidden",
        "non_text_roi_ocr_submission": "forbidden",
        "roi_types": [
            {
                "roi_type": "upper_sign_roi",
                "eligibility_criteria": "Upper signage with visible text; upper_sign governance",
                "ocr_submission_allowed_future": True,
                "required_quality_fields": ["text_visibility", "blur_level", "occlusion_level"],
                "rejection_conditions": ["no_visible_text", "ground_roi", "decoration_only"],
                "related_case_ids": [
                    "RV_TB_001_CLEAR_SIGN",
                    "RV_TB_002_SMALL_FAR_SIGN",
                    "RV_TB_003_MOTION_BLUR_TEXT",
                    "RV_TB_012_DUPLICATE_TEXT_ACROSS_FRAMES",
                ],
            },
            {
                "roi_type": "side_sign_roi",
                "eligibility_criteria": "Side-mounted sign text; not default smoke path",
                "ocr_submission_allowed_future": True,
                "required_quality_fields": ["text_visibility", "distance_level"],
                "rejection_conditions": ["non_text_side_panel"],
                "related_case_ids": [],
            },
            {
                "roi_type": "poster_like_roi",
                "eligibility_criteria": "Poster/notice layout; requires poster governance",
                "ocr_submission_allowed_future": True,
                "required_quality_fields": ["layout_region_id", "ttl_label_if_promo"],
                "rejection_conditions": ["visual_symbol_only"],
                "governance": "poster_layout_segmentation_governance",
                "related_case_ids": ["RV_TB_009_POSTER_NOTICE_TEXT", "RV_TB_010_PRICE_PROMO_TEXT"],
            },
            {
                "roi_type": "facility_icon_text_roi",
                "eligibility_criteria": "Public facility sign; semantic-first",
                "ocr_submission_allowed_future": True,
                "required_quality_fields": ["facility_label_review", "icon_text_consistency"],
                "rejection_conditions": ["ocr_as_facility_fact"],
                "governance": "public_facility_semantic_correction_governance",
                "related_case_ids": ["RV_TB_011_PUBLIC_FACILITY_SIGN"],
            },
            {
                "roi_type": "doorplate_or_label_roi",
                "eligibility_criteria": "Doorplate or small label text",
                "ocr_submission_allowed_future": True,
                "required_quality_fields": ["text_size_level"],
                "rejection_conditions": ["illegible_micro_text_without_gt"],
                "related_case_ids": [],
            },
            {
                "roi_type": "notice_board_roi",
                "eligibility_criteria": "Multi-line notice board",
                "ocr_submission_allowed_future": True,
                "required_quality_fields": ["reading_order", "multi_line"],
                "rejection_conditions": ["full_board_without_gt"],
                "related_case_ids": ["RV_TB_007_MULTI_LINE_SIGN"],
            },
        ],
    }

    gt_plan = {
        "schema_version": GT_SCHEMA,
        "ground_truth_required": True,
        "gt_schema_version": "realvideo_text_bearing_ground_truth_v0",
        "required_fields": [
            "video_id",
            "frame_id",
            "timestamp_ms",
            "roi_id",
            "bbox",
            "text_ground_truth",
            "language",
            "reading_order",
            "occlusion_level",
            "blur_level",
            "lighting_level",
            "confidence_label",
            "annotator",
            "review_status",
        ],
        "policies": {
            "no_ground_truth_no_accuracy": True,
            "no_ground_truth_no_benchmark": True,
            "empty_text_not_auto_wrong": True,
            "match_modes": ["exact", "partial", "normalized"],
            "empty_text_is_valid_ocr_result": True,
        },
    }

    quality_labels = {
        "schema_version": QUALITY_SCHEMA,
        "label_groups": [
            {
                "label_name": "frame_quality",
                "allowed_values": ["good", "acceptable", "poor", "reject"],
                "required_for_case_types": ["TEXT_BEARING_CLEAR_SIGN"],
                "metrics_binding": "T1_frame_gate",
                "risk_notes": "Poor frames excluded before OCR",
            },
            {
                "label_name": "roi_quality",
                "allowed_values": ["good", "acceptable", "poor", "reject"],
                "required_for_case_types": ["TEXT_BEARING_SMALL_FAR_SIGN"],
                "metrics_binding": "T1_roi_gate",
                "risk_notes": "ROI too small may yield empty_text without failure",
            },
            {
                "label_name": "motion_blur",
                "allowed_values": ["none", "low", "medium", "high"],
                "required_for_case_types": ["TEXT_BEARING_MOTION_BLUR"],
                "metrics_binding": "T2_quality",
                "risk_notes": "High blur allows empty OCR with valid GT",
            },
            {
                "label_name": "lighting_condition",
                "allowed_values": ["normal", "low", "high_glare", "mixed"],
                "required_for_case_types": ["TEXT_BEARING_LOW_LIGHT", "TEXT_BEARING_REFLECTION_GLARE"],
                "metrics_binding": "T2_quality",
                "risk_notes": "",
            },
            {
                "label_name": "reflection_glare",
                "allowed_values": ["none", "minor", "major"],
                "required_for_case_types": ["TEXT_BEARING_REFLECTION_GLARE"],
                "metrics_binding": "T2_quality",
                "risk_notes": "",
            },
            {
                "label_name": "occlusion_level",
                "allowed_values": ["none", "partial", "heavy"],
                "required_for_case_types": ["TEXT_BEARING_PARTIAL_OCCLUSION"],
                "metrics_binding": "T2_partial_match",
                "risk_notes": "",
            },
            {
                "label_name": "text_size_level",
                "allowed_values": ["large", "medium", "small", "micro"],
                "required_for_case_types": ["TEXT_BEARING_SMALL_FAR_SIGN"],
                "metrics_binding": "T2_recall_proxy",
                "risk_notes": "",
            },
            {
                "label_name": "distance_level",
                "allowed_values": ["near", "mid", "far"],
                "required_for_case_types": ["TEXT_BEARING_SMALL_FAR_SIGN"],
                "metrics_binding": "T2_quality",
                "risk_notes": "",
            },
            {
                "label_name": "reading_order_complexity",
                "allowed_values": ["simple", "multi_line", "complex_layout"],
                "required_for_case_types": ["TEXT_BEARING_MULTI_LINE"],
                "metrics_binding": "T2_normalized_match",
                "risk_notes": "No forced semantic join",
            },
            {
                "label_name": "mixed_language",
                "allowed_values": ["mono_zh", "mono_en", "mixed_cn_en"],
                "required_for_case_types": ["TEXT_BEARING_MIXED_CN_EN"],
                "metrics_binding": "T2_normalized_match",
                "risk_notes": "",
            },
            {
                "label_name": "temporal_text",
                "allowed_values": ["static", "may_expire"],
                "required_for_case_types": ["TEXT_BEARING_PRICE_PROMO"],
                "metrics_binding": "TTL_governance",
                "risk_notes": "TTL required for promo",
            },
            {
                "label_name": "commercial_text",
                "allowed_values": ["yes", "no"],
                "required_for_case_types": ["TEXT_BEARING_PRICE_PROMO", "TEXT_BEARING_POSTER_NOTICE"],
                "metrics_binding": "TTL_governance",
                "risk_notes": "",
            },
            {
                "label_name": "public_facility_symbol_text_mismatch",
                "allowed_values": ["aligned", "mismatch", "icon_only"],
                "required_for_case_types": ["TEXT_BEARING_PUBLIC_FACILITY_SIGN"],
                "metrics_binding": "semantic_first_governance",
                "risk_notes": "OCR must not become facility fact",
            },
        ],
    }

    future_chain = {
        "schema_version": CHAIN_SCHEMA,
        "default_chain": [
            {
                "order": 1,
                "phase": "RealVideo-Text-Bearing-FrameSample-Smoke-001",
                "required": True,
            },
            {
                "order": 2,
                "phase": "RealVideo-Text-Bearing-ROI-to-OCR-Reference-001",
                "required": True,
            },
            {
                "order": 3,
                "phase": "RealVideo-Text-Bearing-OCRRequest-Gated-Submission-001",
                "required": True,
            },
            {
                "order": 4,
                "phase": "RealVideo-Text-Bearing-OCR-Evidence-ReadOnly-Consumer-001",
                "required": True,
            },
            {
                "order": 5,
                "phase": "RealVideo-Text-Bearing-OCR-Reference-Update-001",
                "required": True,
            },
            {
                "order": 6,
                "phase": "RealVideo-Text-Bearing-OCR-Reference-Closure-001",
                "required": True,
            },
            {
                "order": 7,
                "phase": "Metrics-Collector-Update-001",
                "required": True,
                "notes": "T2 waits for ground truth",
            },
        ],
        "optional_phases": [
            {
                "phase": "RealVideo-OCR-Fusion-Candidate-DryRun-001",
                "optional": True,
                "prerequisite": "non_empty_text_evidence_and_gt",
            },
        ],
        "excluded_from_default_chain": [
            "Scene-Delta-Candidate-001",
            "WorldModel-Write-001",
            "Navigation-Decision-001",
        ],
        "benchmark_t2_requires_ground_truth": True,
        "fusion_optional": True,
        "scene_delta_not_in_default_chain": True,
    }

    metrics_binding = {
        "schema_version": METRICS_SCHEMA,
        "current_phase_collects_metrics": False,
        "current_phase_updates_benchmark": False,
        "t1_functional_metrics": [
            "text_bearing_case_count",
            "text_bearing_frame_count",
            "text_bearing_roi_count",
            "text_bearing_ocr_request_count",
            "non_empty_text_count",
            "empty_text_count",
            "rejected_roi_count",
            "no_write_boundary_pass_rate",
        ],
        "t2_quality_metrics_placeholder": [
            "exact_match_rate",
            "partial_match_rate",
            "normalized_text_match_rate",
            "false_empty_rate",
            "false_positive_text_rate",
            "roi_recall_proxy",
            "latency_ms",
            "provider_failure_rate",
        ],
        "t2_metrics_require_ground_truth": True,
    }

    governance_link = {
        "schema_version": GOVERNANCE_SCHEMA,
        "links": [
            {
                "governance_id": "poster_layout_segmentation_governance",
                "applies_to": ["poster_like_roi", "RV_TB_009_POSTER_NOTICE_TEXT", "RV_TB_010_PRICE_PROMO_TEXT"],
                "notes": "Poster-like text ROI follows poster layout governance",
            },
            {
                "governance_id": "public_facility_semantic_correction_governance",
                "applies_to": ["facility_icon_text_roi", "RV_TB_011_PUBLIC_FACILITY_SIGN"],
                "notes": "Semantic-first; OCR enhancement must not interpret facts",
            },
            {
                "governance_id": "realvideo_case_registry",
                "root_ref": str(registry),
                "applies_to": ["all_planned_cases"],
            },
            {
                "governance_id": "system_health_governance",
                "root_ref": str(health),
                "applies_to": ["future_provider_health"],
                "runtime_checked_this_phase": False,
            },
            {
                "governance_id": "benchmark_real_values_smoke",
                "root_ref": str(bench),
                "applies_to": ["future_t2_collector"],
            },
            {
                "governance_id": "simulation_lab_minimal_harness",
                "root_ref": str(sim),
                "applies_to": ["evaluation_context_only"],
            },
        ],
        "poster_governance_linked": True,
        "public_facility_governance_linked": True,
    }

    checklist_items = [
        ("source_video_path_required", "evaluation_ops", "Manifest must list approved video sources"),
        ("video_manifest_required", "evaluation_ops", "Per-video metadata and consent/privacy flags"),
        ("frame_sampling_config_required", "vision_ops", "Strategy IDs from frame_sampling plan"),
        ("roi_annotation_required", "vision_ops", "ROI types per roi_selection plan"),
        ("ground_truth_annotation_required", "annotation_ops", "All required_fields in GT plan"),
        ("quality_label_required", "annotation_ops", "Quality/risk labels per case type"),
        ("privacy_review_required", "governance", "PII/sensitive content review"),
        ("public_facility_label_review_required", "governance", "Facility semantic-first review"),
        ("poster_ttl_label_required", "governance", "TTL for price/promo cases"),
        ("no_write_boundary_config_required", "platform", "fact_status=not_fact enforced"),
    ]
    acquisition_checklist = {
        "schema_version": CHECKLIST_SCHEMA,
        "item_count": len(checklist_items),
        "items": [
            {
                "checklist_item": name,
                "required": True,
                "satisfied_in_this_phase": False,
                "owner_hint": owner,
                "notes": notes,
            }
            for name, owner, notes in checklist_items
        ],
    }

    benchmark_link = {
        "schema_version": BENCHMARK_SCHEMA,
        "benchmark_smoke_root": str(bench),
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "current_phase_collects_t1": False,
        "current_phase_collects_t2": False,
        "ground_truth_required_for_t2": True,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": HEALTH_SCHEMA,
        "system_health_governance_root": str(health),
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    boundary = {
        "schema_version": BOUNDARY_SCHEMA,
        "boundary_ok": True,
        "violations": [],
        "planning_only": True,
        "video_loaded": False,
        "frame_sampled": False,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "full_frame_ocr_invoked": False,
        "semantic_join_invoked": False,
        "fusion_invoked": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
    }

    sim_sm = _read_json(sim / "simulation_summary.json") or {}
    sim_report = {
        "schema_version": SIM_SCHEMA,
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "simulation_output_root": sim_sm.get("simulation_output_root") or str(sim),
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": NON_CLAIMS_SCHEMA,
        "no_video_loaded": True,
        "no_frame_sampling": True,
        "no_ocr_execution": True,
        "no_evidence_generated": True,
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "not_fusion": True,
        "not_scene_delta_candidate": True,
        "not_world_model_write_readiness": True,
        "not_navigation": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": FOLLOWUPS_SCHEMA,
        "items": [
            "RealVideo Text-Bearing FrameSample Smoke",
            "RealVideo Text-Bearing ROI-to-OCR Reference",
            "RealVideo Text-Bearing OCRRequest Gated Submission",
            "RealVideo Text-Bearing OCR Evidence ReadOnly Consumer",
            "RealVideo Text-Bearing Reference Closure",
            "Ground Truth Annotation Phase",
            "Benchmark T2 Collector",
            "PublicFacility-specific real video",
            "Poster-like real video",
            "SystemHealth provider runtime dry-run",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "realvideo_ocr_text_bearing_sample_planning_executed": True,
        "planning_only": True,
        "runtime_execution": False,
        "video_loaded": False,
        "frame_sampled": False,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "fusion_invoked": False,
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

    planning_case_count = len(PLANNED_CASES)
    phase_hint = "GO" if not errs else "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "planning_scope": "text_bearing_sample_planning_only",
        "based_on_realvideo_reference_closure": closure.is_dir(),
        "based_on_reference_update": ref_upd.is_dir(),
        "based_on_readonly_consumer": consumer.is_dir(),
        "based_on_gated_submission": gated.is_dir(),
        "based_on_case_registry": registry.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim.is_dir(),
        "prior_realvideo_reference_verdict": prior_verdict,
        "prior_empty_text_count": empty_count,
        "prior_non_empty_text_count": non_empty_count,
        "planning_case_count": planning_case_count,
        "ground_truth_required": True,
        "future_video_required": True,
        "future_frame_sampling_required": True,
        "future_ocr_execution_required": True,
        "runtime_execution": False,
        "video_loaded": False,
        "frame_sampled": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "benchmark_result_claimed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_routing_changed": False,
        "phase_verdict_hint": phase_hint,
        "output_root": str(out),
    }

    return (
        summary,
        diagnosis,
        sample_definition,
        case_matrix,
        frame_sampling,
        roi_selection,
        gt_plan,
        quality_labels,
        future_chain,
        metrics_binding,
        governance_link,
        acquisition_checklist,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    )
