# -*- coding: utf-8 -*-
"""Luna Constitution-Capability-Bus Governance Baseline Planning v1."""

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
from capabilities.governance.midplatform_information_integration_layer_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_DR_FINAL_GO,
    NEXT_PHASE_GO as II_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    GOVERNANCE_STANDARDS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_DR_FINAL_GO,
)
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL_GO,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SC_DR_FINAL_GO,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_planning_v1 import (
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
)

PHASE_ID = "Phase-Luna-Constitution-Capability-Bus-Governance-Baseline-Planning-v1-001"
SCOPE = "constitution_capability_bus_governance_baseline_planning_only"
SOURCE_CHAIN = "luna_constitution_capability_bus_governance_baseline_planning_v1"

UPSTREAM_II_DR_FINAL = II_DR_FINAL_GO
UPSTREAM_II_DR_NEXT = II_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "LUNA_CONSTITUTION_CAPABILITY_BUS_GOVERNANCE_BASELINE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "LUNA_CONSTITUTION_CAPABILITY_BUS_GOVERNANCE_BASELINE_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Luna-Constitution-Capability-Bus-Governance-Baseline-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Luna-Constitution-Capability-Bus-Governance-Issue-Review-v1-001"

MODULE_ID = "luna_constitution_capability_bus_governance_v1"
MODULE_VERSION = "1.0.0"
MODULE_SHORT_NAME = "Luna Constitution-Bus v1.0"
MODULE_STATUS = "governance_baseline_closed_candidate"

ARCHITECTURE_LAYERS: Tuple[Dict[str, str], ...] = (
    {"role": "Constitution", "function": "rule source"},
    {"role": "Resolver", "function": "rule interpretation / constraint_bundle generation"},
    {"role": "Reusable Governance Standard Layer", "function": "common governance standards"},
    {
        "role": "Capability Bus",
        "function": "module registration / discovery / contract exchange / governance binding",
    },
    {"role": "Controlled Runtime", "function": "later execution admission framework"},
    {
        "role": "Whitebox / Health / Validation",
        "function": "supervision / trace / enforcement support",
    },
)

GOVERNANCE_POWER_STRUCTURE: Tuple[Dict[str, str], ...] = (
    {"system": "Constitution-Bus", "analogy": "执政系统 / 组织系统"},
    {"system": "Health Management", "analogy": "监察系统 / 体检系统"},
    {
        "system": "Health Enforcement Supervisor",
        "analogy": "对执法层和总线运行状态的监察机关",
    },
    {"system": "Decision Center", "analogy": "综合裁决机关"},
    {"system": "Whitebox", "analogy": "公开审计 / 可解释档案系统"},
)

BUS_CORE_FUNCTIONS: Tuple[str, ...] = (
    "rule propagation",
    "module registration",
    "contract validation",
    "authorization refs",
    "version compatibility",
    "evidence channel",
    "provider binding",
    "runtime admission precondition",
)

BUS_CANNOT_SELF_JUDGE: Tuple[str, ...] = (
    "whether system is healthy",
    "whether system is running well",
    "whether rules may be exempted",
    "whether governance should continue",
    "whether supervision may be bypassed",
)

HEALTH_OVERSIGHT_PRINCIPLE = "Health Oversight Is External to Constitution-Bus"

HEALTH_OVERSIGHT_MAY: Tuple[str, ...] = (
    "transport health_status_ref",
    "require module health declaration",
    "expose health refs to Health Management / Decision Center / Whitebox / Controlled Runtime",
    "preserve health source_chain",
    "mark missing health_ref as contract gap",
)

HEALTH_OVERSIGHT_MUST_NOT: Tuple[str, ...] = (
    "compute health score",
    "judge health pass/fail",
    "self-certify bus health",
    "suppress health warning",
    "block module based on health by itself",
    "enable/degrade runtime based on health by itself",
    "replace Health Management",
    "replace Health Enforcement Supervisor",
)

HEALTH_OVERSIGHT_CONFIRMATIONS: Tuple[str, ...] = (
    "Constitution-Bus requires health indicators, but does not judge health",
    "Health Management acts as independent oversight",
    "Health Enforcement Supervisor observes governance / enforcement layer operation",
    "Decision Center and Controlled Runtime consume health refs for later decision/admission",
    "bus must be supervised by health system, not self-certify health",
)

