# -*- coding: utf-8 -*-
"""Seed Core Drive Signal Contract Planning v1."""

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
    SEED_CORE_COMPONENTS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.seed_core_pluggable_layer_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SC_DR_FINAL_GO,
    NEXT_PHASE_GO as SC_DR_NEXT_PHASE,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_planning_v1 import (
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
)

PHASE_ID = "Phase-Seed-Core-Drive-Signal-Contract-Planning-v1-001"
SCOPE = "drive_signal_contract_planning_only"
SOURCE_CHAIN = "seed_core_drive_signal_contract_planning_v1"

UPSTREAM_SC_DR_FINAL = SC_DR_FINAL_GO
UPSTREAM_SC_DR_NEXT = SC_DR_NEXT_PHASE

FINAL_DECISION_GO = "SEED_CORE_DRIVE_SIGNAL_CONTRACT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "SEED_CORE_DRIVE_SIGNAL_CONTRACT_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Seed-Core-Drive-Signal-Contract-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Seed-Core-Drive-Signal-Contract-Issue-Review-v1-001"

SIGNAL_TAXONOMY: Tuple[str, ...] = (
    "drive_signal_candidate",
    "seed_core_signal_candidate",
    "seed_core_hint_candidate",
    "survival_drive_signal_candidate",
    "task_drive_signal_candidate",
    "resource_allocation_hint_candidate",
    "health_pressure_signal_candidate",
    "system_optimization_hint_candidate",
    "observation_intent_candidate",
    "emotion_state_candidate",
    "relationship_context_candidate",
    "social_adaptation_hint_candidate",
    "evolutionary_proposal_candidate",
    "skill_expansion_candidate",
    "logic_revision_candidate",
    "code_optimization_candidate",
)

SIGNAL_TAXONOMY_CONFIRMATIONS: Tuple[str, ...] = (
    "all signals are candidate-only",
    "no signal is decision",
    "no signal is direct action",
    "no signal is user output",
    "no signal is Memory / WorldModel write",
    "no signal can enable runtime by itself",
)

DRIVE_SIGNAL_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "drive_signal_id",
    "drive_type",
    "drive_subtype",
    "source_seed_core_component",
    "priority_level",
    "urgency_level",
    "confidence",
    "ttl",
    "source_refs",
    "evidence_refs",
    "health_refs",
    "task_refs",
    "scene_refs",
    "risk_refs",
    "resource_refs",
    "personal_continuity_refs",
    "recommended_bias",
    "forbidden_actions",
    "required_observation",
    "affected_cognitive_zones",
    "downstream_consumers",
    "rationale_refs",
    "whitebox_trace_refs",
    "candidate_only",
    "not_decision",
    "not_action",
    "not_user_output",
    "runtime_enable_allowed",
)

SEED_CORE_SIGNAL_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "seed_core_signal_id",
    "signal_family",
    "source_component",
    "signal_payload",
    "priority_level",
    "freshness_status",
    "confidence",
    "ttl",
    "output_scope",
    "affected_zones",
    "governance_refs",
    "evidence_refs",
    "whitebox_trace_refs",
    "candidate_only",
    "runtime_enable_allowed",
)

SEED_CORE_HINT_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "hint_id",
    "hint_type",
    "hint_strength",
    "source_component",
    "target_zone",
    "recommended_adjustment",
    "non_binding",
    "decision_required",
    "candidate_only",
)

SURVIVAL_DRIVE_COVERAGE: Tuple[str, ...] = (
    "safety_survival_signal",
    "resource_survival_signal",
    "health_survival_signal",
    "autonomous_observation_signal",
    "social_survival_signal",
    "evolutionary_survival_signal",
)

SURVIVAL_DRIVE_CONFIRMATIONS: Tuple[str, ...] = (
    "Survival Drive priority can override Task Drive in integration/decision",
    "Survival Drive does not execute action",
    "Survival Drive does not invoke provider",
    "Survival Drive does not directly notify user",
    "Survival Drive outputs survival_drive_signal_candidate only",
)

TASK_DRIVE_COVERAGE: Tuple[str, ...] = (
    "active_task_signal",
    "task_priority_hint",
    "task_progress_candidate",
    "task_interruption_candidate",
    "task_resume_candidate",
    "next_required_observation_hint",
    "task_expiry_or_failure_hint",
)

TASK_DRIVE_CONFIRMATIONS: Tuple[str, ...] = (
    "Task Drive tracks goal/progress/interruption/resume",
    "Task Drive cannot override Survival Drive",
    "Task Drive cannot execute task directly",
    "Task Drive cannot open runtime",
)

