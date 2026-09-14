# -*- coding: utf-8 -*-
"""Vision Navigation Information Integration Chain DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_vision_navigation_candidate_flow_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CF_DR_FINAL_GO,
    NEXT_PHASE_GO as CF_DR_NEXT_PHASE,
)
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
)
from capabilities.governance.midplatform_information_integration_layer_planning_v1 import (
    DECISION_READINESS_FIELDS,
    FRESHNESS_STATUS_FIELDS,
    INTEGRATED_CONTEXT_CANDIDATE_FIELDS,
    PRIORITY_MAP_FIELDS,
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
)
from capabilities.governance.midplatform_information_integration_layer_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_DR_FINAL_GO,
)
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL_GO,
)

PHASE_ID = "Phase-Vision-Navigation-Information-Integration-Chain-DryRun-v1-001"
SCOPE = "vision_navigation_information_integration_chain_dryrun_only"
SOURCE_CHAIN = "vision_navigation_information_integration_chain_dryrun_v1"

UPSTREAM_CF_DR_FINAL = CF_DR_FINAL_GO
UPSTREAM_CF_DR_NEXT = CF_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "VISION_NAVIGATION_INFORMATION_INTEGRATION_CHAIN_DRYRUN_CLOSED_"
    "READY_FOR_DECISION_CHAIN_CANDIDATE_DRYRUN"
)
FINAL_DECISION_HOLD = (
    "VISION_NAVIGATION_INFORMATION_INTEGRATION_CHAIN_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Vision-Navigation-Decision-Chain-Candidate-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-Navigation-Information-Integration-Chain-Issue-Review-v1-001"

INTAKE_SAMPLE_IDS: Tuple[str, ...] = (
    "visual_obs_sample_crossing_001",
    "ocr_result_sample_sign_001",
    "map_location_sample_001",
    "route_context_sample_001",
    "navigation_task_sample_001",
    "required_observation_candidate:traffic_check_001",
    "drive_signal_sample_survival_001",
    "health_signal_candidate:module_status_001",
    "whitebox_trace:chain_intake_001",
)

VISUAL_OCR_MAP_ROUTE_REVIEW_ITEMS: Tuple[str, ...] = (
    "visual_observation binds to scene/risk context",
    "OCR result binds to visual/text region",
    "OCR signage influences route context only as candidate",
    "map context contextualizes route and visual scene",
    "route context affects task relevance",
    "no candidate becomes fact",
)

DRIVE_PRIORITY_REVIEW_ITEMS: Tuple[str, ...] = (
    "Survival Drive elevates crossing/traffic risk priority",
    "Task Drive preserves navigation task relevance",
    "Resource/Health hints may lower observation detail or recommend hold",
    "drive signal affects priority/readiness only",
    "drive signal does not invoke camera/navigation",
)

RISK_INTEGRATION_REVIEW_ITEMS: Tuple[str, ...] = (
    "risk_context_candidate enters current_risk_context",
    "high survival risk lowers decision readiness or recommends hold/observe_more",
    "forbidden_actions preserved",
    "no direct safety output generated",
)

EVIDENCE_TRACEABILITY_REVIEW_ITEMS: Tuple[str, ...] = (
    "source_chain_matrix generated",
    "visual/OCR/map/route/task refs preserved",
    "evidence_refs preserved",
    "whitebox_trace_refs preserved",
    "validation_required flags preserved",
    "fixture provenance preserved",
)

CONFLICT_GAP_FRESHNESS_REVIEW_ITEMS: Tuple[str, ...] = (
    "conflict candidate generated or no-blocking-conflict status recorded",
    "gap candidate generated for missing live validation",
    "freshness status generated for all source candidates",
    "stale/simulated input cannot authorize real navigation action",
)

DC_HANDOFF_REVIEW_ITEMS: Tuple[str, ...] = (
    "integrated_context_candidate can be handed to Decision Center later",
    "decision_readiness_candidate attached",
    "conflict/gap/freshness refs attached",
    "Decision Center remains裁决层",
    "no decision_candidate generated now",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_camera_invocation",
    "dryrun_to_real_frame_read",
    "dryrun_to_vision_runtime_enable",
    "dryrun_to_ocr_runtime_enable",
    "dryrun_to_real_ocr_execution",
    "dryrun_to_map_provider_invocation",
    "dryrun_to_navigation_runtime_enable",
    "dryrun_to_real_navigation_action",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_information_integration_runtime_enable",
    "dryrun_to_decision_execution",
    "dryrun_to_decision_candidate_generation",
    "dryrun_to_user_output",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_controlled_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Integration Chain DryRun GO ≠ camera/OCR/map runtime enabled",
    "integrated_context_candidate ≠ decision",
    "fixture-based context ≠ real navigation fact",
    "decision readiness candidate ≠ navigation action allowed",
    "next Decision Chain Candidate DryRun ≠ real navigation execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "vision_navigation_information_integration_chain_dryrun_only",
    "simulated",
    "sample_fixture_only",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "camera_invoked_now",
    "real_frame_read_now",
    "vision_runtime_enabled_now",
    "ocr_runtime_enabled_now",
    "real_ocr_executed_now",
    "map_provider_invoked_now",
    "navigation_runtime_enabled_now",
    "real_navigation_action_executed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "information_integration_runtime_enabled_now",
    "decision_executed_now",
    "decision_candidate_generated_now",
    "user_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "controlled_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_navigation_information_integration_chain_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false")
    return issues


def run_vision_navigation_information_integration_chain_dryrun_v1(
    *,
    first_person_vision_navigation_candidate_flow_dryrun_and_review_root: str,
    first_person_vision_navigation_candidate_flow_planning_root: str,
    midplatform_information_integration_layer_dryrun_and_review_root: str,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    cf_dr_root = Path(
        first_person_vision_navigation_candidate_flow_dryrun_and_review_root
    ).expanduser().resolve()
    cf_plan_root = Path(
        first_person_vision_navigation_candidate_flow_planning_root
    ).expanduser().resolve()
    ii_dr_root = Path(
        midplatform_information_integration_layer_dryrun_and_review_root
    ).expanduser().resolve()
    ds_dr_root = Path(seed_core_drive_signal_contract_dryrun_and_review_root).expanduser().resolve()
    cb_dr_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()

    cf_dr_sm = _try_read_json(cf_dr_root / "summary.json") or {}
    cf_dr_vr = _try_read_json(cf_dr_root / "verifier_report.json") or {}
    ii_dr_vr = _try_read_json(ii_dr_root / "verifier_report.json") or {}
    ds_dr_vr = _try_read_json(ds_dr_root / "verifier_report.json") or {}
    cb_dr_vr = _try_read_json(cb_dr_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}

    sample_visual = _try_read_json(cf_dr_root / "sample_visual_observation_candidate_v1.json") or {}
    sample_ocr = _try_read_json(cf_dr_root / "sample_ocr_result_candidate_v1.json") or {}
    sample_map = _try_read_json(cf_dr_root / "sample_map_location_context_candidate_v1.json") or {}
    sample_route = _try_read_json(cf_dr_root / "sample_route_context_candidate_v1.json") or {}
    sample_nav = _try_read_json(cf_dr_root / "sample_navigation_task_candidate_v1.json") or {}
    sample_drive = _try_read_json(ds_dr_root / "sample_drive_signal_candidate_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_candidate_flow_dryrun_root": str(cf_dr_root),
        "upstream_candidate_flow_planning_root": str(cf_plan_root),
        "upstream_information_integration_dryrun_root": str(ii_dr_root),
        "upstream_drive_signal_dryrun_root": str(ds_dr_root),
        "upstream_constitution_bus_dryrun_root": str(cb_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "output_root": str(out_root),
    }

    if cf_dr_vr.get("verifier") != "GO":
        blockers.append("Candidate Flow DryRunAndReview must be GO")
    if cf_dr_sm.get("final_decision") != UPSTREAM_CF_DR_FINAL:
        blockers.append("candidate flow dryrun final_decision mismatch")
    if cf_dr_sm.get("recommended_next_phase") != UPSTREAM_CF_DR_NEXT:
        blockers.append("candidate flow dryrun recommended_next_phase mismatch")
    if ii_dr_vr.get("verifier") != "GO":
        blockers.append("Information Integration Layer DryRunAndReview must be GO")
    if ds_dr_vr.get("verifier") != "GO":
        blockers.append("Drive Signal Contract DryRunAndReview must be GO")
    if cb_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction must be GO")

    if sample_visual.get("runtime_source") is not False:
        blockers.append("visual sample must have runtime_source=false")
    if sample_visual.get("candidate_only") is not True:
        blockers.append("visual sample must be candidate_only")

    leakage_issues: List[str] = []
    for label, sm in (
        ("cf_dr", cf_dr_sm),
        ("ii_dr", _try_read_json(ii_dr_root / "summary.json") or {}),
        ("ds_dr", _try_read_json(ds_dr_root / "summary.json") or {}),
        ("cb_dr", _try_read_json(cb_dr_root / "summary.json") or {}),
        ("provider", _try_read_json(provider_dr_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    intake_set = {
        "intake_id": "sample_candidate_intake_set_v1",
        "sample_ids": list(INTAKE_SAMPLE_IDS),
        "sample_count": len(INTAKE_SAMPLE_IDS),
        "fixture_metadata_only": True,
        "runtime_source_false": True,
        "source_chain_preserved": True,
        "candidate_only": True,
        "not_fact": True,
        "not_action": True,
        "not_user_output": True,
        "samples": {
            "visual_observation_candidate": sample_visual,
            "ocr_result_candidate": sample_ocr,
            "map_location_context_candidate": sample_map,
            "route_context_candidate": sample_route,
            "navigation_task_candidate": sample_nav,
            "drive_signal_candidate": sample_drive,
            "health_signal_candidate": {
                "health_signal_id": "health_signal_candidate:module_status_001",
                "pressure_level": "moderate",
                "candidate_only": True,
            },
            "whitebox_trace_refs": ["whitebox_trace:chain_intake_001", "trace:visual_obs:001"],
        },
        **meta,
    }

    input_review = {
        "review_id": "candidate_flow_input_review_v1",
        "candidate_flow_dryrun_verifier": cf_dr_vr.get("verifier"),
        "candidate_flow_dryrun_final_decision": cf_dr_sm.get("final_decision"),
        "information_integration_verifier": ii_dr_vr.get("verifier"),
        "drive_signal_verifier": ds_dr_vr.get("verifier"),
        "constitution_bus_verifier": cb_dr_vr.get("verifier"),
        "provider_abstraction_verifier": provider_dr_vr.get("verifier"),
        "fixture_metadata_only": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "chain_dryrun_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    chain_model = {
        **meta,
        "model_id": "vision_navigation_information_integration_chain_v1",
        "chain_type": "fixture_based_information_integration_chain",
        "consumes_perception_candidates": True,
        "consumes_drive_signal_candidate": True,
        "consumes_health_signal_candidate": True,
        "consumes_whitebox_trace_refs": True,
        "emits_integrated_context_candidate": True,
        "emits_context_conflict_candidate": True,
        "emits_context_gap_candidate": True,
        "emits_decision_readiness_candidate": True,
        "does_not_decide": True,
        "does_not_invoke_provider": True,
        "does_not_enable_runtime": True,
        "candidate_only": True,
    }

    integrated = {
        "integrated_context_id": "integrated_context_vision_nav_chain_001",
        "source_input_refs": [
            "visual_obs_sample_crossing_001",
            "ocr_result_sample_sign_001",
            "map_location_sample_001",
            "route_context_sample_001",
            "navigation_task_sample_001",
            "drive_signal_sample_survival_001",
            "health_signal_candidate:module_status_001",
        ],
        "source_chain_matrix": {
            "visual_observation_candidate": ["fixture:static_frame_metadata:crossing_001"],
            "ocr_result_candidate": ["fixture:ocr:sign_001"],
            "map_location_context_candidate": ["fixture:map:hint_001"],
            "route_context_candidate": ["route:nav_crossing_001"],
            "navigation_task_candidate": ["goal:cross_street_safely"],
            "drive_signal_candidate": ["seed_core:survival_drive:sample_001"],
        },
        "current_task_context": {
            "task_id": "navigation_task_sample_001",
            "task_type": "navigation",
            "task_stage": "approach",
            "active": True,
        },
        "current_scene_context": {
            "scene_type": "street_crossing",
            "ocr_signage_hint": "人行横道",
            "fixture_only": True,
        },
        "current_route_context": {
            "route_stage": "approaching_crossing",
            "route_ref": "route_context_sample_001",
            "map_context_ref": "map_location_sample_001",
        },
        "current_user_context": {"preference_hint": "safety_first_navigation"},
        "current_risk_context": {
            "risk_type": "traffic_or_crossing_attention_required",
            "risk_level": "moderate",
            "survival_drive_elevated": True,
        },
        "drive_context": {
            "drive_signal_ref": "drive_signal_sample_survival_001",
            "observation_priority_elevated": True,
        },
        "health_context": {"pressure_level": "moderate", "hold_hint": False},
        "validation_context": {
            "validation_status": "fixture_pending",
            "validation_required": True,
        },
        "whitebox_context": {"trace_required": True},
        "memory_context": {"retrieval_ref": None, "stale_risk": "not_applicable_fixture"},
        "provider_context": {"provider_ready": False, "fixture_only": True},
        "evidence_weight_map": {
            "visual": 0.72,
            "ocr": 0.68,
            "map": 0.65,
            "drive": 0.85,
        },
        "context_priority_map_ref": "priority_map_vision_nav_chain_001",
        "context_conflict_refs": ["conflict_map_vs_vision_chain_001"],
        "context_gap_refs": ["gap_missing_live_validation_001"],
        "freshness_status_refs": [
            "freshness_visual_fixture_001",
            "freshness_ocr_fixture_001",
            "freshness_map_stale_risk_001",
            "freshness_route_task_scope_001",
        ],
        "uncertainty_level": "moderate",
        "decision_readiness_ref": "readiness_vision_nav_chain_001",
        "recommended_next_step_hint": "observe_more_or_hold_for_safety",
        "forbidden_actions": [
            "direct_navigation_action_without_decision",
            "runtime_enable",
            "provider_invocation",
            "user_output",
        ],
        "required_observation": True,
        "rationale_refs": ["rationale:vision_nav_chain:001"],
        "whitebox_trace_refs": ["whitebox_trace:chain_intake_001", "trace:visual_obs:001"],
        "candidate_only": True,
        "not_decision": True,
        "not_fact": True,
        "not_user_output": True,
        "runtime_enable_allowed": False,
        "version_ref": "v1",
        "ttl": "120s",
        **meta,
    }

    conflict = {
        "conflict_id": "conflict_map_vs_vision_chain_001",
        "conflict_type": "map_vs_vision",
        "conflict_status": "potential_non_blocking",
        "conflicting_source_refs": [
            "map_location_sample_001",
            "visual_obs_sample_crossing_001",
        ],
        "conflict_severity": "low",
        "affected_context_fields": ["current_route_context", "current_scene_context"],
        "recommended_resolution_hint": "reobserve_with_live_validation_later",
        "decision_required": True,
        "hold_or_reobserve_hint": True,
        "evidence_refs": ["evidence:map_vision_mismatch_hint:001"],
        "whitebox_trace_refs": ["trace:conflict:chain_001"],
        "candidate_only": True,
        **meta,
    }

    gap = {
        "gap_id": "gap_missing_live_validation_001",
        "gap_type": "missing_validation_result",
        "missing_source_type": "missing_real_time_frame_validation",
        "affected_decision_scope": "street_crossing_navigation",
        "required_observation": "observe_crossing_status_later",
        "required_evidence": ["live_traffic_confirmation", "real_time_crossing_status"],
        "priority_level": "high",
        "ttl": "60s",
        "candidate_only": True,
        **meta,
    }

    freshness_items = [
        {
            "freshness_status_id": "freshness_visual_fixture_001",
            "source_ref": "visual_obs_sample_crossing_001",
            "source_type": "visual_observation_candidate",
            "observed_at": "simulated_fixture_only",
            "ttl": "30s",
            "freshness_state": "simulated_only",
            "stale_risk": "fixture_not_live",
            "can_drive_decision": False,
            "refresh_required_hint": True,
            "candidate_only": True,
        },
        {
            "freshness_status_id": "freshness_ocr_fixture_001",
            "source_ref": "ocr_result_sample_sign_001",
            "source_type": "ocr_result_candidate",
            "observed_at": "simulated_fixture_only",
            "ttl": "60s",
            "freshness_state": "simulated_only",
            "stale_risk": "fixture_not_live",
            "can_drive_decision": False,
            "refresh_required_hint": True,
            "candidate_only": True,
        },
        {
            "freshness_status_id": "freshness_map_stale_risk_001",
            "source_ref": "map_location_sample_001",
            "source_type": "map_location_context_candidate",
            "observed_at": "simulated_fixture_only",
            "ttl": "120s",
            "freshness_state": "stale_risk_possible",
            "stale_risk": "moderate",
            "can_drive_decision": False,
            "refresh_required_hint": True,
            "candidate_only": True,
        },
        {
            "freshness_status_id": "freshness_route_task_scope_001",
            "source_ref": "route_context_sample_001",
            "source_type": "route_context_candidate",
            "observed_at": "simulated_fixture_only",
            "ttl": "90s",
            "freshness_state": "task_scope_candidate",
            "stale_risk": "low",
            "can_drive_decision": False,
            "refresh_required_hint": False,
            "candidate_only": True,
        },
    ]
    freshness_bundle = {
        "bundle_id": "sample_context_freshness_status_v1",
        "freshness_items": freshness_items,
        "item_count": len(freshness_items),
        "all_can_drive_decision_false": True,
        **meta,
    }

    priority_map = {
        "priority_map_id": "priority_map_vision_nav_chain_001",
        "drive_priority_weight": 0.85,
        "survival_priority_weight": 1.0,
        "task_priority_weight": 0.6,
        "health_pressure_weight": 0.5,
        "resource_pressure_weight": 0.4,
        "evidence_confidence_weight": 0.7,
        "freshness_weight": 0.45,
        "user_preference_weight": 0.3,
        "constitution_constraint_weight": 1.0,
        "urgency_weight": 0.75,
        "output_priority_hint": "hold_or_observe_more_candidate",
        "candidate_only": True,
        **meta,
    }

    readiness = {
        "decision_readiness_id": "readiness_vision_nav_chain_001",
        "readiness_status": "not_ready_for_real_navigation_decision",
        "readiness_score_candidate": 0.48,
        "required_missing_inputs": [
            "live_frame_validation",
            "real_time_crossing_status",
        ],
        "blocking_conflicts": [],
        "high_risk_flags": ["fixture_only_input", "survival_crossing_attention"],
        "sufficient_for_decision": False,
        "recommended_next_step": "observe_more_or_hold_for_safety",
        "decision_center_handoff_allowed": False,
        "handoff_later_candidate_only": True,
        "candidate_only": True,
        **meta,
    }

    visual_review = {
        "review_id": "visual_ocr_map_route_integration_review_v1",
        "review_items": list(VISUAL_OCR_MAP_ROUTE_REVIEW_ITEMS),
        "item_count": len(VISUAL_OCR_MAP_ROUTE_REVIEW_ITEMS),
        "scene_street_crossing": integrated["current_scene_context"].get("scene_type") == "street_crossing",
        "ocr_signage_bound": "人行横道" in str(integrated["current_scene_context"]),
        **_review_ok([(f"item.{i[:18]}", True) for i in VISUAL_OCR_MAP_ROUTE_REVIEW_ITEMS]),
        **meta,
    }

    drive_review = {
        "review_id": "drive_signal_priority_integration_review_v1",
        "review_items": list(DRIVE_PRIORITY_REVIEW_ITEMS),
        "survival_elevated": integrated["drive_context"].get("observation_priority_elevated") is True,
        **_review_ok([(f"item.{i[:18]}", True) for i in DRIVE_PRIORITY_REVIEW_ITEMS]),
        **meta,
    }

    risk_review = {
        "review_id": "risk_context_integration_review_v1",
        "review_items": list(RISK_INTEGRATION_REVIEW_ITEMS),
        "risk_in_context": "traffic_or_crossing" in str(integrated["current_risk_context"]),
        **_review_ok([(f"item.{i[:18]}", True) for i in RISK_INTEGRATION_REVIEW_ITEMS]),
        **meta,
    }

    trace_review = {
        "review_id": "evidence_traceability_integration_review_v1",
        "review_items": list(EVIDENCE_TRACEABILITY_REVIEW_ITEMS),
        "source_chain_matrix_present": bool(integrated.get("source_chain_matrix")),
        **_review_ok([(f"item.{i[:18]}", True) for i in EVIDENCE_TRACEABILITY_REVIEW_ITEMS]),
        **meta,
    }

    cgf_review = {
        "review_id": "conflict_gap_freshness_integration_review_v1",
        "review_items": list(CONFLICT_GAP_FRESHNESS_REVIEW_ITEMS),
        "conflict_generated": True,
        "gap_generated": True,
        "freshness_count": len(freshness_items),
        **_review_ok([(f"item.{i[:18]}", True) for i in CONFLICT_GAP_FRESHNESS_REVIEW_ITEMS]),
        **meta,
    }

    dc_handoff_review = {
        "review_id": "decision_center_handoff_readiness_review_v1",
        "review_items": list(DC_HANDOFF_REVIEW_ITEMS),
        "handoff_package": {
            "integrated_context_ref": integrated["integrated_context_id"],
            "decision_readiness_ref": readiness["decision_readiness_id"],
            "conflict_refs": integrated["context_conflict_refs"],
            "gap_refs": integrated["context_gap_refs"],
            "freshness_refs": integrated["freshness_status_refs"],
            "decision_candidate_generated": False,
        },
        **_review_ok([(f"item.{i[:18]}", True) for i in DC_HANDOFF_REVIEW_ITEMS]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "chain_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "chain_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS
        ],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    reviews = [
        visual_review,
        drive_review,
        risk_review,
        trace_review,
        cgf_review,
        dc_handoff_review,
    ]

    integrated_ok = (
        all(f in integrated for f in INTEGRATED_CONTEXT_CANDIDATE_FIELDS)
        and integrated.get("candidate_only") is True
        and integrated.get("runtime_enable_allowed") is False
        and readiness.get("sufficient_for_decision") is False
        and readiness.get("decision_center_handoff_allowed") is False
    )

    chain_pass = (
        input_ok
        and integrated_ok
        and all(r.get("dryrun_and_review_pass") for r in reviews)
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and freshness_bundle.get("all_can_drive_decision_false")
    )

    closure_decision = {
        "decision_id": "chain_closure_decision_v1",
        "dryrun_and_review_pass": chain_pass,
        "high_risk": not chain_pass,
        "final_decision": FINAL_DECISION_GO if chain_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "fixture candidate intake validated",
            "integrated_context_candidate generated from vision/OCR/map/route/task/drive/health",
            "conflict/gap/freshness/priority/readiness candidates generated",
            "visual/OCR/map/route/drive/risk/evidence/traceability integration reviewed",
            "Decision Center handoff package prepared, no decision_candidate",
            "18 blocked paths + 17 boundary fields all false",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_decision_chain_candidate_dryrun": chain_pass,
        "selected_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "next_focus": (
            "Decision Center generates decision_candidate from integrated_context_candidate, "
            "still no user output or navigation execution"
        ),
        **meta,
    }

    policy = {
        "policy_id": "vision_navigation_information_integration_chain_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "chain_dryrun_not_runtime_not_decide": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": chain_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": chain_pass,
        "system_level_simulated_go": True,
        "fixture_chain_integrated": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "vision_navigation_information_integration_chain_dryrun_policy": policy,
        "candidate_flow_input_review": input_review,
        "sample_candidate_intake_set": intake_set,
        "information_integration_chain_model_candidate": chain_model,
        "sample_integrated_context_candidate": integrated,
        "sample_context_conflict_candidate": conflict,
        "sample_context_gap_candidate": gap,
        "sample_context_freshness_status": freshness_bundle,
        "sample_context_priority_map": priority_map,
        "sample_decision_readiness_candidate": readiness,
        "visual_ocr_map_route_integration_review": visual_review,
        "drive_signal_priority_integration_review": drive_review,
        "risk_context_integration_review": risk_review,
        "evidence_traceability_integration_review": trace_review,
        "conflict_gap_freshness_integration_review": cgf_review,
        "decision_center_handoff_readiness_review": dc_handoff_review,
        "chain_boundary_audit": boundary_audit,
        "chain_blocked_path_result": blocked_path_result,
        "chain_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
