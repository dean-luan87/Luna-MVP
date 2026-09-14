# -*- coding: utf-8 -*-
"""Midplatform Model Governance Binding Standardization Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_BUS_DR_FINAL_GO,
)
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONTROLLED_RUNTIME_DR_FINAL_GO,
)
from capabilities.governance.midplatform_display_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DISPLAY_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_information_integration_layer_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SAFETY_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SPEECH_GATE_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
)
from capabilities.governance.model_profile_registry_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as REGISTRY_DR_FINAL_GO,
)
from capabilities.governance.module_local_model_profile_standardization_dryrun_and_review_v1 import (
    DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
    DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
    FINAL_DECISION_GO as MODULE_LOCAL_DR_FINAL_GO,
    NON_COMPLIANCE_HANDLING_DEFERRAL_CLAIM,
)
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    DOMAIN_COVERAGE,
    DUAL_VALIDATION_MECHANISM_ID,
    DUAL_VALIDATION_NON_CLAIMS,
    REGISTRY_REF,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)
from capabilities.governance.provider_abstraction_standard_alignment_planning_v1 import STANDARD_ID as PROVIDER_ABS_STANDARD_ID

PHASE_ID = "Phase-Midplatform-Model-Governance-Binding-Standardization-Planning-v1-001"
SCOPE = "midplatform_model_governance_binding_standardization_planning_only"
SOURCE_CHAIN = "midplatform_model_governance_binding_standardization_planning_v1"

FINAL_DECISION_GO = (
    "MIDPLATFORM_MODEL_GOVERNANCE_BINDING_STANDARDIZATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_MODEL_GOVERNANCE_BINDING_STANDARDIZATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Model-Governance-Binding-Standardization-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Model-Governance-Binding-Issue-Review-v1-001"

STANDARD_ID = "midplatform_model_governance_binding_standard_v1"
MODULE_LOCAL_PROFILE_STANDARD_REF = "module_local_model_profile_standard_v1"
CONSTITUTION_BUS_REF = "luna_constitution_capability_bus_governance_v1"
CAPABILITY_BUS_REF = "luna_capability_bus_governance_v1"
CONTROLLED_RUNTIME_FRAMEWORK_REF = "midplatform_controlled_runtime_framework_v1"
INFORMATION_INTEGRATION_REF = "midplatform_information_integration_layer_v1"
DECISION_CENTER_REF = "midplatform_decision_center_v1"

BINDING_SCHEMA_FIELDS: Tuple[str, ...] = (
    "midplatform_governance_binding_id",
    "module_local_profile_ref",
    "registry_model_profile_ref",
    "module_id",
    "capability_domain",
    "capability_stack_ref",
    "layered_governance_mapping_ref",
    "constitution_bus_ref",
    "capability_bus_contract_ref",
    "provider_abstraction_ref",
    "validation_requirement_ref",
    "health_requirement_ref",
    "whitebox_trace_requirement_ref",
    "information_integration_consumption_policy_ref",
    "decision_center_consumption_policy_ref",
    "gate_chain_requirement_ref",
    "controlled_runtime_requirement_ref",
    "memory_admission_requirement_ref",
    "worldmodel_admission_requirement_ref",
    "task_state_commit_requirement_ref",
    "privacy_identity_requirement_ref",
    "source_chain_requirement_ref",
    "evidence_requirement_ref",
    "issue_trace_requirement_ref",
    "version_compatibility_ref",
    "fallback_replacement_policy_ref",
    "non_compliance_handling_policy_ref_later",
    "model_selected_now",
    "model_invoked_now",
    "runtime_enabled_now",
)

STANDARD_DUTIES: Tuple[str, ...] = (
    "bind module-local model profiles to Constitution-Bus",
    "bind provider-backed models to Provider Abstraction",
    "bind candidate outputs to Information Integration",
    "bind decision-relevant outputs to Decision Center",
    "bind validation requirements",
    "bind health oversight requirements",
    "bind whitebox trace requirements",
    "bind output-capable modules to Gate Chain",
    "bind runtime-capable modules to Controlled Runtime",
    "bind memory/worldmodel-capable modules to Admission Gates",
    "expose binding refs for future controlled runtime readiness",
)

STANDARD_NOT: Tuple[str, ...] = (
    "model_selector",
    "provider_invoker",
    "runtime_executor",
    "benchmark_runner",
    "license_clearing_authority",
    "module_internal_self_check",
    "non_compliance_handling_executor",
    "universal_brain",
)

REUSED_GOVERNANCE_STANDARDS: Tuple[str, ...] = (
    "Model Profile Registry",
    "Module-Local Model Profile Standard",
    "Dual Validation Mechanism",
    "Layered Capability Stack Standard",
    "Layered Governance Mapping",
    "Constitution-Bus v1.0",
    "Provider Abstraction Standard",
    "Controlled Runtime Framework",
    "Luna Gate Chain / Enforcement Gate System",
    "Health Oversight Externality",
    "Whitebox Trace Standard",
    "Candidate/Evidence Contract pattern",
    "Boundary Matrix / Blocked Path / Non-Claims pattern",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Midplatform Binding Planning GO ≠ model connected",
    "governance binding planned ≠ runtime ready",
    "binding template ≠ real module pass",
    "non-compliance policy deferred ≠ enforcement implemented",
    "next DryRunAndReview ≠ model invocation",
    "Module Internal Self-Check GO ≠ Midplatform Interaction Check GO",
    "Midplatform Interaction Check GO ≠ Runtime Ready",
)

LAYER_BINDING_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "layer": "Layer 1 Current Scene Understanding",
        "layer_id": "layer_1_perception",
        "bindings": [
            "Constitution-Bus refs",
            "source_chain / confidence / ttl",
            "Validation / Whitebox",
            "Information Integration handoff",
        ],
        "forbidden": ["no direct fact/action"],
    },
    {
        "layer": "Layer 2 Spatiotemporal Continuity",
        "layer_id": "layer_2_spatiotemporal",
        "bindings": [
            "freshness / conflict / gap",
            "evidence chain",
            "World continuity hypothesis not fact",
            "Information Integration + Decision handoff",
        ],
        "forbidden": ["no WorldModel write"],
    },
    {
        "layer": "Layer 3 Navigation Application",
        "layer_id": "layer_3_navigation",
        "bindings": [
            "safety priority",
            "Decision Center",
            "Navigation Action Gate later",
            "Controlled Runtime later",
        ],
        "forbidden": ["no direct navigation action"],
    },
    {
        "layer": "Layer 4 Extended Capabilities",
        "layer_id": "layer_4_extended",
        "bindings": [
            "Privacy Gate",
            "Identity Gate",
            "Memory Admission",
            "higher validation",
        ],
        "forbidden": ["no identity fact by default"],
    },
    {
        "layer": "Layer 5 Long-Term Social / Personal",
        "layer_id": "layer_5_social_personal",
        "bindings": [
            "Personal Continuity",
            "Memory/WorldModel admission",
            "relationship/emotion governance",
            "long-term impact review",
        ],
        "forbidden": [],
    },
    {
        "layer": "Layer 6 Evolutionary Recursion",
        "layer_id": "layer_6_evolution",
        "bindings": [
            "proposal_only",
            "owner/governance review",
            "validation/rollback later",
        ],
        "forbidden": ["no code modification", "no skill addition"],
    },
)

BOUNDARY_TRUE: Tuple[str, ...] = ("midplatform_model_governance_binding_standardization_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "midplatform_binding_runtime_enabled_now",
    "model_selected_now",
    "model_downloaded_now",
    "model_invoked_now",
    "provider_invoked_now",
    "model_runtime_enabled_now",
    "benchmark_executed_now",
    "license_cleared_now",
    "security_review_completed_now",
    "training_started_now",
    "fine_tuning_started_now",
    "code_generation_executed_now",
    "skill_added_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "user_output_generated_now",
    "controlled_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_model_governance_binding_standardization_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
        "binding_runtime_enabled_now": False,
        "model_selection_allowed_now": False,
        "model_invocation_allowed_now": False,
        "controlled_runtime_allowed_now": False,
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


def _binding_template(
    template_id: str,
    module_id: str,
    capability_domain: str,
    registry_refs: List[str],
    layers: List[str],
    binding_confirmations: List[str],
    *,
    stack_layer: str = "layer_1_perception",
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    bindings = []
    for ref in registry_refs:
        bindings.append({
            "midplatform_governance_binding_id": f"{module_id}__{ref}__governance_binding",
            "module_local_profile_ref": f"{module_id}__{ref}",
            "registry_model_profile_ref": ref,
            "module_id": module_id,
            "capability_domain": capability_domain,
            "capability_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
            "capability_stack_layer": stack_layer,
            "layered_governance_mapping_ref": ADDENDUM_ID,
            "registry_ref": REGISTRY_REF,
            "constitution_bus_ref": CONSTITUTION_BUS_REF,
            "capability_bus_contract_ref": f"{module_id}_capability_bus_contract",
            "provider_abstraction_ref": PROVIDER_ABS_STANDARD_ID,
            "validation_requirement_ref": f"{module_id}__validation_requirement",
            "health_requirement_ref": f"{module_id}__health_requirement",
            "whitebox_trace_requirement_ref": f"{module_id}__whitebox_trace_requirement",
            "information_integration_consumption_policy_ref": (
                f"{module_id}__ii_consumption_policy"
            ),
            "decision_center_consumption_policy_ref": f"{module_id}__decision_consumption_policy",
            "gate_chain_requirement_ref": GATE_CHAIN_SYSTEM_ID,
            "controlled_runtime_requirement_ref": CONTROLLED_RUNTIME_FRAMEWORK_REF,
            "memory_admission_requirement_ref": "memory_admission_gate_later",
            "worldmodel_admission_requirement_ref": "worldmodel_admission_gate_later",
            "source_chain_requirement_ref": f"{module_id}__source_chain",
            "evidence_requirement_ref": f"{module_id}__evidence",
            "issue_trace_requirement_ref": f"{module_id}__issue_trace",
            "non_compliance_handling_policy_ref_later": DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
            "model_selected_now": False,
            "model_invoked_now": False,
            "runtime_enabled_now": False,
        })
    base = {
        "template_id": template_id,
        "module_id": module_id,
        "capability_domain": capability_domain,
        "registry_ref": REGISTRY_REF,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "midplatform_governance_binding_standard_ref": STANDARD_ID,
        "registry_model_profile_refs": registry_refs,
        "capability_layers": layers,
        "governance_bindings": bindings,
        "confirmations": binding_confirmations,
    }
    if extra:
        base.update(extra)
    return base


def run_midplatform_model_governance_binding_standardization_planning_v1(
    *,
    module_local_model_profile_standardization_dryrun_and_review_root: str,
    module_local_model_profile_standardization_planning_root: str,
    model_profile_registry_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    midplatform_information_integration_layer_dryrun_and_review_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_display_gate_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    ml_dr_root = Path(
        module_local_model_profile_standardization_dryrun_and_review_root
    ).expanduser().resolve()
    ml_plan_root = Path(
        module_local_model_profile_standardization_planning_root
    ).expanduser().resolve()
    registry_dr_root = Path(model_profile_registry_dryrun_and_review_root).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()
    ii_root = Path(
        midplatform_information_integration_layer_dryrun_and_review_root
    ).expanduser().resolve()
    safety_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    speech_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    display_root = Path(midplatform_display_gate_dryrun_and_review_root).expanduser().resolve()

    ml_dr_vr = _try_read_json(ml_dr_root / "verifier_report.json") or {}
    ml_dr_sm = _try_read_json(ml_dr_root / "summary.json") or {}
    ml_plan_sm = _try_read_json(ml_plan_root / "summary.json") or {}
    registry_dr_vr = _try_read_json(registry_dr_root / "verifier_report.json") or {}
    registry_dr_sm = _try_read_json(registry_dr_root / "summary.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    cb_sm = _try_read_json(cb_root / "summary.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    provider_sm = _try_read_json(provider_root / "summary.json") or {}
    cr_vr = _try_read_json(cr_root / "verifier_report.json") or {}
    cr_sm = _try_read_json(cr_root / "summary.json") or {}
    ii_vr = _try_read_json(ii_root / "verifier_report.json") or {}
    ii_sm = _try_read_json(ii_root / "summary.json") or {}
    safety_vr = _try_read_json(safety_root / "verifier_report.json") or {}
    safety_sm = _try_read_json(safety_root / "summary.json") or {}
    speech_vr = _try_read_json(speech_root / "verifier_report.json") or {}
    speech_sm = _try_read_json(speech_root / "summary.json") or {}
    display_vr = _try_read_json(display_root / "verifier_report.json") or {}
    display_sm = _try_read_json(display_root / "summary.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_planning_meta(), "output_root": str(out_root)}

    if ml_dr_vr.get("verifier") != "GO":
        blockers.append("Module-Local Model Profile Standardization DryRunAndReview must be GO")
    if ml_dr_sm.get("final_decision") != MODULE_LOCAL_DR_FINAL_GO:
        blockers.append("Module-Local DryRun final_decision mismatch")
    if not ml_dr_sm.get("module_internal_self_check_review_pass"):
        blockers.append("module_internal_self_check_review_pass must be true")
    if not ml_dr_sm.get("midplatform_interaction_check_review_pass"):
        blockers.append("midplatform_interaction_check_review_pass must be true")
    if registry_dr_vr.get("verifier") != "GO":
        blockers.append("Model Profile Registry DryRunAndReview must be GO")
    if registry_dr_sm.get("final_decision") != REGISTRY_DR_FINAL_GO:
        blockers.append("Registry DryRun final_decision mismatch")
    if cb_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 DryRunAndReview must be GO")
    if cb_sm.get("final_decision") != CONSTITUTION_BUS_DR_FINAL_GO:
        blockers.append("Constitution-Bus final_decision mismatch")
    if provider_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction Standard DryRunAndReview must be GO")
    if provider_sm.get("final_decision") != PROVIDER_ABS_DR_FINAL_GO:
        blockers.append("Provider Abstraction final_decision mismatch")
    if cr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime Framework DryRunAndReview must be GO")
    if cr_sm.get("final_decision") != CONTROLLED_RUNTIME_DR_FINAL_GO:
        blockers.append("Controlled Runtime final_decision mismatch")
    if ii_vr.get("verifier") != "GO":
        blockers.append("Information Integration Layer DryRunAndReview must be GO")
    if ii_sm.get("final_decision") != II_DR_FINAL_GO:
        blockers.append("Information Integration final_decision mismatch")
    for name, vr, sm, expected in (
        ("safety_gate", safety_vr, safety_sm, SAFETY_GATE_DR_FINAL_GO),
        ("speech_gate", speech_vr, speech_sm, SPEECH_GATE_DR_FINAL_GO),
        ("display_gate", display_vr, display_sm, DISPLAY_GATE_DR_FINAL_GO),
    ):
        if vr.get("verifier") != "GO":
            blockers.append(f"{name} DryRunAndReview must be GO")
        if sm.get("final_decision") != expected:
            blockers.append(f"{name} final_decision mismatch")

    input_ok = len(blockers) == 0

    module_local_input_review = {
        "review_id": "module_local_profile_input_review_v1",
        "module_local_dryrun_verifier": ml_dr_vr.get("verifier"),
        "module_local_dryrun_final_decision": ml_dr_sm.get("final_decision"),
        "module_local_planning_final_decision": ml_plan_sm.get("final_decision"),
        "module_internal_self_check_review_pass": ml_dr_sm.get("module_internal_self_check_review_pass"),
        "midplatform_interaction_check_review_pass": ml_dr_sm.get(
            "midplatform_interaction_check_review_pass"
        ),
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "registry_ref": REGISTRY_REF,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    governance_reuse = {
        "review_id": "governance_standard_reuse_review_v1",
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "reuse_rule_text": PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
        "reused_standards": list(REUSED_GOVERNANCE_STANDARDS),
        "new_governance_need_proven": False,
        "no_parallel_duplicate_governance_standard": True,
        "midplatform_binding_standardization_not_new_framework": True,
        **meta,
    }

    standard_definition = {
        "standard_id": STANDARD_ID,
        "standard_type": "midplatform_model_profile_governance_binding_standard",
        "scope": "Luna model profile governance binding",
        "registry_ref": REGISTRY_REF,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "binding_runtime_enabled_now": False,
        "model_selection_allowed_now": False,
        "model_invocation_allowed_now": False,
        "controlled_runtime_allowed_now": False,
        "candidate_only": True,
        "standard_duties": list(STANDARD_DUTIES),
        "standard_not": list(STANDARD_NOT),
        **meta,
    }

    binding_schema = {
        "schema_id": "midplatform_model_governance_binding_schema_v1",
        "standard_ref": STANDARD_ID,
        "required_fields": list(BINDING_SCHEMA_FIELDS),
        "field_count": len(BINDING_SCHEMA_FIELDS),
        "runtime_boundary_fields": {
            "model_selected_now": False,
            "model_invoked_now": False,
            "runtime_enabled_now": False,
        },
        **meta,
    }

    constitution_bus_binding = {
        "policy_id": "constitution_bus_binding_policy_v1",
        "constitution_bus_ref": CONSTITUTION_BUS_REF,
        "constitution_bus_version": "v1.0",
        "rules": [
            "every midplatform binding must reference Constitution-Bus v1.0",
            "raw constitution is not consumed directly by model/module runtime",
            "Resolver / constraint_bundle applies later",
            "applicable_rule_refs preserved",
            "module cannot create parallel governance",
            "module cannot self-authorize",
        ],
        **meta,
    }

    capability_bus_binding = {
        "policy_id": "capability_bus_binding_policy_v1",
        "capability_bus_ref": CAPABILITY_BUS_REF,
        "rules": [
            "module must declare capability bus contract",
            "module registration later requires profile + governance binding",
            "capability bus transports contracts / refs, not model judgement",
            "missing capability bus contract blocks future module admission",
            "capability bus does not invoke model",
        ],
        **meta,
    }

    provider_abstraction_binding = {
        "policy_id": "provider_abstraction_binding_policy_v1",
        "provider_abstraction_ref": PROVIDER_ABS_STANDARD_ID,
        "rules": [
            "provider-backed model must bind Provider Abstraction",
            "runtime ≠ provider",
            "provider_candidate ≠ selected ≠ invoked",
            "provider readiness later required",
            "no auto-switch without policy",
            "module/midplatform binding cannot invoke provider now",
        ],
        **meta,
    }

    validation_binding = {
        "policy_id": "validation_binding_policy_v1",
        "rules": [
            "validation_requirement_ref required",
            "validation tests later required before runtime/benchmark claims",
            "validation failure cannot be suppressed by module-local profile",
            "validation result must be traceable",
            "validation binding does not execute validation now",
        ],
        **meta,
    }

    health_oversight_binding = {
        "policy_id": "health_oversight_binding_policy_v1",
        "rules": [
            "health_requirement_ref required",
            "health_status_ref may be transported",
            "Health Oversight remains external to Constitution-Bus",
            "Bus transports health_ref ≠ Bus judges health",
            "module cannot self-certify health",
            "health binding does not generate health score now",
        ],
        **meta,
    }

    whitebox_trace_binding = {
        "policy_id": "whitebox_trace_binding_policy_v1",
        "rules": [
            "whitebox_trace_requirement_ref required",
            "source_chain / evidence / rationale refs preserved",
            "model output must be explainable at candidate level",
            "issue_trace required for uncertainty / failures",
            "whitebox binding does not execute model",
        ],
        **meta,
    }

    information_integration_binding = {
        "policy_id": "information_integration_binding_policy_v1",
        "information_integration_ref": INFORMATION_INTEGRATION_REF,
        "rules": [
            "observation/evidence/recognition/tracking/transcript/scene/risk outputs flow to "
            "Information Integration if context-relevant",
            "Information Integration consumes candidate/context/signal only",
            "model output cannot bypass Information Integration to Decision Center unless "
            "explicit policy later",
            "Information Integration does not invoke provider",
        ],
        **meta,
    }

    decision_center_binding = {
        "policy_id": "decision_center_binding_policy_v1",
        "decision_center_ref": DECISION_CENTER_REF,
        "rules": [
            "decision-relevant model outputs are consumed by Decision Center only through "
            "integrated_context / decision_request_candidate",
            "model cannot emit decision directly",
            "module cannot perform final decision",
            "Decision Center remains裁决层",
            "no decision executed now",
        ],
        **meta,
    }

    gate_chain_binding = {
        "policy_id": "gate_chain_binding_policy_v1",
        "gate_chain_system_ref": GATE_CHAIN_SYSTEM_ID,
        "rules": [
            "output-capable modules bind User Output Constitution / Safety / Speech / Display / "
            "Notification gates as applicable",
            "user_output_candidate ≠ user-facing output",
            "gate result candidate ≠ execution",
            "Speech/TTS/Display runtime remains later",
            "Privacy / Identity gates required for sensitive/person-recognition scenarios later",
        ],
        "gate_refs": {
            "safety_gate": "midplatform_safety_gate_v1",
            "speech_gate": "midplatform_speech_gate_v1",
            "display_gate": "midplatform_display_gate_v1",
        },
        **meta,
    }

    controlled_runtime_binding = {
        "policy_id": "controlled_runtime_binding_policy_v1",
        "controlled_runtime_framework_ref": CONTROLLED_RUNTIME_FRAMEWORK_REF,
        "rules": [
            "runtime-capable models must bind Controlled Runtime",
            "runtime requires admission / authorization / execution window / evidence / rollback / "
            "post-review later",
            "binding does not enable runtime now",
            "controlled runtime readiness remains future phase",
        ],
        **meta,
    }

    memory_worldmodel_admission_binding = {
        "policy_id": "memory_worldmodel_admission_binding_policy_v1",
        "rules": [
            "memory-capable modules require Memory Admission Gate later",
            "worldmodel-capable modules require WorldModel Admission Gate later",
            "model output cannot write Memory/WorldModel directly",
            "candidate/evidence must pass admission",
            "Personal Continuity protections apply where relevant",
        ],
        **meta,
    }

    by_layer = {
        "matrix_id": "model_governance_binding_by_capability_layer_v1",
        "capability_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layered_governance_mapping_ref": ADDENDUM_ID,
        "layers": list(LAYER_BINDING_SPECS),
        "layer_count": len(LAYER_BINDING_SPECS),
        **meta,
    }

    by_domain = {
        "matrix_id": "model_governance_binding_by_module_domain_v1",
        "domains": [
            {"domain": d, "binding_template_ref": f"{d.lower().replace('/', '_').replace(' ', '_')}_governance_binding_template"}
            for d in DOMAIN_COVERAGE
        ],
        "domain_count": len(DOMAIN_COVERAGE),
        "templates_provided": [
            "vision", "ocr", "tts", "asr", "map_navigation", "world_continuity",
            "memory_emotion_evolution",
        ],
        "provider_model_management_note": (
            "Provider/Model Management domain covered via Provider Abstraction binding; "
            "module template in later phase"
        ),
        **meta,
    }

    vision_binding = _binding_template(
        "vision_model_governance_binding_template_v1",
        "vision_scene_understanding_module",
        "first_person_vision_scene_understanding",
        [
            "yolo_family_object_detection_candidate",
            "grounded_sam_style_grounding_segmentation_candidate",
            "visual_tracking_candidate",
            "vlm_scene_understanding_candidate",
        ],
        ["Current Scene Understanding", "Spatiotemporal Continuity later"],
        [
            "binds Vision module-local profile",
            "binds YOLO/Grounding/Tracking/VLM registry refs as candidates",
            "outputs route through Information Integration",
            "no direct fact/action",
            "no camera/runtime",
            "provider abstraction if provider-backed",
            "controlled runtime later",
        ],
    )

    ocr_binding = _binding_template(
        "ocr_model_governance_binding_template_v1",
        "ocr_text_reading_module",
        "ocr_text_recognition_reading",
        ["rapidocr_candidate", "paddleocr_candidate", "other_ocr_provider_placeholder"],
        ["text region detection", "OCR reading candidate"],
        [
            "binds OCR module-local profile",
            "OCR outputs candidate/evidence only",
            "signage/text meaning goes to Information Integration",
            "no fact/write/action",
            "Memory/WorldModel admission later if reading/storage",
            "provider abstraction if provider-backed",
            "OCR runtime later",
        ],
    )

    tts_binding = _binding_template(
        "tts_model_governance_binding_template_v1",
        "tts_voice_output_module",
        "tts_voice_output",
        ["qianwen_tts_candidate", "moss_tts_style_candidate", "local_tts_placeholder"],
        ["Voice Output / TTS ExecutionRuntime later"],
        [
            "binds TTS module-local profile",
            "output-capable binding requires Speech Gate / Voice Output Plane later",
            "qianwen candidate ≠ selected/invoked",
            "TTS runtime ≠ provider",
            "no audio output now",
        ],
        stack_layer="layer_6_runtime_later",
    )

    asr_binding = _binding_template(
        "asr_model_governance_binding_template_v1",
        "asr_voice_input_module",
        "asr_voice_input",
        ["sensevoice_asr_candidate", "whisper_like_asr_candidate", "qwen_asr_style_candidate"],
        ["audio capture candidate", "ASR transcript candidate"],
        [
            "binds ASR module-local profile",
            "transcript outputs candidate only",
            "task intent goes to Information Integration / Decision",
            "no ASR runtime now",
            "speaker/identity later requires Privacy/Identity gates",
        ],
    )

    map_binding = _binding_template(
        "map_navigation_model_governance_binding_template_v1",
        "map_navigation_application_module",
        "map_location_navigation_application",
        [
            "map_provider_placeholder",
            "route_reasoning_candidate",
            "indoor_facility_search_candidate",
            "transit_context_candidate",
        ],
        ["Stage 3 Navigation Application Layer"],
        [
            "binds Map/Navigation module-local profile",
            "navigation is Layer 3",
            "route/navigation context goes through Information Integration / Decision",
            "Navigation Action Gate later",
            "no map provider invocation",
            "no navigation action",
        ],
        stack_layer="layer_3_navigation",
    )

    world_binding = _binding_template(
        "world_continuity_model_governance_binding_template_v1",
        "world_continuity_understanding_module",
        "spatiotemporal_world_continuity",
        [
            "scene_delta_candidate",
            "temporal_tracking_candidate",
            "visual_map_alignment_candidate",
            "stcm_self_developed_profile",
        ],
        ["Stage 2 Spatiotemporal Continuity / World Continuity"],
        [
            "binds World Continuity module-local profile",
            "external models provide signals only",
            "Luna owns continuity governance",
            "world_continuity_candidate not WorldModel fact",
            "WorldModel Admission Gate later",
        ],
        stack_layer="layer_2_spatiotemporal",
    )

    mem_emo_evo_binding = {
        "template_id": "memory_emotion_evolution_model_governance_binding_template_v1",
        "modules": [
            {"module_id": "memory_personal_continuity_module", "capability_domain": "memory_personal_continuity"},
            {"module_id": "emotion_engine_module", "capability_domain": "emotion_engine_social_adaptation"},
            {"module_id": "evolutionary_recursion_module", "capability_domain": "evolutionary_recursion_self_improvement"},
        ],
        "registry_ref": REGISTRY_REF,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "midplatform_governance_binding_standard_ref": STANDARD_ID,
        "registry_model_profile_refs": [
            "embedding_retrieval_candidate",
            "emotion_signal_model_candidate",
            "relationship_context_model_candidate",
            "market_feedback_analysis_candidate",
            "code_analysis_assistant_candidate",
        ],
        "confirmations": [
            "Memory modules bind Memory Admission / Personal Continuity protections",
            "Emotion Engine binds Survival Drive / social adaptation governance",
            "Evolutionary Recursion proposal_only",
            "external analysis models cannot self-modify Luna",
            "no memory write",
            "no code modification",
            "no skill addition",
        ],
        "governance_bindings": [
            {
                "midplatform_governance_binding_id": "memory_personal_continuity_module__embedding_retrieval_candidate__governance_binding",
                "module_local_profile_ref": "memory_personal_continuity_module__embedding_retrieval_candidate",
                "registry_model_profile_ref": "embedding_retrieval_candidate",
                "module_id": "memory_personal_continuity_module",
                "capability_domain": "memory_personal_continuity",
                "memory_admission_requirement_ref": "memory_admission_gate_later",
                "personal_continuity_protection": True,
                "model_selected_now": False,
                "model_invoked_now": False,
                "runtime_enabled_now": False,
            },
            {
                "midplatform_governance_binding_id": "evolutionary_recursion_module__code_analysis_assistant_candidate__governance_binding",
                "module_local_profile_ref": "evolutionary_recursion_module__code_analysis_assistant_candidate",
                "registry_model_profile_ref": "code_analysis_assistant_candidate",
                "module_id": "evolutionary_recursion_module",
                "capability_domain": "evolutionary_recursion_self_improvement",
                "proposal_only": True,
                "no_code_modification": True,
                "no_skill_addition": True,
                "model_selected_now": False,
                "model_invoked_now": False,
                "runtime_enabled_now": False,
            },
        ],
        **meta,
    }

    dual_validation_handoff = {
        "policy_id": "dual_validation_to_midplatform_binding_handoff_policy_v1",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "rules": [
            "Module Internal Self-Check output can feed midplatform binding review later",
            "Midplatform Interaction Check output can feed binding review later",
            "both are evidence gates, not runtime gates",
            "binding standard consumes their review refs",
            "Self-Check GO ≠ Interaction Check GO",
            "Interaction Check GO ≠ Runtime Ready",
        ],
        "dual_validation_non_claims": list(DUAL_VALIDATION_NON_CLAIMS),
        **meta,
    }

    non_compliance_deferment = {
        "review_id": "non_compliance_handling_deferment_review_v1",
        "non_compliant_module_model_handling_policy_deferred": True,
        "policy_ref_later": DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
        "recommended_future_phase": DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
        "not_implemented_now": True,
        "not_enforced_now": True,
        "deferral_claim": NON_COMPLIANCE_HANDLING_DEFERRAL_CLAIM,
        "defer_until": [
            "Module-local Model Profile Standardization DryRunAndReview completed",
            "Midplatform Model Governance Binding Standardization completed later",
            "at least one module-level self-check + interaction-check dryrun later",
        ],
        "current_phase_may_reference_policy_ref_later_only": True,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "midplatform_model_governance_binding_non_runtime_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "midplatform_model_governance_binding_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "objectives": [
            "generate midplatform_model_governance_binding_standard_candidate",
            "verify binding schema",
            "verify Constitution-Bus / Capability Bus / Provider Abstraction / Validation / Health / "
            "Whitebox / Information Integration / Decision Center / Gate Chain / Controlled Runtime / "
            "Memory-WorldModel Admission binding policies",
            "verify by-layer and by-domain binding",
            "verify Vision/OCR/TTS/ASR/Map/World/Memory-Emotion-Evolution templates",
            "verify non-compliance handling deferred",
            "no model select/download/invoke/benchmark",
            "no runtime enable",
        ],
        **meta,
    }

    planning_pass = input_ok
    planning_decision = {
        "decision_id": "midplatform_model_governance_binding_standardization_planning_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "midplatform_model_governance_binding_standardization_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "midplatform_model_governance_binding_standardization_planning_only": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        "dual_validation_non_claims": list(DUAL_VALIDATION_NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "standard_id": STANDARD_ID,
        "registry_ref": REGISTRY_REF,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "template_count": 7,
        "domain_coverage_count": len(DOMAIN_COVERAGE),
        "layer_binding_count": len(LAYER_BINDING_SPECS),
        "binding_policy_count": 11,
        "non_compliant_module_model_handling_policy_deferred": True,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    for tpl in (
        vision_binding, ocr_binding, tts_binding, asr_binding,
        map_binding, world_binding, mem_emo_evo_binding,
    ):
        tpl.update(meta)

    return {
        "midplatform_model_governance_binding_standardization_planning_policy": policy,
        "module_local_profile_input_review": module_local_input_review,
        "governance_standard_reuse_review": governance_reuse,
        "midplatform_model_governance_binding_standard_definition": standard_definition,
        "midplatform_model_governance_binding_schema": binding_schema,
        "constitution_bus_binding_policy": constitution_bus_binding,
        "capability_bus_binding_policy": capability_bus_binding,
        "provider_abstraction_binding_policy": provider_abstraction_binding,
        "validation_binding_policy": validation_binding,
        "health_oversight_binding_policy": health_oversight_binding,
        "whitebox_trace_binding_policy": whitebox_trace_binding,
        "information_integration_binding_policy": information_integration_binding,
        "decision_center_binding_policy": decision_center_binding,
        "gate_chain_binding_policy": gate_chain_binding,
        "controlled_runtime_binding_policy": controlled_runtime_binding,
        "memory_worldmodel_admission_binding_policy": memory_worldmodel_admission_binding,
        "model_governance_binding_by_capability_layer": by_layer,
        "model_governance_binding_by_module_domain": by_domain,
        "vision_model_governance_binding_template": vision_binding,
        "ocr_model_governance_binding_template": ocr_binding,
        "tts_model_governance_binding_template": tts_binding,
        "asr_model_governance_binding_template": asr_binding,
        "map_navigation_model_governance_binding_template": map_binding,
        "world_continuity_model_governance_binding_template": world_binding,
        "memory_emotion_evolution_model_governance_binding_template": mem_emo_evo_binding,
        "dual_validation_to_midplatform_binding_handoff_policy": dual_validation_handoff,
        "non_compliance_handling_deferment_review": non_compliance_deferment,
        "midplatform_model_governance_binding_non_runtime_boundary_matrix": boundary_matrix,
        "midplatform_model_governance_binding_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "midplatform_model_governance_binding_standardization_planning_decision": planning_decision,
        "summary": summary,
    }