HEALTH_EXTERNAL_OBSERVATIONS: Tuple[str, ...] = (
    "bus latency too high",
    "module registration abnormal",
    "contract validation frequent failure",
    "rule propagation loss",
    "version compatibility conflict",
    "module bypassing bus",
    "bus attempting to judge health / runtime / execution",
)

GOVERNANCE_SEPARATION_SUMMARY: Tuple[str, ...] = (
    "Constitution-Bus governs order",
    "Health governs state",
    "Validation governs compliance",
    "Whitebox governs visibility",
    "Decision governs adjudication",
    "Controlled Runtime governs execution admission",
)

MODULE_CONFIRMATIONS: Tuple[str, ...] = (
    "Bus is constitution-bound",
    "Bus is governance-aware",
    "Bus is not ordinary plugin bus",
    "Bus does not authorize runtime by itself",
    "Bus does not execute modules",
    "Bus does not replace Seed Core",
    "Bus does not replace Decision Center",
    "Bus does not replace Resolver",
    "Bus does not replace Controlled Runtime",
    "Bus does not replace Health Management",
    "Health Oversight Is External to Constitution-Bus",
)

VERSION_MANIFEST_COVERS: Tuple[str, ...] = (
    "Constitution binding",
    "Resolver / constraint propagation",
    "Reusable Governance Standards",
    "Capability Bus governance rules",
    "module registration/discovery baseline",
    "capability contract exchange",
    "provider abstraction binding",
    "health/status sync",
    "evidence output channel",
    "controlled runtime precondition binding",
    "version compatibility",
    "external health oversight policy",
)

VERSION_MANIFEST_DOES_NOT_COVER: Tuple[str, ...] = (
    "real bus runtime",
    "physical hardware implementation",
    "actual module split",
    "provider invocation",
    "production runtime",
)

MODULE_BOUNDARY_CONFIRMATIONS: Tuple[str, ...] = (
    "Constitution-Bus Module is governance baseline, not runtime",
    "raw constitution does not go directly to modules",
    "Resolver / constraint_bundle mediates rule propagation",
    "modules consume contracts / constraints / gate results, not raw rule authority",
    "bus can carry applicable_rule_refs as trace refs",
    "bus cannot let modules self-authorize",
    "bus cannot let modules create parallel governance",
)

RESPONSIBILITY_MATRIX: Tuple[str, ...] = (
    "rule_source_binding",
    "constraint_bundle_propagation",
    "module_registration_governance",
    "module_discovery_governance",
    "capability_contract_exchange",
    "input_output_contract_exchange",
    "provider_candidate_binding",
    "health_status_sync",
    "resource_requirement_declaration",
    "authorization_requirement_declaration",
    "runtime_candidate_binding",
    "evidence_output_channel",
    "failure_route_routing",
    "version_compatibility_check",
    "whitebox_trace_requirement",
    "non_claims_enforcement",
)

PROPAGATION_CHAIN: Tuple[str, ...] = (
    "Constitution / Domain Standard / User Output Constitution",
    "Resolver",
    "constraint_bundle",
    "reusable governance contracts",
    "Capability Bus governance contract",
    "module input/output/runtime/provider/health/evidence constraints",
)

PROPAGATION_CONFIRMATIONS: Tuple[str, ...] = (
    "constitution changes propagate through bundle/contracts",
    "ordinary constitution change should not rewrite modules",
    "breaking contract change requires compatibility phase",
    "modules cannot bind raw constitution as execution authority",
    "bus records version_ref / applicable_rule_refs / source_chain",
)

MODULE_ENFORCEMENT_FIELDS: Tuple[str, ...] = (
    "module_id",
    "module_type",
    "capability_domain",
    "zone_assignment",
    "input_contract_ref",
    "output_contract_ref",
    "provider_candidate_refs",
    "health_status_ref",
    "resource_requirement",
    "authorization_requirement",
    "runtime_candidate_ref",
    "evidence_output_channel",
    "failure_route",
    "version_ref",
    "governance_standard_refs",
)

MODULE_ENFORCEMENT_DEFAULTS: Tuple[str, ...] = (
    "source_chain_required",
    "candidate_only_outputs_by_default",
)

