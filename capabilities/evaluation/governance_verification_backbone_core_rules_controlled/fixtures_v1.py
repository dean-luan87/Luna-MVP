"""Synthetic fixtures for governance rule, authority, and decision checks."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Dict, Tuple

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    ARCHITECTURE_SOURCE_REF,
    AUTHORITY_RESPONSIBILITY_UNITY,
    COMMON_GOVERNANCE_PROFILES,
    CONSTITUTION_SOURCE_REF,
    CORE_GOVERNANCE_RULE_REGISTRY_V1,
    GovernanceAuthorityResponsibilityRecordV1,
    GovernanceRuleRegistryV1,
    PhaseGovernanceProfileV1,
    PROTOCOL_SOURCE_REF,
)


PHASE = "Phase-Luna-Governance-Verification-Backbone-Core-Rules-Controlled-Implementation-v1-001"
PHASE_OWNER = "Protocol Manager"
DOMAIN = "CONTROLLED_PHASE"
TRACE = "trace:governance-backbone:v1"


def valid_profile() -> PhaseGovernanceProfileV1:
    return PhaseGovernanceProfileV1(
        phase_ref=PHASE,
        phase_owner_ref=PHASE_OWNER,
        domains=(DOMAIN,),
        owners_touched=(
            "Protocol Manager",
            "Cognitive Requirement",
            "Observation Demand",
            "Capability Governance",
            "Provider Governance",
            "Runtime",
            "Observation Gateway",
        ),
        governance_profiles=COMMON_GOVERNANCE_PROFILES,
        maturity_level="CONTROLLED_V1",
        runtime_level="NONE",
        candidate_only=True,
        read_only=True,
        truth_authority=False,
        world_truth_authority=False,
        runtime_authority=False,
        authority_refs=("authority:governance-scope", "authority:requirement-semantics"),
        responsibility_refs=(
            "responsibility:governance-scope-resolution",
            "responsibility:requirement-completeness",
        ),
        input_contract_refs=("ControlledPhaseInputV1",),
        output_contract_refs=("ControlledPhaseVerificationResultV1",),
        protocol_refs=(PROTOCOL_SOURCE_REF,),
        constitution_refs=(CONSTITUTION_SOURCE_REF,),
        context_refs=("context:controlled:governance-backbone",),
        trace_ref=TRACE,
    )


def valid_authority_records() -> Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]:
    return (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="protocol-manager:governance-backbone",
            owner_ref="Protocol Manager",
            authority_refs=("authority:governance-scope",),
            responsibility_refs=("responsibility:governance-scope-resolution",),
            decision_types=("governance_scope_resolution",),
            failure_types=("governance_scope_failure",),
            authority_responsibility_map=(
                ("authority:governance-scope", "responsibility:governance-scope-resolution"),
            ),
            responsibility_owner_refs=(
                ("responsibility:governance-scope-resolution", "Protocol Manager"),
            ),
            operational_authority=True,
            admission_authority=True,
        ),
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="cognitive:requirement",
            owner_ref="Cognitive Requirement",
            authority_refs=("authority:requirement-semantics",),
            responsibility_refs=("responsibility:requirement-completeness",),
            decision_types=("requirement_formation",),
            failure_types=("requirement_incomplete",),
            authority_responsibility_map=(
                ("authority:requirement-semantics", "responsibility:requirement-completeness"),
            ),
            responsibility_owner_refs=(
                ("responsibility:requirement-completeness", "Cognitive Requirement"),
            ),
            semantic_authority=True,
        ),
    )


def provider_binding_preparation_reference() -> Dict[str, Any]:
    return {
        "module_ref": "provider-binding-runtime-preparation",
        "owner_ref": "Provider Governance",
        "candidate_only": True,
        "read_only": True,
        "provider_bound": False,
        "runtime_allocated": False,
        "execution_instance_created": False,
        "provider_session_started": False,
        "gateway_submission": False,
        "runtime_started": False,
        "resource_allocated": False,
        "truth_declared": False,
        "world_truth_declared": False,
        "provider_binding_authority_declared": False,
        "source_refs": (
            "provider-target:controlled:reference",
            "compatibility:controlled:reference",
        ),
        "lineage_refs": (
            "problem:controlled:reference",
            "demand:controlled:reference",
            "provider-target:controlled:reference",
        ),
    }


def _case(case_id: str, category: str, payload: Any, expected: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "category": category,
        "payload": payload,
        "expected": expected,
    }


def build_governance_backbone_cases_v1() -> Tuple[Dict[str, Any], ...]:
    registry = CORE_GOVERNANCE_RULE_REGISTRY_V1
    profile = valid_profile()
    records = valid_authority_records()
    valid_artifact = provider_binding_preparation_reference()
    return (
        _case("GOVERNED_PHASE_VALID", "preflight", (profile, registry, records, (PROTOCOL_SOURCE_REF,)), {"status": "PASS"}),
        _case("NO_APPLICABLE_RULES_FAIL_CLOSED", "preflight", (replace(profile, domains=("UNRELATED_DOMAIN",), governance_profiles=("UNRELATED_PROFILE",)), registry, records, (PROTOCOL_SOURCE_REF,)), {"status": "GOVERNANCE_PREFLIGHT_BLOCKED"}),
        _case("UNKNOWN_RULE_OWNER", "preflight", (profile, replace(registry, rules=(replace(registry.rules[0], rule_owner_ref=""), *registry.rules[1:])), records, (PROTOCOL_SOURCE_REF,)), {"status": "GOVERNANCE_PREFLIGHT_BLOCKED", "error": "unknown_rule_owner"}),
        _case("UNKNOWN_RULE_SOURCE", "preflight", (profile, replace(registry, rules=(replace(registry.rules[0], rule_source_ref="docs/unknown.md"), *registry.rules[1:])), records, (PROTOCOL_SOURCE_REF,)), {"status": "GOVERNANCE_PREFLIGHT_BLOCKED", "error": "unknown_rule_source"}),
        _case("ORPHAN_GOVERNANCE_RULE", "preflight", (profile, replace(registry, rules=(replace(registry.rules[0], constitution_ref="", protocol_ref="", architecture_ref=""), *registry.rules[1:])), records, (PROTOCOL_SOURCE_REF,)), {"status": "GOVERNANCE_PREFLIGHT_BLOCKED", "error": "orphan_governance_rule"}),
        _case("INVALID_GOVERNANCE_PROFILE", "preflight", (replace(profile, phase_ref=""), registry, records, (PROTOCOL_SOURCE_REF,)), {"status": "GOVERNANCE_PREFLIGHT_BLOCKED", "error": "phase_ref_missing"}),
        _case("RULE_VERSION_MISSING", "preflight", (profile, replace(registry, rules=(replace(registry.rules[0], rule_version=""), *registry.rules[1:])), records, (PROTOCOL_SOURCE_REF,)), {"status": "GOVERNANCE_PREFLIGHT_BLOCKED", "error": "rule_version_missing"}),
        _case("AUTHORITY_WITH_RESPONSIBILITY", "authority", records, {"errors": ()}),
        _case("AUTHORITY_WITHOUT_RESPONSIBILITY", "authority", (replace(records[0], responsibility_refs=(), authority_responsibility_map=(), responsibility_owner_refs=()),), {"error": "AUTHORITY_WITHOUT_RESPONSIBILITY"}),
        _case("RESPONSIBILITY_WITHOUT_AUTHORITY", "authority", (replace(records[0], authority_refs=(), responsibility_refs=("responsibility:orphan",), authority_responsibility_map=(), responsibility_owner_refs=(("responsibility:orphan", "Protocol Manager"),)),), {"error": "RESPONSIBILITY_WITHOUT_AUTHORITY"}),
        _case("AUTHORITY_OWNER_MISSING", "authority", (replace(records[0], owner_ref=""),), {"error": "AUTHORITY_OWNER_MISSING"}),
        _case("AUTHORITY_COLLISION", "authority", (records[0], replace(records[0], module_ref="duplicate-owner", owner_ref="Other Owner")), {"error": "AUTHORITY_COLLISION"}),
        _case("RESPONSIBILITY_OWNER_MISMATCH", "authority", (replace(records[0], responsibility_owner_refs=(("responsibility:governance-scope-resolution", "Other Owner"),)),), {"error": "RESPONSIBILITY_OWNER_MISMATCH"}),
        _case("CANDIDATE_ONLY_VALID", "postflight", (profile, valid_artifact), {"status": "PASS"}),
        _case("CANDIDATE_ATTEMPTS_AUTHORITY", "postflight", (profile, {**valid_artifact, "authoritative_effects": ("provider_binding_decision",)}), {"status": "GOVERNANCE_POSTFLIGHT_BLOCKED"}),
        _case("NO_RUNTIME_VALID", "postflight", (profile, valid_artifact), {"status": "PASS"}),
        _case("NO_RUNTIME_BUT_EXECUTION_CREATED", "postflight", (profile, {**valid_artifact, "execution_instance_created": True}), {"status": "GOVERNANCE_POSTFLIGHT_BLOCKED"}),
        _case("NO_TRUTH_VALID", "postflight", (profile, valid_artifact), {"status": "PASS"}),
        _case("NO_TRUTH_BUT_TRUTH_DECLARED", "postflight", (profile, {**valid_artifact, "truth_declared": True}), {"status": "GOVERNANCE_POSTFLIGHT_BLOCKED"}),
        _case("REQUESTER_OWNS_REQUIREMENT_COMPLEXITY", "boundary", {"authority_ref": "authority:requirement-semantics", "responsibility_ref": "responsibility:requirement-completeness"}, {"errors": ()}),
        _case("DOWNSTREAM_INVENTS_REQUIREMENT", "boundary", {"downstream_invents_requirement": True}, {"error": "downstream_invents_requirement"}),
        _case("EXECUTOR_OWNS_EXECUTION_COMPLEXITY", "boundary", {"authority_ref": "authority:execution-complexity", "responsibility_ref": "responsibility:execution-complexity"}, {"errors": ()}),
        _case("REQUESTER_ASSIGNED_RESOURCE_FAILURE", "boundary", {"requester_assigned_resource_failure": True}, {"error": "requester_assigned_resource_failure"}),
        _case("GATEWAY_INGRESS_ADMISSION_NOT_PRE_EXECUTION_AUTHORITY", "gateway", {"gateway_authority": "RUNTIME_OBSERVATION_INGRESS_ADMISSION", "pre_execution_authorization": False}, {"errors": ()}),
        _case("ADAPTER_PRESERVES_LINEAGE", "adapter", {"source_refs": ("source:a",), "output_refs": ("output:a",), "lineage_preserved": True, "semantic_authority": False}, {"errors": ()}),
        _case("ADAPTER_ACQUIRES_SEMANTIC_AUTHORITY", "adapter", {"source_refs": ("source:a",), "output_refs": ("output:a",), "lineage_preserved": True, "semantic_authority": True}, {"error": "ADAPTER_HAS_SEMANTIC_AUTHORITY"}),
        _case("ALL_GOVERNANCE_AND_FUNCTIONAL_PASS_GO", "decision", {"functional_checks_passed": True, "contract_failures": (), "governance_preflight": "PASS", "governance_postflight": "PASS", "cognitive_logic_result": "PASS", "operational_result": "PASS"}, {"final_decision": "GO"}),
        _case("GOVERNANCE_FAIL_FORCES_NO_GO", "decision", {"functional_checks_passed": True, "contract_failures": (), "governance_preflight": "GOVERNANCE_PREFLIGHT_BLOCKED", "governance_postflight": "PASS", "cognitive_logic_result": "PASS", "operational_result": "PASS"}, {"final_decision": "NO_GO"}),
        _case("FUNCTIONAL_FAIL_FORCES_NO_GO", "decision", {"functional_checks_passed": False, "contract_failures": (), "governance_preflight": "PASS", "governance_postflight": "PASS", "cognitive_logic_result": "PASS", "operational_result": "PASS"}, {"final_decision": "NO_GO"}),
        _case("CONTRACT_FAILURE_FORCES_NO_GO", "decision", {"functional_checks_passed": True, "contract_failures": ("contract:error",), "governance_preflight": "PASS", "governance_postflight": "PASS", "cognitive_logic_result": "PASS", "operational_result": "PASS"}, {"final_decision": "NO_GO"}),
        _case("WAITING_STATUS_NOT_USED_AS_FINAL_DECISION", "decision", {"runner_status": "WAITING_FOR_USER_TERMINAL_VERIFICATION", "functional_checks_passed": True, "contract_failures": (), "governance_preflight": "PASS", "governance_postflight": "PASS", "cognitive_logic_result": "PASS", "operational_result": "PASS"}, {"final_decision": "GO"}),
        _case("DETERMINISTIC_RULE_RESOLUTION", "determinism", (profile, registry), {"deterministic": True}),
        _case("DETERMINISTIC_FINAL_DECISION", "determinism", {"functional_checks_passed": True, "contract_failures": (), "governance_preflight": "PASS", "governance_postflight": "PASS", "cognitive_logic_result": "PASS", "operational_result": "PASS"}, {"deterministic": True}),
        _case("MALFORMED_PROFILE_FAIL_CLOSED", "preflight", ({}, registry, records, (PROTOCOL_SOURCE_REF,)), {"status": "GOVERNANCE_PREFLIGHT_BLOCKED", "error": "profile_type_invalid"}),
        _case("MALFORMED_RULE_FAIL_CLOSED", "preflight", (profile, replace(registry, rules=("malformed-rule",)), records, (PROTOCOL_SOURCE_REF,)), {"status": "GOVERNANCE_PREFLIGHT_BLOCKED", "error": "rule_type_invalid"}),
    )


__all__ = [
    "PHASE",
    "CONSTITUTION_SOURCE_REF",
    "PROTOCOL_SOURCE_REF",
    "ARCHITECTURE_SOURCE_REF",
    "valid_profile",
    "valid_authority_records",
    "provider_binding_preparation_reference",
    "build_governance_backbone_cases_v1",
]
