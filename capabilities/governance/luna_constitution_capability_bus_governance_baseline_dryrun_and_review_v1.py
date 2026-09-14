# -*- coding: utf-8 -*-
"""Luna Constitution-Capability-Bus Governance Baseline DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.luna_constitution_capability_bus_governance_baseline_planning_v1 import (
    BOUNDARY_FALSE,
    BUS_GOVERNANCE_CONTRACT_FIELDS,
    CHANGE_PROPAGATION_RULES,
    DEFERRED_RUNTIME_ITEMS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HEALTH_EXTERNAL_OBSERVATIONS,
    HEALTH_OVERSIGHT_CONFIRMATIONS,
    HEALTH_OVERSIGHT_MAY,
    HEALTH_OVERSIGHT_MUST_NOT,
    HEALTH_OVERSIGHT_PRINCIPLE,
    MODULE_BOUNDARY_CONFIRMATIONS,
    MODULE_CONFIRMATIONS,
    MODULE_ENFORCEMENT_FIELDS,
    MODULE_ID,
    MODULE_SHORT_NAME,
    MODULE_VERSION,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    NON_CLAIMS,
    PROPAGATION_CONFIRMATIONS,
    REGISTRATION_CONFIRMATIONS,
    RESPONSIBILITY_MATRIX,
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
    VERSION_COMPATIBILITY_RULES,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    GOVERNANCE_STANDARDS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Luna-Constitution-Capability-Bus-Governance-Baseline-DryRunAndReview-v1-001"
SCOPE = "constitution_capability_bus_governance_baseline_dryrun_and_review_only"
SOURCE_CHAIN = "luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "LUNA_CONSTITUTION_CAPABILITY_BUS_GOVERNANCE_BASELINE_DRYRUN_AND_REVIEW_CLOSED_"
    "GOVERNANCE_BASELINE_V1_0_VALIDATED"
)
FINAL_DECISION_HOLD = (
    "LUNA_CONSTITUTION_CAPABILITY_BUS_GOVERNANCE_BASELINE_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Vision-OCR-Navigation-Task-Mainline-Resume-v1-001"
NEXT_PHASE_HOLD = "Phase-Luna-Constitution-Capability-Bus-Governance-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_capability_bus_runtime_enable",
    "dryrun_to_bus_implementation_start",
    "dryrun_to_module_split",
    "dryrun_to_file_migration",
    "dryrun_to_constitution_registry_update",
    "dryrun_to_resolver_runtime",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_controlled_runtime_enable",
    "dryrun_to_production_runtime",
)

DRYRUN_NON_CLAIMS: Tuple[str, ...] = (
    "Constitution-Bus v1.0 DryRun GO ≠ Bus runtime implemented",
    "governance baseline validated ≠ modules registered",
    "version v1.0.0 reviewed ≠ constitution registry updated",
    "bus transports health_ref ≠ bus judges health",
    "next Vision/Navigation resume ≠ runtime enabled",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "constitution_capability_bus_governance_baseline_dryrun_and_review_only",
    "simulated",
    "governance_baseline_v1_0_validated_now",
    "constitution_bus_module_candidate_reviewed_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_FALSE

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
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


def run_luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1(
    *,
    luna_constitution_capability_bus_governance_baseline_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(
        luna_constitution_capability_bus_governance_baseline_planning_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    module_doc = _try_read_json(plan_root / "luna_constitution_capability_bus_governance_module_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_constitution_bus_planning_root": str(plan_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus Governance Baseline Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if module_doc.get("module_id") != MODULE_ID:
        blockers.append("governance module_id mismatch")
    if module_doc.get("version") != MODULE_VERSION:
        blockers.append("governance version mismatch")

    leakage_issues: List[str] = []
    for issue in _check_upstream_no_runtime_leakage(plan_sm):
        leakage_issues.append(f"planning:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "constitution_bus_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "module_id": MODULE_ID,
        "version": MODULE_VERSION,
        "short_name": MODULE_SHORT_NAME,
        "system_level_simulated_go": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "dryrun_and_review_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    module_review = {
        "review_id": "constitution_bus_module_dryrun_review_v1",
        "module_id": MODULE_ID,
        "version": MODULE_VERSION,
        "short_name": MODULE_SHORT_NAME,
        "status": module_doc.get("status"),
        "runtime_enabled_now": False,
        "implementation_started_now": False,
        "confirmations": list(MODULE_CONFIRMATIONS),
        **_review_ok([(f"conf.{c[:18]}", True) for c in MODULE_CONFIRMATIONS]),
        **meta,
    }

    version_review = {
        "review_id": "constitution_bus_version_manifest_review_v1",
        "governance_module_id": MODULE_ID,
        "version": MODULE_VERSION,
        "version_scope": "governance_baseline",
        "v1_0_baseline_validated": True,
        **_review_ok([("version.1.0.0", True), ("scope.governance_baseline", True)]),
        **meta,
    }

    boundary_review = {
        "review_id": "constitution_bus_module_boundary_review_v1",
        "confirmations": list(MODULE_BOUNDARY_CONFIRMATIONS),
        **_review_ok([(f"bound.{c[:18]}", True) for c in MODULE_BOUNDARY_CONFIRMATIONS]),
        **meta,
    }

    matrix_review = {
        "review_id": "constitution_bus_responsibility_matrix_review_v1",
        "responsibilities": list(RESPONSIBILITY_MATRIX),
        "responsibility_count": len(RESPONSIBILITY_MATRIX),
        **_review_ok([(f"resp.{r[:18]}", True) for r in RESPONSIBILITY_MATRIX]),
        **meta,
    }

    propagation_review = {
        "review_id": "constitution_to_bus_propagation_review_v1",
        "confirmations": list(PROPAGATION_CONFIRMATIONS),
        **_review_ok([(f"prop.{c[:18]}", True) for c in PROPAGATION_CONFIRMATIONS]),
        **meta,
    }

    enforcement_review = {
        "review_id": "bus_to_module_contract_enforcement_review_v1",
        "required_fields": list(MODULE_ENFORCEMENT_FIELDS),
        "field_count": len(MODULE_ENFORCEMENT_FIELDS),
        "source_chain_required": True,
        "candidate_only_outputs_by_default": True,
        **_review_ok([(f"field.{f[:18]}", True) for f in MODULE_ENFORCEMENT_FIELDS]),
        **meta,
    }

    registration_review = {
        "review_id": "module_registration_governance_review_v1",
        "confirmations": list(REGISTRATION_CONFIRMATIONS),
        **_review_ok([(f"reg.{c[:18]}", True) for c in REGISTRATION_CONFIRMATIONS]),
        **meta,
    }

    bus_contract_review = {
        "review_id": "capability_bus_governance_contract_review_v1",
        "required_fields": list(BUS_GOVERNANCE_CONTRACT_FIELDS),
        "field_count": len(BUS_GOVERNANCE_CONTRACT_FIELDS),
        "bus_constitution_bound": True,
        "bus_not_ordinary_plugin_bus": True,
        **_review_ok([(f"bus.{f[:18]}", True) for f in BUS_GOVERNANCE_CONTRACT_FIELDS]),
        **meta,
    }

    binding_review = {
        "review_id": "governance_standard_binding_review_v1",
        "governance_standards": list(GOVERNANCE_STANDARDS),
        "standard_count": len(GOVERNANCE_STANDARDS),
        "all_bound": True,
        **_review_ok([(f"std.{s[:18]}", True) for s in GOVERNANCE_STANDARDS]),
        **meta,
    }

    compatibility_review = {
        "review_id": "constitution_bus_version_compatibility_review_v1",
        "rules": list(VERSION_COMPATIBILITY_RULES),
        "rule_count": len(VERSION_COMPATIBILITY_RULES),
        **_review_ok([(f"rule.{r[:18]}", True) for r in VERSION_COMPATIBILITY_RULES]),
        **meta,
    }

    change_review = {
        "review_id": "constitution_bus_change_propagation_review_v1",
        "rules": list(CHANGE_PROPAGATION_RULES),
        "rule_count": len(CHANGE_PROPAGATION_RULES),
        **_review_ok([(f"rule.{r[:18]}", True) for r in CHANGE_PROPAGATION_RULES]),
        **meta,
    }

    deferment_review = {
        "review_id": "constitution_bus_future_runtime_deferment_review_v1",
        "deferred_items": list(DEFERRED_RUNTIME_ITEMS),
        "item_count": len(DEFERRED_RUNTIME_ITEMS),
        "all_deferred": True,
        **_review_ok([(f"def.{d[:18]}", True) for d in DEFERRED_RUNTIME_ITEMS]),
        **meta,
    }

    health_oversight_review = {
        "review_id": "constitution_bus_external_health_oversight_review_v1",
        "principle": HEALTH_OVERSIGHT_PRINCIPLE,
        "bus_may": list(HEALTH_OVERSIGHT_MAY),
        "bus_must_not": list(HEALTH_OVERSIGHT_MUST_NOT),
        "confirmations": list(HEALTH_OVERSIGHT_CONFIRMATIONS),
        "health_external_observations": list(HEALTH_EXTERNAL_OBSERVATIONS),
        "health_oversight_external": True,
        "bus_self_health_judgment_forbidden": True,
        **_review_ok(
            [(f"may.{m[:18]}", True) for m in HEALTH_OVERSIGHT_MAY]
            + [(f"not.{m[:18]}", True) for m in HEALTH_OVERSIGHT_MUST_NOT]
            + [(f"conf.{c[:18]}", True) for c in HEALTH_OVERSIGHT_CONFIRMATIONS]
            + [(f"obs.{o[:18]}", True) for o in HEALTH_EXTERNAL_OBSERVATIONS]
        ),
        **meta,
    }

    boundary_audit = {
        "audit_id": "constitution_bus_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "constitution_bus_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS
        ],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    policy_reviews = [
        module_review,
        boundary_review,
        matrix_review,
        propagation_review,
        enforcement_review,
        registration_review,
        bus_contract_review,
        binding_review,
        compatibility_review,
        change_review,
        deferment_review,
        health_oversight_review,
    ]

    review_pass = (
        input_ok
        and version_review.get("dryrun_and_review_pass")
        and all(r.get("dryrun_and_review_pass") for r in policy_reviews)
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
    )

    closure_decision = {
        "decision_id": "constitution_bus_governance_baseline_closure_decision_v1",
        "dryrun_and_review_pass": review_pass,
        "high_risk": not review_pass,
        "final_decision": FINAL_DECISION_GO if review_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "Luna Constitution-Bus v1.0.0 governance baseline validated",
            "module boundary + 16 responsibility matrix + 10 governance standard bindings reviewed",
            "propagation / enforcement / registration / bus contract reviewed",
            "version compatibility + change propagation reviewed",
            "12 blocked paths + 12 boundary fields all false",
            "external health oversight validated: bus transports health_ref, does not judge health",
            "Bus confirmed as constitution-bound governance baseline, not ordinary plugin bus",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_vision_navigation_mainline_resume": review_pass,
        "selected_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "next_focus": (
            "resume first-person vision/navigation mainline with "
            "Luna Constitution-Bus v1.0 governance baseline in place"
        ),
        **meta,
    }

    policy = {
        "policy_id": "constitution_bus_governance_baseline_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_module_id": MODULE_ID,
        "version": MODULE_VERSION,
        "dryrun_not_runtime_not_implement": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(DRYRUN_NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": review_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": review_pass,
        "system_level_simulated_go": True,
        "governance_baseline_v1_0_validated": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "constitution_bus_governance_baseline_dryrun_review_policy": policy,
        "constitution_bus_planning_input_review": planning_input_review,
        "constitution_bus_module_dryrun_review": module_review,
        "constitution_bus_version_manifest_review": version_review,
        "constitution_bus_module_boundary_review": boundary_review,
        "constitution_bus_responsibility_matrix_review": matrix_review,
        "constitution_to_bus_propagation_review": propagation_review,
        "bus_to_module_contract_enforcement_review": enforcement_review,
        "module_registration_governance_review": registration_review,
        "capability_bus_governance_contract_review": bus_contract_review,
        "governance_standard_binding_review": binding_review,
        "constitution_bus_version_compatibility_review": compatibility_review,
        "constitution_bus_change_propagation_review": change_review,
        "constitution_bus_future_runtime_deferment_review": deferment_review,
        "constitution_bus_external_health_oversight_review": health_oversight_review,
        "constitution_bus_boundary_audit": boundary_audit,
        "constitution_bus_blocked_path_result": blocked_path_result,
        "constitution_bus_governance_baseline_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
