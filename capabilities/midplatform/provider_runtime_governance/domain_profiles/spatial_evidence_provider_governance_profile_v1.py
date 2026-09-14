# -*- coding: utf-8 -*-
"""Spatial Evidence domain profile for shared Provider Runtime Governance."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_registry_v1 import (
    build_provider_planning_bundles_v1,
)
from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_types_v1 import (
    DOMAIN_SPATIAL_EVIDENCE,
    ProviderDomainGovernanceProfile,
    ProviderFallbackRoute,
    ProviderHealthSnapshot,
    ProviderRegistryEntry,
    ProviderRuntimeAdmissionCheck,
    ProviderRuntimeGovernanceManager,
    ProviderRuntimeState,
    SHARED_MANAGER_REF,
    candidate_to_dict,
)

SPATIAL_EVIDENCE_ADMISSION_LAYER_REF = (
    "field_spatial_evidence_provider_admission_registry_v1"
)
SPATIAL_EVIDENCE_PROFILE_REF = "spatial_evidence_provider_governance_profile_v1"

SPATIAL_EVIDENCE_DOMAIN_RISK_TAGS: Tuple[str, ...] = (
    "gpl_license_risk",
    "observation_only_provider",
    "slam_health_signal_required",
    "local_map_drift_risk",
    "scene_graph_observation_only",
    "no_commercial_runtime_by_default",
)


def build_spatial_evidence_provider_governance_profile_v1() -> ProviderDomainGovernanceProfile:
    bundles = build_provider_planning_bundles_v1()
    provider_refs = tuple(b[0].provider_ref for b in bundles)
    candidate_types: List[str] = []
    for bundle in bundles:
        policy, profile, *_rest = bundle
        candidate_types.extend(profile.supported_candidate_types)
    unique_candidates = tuple(dict.fromkeys(candidate_types))

    return ProviderDomainGovernanceProfile(
        profile_ref=SPATIAL_EVIDENCE_PROFILE_REF,
        domain_id=DOMAIN_SPATIAL_EVIDENCE,
        domain_name="Spatial Evidence / SLAM-VIO-SceneGraph",
        admission_layer_ref=SPATIAL_EVIDENCE_ADMISSION_LAYER_REF,
        synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        provider_refs=provider_refs,
        supported_output_candidate_types=unique_candidates,
        domain_risk_tags=SPATIAL_EVIDENCE_DOMAIN_RISK_TAGS,
        uses_shared_manager_skeleton=True,
    )


def build_spatial_evidence_governance_manager_v1() -> ProviderRuntimeGovernanceManager:
    profile = build_spatial_evidence_provider_governance_profile_v1()
    return ProviderRuntimeGovernanceManager(
        manager_ref=f"{SHARED_MANAGER_REF}_{DOMAIN_SPATIAL_EVIDENCE}",
        domain_id=DOMAIN_SPATIAL_EVIDENCE,
        manager_status="planning",
        managed_provider_refs=profile.provider_refs,
        default_enabled_provider_refs=(),
        default_disabled_provider_refs=profile.provider_refs,
        synthesis_entrypoint=profile.synthesis_entrypoint,
        runtime_activation_allowed=False,
        provider_runtime_enabled=False,
    )


def _registry_entry_from_admission_bundle(
    bundle: Tuple[Any, ...],
) -> ProviderRegistryEntry:
    policy, profile, health, fallback, _admission = bundle
    return ProviderRegistryEntry(
        registry_entry_ref=f"registry_entry_{policy.provider_ref}",
        domain_id=DOMAIN_SPATIAL_EVIDENCE,
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
        supported_output_candidate_types=profile.supported_candidate_types,
    )


def _runtime_state_for_provider(provider_ref: str) -> ProviderRuntimeState:
    return ProviderRuntimeState(
        runtime_state_ref=f"runtime_state_{provider_ref}",
        domain_id=DOMAIN_SPATIAL_EVIDENCE,
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
        domain_id=DOMAIN_SPATIAL_EVIDENCE,
        provider_ref=provider_ref,
        signal_name="tracking_status",
        signal_value="ok",
        confidence=0.75,
        source_freshness="fresh",
        health_decision="allow_candidate_output",
        degradation_required=False,
        disable_required=False,
    )


def _admission_check_from_bundle(bundle: Tuple[Any, ...]) -> ProviderRuntimeAdmissionCheck:
    policy, _profile, _health, _fallback, admission = bundle
    return ProviderRuntimeAdmissionCheck(
        admission_check_ref=f"admission_check_{policy.provider_ref}",
        domain_id=DOMAIN_SPATIAL_EVIDENCE,
        provider_ref=policy.provider_ref,
        admission_stage=admission.admission_stage,
        license_gate_passed=admission.license_gate_passed,
        adapter_contract_passed=admission.adapter_contract_passed,
        provider_admission_gate_passed=admission.provider_policy_passed,
        health_gate_passed=admission.health_gate_passed,
        fallback_gate_passed=admission.fallback_policy_passed,
        synthesis_gate_passed=policy.field_synthesis_entrypoint == FIELD_SYNTHESIS_ENTRYPOINT,
        static_validation_passed=admission.static_validation_passed,
        runtime_admission_allowed=False,
        blocked_reasons=admission.blocked_reasons,
    )


def _fallback_route_from_bundle(bundle: Tuple[Any, ...]) -> ProviderFallbackRoute:
    policy, _profile, _health, fallback, _admission = bundle
    return ProviderFallbackRoute(
        fallback_route_ref=f"fallback_route_{policy.provider_ref}",
        domain_id=DOMAIN_SPATIAL_EVIDENCE,
        provider_ref=policy.provider_ref,
        fallback_provider_refs=fallback.fallback_provider_refs,
        fallback_mode=fallback.fallback_mode,
        trigger_conditions=fallback.fallback_trigger_conditions,
        preserve_source_chain=fallback.preserve_source_chain,
        preserve_conflict_refs=fallback.preserve_conflict_refs,
    )


def build_spatial_evidence_domain_governance_catalog_v1() -> Dict[str, object]:
    bundles = build_provider_planning_bundles_v1()
    profile = build_spatial_evidence_provider_governance_profile_v1()
    manager = build_spatial_evidence_governance_manager_v1()

    registry_entries = [_registry_entry_from_admission_bundle(b) for b in bundles]
    runtime_states = [_runtime_state_for_provider(e.provider_ref) for e in registry_entries]
    health_snapshots = [_health_snapshot_for_provider(e.provider_ref) for e in registry_entries]
    fallback_routes = [_fallback_route_from_bundle(b) for b in bundles]
    admission_checks = [_admission_check_from_bundle(b) for b in bundles]

    return {
        "domain_profile": candidate_to_dict(profile),
        "manager": candidate_to_dict(manager),
        "registry_entries": [candidate_to_dict(e) for e in registry_entries],
        "runtime_states": [candidate_to_dict(s) for s in runtime_states],
        "health_snapshots": [candidate_to_dict(h) for h in health_snapshots],
        "fallback_routes": [candidate_to_dict(r) for r in fallback_routes],
        "admission_checks": [candidate_to_dict(c) for c in admission_checks],
    }
