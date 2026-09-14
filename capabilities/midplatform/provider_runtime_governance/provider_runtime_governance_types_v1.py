# -*- coding: utf-8 -*-
"""Shared Provider Runtime Governance Skeleton — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Shared-Provider-Runtime-Governance-Skeleton-v1-001"
SCOPE = "shared_provider_runtime_governance_skeleton_planning_only"
SOURCE_CHAIN = "provider_runtime_governance_v1"

GOVERNANCE_PRINCIPLE_EN = (
    "Shared Provider Runtime Governance defines runtime governance shape across domains, "
    "not runtime activation."
)
GOVERNANCE_PRINCIPLE_ZH = (
    "共享 Provider Runtime Governance 定义跨域运行时治理形态，不代表运行时已启用。"
)

INHERITED_ADMISSION_PRINCIPLE_ZH = "能翻译，不等于能启用。"
INHERITED_MANAGER_PRINCIPLE_ZH = "能准入规划，不等于能 runtime enable。"

MIDPLATFORM_SYNTHESIS_ENTRYPOINT = "midplatform_synthesis_v1"
FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
SHARED_MANAGER_REF = "shared_provider_runtime_governance_manager_v1"

FINAL_DECISION_READY_FOR_DOMAIN_PROFILES = (
    "SHARED_PROVIDER_RUNTIME_GOVERNANCE_SKELETON_READY_FOR_DOMAIN_PROFILES"
)
FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER = (
    "SHARED_PROVIDER_RUNTIME_GOVERNANCE_DRYRUN_CASES_READY_FOR_RUNNER"
)
FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER = (
    "SHARED_PROVIDER_RUNTIME_GOVERNANCE_DRYRUN_TRACE_READY_FOR_VERIFIER"
)
FINAL_DECISION_DRYRUN_RUNNER_UNEXPECTED_OUTCOME = (
    "SHARED_PROVIDER_RUNTIME_GOVERNANCE_DRYRUN_RUNNER_UNEXPECTED_OUTCOME"
)
FINAL_DECISION_DRYRUN_VERIFIER_GO = (
    "SHARED_PROVIDER_RUNTIME_GOVERNANCE_DRYRUN_VERIFIER_GO"
)
FINAL_DECISION_DRYRUN_VERIFIER_BLOCKED = (
    "SHARED_PROVIDER_RUNTIME_GOVERNANCE_DRYRUN_VERIFIER_BLOCKED"
)
FINAL_DECISION_POST_DRYRUN_REVIEW_GO = (
    "SHARED_PROVIDER_RUNTIME_GOVERNANCE_POST_DRYRUN_REVIEW_GO"
)
FINAL_DECISION_POST_DRYRUN_REVIEW_BLOCKED = (
    "SHARED_PROVIDER_RUNTIME_GOVERNANCE_POST_DRYRUN_REVIEW_BLOCKED"
)

DOMAIN_SHARED = "shared"
DOMAIN_SPATIAL_EVIDENCE = "spatial_evidence"
DOMAIN_VISION = "vision"
DOMAIN_OCR = "ocr"
DOMAIN_VISION_OCR = "vision_ocr"
DOMAIN_ASR = "asr"

SUPPORTED_DOMAIN_IDS: Tuple[str, ...] = (
    DOMAIN_SHARED,
    DOMAIN_SPATIAL_EVIDENCE,
    DOMAIN_VISION,
    DOMAIN_OCR,
    DOMAIN_VISION_OCR,
    DOMAIN_ASR,
)

PROVIDER_RUNTIME_GOVERNANCE_MANAGER_FIELDS: Tuple[str, ...] = (
    "manager_ref",
    "domain_id",
    "manager_status",
    "managed_provider_refs",
    "default_enabled_provider_refs",
    "default_disabled_provider_refs",
    "synthesis_entrypoint",
    "runtime_activation_allowed",
    "provider_runtime_enabled",
    "candidate_only",
)

PROVIDER_REGISTRY_ENTRY_FIELDS: Tuple[str, ...] = (
    "registry_entry_ref",
    "domain_id",
    "provider_ref",
    "backend_ref",
    "adapter_ref",
    "provider_role",
    "registration_status",
    "admission_policy_ref",
    "health_gate_ref",
    "fallback_policy_ref",
    "enabled_by_default",
    "runtime_enable_allowed",
    "supported_output_candidate_types",
    "candidate_only",
)

PROVIDER_ENABLE_REQUEST_FIELDS: Tuple[str, ...] = (
    "enable_request_ref",
    "domain_id",
    "provider_ref",
    "requested_scope",
    "requested_by",
    "reason",
    "required_checks",
    "approval_required",
    "execution_allowed",
    "candidate_only",
)

PROVIDER_DISABLE_REQUEST_FIELDS: Tuple[str, ...] = (
    "disable_request_ref",
    "domain_id",
    "provider_ref",
    "disable_reason",
    "disable_scope",
    "fallback_required",
    "preserve_source_chain",
    "execution_allowed",
    "candidate_only",
)

PROVIDER_RUNTIME_STATE_FIELDS: Tuple[str, ...] = (
    "runtime_state_ref",
    "domain_id",
    "provider_ref",
    "runtime_status",
    "health_status",
    "fallback_status",
    "output_status",
    "last_health_signal_ref",
    "source_chain_preserved",
    "candidate_only",
)

PROVIDER_HEALTH_SNAPSHOT_FIELDS: Tuple[str, ...] = (
    "health_snapshot_ref",
    "domain_id",
    "provider_ref",
    "signal_name",
    "signal_value",
    "confidence",
    "source_freshness",
    "health_decision",
    "degradation_required",
    "disable_required",
    "candidate_only",
)

PROVIDER_FALLBACK_ROUTE_FIELDS: Tuple[str, ...] = (
    "fallback_route_ref",
    "domain_id",
    "provider_ref",
    "fallback_provider_refs",
    "fallback_mode",
    "trigger_conditions",
    "preserve_source_chain",
    "preserve_conflict_refs",
    "candidate_only",
)

PROVIDER_RUNTIME_ADMISSION_CHECK_FIELDS: Tuple[str, ...] = (
    "admission_check_ref",
    "domain_id",
    "provider_ref",
    "admission_stage",
    "license_gate_passed",
    "adapter_contract_passed",
    "provider_admission_gate_passed",
    "health_gate_passed",
    "fallback_gate_passed",
    "synthesis_gate_passed",
    "static_validation_passed",
    "runtime_admission_allowed",
    "blocked_reasons",
    "candidate_only",
)

PROVIDER_MANAGER_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "manager_ref",
    "domain_id",
    "registered_provider_refs",
    "runtime_enabled_provider_refs",
    "default_disabled_provider_refs",
    "enable_request_refs",
    "disable_request_refs",
    "fallback_route_refs",
    "runtime_activation_allowed",
    "provider_runtime_enabled",
    "final_decision",
    "candidate_only",
)

PROVIDER_DOMAIN_GOVERNANCE_PROFILE_FIELDS: Tuple[str, ...] = (
    "profile_ref",
    "domain_id",
    "domain_name",
    "admission_layer_ref",
    "synthesis_entrypoint",
    "provider_refs",
    "supported_output_candidate_types",
    "domain_risk_tags",
    "uses_shared_manager_skeleton",
    "candidate_only",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "architecture_definition_only": True,
    "no_runtime_activation": True,
    "no_provider_runtime_enabled": True,
    "no_real_provider_runtime": True,
    "no_provider_manager_runtime": True,
    "no_domain_specific_manager_duplication": True,
    "no_speech_output": True,
    "no_navigation_output": True,
    "no_fact_layer_write": True,
}


@dataclass(frozen=True)
class ProviderRuntimeGovernanceManager:
    manager_ref: str
    domain_id: str
    manager_status: str
    managed_provider_refs: Tuple[str, ...]
    default_enabled_provider_refs: Tuple[str, ...]
    default_disabled_provider_refs: Tuple[str, ...]
    synthesis_entrypoint: str
    runtime_activation_allowed: bool
    provider_runtime_enabled: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderRegistryEntry:
    registry_entry_ref: str
    domain_id: str
    provider_ref: str
    backend_ref: str
    adapter_ref: str
    provider_role: str
    registration_status: str
    admission_policy_ref: str
    health_gate_ref: str
    fallback_policy_ref: str
    enabled_by_default: bool
    runtime_enable_allowed: bool
    supported_output_candidate_types: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderEnableRequest:
    enable_request_ref: str
    domain_id: str
    provider_ref: str
    requested_scope: str
    requested_by: str
    reason: str
    required_checks: Tuple[str, ...]
    approval_required: bool
    execution_allowed: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderDisableRequest:
    disable_request_ref: str
    domain_id: str
    provider_ref: str
    disable_reason: str
    disable_scope: str
    fallback_required: bool
    preserve_source_chain: bool
    execution_allowed: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderRuntimeState:
    runtime_state_ref: str
    domain_id: str
    provider_ref: str
    runtime_status: str
    health_status: str
    fallback_status: str
    output_status: str
    last_health_signal_ref: str
    source_chain_preserved: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderHealthSnapshot:
    health_snapshot_ref: str
    domain_id: str
    provider_ref: str
    signal_name: str
    signal_value: str
    confidence: float
    source_freshness: str
    health_decision: str
    degradation_required: bool
    disable_required: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderFallbackRoute:
    fallback_route_ref: str
    domain_id: str
    provider_ref: str
    fallback_provider_refs: Tuple[str, ...]
    fallback_mode: str
    trigger_conditions: Tuple[str, ...]
    preserve_source_chain: bool
    preserve_conflict_refs: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderRuntimeAdmissionCheck:
    admission_check_ref: str
    domain_id: str
    provider_ref: str
    admission_stage: str
    license_gate_passed: bool
    adapter_contract_passed: bool
    provider_admission_gate_passed: bool
    health_gate_passed: bool
    fallback_gate_passed: bool
    synthesis_gate_passed: bool
    static_validation_passed: bool
    runtime_admission_allowed: bool
    blocked_reasons: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderManagerDecision:
    decision_ref: str
    manager_ref: str
    domain_id: str
    registered_provider_refs: Tuple[str, ...]
    runtime_enabled_provider_refs: Tuple[str, ...]
    default_disabled_provider_refs: Tuple[str, ...]
    enable_request_refs: Tuple[str, ...]
    disable_request_refs: Tuple[str, ...]
    fallback_route_refs: Tuple[str, ...]
    runtime_activation_allowed: bool
    provider_runtime_enabled: bool
    final_decision: str
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderDomainGovernanceProfile:
    profile_ref: str
    domain_id: str
    domain_name: str
    admission_layer_ref: str
    synthesis_entrypoint: str
    provider_refs: Tuple[str, ...]
    supported_output_candidate_types: Tuple[str, ...]
    domain_risk_tags: Tuple[str, ...]
    uses_shared_manager_skeleton: bool
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
