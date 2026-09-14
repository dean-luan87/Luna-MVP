# -*- coding: utf-8 -*-
"""Field Spatial Evidence Provider Admission Planning — registry and catalog v1."""

from __future__ import annotations

from typing import Dict, FrozenSet, List, Tuple

from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    MOCK_FALLBACK_PROVIDER_REF,
    ProviderAdmissionPlanningDecision,
    ProviderCapabilityProfile,
    ProviderFallbackPolicy,
    ProviderHealthGate,
    ProviderRuntimeAdmissionCandidate,
    SpatialEvidenceProviderAdmissionPolicy,
    candidate_to_dict,
)

REGISTRY_ID = "field_spatial_evidence_provider_admission_registry_v1"

PROVIDER_ROLES: Tuple[str, ...] = (
    "pose_motion_provider",
    "local_map_provider",
    "relocalization_provider",
    "semantic_spatial_provider",
    "scene_graph_observation_provider",
    "mock_provider",
    "custom_luna_provider",
)

ADMISSION_MODES: Tuple[str, ...] = (
    "planning_only",
    "technical_reference_only",
    "internal_runtime_candidate",
    "commercial_runtime_candidate",
    "observation_only",
    "blocked",
)

RUNTIME_SCOPES: Tuple[str, ...] = (
    "none",
    "offline_reference",
    "dryrun_only",
    "internal_dev_only",
    "commercial_runtime",
    "observation_only",
)

REQUIRED_GATES: Tuple[str, ...] = (
    "license_gate",
    "adapter_contract_gate",
    "provider_policy_gate",
    "capability_profile_gate",
    "health_gate",
    "fallback_gate",
    "static_validation_gate",
    "runtime_admission_gate",
)

HEALTH_SIGNALS: Tuple[str, ...] = (
    "tracking_status",
    "drift_risk",
    "confidence",
    "source_freshness",
    "feature_quality",
    "imu_quality",
    "mapping_quality",
    "relocalization_quality",
)

DEGRADED_CONDITIONS: Tuple[str, ...] = (
    "tracking_degraded",
    "high_drift",
    "low_confidence",
    "stale_source",
    "poor_feature_quality",
    "imu_unstable",
    "mapping_unstable",
    "relocalization_uncertain",
)

BLOCKED_CONDITIONS: Tuple[str, ...] = (
    "tracking_lost",
    "license_blocked",
    "adapter_contract_failed",
    "field_synthesis_entrypoint_missing",
    "candidate_only_violation",
    "source_refs_missing",
    "runtime_scope_violation",
)

FALLBACK_MODES: Tuple[str, ...] = (
    "none",
    "disable_only",
    "switch_to_mock",
    "switch_to_lower_capability_provider",
    "request_more_observation",
    "user_confirmation_required",
)

DISABLE_SCOPES: Tuple[str, ...] = (
    "provider_only",
    "backend_only",
    "runtime_scope",
    "commercial_scope",
    "all_scopes",
)

LATENCY_CLASSES: Tuple[str, ...] = (
    "realtime",
    "near_realtime",
    "offline",
    "unknown",
)

COMPUTE_CLASSES: Tuple[str, ...] = (
    "light",
    "medium",
    "heavy",
    "unknown",
)

RELIABILITY_CLASSES: Tuple[str, ...] = (
    "high",
    "medium",
    "low",
    "unknown",
)

FIT_LEVELS: Tuple[str, ...] = (
    "high",
    "medium",
    "low",
    "not_applicable",
    "unknown",
)

ADMISSION_STAGES: Tuple[str, ...] = (
    "technical_reference",
    "adapter_planning",
    "dryrun_candidate",
    "internal_runtime_candidate",
    "commercial_runtime_candidate",
    "observation_only",
    "blocked",
)

DRIFT_POLICIES: Tuple[str, ...] = (
    "downweight_evidence",
    "request_relocalization",
    "disable_provider",
    "needs_more_observation",
)

