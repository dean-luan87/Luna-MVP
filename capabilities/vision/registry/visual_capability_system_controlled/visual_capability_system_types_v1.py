"""Candidate-only types for the controlled Luna V1 Visual Capability System.

This module represents capability identity, lifecycle, registration, and
channel routing only. It never imports or invokes a provider/model runtime.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, Tuple

OWNER = "Capability Registry"
MODEL_ADMISSION_OWNER = "Model Manager / Model Governance"
OBSERVATION_OWNER = "FPO / Active Observation Control"
GATEWAY_OWNER = "Observation Gateway"

LIFECYCLE_STATES = (
    "MANDATORY", "AVAILABLE", "NOT_INSTALLED", "INSTALLING", "INSTALLED",
    "ACTIVE", "SUSPENDED", "DEGRADED", "INCOMPATIBLE", "RETIRED",
)
ROUTE_OUTCOMES = (
    "ROUTE_READY_CANDIDATE", "CAPABILITY_NOT_INSTALLED", "CAPABILITY_DEGRADED",
    "CAPABILITY_INCOMPATIBLE", "SAFETY_BASELINE_BLOCKED", "OBSERVATION_NEED_REQUIRED",
)
CAPABILITY_DOMAINS = (
    "SAFETY_ENVIRONMENT_AWARENESS",
    "SAFETY_MOTION_RISK_AWARENESS",
    "SAFETY_PASSABILITY_HAZARD_AWARENESS",
    "SAFETY_SIGN_AWARENESS",
    "VISUAL_SENSOR_HEALTH",
    "OPTIONAL_VISUAL_CAPABILITY",
)


@dataclass(frozen=True)
class SafetyCapabilitySlotV1:
    slot_id: str
    capability_category: str
    mandatory: bool
    minimum_semantic_set_ref: str
    minimum_supported_baseline: str
    approved_provider_refs: Tuple[str, ...]
    rollback_policy_ref: str
    degradation_policy_ref: str
    user_uninstall_allowed: bool = False
    user_disable_below_baseline_allowed: bool = False
    unapproved_provider_replacement_allowed: bool = False
    safety_baseline_required: bool = True
    degradation_monitoring_required: bool = True
    rollback_required: bool = True
    candidate_only: bool = True
    truth_authority: bool = False


@dataclass(frozen=True)
class VisualCapabilityManifestV1:
    capability_id: str
    capability_domain: str
    capability_version: str
    capability_kind: str
    mandatory_or_optional: str
    input_contract_refs: Tuple[str, ...]
    evidence_contract_refs: Tuple[str, ...]
    provider_contract_refs: Tuple[str, ...]
    model_asset_refs: Tuple[str, ...]
    resource_profile_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    compatibility_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    lifecycle_state: str
    trace_ref: str
    candidate_only: bool = True
    model_independent_identity: bool = True
    user_uninstall_allowed: bool = True
    user_disable_below_baseline_allowed: bool = True
    unapproved_provider_replacement_allowed: bool = True
    safety_baseline_required: bool = False
    degradation_monitoring_required: bool = False
    rollback_required: bool = False
    social_norm_semantic_pack_ref: Optional[str] = None
    semantic_resolution_request_ref: Optional[str] = None


@dataclass(frozen=True)
class CapabilityRegistrationCandidateV1:
    registration_id: str
    manifest: VisualCapabilityManifestV1
    registration_status: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityRegistrationOutcomeV1:
    registration_id: str
    accepted: bool
    reason: str
    lifecycle_state: str
    automatic_install: bool = False
    automatic_activation: bool = False
    provider_invocation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class SafetyRegistrationAssessmentV1:
    capability_id: str
    approved_provider: bool
    minimum_baseline_met: bool
    compatibility_verified: bool
    provenance_present: bool
    checksum_refs_present: bool
    rollback_available: bool
    degradation_policy_present: bool
    resource_ready: bool
    accepted: bool
    reason: str
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityLifecycleTransitionCandidateV1:
    capability_id: str
    requested_state: str
    accepted: bool
    actor: str
    reason: str
    user_controlled: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityRouteRequestCandidateV1:
    request_id: str
    channel: str
    capability_id: str
    ordinary_observation_need_present: bool
    observation_need_ref: Optional[str]
    semantic_resolution_request_ref: Optional[str]
    social_norm_semantic_pack_ref: Optional[str]
    trace_ref: str
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityRouteResultV1:
    request_id: str
    outcome: str
    selected_capability_ref: Optional[str]
    reason: str
    safety_priority: bool
    interrupt_candidate: bool
    escalation_candidate: bool
    observation_gateway_required: bool = True
    provider_invocation: bool = False
    model_inference: bool = False
    truth_declared: bool = False
    fact_admitted: bool = False
    field_mutation: bool = False
    current_world_mutation: bool = False
    candidate_only: bool = True


def to_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)