RESOURCE_GOVERNANCE_COVERAGE: Tuple[str, ...] = (
    "compute_budget_hint",
    "battery_budget_hint",
    "network_budget_hint",
    "storage_budget_hint",
    "provider_budget_hint",
    "sensor_budget_hint",
    "degraded_resource_mode_hint",
)

RESOURCE_GOVERNANCE_CONFIRMATIONS: Tuple[str, ...] = (
    "resource signal can recommend hold/degrade/fallback",
    "resource signal cannot invoke provider",
    "resource signal cannot select provider",
    "resource signal cannot authorize runtime",
)

HEALTH_MANAGEMENT_COVERAGE: Tuple[str, ...] = (
    "module_health_signal",
    "gate_health_signal",
    "runtime_pressure_signal",
    "degradation_status_signal",
    "recovery_hint_candidate",
    "enforcement_health_signal",
)

HEALTH_MANAGEMENT_CONFIRMATIONS: Tuple[str, ...] = (
    "Health signal can influence Decision / Integration",
    "Health signal cannot directly block output",
    "Health signal cannot authorize runtime",
    "Health signal cannot mutate gate result",
)

SYSTEM_OPTIMIZATION_COVERAGE: Tuple[str, ...] = (
    "repeated_failure_hint",
    "inefficient_chain_hint",
    "provider_performance_hint",
    "cache_optimization_hint",
    "routing_optimization_hint",
    "future_improvement_candidate",
)

SYSTEM_OPTIMIZATION_CONFIRMATIONS: Tuple[str, ...] = (
    "optimization signal is advisory",
    "optimization signal cannot auto-refactor",
    "optimization signal cannot modify code",
    "optimization signal cannot change provider automatically",
    "optimization signal cannot rewrite governance",
)

AUTONOMOUS_OBSERVATION_COVERAGE: Tuple[str, ...] = (
    "observation_intent_candidate",
    "environment_change_hint",
    "risk_observation_candidate",
    "context_gap_fill_candidate",
    "world_model_candidate_later_ref",
)

AUTONOMOUS_OBSERVATION_CONFIRMATIONS: Tuple[str, ...] = (
    "Autonomous Observation belongs under Survival Drive",
    "it cannot directly invoke camera/provider/runtime",
    "it cannot write WorldModel fact",
    "it cannot notify user directly",
    "it is governed by privacy/resource/task/safety constraints",
)

EMOTION_ENGINE_COVERAGE: Tuple[str, ...] = (
    "emotion_state_candidate",
    "relationship_context_candidate",
    "social_adaptation_hint",
    "interaction_rhythm_hint",
    "companionship_expression_hint",
)

EMOTION_ENGINE_CONFIRMATIONS: Tuple[str, ...] = (
    "Emotion Engine handles social integration",
    "Emotion Engine is future Survival Drive submodule",
    "Emotion Engine cannot amend constitution",
    "Emotion Engine cannot directly change personality core",
    "Emotion Engine cannot write Memory without admission",
    "Emotion Engine cannot invoke output/runtime directly",
)

EVOLUTIONARY_RECURSION_COVERAGE: Tuple[str, ...] = (
    "evolutionary_proposal_candidate",
    "market_adaptation_hint",
    "skill_expansion_candidate",
    "logic_revision_candidate",
    "code_optimization_candidate",
    "product_feedback_absorption_candidate",
)

EVOLUTIONARY_RECURSION_CONFIRMATIONS: Tuple[str, ...] = (
    "Evolutionary Recursion is future Survival Drive submodule",
    "proposal_only=true",
    "cannot directly modify code",
    "cannot directly add skill",
    "cannot directly amend constitution",
    "cannot directly deploy",
    "cannot enable runtime",
    "cannot replace model/provider",
    "requires owner/governance/validation/whitebox/rollback later",
)

PRIORITY_LEVELS: Tuple[Dict[str, Any], ...] = (
    {"rank": 1, "level": "Survival safety / emergency risk"},
    {"rank": 2, "level": "Constitution / safety constraints"},
    {"rank": 3, "level": "Health critical pressure"},
    {"rank": 4, "level": "Resource critical pressure"},
    {"rank": 5, "level": "Active user task"},
    {"rank": 6, "level": "Task progress optimization"},
    {"rank": 7, "level": "Social adaptation / emotion rhythm"},
    {"rank": 8, "level": "System optimization"},
    {"rank": 9, "level": "Evolutionary proposal"},
)

