"""Metadata-only governance for the controlled visual capability system."""
from __future__ import annotations

from dataclasses import replace
from typing import Iterable, Mapping

from .visual_capability_system_types_v1 import (
    CapabilityLifecycleTransitionCandidateV1,
    CapabilityRegistrationCandidateV1,
    CapabilityRegistrationOutcomeV1,
    CapabilityRouteRequestCandidateV1,
    CapabilityRouteResultV1,
    SafetyCapabilitySlotV1,
    SafetyRegistrationAssessmentV1,
    VisualCapabilityManifestV1,
)


def register_candidate(candidate: CapabilityRegistrationCandidateV1) -> CapabilityRegistrationOutcomeV1:
    manifest = candidate.manifest
    if manifest.candidate_only is not True:
        return CapabilityRegistrationOutcomeV1(candidate.registration_id, False, "REGISTRATION_MUST_BE_CANDIDATE_ONLY", manifest.lifecycle_state)
    if manifest.mandatory_or_optional == "MANDATORY" and not manifest.safety_baseline_required:
        return CapabilityRegistrationOutcomeV1(candidate.registration_id, False, "MANDATORY_CAPABILITY_REQUIRES_SAFETY_BASELINE", manifest.lifecycle_state)
    if manifest.mandatory_or_optional == "MANDATORY" and manifest.lifecycle_state not in {"MANDATORY", "AVAILABLE", "ACTIVE", "DEGRADED"}:
        return CapabilityRegistrationOutcomeV1(candidate.registration_id, False, "INVALID_MANDATORY_LIFECYCLE_STATE", manifest.lifecycle_state)
    return CapabilityRegistrationOutcomeV1(candidate.registration_id, True, "REGISTERED_CANDIDATE_ONLY", manifest.lifecycle_state)


def assess_safety_registration(
    manifest: VisualCapabilityManifestV1,
    *,
    approved_provider: bool,
    minimum_baseline_met: bool,
    compatibility_verified: bool,
    provenance_present: bool,
    checksum_refs_present: bool,
    rollback_available: bool,
    degradation_policy_present: bool,
    resource_ready: bool,
) -> SafetyRegistrationAssessmentV1:
    checks = (approved_provider, minimum_baseline_met, compatibility_verified, provenance_present,
              checksum_refs_present, rollback_available, degradation_policy_present, resource_ready)
    accepted = manifest.mandatory_or_optional == "MANDATORY" and all(checks)
    reason = "APPROVED_SAFETY_REPLACEMENT_CANDIDATE" if accepted else "SAFETY_REGISTRATION_REQUIREMENT_MISSING"
    return SafetyRegistrationAssessmentV1(
        capability_id=manifest.capability_id,
        approved_provider=approved_provider,
        minimum_baseline_met=minimum_baseline_met,
        compatibility_verified=compatibility_verified,
        provenance_present=provenance_present,
        checksum_refs_present=checksum_refs_present,
        rollback_available=rollback_available,
        degradation_policy_present=degradation_policy_present,
        resource_ready=resource_ready,
        accepted=accepted,
        reason=reason,
    )


def request_user_transition(
    manifest: VisualCapabilityManifestV1,
    requested_state: str,
) -> CapabilityLifecycleTransitionCandidateV1:
    forbidden = manifest.mandatory_or_optional == "MANDATORY" and requested_state in {"NOT_INSTALLED", "RETIRED", "DISABLE_BELOW_BASELINE"}
    accepted = requested_state in {"NOT_INSTALLED", "SUSPENDED", "RETIRED"} and not forbidden and manifest.mandatory_or_optional == "OPTIONAL"
    reason = "OPTIONAL_USER_LIFECYCLE_OPERATION_ACCEPTED" if accepted else ("MANDATORY_SAFETY_BASELINE_PROTECTED" if forbidden else "USER_TRANSITION_NOT_ALLOWED")
    return CapabilityLifecycleTransitionCandidateV1(manifest.capability_id, requested_state, accepted, "USER", reason, True)


