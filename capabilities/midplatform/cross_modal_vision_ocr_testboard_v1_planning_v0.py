# -*- coding: utf-8 -*-
"""CrossModal Vision-OCR TestBoard v1 planning (scope freeze only, no implementation).

Phase-CrossModal-Vision-OCR-TestBoard-v1-Planning-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_v1_planning_summary_v0"
TRACK_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_v1_track_matrix_v0"
PHASE_ROADMAP_SCHEMA = "cross_modal_vision_ocr_testboard_v1_phase_roadmap_v0"
NON_GOALS_SCHEMA = "cross_modal_vision_ocr_testboard_v1_non_goals_report_v0"
RISK_REGISTER_SCHEMA = "cross_modal_vision_ocr_testboard_v1_risk_register_v0"
GATE_POLICY_SCHEMA = "cross_modal_vision_ocr_testboard_v1_gate_policy_v0"
EXECUTION_ORDER_SCHEMA = "cross_modal_vision_ocr_testboard_v1_execution_order_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_v1_planning_audit_v0"


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def build_track_matrix() -> Dict[str, Any]:
    tracks = [
        {
            "track_id": "TVOCR_V1_A_REAL_VIDEO",
            "track_name": "real_video_cases",
            "purpose": "Extend from synthetic fixtures to real video frames and natural-scene ROI evaluation.",
            "entry_requirements": [
                "TestBoard v0 closed_for_v0 with 10/10 executed cases",
                "v0 no-write / not_fact / blocked_by_gate boundaries intact",
                "ocr_mainline_bridge_v0 evaluation-only path available",
            ],
            "planned_phases": [
                "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001",
                "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001",
                "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001",
                "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-Closure-001",
            ],
            "exit_criteria": [
                "Real-video case registry frozen with frame/ROI metadata",
                "Multi-frame smoke cases executed evaluation-only",
                "ROI-to-OCR reference matrix produced without fact writes",
                "Track closure audit: not_fact, no_write, no WorldModel",
            ],
            "non_claims": [
                "Does not validate navigation decisions",
                "Does not confirm real merchant/business status",
                "Does not represent production-grade OCR benchmark",
                "Does not authorize writing repeated text to WorldModel",
            ],
            "priority": 2,
            "in_scope": [
                "Real video frame sampling",
                "upper_sign / poster-like / street sign ROI from real frames",
                "Natural empty vs non-empty text distribution",
                "Inter-frame duplicate text",
                "Motion blur, lighting change, occlusion, ROI mis-cut cases",
            ],
            "out_of_scope": [
                "Navigation decisions",
                "WorldModel writes",
                "Production benchmark (track C owns metrics framework)",
            ],
        },
        {
            "track_id": "TVOCR_V1_B_POSTER_LAYOUT",
            "track_name": "poster_layout_segmentation_governance",
            "purpose": "Govern poster/announcement/ad complex layouts before regional OCR; no default full-image OCR.",
            "entry_requirements": [
                "v0 poster-class lessons from FALSE_POSITIVE / MIXED_CN_EN cases",
                "OCR image input governance config available",
                "explicit full_image_ocr_allowed=false policy slot",
            ],
            "planned_phases": [
                "Phase-OCR-Poster-Layout-Segmentation-Governance-001",
                "Phase-OCR-Poster-Region-OCR-Plan-Stub-001",
                "Phase-OCR-Poster-VisualSymbolEvidence-Stub-001",
                "Phase-CrossModal-Poster-OCR-ReferenceOnly-001",
                "Phase-Poster-TestBoard-Closure-001",
            ],
            "exit_criteria": [
                "poster_like classification and layout_complexity gates defined",
                "ocr_region_plan and reading_order_candidate stubs produced",
                "full_image_ocr_allowed=false enforced as default",
                "Reference-only poster OCR path without fact writes",
            ],
            "non_claims": [
                "Does not solve all artistic/stylized fonts",
                "Does not write ad copy to fact layer",
                "Does not treat logos as OCR text targets",
                "Does not authorize full-image poster OCR as primary path",
            ],
            "priority": 1,
            "in_scope": [
                "poster_like image classification",
                "text_density / layout_complexity assessment",
                "non_text region filtering",
                "visual_symbol_candidate",
                "title/body/price/time/location/qr/logo region planning",
                "ocr_region_plan",
                "reading_order_candidate",
                "commercial_text_may_expire risk flag",
            ],
            "out_of_scope": [
                "Default whole-image OCR as main path",
                "Fact-layer ad copy persistence",
                "Logo-as-text OCR",
            ],
        },
        {
            "track_id": "TVOCR_V1_C_BENCHMARK_PERFORMANCE",
            "track_name": "benchmark_performance_layer",
            "purpose": "Establish measurement schema and collectors without changing chain write capabilities.",
            "entry_requirements": [
                "Frozen v0 case matrix as baseline reference",
                "Track A/B fixtures may feed metrics but metrics phase does not own fixture creation",
            ],
            "planned_phases": [
                "Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001",
                "Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Collector-Smoke-001",
                "Phase-CrossModal-Vision-OCR-TestBoard-Regression-Comparison-001",
                "Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Closure-001",
            ],
            "exit_criteria": [
                "Metrics schema frozen (rates, latency, boundary violations)",
                "Collector smoke passes evaluation-only audit",
                "Regression comparison harness documented",
                "Metrics closure: no production performance promise",
            ],
            "non_claims": [
                "Does not make production performance commitments",
                "Does not replace formal Evaluation Platform",
                "Does not serve as final model-selection verdict",
            ],
            "priority": 2,
            "in_scope": [
                "OCR non_empty_rate",
                "empty_text_rate",
                "false_positive_text_rate",
                "text_item_count",
                "per-case latency",
                "provider distribution",
                "boundary_violation_count",
                "no-write audit pass rate",
                "repeatability / regression comparison",
            ],
            "out_of_scope": [
                "Production SLA promises",
                "Policy auto-approve",
                "Model selection final ruling",
            ],
        },
    ]
    return {
        "schema_version": TRACK_MATRIX_SCHEMA,
        "row_count": len(tracks),
        "tracks": tracks,
        "independence_rules": [
            "Track A owns real video fixtures; must not merge poster segmentation logic.",
            "Track B owns poster governance path; full_image_ocr_allowed defaults false.",
            "Track C owns metrics only; must not block A/B design or substitute formal eval platform.",
        ],
    }


def build_phase_roadmap() -> Dict[str, Any]:
    return {
        "schema_version": PHASE_ROADMAP_SCHEMA,
        "tracks": {
            "TVOCR_V1_A_REAL_VIDEO": [
                {
                    "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001",
                    "goal": "Freeze real-video case registry and ROI taxonomy",
                },
                {
                    "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001",
                    "goal": "Smoke sample frames with evaluation-only OCR bridge",
                },
                {
                    "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001",
                    "goal": "Reference matrix vision ROI → OCR request (no writes)",
                },
                {
                    "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-Closure-001",
                    "goal": "Close track A with audit and non-claims",
                },
            ],
            "TVOCR_V1_B_POSTER_LAYOUT": [
                {
                    "phase_id": "Phase-OCR-Poster-Layout-Segmentation-Governance-001",
                    "goal": "Governance + layout segmentation rules for poster-class images",
                },
                {
                    "phase_id": "Phase-OCR-Poster-Region-OCR-Plan-Stub-001",
                    "goal": "Per-region ocr_region_plan stubs",
                },
                {
                    "phase_id": "Phase-OCR-Poster-VisualSymbolEvidence-Stub-001",
                    "goal": "VisualSymbolEvidence dry-run stubs (not facts)",
                },
                {
                    "phase_id": "Phase-CrossModal-Poster-OCR-ReferenceOnly-001",
                    "goal": "Reference-only regional OCR path",
                },
                {
                    "phase_id": "Phase-Poster-TestBoard-Closure-001",
                    "goal": "Poster track closure",
                },
            ],
            "TVOCR_V1_C_BENCHMARK_PERFORMANCE": [
                {
                    "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001",
                    "goal": "Freeze metrics schema",
                },
                {
                    "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Collector-Smoke-001",
                    "goal": "Collector smoke on frozen fixtures",
                },
                {
                    "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-Regression-Comparison-001",
                    "goal": "Regression comparison harness",
                },
                {
                    "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Closure-001",
                    "goal": "Metrics track closure",
                },
            ],
        },
    }


def build_non_goals_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_GOALS_SCHEMA,
        "explicit_non_goals": [
            "No MidPlatform fact-layer writes",
            "No Scene Delta writes",
            "No WorldModel writes",
            "No navigation decisions",
            "No auto-approval",
            "No production executor attachment",
            "No claim of real-scene generalization completion",
            "No claim of OCR benchmark completion",
            "No claim of performance SLA compliance",
            "Does not solve all poster complex layout cases",
        ],
        "write_policy": {
            "midplatform_fact_write": False,
            "scene_delta_write": False,
            "world_model_write": False,
            "navigation_decision": False,
            "auto_approval": False,
        },
        "v1_planning_phase_non_goals": [
            "No new production capabilities in planning phase",
            "No OCR execution in planning phase",
            "No Vision provider execution in planning phase",
            "Do not treat planning artifacts as implementation GO",
        ],
    }


def build_risk_register() -> Dict[str, Any]:
    risks = [
        {
            "risk_id": "real_video_roi_noise",
            "risk_name": "Real video ROI noise",
            "description": "Real frames produce unstable or misaligned ROIs vs synthetic fixtures.",
            "mitigation": "Case registry with ROI mis-cut and occlusion tags; evaluation-only reference matrix.",
            "related_track": "TVOCR_V1_A_REAL_VIDEO",
        },
        {
            "risk_id": "poster_layout_complexity",
            "risk_name": "Poster layout complexity",
            "description": "Dense multi-column poster layouts break naive single-ROI OCR.",
            "mitigation": "Governance-first segmentation; ocr_region_plan per zone; full_image_ocr_allowed=false.",
            "related_track": "TVOCR_V1_B_POSTER_LAYOUT",
        },
        {
            "risk_id": "reading_order_uncertainty",
            "risk_name": "Reading order uncertainty",
            "description": "Ambiguous reading order on posters may mis-associate text blocks.",
            "mitigation": "reading_order_candidate as non-fact stub; no auto-approve from order alone.",
            "related_track": "TVOCR_V1_B_POSTER_LAYOUT",
        },
        {
            "risk_id": "commercial_text_expiry",
            "risk_name": "Commercial text expiry",
            "description": "Promotional copy may be stale; must not become durable facts.",
            "mitigation": "commercial_text_may_expire flag; blocked_by_gate; not_fact default.",
            "related_track": "TVOCR_V1_B_POSTER_LAYOUT",
        },
        {
            "risk_id": "visual_symbol_ocr_confusion",
            "risk_name": "Visual symbol OCR confusion",
            "description": "Logos/icons mistaken for text regions or vice versa.",
            "mitigation": "visual_symbol_candidate path; non_text filtering; logo not OCR target.",
            "related_track": "TVOCR_V1_B_POSTER_LAYOUT",
        },
        {
            "risk_id": "duplicate_text_across_frames",
            "risk_name": "Duplicate text across frames",
            "description": "Same sign text in consecutive frames may inflate confidence.",
            "mitigation": "Track A duplicate-frame cases; forbid WorldModel write from repetition.",
            "related_track": "TVOCR_V1_A_REAL_VIDEO",
        },
        {
            "risk_id": "conflicting_text_across_regions",
            "risk_name": "Conflicting text across regions",
            "description": "Adjacent regions may yield incompatible OCR strings.",
            "mitigation": "Carry v0 CONFLICTING_TEXT_ROI pattern; fusion remains not_fact.",
            "related_track": "TVOCR_V1_A_REAL_VIDEO",
        },
        {
            "risk_id": "performance_overhead",
            "risk_name": "Performance overhead",
            "description": "Multi-frame and multi-region paths increase latency and resource use.",
            "mitigation": "Track C metrics only; no production SLA in v1.",
            "related_track": "TVOCR_V1_C_BENCHMARK_PERFORMANCE",
        },
        {
            "risk_id": "provider_variability",
            "risk_name": "Provider variability",
            "description": "OCR provider/version drift changes observed text without code changes.",
            "mitigation": "provider distribution metric; regression comparison harness.",
            "related_track": "TVOCR_V1_C_BENCHMARK_PERFORMANCE",
        },
        {
            "risk_id": "false_confidence_from_ai_interpretation",
            "risk_name": "False confidence from AI interpretation",
            "description": "Downstream interpretation may treat OCR candidates as ground truth.",
            "mitigation": "fact_status=not_fact; no_auto_approval; explicit non-claims on all tracks.",
            "related_track": "TVOCR_V1_A_REAL_VIDEO",
        },
    ]
    return {"schema_version": RISK_REGISTER_SCHEMA, "risk_count": len(risks), "risks": risks}


def build_gate_policy() -> Dict[str, Any]:
    return {
        "schema_version": GATE_POLICY_SCHEMA,
        "default_for_all_v1_phases": {
            "evaluation_only": True,
            "write_allowed": False,
            "fact_status": "not_fact",
            "no_auto_approval": True,
            "no_navigation_decision": True,
        },
        "track_policies": {
            "TVOCR_V1_A_REAL_VIDEO": {
                "world_model_write_from_duplicate_text": False,
                "navigation_decision_allowed": False,
            },
            "TVOCR_V1_B_POSTER_LAYOUT": {
                "full_image_ocr_allowed_default": False,
                "ad_copy_fact_write_allowed": False,
                "logo_as_ocr_text_allowed": False,
            },
            "TVOCR_V1_C_BENCHMARK_PERFORMANCE": {
                "may_substitute_formal_eval_platform": False,
                "production_performance_promise_allowed": False,
            },
        },
        "closure_rules": [
            "No track may enter downstream write chain before track closure audit passes.",
            "Poster track must keep full_image_ocr_allowed=false unless explicit future phase overrides with governance.",
            "Benchmark track metrics are observational only.",
        ],
    }


def build_execution_order() -> Dict[str, Any]:
    steps = [
        {
            "order": 1,
            "phase_id": "Phase-OCR-Poster-Layout-Segmentation-Governance-001",
            "track_id": "TVOCR_V1_B_POSTER_LAYOUT",
        },
        {
            "order": 2,
            "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001",
            "track_id": "TVOCR_V1_C_BENCHMARK_PERFORMANCE",
        },
        {
            "order": 3,
            "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001",
            "track_id": "TVOCR_V1_A_REAL_VIDEO",
        },
        {
            "order": 4,
            "phase_id": "Phase-OCR-Poster-Region-OCR-Plan-Stub-001",
            "track_id": "TVOCR_V1_B_POSTER_LAYOUT",
        },
        {
            "order": 5,
            "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001",
            "track_id": "TVOCR_V1_A_REAL_VIDEO",
        },
        {
            "order": 6,
            "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Collector-Smoke-001",
            "track_id": "TVOCR_V1_C_BENCHMARK_PERFORMANCE",
        },
        {
            "order": 7,
            "phase_id": "Phase-OCR-Poster-VisualSymbolEvidence-Stub-001",
            "track_id": "TVOCR_V1_B_POSTER_LAYOUT",
        },
        {
            "order": 8,
            "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001",
            "track_id": "TVOCR_V1_A_REAL_VIDEO",
        },
        {
            "order": 9,
            "phase_id": "Phase-CrossModal-Vision-OCR-TestBoard-Regression-Comparison-001",
            "track_id": "TVOCR_V1_C_BENCHMARK_PERFORMANCE",
        },
        {
            "order": 10,
            "phase_id": "v1_track_closures",
            "track_id": "ALL",
            "includes": [
                "Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-Closure-001",
                "Phase-Poster-TestBoard-Closure-001",
                "Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Closure-001",
            ],
        },
    ]
    return {
        "schema_version": EXECUTION_ORDER_SCHEMA,
        "recommended_execution_order": steps,
        "rationale": (
            "Establish poster governance and metrics schema before real-video expansion; "
            "otherwise poster-like frames in real video cannot be evaluated consistently."
        ),
    }


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "cross_modal_vision_ocr_testboard_v1_planning_executed": True,
        "planning_only": True,
        "v1_scope_locked": True,
        "no_runtime_execution": True,
        "no_ocr_invoked": True,
        "no_vision_provider_invoked": True,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }


def run_cross_modal_vision_ocr_testboard_v1_planning_v0(
    *,
    v0_closure_root: str,
) -> Tuple[
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
    v0 = Path(v0_closure_root).resolve()

    v0_summary = _read_json(v0 / "cross_modal_vision_ocr_testboard_v0_closure_summary.json")
    if not v0_summary:
        errs.append("missing_v0_closure_summary")
    elif v0_summary.get("testboard_status") != "closed_for_v0":
        errs.append("v0_not_closed_for_v0")

    based_on = (v0_summary or {}).get("testboard_status", "closed_for_v0")
    if based_on != "closed_for_v0":
        based_on = "closed_for_v0" if not errs else based_on

    track_matrix = build_track_matrix()
    phase_roadmap = build_phase_roadmap()
    non_goals = build_non_goals_report()
    risk_register = build_risk_register()
    gate_policy = build_gate_policy()
    execution_order = build_execution_order()
    audit = build_audit()

    phase_verdict = "GO" if not errs else "CONDITIONAL_GO"
    if "v0_not_closed_for_v0" in errs:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-v1-Planning-001",
        "planning_status": "planned",
        "based_on_v0_status": based_on,
        "v0_closure_root": str(v0),
        "v1_scope_locked": True,
        "v1_tracks": [
            "real_video_cases",
            "poster_layout_segmentation_governance",
            "benchmark_performance_layer",
        ],
        "write_policy": {
            "midplatform_fact_write_allowed": False,
            "scene_delta_write_allowed": False,
            "world_model_write_allowed": False,
            "navigation_decision_allowed": False,
            "auto_approval_allowed": False,
        },
        "v1_track_count": 3,
        "v1_implementation_in_this_phase": False,
        "recommended_first_track": "poster_layout_segmentation_governance",
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return (
        summary,
        track_matrix,
        phase_roadmap,
        non_goals,
        risk_register,
        gate_policy,
        execution_order,
        audit,
        errs,
    )
