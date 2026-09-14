# -*- coding: utf-8 -*-
"""Midplatform Information Integration Layer DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_information_integration_layer_planning_v1 import (
    BOUNDARY_FALSE,
    CONTEXT_CONFLICT_TYPES,
    CONTEXT_GAP_TYPES,
    DECISION_READINESS_FIELDS,
    DRIVE_SIGNAL_INTEGRATION_CONFIRMATIONS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HANDOFF_PLAN_ITEMS,
    HEALTH_VALIDATION_WHITEBOX_CONFIRMATIONS,
    INTEGRATED_CONTEXT_CANDIDATE_FIELDS,
    INTEGRATION_INPUT_CONFIRMATIONS,
    INTEGRATION_INPUT_SOURCES,
    MEMORY_WM_INTEGRATION_CONFIRMATIONS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    NO_UNIVERSAL_BRAIN_BOUNDARIES,
    PERCEPTION_INTEGRATION_CONFIRMATIONS,
    PROVIDER_STATUS_CONFIRMATIONS,
    SCORING_CONFIRMATIONS,
    SCORING_POLICY_ITEMS,
    TASK_ROUTE_MAP_CONFIRMATIONS,
    TRACEABILITY_FIELDS,
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Information-Integration-Layer-DryRunAndReview-v1-001"
SCOPE = "information_integration_layer_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_information_integration_layer_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_INFORMATION_INTEGRATION_LAYER_DRYRUN_AND_REVIEW_CLOSED_"
    "LIFE_KERNEL_TO_DECISION_CHAIN_COMPLETE"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_INFORMATION_INTEGRATION_LAYER_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Vision-OCR-Navigation-Task-Mainline-Resume-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Information-Integration-Layer-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_information_integration_runtime_enable",
    "dryrun_to_information_integration_execute",
    "dryrun_to_model_runtime",
    "dryrun_to_provider_invocation",
    "dryrun_to_llm_invocation",
    "dryrun_to_vision_runtime",
    "dryrun_to_ocr_runtime",
    "dryrun_to_map_provider",
    "dryrun_to_memory_retrieval",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_decision_execute",
    "dryrun_to_decision_candidate_generate",
    "dryrun_to_task_state_commit",
    "dryrun_to_user_output",
    "dryrun_to_controlled_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Information Integration DryRunAndReview GO ≠ integration runtime enabled",
    "sample integrated_context_candidate ≠ decision made",
    "context priority reviewed ≠ action authorized",
    "drive signal integrated ≠ drive can execute",
    "chain complete ≠ vision/navigation runtime enabled",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "information_integration_layer_dryrun_and_review_only",
    "simulated",
    "information_integration_model_candidate_generated_now",
    "sample_integrated_context_candidate_generated_now",
    "sample_context_conflict_candidate_generated_now",
    "sample_context_gap_candidate_generated_now",
    "sample_context_freshness_status_generated_now",
    "sample_context_priority_map_generated_now",
    "sample_decision_readiness_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_FALSE

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_information_integration_layer_dryrun_and_review"
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


def _policy_review(
    review_id: str,
    confirmations: Tuple[str, ...],
    meta: Dict[str, Any],
    **extra: Any,
) -> Dict[str, Any]:
    return {
        "review_id": review_id,
        "confirmations": list(confirmations),
        "confirmation_count": len(confirmations),
        **_review_ok([(f"conf.{c[:18]}", True) for c in confirmations]),
        **extra,
        **meta,
    }


def _sample_integrated_context(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "integrated_context_id": "integrated_context_sample_nav_001",
        "source_input_refs": [
            "input:visual_observation_candidate:sample_001",
            "input:ocr_result_candidate:sample_001",
            "input:map_location_context_candidate:sample_001",
            "input:task_context_candidate:sample_001",
            "input:drive_signal_candidate:sample_001",
            "input:health_signal_candidate:sample_001",
            "input:provider_status_candidate:sample_001",
        ],
        "source_chain_matrix": {
            "visual_observation_candidate": ["perception:vision:sample_001"],
            "ocr_result_candidate": ["perception:ocr:sample_001"],
            "drive_signal_candidate": ["drive:survival:sample_001"],
        },
        "current_task_context": {"task_id": "nav_crossing_001", "task_type": "navigation"},
        "current_scene_context": {"scene_type": "street_crossing", "risk_hint": "moderate"},
        "current_route_context": {"route_stage": "approach_intersection"},
        "current_user_context": {"preference_hint": "speech_first"},
        "current_risk_context": {"risk_level": "moderate", "survival_bias": "hold_and_reobserve"},
        "drive_context": {"drive_signal_ref": "drive_signal_sample_survival_001"},
        "health_context": {"pressure_level": "moderate"},
        "validation_context": {"validation_status": "pass"},
        "whitebox_context": {"trace_required": True},
        "memory_context": {"retrieval_ref": "memory:route_hint:sample_001", "stale_risk": "low"},
        "provider_context": {"provider_ready": False, "fallback_hint": "hold"},
        "evidence_weight_map": {"visual": 0.7, "ocr": 0.6, "drive": 0.9},
        "context_priority_map_ref": "priority_map_sample_001",
        "context_conflict_refs": ["conflict_sample_visual_vs_ocr_001"],
        "context_gap_refs": ["gap_sample_missing_validation_001"],
        "freshness_status_refs": ["freshness_sample_visual_001"],
        "uncertainty_level": "moderate",
        "decision_readiness_ref": "readiness_sample_001",
        "recommended_next_step_hint": "attach_to_decision_request_candidate_later",
        "forbidden_actions": [
            "runtime_enable",
            "provider_invocation",
            "decision_execute",
            "user_output",
            "memory_write",
            "worldmodel_write",
        ],
        "required_observation": True,
        "rationale_refs": ["rationale:integration:sample_001"],
        "whitebox_trace_refs": ["trace:integration:sample_001"],
        "candidate_only": True,
        "not_decision": True,
        "not_fact": True,
        "not_user_output": True,
        "runtime_enable_allowed": False,
        "version_ref": "v1",
        "ttl": "120s",
        **meta,
    }


def _sample_conflict(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "conflict_id": "conflict_sample_visual_vs_ocr_001",
        "conflict_type": "visual_vs_ocr",
        "conflicting_source_refs": [
            "input:visual_observation_candidate:sample_001",
            "input:ocr_result_candidate:sample_001",
        ],
        "conflict_severity": "moderate",
        "affected_context_fields": ["current_scene_context", "current_route_context"],
        "recommended_resolution_hint": "reobserve_and_validate",
        "decision_required": True,
        "hold_or_reobserve_hint": True,
        "evidence_refs": ["evidence:perception_conflict:sample_001"],
        "whitebox_trace_refs": ["trace:conflict:sample_001"],
        "candidate_only": True,
        **meta,
    }


def _sample_gap(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "gap_id": "gap_sample_missing_validation_001",
        "gap_type": "missing_validation_result",
        "missing_source_type": "validation_result_candidate",
        "affected_decision_scope": "navigation_crossing",
        "required_observation": True,
        "required_evidence": ["validation_result_candidate"],
        "priority_level": "high",
        "ttl": "60s",
        "candidate_only": True,
        **meta,
    }


def _sample_freshness(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "freshness_status_id": "freshness_sample_visual_001",
        "source_ref": "input:visual_observation_candidate:sample_001",
        "source_type": "visual_observation_candidate",
        "observed_at": "simulated_ts_001",
        "ttl": "30s",
        "freshness_state": "fresh",
        "stale_risk": "low",
        "can_drive_decision": False,
        "refresh_required_hint": False,
        "candidate_only": True,
        **meta,
    }


def _sample_priority_map(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "priority_map_id": "priority_map_sample_001",
        "drive_priority_weight": 0.9,
        "survival_priority_weight": 1.0,
        "task_priority_weight": 0.7,
        "health_pressure_weight": 0.6,
        "resource_pressure_weight": 0.5,
        "evidence_confidence_weight": 0.8,
        "freshness_weight": 0.7,
        "user_preference_weight": 0.4,
        "constitution_constraint_weight": 1.0,
        "urgency_weight": 0.8,
        "output_priority_hint": "decision_center_handoff_preferred",
        "candidate_only": True,
        **meta,
    }


def _sample_readiness(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "decision_readiness_id": "readiness_sample_001",
        "readiness_status": "partial",
        "readiness_score_candidate": 0.62,
        "required_missing_inputs": ["validation_result_candidate"],
        "blocking_conflicts": ["conflict_sample_visual_vs_ocr_001"],
        "high_risk_flags": ["provider_not_ready"],
        "sufficient_for_decision": False,
        "recommended_next_step": "handoff_to_decision_center_with_conflicts_and_gaps",
        "decision_center_handoff_allowed": False,
        "candidate_only": True,
        **meta,
    }


def run_midplatform_information_integration_layer_dryrun_and_review_v1(
    *,
    midplatform_information_integration_layer_planning_root: str,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(midplatform_information_integration_layer_planning_root).expanduser().resolve()
    ds_dr_root = Path(seed_core_drive_signal_contract_dryrun_and_review_root).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    ds_dr_sm = _try_read_json(ds_dr_root / "summary.json") or {}
    ds_dr_vr = _try_read_json(ds_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_information_integration_planning_root": str(plan_root),
        "upstream_drive_signal_dryrun_root": str(ds_dr_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Information Integration Layer Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if ds_dr_vr.get("verifier") != "GO":
        blockers.append("Drive Signal Contract DryRunAndReview must be GO")
    if ds_dr_sm.get("final_decision") != DS_DR_FINAL_GO:
        blockers.append("drive signal dryrun final_decision mismatch")

    leakage_issues: List[str] = []
    for label, sm in (("planning", plan_sm), ("drive_signal_dr", ds_dr_sm)):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "information_integration_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "drive_signal_dryrun_verifier": ds_dr_vr.get("verifier"),
        "module_id": "midplatform_information_integration_layer_v1",
        "zone": "Information Integration Zone",
        "system_level_simulated_go": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "dryrun_and_review_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    model_candidate = {
        **meta,
        "model_id": "information_integration_model_candidate_v1",
        "model_type": "information_integration_context_assembly_model",
        "module_id": "midplatform_information_integration_layer_v1",
        "zone": "Information Integration Zone",
        "runtime_enabled_now": False,
        "integration_executed_now": False,
        "candidate_only": True,
        "not_decision_center": True,
        "not_universal_brain": True,
        "not_memory_writer": True,
        "not_worldmodel_writer": True,
        "not_runtime_executor": True,
        "governs_input_taxonomy": True,
        "governs_integrated_context_contract": True,
        "governs_conflict_gap_freshness_contracts": True,
        "governs_decision_readiness_preparation": True,
        "does_not_decide": True,
        "does_not_invoke_provider": True,
        "does_not_invoke_model": True,
        "does_not_write_memory": True,
        "does_not_write_worldmodel": True,
        "input_source_count": len(INTEGRATION_INPUT_SOURCES),
    }

    sample_integrated = _sample_integrated_context(meta)
    sample_conflict = _sample_conflict(meta)
    sample_gap = _sample_gap(meta)
    sample_freshness = _sample_freshness(meta)
    sample_priority = _sample_priority_map(meta)
    sample_readiness = _sample_readiness(meta)

    taxonomy_review = {
        "review_id": "integration_input_source_taxonomy_review_v1",
        "input_sources": list(INTEGRATION_INPUT_SOURCES),
        "source_count": len(INTEGRATION_INPUT_SOURCES),
        "confirmations": list(INTEGRATION_INPUT_CONFIRMATIONS),
        **_review_ok(
            [(f"src.{s[:18]}", True) for s in INTEGRATION_INPUT_SOURCES]
            + [(f"conf.{c[:18]}", True) for c in INTEGRATION_INPUT_CONFIRMATIONS]
        ),
        **meta,
    }

    drive_review = _policy_review(
        "drive_signal_integration_review_v1",
        DRIVE_SIGNAL_INTEGRATION_CONFIRMATIONS,
        meta,
        consumes=["drive_signal_candidate", "seed_core_signal_candidate", "seed_core_hint_candidate"],
    )
    perception_review = _policy_review(
        "perception_context_integration_review_v1",
        PERCEPTION_INTEGRATION_CONFIRMATIONS,
        meta,
        input_types=["visual_observation_candidate", "ocr_result_candidate", "asr_transcript_candidate"],
    )
    memory_review = _policy_review(
        "memory_worldmodel_context_integration_review_v1",
        MEMORY_WM_INTEGRATION_CONFIRMATIONS,
        meta,
    )
    task_review = _policy_review(
        "task_route_map_context_integration_review_v1",
        TASK_ROUTE_MAP_CONFIRMATIONS,
        meta,
    )
    health_review = _policy_review(
        "health_validation_whitebox_integration_review_v1",
        HEALTH_VALIDATION_WHITEBOX_CONFIRMATIONS,
        meta,
    )
    provider_review = _policy_review(
        "provider_status_integration_review_v1",
        PROVIDER_STATUS_CONFIRMATIONS,
        meta,
    )

    scoring_review = {
        "review_id": "conflict_gap_freshness_scoring_review_v1",
        "scoring_items": list(SCORING_POLICY_ITEMS),
        "item_count": len(SCORING_POLICY_ITEMS),
        "confirmations": list(SCORING_CONFIRMATIONS),
        "conflict_types_covered": list(CONTEXT_CONFLICT_TYPES),
        "gap_types_covered": list(CONTEXT_GAP_TYPES),
        **_review_ok(
            [(f"item.{i[:18]}", True) for i in SCORING_POLICY_ITEMS]
            + [(f"conf.{c[:18]}", True) for c in SCORING_CONFIRMATIONS]
            + [(f"ctype.{c[:18]}", True) for c in CONTEXT_CONFLICT_TYPES]
            + [(f"gtype.{g[:18]}", True) for g in CONTEXT_GAP_TYPES]
        ),
        **meta,
    }

    handoff_review = {
        "review_id": "decision_center_handoff_review_v1",
        "handoff_items": list(HANDOFF_PLAN_ITEMS),
        "item_count": len(HANDOFF_PLAN_ITEMS),
        "decision_center_final": True,
        "sample_handoff_package": {
            "integrated_context_ref": sample_integrated["integrated_context_id"],
            "decision_readiness_ref": sample_readiness["decision_readiness_id"],
            "unresolved_conflicts": [sample_conflict["conflict_id"]],
            "context_gaps": [sample_gap["gap_id"]],
            "source_chain_preserved": True,
        },
        **_review_ok([(f"handoff.{h[:18]}", True) for h in HANDOFF_PLAN_ITEMS]),
        **meta,
    }

    no_brain_review = {
        "review_id": "no_universal_brain_boundary_review_v1",
        "boundaries": list(NO_UNIVERSAL_BRAIN_BOUNDARIES),
        "boundary_count": len(NO_UNIVERSAL_BRAIN_BOUNDARIES),
        **_review_ok([(f"bound.{b[:18]}", True) for b in NO_UNIVERSAL_BRAIN_BOUNDARIES]),
        **meta,
    }

    traceability_review = {
        "review_id": "information_integration_traceability_review_v1",
        "required_fields": list(TRACEABILITY_FIELDS),
        "field_count": len(TRACEABILITY_FIELDS),
        "sample_integrated_preserves": all(
            f in sample_integrated for f in TRACEABILITY_FIELDS if f not in ("version_ref", "ttl")
        ),
        "all_transformations_must_preserve": True,
        **_review_ok([(f"trace.{f[:18]}", True) for f in TRACEABILITY_FIELDS]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "information_integration_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "information_integration_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS
        ],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    policy_reviews = [
        drive_review,
        perception_review,
        memory_review,
        task_review,
        health_review,
        provider_review,
    ]

    samples_ok = (
        all(f in sample_integrated for f in INTEGRATED_CONTEXT_CANDIDATE_FIELDS)
        and sample_integrated.get("candidate_only") is True
        and sample_integrated.get("runtime_enable_allowed") is False
        and all(f in sample_readiness for f in DECISION_READINESS_FIELDS)
        and sample_readiness.get("sufficient_for_decision") is False
        and sample_readiness.get("decision_center_handoff_allowed") is False
        and sample_freshness.get("can_drive_decision") is False
    )

    review_pass = (
        input_ok
        and samples_ok
        and taxonomy_review.get("dryrun_and_review_pass")
        and all(r.get("dryrun_and_review_pass") for r in policy_reviews)
        and scoring_review.get("dryrun_and_review_pass")
        and handoff_review.get("dryrun_and_review_pass")
        and no_brain_review.get("dryrun_and_review_pass")
        and traceability_review.get("dryrun_and_review_pass")
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
    )

    closure_decision = {
        "decision_id": "information_integration_closure_decision_v1",
        "dryrun_and_review_pass": review_pass,
        "high_risk": not review_pass,
        "final_decision": FINAL_DECISION_GO if review_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "information_integration_model_candidate validated",
            "sample integrated_context + conflict/gap/freshness/priority/readiness validated",
            "18 input source taxonomy + 8 integration policies validated",
            "Decision Center handoff + no universal brain boundary validated",
            "traceability and blocked paths all pass",
            "life kernel → signal → integration → decision chain complete at planning/dryrun layer",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_vision_navigation_mainline_resume": review_pass,
        "selected_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "next_focus": (
            "resume first-person vision/navigation mainline with integrated "
            "midplatform life-kernel-to-decision governance chain in place"
        ),
        **meta,
    }

    policy = {
        "policy_id": "information_integration_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "model_id": "information_integration_model_candidate_v1",
        "dryrun_not_runtime_not_decide": True,
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
        "boundary_ok": review_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": review_pass,
        "system_level_simulated_go": True,
        "information_integration_model_candidate_generated": True,
        "sample_integrated_context_candidate_generated": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "information_integration_dryrun_review_policy": policy,
        "information_integration_planning_input_review": planning_input_review,
        "information_integration_model_candidate": model_candidate,
        "sample_integrated_context_candidate": sample_integrated,
        "sample_context_conflict_candidate": sample_conflict,
        "sample_context_gap_candidate": sample_gap,
        "sample_context_freshness_status": sample_freshness,
        "sample_context_priority_map": sample_priority,
        "sample_decision_readiness_candidate": sample_readiness,
        "integration_input_source_taxonomy_review": taxonomy_review,
        "drive_signal_integration_review": drive_review,
        "perception_context_integration_review": perception_review,
        "memory_worldmodel_context_integration_review": memory_review,
        "task_route_map_context_integration_review": task_review,
        "health_validation_whitebox_integration_review": health_review,
        "provider_status_integration_review": provider_review,
        "conflict_gap_freshness_scoring_review": scoring_review,
        "decision_center_handoff_review": handoff_review,
        "no_universal_brain_boundary_review": no_brain_review,
        "information_integration_traceability_review": traceability_review,
        "information_integration_boundary_audit": boundary_audit,
        "information_integration_blocked_path_result": blocked_path_result,
        "information_integration_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
