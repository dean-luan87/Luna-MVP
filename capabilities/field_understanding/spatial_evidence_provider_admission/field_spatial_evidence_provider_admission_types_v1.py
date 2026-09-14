# -*- coding: utf-8 -*-
"""Field Spatial Evidence Provider Admission Planning — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Field-Spatial-Evidence-Provider-Admission-Planning-v1-001"
SCOPE = "spatial_evidence_provider_admission_planning_only"
SOURCE_CHAIN = "spatial_evidence_provider_admission_v1"

ADMISSION_PRINCIPLE_EN = (
    "Provider Admission is the runtime admission layer. Adapter Contract pass does not mean "
    "a provider may run. A provider must pass license gate, adapter gate, health gate, "
    "fallback gate, and field synthesis gate before runtime admission."
)
ADMISSION_PRINCIPLE_ZH = "能翻译，不等于能启用。"

FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
MOCK_FALLBACK_PROVIDER_REF = "mock_spatial_provider"

FINAL_DECISION_READY_FOR_DRYRUN_CASES = (
    "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_PLANNING_READY_FOR_DRYRUN_CASES"
)

SPATIAL_EVIDENCE_PROVIDER_ADMISSION_POLICY_FIELDS: Tuple[str, ...] = (
    "policy_ref",
    "provider_ref",
    "backend_ref",
    "adapter_ref",
    "provider_role",
    "admission_mode",
    "allowed_runtime_scope",
    "required_candidate_types",
    "optional_candidate_types",
    "required_gates",
    "disable_conditions",
    "fallback_policy_ref",
    "field_synthesis_entrypoint",
    "runtime_admission_allowed",
    "commercial_runtime_allowed",
    "candidate_only",
)

PROVIDER_CAPABILITY_PROFILE_FIELDS: Tuple[str, ...] = (
    "profile_ref",
    "provider_ref",
    "backend_ref",
    "supported_candidate_types",
    "required_input_modes",
    "supported_runtime_modes",
    "latency_class",
    "compute_class",
    "reliability_class",
    "wearable_fit",
    "offline_fit",
    "semantic_extension_fit",
    "health_signal_supported",
    "candidate_only",
)

PROVIDER_HEALTH_GATE_FIELDS: Tuple[str, ...] = (
    "health_gate_ref",
    "provider_ref",
    "required_health_signals",
    "degraded_conditions",
    "blocked_conditions",
    "drift_policy",
    "tracking_lost_policy",
    "confidence_floor",
    "degradation_output_policy",
    "candidate_only",
)

PROVIDER_FALLBACK_POLICY_FIELDS: Tuple[str, ...] = (
    "fallback_policy_ref",
    "provider_ref",
    "fallback_provider_refs",
    "fallback_mode",
    "fallback_trigger_conditions",
    "fallback_output_policy",
    "preserve_source_chain",
    "preserve_conflict_refs",
    "candidate_only",
)

PROVIDER_RUNTIME_ADMISSION_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "admission_ref",
    "provider_ref",
    "backend_ref",
    "adapter_ref",
    "admission_stage",
    "license_gate_passed",
    "adapter_contract_passed",
    "provider_policy_passed",
    "capability_profile_passed",
    "health_gate_passed",
    "fallback_policy_passed",
    "static_validation_passed",
    "runtime_admission_allowed",
    "admission_reasons",
    "blocked_reasons",
    "candidate_only",
)

PROVIDER_DISABLE_DECISION_FIELDS: Tuple[str, ...] = (
    "disable_ref",
    "provider_ref",
    "disable_reason",
    "disable_scope",
    "disable_duration_policy",
    "fallback_policy_ref",
    "evidence_refs",
    "requires_user_confirmation",
    "candidate_only",
)

PROVIDER_ADMISSION_PLANNING_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "planned_provider_refs",
    "runtime_admission_candidates",
    "commercial_runtime_candidates",
    "blocked_runtime_providers",
    "observation_only_providers",
    "fallback_required",
    "health_gate_required",
    "provider_replaceability_required",
    "final_decision",
    "candidate_only",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "architecture_definition_only": True,
    "no_runtime_admission": True,
    "no_real_provider_runtime": True,
    "no_real_slam_backend": True,
    "no_camera_runtime": True,
    "no_ros_runtime": True,
    "no_benchmark_runtime": True,
    "no_commercial_runtime_selection": True,
    "no_provider_manager_runtime": True,
    "no_speech_output": True,
    "no_navigation_output": True,
    "no_fact_layer_write": True,
}


@dataclass(frozen=True)
class SpatialEvidenceProviderAdmissionPolicy:
    policy_ref: str
    provider_ref: str
    backend_ref: str
    adapter_ref: str
    provider_role: str
    admission_mode: str
    allowed_runtime_scope: str
    required_candidate_types: Tuple[str, ...]
    optional_candidate_types: Tuple[str, ...]
    required_gates: Tuple[str, ...]
    disable_conditions: Tuple[str, ...]
    fallback_policy_ref: str
    field_synthesis_entrypoint: str
    runtime_admission_allowed: bool
    commercial_runtime_allowed: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderCapabilityProfile:
    profile_ref: str
    provider_ref: str
    backend_ref: str
    supported_candidate_types: Tuple[str, ...]
    required_input_modes: Tuple[str, ...]
    supported_runtime_modes: Tuple[str, ...]
    latency_class: str
    compute_class: str
    reliability_class: str
    wearable_fit: str
    offline_fit: str
    semantic_extension_fit: str
    health_signal_supported: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderHealthGate:
    health_gate_ref: str
    provider_ref: str
    required_health_signals: Tuple[str, ...]
    degraded_conditions: Tuple[str, ...]
    blocked_conditions: Tuple[str, ...]
    drift_policy: str
    tracking_lost_policy: str
    confidence_floor: float
    degradation_output_policy: str
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderFallbackPolicy:
    fallback_policy_ref: str
    provider_ref: str
    fallback_provider_refs: Tuple[str, ...]
    fallback_mode: str
    fallback_trigger_conditions: Tuple[str, ...]
    fallback_output_policy: str
    preserve_source_chain: bool
    preserve_conflict_refs: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderRuntimeAdmissionCandidate:
    admission_ref: str
    provider_ref: str
    backend_ref: str
    adapter_ref: str
    admission_stage: str
    license_gate_passed: bool
    adapter_contract_passed: bool
    provider_policy_passed: bool
    capability_profile_passed: bool
    health_gate_passed: bool
    fallback_policy_passed: bool
    static_validation_passed: bool
    runtime_admission_allowed: bool
    admission_reasons: Tuple[str, ...]
    blocked_reasons: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderDisableDecision:
    disable_ref: str
    provider_ref: str
    disable_reason: str
    disable_scope: str
    disable_duration_policy: str
    fallback_policy_ref: str
    evidence_refs: Tuple[str, ...]
    requires_user_confirmation: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderAdmissionPlanningDecision:
    decision_ref: str
    planned_provider_refs: Tuple[str, ...]
    runtime_admission_candidates: Tuple[str, ...]
    commercial_runtime_candidates: Tuple[str, ...]
    blocked_runtime_providers: Tuple[str, ...]
    observation_only_providers: Tuple[str, ...]
    fallback_required: bool
    health_gate_required: bool
    provider_replaceability_required: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