TRACKING_LOST_POLICIES: Tuple[str, ...] = (
    "disable_provider",
    "fallback_to_mock",
    "needs_more_observation",
)

DEGRADATION_OUTPUT_POLICIES: Tuple[str, ...] = (
    "emit_health_only",
    "downweight_evidence",
    "needs_more_observation",
    "disable_output",
)

FALLBACK_OUTPUT_POLICIES: Tuple[str, ...] = (
    "preserve_candidate_chain",
    "emit_health_only",
    "needs_more_observation",
    "disable_output",
)

DISABLE_DURATION_POLICIES: Tuple[str, ...] = (
    "until_health_recovered",
    "until_manual_reset",
    "session_only",
    "permanent_until_review",
)

OUTPUT_CANDIDATE_TYPES: Tuple[str, ...] = (
    "PoseCandidate",
    "MotionCandidate",
    "SpatialAnchorCandidate",
    "LocalMapCandidate",
    "SLAMHealthCandidate",
    "MapDriftCandidate",
    "RelocalizationCandidate",
    "SemanticFieldObjectCandidate",
    "FieldGraphCandidate",
    "SemanticMemoryMapCandidate",
)

INPUT_MODES: Tuple[str, ...] = (
    "monocular_camera",
    "stereo_camera",
    "rgbd_camera",
    "imu",
    "offline_trace",
    "mock",
)

FORBIDDEN_PROVIDER_ADMISSION_POLICIES: Tuple[str, ...] = (
    "provider_direct_action",
    "provider_direct_speech",
    "provider_direct_fact_write",
    "provider_bypass_adapter_contract",
    "provider_bypass_field_synthesis",
    "provider_bypass_license_gate",
    "provider_runtime_without_health_gate",
    "provider_runtime_without_fallback",
    "gpl_provider_commercial_runtime",
    "observation_provider_runtime_admission",
    "provider_output_without_candidate_only",
    "provider_output_without_source_refs",
)

GPL_BACKEND_REFS: FrozenSet[str] = frozenset({"openvins", "vins_fusion", "orb_slam3"})

BLOCKED_RUNTIME_PROVIDER_REFS: FrozenSet[str] = frozenset(
    {"provider_openvins", "provider_vins_fusion", "provider_orb_slam3", "provider_grapheqa"}
)

OBSERVATION_ONLY_PROVIDER_REFS: FrozenSet[str] = frozenset(
    {"provider_kimera", "provider_hydra", "provider_grapheqa"}
)