REGISTRATION_CONFIRMATIONS: Tuple[str, ...] = (
    "module cannot register without zone assignment",
    "module cannot register without input/output contract",
    "provider-backed module must bind Provider Abstraction",
    "runtime-capable module must bind Controlled Runtime Standard",
    "output-capable module must bind Gate / Enforcement Standard",
    "memory/worldmodel-capable module must bind admission policy later",
    "module registration does not equal runtime permission",
)

BUS_GOVERNANCE_CONTRACT_FIELDS: Tuple[str, ...] = (
    "governance_version_ref",
    "constitution_bundle_ref",
    "module_contract_ref",
    "capability_contract_ref",
    "provider_abstraction_ref",
    "validation_requirement_ref",
    "health_requirement_ref",
    "whitebox_trace_requirement_ref",
    "runtime_admission_requirement_ref",
    "evidence_requirement_ref",
    "failure_route_ref",
    "compatibility_version_ref",
)

VERSION_COMPATIBILITY_RULES: Tuple[str, ...] = (
    "semantic versioning required",
    "major version change may require module compatibility review",
    "minor version change may add optional governance fields",
    "patch version may clarify wording / non-breaking rules",
    "module contract must declare compatible governance_bus_version",
    "incompatible module enters hold / issue_trace",
    "no silent compatibility mutation",
)

CHANGE_PROPAGATION_RULES: Tuple[str, ...] = (
    "constitution change → resolver/bundle update",
    "governance standard change → bus contract update",
    "bus contract breaking change → compatibility phase",
    "module contract mismatch → issue_trace_candidate",
    "runtime policy change → controlled_runtime compatibility review",
    "version_ref must be preserved",
)

