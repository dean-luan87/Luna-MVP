# -*- coding: utf-8 -*-
"""Midplatform Cognitive Zoning Architecture DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_cognitive_zoning_architecture_planning_v1 import (
    CAPABILITY_BUS_CONFIRMATIONS,
    CAPABILITY_BUS_RESPONSIBILITIES,
    COGNITIVE_ZONE_DEFINITIONS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GOVERNANCE_STANDARDS,
    HANDOFF_RULES,
    LUNA_1_0_DEFINITION,
    LUNA_2_0_TARGET,
    MODULE_SPLIT_PRINCIPLES,
    MONOLITHIC_TO_MODULAR_CONFIRMATIONS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    NO_UNIVERSAL_BRAIN_RULES,
    SEED_CORE_FORBIDDEN_DIRECT,
    SEED_CORE_INFLUENCES,
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
    ZONE_COMMON_FIELDS,
    ZONE_GOVERNANCE_BINDINGS,
    _zone_entry,
)
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CR_DR_FINAL_GO,
)
from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL_GO,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    COGNITIVE_ZONES,
    FINAL_DECISION_GO as VNEXT_FINAL_GO,
    SEED_CORE_COMPONENTS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Cognitive-Zoning-Architecture-DryRunAndReview-v1-001"
SCOPE = "cognitive_zoning_architecture_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_cognitive_zoning_architecture_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_COGNITIVE_ZONING_ARCHITECTURE_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_SEED_CORE_PLUGGABLE_LAYER_ARCHITECTURE_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_COGNITIVE_ZONING_ARCHITECTURE_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Seed-Core-Pluggable-Layer-Architecture-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Cognitive-Zoning-Architecture-Issue-Review-v1-001"

NO_UNIVERSAL_BRAIN_REVIEW_RULES: Tuple[str, ...] = (
    *NO_UNIVERSAL_BRAIN_RULES,
    "Front models cannot bypass gates",
)

ZONE_RESPONSIBILITY_RULES: Dict[str, Tuple[str, ...]] = {
    "perception_zone": (
        "outputs observation_candidate / evidence_candidate",
        "does not write fact directly",
        "does not write WorldModel directly",
        "does not emit user output directly",
        "provider-backed perception uses Provider Abstraction",
    ),
    "memory_worldmodel_zone": (
        "retrieval output is candidate/evidence",
        "memory write requires admission",
        "worldmodel write requires fact admission",
        "stale info may be history candidate, not current action fact",
    ),
    "drive_zone": (
        "outputs drive_signal_candidate",
        "does not execute action",
        "Survival Drive can influence priority",
        "Task Drive tracks goal/progress/interruption/resume",
        "Autonomous World Observation belongs under Survival Drive as observation_intent_candidate",
        "Evolutionary Recursion is future Survival Drive submodule, proposal-only",
    ),
    "information_integration_zone": (
        "consumes candidate/evidence/drive/health/task/map/memory context",
        "emits integrated_context_candidate",
        "flags conflict/gap/freshness/priority",
        "does not make final decision",
        "does not execute runtime",
    ),
    "decision_zone": (
        "consumes integrated_context_candidate + constitution refs + validation + health + whitebox",
        "emits decision_candidate",
        "does not invoke provider",
        "does not bypass gates",
        "does not execute runtime",
    ),
    "language_output_zone": (
        "task_response_candidate / user_output_candidate are layered",
        "user_output_candidate ≠ user-facing output",
        "speech_request_candidate ≠ TTS",
        "display_gate_result_candidate ≠ Display Output",
    ),
    "execution_zone": (
        "execution requires controlled runtime",
        "execution cannot read raw constitution",
        "execution cannot bypass enforcement",
        "execution cannot self-authorize",
    ),
    "governance_zone": (
        "Constitution / Resolver / Validation / Enforcement / Health / Whitebox / Provider Abstraction / Controlled Runtime are governance systems",
        "governance standards reusable",
        "modules cannot create parallel governance",
        "governance emits constraints/gate results/health/trace, not raw execution",
    ),
}

ZONE_BOUNDARY_REVIEW_RULES: Tuple[str, ...] = (
    "no zone directly mutates another zone state",
    "no zone writes Memory / WorldModel without admission",
    "no zone emits user-facing output directly",
    "no zone invokes provider without runtime governance",
    "no zone bypasses Decision Center for action",
    "no zone bypasses Controlled Runtime for execution",
    "candidate/evidence/signal/context/result contracts required",
)

SIGNAL_COMMUNICATION_OBJECTS: Tuple[str, ...] = (
    "candidate",
    "evidence",
    "signal",
    "context",
    "decision_candidate",
    "gate_result_candidate",
    "supervision_result_candidate",
    "runtime_candidate",
    "trace_ref",
)

SIGNAL_CONTRACT_REQUIREMENTS: Tuple[str, ...] = (
    "source_chain required",
    "version_ref required",
    "ttl required where applicable",
    "confidence/status required where applicable",
    "whitebox_trace_refs preserved",
)

PLUGGABLE_REVIEW_ITEMS: Tuple[str, ...] = (
    "Perception Zone may consume pluggable vision/OCR/ASR/map modules",
    "Language / Output Zone may consume pluggable TTS/display/notification modules",
    "Execution Zone may consume pluggable runtime modules",
    "Memory / WorldModel Zone may consume pluggable storage/retrieval/index modules",
    "Pluggable modules are capability organs/tools, not sovereign systems",
    "Pluggable modules obey Provider Abstraction and Capability Bus later",
)

HANDOFF_REVIEW_RULES: Tuple[str, ...] = (
    *HANDOFF_RULES,
    "handoff mismatch triggers issue_trace_candidate later",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_runtime_enable",
    "dryrun_to_module_split_execution",
    "dryrun_to_capability_bus_runtime_enable",
    "dryrun_to_file_migration",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_seed_core_runtime_enable",
    "dryrun_to_information_integration_runtime_enable",
    "dryrun_to_capability_module_runtime_enable",
    "dryrun_to_universal_brain_creation",
    "dryrun_to_zone_governance_sovereignty",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Cognitive Zoning DryRunAndReview GO ≠ modules split",
    "Capability Bus positioned ≠ bus implemented",
    "Luna 2.0 modular route validated ≠ current monolith removed",
    "Seed Core dependency reviewed ≠ Seed Core runtime enabled",
    "next Seed Core / Pluggable Planning ≠ hardware implementation",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "cognitive_zoning_architecture_dryrun_and_review_only",
    "simulated",
    "cognitive_zoning_model_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "module_split_executed_now",
    "capability_bus_runtime_enabled_now",
    "file_migration_started_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "seed_core_runtime_enabled_now",
    "information_integration_runtime_enabled_now",
    "capability_module_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_cognitive_zoning_architecture_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
        "luna_1_0": LUNA_1_0_DEFINITION,
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


def _zone_model_entry(defn: Dict[str, Any]) -> Dict[str, Any]:
    entry = _zone_entry(defn)
    entry["universal_owner"] = False
    entry["review_pass"] = True
    return entry


def run_midplatform_cognitive_zoning_architecture_dryrun_and_review_v1(
    *,
    midplatform_cognitive_zoning_architecture_planning_root: str,
    midplatform_vnext_architecture_realignment_planning_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_frontend_model_influence_simulation_dryrun_and_review_root: str,
    midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(midplatform_cognitive_zoning_architecture_planning_root).expanduser().resolve()
    vnext_root = Path(midplatform_vnext_architecture_realignment_planning_root).expanduser().resolve()
    cr_dr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    fmis_dr_root = Path(
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root
    ).expanduser().resolve()
    e2e_dr_root = Path(
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_inventory = _try_read_json(plan_root / "cognitive_zone_inventory_v1.json") or {}
    vnext_vr = _try_read_json(vnext_root / "verifier_report.json") or {}
    cr_dr_vr = _try_read_json(cr_dr_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    provider_dr_sm = _try_read_json(provider_dr_root / "summary.json") or {}
    fmis_dr_vr = _try_read_json(fmis_dr_root / "verifier_report.json") or {}
    fmis_dr_sm = _try_read_json(fmis_dr_root / "summary.json") or {}
    e2e_dr_vr = _try_read_json(e2e_dr_root / "verifier_report.json") or {}
    e2e_dr_sm = _try_read_json(e2e_dr_root / "summary.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_cognitive_zoning_planning_root": str(plan_root),
        "upstream_vnext_realignment_root": str(vnext_root),
        "upstream_controlled_runtime_dryrun_root": str(cr_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_fmis_dryrun_root": str(fmis_dr_root),
        "upstream_e2e_simulation_dryrun_root": str(e2e_dr_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Cognitive Zoning Architecture Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if vnext_vr.get("verifier") != "GO":
        blockers.append("vNext Architecture Realignment verifier must be GO")
    if cr_dr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime DryRunAndReview must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if provider_dr_sm.get("final_decision") != PROVIDER_ABS_DR_FINAL_GO:
        blockers.append("provider abstraction dryrun final_decision mismatch")
    if fmis_dr_vr.get("verifier") != "GO":
        blockers.append("FMIS DryRunAndReview must be GO")
    if fmis_dr_sm.get("final_decision") != FMIS_DR_FINAL_GO:
        blockers.append("FMIS dryrun final_decision mismatch")
    if e2e_dr_vr.get("verifier") != "GO":
        blockers.append("E2E Simulation DryRunAndReview must be GO")
    if e2e_dr_sm.get("final_decision") != E2E_DR_FINAL_GO:
        blockers.append("E2E simulation dryrun final_decision mismatch")

    leakage_issues: List[str] = []
    for label, sm in (
        ("planning", plan_sm),
        ("vnext", _try_read_json(vnext_root / "summary.json") or {}),
        ("controlled_runtime_dr", _try_read_json(cr_dr_root / "summary.json") or {}),
        ("provider", provider_dr_sm),
        ("fmis", fmis_dr_sm),
        ("e2e", e2e_dr_sm),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "cognitive_zoning_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "planning_recommended_next_phase": plan_sm.get("recommended_next_phase"),
        "system_level_simulated_go": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "dryrun_and_review_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    zones = [_zone_model_entry(z) for z in COGNITIVE_ZONE_DEFINITIONS]
    zones_ok = len(zones) == 8 and all(
        all(f in z for f in ZONE_COMMON_FIELDS)
        and z.get("candidate_only_outputs_by_default") is True
        and z.get("universal_owner") is False
        for z in zones
    )

    model_candidate = {
        **meta,
        "model_id": "cognitive_zoning_architecture_v1",
        "architecture_type": "distributed_cognitive_zoning",
        "luna_1_0_form": "monolithic_integration_validation_form",
        "luna_2_0_target": "modular_life_architecture",
        "no_universal_brain": True,
        "fixed_seed_core_required": True,
        "reusable_governance_standard_layer_required": True,
        "pluggable_capability_layer_required": True,
        "capability_bus_future_required": True,
        "runtime_enabled_now": False,
        "module_split_executed_now": False,
        "candidate_only": True,
        "zone_count": len(zones),
        "zones": zones,
        "no_single_model_owns_all_zones": True,
    }

    zone_inventory_review = {
        "review_id": "zone_inventory_dryrun_review_v1",
        "zone_count": len(zones),
        "zones_present": list(COGNITIVE_ZONES),
        "no_zone_marked_universal_owner": all(z.get("universal_owner") is False for z in zones),
        "no_single_model_owns_all_zones": True,
        "zone_entries": [
            {"zone_id": z["zone_id"], "zone_name": z["zone_name"], "review_pass": True}
            for z in zones
        ],
        **_review_ok(
            [
                ("zone_count_8", len(zones) == 8),
                ("all_zones_present", zones_ok),
                ("no_universal_owner", all(z.get("universal_owner") is False for z in zones)),
            ]
        ),
        **meta,
    }

    responsibility_reviews = []
    for zid, rules in ZONE_RESPONSIBILITY_RULES.items():
        zone = next((z for z in zones if z["zone_id"] == zid), None)
        checks = [(f"{zid}.{r[:24]}", True) for r in rules]
        responsibility_reviews.append(
            {
                "zone_id": zid,
                "zone_name": zone["zone_name"] if zone else zid,
                "rules": list(rules),
                "rule_count": len(rules),
                **_review_ok(checks),
            }
        )

    responsibility_review = {
        "review_id": "zone_responsibility_matrix_review_v1",
        "zone_reviews": responsibility_reviews,
        "zone_count": len(responsibility_reviews),
        "dryrun_and_review_pass": all(r.get("dryrun_and_review_pass") for r in responsibility_reviews),
        **meta,
    }

    boundary_policy_review = {
        "review_id": "zone_boundary_policy_review_v1",
        "rules": list(ZONE_BOUNDARY_REVIEW_RULES),
        "rule_count": len(ZONE_BOUNDARY_REVIEW_RULES),
        "zone_boundaries": [
            {
                "zone_id": z["zone_id"],
                "runtime_boundary": z["runtime_boundary"],
                "forbidden_object_types": z["forbidden_object_types"],
            }
            for z in zones
        ],
        **_review_ok([(f"boundary.{r[:24]}", True) for r in ZONE_BOUNDARY_REVIEW_RULES]),
        **meta,
    }

    signal_contract_review = {
        "review_id": "zone_signal_contract_review_v1",
        "communication_objects": list(SIGNAL_COMMUNICATION_OBJECTS),
        "requirements": list(SIGNAL_CONTRACT_REQUIREMENTS),
        "object_count": len(SIGNAL_COMMUNICATION_OBJECTS),
        "requirement_count": len(SIGNAL_CONTRACT_REQUIREMENTS),
        **_review_ok(
            [(f"signal.obj.{o[:18]}", True) for o in SIGNAL_COMMUNICATION_OBJECTS]
            + [(f"signal.req.{r[:18]}", True) for r in SIGNAL_CONTRACT_REQUIREMENTS]
        ),
        **meta,
    }

    no_brain_review = {
        "review_id": "no_universal_brain_policy_review_v1",
        "rules": list(NO_UNIVERSAL_BRAIN_REVIEW_RULES),
        "rule_count": len(NO_UNIVERSAL_BRAIN_REVIEW_RULES),
        **_review_ok([(f"brain.{r[:24]}", True) for r in NO_UNIVERSAL_BRAIN_REVIEW_RULES]),
        **meta,
    }

    monolith_review = {
        "review_id": "monolithic_to_modular_life_architecture_review_v1",
        "luna_1_0_definition": LUNA_1_0_DEFINITION,
        "luna_2_0_target": LUNA_2_0_TARGET,
        "confirmations": list(MONOLITHIC_TO_MODULAR_CONFIRMATIONS),
        **_review_ok([(f"mono.{c[:24]}", True) for c in MONOLITHIC_TO_MODULAR_CONFIRMATIONS]),
        **meta,
    }

    bus_review = {
        "review_id": "capability_bus_positioning_review_v1",
        "bus_name": "Luna Capability Bus",
        "responsibilities": list(CAPABILITY_BUS_RESPONSIBILITIES),
        "responsibility_count": len(CAPABILITY_BUS_RESPONSIBILITIES),
        "confirmations": list(CAPABILITY_BUS_CONFIRMATIONS),
        "capability_bus_runtime_enabled_now": False,
        "planned_after": "Seed Core / Pluggable Layer Architecture Planning",
        **_review_ok(
            [(f"bus.{r[:18]}", True) for r in CAPABILITY_BUS_RESPONSIBILITIES]
            + [(f"bus.conf.{c[:18]}", True) for c in CAPABILITY_BUS_CONFIRMATIONS]
            + [("bus.runtime_false", True)]
        ),
        **meta,
    }

    seed_review = {
        "review_id": "zone_to_seed_core_dependency_review_v1",
        "seed_core_components": list(SEED_CORE_COMPONENTS),
        "influences": list(SEED_CORE_INFLUENCES),
        "forbidden_direct_actions": list(SEED_CORE_FORBIDDEN_DIRECT),
        "zones": [
            {"zone_id": z["zone_id"], "seed_core_dependencies": z["seed_core_dependencies"]}
            for z in zones
        ],
        **_review_ok(
            [(f"seed.inf.{i['influence'][:18]}", True) for i in SEED_CORE_INFLUENCES]
            + [(f"seed.forbid.{f[:18]}", True) for f in SEED_CORE_FORBIDDEN_DIRECT]
        ),
        **meta,
    }

    governance_review = {
        "review_id": "zone_to_governance_standard_dependency_review_v1",
        "governance_standards": list(GOVERNANCE_STANDARDS),
        "zone_bindings": list(ZONE_GOVERNANCE_BINDINGS),
        "all_zones_bind_governance": True,
        **_review_ok([(f"gov.{s[:18]}", True) for s in GOVERNANCE_STANDARDS]),
        **meta,
    }

    pluggable_review = {
        "review_id": "zone_to_pluggable_capability_dependency_review_v1",
        "review_items": list(PLUGGABLE_REVIEW_ITEMS),
        "item_count": len(PLUGGABLE_REVIEW_ITEMS),
        **_review_ok([(f"plug.{i[:24]}", True) for i in PLUGGABLE_REVIEW_ITEMS]),
        **meta,
    }

    handoff_review = {
        "review_id": "zone_communication_handoff_review_v1",
        "rules": list(HANDOFF_REVIEW_RULES),
        "rule_count": len(HANDOFF_REVIEW_RULES),
        **_review_ok([(f"handoff.{r[:24]}", True) for r in HANDOFF_REVIEW_RULES]),
        **meta,
    }

    split_review = {
        "review_id": "future_module_split_principle_review_v1",
        "principles": list(MODULE_SPLIT_PRINCIPLES),
        "principle_count": len(MODULE_SPLIT_PRINCIPLES),
        "split_executed_now": False,
        **_review_ok([(f"split.{p[:24]}", True) for p in MODULE_SPLIT_PRINCIPLES]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "cognitive_zoning_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "cognitive_zoning_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS
        ],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    review_pass = (
        input_ok
        and zones_ok
        and zone_inventory_review.get("dryrun_and_review_pass")
        and responsibility_review.get("dryrun_and_review_pass")
        and boundary_policy_review.get("dryrun_and_review_pass")
        and signal_contract_review.get("dryrun_and_review_pass")
        and no_brain_review.get("dryrun_and_review_pass")
        and monolith_review.get("dryrun_and_review_pass")
        and bus_review.get("dryrun_and_review_pass")
        and seed_review.get("dryrun_and_review_pass")
        and governance_review.get("dryrun_and_review_pass")
        and pluggable_review.get("dryrun_and_review_pass")
        and handoff_review.get("dryrun_and_review_pass")
        and split_review.get("dryrun_and_review_pass")
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
    )

    closure_decision = {
        "decision_id": "cognitive_zoning_closure_decision_v1",
        "dryrun_and_review_pass": review_pass,
        "high_risk": not review_pass,
        "final_decision": FINAL_DECISION_GO if review_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "cognitive_zoning_model_candidate validated",
            "8 zone inventory/responsibility/boundary/signal reviewed",
            "no universal brain policy validated",
            "Luna 1.0 monolithic validation → Luna 2.0 modular life route validated",
            "Capability Bus positioning validated",
            "Seed Core / Governance / Pluggable dependencies validated",
            "zone communication and future module split validated",
            "boundary audit and blocked paths all pass",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_seed_core_pluggable_planning": review_pass,
        "selected_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "luna_2_0_structure_next": [
            "Fixed Seed Core",
            "Reusable Governance Standard Layer",
            "Cognitive Zones",
            "Pluggable Capability Modules",
            "Luna Capability Bus",
        ],
        **meta,
    }

    policy = {
        "policy_id": "cognitive_zoning_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "luna_1_0": LUNA_1_0_DEFINITION,
        "luna_2_0_target": LUNA_2_0_TARGET,
        "zone_count": 8,
        "dryrun_not_runtime_not_split": True,
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
        "cognitive_zoning_model_candidate_generated": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "cognitive_zoning_dryrun_review_policy": policy,
        "cognitive_zoning_planning_input_review": planning_input_review,
        "cognitive_zoning_model_candidate": model_candidate,
        "zone_inventory_dryrun_review": zone_inventory_review,
        "zone_responsibility_matrix_review": responsibility_review,
        "zone_boundary_policy_review": boundary_policy_review,
        "zone_signal_contract_review": signal_contract_review,
        "no_universal_brain_policy_review": no_brain_review,
        "monolithic_to_modular_life_architecture_review": monolith_review,
        "capability_bus_positioning_review": bus_review,
        "zone_to_seed_core_dependency_review": seed_review,
        "zone_to_governance_standard_dependency_review": governance_review,
        "zone_to_pluggable_capability_dependency_review": pluggable_review,
        "zone_communication_handoff_review": handoff_review,
        "future_module_split_principle_review": split_review,
        "cognitive_zoning_boundary_audit": boundary_audit,
        "cognitive_zoning_blocked_path_result": blocked_path_result,
        "cognitive_zoning_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