PRIORITY_CONFIRMATIONS: Tuple[str, ...] = (
    "Survival Drive > Task Drive when risk exists",
    "Constitution constraints override drive preference",
    "Health/Resource can force hold/degrade",
    "Evolutionary Recursion cannot override safety/runtime governance",
)

CONFLICT_TYPES: Tuple[Dict[str, str], ...] = (
    {"conflict_id": "survival_vs_task", "resolution": "Survival priority wins"},
    {"conflict_id": "resource_vs_task", "resolution": "hold_or_degrade_hint"},
    {"conflict_id": "health_vs_runtime", "resolution": "hold_or_degrade_hint"},
    {"conflict_id": "emotion_vs_safety", "resolution": "safety wins"},
    {"conflict_id": "evolution_vs_governance", "resolution": "governance wins"},
    {"conflict_id": "observation_vs_privacy", "resolution": "privacy constraint wins"},
    {"conflict_id": "optimization_vs_stability", "resolution": "stability wins"},
)

CONFLICT_OUTPUT_REQUIREMENTS: Tuple[str, ...] = (
    "conflict_candidate",
    "hold_or_degrade_hint",
    "decision_required=true",
    "escalation_required if high risk",
)

ZONE_HANDOFF_PLAN: Tuple[Dict[str, str], ...] = (
    {
        "zone": "Perception Zone",
        "receives": "observation_priority / observation_intent",
    },
    {
        "zone": "Memory / WorldModel Zone",
        "receives": "retrieval/write admission hints only",
    },
    {"zone": "Drive Zone", "receives": "owns signal generation"},
    {
        "zone": "Information Integration Zone",
        "receives": "drive_signal_candidate",
    },
    {
        "zone": "Decision Zone",
        "receives": "integrated drive context",
    },
    {
        "zone": "Language / Output Zone",
        "receives": "tone/social/output hints only after decision",
    },
    {"zone": "Execution Zone", "receives": "no direct drive command"},
    {
        "zone": "Governance Zone",
        "receives": "conflict / violation / evolution proposal refs",
    },
)

INTEGRATION_PLAN_CONFIRMATIONS: Tuple[str, ...] = (
    "Information Integration consumes drive_signal_candidate",
    "integrates with candidate/evidence/health/task/map/memory context",
    "produces integrated_context_candidate later",
    "does not let drive directly decide",
    "drive signal affects priority/attention/readiness",
)

DECISION_BOUNDARY_CONFIRMATIONS: Tuple[str, ...] = (
    "Decision Center consumes drive context later",
    "drive signal is input, not decision",
    "Decision Center must still consume Constitution / Validation / Health / Whitebox",
    "drive signal cannot bypass Decision Center",
    "drive signal cannot force action",
)

RUNTIME_BOUNDARY_CONFIRMATIONS: Tuple[str, ...] = (
    "drive signal cannot enable runtime",
    "drive signal cannot open execution window",
    "drive signal cannot select provider",
    "drive signal can only recommend runtime readiness / hold / degrade",
    "controlled runtime requires separate authorization",
)