DEFERRED_RUNTIME_ITEMS: Tuple[str, ...] = (
    "Capability Bus runtime deferred",
    "module registration runtime deferred",
    "module discovery runtime deferred",
    "compatibility checker runtime deferred",
    "governance contract validator runtime deferred",
    "physical hardware bus deferred",
    "product form bus topology runtime deferred",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Constitution-Bus v1.0 Planning GO ≠ Bus runtime implemented",
    "version manifest planned ≠ constitution registry updated",
    "bus governance baseline planned ≠ modules split",
    "module registration contract planned ≠ modules registered",
    "bus transports health_ref ≠ bus judges health",
    "next DryRunAndReview ≠ runtime execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("constitution_capability_bus_governance_baseline_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "capability_bus_runtime_enabled_now",
    "bus_implementation_started_now",
    "module_split_executed_now",
    "file_migration_started_now",
    "constitution_registry_updated_now",
    "resolver_runtime_enabled_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "controlled_runtime_enabled_now",
    "production_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_planning"
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


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false")
    return issues


def run_luna_constitution_capability_bus_governance_baseline_planning_v1(
    *,
    midplatform_information_integration_layer_dryrun_and_review_root: str,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    seed_core_pluggable_layer_architecture_dryrun_and_review_root: str,
    midplatform_cognitive_zoning_architecture_dryrun_and_review_root: str,
    midplatform_vnext_architecture_realignment_planning_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    ii_dr_root = Path(
        midplatform_information_integration_layer_dryrun_and_review_root
    ).expanduser().resolve()
    ds_dr_root = Path(seed_core_drive_signal_contract_dryrun_and_review_root).expanduser().resolve()
    sc_dr_root = Path(seed_core_pluggable_layer_architecture_dryrun_and_review_root).expanduser().resolve()
    cz_dr_root = Path(midplatform_cognitive_zoning_architecture_dryrun_and_review_root).expanduser().resolve()
    vnext_root = Path(midplatform_vnext_architecture_realignment_planning_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_dr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    ii_dr_sm = _try_read_json(ii_dr_root / "summary.json") or {}
    ii_dr_vr = _try_read_json(ii_dr_root / "verifier_report.json") or {}
    ds_dr_vr = _try_read_json(ds_dr_root / "verifier_report.json") or {}
    sc_dr_vr = _try_read_json(sc_dr_root / "verifier_report.json") or {}
    sc_dr_sm = _try_read_json(sc_dr_root / "summary.json") or {}
    cz_dr_vr = _try_read_json(cz_dr_root / "verifier_report.json") or {}
    vnext_vr = _try_read_json(vnext_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    cr_dr_vr = _try_read_json(cr_dr_root / "verifier_report.json") or {}

    bus_review = (
        _try_read_json(sc_dr_root / "capability_bus_placeholder_review_v1.json")
        or _try_read_json(cz_dr_root / "capability_bus_positioning_review_v1.json")
        or {}
    )

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_information_integration_dryrun_root": str(ii_dr_root),
        "upstream_drive_signal_dryrun_root": str(ds_dr_root),
        "upstream_seed_core_pluggable_dryrun_root": str(sc_dr_root),
        "upstream_cognitive_zoning_dryrun_root": str(cz_dr_root),
        "upstream_vnext_realignment_root": str(vnext_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_controlled_runtime_dryrun_root": str(cr_dr_root),
        "output_root": str(out_root),
    }

    if ii_dr_vr.get("verifier") != "GO":
        blockers.append("Information Integration Layer DryRunAndReview must be GO")
    if ii_dr_sm.get("final_decision") != UPSTREAM_II_DR_FINAL:
        blockers.append("information integration dryrun final_decision mismatch")
    if ii_dr_sm.get("recommended_next_phase") != UPSTREAM_II_DR_NEXT:
        blockers.append("information integration dryrun recommended_next_phase mismatch")
    if ds_dr_vr.get("verifier") != "GO":
        blockers.append("Drive Signal Contract DryRunAndReview must be GO")
    if sc_dr_vr.get("verifier") != "GO":
        blockers.append("Seed Core / Pluggable DryRunAndReview must be GO")
    if sc_dr_sm.get("final_decision") != SC_DR_FINAL_GO:
        blockers.append("seed core pluggable dryrun final_decision mismatch")
    if cz_dr_vr.get("verifier") != "GO":
        blockers.append("Cognitive Zoning DryRunAndReview must be GO")
    if vnext_vr.get("verifier") != "GO":
        blockers.append("vNext Architecture Realignment Planning must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if cr_dr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime DryRunAndReview must be GO")
    leakage_issues: List[str] = []
    for label, sm in (
        ("ii_dr", ii_dr_sm),
        ("ds_dr", _try_read_json(ds_dr_root / "summary.json") or {}),
        ("sc_dr", sc_dr_sm),
        ("cz_dr", _try_read_json(cz_dr_root / "summary.json") or {}),
        ("vnext", _try_read_json(vnext_root / "summary.json") or {}),
        ("provider", _try_read_json(provider_dr_root / "summary.json") or {}),
        ("cr_dr", _try_read_json(cr_dr_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    if not bus_review:
        blockers.append("Capability Bus positioning review must exist")
    bus_positioned = bus_review.get("dryrun_and_review_pass") is True
    if bus_review and not bus_positioned:
        blockers.append("Capability Bus must be positioned as future modular connection layer")

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "upstream_information_integration_input_review_v1",
        "information_integration_dryrun_verifier": ii_dr_vr.get("verifier"),
        "information_integration_dryrun_final_decision": ii_dr_sm.get("final_decision"),
        "drive_signal_dryrun_verifier": ds_dr_vr.get("verifier"),
        "seed_core_pluggable_dryrun_verifier": sc_dr_vr.get("verifier"),
        "cognitive_zoning_dryrun_verifier": cz_dr_vr.get("verifier"),
        "vnext_realignment_verifier": vnext_vr.get("verifier"),
        "provider_abstraction_verifier": provider_dr_vr.get("verifier"),
        "controlled_runtime_verifier": cr_dr_vr.get("verifier"),
        "capability_bus_positioned": bus_positioned,
        "reusable_governance_standard_layer_defined": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "planning_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    governance_module = {
        "module_id": MODULE_ID,
        "module_name": "Luna Constitution-Bus Governance Module",
        "version": MODULE_VERSION,
        "short_name": MODULE_SHORT_NAME,
        "status": MODULE_STATUS,
        "module_type": "governance_bus_baseline_module",
        "architectural_layer": "ReusableGovernanceStandardLayer",
        "runtime_enabled_now": False,
        "implementation_started_now": False,
        "candidate_only": True,
        "definition": (
            "Constitution-bound Capability Bus Governance Baseline — "
            "not highest authority, but rule propagation and organizational "
            "governance system; health oversight is external to the bus"
        ),
        "governance_power_structure": list(GOVERNANCE_POWER_STRUCTURE),
        "bus_core_functions": list(BUS_CORE_FUNCTIONS),
        "bus_cannot_self_judge": list(BUS_CANNOT_SELF_JUDGE),
        "health_oversight_principle": HEALTH_OVERSIGHT_PRINCIPLE,
        "governance_separation_summary": list(GOVERNANCE_SEPARATION_SUMMARY),
        "architecture_layers": list(ARCHITECTURE_LAYERS),
        "layer_count": len(ARCHITECTURE_LAYERS),
        "confirmations": list(MODULE_CONFIRMATIONS),
        "confirmation_count": len(MODULE_CONFIRMATIONS),
        **meta,
    }

    version_manifest = {
        "manifest_id": "constitution_bus_version_manifest_v1",
        "governance_module_id": MODULE_ID,
        "version": MODULE_VERSION,
        "version_scope": "governance_baseline",
        "applies_to": "Luna 2.0 Modular Life Architecture",
        "covers": list(VERSION_MANIFEST_COVERS),
        "cover_count": len(VERSION_MANIFEST_COVERS),
        "does_not_cover": list(VERSION_MANIFEST_DOES_NOT_COVER),
        "does_not_cover_count": len(VERSION_MANIFEST_DOES_NOT_COVER),
        **meta,
    }

    module_boundary = {
        "boundary_id": "constitution_bus_module_boundary_v1",
        "confirmations": list(MODULE_BOUNDARY_CONFIRMATIONS),
        "confirmation_count": len(MODULE_BOUNDARY_CONFIRMATIONS),
        **meta,
    }

    responsibility_matrix = {
        "matrix_id": "constitution_bus_responsibility_matrix_v1",
        "responsibilities": list(RESPONSIBILITY_MATRIX),
        "responsibility_count": len(RESPONSIBILITY_MATRIX),
        **meta,
    }

    propagation_model = {
        "model_id": "constitution_to_bus_propagation_model_v1",
        "propagation_chain": list(PROPAGATION_CHAIN),
        "chain_length": len(PROPAGATION_CHAIN),
        "confirmations": list(PROPAGATION_CONFIRMATIONS),
        "confirmation_count": len(PROPAGATION_CONFIRMATIONS),
        **meta,
    }

    enforcement_model = {
        "model_id": "bus_to_module_contract_enforcement_model_v1",
        "required_fields": list(MODULE_ENFORCEMENT_FIELDS),
        "field_count": len(MODULE_ENFORCEMENT_FIELDS),
        "defaults": {
            "source_chain_required": True,
            "candidate_only_outputs_by_default": True,
        },
        "default_flags": list(MODULE_ENFORCEMENT_DEFAULTS),
        **meta,
    }

    registration_contract = {
        "contract_id": "module_registration_governance_contract_v1",
        "confirmations": list(REGISTRATION_CONFIRMATIONS),
        "confirmation_count": len(REGISTRATION_CONFIRMATIONS),
        **meta,
    }

    bus_contract = {
        "contract_id": "capability_bus_governance_contract_v1",
        "required_fields": list(BUS_GOVERNANCE_CONTRACT_FIELDS),
        "field_count": len(BUS_GOVERNANCE_CONTRACT_FIELDS),
        "bus_must_carry_governance": True,
        "bus_not_ordinary_plugin_bus": True,
        **meta,
    }

    binding_matrix = {
        "matrix_id": "governance_standard_binding_matrix_v1",
        "governance_standards": list(GOVERNANCE_STANDARDS),
        "standard_count": len(GOVERNANCE_STANDARDS),
        "all_standards_bound": True,
        **meta,
    }

    compatibility_policy = {
        "policy_id": "constitution_bus_version_compatibility_policy_v1",
        "rules": list(VERSION_COMPATIBILITY_RULES),
        "rule_count": len(VERSION_COMPATIBILITY_RULES),
        **meta,
    }

    change_propagation_policy = {
        "policy_id": "constitution_bus_change_propagation_policy_v1",
        "rules": list(CHANGE_PROPAGATION_RULES),
        "rule_count": len(CHANGE_PROPAGATION_RULES),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "constitution_bus_non_runtime_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "boundary_pass": True,
        **meta,
    }

    deferment_register = {
        "register_id": "constitution_bus_future_runtime_deferment_register_v1",
        "deferred_items": list(DEFERRED_RUNTIME_ITEMS),
        "item_count": len(DEFERRED_RUNTIME_ITEMS),
        **meta,
    }

    health_oversight_policy = {
        "policy_id": "constitution_bus_external_health_oversight_policy_v1",
        "principle": HEALTH_OVERSIGHT_PRINCIPLE,
        "principle_zh": "健康监察权独立于总线",
        "summary": "Constitution-Bus requires health indicators, but does not judge health",
        "bus_may": list(HEALTH_OVERSIGHT_MAY),
        "may_count": len(HEALTH_OVERSIGHT_MAY),
        "bus_must_not": list(HEALTH_OVERSIGHT_MUST_NOT),
        "must_not_count": len(HEALTH_OVERSIGHT_MUST_NOT),
        "confirmations": list(HEALTH_OVERSIGHT_CONFIRMATIONS),
        "confirmation_count": len(HEALTH_OVERSIGHT_CONFIRMATIONS),
        "health_external_observations": list(HEALTH_EXTERNAL_OBSERVATIONS),
        "observation_count": len(HEALTH_EXTERNAL_OBSERVATIONS),
        "governance_separation_summary": list(GOVERNANCE_SEPARATION_SUMMARY),
        "health_oversight_external": True,
        "bus_self_health_judgment_forbidden": True,
        **meta,
    }

    contracts_ok = (
        len(RESPONSIBILITY_MATRIX) == 16
        and len(GOVERNANCE_STANDARDS) == 10
        and len(BUS_GOVERNANCE_CONTRACT_FIELDS) == 12
        and len(VERSION_MANIFEST_COVERS) == 12
    )
    planning_pass = input_ok and contracts_ok

    baseline_closure = {
        "decision_id": "constitution_bus_baseline_closure_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "Luna Constitution-Bus Governance Module v1.0.0 baseline defined",
            "Constitution / Resolver / Governance Standards / Capability Bus unified as governance module",
            "16 responsibility matrix items + 10 governance standard bindings",
            "constitution-to-bus propagation + module contract enforcement defined",
            "version compatibility + change propagation policies defined",
            "external health oversight policy: bus transports health_ref, does not judge health",
            "Bus is constitution-bound governance baseline, not ordinary plugin bus or runtime",
        ],
        **meta,
    }

    policy = {
        "policy_id": "constitution_capability_bus_governance_baseline_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_module_id": MODULE_ID,
        "version": MODULE_VERSION,
        "short_name": MODULE_SHORT_NAME,
        "planning_not_runtime_not_implement": True,
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
        "final_decision": baseline_closure["final_decision"],
        "recommended_next_phase": baseline_closure["recommended_next_phase"],
        **meta,
    }

    return {
        "constitution_capability_bus_governance_baseline_policy": policy,
        "upstream_information_integration_input_review": input_review,
        "luna_constitution_capability_bus_governance_module": governance_module,
        "constitution_bus_version_manifest": version_manifest,
        "constitution_bus_module_boundary": module_boundary,
        "constitution_bus_responsibility_matrix": responsibility_matrix,
        "constitution_to_bus_propagation_model": propagation_model,
        "bus_to_module_contract_enforcement_model": enforcement_model,
        "module_registration_governance_contract": registration_contract,
        "capability_bus_governance_contract": bus_contract,
        "governance_standard_binding_matrix": binding_matrix,
        "constitution_bus_version_compatibility_policy": compatibility_policy,
        "constitution_bus_change_propagation_policy": change_propagation_policy,
        "constitution_bus_non_runtime_boundary_matrix": boundary_matrix,
        "constitution_bus_future_runtime_deferment_register": deferment_register,
        "constitution_bus_external_health_oversight_policy": health_oversight_policy,
        "constitution_bus_baseline_closure_decision": baseline_closure,
        "non_claims_register": non_claims,
        "summary": summary,
    }
