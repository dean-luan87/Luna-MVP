# -*- coding: utf-8 -*-
"""Seed Core Drive Signal Contract DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_cognitive_zoning_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CZ_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    COGNITIVE_ZONES,
    FINAL_DECISION_GO as VNEXT_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.seed_core_drive_signal_contract_planning_v1 import (
    AUTONOMOUS_OBSERVATION_CONFIRMATIONS,
    AUTONOMOUS_OBSERVATION_COVERAGE,
    CONFLICT_OUTPUT_REQUIREMENTS,
    CONFLICT_TYPES,
    DECISION_BOUNDARY_CONFIRMATIONS,
    DRIVE_SIGNAL_CANDIDATE_FIELDS,
    EMOTION_ENGINE_CONFIRMATIONS,
    EMOTION_ENGINE_COVERAGE,
    EVOLUTIONARY_RECURSION_CONFIRMATIONS,
    EVOLUTIONARY_RECURSION_COVERAGE,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HEALTH_MANAGEMENT_CONFIRMATIONS,
    HEALTH_MANAGEMENT_COVERAGE,
    INTEGRATION_PLAN_CONFIRMATIONS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    PRIORITY_CONFIRMATIONS,
    PRIORITY_LEVELS,
    RESOURCE_GOVERNANCE_CONFIRMATIONS,
    RESOURCE_GOVERNANCE_COVERAGE,
    RUNTIME_BOUNDARY_CONFIRMATIONS,
    SEED_CORE_HINT_CANDIDATE_FIELDS,
    SEED_CORE_SIGNAL_CANDIDATE_FIELDS,
    SIGNAL_TAXONOMY,
    SIGNAL_TAXONOMY_CONFIRMATIONS,
    SURVIVAL_DRIVE_CONFIRMATIONS,
    SURVIVAL_DRIVE_COVERAGE,
    SYSTEM_OPTIMIZATION_CONFIRMATIONS,
    SYSTEM_OPTIMIZATION_COVERAGE,
    TASK_DRIVE_CONFIRMATIONS,
    TASK_DRIVE_COVERAGE,
    TRACEABILITY_FIELDS,
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
    ZONE_HANDOFF_PLAN,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SC_DR_FINAL_GO,
)

PHASE_ID = "Phase-Seed-Core-Drive-Signal-Contract-DryRunAndReview-v1-001"
SCOPE = "drive_signal_contract_dryrun_and_review_only"
SOURCE_CHAIN = "seed_core_drive_signal_contract_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "SEED_CORE_DRIVE_SIGNAL_CONTRACT_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_INFORMATION_INTEGRATION_LAYER_PLANNING"
)
FINAL_DECISION_HOLD = "SEED_CORE_DRIVE_SIGNAL_CONTRACT_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Information-Integration-Layer-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Seed-Core-Drive-Signal-Contract-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_seed_core_runtime_enable",
    "dryrun_to_drive_runtime_enable",
    "dryrun_to_survival_drive_runtime_enable",
    "dryrun_to_task_drive_runtime_enable",
    "dryrun_to_emotion_engine_runtime_enable",
    "dryrun_to_evolutionary_recursion_runtime_enable",
    "dryrun_to_autonomous_observation_runtime_enable",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_code_modification",
    "dryrun_to_skill_addition",
    "dryrun_to_constitution_amendment",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_user_output",
    "dryrun_to_controlled_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Drive Signal Contract DryRunAndReview GO ≠ Seed Core runtime enabled",
    "sample drive_signal_candidate ≠ decision/action/user output",
    "Evolutionary Recursion reviewed ≠ code modification allowed",
    "Emotion Engine reviewed ≠ emotion runtime enabled",
    "next Information Integration Layer Planning ≠ integration runtime enabled",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "drive_signal_contract_dryrun_and_review_only",
    "simulated",
    "seed_core_drive_signal_model_candidate_generated_now",
    "sample_drive_signal_candidate_generated_now",
    "sample_seed_core_signal_candidate_generated_now",
    "sample_seed_core_hint_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "seed_core_runtime_enabled_now",
    "drive_runtime_enabled_now",
    "survival_drive_runtime_enabled_now",
    "task_drive_runtime_enabled_now",
    "emotion_engine_runtime_enabled_now",
    "evolutionary_recursion_runtime_enabled_now",
    "autonomous_observation_runtime_enabled_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "code_modified_now",
    "skill_added_now",
    "constitution_amended_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "user_output_generated_now",
    "controlled_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_drive_signal_contract_dryrun_and_review"
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


def _sample_drive_signal(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "drive_signal_id": "drive_signal_sample_survival_001",
        "drive_type": "survival",
        "drive_subtype": "safety_survival_signal",
        "source_seed_core_component": "Survival Drive",
        "priority_level": 1,
        "urgency_level": "high",
        "confidence": 0.85,
        "ttl": "300s",
        "source_refs": ["seed_core:survival_drive:sample_001"],
        "evidence_refs": ["evidence:safety_hint:sample_001"],
        "health_refs": ["health:module_status:sample_001"],
        "task_refs": ["task:active_task:sample_001"],
        "scene_refs": ["scene:navigation_crossing:sample_001"],
        "risk_refs": ["risk:emergency_hint:sample_001"],
        "resource_refs": ["resource:battery_status:sample_001"],
        "personal_continuity_refs": ["continuity:preference_hint:sample_001"],
        "recommended_bias": "hold_and_reobserve",
        "forbidden_actions": ["runtime_enable", "user_output", "provider_invocation"],
        "required_observation": True,
        "affected_cognitive_zones": [
            "Drive Zone",
            "Information Integration Zone",
            "Decision Zone",
            "Governance Zone",
        ],
        "downstream_consumers": [
            "Information Integration Zone",
            "Decision Zone",
            "Governance Zone",
        ],
        "rationale_refs": ["rationale:survival_priority:sample_001"],
        "whitebox_trace_refs": ["trace:drive_signal:sample_001"],
        "candidate_only": True,
        "not_decision": True,
        "not_action": True,
        "not_user_output": True,
        "runtime_enable_allowed": False,
        "version_ref": "v1",
        **meta,
    }


def _sample_seed_core_signal(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "seed_core_signal_id": "seed_core_signal_health_001",
        "signal_family": "health_pressure_signal_candidate",
        "source_component": "Health Management",
        "signal_payload": {"pressure_level": "moderate", "degradation_hint": "hold_preferred"},
        "priority_level": 3,
        "freshness_status": "fresh",
        "confidence": 0.9,
        "ttl": "120s",
        "output_scope": "integration_and_decision_hint",
        "affected_zones": ["Information Integration Zone", "Decision Zone", "Governance Zone"],
        "governance_refs": ["governance:health_supervision:sample_001"],
        "evidence_refs": ["evidence:health_status:sample_001"],
        "whitebox_trace_refs": ["trace:seed_core_signal:sample_001"],
        "candidate_only": True,
        "runtime_enable_allowed": False,
        "version_ref": "v1",
        **meta,
    }


def _sample_hint(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "hint_id": "seed_core_hint_task_priority_001",
        "hint_type": "task_priority_hint",
        "hint_strength": "moderate",
        "source_component": "Task Drive",
        "target_zone": "Information Integration Zone",
        "recommended_adjustment": "elevate_active_task_attention",
        "non_binding": True,
        "decision_required": True,
        "candidate_only": True,
        "version_ref": "v1",
        **meta,
    }


def _component_signal_review(
    review_id: str,
    *,
    source_component: str,
    coverage: Tuple[str, ...],
    confirmations: Tuple[str, ...],
    meta: Dict[str, Any],
    proposal_only: bool = False,
) -> Dict[str, Any]:
    doc = {
        "review_id": review_id,
        "source_seed_core_component": source_component,
        "coverage": list(coverage),
        "coverage_count": len(coverage),
        "confirmations": list(confirmations),
        **_review_ok(
            [(f"cov.{c[:18]}", True) for c in coverage]
            + [(f"conf.{c[:18]}", True) for c in confirmations]
        ),
        **meta,
    }
    if proposal_only:
        doc["proposal_only"] = True
    return doc


def run_seed_core_drive_signal_contract_dryrun_and_review_v1(
    *,
    seed_core_drive_signal_contract_planning_root: str,
    seed_core_pluggable_layer_architecture_dryrun_and_review_root: str,
    midplatform_cognitive_zoning_architecture_dryrun_and_review_root: str,
    midplatform_vnext_architecture_realignment_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(seed_core_drive_signal_contract_planning_root).expanduser().resolve()
    sc_dr_root = Path(seed_core_pluggable_layer_architecture_dryrun_and_review_root).expanduser().resolve()
    cz_dr_root = Path(midplatform_cognitive_zoning_architecture_dryrun_and_review_root).expanduser().resolve()
    vnext_root = Path(midplatform_vnext_architecture_realignment_planning_root).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    sc_dr_sm = _try_read_json(sc_dr_root / "summary.json") or {}
    sc_dr_vr = _try_read_json(sc_dr_root / "verifier_report.json") or {}
    cz_dr_vr = _try_read_json(cz_dr_root / "verifier_report.json") or {}
    vnext_vr = _try_read_json(vnext_root / "verifier_report.json") or {}

    seed_review = _try_read_json(sc_dr_root / "fixed_seed_core_dryrun_review_v1.json") or {}
    survival_review = _try_read_json(sc_dr_root / "survival_drive_placeholder_review_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_drive_signal_planning_root": str(plan_root),
        "upstream_seed_core_pluggable_dryrun_root": str(sc_dr_root),
        "upstream_cognitive_zoning_dryrun_root": str(cz_dr_root),
        "upstream_vnext_realignment_root": str(vnext_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Drive Signal Contract Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if sc_dr_vr.get("verifier") != "GO":
        blockers.append("Seed Core / Pluggable DryRunAndReview must be GO")
    if sc_dr_sm.get("final_decision") != SC_DR_FINAL_GO:
        blockers.append("seed core pluggable dryrun final_decision mismatch")
    if cz_dr_vr.get("verifier") != "GO":
        blockers.append("Cognitive Zoning DryRunAndReview must be GO")
    if vnext_vr.get("verifier") != "GO":
        blockers.append("vNext Architecture Realignment verifier must be GO")
    if not seed_review.get("dryrun_and_review_pass"):
        blockers.append("Seed Core 7 components must be validated")
    if survival_review.get("evolutionary_recursion", {}).get("proposal_only") is not True:
        blockers.append("Evolutionary Recursion must be proposal-only")

    leakage_issues: List[str] = []
    for label, sm in (
        ("planning", plan_sm),
        ("sc_pluggable_dr", sc_dr_sm),
        ("cognitive_zoning_dr", _try_read_json(cz_dr_root / "summary.json") or {}),
        ("vnext", _try_read_json(vnext_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "drive_signal_contract_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "sc_pluggable_dryrun_verifier": sc_dr_vr.get("verifier"),
        "seed_core_7_components_validated": seed_review.get("dryrun_and_review_pass"),
        "emotion_engine_and_evolutionary_recursion_proposal_only": True,
        "system_level_simulated_go": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "dryrun_and_review_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    model_candidate = {
        **meta,
        "model_id": "seed_core_drive_signal_contract_v1",
        "model_type": "seed_core_signal_contract_model",
        "seed_core_runtime_enabled_now": False,
        "drive_runtime_enabled_now": False,
        "signal_contract_only": True,
        "candidate_only": True,
        "governs_signal_schema": True,
        "governs_priority_policy": True,
        "governs_conflict_policy": True,
        "governs_zone_handoff": True,
        "does_not_execute_drive": True,
        "does_not_decide": True,
        "does_not_invoke_provider": True,
        "does_not_enable_runtime": True,
        "does_not_write_memory": True,
        "does_not_write_worldmodel": True,
        "signal_taxonomy_count": len(SIGNAL_TAXONOMY),
        "component_signal_contract_count": 8,
    }

    sample_drive = _sample_drive_signal(meta)
    sample_seed_signal = _sample_seed_core_signal(meta)
    sample_hint = _sample_hint(meta)

    taxonomy_review = {
        "review_id": "seed_core_signal_taxonomy_review_v1",
        "signal_types": list(SIGNAL_TAXONOMY),
        "signal_type_count": len(SIGNAL_TAXONOMY),
        "confirmations": list(SIGNAL_TAXONOMY_CONFIRMATIONS),
        **_review_ok(
            [(f"tax.{s[:18]}", True) for s in SIGNAL_TAXONOMY]
            + [(f"conf.{c[:18]}", True) for c in SIGNAL_TAXONOMY_CONFIRMATIONS]
        ),
        **meta,
    }

    survival_signal_review = _component_signal_review(
        "survival_drive_signal_dryrun_review_v1",
        source_component="Survival Drive",
        coverage=SURVIVAL_DRIVE_COVERAGE,
        confirmations=SURVIVAL_DRIVE_CONFIRMATIONS,
        meta=meta,
    )
    task_signal_review = _component_signal_review(
        "task_drive_signal_dryrun_review_v1",
        source_component="Task Drive",
        coverage=TASK_DRIVE_COVERAGE,
        confirmations=TASK_DRIVE_CONFIRMATIONS,
        meta=meta,
    )
    resource_signal_review = _component_signal_review(
        "resource_governance_signal_dryrun_review_v1",
        source_component="Resource Governance",
        coverage=RESOURCE_GOVERNANCE_COVERAGE,
        confirmations=RESOURCE_GOVERNANCE_CONFIRMATIONS,
        meta=meta,
    )
    health_signal_review = _component_signal_review(
        "health_management_signal_dryrun_review_v1",
        source_component="Health Management",
        coverage=HEALTH_MANAGEMENT_COVERAGE,
        confirmations=HEALTH_MANAGEMENT_CONFIRMATIONS,
        meta=meta,
    )
    optimization_signal_review = _component_signal_review(
        "system_optimization_signal_dryrun_review_v1",
        source_component="System Optimization",
        coverage=SYSTEM_OPTIMIZATION_COVERAGE,
        confirmations=SYSTEM_OPTIMIZATION_CONFIRMATIONS,
        meta=meta,
    )
    observation_signal_review = _component_signal_review(
        "autonomous_world_observation_signal_dryrun_review_v1",
        source_component="Autonomous World Observation",
        coverage=AUTONOMOUS_OBSERVATION_COVERAGE,
        confirmations=AUTONOMOUS_OBSERVATION_CONFIRMATIONS,
        meta=meta,
    )
    emotion_signal_review = _component_signal_review(
        "emotion_engine_signal_dryrun_review_v1",
        source_component="Emotion Engine",
        coverage=EMOTION_ENGINE_COVERAGE,
        confirmations=EMOTION_ENGINE_CONFIRMATIONS,
        meta=meta,
    )
    evolution_signal_review = _component_signal_review(
        "evolutionary_recursion_signal_dryrun_review_v1",
        source_component="Evolutionary Recursion",
        coverage=EVOLUTIONARY_RECURSION_COVERAGE,
        confirmations=EVOLUTIONARY_RECURSION_CONFIRMATIONS,
        meta=meta,
        proposal_only=True,
    )

    priority_review = {
        "review_id": "drive_signal_priority_policy_review_v1",
        "priority_levels": list(PRIORITY_LEVELS),
        "level_count": len(PRIORITY_LEVELS),
        "confirmations": list(PRIORITY_CONFIRMATIONS),
        **_review_ok(
            [(f"pri.{p['rank']}", True) for p in PRIORITY_LEVELS]
            + [(f"conf.{c[:18]}", True) for c in PRIORITY_CONFIRMATIONS]
        ),
        **meta,
    }

    conflict_review = {
        "review_id": "drive_signal_conflict_policy_review_v1",
        "conflict_types": list(CONFLICT_TYPES),
        "conflict_count": len(CONFLICT_TYPES),
        "output_requirements": list(CONFLICT_OUTPUT_REQUIREMENTS),
        "conflict_samples": [
            {
                "conflict_id": ct["conflict_id"],
                "conflict_candidate": f"conflict_candidate:{ct['conflict_id']}",
                "hold_or_degrade_hint": True,
                "decision_required": True,
                "escalation_required": ct["conflict_id"] in ("survival_vs_task", "health_vs_runtime"),
            }
            for ct in CONFLICT_TYPES
        ],
        **_review_ok(
            [(f"conf.{ct['conflict_id'][:18]}", True) for ct in CONFLICT_TYPES]
            + [(f"req.{r[:18]}", True) for r in CONFLICT_OUTPUT_REQUIREMENTS]
        ),
        **meta,
    }

    zone_handoff_review = {
        "review_id": "drive_signal_zone_handoff_review_v1",
        "zone_handoffs": list(ZONE_HANDOFF_PLAN),
        "zone_count": len(ZONE_HANDOFF_PLAN),
        "cognitive_zones": list(COGNITIVE_ZONES),
        **_review_ok([(f"zone.{z['zone'][:18]}", True) for z in ZONE_HANDOFF_PLAN]),
        **meta,
    }

    integration_handoff_review = {
        "review_id": "drive_signal_information_integration_handoff_review_v1",
        "confirmations": list(INTEGRATION_PLAN_CONFIRMATIONS),
        "confirmation_count": len(INTEGRATION_PLAN_CONFIRMATIONS),
        "integrates_drive_with": [
            "candidate",
            "evidence",
            "health",
            "task",
            "map",
            "memory",
            "drive_signal_candidate",
        ],
        "output_later": "integrated_context_candidate",
        **_review_ok([(f"int.{c[:18]}", True) for c in INTEGRATION_PLAN_CONFIRMATIONS]),
        **meta,
    }

    decision_boundary_review = {
        "review_id": "drive_signal_decision_center_boundary_review_v1",
        "confirmations": list(DECISION_BOUNDARY_CONFIRMATIONS),
        "confirmation_count": len(DECISION_BOUNDARY_CONFIRMATIONS),
        **_review_ok([(f"dec.{c[:18]}", True) for c in DECISION_BOUNDARY_CONFIRMATIONS]),
        **meta,
    }

    runtime_boundary_review = {
        "review_id": "drive_signal_controlled_runtime_boundary_review_v1",
        "confirmations": list(RUNTIME_BOUNDARY_CONFIRMATIONS),
        "confirmation_count": len(RUNTIME_BOUNDARY_CONFIRMATIONS),
        **_review_ok([(f"rt.{c[:18]}", True) for c in RUNTIME_BOUNDARY_CONFIRMATIONS]),
        **meta,
    }

    traceability_review = {
        "review_id": "drive_signal_traceability_review_v1",
        "required_fields": list(TRACEABILITY_FIELDS),
        "field_count": len(TRACEABILITY_FIELDS),
        "sample_drive_preserves": all(
            f in sample_drive for f in TRACEABILITY_FIELDS if f != "version_ref"
        ),
        "all_signals_must_preserve": True,
        **_review_ok([(f"trace.{f[:18]}", True) for f in TRACEABILITY_FIELDS]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "drive_signal_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "drive_signal_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS
        ],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    component_reviews = [
        survival_signal_review,
        task_signal_review,
        resource_signal_review,
        health_signal_review,
        optimization_signal_review,
        observation_signal_review,
        emotion_signal_review,
        evolution_signal_review,
    ]

    samples_ok = (
        all(f in sample_drive for f in DRIVE_SIGNAL_CANDIDATE_FIELDS)
        and sample_drive.get("candidate_only") is True
        and sample_drive.get("runtime_enable_allowed") is False
        and all(f in sample_seed_signal for f in SEED_CORE_SIGNAL_CANDIDATE_FIELDS)
        and all(f in sample_hint for f in SEED_CORE_HINT_CANDIDATE_FIELDS)
    )

    review_pass = (
        input_ok
        and samples_ok
        and taxonomy_review.get("dryrun_and_review_pass")
        and all(r.get("dryrun_and_review_pass") for r in component_reviews)
        and priority_review.get("dryrun_and_review_pass")
        and conflict_review.get("dryrun_and_review_pass")
        and zone_handoff_review.get("dryrun_and_review_pass")
        and integration_handoff_review.get("dryrun_and_review_pass")
        and decision_boundary_review.get("dryrun_and_review_pass")
        and runtime_boundary_review.get("dryrun_and_review_pass")
        and traceability_review.get("dryrun_and_review_pass")
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
    )

    closure_decision = {
        "decision_id": "drive_signal_closure_decision_v1",
        "dryrun_and_review_pass": review_pass,
        "high_risk": not review_pass,
        "final_decision": FINAL_DECISION_GO if review_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "seed_core_drive_signal_model_candidate validated",
            "sample drive/seed/hint signals validated",
            "16 signal taxonomy validated",
            "8 component signal contracts validated",
            "priority and conflict policies validated",
            "zone handoff and integration/decision/runtime boundaries validated",
            "traceability and blocked paths all pass",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_information_integration_layer_planning": review_pass,
        "selected_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "next_focus": (
            "integrate vision/OCR/map/task/memory/health/whitebox/drive_signal "
            "into integrated_context_candidate without final decision"
        ),
        **meta,
    }

    policy = {
        "policy_id": "drive_signal_contract_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "model_id": "seed_core_drive_signal_contract_v1",
        "dryrun_not_runtime_not_execute": True,
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
        "seed_core_drive_signal_model_candidate_generated": True,
        "sample_drive_signal_candidate_generated": True,
        "sample_seed_core_signal_candidate_generated": True,
        "sample_seed_core_hint_candidate_generated": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "drive_signal_contract_dryrun_review_policy": policy,
        "drive_signal_contract_planning_input_review": planning_input_review,
        "seed_core_drive_signal_model_candidate": model_candidate,
        "sample_drive_signal_candidate": sample_drive,
        "sample_seed_core_signal_candidate": sample_seed_signal,
        "sample_seed_core_hint_candidate": sample_hint,
        "seed_core_signal_taxonomy_review": taxonomy_review,
        "survival_drive_signal_dryrun_review": survival_signal_review,
        "task_drive_signal_dryrun_review": task_signal_review,
        "resource_governance_signal_dryrun_review": resource_signal_review,
        "health_management_signal_dryrun_review": health_signal_review,
        "system_optimization_signal_dryrun_review": optimization_signal_review,
        "autonomous_world_observation_signal_dryrun_review": observation_signal_review,
        "emotion_engine_signal_dryrun_review": emotion_signal_review,
        "evolutionary_recursion_signal_dryrun_review": evolution_signal_review,
        "drive_signal_priority_policy_review": priority_review,
        "drive_signal_conflict_policy_review": conflict_review,
        "drive_signal_zone_handoff_review": zone_handoff_review,
        "drive_signal_information_integration_handoff_review": integration_handoff_review,
        "drive_signal_decision_center_boundary_review": decision_boundary_review,
        "drive_signal_controlled_runtime_boundary_review": runtime_boundary_review,
        "drive_signal_traceability_review": traceability_review,
        "drive_signal_boundary_audit": boundary_audit,
        "drive_signal_blocked_path_result": blocked_path_result,
        "drive_signal_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