STANDARD_REQUIRED_GATES: Tuple[str, ...] = (
    "license_gate",
    "adapter_contract_gate",
    "provider_policy_gate",
    "capability_profile_gate",
    "health_gate",
    "fallback_gate",
    "static_validation_gate",
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "provider_roles": PROVIDER_ROLES,
    "admission_modes": ADMISSION_MODES,
    "runtime_scopes": RUNTIME_SCOPES,
    "required_gates": REQUIRED_GATES,
    "health_signals": HEALTH_SIGNALS,
    "degraded_conditions": DEGRADED_CONDITIONS,
    "blocked_conditions": BLOCKED_CONDITIONS,
    "fallback_modes": FALLBACK_MODES,
    "disable_scopes": DISABLE_SCOPES,
    "latency_classes": LATENCY_CLASSES,
    "compute_classes": COMPUTE_CLASSES,
    "reliability_classes": RELIABILITY_CLASSES,
    "fit_levels": FIT_LEVELS,
    "admission_stages": ADMISSION_STAGES,
    "output_candidate_types": OUTPUT_CANDIDATE_TYPES,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for domain, values in REGISTRY.items():
        if not values:
            issues.append(f"registry_domain_missing:{domain}")
    if len(FORBIDDEN_PROVIDER_ADMISSION_POLICIES) < 12:
        issues.append("forbidden_provider_admission_policies_incomplete")
    return len(issues) == 0, issues


def _tech_ref_policy(
    *,
    backend_ref: str,
    provider_ref: str,
    adapter_ref: str,
    provider_role: str,
    required_candidate_types: Tuple[str, ...],
    optional_candidate_types: Tuple[str, ...],
    disable_conditions: Tuple[str, ...],
    health_signals: Tuple[str, ...],
) -> Tuple[
    SpatialEvidenceProviderAdmissionPolicy,
    ProviderCapabilityProfile,
    ProviderHealthGate,
    ProviderFallbackPolicy,
    ProviderRuntimeAdmissionCandidate,
]:
    fallback_ref = f"fallback_{provider_ref}"
    policy = SpatialEvidenceProviderAdmissionPolicy(
        policy_ref=f"admission_policy_{provider_ref}",
        provider_ref=provider_ref,
        backend_ref=backend_ref,
        adapter_ref=adapter_ref,
        provider_role=provider_role,
        admission_mode="technical_reference_only",
        allowed_runtime_scope="offline_reference",
        required_candidate_types=required_candidate_types,
        optional_candidate_types=optional_candidate_types,
        required_gates=STANDARD_REQUIRED_GATES,
        disable_conditions=disable_conditions,
        fallback_policy_ref=fallback_ref,
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        runtime_admission_allowed=False,
        commercial_runtime_allowed=False,
    )
    profile = ProviderCapabilityProfile(
        profile_ref=f"capability_{provider_ref}",
        provider_ref=provider_ref,
        backend_ref=backend_ref,
        supported_candidate_types=required_candidate_types + optional_candidate_types,
        required_input_modes=("offline_trace", "mock"),
        supported_runtime_modes=("offline_reference", "dryrun_only"),
        latency_class="near_realtime",
        compute_class="medium",
        reliability_class="medium",
        wearable_fit="medium",
        offline_fit="high",
        semantic_extension_fit="not_applicable",
        health_signal_supported=len(health_signals) > 0,
    )
    health = ProviderHealthGate(
        health_gate_ref=f"health_gate_{provider_ref}",
        provider_ref=provider_ref,
        required_health_signals=health_signals,
        degraded_conditions=("tracking_degraded", "high_drift", "low_confidence"),
        blocked_conditions=("tracking_lost", "license_blocked", "candidate_only_violation"),
        drift_policy="downweight_evidence",
        tracking_lost_policy="disable_provider",
        confidence_floor=0.35,
        degradation_output_policy="needs_more_observation",
    )
    fallback = ProviderFallbackPolicy(
        fallback_policy_ref=fallback_ref,
        provider_ref=provider_ref,
        fallback_provider_refs=(MOCK_FALLBACK_PROVIDER_REF,),
        fallback_mode="switch_to_mock",
        fallback_trigger_conditions=("tracking_lost", "adapter_contract_failed", "high_drift"),
        fallback_output_policy="preserve_candidate_chain",
        preserve_source_chain=True,
        preserve_conflict_refs=True,
    )
    blocked_reason = (
        ("gpl_license_blocks_commercial_runtime",)
        if backend_ref in GPL_BACKEND_REFS
        else ("planning_only_no_runtime_admission",)
    )
    admission = ProviderRuntimeAdmissionCandidate(
        admission_ref=f"provider_admission_{provider_ref}",
        provider_ref=provider_ref,
        backend_ref=backend_ref,
        adapter_ref=adapter_ref,
        admission_stage="technical_reference",
        license_gate_passed=True,
        adapter_contract_passed=True,
        provider_policy_passed=True,
        capability_profile_passed=True,
        health_gate_passed=True,
        fallback_policy_passed=True,
        static_validation_passed=True,
        runtime_admission_allowed=False,
        admission_reasons=("adapter_contract_planning_complete", "provider_admission_planning_only"),
        blocked_reasons=blocked_reason,
    )
    return policy, profile, health, fallback, admission


def _observation_bundle(
    *,
    backend_ref: str,
    provider_ref: str,
    adapter_ref: str,
    provider_role: str,
    required_candidate_types: Tuple[str, ...],
    optional_candidate_types: Tuple[str, ...],
    semantic_fit: str,
) -> Tuple[
    SpatialEvidenceProviderAdmissionPolicy,
    ProviderCapabilityProfile,
    ProviderHealthGate,
    ProviderFallbackPolicy,
    ProviderRuntimeAdmissionCandidate,
]:
    fallback_ref = f"fallback_{provider_ref}"
    policy = SpatialEvidenceProviderAdmissionPolicy(
        policy_ref=f"admission_policy_{provider_ref}",
        provider_ref=provider_ref,
        backend_ref=backend_ref,
        adapter_ref=adapter_ref,
        provider_role=provider_role,
        admission_mode="observation_only",
        allowed_runtime_scope="observation_only",
        required_candidate_types=required_candidate_types,
        optional_candidate_types=optional_candidate_types,
        required_gates=STANDARD_REQUIRED_GATES,
        disable_conditions=("runtime_scope_violation", "license_blocked", "tracking_lost"),
        fallback_policy_ref=fallback_ref,
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        runtime_admission_allowed=False,
        commercial_runtime_allowed=False,
    )
    profile = ProviderCapabilityProfile(
        profile_ref=f"capability_{provider_ref}",
        provider_ref=provider_ref,
        backend_ref=backend_ref,
        supported_candidate_types=required_candidate_types + optional_candidate_types,
        required_input_modes=("offline_trace", "mock"),
        supported_runtime_modes=("observation_only",),
        latency_class="offline",
        compute_class="heavy",
        reliability_class="low",
        wearable_fit="low",
        offline_fit="high",
        semantic_extension_fit=semantic_fit,
        health_signal_supported=False,
    )
    health = ProviderHealthGate(
        health_gate_ref=f"health_gate_{provider_ref}",
        provider_ref=provider_ref,
        required_health_signals=("source_freshness", "confidence"),
        degraded_conditions=("low_confidence", "stale_source"),
        blocked_conditions=(
            "runtime_scope_violation",
            "license_blocked",
            "candidate_only_violation",
        ),
        drift_policy="needs_more_observation",
        tracking_lost_policy="disable_provider",
        confidence_floor=0.4,
        degradation_output_policy="emit_health_only",
    )
    fallback = ProviderFallbackPolicy(
        fallback_policy_ref=fallback_ref,
        provider_ref=provider_ref,
        fallback_provider_refs=(),
        fallback_mode="disable_only",
        fallback_trigger_conditions=("runtime_scope_violation", "license_blocked"),
        fallback_output_policy="needs_more_observation",
        preserve_source_chain=True,
        preserve_conflict_refs=True,
    )
    admission = ProviderRuntimeAdmissionCandidate(
        admission_ref=f"provider_admission_{provider_ref}",
        provider_ref=provider_ref,
        backend_ref=backend_ref,
        adapter_ref=adapter_ref,
        admission_stage="observation_only",
        license_gate_passed=True,
        adapter_contract_passed=True,
        provider_policy_passed=True,
        capability_profile_passed=True,
        health_gate_passed=True,
        fallback_policy_passed=True,
        static_validation_passed=True,
        runtime_admission_allowed=False,
        admission_reasons=("observation_only_provider",),
        blocked_reasons=("observation_backend_no_runtime_admission",),
    )
    return policy, profile, health, fallback, admission


def build_provider_admission_policies_v1() -> Tuple[SpatialEvidenceProviderAdmissionPolicy, ...]:
    items = build_provider_admission_planning_catalog_v1()
    return tuple(items["admission_policies"])  # type: ignore[return-value]


def build_provider_planning_bundles_v1() -> Tuple[
    Tuple[
        SpatialEvidenceProviderAdmissionPolicy,
        ProviderCapabilityProfile,
        ProviderHealthGate,
        ProviderFallbackPolicy,
        ProviderRuntimeAdmissionCandidate,
    ],
    ...,
]:
    openvins = _tech_ref_policy(
        backend_ref="openvins",
        provider_ref="provider_openvins",
        adapter_ref="openvins_adapter",
        provider_role="pose_motion_provider",
        required_candidate_types=("PoseCandidate", "MotionCandidate", "SLAMHealthCandidate"),
        optional_candidate_types=(),
        disable_conditions=("tracking_lost", "high_drift", "license_blocked"),
        health_signals=("tracking_status", "confidence", "feature_quality", "imu_quality"),
    )
    vins = _tech_ref_policy(
        backend_ref="vins_fusion",
        provider_ref="provider_vins_fusion",
        adapter_ref="vins_fusion_adapter",
        provider_role="pose_motion_provider",
        required_candidate_types=("PoseCandidate", "MotionCandidate", "SLAMHealthCandidate"),
        optional_candidate_types=("RelocalizationCandidate",),
        disable_conditions=("tracking_lost", "high_drift", "license_blocked"),
        health_signals=("tracking_status", "confidence", "feature_quality", "imu_quality"),
    )
    orb = _tech_ref_policy(
        backend_ref="orb_slam3",
        provider_ref="provider_orb_slam3",
        adapter_ref="orb_slam3_adapter",
        provider_role="local_map_provider",
        required_candidate_types=(
            "PoseCandidate",
            "LocalMapCandidate",
            "RelocalizationCandidate",
            "SLAMHealthCandidate",
        ),
        optional_candidate_types=("SpatialAnchorCandidate",),
        disable_conditions=("tracking_lost", "high_drift", "license_blocked"),
        health_signals=("tracking_status", "drift_risk", "confidence", "mapping_quality"),
    )
    rtab_policy, rtab_profile, rtab_health, rtab_fallback, rtab_admission = _tech_ref_policy(
        backend_ref="rtab_map",
        provider_ref="provider_rtab_map",
        adapter_ref="rtab_map_adapter",
        provider_role="local_map_provider",
        required_candidate_types=(
            "LocalMapCandidate",
            "MapDriftCandidate",
            "RelocalizationCandidate",
        ),
        optional_candidate_types=("PoseCandidate", "SpatialAnchorCandidate"),
        disable_conditions=("mapping_unstable", "high_drift", "tracking_lost"),
        health_signals=("drift_risk", "mapping_quality", "relocalization_quality"),
    )
    rtab_admission = ProviderRuntimeAdmissionCandidate(
        admission_ref=rtab_admission.admission_ref,
        provider_ref=rtab_admission.provider_ref,
        backend_ref=rtab_admission.backend_ref,
        adapter_ref=rtab_admission.adapter_ref,
        admission_stage="technical_reference",
        license_gate_passed=False,
        adapter_contract_passed=True,
        provider_policy_passed=True,
        capability_profile_passed=True,
        health_gate_passed=True,
        fallback_policy_passed=True,
        static_validation_passed=True,
        runtime_admission_allowed=False,
        admission_reasons=("adapter_contract_planning_complete", "provider_admission_planning_only"),
        blocked_reasons=("license_gate_needs_legal_review", "planning_only_no_runtime_admission"),
    )
    rtab = (rtab_policy, rtab_profile, rtab_health, rtab_fallback, rtab_admission)

    kimera = _observation_bundle(
        backend_ref="kimera",
        provider_ref="provider_kimera",
        adapter_ref="kimera_adapter",
        provider_role="semantic_spatial_provider",
        required_candidate_types=("LocalMapCandidate", "SemanticFieldObjectCandidate"),
        optional_candidate_types=(
            "PoseCandidate",
            "SpatialAnchorCandidate",
            "MapDriftCandidate",
            "RelocalizationCandidate",
        ),
        semantic_fit="high",
    )
    hydra = _observation_bundle(
        backend_ref="hydra",
        provider_ref="provider_hydra",
        adapter_ref="hydra_adapter",
        provider_role="scene_graph_observation_provider",
        required_candidate_types=("FieldGraphCandidate", "SemanticMemoryMapCandidate"),
        optional_candidate_types=("SpatialAnchorCandidate",),
        semantic_fit="high",
    )
    grapheqa = _observation_bundle(
        backend_ref="grapheqa",
        provider_ref="provider_grapheqa",
        adapter_ref="grapheqa_adapter",
        provider_role="scene_graph_observation_provider",
        required_candidate_types=("FieldGraphCandidate", "SemanticMemoryMapCandidate"),
        optional_candidate_types=(),
        semantic_fit="medium",
    )
    grapheqa_admission = grapheqa[4]
    grapheqa_admission = ProviderRuntimeAdmissionCandidate(
        admission_ref=grapheqa_admission.admission_ref,
        provider_ref=grapheqa_admission.provider_ref,
        backend_ref=grapheqa_admission.backend_ref,
        adapter_ref=grapheqa_admission.adapter_ref,
        admission_stage="observation_only",
        license_gate_passed=False,
        adapter_contract_passed=True,
        provider_policy_passed=True,
        capability_profile_passed=True,
        health_gate_passed=True,
        fallback_policy_passed=True,
        static_validation_passed=True,
        runtime_admission_allowed=False,
        admission_reasons=("observation_only_provider",),
        blocked_reasons=(
            "observation_backend_no_runtime_admission",
            "unknown_license",
            "gpl_license_blocks_commercial_runtime",
        ),
    )
    grapheqa = (grapheqa[0], grapheqa[1], grapheqa[2], grapheqa[3], grapheqa_admission)

    return (openvins, vins, orb, rtab, kimera, hydra, grapheqa)


def get_provider_planning_bundle_v1(
    provider_ref: str,
) -> Tuple[
    SpatialEvidenceProviderAdmissionPolicy,
    ProviderCapabilityProfile,
    ProviderHealthGate,
    ProviderFallbackPolicy,
    ProviderRuntimeAdmissionCandidate,
]:
    for bundle in build_provider_planning_bundles_v1():
        if bundle[0].provider_ref == provider_ref:
            return bundle
    raise KeyError(f"unknown_provider_ref:{provider_ref}")


def build_provider_admission_planning_catalog_v1() -> Dict[str, object]:
    bundles = build_provider_planning_bundles_v1()
    policies = [b[0] for b in bundles]
    profiles = [b[1] for b in bundles]
    health_gates = [b[2] for b in bundles]
    fallbacks = [b[3] for b in bundles]
    admissions = [b[4] for b in bundles]

    provider_refs = tuple(p.provider_ref for p in policies)
    decision = ProviderAdmissionPlanningDecision(
        decision_ref="provider_admission_planning_decision_v1",
        planned_provider_refs=provider_refs,
        runtime_admission_candidates=(),
        commercial_runtime_candidates=(),
        blocked_runtime_providers=tuple(sorted(BLOCKED_RUNTIME_PROVIDER_REFS)),
        observation_only_providers=tuple(sorted(OBSERVATION_ONLY_PROVIDER_REFS)),
        fallback_required=True,
        health_gate_required=True,
        provider_replaceability_required=True,
        final_decision=FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    )

    return {
        "admission_policies": [candidate_to_dict(p) for p in policies],
        "capability_profiles": [candidate_to_dict(p) for p in profiles],
        "health_gates": [candidate_to_dict(h) for h in health_gates],
        "fallback_policies": [candidate_to_dict(f) for f in fallbacks],
        "runtime_admission_candidates": [candidate_to_dict(a) for a in admissions],
        "disable_decisions": [],
        "decision": candidate_to_dict(decision),
    }


def build_provider_admission_planning_matrix_v1() -> Dict[str, object]:
    return build_provider_admission_planning_catalog_v1()