def build_route_request(
    request_id: str,
    *,
    channel: str,
    capability_id: str,
    ordinary_observation_need_present: bool,
    observation_need_ref: str | None = None,
    semantic_resolution_request_ref: str | None = None,
    social_norm_semantic_pack_ref: str | None = None,
) -> CapabilityRouteRequestCandidateV1:
    return CapabilityRouteRequestCandidateV1(
        request_id=request_id,
        channel=channel,
        capability_id=capability_id,
        ordinary_observation_need_present=ordinary_observation_need_present,
        observation_need_ref=observation_need_ref,
        semantic_resolution_request_ref=semantic_resolution_request_ref,
        social_norm_semantic_pack_ref=social_norm_semantic_pack_ref,
        trace_ref=f"trace:{request_id}",
    )


def route_candidate(
    request: CapabilityRouteRequestCandidateV1,
    manifests: Iterable[VisualCapabilityManifestV1],
) -> CapabilityRouteResultV1:
    manifest = next((item for item in manifests if item.capability_id == request.capability_id), None)
    safety = request.channel == "SAFETY_PERCEPTION"
    if not safety and not request.ordinary_observation_need_present:
        return CapabilityRouteResultV1(request.request_id, "OBSERVATION_NEED_REQUIRED", None, "TASK_OBSERVATION_REQUIRES_ORDINARY_OBSERVATION_NEED", False, False, False)
    if manifest is None:
        return CapabilityRouteResultV1(request.request_id, "SAFETY_BASELINE_BLOCKED" if safety else "CAPABILITY_NOT_INSTALLED", None, "CAPABILITY_REFERENCE_NOT_REGISTERED", safety, safety, safety)
    if safety and manifest.mandatory_or_optional != "MANDATORY":
        return CapabilityRouteResultV1(request.request_id, "SAFETY_BASELINE_BLOCKED", manifest.capability_id, "SAFETY_CHANNEL_REQUIRES_MANDATORY_CAPABILITY", True, True, True)
    if manifest.lifecycle_state == "INCOMPATIBLE":
        return CapabilityRouteResultV1(request.request_id, "CAPABILITY_INCOMPATIBLE", manifest.capability_id, "REGISTERED_CAPABILITY_INCOMPATIBLE", safety, safety, safety)
    if manifest.lifecycle_state == "DEGRADED":
        return CapabilityRouteResultV1(request.request_id, "CAPABILITY_DEGRADED", manifest.capability_id, "CAPABILITY_DEGRADED_REQUIRES_ESCALATION", safety, safety, True)
    if manifest.mandatory_or_optional == "OPTIONAL" and manifest.lifecycle_state in {"NOT_INSTALLED", "INSTALLING", "SUSPENDED", "RETIRED"}:
        return CapabilityRouteResultV1(request.request_id, "CAPABILITY_NOT_INSTALLED", manifest.capability_id, "OPTIONAL_CAPABILITY_UNAVAILABLE", safety, False, False)
    if manifest.mandatory_or_optional == "MANDATORY" and manifest.lifecycle_state not in {"MANDATORY", "AVAILABLE", "ACTIVE"}:
        return CapabilityRouteResultV1(request.request_id, "SAFETY_BASELINE_BLOCKED", manifest.capability_id, "MANDATORY_SAFETY_BASELINE_NOT_READY", True, True, True)
    return CapabilityRouteResultV1(request.request_id, "ROUTE_READY_CANDIDATE", manifest.capability_id, "CONTROLLED_ROUTE_READY_WITHOUT_PROVIDER", safety, safety, False)


def degrade(manifest: VisualCapabilityManifestV1) -> VisualCapabilityManifestV1:
    return replace(manifest, lifecycle_state="DEGRADED")


def make_mandatory_slot(slot_id: str, category: str, minimum_ref: str) -> SafetyCapabilitySlotV1:
    return SafetyCapabilitySlotV1(
        slot_id=slot_id,
        capability_category=category,
        mandatory=True,
        minimum_semantic_set_ref=minimum_ref,
        minimum_supported_baseline="safety-baseline-v1",
        approved_provider_refs=(f"approved-provider:{category.lower()}",),
        rollback_policy_ref=f"rollback:{slot_id}",
        degradation_policy_ref=f"degradation:{slot_id}",
    )
