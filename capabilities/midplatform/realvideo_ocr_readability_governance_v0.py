# -*- coding: utf-8 -*-
"""RealVideo OCR readability governance (policy only; no video/OCR).

Phase-RealVideo-OCR-Readability-Governance-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "RealVideo-OCR-Readability-Governance-001"

READABILITY_FACTORS: Tuple[Dict[str, Any], ...] = (
    {
        "factor_id": "text_frontality_score",
        "factor_name": "text_frontality_score",
        "value_type": "float_0_1",
        "allowed_values": ["0.0-1.0"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": True,
        "affects_submission_strategy": True,
        "notes": "Low frontality downgrades grade",
    },
    {
        "factor_id": "text_size_level",
        "factor_name": "text_size_level",
        "value_type": "enum",
        "allowed_values": ["large", "medium", "small", "micro"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": True,
        "affects_submission_strategy": True,
        "notes": "Micro text may require resample",
    },
    {
        "factor_id": "occlusion_level",
        "factor_name": "occlusion_level",
        "value_type": "enum",
        "allowed_values": ["none", "partial", "heavy"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": True,
        "affects_submission_strategy": True,
        "notes": "Drives partial evidence policy",
    },
    {
        "factor_id": "motion_blur_level",
        "factor_name": "motion_blur_level",
        "value_type": "enum",
        "allowed_values": ["none", "low", "medium", "high"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": True,
        "affects_submission_strategy": True,
        "notes": "",
    },
    {
        "factor_id": "compression_artifact_level",
        "factor_name": "compression_artifact_level",
        "value_type": "enum",
        "allowed_values": ["none", "low", "medium", "high"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": True,
        "affects_submission_strategy": True,
        "notes": "Codec/blocking may fragment OCR",
    },
    {
        "factor_id": "angle_skew_level",
        "factor_name": "angle_skew_level",
        "value_type": "enum",
        "allowed_values": ["none", "mild", "severe"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": True,
        "affects_submission_strategy": True,
        "notes": "",
    },
    {
        "factor_id": "lighting_quality",
        "factor_name": "lighting_quality",
        "value_type": "enum",
        "allowed_values": ["good", "low", "high_glare", "mixed"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": True,
        "affects_submission_strategy": True,
        "notes": "",
    },
    {
        "factor_id": "contrast_score",
        "factor_name": "contrast_score",
        "value_type": "float_0_1",
        "allowed_values": ["0.0-1.0"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": True,
        "affects_submission_strategy": False,
        "notes": "",
    },
    {
        "factor_id": "tree_or_object_occlusion",
        "factor_name": "tree_or_object_occlusion",
        "value_type": "boolean",
        "allowed_values": ["true", "false"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": True,
        "affects_submission_strategy": True,
        "notes": "e.g. branches over bank sign",
    },
    {
        "factor_id": "partial_text_visible",
        "factor_name": "partial_text_visible",
        "value_type": "boolean",
        "allowed_values": ["true", "false"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": True,
        "affects_submission_strategy": True,
        "notes": "Triggers partial evidence path",
    },
    {
        "factor_id": "multi_frame_recoverable",
        "factor_name": "multi_frame_recoverable",
        "value_type": "boolean",
        "allowed_values": ["true", "false"],
        "affects_ocr_eligibility": False,
        "affects_evidence_confidence": True,
        "affects_submission_strategy": True,
        "notes": "Candidate-only multiframe recovery",
    },
    {
        "factor_id": "logo_or_visual_symbol_likelihood",
        "factor_name": "logo_or_visual_symbol_likelihood",
        "value_type": "float_0_1",
        "allowed_values": ["0.0-1.0"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": False,
        "affects_submission_strategy": True,
        "notes": "High likelihood routes to VisualSymbolEvidence",
    },
    {
        "factor_id": "public_facility_semantic_likelihood",
        "factor_name": "public_facility_semantic_likelihood",
        "value_type": "float_0_1",
        "allowed_values": ["0.0-1.0"],
        "affects_ocr_eligibility": True,
        "affects_evidence_confidence": False,
        "affects_submission_strategy": True,
        "notes": "Routes to PublicFacility semantic-first",
    },
)

ELIGIBILITY_GRADES: Tuple[Dict[str, Any], ...] = (
    {
        "grade": "A",
        "criteria": "正面、清晰、无遮挡、大字",
        "direct_ocr_allowed": True,
        "ordinary_ocr_allowed": True,
        "ocr_submission_allowed": True,
        "requires_review": False,
        "evidence_status": "ocr_candidate",
        "route_to_visual_symbol_evidence": False,
        "route_to_public_facility_semantic": False,
        "route_to_multiframe_recovery": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    },
    {
        "grade": "B",
        "criteria": "轻微角度/轻微遮挡",
        "direct_ocr_allowed": True,
        "ordinary_ocr_allowed": True,
        "ocr_submission_allowed": True,
        "requires_review": True,
        "evidence_status": "partial_or_uncertain_candidate",
        "route_to_visual_symbol_evidence": False,
        "route_to_public_facility_semantic": False,
        "route_to_multiframe_recovery": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    },
    {
        "grade": "C",
        "criteria": "明显遮挡/远距/模糊",
        "direct_ocr_allowed": False,
        "ordinary_ocr_allowed": False,
        "ocr_submission_allowed": True,
        "ocr_allowed": "conditional",
        "requires_review": True,
        "requires_resample_or_multiframe": True,
        "evidence_status": "partial_or_uncertain_candidate",
        "route_to_visual_symbol_evidence": False,
        "route_to_public_facility_semantic": False,
        "route_to_multiframe_recovery": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    },
    {
        "grade": "D",
        "criteria": "Logo / 品牌符号 / 图形化文字",
        "direct_ocr_allowed": False,
        "ordinary_ocr_allowed": False,
        "ocr_submission_allowed": False,
        "requires_review": True,
        "route_to_visual_symbol_evidence": True,
        "route_to_public_facility_semantic": False,
        "route_to_multiframe_recovery": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    },
    {
        "grade": "E",
        "criteria": "不可读",
        "direct_ocr_allowed": False,
        "ordinary_ocr_allowed": False,
        "ocr_submission_allowed": False,
        "requires_review": False,
        "record_as_unreadable_roi_candidate": True,
        "route_to_visual_symbol_evidence": False,
        "route_to_public_facility_semantic": False,
        "route_to_multiframe_recovery": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    },
)

ENHANCEMENT_OPERATIONS: Tuple[Dict[str, Any], ...] = (
    ("normalize_candidate", True, "candidate", "dictionary_or_rules", True),
    ("correction_candidate", True, "candidate", "gt_or_review", True),
    ("completion_candidate", True, "candidate", "multiframe_or_gt", True),
    ("common_entity_prior_candidate", True, "candidate", "entity_prior", True),
    ("dictionary_match_candidate", True, "candidate", "dictionary", True),
    ("multi_frame_merge_candidate", True, "candidate", "multiframe_alignment", True),
    ("visual_context_hint_candidate", True, "candidate", "visual_symbol_context", True),
    ("overwrite_raw_ocr_text", False, "forbidden", "n/a", True),
    ("pretend_completion_as_seen_text", False, "forbidden", "n/a", True),
    ("commit_without_review", False, "forbidden", "n/a", True),
    ("write_enhanced_text_as_fact", False, "forbidden", "n/a", True),
    ("use_enhancement_for_navigation_decision", False, "forbidden", "n/a", True),
    ("auto_approve_enhancement", False, "forbidden", "n/a", True),
)


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def run_realvideo_ocr_readability_governance_v0(
    *,
    text_bearing_sample_planning_root: str,
    realvideo_reference_closure_root: str,
    realvideo_reference_update_root: str,
    realvideo_readonly_consumer_root: str,
    existing_video_candidate_scan_root: str,
    poster_fusion_gate_chain_closure_root: str,
    public_facility_governance_root: str,
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
    planning = Path(text_bearing_sample_planning_root).resolve()
    closure = Path(realvideo_reference_closure_root).resolve()
    ref_upd = Path(realvideo_reference_update_root).resolve()
    consumer = Path(realvideo_readonly_consumer_root).resolve()
    scan = Path(existing_video_candidate_scan_root).resolve()
    poster = Path(poster_fusion_gate_chain_closure_root).resolve()
    facility = Path(public_facility_governance_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    scan_report = _read_json(scan / "realvideo_ocr_text_bearing_existing_video_scan_report.json") or {}
    facility_sm = _read_json(facility / "public_facility_runtime_dryrun_summary.json") or {}

    summary = {
        "schema_version": "realvideo_ocr_readability_governance_summary_v0",
        "phase": PHASE_ID,
        "governance_scope": "readability_governance_only",
        "based_on_text_bearing_planning": planning.is_dir(),
        "based_on_reference_closure": closure.is_dir(),
        "based_on_reference_update": ref_upd.is_dir(),
        "based_on_readonly_consumer": consumer.is_dir(),
        "based_on_existing_video_candidate_scan": scan.is_dir(),
        "based_on_public_facility_governance": facility.is_dir(),
        "based_on_poster_gate_chain_closure": poster.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim.is_dir(),
        "ocr_readability_governance_defined": True,
        "ocr_enhancement_boundary_defined": True,
        "partial_evidence_policy_defined": True,
        "visual_symbol_fallback_policy_defined": True,
        "multi_frame_recovery_policy_defined": True,
        "runtime_execution": False,
        "video_loaded": False,
        "frame_sampled": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "fusion_invoked": False,
        "scene_delta_candidate_generated": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_routing_changed": False,
        "phase_verdict_hint": "GO",
        "output_root": str(out),
        "source_scan_text_bearing_ratio": scan_report.get("text_bearing_ratio"),
    }

    factor_matrix = {
        "schema_version": "realvideo_ocr_readability_factor_matrix_v0",
        "factor_count": len(READABILITY_FACTORS),
        "factors": list(READABILITY_FACTORS),
    }

    eligibility_policy = {
        "schema_version": "realvideo_ocr_eligibility_grade_policy_v0",
        "grade_count": len(ELIGIBILITY_GRADES),
        "grades": list(ELIGIBILITY_GRADES),
    }

    partial_policy = {
        "schema_version": "realvideo_ocr_partial_evidence_policy_v0",
        "partial_evidence_allowed": True,
        "raw_ocr_text_must_be_preserved": True,
        "completion_candidate_allowed": True,
        "completion_committed": False,
        "completion_source_required": True,
        "user_visible_uncertainty_required": True,
        "covers": [
            "occluded_text",
            "fragment_text",
            "half_visible_text",
            "tree_or_pole_occlusion",
            "pedestrian_occlusion",
            "compression_fragment",
            "missing_prefix_or_suffix",
        ],
        "policies": {
            "completion_candidate_may_exist": True,
            "completion_must_not_overwrite_raw_ocr_text": True,
            "completion_not_broadcast_as_direct_recognition": True,
            "requires_review_and_source_validation": True,
        },
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    enhancement_ops = [
        {
            "operation": op,
            "allowed": allowed,
            "output_type": out_type,
            "required_source": src,
            "required_review": review,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        for op, allowed, out_type, src, review in ENHANCEMENT_OPERATIONS
    ]
    enhancement_boundary = {
        "schema_version": "realvideo_ocr_enhancement_boundary_policy_v0",
        "ocr_is_executor_not_fact_source": True,
        "system_may_intervene_upstream_downstream": True,
        "must_not_tamper_raw_ocr_output": True,
        "operations": enhancement_ops,
    }

    visual_fallback = {
        "schema_version": "realvideo_ocr_visual_symbol_fallback_policy_v0",
        "gap_logo_brand_sign_rule": "Do not rely on ordinary OCR alone for logo-like brand signs",
        "route_to_visual_symbol_evidence": True,
        "route_to_brand_symbol_candidate": True,
        "ordinary_ocr_result_optional": True,
        "brand_identity_confirmed": False,
        "visual_symbol_registry_required_later": True,
        "no_brand_fact_without_registry_or_review": True,
        "triggers": [
            {
                "visual_symbol_candidate_type": "brand_logo_sign",
                "trigger_condition": "logo_or_visual_symbol_likelihood >= 0.7",
                "ocr_chain_allowed": False,
                "visual_symbol_evidence_required": True,
                "registry_required_later": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            {
                "visual_symbol_candidate_type": "icon_like_text",
                "trigger_condition": "stylized_glyph_dominant",
                "ocr_chain_allowed": False,
                "visual_symbol_evidence_required": True,
                "registry_required_later": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
        ],
    }

    facility_types = [
        "restroom",
        "exit",
        "elevator",
        "bus_stop",
        "no_smoking",
        "accessibility",
        "hospital",
        "service_desk",
    ]
    facility_policy = {
        "schema_version": "realvideo_ocr_public_facility_semantic_first_policy_v0",
        "inherits_public_facility_runtime_dryrun": True,
        "public_facility_root_ref": str(facility),
        "default_ocr_mainline_allowed": facility_sm.get("default_ocr_mainline_allowed", False),
        "semantic_first_required": facility_sm.get("semantic_first_required", True),
        "ocr_text_evidence_auxiliary_only": True,
        "correction_candidate_allowed": True,
        "midplatform_arbitration_required": True,
        "raw_ocr_text_preserved": True,
        "facility_types_covered": facility_types,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    multiframe_policy = {
        "schema_version": "realvideo_ocr_multiframe_recovery_policy_v0",
        "output_status": "candidate_only",
        "strategies": [
            {
                "recovery_strategy": "same_roi_across_frames_candidate",
                "allowed": True,
                "required_inputs": ["roi_id", "frame_sequence", "readability_labels"],
                "required_quality_conditions": ["multi_frame_recoverable=true"],
                "review_required": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            {
                "recovery_strategy": "stable_text_fragment_merge_candidate",
                "allowed": True,
                "required_inputs": ["per_frame_raw_ocr", "alignment"],
                "required_quality_conditions": ["temporal_consistency"],
                "review_required": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            {
                "recovery_strategy": "best_frame_selection_candidate",
                "allowed": True,
                "required_inputs": ["readability_grade_per_frame"],
                "required_quality_conditions": ["grade_A_or_B_exists"],
                "review_required": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            {
                "recovery_strategy": "temporal_consistency_check_candidate",
                "allowed": True,
                "required_inputs": ["frame_pair", "text_fragments"],
                "required_quality_conditions": [],
                "review_required": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
        ],
        "forbidden": [
            "commit_multiframe_text_as_fact_without_review",
            "infer_missing_text_without_source",
            "write_world_model_from_multiframe_candidate",
        ],
    }

    risk_examples = {
        "schema_version": "realvideo_ocr_readability_risk_examples_report_v0",
        "source_video_id": scan_report.get("video_id", "test_video_complex_6m42s"),
        "source_scan_root": str(scan),
        "examples": [
            {
                "example_id": "construction_bank_occluded",
                "observed_issue": "front_part_occluded_by_tree",
                "raw_ocr_text_candidate": "建设银行 / Construction Bank",
                "missing_text_candidate": "中国",
                "readability_factors": ["tree_or_object_occlusion", "partial_text_visible", "occlusion_level=partial"],
                "recommended_grade": "B",
                "handling": "partial_evidence_plus_completion_candidate",
                "fact_status": "not_fact",
            },
            {
                "example_id": "gap_logo_sign",
                "observed_issue": "brand_logo_like_text",
                "raw_ocr_text_candidate": "null_or_unstable",
                "handling": "visual_symbol_evidence_brand_candidate",
                "recommended_grade": "D",
                "readability_factors": ["logo_or_visual_symbol_likelihood=high"],
                "fact_status": "not_fact",
            },
            {
                "example_id": "american_style_glasses_sign",
                "observed_issue": "tree_trunk_occlusion_angle_compression",
                "raw_ocr_text_candidate": "partial_or_unstable",
                "handling": "readability_low_requires_resample_or_multiframe",
                "recommended_grade": "C",
                "readability_factors": [
                    "tree_or_object_occlusion",
                    "angle_skew_level",
                    "compression_artifact_level",
                ],
                "fact_status": "not_fact",
            },
        ],
    }

    submission_plan = {
        "schema_version": "realvideo_ocr_readability_submission_strategy_update_plan_v0",
        "readability_grade_required_before_submission": True,
        "grade_A_submit": True,
        "grade_B_submit_with_partial_flag": True,
        "grade_C_submit_conditionally_or_resample": True,
        "grade_D_route_to_visual_symbol": True,
        "grade_E_reject_or_record_unreadable": True,
        "full_frame_ocr_default": False,
        "non_text_roi_submit": False,
        "no_write_boundary_required": True,
    }

    metrics_binding = {
        "schema_version": "realvideo_ocr_readability_metrics_binding_plan_v0",
        "future_metrics": [
            "readability_grade_distribution",
            "occlusion_level_distribution",
            "partial_evidence_count",
            "completion_candidate_count",
            "visual_symbol_fallback_count",
            "public_facility_semantic_first_count",
            "multiframe_recovery_candidate_count",
            "false_empty_due_to_readability_count",
            "non_empty_text_after_resample_count",
            "no_write_boundary_pass_rate",
        ],
        "current_phase_collects_metrics": False,
        "current_phase_updates_benchmark": False,
        "t2_metrics_require_ground_truth": True,
    }

    governance_link = {
        "schema_version": "realvideo_ocr_readability_governance_link_report_v0",
        "links": [
            {"id": "text_bearing_sample_planning", "root": str(planning)},
            {"id": "realvideo_reference_closure", "root": str(closure)},
            {"id": "poster_layout_governance", "root": str(poster), "via": "poster_gate_chain_closure"},
            {"id": "visual_symbol_evidence", "notes": "BrandSymbolCandidate / VisualSymbolEvidence track"},
            {"id": "public_facility_semantic_correction", "root": str(facility), "linked": True},
            {"id": "benchmark_real_values_smoke", "root": str(bench)},
            {"id": "system_health_governance", "root": str(health)},
            {"id": "simulation_lab", "root": str(sim)},
            {"id": "existing_video_candidate_scan", "root": str(scan)},
        ],
        "public_facility_governance_linked": True,
        "poster_governance_linked": True,
    }

    benchmark_link = {
        "schema_version": "realvideo_ocr_readability_benchmark_link_report_v0",
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
        "schema_version": "realvideo_ocr_readability_system_health_link_report_v0",
        "system_health_governance_root": str(health),
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    boundary = {
        "schema_version": "realvideo_ocr_readability_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "governance_only": True,
        "runtime_execution": False,
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
        "schema_version": "realvideo_ocr_readability_simulation_context_report_v0",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "simulation_output_root": sim_sm.get("simulation_output_root") or str(sim),
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "realvideo_ocr_readability_non_claims_report_v0",
        "no_video_loaded": True,
        "no_frame_sampling": True,
        "no_ocr_execution": True,
        "no_evidence_generated": True,
        "no_ocr_output_modification": True,
        "no_correction_commit": True,
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "visual_symbol_registry_not_integrated": True,
        "public_facility_runtime_not_on_mainline": True,
        "not_fusion": True,
        "not_scene_delta_candidate": True,
        "not_world_model_write_readiness": True,
        "not_navigation": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": "realvideo_ocr_readability_open_followups_v0",
        "items": [
            "Readability score stub",
            "Text-bearing frame sample with readability labels",
            "OCRRequest gate consuming readability grade",
            "Multi-frame recovery candidate phase",
            "VisualSymbolRegistry integration",
            "PublicFacility semantic-first runtime extension",
            "OCR enhancement candidate schema",
            "Ground truth annotation schema",
            "Benchmark T2 collector",
            "SystemHealth provider runtime dry-run",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": "realvideo_ocr_readability_audit_v0",
        "realvideo_ocr_readability_governance_executed": True,
        "governance_only": True,
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

    if not planning.is_dir():
        errs.append("planning_root_missing")
    if not scan.is_dir():
        errs.append("scan_root_missing")
    if errs:
        summary["phase_verdict_hint"] = "NO_GO"
        summary["errors"] = errs

    return (
        summary,
        factor_matrix,
        eligibility_policy,
        partial_policy,
        enhancement_boundary,
        visual_fallback,
        facility_policy,
        multiframe_policy,
        risk_examples,
        submission_plan,
        metrics_binding,
        governance_link,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    )
