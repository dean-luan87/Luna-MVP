# -*- coding: utf-8 -*-
"""CrossModal Vision-OCR TestBoard v1 RealVideo case registry (definition only).

Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001"

SUMMARY_SCHEMA = "cross_modal_vision_ocr_realvideo_case_registry_summary_v0"
REGISTRY_SCHEMA = "cross_modal_vision_ocr_realvideo_case_registry_v0"
TAXONOMY_SCHEMA = "cross_modal_vision_ocr_realvideo_case_taxonomy_v0"
SAMPLING_SCHEMA = "cross_modal_vision_ocr_realvideo_sampling_policy_stub_v0"
BEHAVIOR_SCHEMA = "cross_modal_vision_ocr_realvideo_expected_behavior_matrix_v0"
METRICS_BINDING_SCHEMA = "cross_modal_vision_ocr_realvideo_metrics_binding_matrix_v0"
GOVERNANCE_LINK_SCHEMA = "cross_modal_vision_ocr_realvideo_governance_link_report_v0"
NON_GOALS_SCHEMA = "cross_modal_vision_ocr_realvideo_non_goals_report_v0"
RISK_SCHEMA = "cross_modal_vision_ocr_realvideo_risk_register_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_realvideo_case_registry_audit_v0"

BASE_METRICS = [
    "ocr_empty_text_count",
    "ocr_non_empty_text_count",
    "text_item_count_total",
    "provider_distribution",
    "case_count",
    "not_fact_case_count",
    "no_write_case_count",
    "blocked_by_gate_count",
    "no_write_boundary_pass_rate",
]

POSTER_METRICS = [
    "poster_image_count",
    "full_image_ocr_forbidden_count",
    "segment_first_required_count",
    "text_region_count",
    "visual_symbol_region_count",
    "ocr_region_plan_count",
    "reading_order_low_confidence_count",
]

PERF_PLACEHOLDER = ["performance_metrics_available", "per_case_latency_ms", "total_pipeline_latency_ms"]


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _case(
    *,
    case_id: str,
    case_type: str,
    expected_trigger: str,
    expected_evidence_type: str,
    expected_risk_flags: List[str],
    expected_metrics: List[str],
    related_governance: List[str],
    risk_coverage_metric: str,
    taxonomy_tags: List[str],
) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "case_type": case_type,
        "track": "real_video_cases",
        "source_modality": "video_frame",
        "planned_input": "real_video_frame_or_roi",
        "expected_trigger": expected_trigger,
        "expected_evidence_type": expected_evidence_type,
        "expected_risk_flags": expected_risk_flags,
        "expected_metrics": expected_metrics,
        "related_governance": related_governance,
        "risk_coverage_metric": risk_coverage_metric,
        "taxonomy_tags": taxonomy_tags,
        "expected_final_fact_status": "not_fact",
        "expected_final_write_status": "no_write",
        "auto_approval_allowed": False,
        "navigation_decision_allowed": False,
        "execution_status": "registered_only",
    }


def build_case_registry() -> Dict[str, Any]:
    gov_metrics = ["metrics_schema", "boundary_metrics"]
    poster_gov = ["poster_layout_segmentation_governance"]
    facility_gov = ["public_facility_semantic_correction_governance"]

    cases: List[Dict[str, Any]] = [
        _case(
            case_id="RV_TEXT_CLEAR_SIGN",
            case_type="REAL_VIDEO_TEXT_CLEAR",
            expected_trigger="upper_sign_or_street_sign_roi",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["real_video_roi_noise"],
            expected_metrics=BASE_METRICS + ["positive_text_case_covered"],
            related_governance=gov_metrics,
            risk_coverage_metric="positive_text_case_covered",
            taxonomy_tags=["text_quality", "roi_quality"],
        ),
        _case(
            case_id="RV_TEXT_SMALL_FAR",
            case_type="REAL_VIDEO_TEXT_SMALL_FAR",
            expected_trigger="distant_sign_roi",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["small_far_text", "real_video_roi_noise"],
            expected_metrics=BASE_METRICS + ["low_quality_text_case_covered"],
            related_governance=gov_metrics,
            risk_coverage_metric="low_quality_text_case_covered",
            taxonomy_tags=["text_quality", "roi_quality"],
        ),
        _case(
            case_id="RV_TEXT_MOTION_BLUR",
            case_type="REAL_VIDEO_TEXT_MOTION_BLUR",
            expected_trigger="motion_blurred_frame_roi",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["motion_blur", "ocr_confidence_uncertain"],
            expected_metrics=BASE_METRICS + ["low_quality_text_case_covered"],
            related_governance=gov_metrics,
            risk_coverage_metric="low_quality_text_case_covered",
            taxonomy_tags=["motion_condition", "text_quality"],
        ),
        _case(
            case_id="RV_TEXT_LOW_LIGHT",
            case_type="REAL_VIDEO_TEXT_LOW_LIGHT",
            expected_trigger="low_light_frame_roi",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["low_light", "quality_risk"],
            expected_metrics=BASE_METRICS + ["low_quality_text_case_covered"],
            related_governance=gov_metrics,
            risk_coverage_metric="low_quality_text_case_covered",
            taxonomy_tags=["lighting_condition", "text_quality"],
        ),
        _case(
            case_id="RV_TEXT_REFLECTION_GLARE",
            case_type="REAL_VIDEO_TEXT_REFLECTION_GLARE",
            expected_trigger="glare_or_reflection_roi",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["reflection_glare", "false_positive_text_candidate"],
            expected_metrics=BASE_METRICS + ["false_positive_visual_roi_case_covered"],
            related_governance=gov_metrics,
            risk_coverage_metric="false_positive_visual_roi_case_covered",
            taxonomy_tags=["lighting_condition", "text_quality"],
        ),
        _case(
            case_id="RV_TEXT_PARTIAL_OCCLUSION",
            case_type="REAL_VIDEO_TEXT_PARTIAL_OCCLUSION",
            expected_trigger="partially_occluded_sign_roi",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["partial_occlusion", "partial_text_risk"],
            expected_metrics=BASE_METRICS + ["partial_text_case_covered"],
            related_governance=gov_metrics,
            risk_coverage_metric="partial_text_case_covered",
            taxonomy_tags=["text_quality", "roi_quality"],
        ),
        _case(
            case_id="RV_TEXT_MULTI_LINE_SIGN",
            case_type="REAL_VIDEO_TEXT_MULTI_LINE",
            expected_trigger="multi_line_sign_roi",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["multi_line_text_risk"],
            expected_metrics=BASE_METRICS + ["multi_line_text_case_covered"],
            related_governance=gov_metrics,
            risk_coverage_metric="multi_line_text_case_covered",
            taxonomy_tags=["text_quality", "layout_complexity"],
        ),
        _case(
            case_id="RV_TEXT_MIXED_CN_EN",
            case_type="REAL_VIDEO_TEXT_MIXED_CN_EN",
            expected_trigger="mixed_language_sign_roi",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["mixed_language_text_risk"],
            expected_metrics=BASE_METRICS + ["mixed_language_case_covered"],
            related_governance=gov_metrics,
            risk_coverage_metric="mixed_language_case_covered",
            taxonomy_tags=["text_quality"],
        ),
        _case(
            case_id="RV_POSTER_COMPLEX_LAYOUT",
            case_type="REAL_VIDEO_POSTER_COMPLEX_LAYOUT",
            expected_trigger="poster_like_frame_or_roi",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["poster_layout_complexity", "reading_order_uncertain"],
            expected_metrics=BASE_METRICS + POSTER_METRICS,
            related_governance=gov_metrics + poster_gov,
            risk_coverage_metric="false_positive_visual_roi_case_covered",
            taxonomy_tags=["poster_commercial_context", "layout_complexity"],
        ),
        _case(
            case_id="RV_POSTER_PRICE_PROMO",
            case_type="REAL_VIDEO_POSTER_PRICE_PROMO",
            expected_trigger="price_or_promo_region",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["commercial_text_may_expire", "poster_layout_complexity"],
            expected_metrics=BASE_METRICS + POSTER_METRICS,
            related_governance=gov_metrics + poster_gov,
            risk_coverage_metric="false_positive_visual_roi_case_covered",
            taxonomy_tags=["poster_commercial_context"],
        ),
        _case(
            case_id="RV_POSTER_QR_LOGO_MIXED",
            case_type="REAL_VIDEO_POSTER_QR_LOGO_MIXED",
            expected_trigger="qr_or_logo_zone_in_poster",
            expected_evidence_type="visual_symbol_candidate",
            expected_risk_flags=["visual_symbol_not_plain_text", "qr_not_ocr_text"],
            expected_metrics=BASE_METRICS + POSTER_METRICS,
            related_governance=gov_metrics + poster_gov,
            risk_coverage_metric="false_positive_visual_roi_case_covered",
            taxonomy_tags=["poster_commercial_context", "layout_complexity"],
        ),
        _case(
            case_id="RV_FACILITY_RESTROOM_SIGN",
            case_type="REAL_VIDEO_FACILITY_RESTROOM",
            expected_trigger="restroom_facility_sign",
            expected_evidence_type="FacilitySemanticCandidate",
            expected_risk_flags=["public_facility_symbol_text_mismatch", "ocr_typo_auxiliary_only"],
            expected_metrics=BASE_METRICS,
            related_governance=gov_metrics + facility_gov,
            risk_coverage_metric="positive_text_case_covered",
            taxonomy_tags=["public_facility_semantics"],
        ),
        _case(
            case_id="RV_FACILITY_EXIT_SIGN",
            case_type="REAL_VIDEO_FACILITY_EXIT",
            expected_trigger="exit_facility_sign",
            expected_evidence_type="FacilitySemanticCandidate",
            expected_risk_flags=["public_facility_symbol_text_mismatch"],
            expected_metrics=BASE_METRICS,
            related_governance=gov_metrics + facility_gov,
            risk_coverage_metric="positive_text_case_covered",
            taxonomy_tags=["public_facility_semantics"],
        ),
        _case(
            case_id="RV_FACILITY_ELEVATOR_SIGN",
            case_type="REAL_VIDEO_FACILITY_ELEVATOR",
            expected_trigger="elevator_facility_sign",
            expected_evidence_type="FacilitySemanticCandidate",
            expected_risk_flags=["public_facility_symbol_text_mismatch"],
            expected_metrics=BASE_METRICS,
            related_governance=gov_metrics + facility_gov,
            risk_coverage_metric="positive_text_case_covered",
            taxonomy_tags=["public_facility_semantics"],
        ),
        _case(
            case_id="RV_DUPLICATE_TEXT_ACROSS_FRAMES",
            case_type="REAL_VIDEO_DUPLICATE_TEXT",
            expected_trigger="same_text_multi_frame",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["duplicate_text_across_frames"],
            expected_metrics=BASE_METRICS + ["duplicate_text_case_covered"],
            related_governance=gov_metrics,
            risk_coverage_metric="duplicate_text_case_covered",
            taxonomy_tags=["temporal_consistency"],
        ),
        _case(
            case_id="RV_CONFLICTING_TEXT_ACROSS_REGIONS",
            case_type="REAL_VIDEO_CONFLICTING_TEXT",
            expected_trigger="conflicting_adjacent_rois",
            expected_evidence_type="layout_text_evidence_candidate",
            expected_risk_flags=["conflicting_text_across_regions"],
            expected_metrics=BASE_METRICS + ["conflicting_text_case_covered"],
            related_governance=gov_metrics,
            risk_coverage_metric="conflicting_text_case_covered",
            taxonomy_tags=["conflict_condition", "layout_complexity"],
        ),
    ]

    return {
        "schema_version": REGISTRY_SCHEMA,
        "phase": PHASE_ID,
        "case_count": len(cases),
        "cases": cases,
    }


def build_taxonomy(registry: Dict[str, Any]) -> Dict[str, Any]:
    cases = registry.get("cases") if isinstance(registry.get("cases"), list) else []
    by_tag: Dict[str, List[str]] = {}
    for c in cases:
        if not isinstance(c, dict):
            continue
        for tag in c.get("taxonomy_tags") or []:
            by_tag.setdefault(str(tag), []).append(c["case_id"])

    defs = [
        ("text_quality", "Readable text under real-world capture conditions", "ocr_quality"),
        ("layout_complexity", "Multi-region or poster-like layout", "layout"),
        ("temporal_consistency", "Cross-frame text stability", "temporal"),
        ("public_facility_semantics", "Facility signs; semantic-first path", "facility"),
        ("poster_commercial_context", "Poster/ad ROI; segment-first governance", "poster"),
        ("roi_quality", "ROI proposal quality and mis-crop risk", "roi"),
        ("lighting_condition", "Low light, glare, reflection", "lighting"),
        ("motion_condition", "Motion blur and frame instability", "motion"),
        ("conflict_condition", "Conflicting text across regions", "conflict"),
    ]
    categories = []
    for tid, desc, dim in defs:
        categories.append(
            {
                "taxonomy_id": tid,
                "description": desc,
                "case_ids": by_tag.get(tid, []),
                "risk_dimension": dim,
                "metrics_dimension": dim,
            }
        )
    return {"schema_version": TAXONOMY_SCHEMA, "category_count": len(categories), "categories": categories}


def build_sampling_policy_stub() -> Dict[str, Any]:
    return {
        "schema_version": SAMPLING_SCHEMA,
        "sample_mode": "registry_only_no_sampling",
        "real_video_loaded": False,
        "frame_sampling_enabled": False,
        "suggested_future_sampling_modes": [
            "fixed_interval",
            "keyframe_candidate",
            "roi_triggered",
            "scene_change_triggered",
            "text_density_triggered",
        ],
        "sample_metadata_fields": [
            "video_id",
            "frame_id",
            "timestamp_ms",
            "stream_id",
            "frame_quality",
            "motion_blur_score_placeholder",
            "lighting_score_placeholder",
            "roi_quality_score_placeholder",
        ],
    }


def _behavior_row(case: Dict[str, Any]) -> Dict[str, Any]:
    cid = case["case_id"]
    ctype = case["case_type"]
    is_poster = ctype.startswith("REAL_VIDEO_POSTER")
    is_facility = ctype.startswith("REAL_VIDEO_FACILITY")
    is_duplicate = "DUPLICATE" in cid
    is_conflict = "CONFLICTING" in cid
    is_non_text_uncertain = ctype in ("REAL_VIDEO_POSTER_QR_LOGO_MIXED",)

    return {
        "case_id": cid,
        "should_generate_ocr_request": False if is_facility else (not is_non_text_uncertain),
        "should_invoke_rapidocr_later": False if is_facility else True,
        "should_use_poster_governance": is_poster,
        "should_use_public_facility_governance": is_facility,
        "should_generate_reference_only_later": not is_facility,
        "should_generate_fusion_candidate_later": not is_facility and not is_duplicate,
        "should_require_review": is_conflict or is_poster,
        "should_write_fact": False,
        "should_invoke_navigation": False,
        "expected_gate_decision": "hold_for_review_or_no_write",
    }


def build_expected_behavior_matrix(registry: Dict[str, Any]) -> Dict[str, Any]:
    cases = registry.get("cases") if isinstance(registry.get("cases"), list) else []
    rows = [_behavior_row(c) for c in cases if isinstance(c, dict)]
    return {"schema_version": BEHAVIOR_SCHEMA, "row_count": len(rows), "rows": rows}


def build_metrics_binding_matrix(registry: Dict[str, Any]) -> Dict[str, Any]:
    cases = registry.get("cases") if isinstance(registry.get("cases"), list) else []
    rows = []
    for c in cases:
        if not isinstance(c, dict):
            continue
        rows.append(
            {
                "case_id": c["case_id"],
                "bound_metrics": list(c.get("expected_metrics") or []),
                "risk_coverage_metric": c.get("risk_coverage_metric"),
                "performance_placeholders": PERF_PLACEHOLDER,
                "no_write_boundary_pass_rate_required": True,
            }
        )
    return {"schema_version": METRICS_BINDING_SCHEMA, "row_count": len(rows), "rows": rows}


def build_governance_link_report(registry: Dict[str, Any]) -> Dict[str, Any]:
    cases = registry.get("cases") if isinstance(registry.get("cases"), list) else []
    poster_cases = [c["case_id"] for c in cases if isinstance(c, dict) and "POSTER" in c.get("case_id", "")]
    facility_cases = [c["case_id"] for c in cases if isinstance(c, dict) and "FACILITY" in c.get("case_id", "")]
    return {
        "schema_version": GOVERNANCE_LINK_SCHEMA,
        "poster_governance_linked": True,
        "public_facility_governance_linked": True,
        "metrics_schema_linked": True,
        "metrics_collector_linked": True,
        "v0_closure_boundary_inherited": True,
        "links": [
            {
                "case_group": "poster_cases",
                "case_ids": poster_cases,
                "governance": "Poster Layout Segmentation Governance",
            },
            {
                "case_group": "facility_cases",
                "case_ids": facility_cases,
                "governance": "Public Facility Semantic Correction Governance",
            },
            {
                "case_group": "all_cases",
                "case_ids": [c["case_id"] for c in cases if isinstance(c, dict)],
                "governance": "Metrics Schema / Boundary Metrics / v0 no-write inheritance",
            },
        ],
    }


def build_non_goals_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_GOALS_SCHEMA,
        "explicit_non_goals": [
            "Does not load or read real video files in this phase",
            "Does not sample frames",
            "Does not run OCR or Vision providers",
            "Does not generate OCR evidence or fusion candidates",
            "Does not generate Scene Delta candidates",
            "Does not write facts, Scene Delta, or WorldModel",
            "Does not make navigation decisions or auto-approve",
            "Does not claim real-scene generalization, OCR benchmark, or performance SLA",
        ],
    }


def build_risk_register(registry: Dict[str, Any]) -> Dict[str, Any]:
    cases = registry.get("cases") if isinstance(registry.get("cases"), list) else []
    id_list = {c["case_id"]: c for c in cases if isinstance(c, dict)}

    def _ids(*prefixes: str) -> List[str]:
        out = []
        for cid in id_list:
            if any(p in cid for p in prefixes):
                out.append(cid)
        return out

    risks = [
        ("real_video_roi_noise", "Unstable ROI on real frames", ["RV_TEXT_CLEAR_SIGN", "RV_TEXT_SMALL_FAR"], "roi_quality_score_placeholder"),
        ("small_far_text", "Distant small text", ["RV_TEXT_SMALL_FAR"], "ocr_empty_text_count"),
        ("motion_blur", "Motion blur degrades OCR", ["RV_TEXT_MOTION_BLUR"], "ocr_empty_text_count"),
        ("low_light", "Low light capture", ["RV_TEXT_LOW_LIGHT"], "ocr_empty_text_count"),
        ("reflection_glare", "Glare/reflection false reads", ["RV_TEXT_REFLECTION_GLARE"], "false_positive_text_rate"),
        ("partial_occlusion", "Partially hidden text", ["RV_TEXT_PARTIAL_OCCLUSION"], "partial_text_case_covered"),
        ("poster_layout_complexity", "Poster layout in video ROI", ["RV_POSTER_COMPLEX_LAYOUT"], "segment_first_required_count"),
        ("public_facility_symbol_text_mismatch", "Icon vs OCR text mismatch", ["RV_FACILITY_RESTROOM_SIGN"], "facility_semantic_candidate"),
        ("duplicate_text_across_frames", "Repeated text inflates confidence", ["RV_DUPLICATE_TEXT_ACROSS_FRAMES"], "duplicate_text_case_covered"),
        ("conflicting_text_across_regions", "Adjacent region conflict", ["RV_CONFLICTING_TEXT_ACROSS_REGIONS"], "conflicting_text_case_covered"),
        ("roi_mis_crop", "ROI mis-alignment", _ids("RV_TEXT"), "roi_quality_score_placeholder"),
        ("false_positive_text_candidate", "Non-text reads as text", ["RV_TEXT_REFLECTION_GLARE"], "false_positive_visual_roi_case_covered"),
        ("performance_overhead", "Multi-frame cost", list(id_list.keys()), "performance_metrics_available"),
    ]
    return {
        "schema_version": RISK_SCHEMA,
        "risks": [
            {
                "risk_id": rid,
                "description": desc,
                "related_case_ids": rids,
                "mitigation": "registry_governance_and_metrics_binding",
                "metrics_to_watch": [mwatch],
            }
            for rid, desc, rids, mwatch in risks
        ],
    }


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "realvideo_case_registry_executed": True,
        "registry_only": True,
        "real_video_loaded": False,
        "frame_sampled": False,
        "runtime_execution": False,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
        "ai_interpretation_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }


def build_summary(
    *,
    v1_planning_root: Path,
    metrics_collector_root: Path,
    poster_governance_root: Path,
    public_facility_governance_root: Path,
    case_count: int,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "registry_scope": "case_registry_only",
        "based_on_v1_planning": v1_planning_root.is_dir(),
        "based_on_metrics_collector": metrics_collector_root.is_dir(),
        "based_on_poster_governance": poster_governance_root.is_dir(),
        "based_on_public_facility_governance": public_facility_governance_root.is_dir(),
        "v1_planning_root": str(v1_planning_root),
        "metrics_collector_root": str(metrics_collector_root),
        "poster_governance_root": str(poster_governance_root),
        "public_facility_governance_root": str(public_facility_governance_root),
        "case_count": case_count,
        "real_video_loaded": False,
        "frame_sampled": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "fact_status_default": "not_fact",
        "write_allowed_default": False,
    }


def run_cross_modal_vision_ocr_realvideo_case_registry_v0(
    *,
    v1_planning_root: str,
    metrics_collector_root: str,
    poster_governance_root: str,
    public_facility_governance_root: str,
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
    List[str],
]:
    errs: List[str] = []
    v1 = Path(v1_planning_root).resolve()
    mc = Path(metrics_collector_root).resolve()
    poster = Path(poster_governance_root).resolve()
    facility = Path(public_facility_governance_root).resolve()

    if not _read_json(v1 / "cross_modal_vision_ocr_testboard_v1_planning_summary.json"):
        errs.append("missing_v1_planning_summary")
    if not _read_json(mc / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json"):
        errs.append("missing_metrics_collector_summary")
    if not _read_json(poster / "poster_layout_governance_summary.json"):
        errs.append("missing_poster_governance_summary")
    if not _read_json(facility / "public_facility_semantic_correction_governance_summary.json"):
        errs.append("missing_public_facility_governance_summary")

    registry = build_case_registry()
    if registry["case_count"] < 15:
        errs.append("case_count_below_15")

    taxonomy = build_taxonomy(registry)
    sampling = build_sampling_policy_stub()
    behavior = build_expected_behavior_matrix(registry)
    metrics_binding = build_metrics_binding_matrix(registry)
    gov_link = build_governance_link_report(registry)
    non_goals = build_non_goals_report()
    risks = build_risk_register(registry)
    audit = build_audit()

    summary = build_summary(
        v1_planning_root=v1,
        metrics_collector_root=mc,
        poster_governance_root=poster,
        public_facility_governance_root=facility,
        case_count=int(registry["case_count"]),
    )
    phase_verdict = "GO" if not errs else ("CONDITIONAL_GO" if registry["case_count"] >= 12 else "NO_GO")
    summary["phase_verdict_hint"] = phase_verdict
    summary["errors"] = list(errs)

    return (
        summary,
        registry,
        taxonomy,
        sampling,
        behavior,
        metrics_binding,
        gov_link,
        non_goals,
        risks,
        audit,
        errs,
    )