TRACEABILITY_FIELDS: Tuple[str, ...] = (
    "source_seed_core_component",
    "source_refs",
    "evidence_refs",
    "rationale_refs",
    "health_refs",
    "task_refs",
    "scene_refs",
    "whitebox_trace_refs",
    "version_ref",
    "ttl",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Drive Signal Contract Planning GO ≠ Seed Core runtime enabled",
    "drive_signal_candidate ≠ decision/action/user output",
    "Evolutionary Recursion planned ≠ code modification allowed",
    "Emotion Engine signal planned ≠ emotion runtime enabled",
    "Autonomous Observation signal planned ≠ camera/provider invoked",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("drive_signal_contract_planning_only",)

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
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/seed_core_drive_signal_contract_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
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


def _contract_doc(
    contract_id: str,
    *,
    coverage: Tuple[str, ...],
    confirmations: Tuple[str, ...],
    source_component: str,
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "contract_id": contract_id,
        "source_seed_core_component": source_component,
        "signal_output_type": "drive_signal_candidate",
        "coverage": list(coverage),
        "coverage_count": len(coverage),
        "confirmations": list(confirmations),
        "candidate_only": True,
        "runtime_enable_allowed": False,
        **meta,
    }


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false")
    return issues


def run_seed_core_drive_signal_contract_planning_v1(
    *,
    seed_core_pluggable_layer_architecture_dryrun_and_review_root: str,
    seed_core_pluggable_layer_architecture_planning_root: str,
    midplatform_cognitive_zoning_architecture_dryrun_and_review_root: str,
    midplatform_vnext_architecture_realignment_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    sc_dr_root = Path(seed_core_pluggable_layer_architecture_dryrun_and_review_root).expanduser().resolve()
    sc_plan_root = Path(seed_core_pluggable_layer_architecture_planning_root).expanduser().resolve()
    cz_dr_root = Path(midplatform_cognitive_zoning_architecture_dryrun_and_review_root).expanduser().resolve()
    vnext_root = Path(midplatform_vnext_architecture_realignment_planning_root).expanduser().resolve()

    sc_dr_sm = _try_read_json(sc_dr_root / "summary.json") or {}
    sc_dr_vr = _try_read_json(sc_dr_root / "verifier_report.json") or {}
    sc_plan_vr = _try_read_json(sc_plan_root / "verifier_report.json") or {}
    cz_dr_vr = _try_read_json(cz_dr_root / "verifier_report.json") or {}
    vnext_vr = _try_read_json(vnext_root / "verifier_report.json") or {}

    survival_review = _try_read_json(sc_dr_root / "survival_drive_placeholder_review_v1.json") or {}
    continuity_review = _try_read_json(sc_dr_root / "personal_continuity_module_review_v1.json") or {}
    pluggable_review = _try_read_json(sc_dr_root / "pluggable_capability_layer_review_v1.json") or {}
    seed_review = _try_read_json(sc_dr_root / "fixed_seed_core_dryrun_review_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_seed_core_pluggable_dryrun_root": str(sc_dr_root),
        "upstream_seed_core_pluggable_planning_root": str(sc_plan_root),
        "upstream_cognitive_zoning_dryrun_root": str(cz_dr_root),
        "upstream_vnext_realignment_root": str(vnext_root),
        "output_root": str(out_root),
    }

    if sc_dr_vr.get("verifier") != "GO":
        blockers.append("Seed Core / Pluggable DryRunAndReview verifier must be GO")
    if sc_dr_sm.get("final_decision") != UPSTREAM_SC_DR_FINAL:
        blockers.append("seed core pluggable dryrun final_decision mismatch")
    if sc_dr_sm.get("recommended_next_phase") != UPSTREAM_SC_DR_NEXT:
        blockers.append("seed core pluggable dryrun recommended_next_phase mismatch")
    if sc_plan_vr.get("verifier") != "GO":
        blockers.append("Seed Core / Pluggable Planning verifier must be GO")
    if cz_dr_vr.get("verifier") != "GO":
        blockers.append("Cognitive Zoning DryRunAndReview must be GO")
    if vnext_vr.get("verifier") != "GO":
        blockers.append("vNext Architecture Realignment verifier must be GO")
    if not seed_review.get("dryrun_and_review_pass"):
        blockers.append("Seed Core 7 components must be validated")
    if not survival_review.get("dryrun_and_review_pass"):
        blockers.append("Survival Drive placeholder must pass")
    if survival_review.get("evolutionary_recursion", {}).get("proposal_only") is not True:
        blockers.append("Evolutionary Recursion must be proposal-only")
    if not continuity_review.get("dryrun_and_review_pass"):
        blockers.append("Personal Continuity Module must be validated")
    if not pluggable_review.get("dryrun_and_review_pass"):
        blockers.append("Pluggable Capability Layer must be validated")

    leakage_issues: List[str] = []
    for label, sm in (
        ("sc_pluggable_dr", sc_dr_sm),
        ("sc_pluggable_plan", _try_read_json(sc_plan_root / "summary.json") or {}),
        ("cognitive_zoning_dr", _try_read_json(cz_dr_root / "summary.json") or {}),
        ("vnext", _try_read_json(vnext_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "seed_core_architecture_input_review_v1",
        "sc_pluggable_dryrun_verifier": sc_dr_vr.get("verifier"),
        "sc_pluggable_dryrun_final_decision": sc_dr_sm.get("final_decision"),
        "seed_core_7_components_validated": seed_review.get("dryrun_and_review_pass"),
        "emotion_engine_and_evolutionary_recursion_proposal_only": True,
        "personal_continuity_validated": continuity_review.get("dryrun_and_review_pass"),
        "pluggable_layer_validated": pluggable_review.get("dryrun_and_review_pass"),
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "planning_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    taxonomy = {
        "taxonomy_id": "seed_core_signal_taxonomy_v1",
        "signal_types": list(SIGNAL_TAXONOMY),
        "signal_type_count": len(SIGNAL_TAXONOMY),
        "confirmations": list(SIGNAL_TAXONOMY_CONFIRMATIONS),
        **meta,
    }

    drive_contract = {
        "contract_id": "drive_signal_candidate_contract_v1",
        "required_fields": list(DRIVE_SIGNAL_CANDIDATE_FIELDS),
        "field_count": len(DRIVE_SIGNAL_CANDIDATE_FIELDS),
        "defaults": {
            "candidate_only": True,
            "not_decision": True,
            "not_action": True,
            "not_user_output": True,
            "runtime_enable_allowed": False,
        },
        **meta,
    }

    seed_signal_contract = {
        "contract_id": "seed_core_signal_candidate_contract_v1",
        "required_fields": list(SEED_CORE_SIGNAL_CANDIDATE_FIELDS),
        "field_count": len(SEED_CORE_SIGNAL_CANDIDATE_FIELDS),
        "defaults": {"candidate_only": True, "runtime_enable_allowed": False},
        **meta,
    }

    hint_contract = {
        "contract_id": "seed_core_hint_candidate_contract_v1",
        "required_fields": list(SEED_CORE_HINT_CANDIDATE_FIELDS),
        "field_count": len(SEED_CORE_HINT_CANDIDATE_FIELDS),
        "defaults": {"non_binding": True, "decision_required": True, "candidate_only": True},
        **meta,
    }

    survival_contract = _contract_doc(
        "survival_drive_signal_contract_v1",
        coverage=SURVIVAL_DRIVE_COVERAGE,
        confirmations=SURVIVAL_DRIVE_CONFIRMATIONS,
        source_component="Survival Drive",
        meta=meta,
    )
    task_contract = _contract_doc(
        "task_drive_signal_contract_v1",
        coverage=TASK_DRIVE_COVERAGE,
        confirmations=TASK_DRIVE_CONFIRMATIONS,
        source_component="Task Drive",
        meta=meta,
    )
    resource_contract = _contract_doc(
        "resource_governance_signal_contract_v1",
        coverage=RESOURCE_GOVERNANCE_COVERAGE,
        confirmations=RESOURCE_GOVERNANCE_CONFIRMATIONS,
        source_component="Resource Governance",
        meta=meta,
    )
    health_contract = _contract_doc(
        "health_management_signal_contract_v1",
        coverage=HEALTH_MANAGEMENT_COVERAGE,
        confirmations=HEALTH_MANAGEMENT_CONFIRMATIONS,
        source_component="Health Management",
        meta=meta,
    )
    optimization_contract = _contract_doc(
        "system_optimization_signal_contract_v1",
        coverage=SYSTEM_OPTIMIZATION_COVERAGE,
        confirmations=SYSTEM_OPTIMIZATION_CONFIRMATIONS,
        source_component="System Optimization",
        meta=meta,
    )
    observation_contract = _contract_doc(
        "autonomous_world_observation_signal_contract_v1",
        coverage=AUTONOMOUS_OBSERVATION_COVERAGE,
        confirmations=AUTONOMOUS_OBSERVATION_CONFIRMATIONS,
        source_component="Autonomous World Observation",
        meta=meta,
    )
    emotion_contract = _contract_doc(
        "emotion_engine_signal_contract_v1",
        coverage=EMOTION_ENGINE_COVERAGE,
        confirmations=EMOTION_ENGINE_CONFIRMATIONS,
        source_component="Emotion Engine",
        meta=meta,
    )
    evolution_contract = {
        **_contract_doc(
            "evolutionary_recursion_signal_contract_v1",
            coverage=EVOLUTIONARY_RECURSION_COVERAGE,
            confirmations=EVOLUTIONARY_RECURSION_CONFIRMATIONS,
            source_component="Evolutionary Recursion",
            meta=meta,
        ),
        "proposal_only": True,
    }

    priority_policy = {
        "policy_id": "drive_signal_priority_policy_v1",
        "priority_levels": list(PRIORITY_LEVELS),
        "level_count": len(PRIORITY_LEVELS),
        "confirmations": list(PRIORITY_CONFIRMATIONS),
        **meta,
    }

    conflict_policy = {
        "policy_id": "drive_signal_conflict_policy_v1",
        "conflict_types": list(CONFLICT_TYPES),
        "conflict_count": len(CONFLICT_TYPES),
        "output_requirements": list(CONFLICT_OUTPUT_REQUIREMENTS),
        **meta,
    }

    zone_handoff = {
        "plan_id": "drive_signal_to_cognitive_zone_handoff_plan_v1",
        "zone_handoffs": list(ZONE_HANDOFF_PLAN),
        "zone_count": len(ZONE_HANDOFF_PLAN),
        "cognitive_zones": list(COGNITIVE_ZONES),
        **meta,
    }

    integration_plan = {
        "plan_id": "drive_signal_to_information_integration_plan_v1",
        "confirmations": list(INTEGRATION_PLAN_CONFIRMATIONS),
        "confirmation_count": len(INTEGRATION_PLAN_CONFIRMATIONS),
        **meta,
    }

    decision_boundary = {
        "plan_id": "drive_signal_to_decision_center_boundary_plan_v1",
        "confirmations": list(DECISION_BOUNDARY_CONFIRMATIONS),
        "confirmation_count": len(DECISION_BOUNDARY_CONFIRMATIONS),
        **meta,
    }

    runtime_boundary = {
        "plan_id": "drive_signal_to_controlled_runtime_boundary_plan_v1",
        "confirmations": list(RUNTIME_BOUNDARY_CONFIRMATIONS),
        "confirmation_count": len(RUNTIME_BOUNDARY_CONFIRMATIONS),
        **meta,
    }

    traceability = {
        "policy_id": "drive_signal_traceability_policy_v1",
        "required_fields": list(TRACEABILITY_FIELDS),
        "field_count": len(TRACEABILITY_FIELDS),
        "all_signals_must_preserve": True,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "drive_signal_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "boundary_pass": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "drive_signal_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate seed_core_drive_signal_model_candidate",
            "generate sample drive_signal_candidate",
            "verify Survival / Task / Resource / Health / Optimization / Observation / Emotion / Evolution signal contracts",
            "verify drive priority/conflict policy",
            "verify drive signal cognitive zone handoff",
            "verify drive signal cannot directly execute/runtime/write/user output",
        ],
        **meta,
    }

    contracts_ok = (
        len(SIGNAL_TAXONOMY) == 16
        and len(DRIVE_SIGNAL_CANDIDATE_FIELDS) >= 24
        and len(ZONE_HANDOFF_PLAN) == 8
    )
    planning_pass = input_ok and contracts_ok

    planning_decision = {
        "decision_id": "drive_signal_contract_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "architecture_summary": [
            "drive_signal_candidate / seed_core_signal_candidate / seed_core_hint_candidate unified",
            "8 Seed Core component signal contracts defined",
            "priority and conflict policies defined",
            "cognitive zone handoff and integration/decision/runtime boundaries defined",
            "Seed Core influences behavior via signals only, not direct execution",
        ],
        **meta,
    }

    policy = {
        "policy_id": "drive_signal_contract_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "signal_taxonomy_count": len(SIGNAL_TAXONOMY),
        "seed_core_components": list(SEED_CORE_COMPONENTS),
        "planning_not_runtime_not_execute": True,
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
        "boundary_ok": planning_pass,
        "violations": list(blockers),
        "planning_pass": planning_pass,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "drive_signal_contract_planning_policy": policy,
        "seed_core_architecture_input_review": input_review,
        "seed_core_signal_taxonomy": taxonomy,
        "drive_signal_candidate_contract": drive_contract,
        "seed_core_signal_candidate_contract": seed_signal_contract,
        "seed_core_hint_candidate_contract": hint_contract,
        "survival_drive_signal_contract": survival_contract,
        "task_drive_signal_contract": task_contract,
        "resource_governance_signal_contract": resource_contract,
        "health_management_signal_contract": health_contract,
        "system_optimization_signal_contract": optimization_contract,
        "autonomous_world_observation_signal_contract": observation_contract,
        "emotion_engine_signal_contract": emotion_contract,
        "evolutionary_recursion_signal_contract": evolution_contract,
        "drive_signal_priority_policy": priority_policy,
        "drive_signal_conflict_policy": conflict_policy,
        "drive_signal_to_cognitive_zone_handoff_plan": zone_handoff,
        "drive_signal_to_information_integration_plan": integration_plan,
        "drive_signal_to_decision_center_boundary_plan": decision_boundary,
        "drive_signal_to_controlled_runtime_boundary_plan": runtime_boundary,
        "drive_signal_traceability_policy": traceability,
        "drive_signal_boundary_matrix": boundary_matrix,
        "drive_signal_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "drive_signal_contract_planning_decision": planning_decision,
        "summary": summary,
    }
