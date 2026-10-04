# -*- coding: utf-8 -*-
"""Shared Provider Runtime Governance Skeleton — registry v1."""

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.provider_runtime_governance.domain_profiles.spatial_evidence_provider_governance_profile_v1 import (
    build_spatial_evidence_domain_governance_catalog_v1,
    build_spatial_evidence_provider_governance_profile_v1,
)
from capabilities.midplatform.provider_runtime_governance.domain_profiles.vision_ocr_governance_compatibility_v1 import (
    build_ocr_provider_governance_profile_stub_v1,
    build_vision_provider_governance_profile_stub_v1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_types_v1 import (
    DOMAIN_ASR,
    DOMAIN_OCR,
    DOMAIN_SPATIAL_EVIDENCE,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_DOMAIN_PROFILES,
    MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
    ProviderDisableRequest,
    ProviderDomainGovernanceProfile,
    ProviderEnableRequest,
    ProviderManagerDecision,
    ProviderRuntimeEligibilityResultV1,
    ProviderRuntimeEvaluationProfileV1,
    CANONICAL_PREGRANT_AUTHORITY_BINDING_KEY_FIELDS,
    PREGRANT_AUTHORITY_BINDING_KEY_FIELDS,
    SHARED_MANAGER_REF,
    SUPPORTED_DOMAIN_IDS,
    candidate_to_dict,
)

REGISTRY_ID = "provider_runtime_governance_registry_v1"
PREGRANT_CATALOG_REF = "provider-runtime-governance-catalog"
PREGRANT_CATALOG_VERSION = "v1"
PRODUCTION_PROVIDER_EVALUATION_PROFILE_REF = "provider-runtime-profile:production-canonical"
CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF = "provider-runtime-profile:controlled-binding-evaluation-v1"
EVALUATION_PROFILE_CATALOG_REF = "provider-runtime-evaluation-profiles"
EVALUATION_PROFILE_CATALOG_VERSION = "v1"
CONTROLLED_PROVIDER_REFS = (
    "provider:yolo:local:v1",
    "provider:controlled:1",
    "provider:controlled:2",
    "provider:controlled:model",
    "provider:controlled:shared",
    "provider:controlled:scenario12:signage",
    "provider:controlled:scenario12:flow",
)

MANAGER_STATUSES: Tuple[str, ...] = (
    "planning",
    "dryrun_ready",
    "runtime_skeleton_ready",
    "blocked",
    "disabled",
)

REGISTRATION_STATUSES: Tuple[str, ...] = (
    "registered_candidate",
    "admission_planned",
    "runtime_pending",
    "runtime_blocked",
    "disabled",
)

RUNTIME_STATUSES: Tuple[str, ...] = (
    "disabled",
    "planned",
    "pending_admission",
    "enabled",
    "degraded",
    "fallback_active",
    "blocked",
)

HEALTH_STATUSES: Tuple[str, ...] = (
    "healthy",
    "degraded",
    "unhealthy",
    "unknown",
)

FALLBACK_STATUSES: Tuple[str, ...] = (
    "not_required",
    "planned",
    "active",
    "failed",
    "unavailable",
)

OUTPUT_STATUSES: Tuple[str, ...] = (
    "no_output",
    "candidate_output_only",
    "degraded_candidate_output",
    "blocked",
)

REQUEST_SCOPES: Tuple[str, ...] = (
    "dryrun_only",
    "internal_dev",
    "commercial_runtime",
    "observation_only",
    "disabled_scope",
)

REQUESTED_BY: Tuple[str, ...] = (
    "system",
    "owner",
    "test_harness",
    "runtime_manager",
    "unknown",
)

REQUIRED_CHECKS: Tuple[str, ...] = (
    "license_gate",
    "adapter_contract_gate",
    "provider_admission_gate",
    "health_gate",
    "fallback_gate",
    "field_synthesis_gate",
    "static_validation_gate",
    "owner_approval_gate",
)

HEALTH_DECISIONS: Tuple[str, ...] = (
    "allow_candidate_output",
    "degrade_candidate_output",
    "disable_provider",
    "request_more_observation",
    "block_runtime",
)

FALLBACK_MODES: Tuple[str, ...] = (
    "none",
    "disable_only",
    "switch_to_mock",
    "switch_to_lower_capability_provider",
    "request_more_observation",
    "user_confirmation_required",
)

SIGNAL_NAMES: Tuple[str, ...] = (
    "tracking_status",
    "drift_risk",
    "confidence",
    "source_freshness",
    "ocr_quality",
    "detection_quality",
    "unknown",
)

SOURCE_FRESHNESS_LEVELS: Tuple[str, ...] = (
    "fresh",
    "stale",
    "unknown",
)

ADMISSION_STAGES: Tuple[str, ...] = (
    "planning_only",
    "technical_reference",
    "observation_only",
    "runtime_pending",
    "blocked",
)

SYNTHESIS_ENTRYPOINTS: Tuple[str, ...] = (
    FIELD_SYNTHESIS_ENTRYPOINT,
    MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
)

FORBIDDEN_PROVIDER_MANAGER_POLICIES: Tuple[str, ...] = (
    "manager_enable_runtime_without_admission",
    "manager_enable_commercial_runtime",
    "manager_bypass_license_gate",
    "manager_bypass_adapter_contract",
    "manager_bypass_provider_admission",
    "manager_bypass_field_synthesis",
    "manager_direct_action",
    "manager_direct_speech",
    "manager_direct_fact_write",
    "manager_enable_provider_by_default",
    "manager_output_without_candidate_only",
    "manager_fallback_without_source_chain",
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "manager_statuses": MANAGER_STATUSES,
    "registration_statuses": REGISTRATION_STATUSES,
    "runtime_statuses": RUNTIME_STATUSES,
    "health_statuses": HEALTH_STATUSES,
    "fallback_statuses": FALLBACK_STATUSES,
    "output_statuses": OUTPUT_STATUSES,
    "request_scopes": REQUEST_SCOPES,
    "requested_by": REQUESTED_BY,
    "required_checks": REQUIRED_CHECKS,
    "health_decisions": HEALTH_DECISIONS,
    "fallback_modes": FALLBACK_MODES,
    "signal_names": SIGNAL_NAMES,
    "source_freshness_levels": SOURCE_FRESHNESS_LEVELS,
    "admission_stages": ADMISSION_STAGES,
    "synthesis_entrypoints": SYNTHESIS_ENTRYPOINTS,
    "supported_domain_ids": SUPPORTED_DOMAIN_IDS,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for domain, values in REGISTRY.items():
        if not values:
            issues.append(f"registry_domain_missing:{domain}")
    if len(FORBIDDEN_PROVIDER_MANAGER_POLICIES) < 12:
        issues.append("forbidden_provider_manager_policies_incomplete")
    return len(issues) == 0, issues


def _profile_from_stub(stub: Dict[str, Any]) -> ProviderDomainGovernanceProfile:
    return ProviderDomainGovernanceProfile(
        profile_ref=stub["profile_ref"],
        domain_id=stub["domain_id"],
        domain_name=stub["domain_name"],
        admission_layer_ref=stub["admission_layer_ref"],
        synthesis_entrypoint=stub["synthesis_entrypoint"],
        provider_refs=tuple(stub["provider_refs"]),
        supported_output_candidate_types=tuple(stub["supported_output_candidate_types"]),
        domain_risk_tags=tuple(stub["domain_risk_tags"]),
        uses_shared_manager_skeleton=stub["uses_shared_manager_skeleton"],
    )


def build_shared_provider_runtime_governance_catalog_v1() -> Dict[str, object]:
    spatial_catalog = build_spatial_evidence_domain_governance_catalog_v1()
    spatial_profile = build_spatial_evidence_provider_governance_profile_v1()
    vision_profile = _profile_from_stub(build_vision_provider_governance_profile_stub_v1())
    ocr_profile = _profile_from_stub(build_ocr_provider_governance_profile_stub_v1())

    enable_requests = (
        ProviderEnableRequest(
            enable_request_ref="enable_request_spatial_openvins_dryrun",
            domain_id=DOMAIN_SPATIAL_EVIDENCE,
            provider_ref="provider_openvins",
            requested_scope="dryrun_only",
            requested_by="test_harness",
            reason="shared_skeleton_planning_enable_candidate",
            required_checks=REQUIRED_CHECKS[:-1],
            approval_required=False,
            execution_allowed=False,
        ),
        ProviderEnableRequest(
            enable_request_ref="enable_request_ocr_mock_observation",
            domain_id=DOMAIN_OCR,
            provider_ref="ocr_provider_mock_fixture",
            requested_scope="observation_only",
            requested_by="system",
            reason="ocr_shared_skeleton_enable_candidate",
            required_checks=REQUIRED_CHECKS,
            approval_required=True,
            execution_allowed=False,
        ),
    )

    disable_requests = (
        ProviderDisableRequest(
            disable_request_ref="disable_request_spatial_default",
            domain_id=DOMAIN_SPATIAL_EVIDENCE,
            provider_ref="provider_openvins",
            disable_reason="planning_default_disabled",
            disable_scope="provider_only",
            fallback_required=True,
            preserve_source_chain=True,
            execution_allowed=False,
        ),
    )

    decision = ProviderManagerDecision(
        decision_ref="shared_provider_runtime_governance_decision_v1",
        manager_ref=SHARED_MANAGER_REF,
        domain_id=DOMAIN_SPATIAL_EVIDENCE,
        registered_provider_refs=spatial_profile.provider_refs,
        runtime_enabled_provider_refs=(),
        default_disabled_provider_refs=spatial_profile.provider_refs,
        enable_request_refs=tuple(r.enable_request_ref for r in enable_requests),
        disable_request_refs=tuple(r.disable_request_ref for r in disable_requests),
        fallback_route_refs=tuple(
            item["fallback_route_ref"] for item in spatial_catalog["fallback_routes"]  # type: ignore[index]
        ),
        runtime_activation_allowed=False,
        provider_runtime_enabled=False,
        final_decision=FINAL_DECISION_READY_FOR_DOMAIN_PROFILES,
    )

    return {
        "shared_manager_ref": SHARED_MANAGER_REF,
        "domain_profiles": [
            candidate_to_dict(spatial_profile),
            candidate_to_dict(vision_profile),
            candidate_to_dict(ocr_profile),
        ],
        "spatial_evidence_catalog": spatial_catalog,
        "vision_profile": candidate_to_dict(vision_profile),
        "ocr_profile": candidate_to_dict(ocr_profile),
        "enable_requests": [candidate_to_dict(r) for r in enable_requests],
        "disable_requests": [candidate_to_dict(r) for r in disable_requests],
        "decision": candidate_to_dict(decision),
        "route_note": (
            "Domain-specific ProviderManager skeletons are superseded by this shared layer. "
            "Spatial Evidence connects via spatial_evidence_provider_governance_profile_v1."
        ),
    }


def build_shared_provider_runtime_governance_matrix_v1() -> Dict[str, object]:
    return build_shared_provider_runtime_governance_catalog_v1()


def _production_provider_refs() -> Tuple[str, ...]:
    catalog = build_shared_provider_runtime_governance_catalog_v1()
    profiles = catalog.get("domain_profiles", ())
    return tuple(
        dict.fromkeys(
            provider_ref
            for profile in profiles
            for provider_ref in profile.get("provider_refs", ())
        )
    )


def _provider_evaluation_profiles() -> Dict[str, ProviderRuntimeEvaluationProfileV1]:
    return {
        PRODUCTION_PROVIDER_EVALUATION_PROFILE_REF: ProviderRuntimeEvaluationProfileV1(
            profile_ref=PRODUCTION_PROVIDER_EVALUATION_PROFILE_REF,
            owner_ref="Provider Governance",
            catalog_ref=PREGRANT_CATALOG_REF,
            catalog_version=PREGRANT_CATALOG_VERSION,
            provider_refs=_production_provider_refs(),
            provenance_refs=("provenance:provider-runtime-governance:production",),
            production_canonical=True,
        ),
        CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF: ProviderRuntimeEvaluationProfileV1(
            profile_ref=CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF,
            owner_ref="Provider Governance",
            catalog_ref=EVALUATION_PROFILE_CATALOG_REF,
            catalog_version=EVALUATION_PROFILE_CATALOG_VERSION,
            provider_refs=CONTROLLED_PROVIDER_REFS,
            provenance_refs=("provenance:provider-runtime-governance:controlled-evaluation",),
            production_canonical=False,
        ),
    }


def resolve_provider_runtime_evaluation_profile_v1(
    profile_ref: object = PRODUCTION_PROVIDER_EVALUATION_PROFILE_REF,
) -> ProviderRuntimeEvaluationProfileV1 | None:
    if not isinstance(profile_ref, str) or not profile_ref.strip():
        return None
    return _provider_evaluation_profiles().get(profile_ref)


def _pregrant_result_ref(
    binding_key: Tuple[str, ...],
    provider_ref: str,
    capability_ref: str,
    profile_ref: str,
) -> str:
    digest = hashlib.sha256(
        "|".join(
            (*binding_key, provider_ref, capability_ref, profile_ref, PREGRANT_CATALOG_VERSION)
        ).encode("utf-8")
    ).hexdigest()[:24]
    return f"provider-runtime-eligibility:{digest}"


def evaluate_provider_runtime_eligibility_v1(
    *,
    binding_key: Tuple[str, ...],
    provider_candidate_ref: str,
    capability_candidate_ref: str,
    execution_instance_preparation_candidate_ref: str,
    profile_ref: object = PRODUCTION_PROVIDER_EVALUATION_PROFILE_REF,
) -> ProviderRuntimeEligibilityResultV1:
    """Resolve provider eligibility from an owner-defined current profile.

    Binding candidates and caller status fields are never treated as Provider
    admission.  The profile is selected by reference only; its catalog content
    is resolved inside Provider Governance and an unknown profile fails closed.
    """

    profile = resolve_provider_runtime_evaluation_profile_v1(profile_ref)
    if profile is None:
        return ProviderRuntimeEligibilityResultV1(
            result_ref="",
            binding_key=tuple(binding_key),
            provider_candidate_ref=provider_candidate_ref,
            capability_candidate_ref=capability_candidate_ref,
            execution_instance_preparation_candidate_ref=execution_instance_preparation_candidate_ref,
            status="DENIED",
            reason="provider_evaluation_profile_invalid",
            catalog_ref=EVALUATION_PROFILE_CATALOG_REF,
            catalog_version=EVALUATION_PROFILE_CATALOG_VERSION,
            evaluation_profile_ref="",
        )

    canonical_binding = (
        len(binding_key) == len(CANONICAL_PREGRANT_AUTHORITY_BINDING_KEY_FIELDS)
        and binding_key[0] == "runtime-scope:v2"
    )
    if not canonical_binding or not all(binding_key):
        return ProviderRuntimeEligibilityResultV1(
            result_ref="",
            binding_key=tuple(binding_key),
            provider_candidate_ref=provider_candidate_ref,
            capability_candidate_ref=capability_candidate_ref,
            execution_instance_preparation_candidate_ref=execution_instance_preparation_candidate_ref,
            status="DENIED",
            reason="provider_binding_key_invalid",
            catalog_ref=profile.catalog_ref,
            catalog_version=profile.catalog_version,
            evaluation_profile_ref=profile.profile_ref,
        )

    known = provider_candidate_ref in profile.provider_refs
    return ProviderRuntimeEligibilityResultV1(
        result_ref=_pregrant_result_ref(
            binding_key,
            provider_candidate_ref,
            capability_candidate_ref,
            profile.profile_ref,
        ),
        binding_key=tuple(binding_key),
        provider_candidate_ref=provider_candidate_ref,
        capability_candidate_ref=capability_candidate_ref,
        execution_instance_preparation_candidate_ref=execution_instance_preparation_candidate_ref,
        status="ELIGIBLE" if known else "DENIED",
        reason="current_provider_profile_match" if known else "provider_not_registered_in_selected_profile",
        catalog_ref=profile.catalog_ref,
        catalog_version=profile.catalog_version,
        evaluation_profile_ref=profile.profile_ref,
    )


__all__ = [
    "evaluate_provider_runtime_eligibility_v1",
    "resolve_provider_runtime_evaluation_profile_v1",
    "build_shared_provider_runtime_governance_catalog_v1",
    "build_shared_provider_runtime_governance_matrix_v1",
    "PRODUCTION_PROVIDER_EVALUATION_PROFILE_REF",
    "CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF",
    "ProviderRuntimeEligibilityResultV1",
    "ProviderRuntimeEvaluationProfileV1",
]
