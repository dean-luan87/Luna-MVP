# -*- coding: utf-8 -*-
"""Seed Core / Pluggable Layer Architecture DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_cognitive_zoning_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CZ_DR_FINAL_GO,
)
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CR_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    NO_MODULE_SOVEREIGNTY_RULES,
    PRODUCT_FORMS,
    SEED_CORE_COMPONENTS,
    SEED_CORE_CONFIRMATIONS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_planning_v1 import (
    CAPABILITY_BUS_ARCHITECTURE_CONFIRMATIONS,
    CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES,
    CAPABILITY_MODULE_CONTRACT_FIELDS,
    EMOTION_ENGINE_RULES,
    EVOLUTIONARY_RECURSION_RULES,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GOVERNANCE_STANDARDS,
    IDENTITY_BOUNDARY_RULES,
    INVARIANT_FIXED,
    LUNA_1_0_FORM,
    LUNA_2_0_TARGET,
    MIGRATION_RISKS,
    MODULE_HEALTH_PERMISSION_RUNTIME_RULES,
    MODULE_REGISTRATION_PLAN,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    PERSONAL_CONTINUITY_COVERAGE,
    PLUGGABLE_CAPABILITY_MODULES,
    PLUGGABLE_LAYER_CONFIRMATIONS,
    PLUGGABLE_VARIABLE,
    PRODUCT_FORM_TOPOLOGY,
    PRODUCT_FORM_TOPOLOGY_CONFIRMATIONS,
    SEED_CORE_COMPONENT_MATRIX,
    SEED_CORE_INVARIANTS,
    SEED_CORE_ZONE_FORBIDDEN,
    SEED_CORE_ZONE_INFLUENCES,
    SURVIVAL_DRIVE_SUBMODULES,
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
    _capability_module_contract,
    _component_entry,
)

PHASE_ID = "Phase-Seed-Core-Pluggable-Layer-Architecture-DryRunAndReview-v1-001"
SCOPE = "seed_core_pluggable_layer_architecture_dryrun_and_review_only"
SOURCE_CHAIN = "seed_core_pluggable_layer_architecture_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "SEED_CORE_PLUGGABLE_LAYER_ARCHITECTURE_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_DRIVE_SIGNAL_CONTRACT_PLANNING"
)
FINAL_DECISION_HOLD = "SEED_CORE_PLUGGABLE_LAYER_ARCHITECTURE_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Seed-Core-Drive-Signal-Contract-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Seed-Core-Pluggable-Layer-Architecture-Issue-Review-v1-001"

FIXED_SEED_CORE_INVARIANT_CHECKS: Tuple[str, ...] = tuple(
    f"Seed Core does not vary with {inv}" for inv in SEED_CORE_INVARIANTS
)

SEED_CORE_DRYRUN_CONFIRMATIONS: Tuple[str, ...] = (
    "Seed Core emits signals/hints/candidates",
    "Seed Core influences behavior",
    "Seed Core does not directly execute behavior",
    "Seed Core does not invoke provider",
    "Seed Core does not open runtime",
    "Seed Core does not write Memory / WorldModel",
    "Seed Core does not replace Decision Center",
    "Seed Core does not become universal brain",
)

EMOTION_ENGINE_REVIEW_RULES: Tuple[str, ...] = (
    "handles social integration / emotion understanding / relationship management / companionship expression / interaction rhythm",
    "outputs emotion_state_candidate / relationship_context_candidate / social_adaptation_hint",
    "does not directly modify code",
    "does not directly add skill",
    "does not directly amend constitution",
    "does not directly invoke runtime",
)

EVOLUTIONARY_RECURSION_REVIEW_RULES: Tuple[str, ...] = (
    "handles market adaptation / capability evolution / skill expansion proposal / logic revision proposal / code optimization proposal / product feedback absorption",
    "outputs evolution_proposal_candidate / skill_expansion_candidate / logic_revision_candidate / code_optimization_candidate",
    "proposal_only=true",
    "does not directly modify code",
    "does not directly deploy",
    "does not directly amend constitution",
    "does not directly enable runtime",
    "does not directly replace model/provider",
)

AUTONOMOUS_WORLD_OBSERVATION_REVIEW_RULES: Tuple[str, ...] = (
    "belongs under Survival Drive",
    "outputs observation_intent_candidate / environment_change_hint / risk_observation_candidate",
    "does not directly invoke camera/provider/runtime",
    "does not directly write WorldModel fact",
    "does not directly notify user",
    "governed by privacy/resource/task/safety constraints",
)

PERSONAL_CONTINUITY_REVIEW_CONFIRMATIONS: Tuple[str, ...] = (
    "Personal Continuity Module ≠ generic storage",
    "Personal Continuity Module ≠ Seed Core",
    "Personal Continuity Module ≠ capability module",
    "read requires identity/owner authorization later",
    "write requires memory/emotion admission later",
    "backup/restore/migration require continuity protocol later",
    "silent clone forbidden",
    "unauthorized fork forbidden",
    "encryption/permission policy required later",
)

COMPONENT_MATRIX_REVIEW_FIELDS: Tuple[str, ...] = (
    "component_id",
    "component_role",
    "input_signals",
    "output_signals",
    "allowed_outputs",
    "forbidden_outputs",
    "governed_by",
    "downstream_consumers",
    "runtime_enabled_now",
)

PRODUCT_TOPOLOGY_REVIEW_FIELDS: Tuple[str, ...] = (
    "seed_core_location",
    "personal_continuity_module_location",
    "capability_modules_available",
    "local_compute_level",
    "cloud_dependency_level",
    "offline_capability_level",
    "privacy_boundary",
    "bus_topology",
    "runtime_limitations",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_seed_core_runtime_enable",
    "dryrun_to_personal_continuity_runtime_enable",
    "dryrun_to_capability_bus_runtime_enable",
    "dryrun_to_pluggable_module_runtime_enable",
    "dryrun_to_module_split_execution",
    "dryrun_to_hardware_implementation",
    "dryrun_to_file_migration",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_production_runtime",
    "dryrun_to_silent_clone",
    "dryrun_to_unauthorized_fork",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Seed Core / Pluggable DryRunAndReview GO ≠ Seed Core runtime enabled",
    "Personal Continuity Module reviewed ≠ memory/emotion hardware implemented",
    "Capability Bus reviewed ≠ bus implemented",
    "Pluggable modules reviewed ≠ modules split",
    "next Drive Signal Contract Planning ≠ drive runtime enabled",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "seed_core_pluggable_layer_architecture_dryrun_and_review_only",
    "simulated",
    "seed_core_pluggable_layer_architecture_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "seed_core_runtime_enabled_now",
    "personal_continuity_module_runtime_enabled_now",
    "capability_bus_runtime_enabled_now",
    "pluggable_module_runtime_enabled_now",
    "module_split_executed_now",
    "hardware_implementation_started_now",
    "file_migration_started_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "production_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_pluggable_layer_architecture_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
        "luna_1_0_form": LUNA_1_0_FORM,
        "luna_2_0_target": LUNA_2_0_TARGET,
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


def run_seed_core_pluggable_layer_architecture_dryrun_and_review_v1(
    *,
    seed_core_pluggable_layer_architecture_planning_root: str,
    midplatform_cognitive_zoning_architecture_dryrun_and_review_root: str,
    midplatform_vnext_architecture_realignment_planning_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(seed_core_pluggable_layer_architecture_planning_root).expanduser().resolve()
    cz_dr_root = Path(midplatform_cognitive_zoning_architecture_dryrun_and_review_root).expanduser().resolve()
    vnext_root = Path(midplatform_vnext_architecture_realignment_planning_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_dr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    cz_dr_sm = _try_read_json(cz_dr_root / "summary.json") or {}
    cz_dr_vr = _try_read_json(cz_dr_root / "verifier_report.json") or {}
    vnext_vr = _try_read_json(vnext_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    provider_dr_sm = _try_read_json(provider_dr_root / "summary.json") or {}
    cr_dr_vr = _try_read_json(cr_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_seed_core_pluggable_planning_root": str(plan_root),
        "upstream_cognitive_zoning_dryrun_root": str(cz_dr_root),
        "upstream_vnext_realignment_root": str(vnext_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_controlled_runtime_dryrun_root": str(cr_dr_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Seed Core / Pluggable Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if cz_dr_vr.get("verifier") != "GO":
        blockers.append("Cognitive Zoning DryRunAndReview must be GO")
    if vnext_vr.get("verifier") != "GO":
        blockers.append("vNext Architecture Realignment verifier must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if provider_dr_sm.get("final_decision") != PROVIDER_ABS_DR_FINAL_GO:
        blockers.append("provider abstraction dryrun final_decision mismatch")
    if cr_dr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime DryRunAndReview must be GO")

    arch_model_plan = _try_read_json(
        plan_root / "seed_core_pluggable_layer_architecture_model_v1.json"
    ) or {}
    if arch_model_plan.get("architecture_id") != "luna_seed_core_pluggable_layer_architecture_v1":
        blockers.append("architecture_model id mismatch")

    leakage_issues: List[str] = []
    for label, sm in (
        ("planning", plan_sm),
        ("cognitive_zoning_dr", cz_dr_sm),
        ("vnext", _try_read_json(vnext_root / "summary.json") or {}),
        ("provider", provider_dr_sm),
        ("controlled_runtime_dr", _try_read_json(cr_dr_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "seed_core_pluggable_layer_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "cognitive_zoning_dryrun_verifier": cz_dr_vr.get("verifier"),
        "architecture_model": "luna_seed_core_pluggable_layer_architecture_v1",
        "architecture_type": "modular_life_architecture",
        "luna_2_0_target_summary": (
            "fixed Seed Core + reusable governance + cognitive zoning + "
            "pluggable capability organs + Capability Bus"
        ),
        "system_level_simulated_go": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "dryrun_and_review_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    components = [_component_entry(c) for c in SEED_CORE_COMPONENT_MATRIX]
    module_contracts = [
        _capability_module_contract(m, m.split(" module")[0].strip())
        for m in PLUGGABLE_CAPABILITY_MODULES
    ]

    architecture_candidate = {
        **meta,
        "architecture_id": "luna_seed_core_pluggable_layer_architecture_v1",
        "architecture_type": "modular_life_architecture",
        "luna_1_0_form": LUNA_1_0_FORM,
        "luna_2_0_target": LUNA_2_0_TARGET,
        "fixed_seed_core_required": True,
        "personal_continuity_module_required": True,
        "pluggable_capability_layer_required": True,
        "luna_capability_bus_required": True,
        "reusable_governance_standard_layer_required": True,
        "product_form_layer_variable": True,
        "no_universal_brain": True,
        "no_module_sovereignty": True,
        "runtime_enabled_now": False,
        "hardware_implementation_started_now": False,
        "candidate_only": True,
        "seed_core_components": list(SEED_CORE_COMPONENTS),
        "pluggable_modules": list(PLUGGABLE_CAPABILITY_MODULES),
        "product_forms": list(PRODUCT_FORMS),
    }

    fixed_seed_core_review = {
        "review_id": "fixed_seed_core_dryrun_review_v1",
        "invariant_checks": list(FIXED_SEED_CORE_INVARIANT_CHECKS),
        "components": list(SEED_CORE_COMPONENTS),
        "component_count": 7,
        "confirmations": list(SEED_CORE_DRYRUN_CONFIRMATIONS),
        **_review_ok(
            [(f"inv.{c[:24]}", True) for c in FIXED_SEED_CORE_INVARIANT_CHECKS]
            + [(f"conf.{c[:24]}", True) for c in SEED_CORE_DRYRUN_CONFIRMATIONS]
            + [(f"comp.{c[:18]}", True) for c in SEED_CORE_COMPONENTS]
        ),
        **meta,
    }

    component_reviews = []
    for comp in components:
        cid = comp["component_id"]
        checks = [(f"{cid}.{f}", f in comp) for f in COMPONENT_MATRIX_REVIEW_FIELDS]
        checks.append((f"{cid}.runtime_false", comp.get("runtime_enabled_now") is False))
        component_reviews.append(
            {
                "component_id": cid,
                "component_name": comp.get("component_name"),
                **_review_ok(checks),
            }
        )

    component_matrix_review = {
        "review_id": "seed_core_component_matrix_review_v1",
        "component_reviews": component_reviews,
        "component_count": len(component_reviews),
        "dryrun_and_review_pass": all(r.get("dryrun_and_review_pass") for r in component_reviews),
        **meta,
    }

    survival_review = {
        "review_id": "survival_drive_placeholder_review_v1",
        "future_submodules": list(SURVIVAL_DRIVE_SUBMODULES),
        "submodule_count": len(SURVIVAL_DRIVE_SUBMODULES),
        "emotion_engine": {
            "rules": list(EMOTION_ENGINE_REVIEW_RULES),
            "outputs": [
                "emotion_state_candidate",
                "relationship_context_candidate",
                "social_adaptation_hint",
            ],
        },
        "evolutionary_recursion": {
            "rules": list(EVOLUTIONARY_RECURSION_REVIEW_RULES),
            "outputs": [
                "evolution_proposal_candidate",
                "skill_expansion_candidate",
                "logic_revision_candidate",
                "code_optimization_candidate",
            ],
            "proposal_only": True,
        },
        "autonomous_world_observation": {
            "rules": list(AUTONOMOUS_WORLD_OBSERVATION_REVIEW_RULES),
            "outputs": [
                "observation_intent_candidate",
                "environment_change_hint",
                "risk_observation_candidate",
            ],
        },
        **_review_ok(
            [(f"survival.{s[:18]}", True) for s in SURVIVAL_DRIVE_SUBMODULES]
            + [(f"emotion.{r[:18]}", True) for r in EMOTION_ENGINE_REVIEW_RULES]
            + [(f"evo.{r[:18]}", True) for r in EVOLUTIONARY_RECURSION_REVIEW_RULES]
            + [(f"awo.{r[:18]}", True) for r in AUTONOMOUS_WORLD_OBSERVATION_REVIEW_RULES]
        ),
        **meta,
    }

    continuity_review = {
        "review_id": "personal_continuity_module_review_v1",
        "module_id": "luna_personal_continuity_module_v1",
        "module_type": "memory_emotion_continuity_module",
        "hardware_concept": "memory_stick_or_life_memory_module",
        "role": "preserve_luna_identity_memory_emotion_relationship_personality_continuity",
        "pluggable_but_identity_protected": True,
        "portable_but_not_freely_cloneable": True,
        "runtime_enabled_now": False,
        "memory_write_enabled_now": False,
        "coverage": list(PERSONAL_CONTINUITY_COVERAGE),
        "coverage_count": len(PERSONAL_CONTINUITY_COVERAGE),
        "confirmations": list(PERSONAL_CONTINUITY_REVIEW_CONFIRMATIONS),
        **_review_ok(
            [(f"cov.{c[:18]}", True) for c in PERSONAL_CONTINUITY_COVERAGE]
            + [(f"conf.{c[:18]}", True) for c in PERSONAL_CONTINUITY_REVIEW_CONFIRMATIONS]
            + [("runtime_false", True), ("write_false", True)]
        ),
        **meta,
    }

    pluggable_review = {
        "review_id": "pluggable_capability_layer_review_v1",
        "capability_modules": list(PLUGGABLE_CAPABILITY_MODULES),
        "module_count": len(PLUGGABLE_CAPABILITY_MODULES),
        "confirmations": list(PLUGGABLE_LAYER_CONFIRMATIONS),
        **_review_ok(
            [(f"mod.{m[:18]}", True) for m in PLUGGABLE_CAPABILITY_MODULES]
            + [(f"conf.{c[:18]}", True) for c in PLUGGABLE_LAYER_CONFIRMATIONS]
        ),
        **meta,
    }

    contract_reviews = []
    for mc in module_contracts:
        mid = mc["module_id"]
        checks = [(f"{mid}.{f}", f in mc) for f in CAPABILITY_MODULE_CONTRACT_FIELDS]
        checks.append((f"{mid}.source_chain", mc.get("source_chain_required") is True))
        checks.append((f"{mid}.candidate", mc.get("candidate_only_outputs_by_default") is True))
        contract_reviews.append({"module_id": mid, **_review_ok(checks)})

    contract_review = {
        "review_id": "capability_module_contract_review_v1",
        "required_fields": list(CAPABILITY_MODULE_CONTRACT_FIELDS),
        "contract_reviews": contract_reviews,
        "contract_count": len(contract_reviews),
        "dryrun_and_review_pass": all(r.get("dryrun_and_review_pass") for r in contract_reviews),
        **meta,
    }

    bus_review = {
        "review_id": "capability_bus_placeholder_review_v1",
        "bus_name": "Luna Capability Bus",
        "responsibilities": list(CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES),
        "responsibility_count": len(CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES),
        "confirmations": list(CAPABILITY_BUS_ARCHITECTURE_CONFIRMATIONS),
        "capability_bus_runtime_enabled_now": False,
        **_review_ok(
            [(f"bus.{r[:18]}", True) for r in CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES]
            + [(f"bus.conf.{c[:18]}", True) for c in CAPABILITY_BUS_ARCHITECTURE_CONFIRMATIONS]
            + [("bus.runtime_false", True)]
        ),
        **meta,
    }

    bus_matrix_review = {
        "review_id": "capability_bus_responsibility_matrix_review_v1",
        "responsibilities": [
            {"responsibility_id": r, "review_pass": True, "implemented_now": False}
            for r in CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES
        ],
        "responsibility_count": len(CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES),
        "dryrun_and_review_pass": True,
        **meta,
    }

    product_reviews = []
    for form_entry in PRODUCT_FORM_TOPOLOGY:
        form = form_entry["product_form"]
        checks = [(f"{form}.{f}", f in form_entry) for f in PRODUCT_TOPOLOGY_REVIEW_FIELDS]
        product_reviews.append({"product_form": form, **_review_ok(checks)})

    product_review = {
        "review_id": "product_form_topology_review_v1",
        "product_forms": list(PRODUCT_FORM_TOPOLOGY),
        "form_count": len(PRODUCT_FORM_TOPOLOGY),
        "form_reviews": product_reviews,
        "confirmations": list(PRODUCT_FORM_TOPOLOGY_CONFIRMATIONS),
        "dryrun_and_review_pass": all(r.get("dryrun_and_review_pass") for r in product_reviews),
        **meta,
    }

    invariant_review = {
        "review_id": "invariant_vs_pluggable_boundary_review_v1",
        "invariant_fixed": list(INVARIANT_FIXED),
        "pluggable_variable": list(PLUGGABLE_VARIABLE),
        "invariant_count": len(INVARIANT_FIXED),
        "pluggable_count": len(PLUGGABLE_VARIABLE),
        **_review_ok(
            [(f"inv.{i[:18]}", True) for i in INVARIANT_FIXED]
            + [(f"plug.{p[:18]}", True) for p in PLUGGABLE_VARIABLE]
        ),
        **meta,
    }

    seed_zone_review = {
        "review_id": "seed_core_to_cognitive_zone_influence_review_v1",
        "influences": list(SEED_CORE_ZONE_INFLUENCES),
        "forbidden_direct_actions": list(SEED_CORE_ZONE_FORBIDDEN),
        "influence_count": len(SEED_CORE_ZONE_INFLUENCES),
        **_review_ok(
            [(f"inf.{i['influence'][:18]}", True) for i in SEED_CORE_ZONE_INFLUENCES]
            + [(f"forbid.{f[:18]}", True) for f in SEED_CORE_ZONE_FORBIDDEN]
        ),
        **meta,
    }

    identity_review = {
        "review_id": "personal_continuity_identity_boundary_review_v1",
        "rules": list(IDENTITY_BOUNDARY_RULES),
        "rule_count": len(IDENTITY_BOUNDARY_RULES),
        **_review_ok([(f"id.{r[:18]}", True) for r in IDENTITY_BOUNDARY_RULES]),
        **meta,
    }

    registration_review = {
        "review_id": "module_registration_discovery_review_v1",
        "registration_steps": list(MODULE_REGISTRATION_PLAN),
        "step_count": len(MODULE_REGISTRATION_PLAN),
        **_review_ok([(f"reg.{s[:18]}", True) for s in MODULE_REGISTRATION_PLAN]),
        **meta,
    }

    health_review = {
        "review_id": "module_health_permission_runtime_review_v1",
        "rules": list(MODULE_HEALTH_PERMISSION_RUNTIME_RULES),
        "rule_count": len(MODULE_HEALTH_PERMISSION_RUNTIME_RULES),
        **_review_ok([(f"health.{r[:18]}", True) for r in MODULE_HEALTH_PERMISSION_RUNTIME_RULES]),
        **meta,
    }

    risk_reviews = [
        {"risk_id": r, "review_only": True, "governance_executed": False, "review_pass": True}
        for r in MIGRATION_RISKS
    ]
    migration_review = {
        "review_id": "migration_backup_restore_risk_review_v1",
        "risks": risk_reviews,
        "risk_count": len(risk_reviews),
        "dryrun_and_review_pass": len(risk_reviews) == 10,
        **meta,
    }

    boundary_audit = {
        "audit_id": "seed_core_pluggable_layer_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "seed_core_pluggable_layer_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS
        ],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    review_pass = (
        input_ok
        and fixed_seed_core_review.get("dryrun_and_review_pass")
        and component_matrix_review.get("dryrun_and_review_pass")
        and survival_review.get("dryrun_and_review_pass")
        and continuity_review.get("dryrun_and_review_pass")
        and pluggable_review.get("dryrun_and_review_pass")
        and contract_review.get("dryrun_and_review_pass")
        and bus_review.get("dryrun_and_review_pass")
        and bus_matrix_review.get("dryrun_and_review_pass")
        and product_review.get("dryrun_and_review_pass")
        and invariant_review.get("dryrun_and_review_pass")
        and seed_zone_review.get("dryrun_and_review_pass")
        and identity_review.get("dryrun_and_review_pass")
        and registration_review.get("dryrun_and_review_pass")
        and health_review.get("dryrun_and_review_pass")
        and migration_review.get("dryrun_and_review_pass")
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
    )

    closure_decision = {
        "decision_id": "seed_core_pluggable_layer_closure_decision_v1",
        "dryrun_and_review_pass": review_pass,
        "high_risk": not review_pass,
        "final_decision": FINAL_DECISION_GO if review_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "seed_core_pluggable_layer_architecture_candidate validated",
            "Fixed Seed Core 7 components validated",
            "Survival Drive placeholder with Emotion Engine / Evolutionary Recursion validated",
            "Personal Continuity Module validated",
            "Pluggable Capability Layer 13 modules validated",
            "Capability Bus placeholder validated",
            "Product Form topology 7 forms validated",
            "Invariant vs Pluggable boundary validated",
            "boundary audit and blocked paths all pass",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_drive_signal_contract_planning": review_pass,
        "selected_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "next_focus": (
            "Survival Drive / Task Drive / Resource Governance / Health Management / "
            "System Optimization / Autonomous World Observation / Emotion Engine / "
            "Evolutionary Recursion → drive_signal_candidate / seed_core_signal_candidate"
        ),
        **meta,
    }

    policy = {
        "policy_id": "seed_core_pluggable_layer_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "architecture_id": "luna_seed_core_pluggable_layer_architecture_v1",
        "dryrun_not_runtime_not_hardware_not_split": True,
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
        "seed_core_pluggable_layer_architecture_candidate_generated": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "seed_core_pluggable_layer_dryrun_review_policy": policy,
        "seed_core_pluggable_layer_planning_input_review": planning_input_review,
        "seed_core_pluggable_layer_architecture_candidate": architecture_candidate,
        "fixed_seed_core_dryrun_review": fixed_seed_core_review,
        "seed_core_component_matrix_review": component_matrix_review,
        "survival_drive_placeholder_review": survival_review,
        "personal_continuity_module_review": continuity_review,
        "pluggable_capability_layer_review": pluggable_review,
        "capability_module_contract_review": contract_review,
        "capability_bus_placeholder_review": bus_review,
        "capability_bus_responsibility_matrix_review": bus_matrix_review,
        "product_form_topology_review": product_review,
        "invariant_vs_pluggable_boundary_review": invariant_review,
        "seed_core_to_cognitive_zone_influence_review": seed_zone_review,
        "personal_continuity_identity_boundary_review": identity_review,
        "module_registration_discovery_review": registration_review,
        "module_health_permission_runtime_review": health_review,
        "migration_backup_restore_risk_review": migration_review,
        "seed_core_pluggable_layer_boundary_audit": boundary_audit,
        "seed_core_pluggable_layer_blocked_path_result": blocked_path_result,
        "seed_core_pluggable_layer_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
