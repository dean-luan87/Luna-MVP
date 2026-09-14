# -*- coding: utf-8 -*-
"""Seed Core / Pluggable Layer Architecture Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_cognitive_zoning_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CZ_DR_FINAL_GO,
    NEXT_PHASE_GO as CZ_DR_NEXT_PHASE,
    NO_UNIVERSAL_BRAIN_REVIEW_RULES,
)
from capabilities.governance.midplatform_cognitive_zoning_architecture_planning_v1 import (
    CAPABILITY_BUS_RESPONSIBILITIES,
    SEED_CORE_FORBIDDEN_DIRECT,
    SEED_CORE_INFLUENCES,
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
)
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CR_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    GOVERNANCE_STANDARDS,
    INVARIANT_BOUNDARIES,
    PRODUCT_FORMS,
    SEED_CORE_COMPONENTS,
    SEED_CORE_CONFIRMATIONS,
    VARIANT_BOUNDARIES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)

PHASE_ID = "Phase-Seed-Core-Pluggable-Layer-Architecture-Planning-v1-001"
SCOPE = "seed_core_pluggable_layer_architecture_planning_only"
SOURCE_CHAIN = "seed_core_pluggable_layer_architecture_planning_v1"

UPSTREAM_CZ_DR_FINAL = CZ_DR_FINAL_GO
UPSTREAM_CZ_DR_NEXT = CZ_DR_NEXT_PHASE

FINAL_DECISION_GO = "SEED_CORE_PLUGGABLE_LAYER_ARCHITECTURE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "SEED_CORE_PLUGGABLE_LAYER_ARCHITECTURE_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Seed-Core-Pluggable-Layer-Architecture-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Seed-Core-Pluggable-Layer-Architecture-Issue-Review-v1-001"

LUNA_1_0_FORM = "monolithic_integration_validation_form"
LUNA_2_0_TARGET = "fixed_seed_core_plus_pluggable_capability_layer"

SEED_CORE_INVARIANTS: Tuple[str, ...] = (
    "hardware form",
    "product form",
    "model provider",
    "local/cloud deployment",
    "capability module availability",
    "UI/output channel",
    "runtime implementation",
)

SURVIVAL_DRIVE_SUBMODULES: Tuple[str, ...] = (
    "Safety Survival",
    "Resource Survival",
    "Health Survival",
    "Autonomous World Observation",
    "Emotion Engine",
    "Evolutionary Recursion",
)

EMOTION_ENGINE_RULES: Tuple[str, ...] = (
    "responsible for social integration, emotion understanding, relationship management, companionship expression, interaction rhythm",
    "outputs emotion_state_candidate / relationship_context_candidate / social_adaptation_hint",
    "does not directly modify code",
    "does not directly add skill",
    "does not directly modify constitution",
    "does not directly invoke runtime",
)

EVOLUTIONARY_RECURSION_RULES: Tuple[str, ...] = (
    "responsible for market adaptation, capability evolution, skill add/remove proposals, logic optimization proposals, code optimization candidates, product feedback absorption",
    "outputs evolution_proposal_candidate / skill_expansion_candidate / logic_revision_candidate / code_optimization_candidate",
    "proposal_only=true",
    "does not directly modify code",
    "does not directly go live",
    "does not directly modify constitution",
    "does not directly enable runtime",
    "does not directly replace model",
)

PERSONAL_CONTINUITY_COVERAGE: Tuple[str, ...] = (
    "long_term_memory",
    "emotion_state",
    "personality_parameters",
    "relationship_model",
    "user_preference",
    "belief_value_candidate_store",
    "interaction_history_index",
    "whitebox_life_trace_index",
    "personal_worldmodel_candidate_snapshot",
    "life_state_snapshot",
)

PERSONAL_CONTINUITY_CONFIRMATIONS: Tuple[str, ...] = (
    "Personal Continuity Module ≠ generic storage",
    "Personal Continuity Module ≠ Seed Core",
    "Personal Continuity Module cannot be read without identity/owner authorization later",
    "write requires memory/emotion admission later",
    "backup/restore/migration require continuity protocol later",
    "clone/fork must be controlled",
    "encryption/permission policy required later",
)

PLUGGABLE_CAPABILITY_MODULES: Tuple[str, ...] = (
    "Vision module",
    "OCR module",
    "ASR module",
    "TTS module",
    "Map / Location module",
    "Display module",
    "Notification module",
    "Voice Output / Audio module",
    "Sensor module",
    "Provider Adapter module",
    "Memory / Retrieval / Index module",
    "Device Action module",
    "Product-specific business module",
)

PLUGGABLE_LAYER_CONFIRMATIONS: Tuple[str, ...] = (
    "capability modules are organs/tools, not sovereign systems",
    "capability modules can be added/removed/replaced",
    "capability modules must declare contract",
    "capability modules must obey Provider Abstraction if provider-backed",
    "capability modules output candidate/evidence/signal/context/result",
    "capability modules cannot emit fact/action/user_output directly",
    "capability modules cannot bypass governance standards",
    "capability modules cannot open runtime by themselves",
)

CAPABILITY_MODULE_CONTRACT_FIELDS: Tuple[str, ...] = (
    "module_id",
    "module_type",
    "capability_domain",
    "product_form_compatibility",
    "input_contract_ref",
    "output_contract_ref",
    "provider_candidate_refs",
    "resource_requirement",
    "health_status_ref",
    "authorization_requirement",
    "runtime_candidate_ref",
    "evidence_output_channel",
    "failure_route",
    "version_ref",
    "source_chain_required",
    "candidate_only_outputs_by_default",
    "governance_standard_refs",
)

CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES: Tuple[str, ...] = (
    "module_registration",
    "module_discovery",
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
)

CAPABILITY_BUS_ARCHITECTURE_CONFIRMATIONS: Tuple[str, ...] = (
    "Capability Bus is not runtime execution",
    "Capability Bus does not replace Seed Core",
    "Capability Bus does not replace Personal Continuity Module",
    "Capability Bus does not replace Decision Center",
    "Capability Bus does not authorize runtime",
    "Capability Bus does not mutate module logic",
    "Capability Bus standardizes connection/governance interface",
)

PRODUCT_FORM_TOPOLOGY_CONFIRMATIONS: Tuple[str, ...] = (
    "Product form can change hardware/capability/provider",
    "Product form cannot remove Seed Core",
    "Product form cannot bypass governance standards",
    "Product form must declare capability profile",
    "thin-client form must still bind to Seed Core / identity / permission root",
)

INVARIANT_FIXED: Tuple[str, ...] = (
    "Seed Core",
    "Seed Core Signal Bus semantics",
    "reusable governance standards",
    "candidate/evidence semantics",
    "provider abstraction principle",
    "controlled runtime principle",
    "no universal brain principle",
    "no module sovereignty principle",
    "identity continuity principles",
)

PLUGGABLE_VARIABLE: Tuple[str, ...] = (
    "models",
    "providers",
    "sensors",
    "hardware modules",
    "output modules",
    "runtime implementations",
    "product-specific modules",
    "UI/output channels",
    "business capabilities",
)

SEED_CORE_ZONE_INFLUENCES: Tuple[Dict[str, str], ...] = (
    *SEED_CORE_INFLUENCES,
    {"influence": "Information Integration priority", "via": "integration_priority_hint"},
    {"influence": "Controlled Runtime readiness hint", "via": "runtime_readiness_hint"},
)

SEED_CORE_ZONE_FORBIDDEN: Tuple[str, ...] = (
    *SEED_CORE_FORBIDDEN_DIRECT,
    "mutate zone state directly",
)

IDENTITY_BOUNDARY_RULES: Tuple[str, ...] = (
    "migration allowed later with authorization",
    "backup allowed later with encryption and owner control",
    "restore allowed later with identity continuity validation",
    "silent clone forbidden",
    "unauthorized fork forbidden",
    "parallel identity activation requires governance policy later",
    "memory/emotion data access requires authorization",
    "continuity module loss/theft risk requires protection policy later",
)

MODULE_REGISTRATION_PLAN: Tuple[str, ...] = (
    "module announces identity",
    "module declares capability",
    "module declares input/output contract",
    "module declares provider candidates",
    "module declares health status",
    "module declares resource requirements",
    "module declares runtime requirements",
    "governance validates module",
    "Decision/Integration can consume module only after registration",
)

MODULE_HEALTH_PERMISSION_RUNTIME_RULES: Tuple[str, ...] = (
    "module health status required",
    "module permission required",
    "module runtime candidate required",
    "module cannot self-authorize",
    "module cannot auto-switch provider",
    "module cannot execute without Controlled Runtime later",
    "module failure emits issue_trace_candidate",
)

MIGRATION_RISKS: Tuple[str, ...] = (
    "identity split",
    "unauthorized clone",
    "memory corruption",
    "emotion state pollution",
    "relationship model poisoning",
    "schema incompatibility",
    "lost continuity module",
    "stolen continuity module",
    "cloud/local state divergence",
    "rollback failure",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Seed Core / Pluggable Planning GO ≠ Seed Core runtime enabled",
    "Personal Continuity Module planned ≠ memory/emotion hardware implemented",
    "Capability Bus planned ≠ bus implemented",
    "module registration planned ≠ modules split",
    "product topology planned ≠ hardware product ready",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("seed_core_pluggable_layer_architecture_planning_only",)

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
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/seed_core_pluggable_layer_architecture_planning"
)

SEED_CORE_COMPONENT_MATRIX: Tuple[Dict[str, Any], ...] = (
    {
        "component_id": "survival_drive",
        "component_name": "Survival Drive",
        "component_role": "safety/resource/health survival and autonomous observation drive signals",
        "input_signals": ["health_signal", "resource_status", "safety_hint", "observation_feedback"],
        "output_signals": ["survival_priority_hint", "observation_intent_candidate", "drive_signal_candidate"],
        "allowed_outputs": ["drive_signal_candidate", "observation_intent_candidate", "priority_hint"],
        "forbidden_outputs": ["action_execution", "user_output", "runtime_enable", "memory_write"],
        "governed_by": ["Health Supervision Standard", "Non-Claims Standard"],
        "downstream_consumers": ["Drive Zone", "Information Integration Zone", "Decision Zone"],
    },
    {
        "component_id": "task_drive",
        "component_name": "Task Drive",
        "component_role": "goal/progress/interrupt/resume task drive signals",
        "input_signals": ["task_state_candidate", "health_signal", "resource_status"],
        "output_signals": ["task_drive_signal", "task_priority_hint", "interrupt_resume_hint"],
        "allowed_outputs": ["drive_signal_candidate", "task_priority_hint"],
        "forbidden_outputs": ["action_execution", "user_output", "runtime_enable"],
        "governed_by": ["Health Supervision Standard", "Gate / Enforcement Standard"],
        "downstream_consumers": ["Drive Zone", "Information Integration Zone", "Decision Zone"],
    },
    {
        "component_id": "resource_governance",
        "component_name": "Resource Governance",
        "component_role": "resource allocation and budget hints",
        "input_signals": ["health_signal", "resource_status", "capability_availability"],
        "output_signals": ["resource_governance_hint", "allocation_hint"],
        "allowed_outputs": ["resource_governance_hint", "allocation_hint"],
        "forbidden_outputs": ["runtime_enable", "provider_invocation", "memory_write"],
        "governed_by": ["Health Supervision Standard", "Controlled Runtime Standard"],
        "downstream_consumers": ["Perception Zone", "Execution Zone", "Governance Zone"],
    },
    {
        "component_id": "health_management",
        "component_name": "Health Management",
        "component_role": "system health pressure and supervision hints",
        "input_signals": ["health_supervision_result", "module_health_status"],
        "output_signals": ["health_signal_candidate", "health_pressure_hint"],
        "allowed_outputs": ["health_signal_candidate", "health_pressure_hint"],
        "forbidden_outputs": ["runtime_enable", "user_output", "gate_bypass"],
        "governed_by": ["Health Supervision Standard", "Whitebox Trace Standard"],
        "downstream_consumers": ["Drive Zone", "Decision Zone", "Governance Zone"],
    },
    {
        "component_id": "system_optimization",
        "component_name": "System Optimization",
        "component_role": "system optimization and efficiency hints",
        "input_signals": ["performance_metrics", "health_signal", "resource_status"],
        "output_signals": ["optimization_hint", "efficiency_hint"],
        "allowed_outputs": ["optimization_hint", "efficiency_hint"],
        "forbidden_outputs": ["runtime_enable", "code_modification", "constitution_change"],
        "governed_by": ["Health Supervision Standard", "Non-Claims Standard"],
        "downstream_consumers": ["Information Integration Zone", "Governance Zone"],
    },
    {
        "component_id": "autonomous_world_observation",
        "component_name": "Autonomous World Observation",
        "component_role": "autonomous observation intent under Survival Drive",
        "input_signals": ["survival_priority_hint", "health_signal", "observation_feedback"],
        "output_signals": ["observation_intent_candidate", "observation_priority_hint"],
        "allowed_outputs": ["observation_intent_candidate", "observation_priority_hint"],
        "forbidden_outputs": ["provider_invocation", "runtime_enable", "user_output"],
        "governed_by": ["Health Supervision Standard", "Provider Abstraction Standard"],
        "downstream_consumers": ["Perception Zone", "Drive Zone"],
    },
    {
        "component_id": "seed_core_signal_bus",
        "component_name": "Seed Core Signal Bus",
        "component_role": "internal Seed Core signal routing bus",
        "input_signals": ["all_seed_core_component_outputs"],
        "output_signals": ["routed_signal_candidate", "signal_bundle"],
        "allowed_outputs": ["signal_candidate", "hint_candidate", "priority_hint"],
        "forbidden_outputs": ["fact", "action_execution", "user_output", "runtime_enable"],
        "governed_by": ["Input / Output Boundary Standard", "Whitebox Trace Standard"],
        "downstream_consumers": ["Cognitive Zones", "Governance Zone"],
    },
)

PRODUCT_FORM_TOPOLOGY: Tuple[Dict[str, Any], ...] = (
    {
        "product_form": "Luna Badge",
        "seed_core_location": "edge_device",
        "personal_continuity_module_location": "edge_device_or_paired_host",
        "capability_modules_available": ["Sensor", "Notification", "Voice Output"],
        "local_compute_level": "minimal",
        "cloud_dependency_level": "optional",
        "offline_capability_level": "limited",
        "privacy_boundary": "edge_first",
        "bus_topology": "local_bus_with_cloud_sync",
        "runtime_limitations": ["no_heavy_vision", "no_display"],
    },
    {
        "product_form": "Luna Glasses",
        "seed_core_location": "edge_device_or_paired_phone",
        "personal_continuity_module_location": "paired_phone_or_host",
        "capability_modules_available": ["Vision", "OCR", "ASR", "Map", "Display", "Voice Output"],
        "local_compute_level": "moderate",
        "cloud_dependency_level": "optional",
        "offline_capability_level": "moderate",
        "privacy_boundary": "edge_first_with_selective_cloud",
        "bus_topology": "hybrid_local_cloud_bus",
        "runtime_limitations": ["controlled_runtime_required"],
    },
    {
        "product_form": "Phone",
        "seed_core_location": "device",
        "personal_continuity_module_location": "device_or_secure_enclave",
        "capability_modules_available": ["Vision", "OCR", "ASR", "TTS", "Map", "Display", "Notification"],
        "local_compute_level": "high",
        "cloud_dependency_level": "optional",
        "offline_capability_level": "high",
        "privacy_boundary": "device_first",
        "bus_topology": "local_bus_with_cloud_optional",
        "runtime_limitations": ["battery_aware_runtime"],
    },
    {
        "product_form": "Desktop",
        "seed_core_location": "local_host",
        "personal_continuity_module_location": "local_host",
        "capability_modules_available": ["Vision", "OCR", "ASR", "TTS", "Display", "Memory/Retrieval"],
        "local_compute_level": "very_high",
        "cloud_dependency_level": "low",
        "offline_capability_level": "very_high",
        "privacy_boundary": "local_first",
        "bus_topology": "local_bus",
        "runtime_limitations": ["controlled_runtime_required"],
    },
    {
        "product_form": "Home Host / NAS",
        "seed_core_location": "home_host",
        "personal_continuity_module_location": "home_host_encrypted_store",
        "capability_modules_available": ["Memory/Retrieval", "Provider Adapter", "Notification"],
        "local_compute_level": "high",
        "cloud_dependency_level": "low",
        "offline_capability_level": "very_high",
        "privacy_boundary": "home_network_first",
        "bus_topology": "home_bus_with_device_peers",
        "runtime_limitations": ["no_direct_user_output_without_gate"],
    },
    {
        "product_form": "Robot",
        "seed_core_location": "robot_compute_unit",
        "personal_continuity_module_location": "robot_or_paired_host",
        "capability_modules_available": ["Vision", "Sensor", "Map", "Device Action", "Voice Output"],
        "local_compute_level": "high",
        "cloud_dependency_level": "optional",
        "offline_capability_level": "moderate",
        "privacy_boundary": "edge_first",
        "bus_topology": "robot_local_bus",
        "runtime_limitations": ["device_action_requires_controlled_runtime"],
    },
    {
        "product_form": "Cloud Luna",
        "seed_core_location": "cloud_service",
        "personal_continuity_module_location": "encrypted_cloud_store",
        "capability_modules_available": ["Provider Adapter", "Memory/Retrieval", "Product-specific business"],
        "local_compute_level": "cloud",
        "cloud_dependency_level": "high",
        "offline_capability_level": "none",
        "privacy_boundary": "cloud_with_encryption",
        "bus_topology": "cloud_bus",
        "runtime_limitations": ["no_direct_hardware_access"],
    },
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
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


def _component_entry(defn: Dict[str, Any]) -> Dict[str, Any]:
    return {**defn, "runtime_enabled_now": False}


def _capability_module_contract(module_type: str, domain: str) -> Dict[str, Any]:
    slug = module_type.lower().replace(" ", "_").replace("/", "_")
    return {
        "module_id": f"capability_{slug}_v1",
        "module_type": module_type,
        "capability_domain": domain,
        "product_form_compatibility": list(PRODUCT_FORMS),
        "input_contract_ref": f"input_contract:{slug}",
        "output_contract_ref": f"output_contract:{slug}",
        "provider_candidate_refs": [f"provider_candidate:{slug}"] if "Provider" not in module_type else [],
        "resource_requirement": f"resource_req:{slug}",
        "health_status_ref": f"health_status:{slug}",
        "authorization_requirement": "governance_authorization_required",
        "runtime_candidate_ref": f"runtime_candidate:{slug}",
        "evidence_output_channel": f"evidence_channel:{slug}",
        "failure_route": f"failure_route:{slug}",
        "version_ref": "v1",
        "source_chain_required": True,
        "candidate_only_outputs_by_default": True,
        "governance_standard_refs": list(GOVERNANCE_STANDARDS),
    }


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false")
    return issues


def run_seed_core_pluggable_layer_architecture_planning_v1(
    *,
    midplatform_cognitive_zoning_architecture_dryrun_and_review_root: str,
    midplatform_cognitive_zoning_architecture_planning_root: str,
    midplatform_vnext_architecture_realignment_planning_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    cz_dr_root = Path(midplatform_cognitive_zoning_architecture_dryrun_and_review_root).expanduser().resolve()
    cz_plan_root = Path(midplatform_cognitive_zoning_architecture_planning_root).expanduser().resolve()
    vnext_root = Path(midplatform_vnext_architecture_realignment_planning_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_dr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    cz_dr_sm = _try_read_json(cz_dr_root / "summary.json") or {}
    cz_dr_vr = _try_read_json(cz_dr_root / "verifier_report.json") or {}
    cz_plan_vr = _try_read_json(cz_plan_root / "verifier_report.json") or {}
    vnext_vr = _try_read_json(vnext_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    provider_dr_sm = _try_read_json(provider_dr_root / "summary.json") or {}
    cr_dr_vr = _try_read_json(cr_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_cognitive_zoning_dryrun_root": str(cz_dr_root),
        "upstream_cognitive_zoning_planning_root": str(cz_plan_root),
        "upstream_vnext_realignment_root": str(vnext_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_controlled_runtime_dryrun_root": str(cr_dr_root),
        "output_root": str(out_root),
    }

    if cz_dr_vr.get("verifier") != "GO":
        blockers.append("Cognitive Zoning DryRunAndReview verifier must be GO")
    if cz_dr_sm.get("final_decision") != UPSTREAM_CZ_DR_FINAL:
        blockers.append("cognitive zoning dryrun final_decision mismatch")
    if cz_dr_sm.get("recommended_next_phase") != UPSTREAM_CZ_DR_NEXT:
        blockers.append("cognitive zoning dryrun recommended_next_phase mismatch")
    if cz_plan_vr.get("verifier") != "GO":
        blockers.append("Cognitive Zoning Planning verifier must be GO")
    if vnext_vr.get("verifier") != "GO":
        blockers.append("vNext Architecture Realignment verifier must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if provider_dr_sm.get("final_decision") != PROVIDER_ABS_DR_FINAL_GO:
        blockers.append("provider abstraction dryrun final_decision mismatch")
    if cr_dr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime DryRunAndReview must be GO")

    brain_review = _try_read_json(cz_dr_root / "no_universal_brain_policy_review_v1.json") or {}
    if not brain_review.get("dryrun_and_review_pass"):
        blockers.append("No Universal Brain policy must pass")

    resp_review = _try_read_json(cz_dr_root / "zone_responsibility_matrix_review_v1.json") or {}
    drive_review = next(
        (z for z in (resp_review.get("zone_reviews") or []) if z.get("zone_id") == "drive_zone"),
        {},
    )
    evo_rule = "Evolutionary Recursion is future Survival Drive submodule, proposal-only"
    if evo_rule not in (drive_review.get("rules") or []):
        blockers.append("Evolutionary Recursion must be registered as future Survival Drive submodule")

    bus_review = _try_read_json(cz_dr_root / "capability_bus_positioning_review_v1.json") or {}
    if not bus_review.get("dryrun_and_review_pass"):
        blockers.append("Capability Bus positioning must pass")
    if bus_review.get("capability_bus_runtime_enabled_now") is not False:
        blockers.append("Capability Bus must not be runtime enabled")

    leakage_issues: List[str] = []
    for label, sm in (
        ("cognitive_zoning_dr", cz_dr_sm),
        ("cognitive_zoning_plan", _try_read_json(cz_plan_root / "summary.json") or {}),
        ("vnext", _try_read_json(vnext_root / "summary.json") or {}),
        ("provider", provider_dr_sm),
        ("controlled_runtime_dr", _try_read_json(cr_dr_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "cognitive_zoning_input_review_v1",
        "cognitive_zoning_dryrun_verifier": cz_dr_vr.get("verifier"),
        "cognitive_zoning_dryrun_final_decision": cz_dr_sm.get("final_decision"),
        "no_universal_brain_pass": brain_review.get("dryrun_and_review_pass"),
        "capability_bus_positioned_not_implemented": True,
        "evolutionary_recursion_proposal_only": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "planning_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    components = [_component_entry(c) for c in SEED_CORE_COMPONENT_MATRIX]

    architecture_model = {
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
        "runtime_enabled_now": False,
        "hardware_implementation_started_now": False,
        "candidate_only": True,
    }

    fixed_seed_core = {
        "definition_id": "fixed_seed_core_definition_v1",
        "seed_core_role": "fixed life kernel invariant across product/hardware/provider",
        "invariants": list(SEED_CORE_INVARIANTS),
        "invariant_count": len(SEED_CORE_INVARIANTS),
        "components": list(SEED_CORE_COMPONENTS),
        "component_count": 7,
        "confirmations": list(SEED_CORE_CONFIRMATIONS),
        **meta,
    }

    component_matrix = {
        "matrix_id": "seed_core_component_matrix_v1",
        "components": components,
        "component_count": len(components),
        **meta,
    }

    survival_drive = {
        "placeholder_id": "survival_drive_architecture_placeholder_v1",
        "future_submodules": list(SURVIVAL_DRIVE_SUBMODULES),
        "submodule_count": len(SURVIVAL_DRIVE_SUBMODULES),
        "emotion_engine": {
            "rules": list(EMOTION_ENGINE_RULES),
            "outputs": [
                "emotion_state_candidate",
                "relationship_context_candidate",
                "social_adaptation_hint",
            ],
        },
        "evolutionary_recursion": {
            "rules": list(EVOLUTIONARY_RECURSION_RULES),
            "outputs": [
                "evolution_proposal_candidate",
                "skill_expansion_candidate",
                "logic_revision_candidate",
                "code_optimization_candidate",
            ],
            "proposal_only": True,
        },
        **meta,
    }

    personal_continuity = {
        "positioning_id": "personal_continuity_module_positioning_v1",
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
        "confirmations": list(PERSONAL_CONTINUITY_CONFIRMATIONS),
        **meta,
    }

    pluggable_layer = {
        "definition_id": "pluggable_capability_layer_definition_v1",
        "capability_modules": list(PLUGGABLE_CAPABILITY_MODULES),
        "module_count": len(PLUGGABLE_CAPABILITY_MODULES),
        "confirmations": list(PLUGGABLE_LAYER_CONFIRMATIONS),
        **meta,
    }

    module_contracts = [
        _capability_module_contract(m, m.split(" module")[0].strip())
        for m in PLUGGABLE_CAPABILITY_MODULES
    ]
    capability_contract = {
        "contract_id": "capability_module_contract_v1",
        "required_fields": list(CAPABILITY_MODULE_CONTRACT_FIELDS),
        "module_contracts": module_contracts,
        "contract_count": len(module_contracts),
        **meta,
    }

    capability_bus = {
        "placeholder_id": "luna_capability_bus_architecture_placeholder_v1",
        "bus_name": "Luna Capability Bus",
        "responsibilities": list(CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES),
        "responsibility_count": len(CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES),
        "confirmations": list(CAPABILITY_BUS_ARCHITECTURE_CONFIRMATIONS),
        "capability_bus_runtime_enabled_now": False,
        "planned_not_implemented": True,
        **meta,
    }

    bus_matrix = {
        "matrix_id": "capability_bus_responsibility_matrix_v1",
        "responsibilities": [
            {"responsibility_id": r, "runtime_enabled_now": False, "implemented_now": False}
            for r in CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES
        ],
        "responsibility_count": len(CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES),
        **meta,
    }

    product_topology = {
        "matrix_id": "product_form_topology_matrix_v1",
        "product_forms": list(PRODUCT_FORM_TOPOLOGY),
        "form_count": len(PRODUCT_FORM_TOPOLOGY),
        "confirmations": list(PRODUCT_FORM_TOPOLOGY_CONFIRMATIONS),
        **meta,
    }

    invariant_review = {
        "review_id": "invariant_vs_pluggable_boundary_review_v1",
        "invariant_fixed": list(INVARIANT_FIXED),
        "pluggable_variable": list(PLUGGABLE_VARIABLE),
        "invariant_count": len(INVARIANT_FIXED),
        "pluggable_count": len(PLUGGABLE_VARIABLE),
        "boundary_clear": True,
        **meta,
    }

    seed_zone_matrix = {
        "matrix_id": "seed_core_to_cognitive_zone_influence_matrix_v1",
        "influences": list(SEED_CORE_ZONE_INFLUENCES),
        "forbidden_direct_actions": list(SEED_CORE_ZONE_FORBIDDEN),
        "influence_count": len(SEED_CORE_ZONE_INFLUENCES),
        **meta,
    }

    identity_boundary = {
        "policy_id": "personal_continuity_identity_boundary_policy_v1",
        "rules": list(IDENTITY_BOUNDARY_RULES),
        "rule_count": len(IDENTITY_BOUNDARY_RULES),
        **meta,
    }

    registration_plan = {
        "plan_id": "module_registration_and_discovery_plan_v1",
        "registration_steps": list(MODULE_REGISTRATION_PLAN),
        "step_count": len(MODULE_REGISTRATION_PLAN),
        "bus_required": True,
        "implemented_now": False,
        **meta,
    }

    health_permission_plan = {
        "plan_id": "module_health_permission_runtime_plan_v1",
        "rules": list(MODULE_HEALTH_PERMISSION_RUNTIME_RULES),
        "rule_count": len(MODULE_HEALTH_PERMISSION_RUNTIME_RULES),
        **meta,
    }

    risk_register = {
        "register_id": "migration_backup_restore_risk_register_v1",
        "risks": [
            {"risk_id": r, "planned_only": True, "governance_executed": False}
            for r in MIGRATION_RISKS
        ],
        "risk_count": len(MIGRATION_RISKS),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "seed_core_pluggable_layer_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate seed_core_pluggable_layer_architecture_candidate",
            "verify Seed Core 7 components",
            "verify Personal Continuity Module positioning",
            "verify Pluggable Capability Layer",
            "verify Capability Bus placeholder",
            "verify Product Form topology",
            "verify invariant/pluggable boundary",
            "verify module registration/discovery plan",
            "no runtime enabled",
            "no file split",
            "no hardware implementation",
        ],
        **meta,
    }

    components_ok = len(components) == 7
    planning_pass = input_ok and components_ok

    planning_decision = {
        "decision_id": "seed_core_pluggable_layer_architecture_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "architecture_summary": [
            "Fixed Seed Core = life kernel (7 components, invariant)",
            "Personal Continuity Module = identity/memory/emotion continuity carrier",
            "Pluggable Capability Layer = capability organs/tools",
            "Luna Capability Bus = future modular connection layer",
            "Product Form Layer = variable hardware/topology",
        ],
        **meta,
    }

    policy = {
        "policy_id": "seed_core_pluggable_layer_architecture_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "luna_2_0": "Modular Life Architecture",
        "planning_not_runtime_not_hardware_not_split": True,
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
        "seed_core_pluggable_layer_architecture_planning_policy": policy,
        "cognitive_zoning_input_review": input_review,
        "seed_core_pluggable_layer_architecture_model": architecture_model,
        "fixed_seed_core_definition": fixed_seed_core,
        "seed_core_component_matrix": component_matrix,
        "survival_drive_architecture_placeholder": survival_drive,
        "personal_continuity_module_positioning": personal_continuity,
        "pluggable_capability_layer_definition": pluggable_layer,
        "capability_module_contract": capability_contract,
        "luna_capability_bus_architecture_placeholder": capability_bus,
        "capability_bus_responsibility_matrix": bus_matrix,
        "product_form_topology_matrix": product_topology,
        "invariant_vs_pluggable_boundary_review": invariant_review,
        "seed_core_to_cognitive_zone_influence_matrix": seed_zone_matrix,
        "personal_continuity_identity_boundary_policy": identity_boundary,
        "module_registration_and_discovery_plan": registration_plan,
        "module_health_permission_runtime_plan": health_permission_plan,
        "migration_backup_restore_risk_register": risk_register,
        "seed_core_pluggable_layer_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "seed_core_pluggable_layer_architecture_planning_decision": planning_decision,
        "summary": summary,
    }
