# -*- coding: utf-8 -*-
"""Field Spatial Evidence Provider Manager Skeleton Planning — registry v1.

SUPERSEDED_BY_SHARED_PROVIDER_RUNTIME_GOVERNANCE:
Use capabilities/midplatform/provider_runtime_governance/domain_profiles/
spatial_evidence_provider_governance_profile_v1.py for domain mapping.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_registry_v1 import (
    PROVIDER_ROLES as ADMISSION_PROVIDER_ROLES,
    build_provider_planning_bundles_v1,
)
from capabilities.field_understanding.spatial_evidence_provider_manager.field_spatial_evidence_provider_manager_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    MANAGER_REF,
    ProviderDisableRequest,
    ProviderEnableRequest,
    ProviderFallbackRoute,
    ProviderHealthSnapshot,
    ProviderManagerPlanningDecision,
    ProviderRegistryEntry,
    ProviderRuntimeState,
    SpatialEvidenceProviderManager,
    candidate_to_dict,
)

REGISTRY_ID = "field_spatial_evidence_provider_manager_registry_v1"

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

TRACKING_STATUSES: Tuple[str, ...] = (
    "ok",
    "degraded",
    "tracking_lost",
    "unknown",
)

DRIFT_RISK_LEVELS: Tuple[str, ...] = (
    "low",
    "medium",
    "high",
    "unknown",
)

SOURCE_FRESHNESS_LEVELS: Tuple[str, ...] = (
    "fresh",
    "stale",
    "unknown",
)

DISABLE_REASONS: Tuple[str, ...] = (
    "planning_default_disabled",
    "admission_not_granted",
    "health_gate_failed",
    "license_blocked",
    "owner_requested",
    "tracking_lost",
    "high_drift",
)

DISABLE_SCOPES: Tuple[str, ...] = (
    "provider_only",
    "backend_only",
    "runtime_scope",
    "commercial_scope",
    "all_scopes",
)

PLANNING_PROVIDER_REFS: Tuple[str, ...] = (
    "provider_openvins",
    "provider_vins_fusion",
    "provider_orb_slam3",
    "provider_rtab_map",
    "provider_kimera",
    "provider_hydra",
    "provider_grapheqa",
)

STANDARD_REQUIRED_CHECKS: Tuple[str, ...] = (
    "license_gate",
    "adapter_contract_gate",
    "provider_admission_gate",
    "health_gate",
    "fallback_gate",
    "field_synthesis_gate",
    "static_validation_gate",
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
    "tracking_statuses": TRACKING_STATUSES,
    "drift_risk_levels": DRIFT_RISK_LEVELS,
    "source_freshness_levels": SOURCE_FRESHNESS_LEVELS,
    "disable_reasons": DISABLE_REASONS,
    "disable_scopes": DISABLE_SCOPES,
    "provider_roles": ADMISSION_PROVIDER_ROLES,
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


def _registry_entry_from_admission_bundle(
    bundle: Tuple[Any, ...],
) -> ProviderRegistryEntry:
    policy, profile, health, fallback, _admission = bundle
    return ProviderRegistryEntry(
        registry_entry_ref=f"registry_entry_{policy.provider_ref}",
        provider_ref=policy.provider_ref,
        backend_ref=policy.backend_ref,
        adapter_ref=policy.adapter_ref,
        provider_role=policy.provider_role,
        registration_status="registered_candidate",
        admission_policy_ref=policy.policy_ref,
        health_gate_ref=health.health_gate_ref,
        fallback_policy_ref=fallback.fallback_policy_ref,
        enabled_by_default=False,
        runtime_enable_allowed=False,
        supported_candidate_types=profile.supported_candidate_types,
    )


def _runtime_state_for_provider(provider_ref: str) -> ProviderRuntimeState:
    return ProviderRuntimeState(
        runtime_state_ref=f"runtime_state_{provider_ref}",
        provider_ref=provider_ref,
        runtime_status="disabled",
        health_status="healthy",
        fallback_status="not_required",
        output_status="no_output",
        last_health_signal_ref=f"health_snapshot_{provider_ref}",
        source_chain_preserved=True,
    )


def _health_snapshot_for_provider(provider_ref: str) -> ProviderHealthSnapshot:
    return ProviderHealthSnapshot(
        health_snapshot_ref=f"health_snapshot_{provider_ref}",
        provider_ref=provider_ref,
        tracking_status="ok",
        drift_risk="low",
        confidence=0.75,
        source_freshness="fresh",
        health_decision="allow_candidate_output",
        degradation_required=False,
        disable_required=False,
    )


def _fallback_route_from_admission(
    bundle: Tuple[Any, ...],
) -> ProviderFallbackRoute:
    policy, _profile, _health, fallback, _admission = bundle
    return ProviderFallbackRoute(
        fallback_route_ref=f"fallback_route_{policy.provider_ref}",
        provider_ref=policy.provider_ref,
        fallback_provider_refs=fallback.fallback_provider_refs,
        fallback_mode=fallback.fallback_mode,
        trigger_conditions=fallback.fallback_trigger_conditions,
        preserve_source_chain=fallback.preserve_source_chain,
        preserve_conflict_refs=fallback.preserve_conflict_refs,
    )


def build_provider_enable_requests_v1() -> Tuple[ProviderEnableRequest, ...]:
    return (
        ProviderEnableRequest(
            enable_request_ref="enable_request_openvins_dryrun",
            provider_ref="provider_openvins",
            requested_scope="dryrun_only",
            requested_by="test_harness",
            reason="planning_only_enable_request_candidate",
            required_checks=STANDARD_REQUIRED_CHECKS,
            approval_required=False,
            execution_allowed=False,
        ),
        ProviderEnableRequest(
            enable_request_ref="enable_request_kimera_observation",
            provider_ref="provider_kimera",
            requested_scope="observation_only",
            requested_by="system",
            reason="observation_scope_enable_request_candidate",
            required_checks=STANDARD_REQUIRED_CHECKS,
            approval_required=True,
            execution_allowed=False,
        ),
        ProviderEnableRequest(
            enable_request_ref="enable_request_openvins_commercial",
            provider_ref="provider_openvins",
            requested_scope="commercial_runtime",
            requested_by="owner",
            reason="commercial_runtime_enable_request_must_not_execute",
            required_checks=STANDARD_REQUIRED_CHECKS + ("owner_approval_gate",),
            approval_required=True,
            execution_allowed=False,
        ),
    )


def build_provider_disable_requests_v1() -> Tuple[ProviderDisableRequest, ...]:
    return (
        ProviderDisableRequest(
            disable_request_ref="disable_request_openvins_planning_default",
            provider_ref="provider_openvins",
            disable_reason="planning_default_disabled",
            disable_scope="provider_only",
            fallback_required=True,
            preserve_source_chain=True,
            execution_allowed=False,
        ),
        ProviderDisableRequest(
            disable_request_ref="disable_request_grapheqa_observation",
            provider_ref="provider_grapheqa",
            disable_reason="admission_not_granted",
            disable_scope="runtime_scope",
            fallback_required=True,
            preserve_source_chain=True,
            execution_allowed=False,
        ),
    )


def build_spatial_evidence_provider_manager_v1() -> SpatialEvidenceProviderManager:
    provider_refs = PLANNING_PROVIDER_REFS
    return SpatialEvidenceProviderManager(
        manager_ref=MANAGER_REF,
        manager_status="planning",
        managed_provider_refs=provider_refs,
        default_enabled_provider_refs=(),
        default_disabled_provider_refs=provider_refs,
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        runtime_activation_allowed=False,
        provider_runtime_enabled=False,
    )


def build_provider_manager_planning_catalog_v1() -> Dict[str, object]:
    bundles = build_provider_planning_bundles_v1()
    registry_entries = [_registry_entry_from_admission_bundle(b) for b in bundles]
    runtime_states = [_runtime_state_for_provider(e.provider_ref) for e in registry_entries]
    health_snapshots = [_health_snapshot_for_provider(e.provider_ref) for e in registry_entries]
    fallback_routes = [_fallback_route_from_admission(b) for b in bundles]
    enable_requests = list(build_provider_enable_requests_v1())
    disable_requests = list(build_provider_disable_requests_v1())

    manager = build_spatial_evidence_provider_manager_v1()
    provider_refs = tuple(e.provider_ref for e in registry_entries)

    decision = ProviderManagerPlanningDecision(
        decision_ref="provider_manager_planning_decision_v1",
        manager_ref=manager.manager_ref,
        registered_provider_refs=provider_refs,
        runtime_enabled_provider_refs=(),
        default_disabled_provider_refs=provider_refs,
        enable_request_refs=tuple(r.enable_request_ref for r in enable_requests),
        disable_request_refs=tuple(r.disable_request_ref for r in disable_requests),
        fallback_route_refs=tuple(r.fallback_route_ref for r in fallback_routes),
        runtime_activation_allowed=False,
        provider_runtime_enabled=False,
        final_decision=FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    )

    return {
        "manager": candidate_to_dict(manager),
        "registry_entries": [candidate_to_dict(e) for e in registry_entries],
        "enable_requests": [candidate_to_dict(r) for r in enable_requests],
        "disable_requests": [candidate_to_dict(r) for r in disable_requests],
        "runtime_states": [candidate_to_dict(s) for s in runtime_states],
        "health_snapshots": [candidate_to_dict(h) for h in health_snapshots],
        "fallback_routes": [candidate_to_dict(r) for r in fallback_routes],
        "decision": candidate_to_dict(decision),
    }


def build_provider_manager_planning_matrix_v1() -> Dict[str, object]:
    return build_provider_manager_planning_catalog_v1()
