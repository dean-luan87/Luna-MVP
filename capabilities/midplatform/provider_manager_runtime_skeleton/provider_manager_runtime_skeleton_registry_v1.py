# -*- coding: utf-8 -*-
"""Provider Manager Runtime Skeleton — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.provider_runtime_governance.domain_profiles.spatial_evidence_provider_governance_profile_v1 import (
    build_spatial_evidence_provider_governance_profile_v1,
)
from capabilities.midplatform.provider_runtime_governance.domain_profiles.vision_ocr_governance_compatibility_v1 import (
    build_vision_ocr_combined_governance_profile_v1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
)
from capabilities.midplatform.provider_manager_runtime_skeleton.provider_manager_runtime_skeleton_types_v1 import (
    ACTIVATION_GATE_REQUIRED_CHECKS,
    DOMAIN_SHARED,
    DOMAIN_SPATIAL_EVIDENCE,
    DOMAIN_VISION_OCR,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    RUNTIME_SKELETON_REF,
    SHARED_GOVERNANCE_SOURCE_REF,
    SUPPORTED_DOMAIN_IDS,
    ProviderActivationGate,
    ProviderFallbackExecutorCandidate,
    ProviderManagerRuntimeSkeleton,
    ProviderOutputDispatchCandidate,
    ProviderRuntimeDecision,
    ProviderRuntimeHealthLoop,
    ProviderRuntimeSkeletonPlanningDecision,
    RuntimeProviderRegistry,
    candidate_to_dict,
)

REGISTRY_ID = "provider_manager_runtime_skeleton_registry_v1"

SKELETON_STATUSES: Tuple[str, ...] = (
    "planning",
    "dryrun_ready",
    "runtime_skeleton_ready",
    "blocked",
)

REGISTRATION_STATUSES: Tuple[str, ...] = (
    "registered_candidate",
    "admission_planned",
    "runtime_blocked",
    "disabled",
)

LOOP_STATUSES: Tuple[str, ...] = (
    "monitoring_candidate",
    "degraded_candidate",
    "blocked_candidate",
    "disabled",
)

HEALTH_DECISION_CANDIDATES: Tuple[str, ...] = (
    "allow_candidate_output",
    "degrade_candidate_output",
    "disable_provider_candidate",
    "request_more_observation_candidate",
    "block_runtime_candidate",
)

ACTIVATION_DECISION_CANDIDATES: Tuple[str, ...] = (
    "activation_blocked_pending_gates",
    "activation_blocked_owner_approval",
    "activation_candidate_only",
    "activation_not_allowed_in_planning",
)

FALLBACK_MODES: Tuple[str, ...] = (
    "none",
    "disable_only",
    "switch_to_mock",
    "switch_to_lower_capability_provider",
    "request_more_observation",
    "user_confirmation_required",
)

DECISION_TYPES: Tuple[str, ...] = (
    "activation_candidate",
    "health_candidate",
    "fallback_candidate",
    "dispatch_candidate",
    "composite_runtime_candidate",
)

DECISION_STATUSES: Tuple[str, ...] = (
    "planned",
    "candidate_only",
    "blocked",
    "pending_approval",
)

SYNTHESIS_ENTRYPOINTS: Tuple[str, ...] = (
    FIELD_SYNTHESIS_ENTRYPOINT,
    MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
)

FORBIDDEN_RUNTIME_SKELETON_POLICIES: Tuple[str, ...] = (
    "runtime_execute_without_activation_gate",
    "runtime_activate_without_owner_approval",
    "runtime_activate_without_admission",
    "runtime_fallback_without_source_chain",
    "runtime_bypass_domain_profile",
    "runtime_bypass_shared_governance",
    "runtime_direct_action",
    "runtime_direct_speech",
    "runtime_direct_fact_write",
    "runtime_enable_commercial_without_gate",
    "runtime_cross_domain_candidate_pollution",
    "runtime_domain_specific_manager_duplication",
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "skeleton_statuses": SKELETON_STATUSES,
    "registration_statuses": REGISTRATION_STATUSES,
    "loop_statuses": LOOP_STATUSES,
    "health_decision_candidates": HEALTH_DECISION_CANDIDATES,
    "activation_decision_candidates": ACTIVATION_DECISION_CANDIDATES,
    "fallback_modes": FALLBACK_MODES,
    "decision_types": DECISION_TYPES,
    "decision_statuses": DECISION_STATUSES,
    "synthesis_entrypoints": SYNTHESIS_ENTRYPOINTS,
    "supported_domain_ids": SUPPORTED_DOMAIN_IDS,
    "activation_gate_required_checks": ACTIVATION_GATE_REQUIRED_CHECKS,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for domain, values in REGISTRY.items():
        if not values:
            issues.append(f"registry_domain_missing:{domain}")
    if len(ACTIVATION_GATE_REQUIRED_CHECKS) < 6:
        issues.append("activation_gate_required_checks_incomplete")
    if len(FORBIDDEN_RUNTIME_SKELETON_POLICIES) < 12:
        issues.append("forbidden_runtime_skeleton_policies_incomplete")
    return len(issues) == 0, issues


def _activation_gate(
    *,
    provider_ref: str,
    domain_id: str,
    domain_profile_ref: str,
    gates_passed: Tuple[str, ...],
) -> ProviderActivationGate:
    all_passed = set(gates_passed) >= set(ACTIVATION_GATE_REQUIRED_CHECKS)
    return ProviderActivationGate(
        gate_ref=f"activation_gate_{domain_id}_{provider_ref}",
        domain_id=domain_id,
        provider_ref=provider_ref,
        domain_profile_ref=domain_profile_ref,
        shared_governance_source_ref=SHARED_GOVERNANCE_SOURCE_REF,
        required_gates=ACTIVATION_GATE_REQUIRED_CHECKS,
        gates_passed=gates_passed,
        all_gates_passed=all_passed,
        provider_activation_allowed=False,
        activation_decision_candidate=(
            "activation_not_allowed_in_planning"
            if all_passed
            else "activation_blocked_pending_gates"
        ),
        runtime_execution_allowed=False,
    )


def _health_loop(*, provider_ref: str, domain_id: str) -> ProviderRuntimeHealthLoop:
    return ProviderRuntimeHealthLoop(
        health_loop_ref=f"health_loop_{domain_id}_{provider_ref}",
        domain_id=domain_id,
        provider_ref=provider_ref,
        loop_status="monitoring_candidate",
        monitored_signals=("tracking_status", "confidence", "source_freshness"),
        health_decision_candidate="allow_candidate_output",
        runtime_disable_executed=False,
        direct_runtime_disable_allowed=False,
        runtime_execution_allowed=False,
    )


def _fallback_executor(
    *,
    provider_ref: str,
    domain_id: str,
    fallback_provider_refs: Tuple[str, ...],
) -> ProviderFallbackExecutorCandidate:
    return ProviderFallbackExecutorCandidate(
        fallback_executor_ref=f"fallback_executor_{domain_id}_{provider_ref}",
        domain_id=domain_id,
        provider_ref=provider_ref,
        fallback_mode="switch_to_mock",
        fallback_provider_refs=fallback_provider_refs,
        preserve_source_chain=True,
        preserve_conflict_refs=True,
        fallback_execution_allowed=False,
        fallback_executed=False,
        runtime_execution_allowed=False,
    )


def _output_dispatch(
    *,
    provider_ref: str,
    domain_id: str,
    synthesis_entrypoint: str,
    output_candidate_types: Tuple[str, ...],
) -> ProviderOutputDispatchCandidate:
    return ProviderOutputDispatchCandidate(
        dispatch_ref=f"output_dispatch_{domain_id}_{provider_ref}",
        domain_id=domain_id,
        provider_ref=provider_ref,
        synthesis_entrypoint=synthesis_entrypoint,
        output_candidate_types=output_candidate_types,
        output_dispatch_allowed=False,
        direct_action_allowed=False,
        direct_speech_allowed=False,
        direct_fact_write_allowed=False,
        runtime_execution_allowed=False,
    )


def _runtime_decision(
    *,
    provider_ref: str,
    domain_id: str,
    decision_type: str,
    decision_candidate_ref: str,
) -> ProviderRuntimeDecision:
    return ProviderRuntimeDecision(
        decision_ref=f"runtime_decision_{domain_id}_{provider_ref}_{decision_type}",
        domain_id=domain_id,
        provider_ref=provider_ref,
        decision_type=decision_type,
        decision_status="candidate_only",
        runtime_execution_allowed=False,
        provider_activation_allowed=False,
        fallback_execution_allowed=False,
        output_dispatch_allowed=False,
        decision_candidate_ref=decision_candidate_ref,
    )


def build_provider_manager_runtime_skeleton_matrix_v1() -> Dict[str, Any]:
    spatial_profile = build_spatial_evidence_provider_governance_profile_v1()
    vision_profile = build_vision_ocr_combined_governance_profile_v1()

    spatial_provider = spatial_profile.provider_refs[0]
    vision_provider = vision_profile["provider_refs"][0]
    ocr_provider = vision_profile["provider_refs"][1]

    managed_provider_refs = (
        spatial_provider,
        vision_provider,
        ocr_provider,
    )

    skeleton = ProviderManagerRuntimeSkeleton(
        skeleton_ref=RUNTIME_SKELETON_REF,
        domain_id=DOMAIN_SHARED,
        skeleton_status="planning",
        shared_governance_source_ref=SHARED_GOVERNANCE_SOURCE_REF,
        domain_profile_refs=(
            spatial_profile.profile_ref,
            vision_profile["profile_ref"],
        ),
        synthesis_entrypoints=(FIELD_SYNTHESIS_ENTRYPOINT, MIDPLATFORM_SYNTHESIS_ENTRYPOINT),
        managed_domain_ids=(DOMAIN_SPATIAL_EVIDENCE, DOMAIN_VISION_OCR),
        managed_provider_refs=managed_provider_refs,
        runtime_execution_allowed=False,
        provider_activation_allowed=False,
        real_provider_connected=False,
    )

    spatial_registry = RuntimeProviderRegistry(
        registry_ref=f"runtime_provider_registry_{DOMAIN_SPATIAL_EVIDENCE}",
        domain_id=DOMAIN_SPATIAL_EVIDENCE,
        domain_profile_ref=spatial_profile.profile_ref,
        shared_governance_source_ref=SHARED_GOVERNANCE_SOURCE_REF,
        provider_refs=spatial_profile.provider_refs,
        supported_output_candidate_types=spatial_profile.supported_output_candidate_types,
        registration_status="registered_candidate",
        runtime_execution_allowed=False,
        provider_activation_allowed=False,
        real_provider_connected=False,
    )

    vision_registry = RuntimeProviderRegistry(
        registry_ref=f"runtime_provider_registry_{DOMAIN_VISION_OCR}",
        domain_id=DOMAIN_VISION_OCR,
        domain_profile_ref=vision_profile["profile_ref"],
        shared_governance_source_ref=SHARED_GOVERNANCE_SOURCE_REF,
        provider_refs=tuple(vision_profile["provider_refs"]),
        supported_output_candidate_types=tuple(
            vision_profile["supported_output_candidate_types"]
        ),
        registration_status="registered_candidate",
        runtime_execution_allowed=False,
        provider_activation_allowed=False,
        real_provider_connected=False,
    )

    spatial_gate_passed = (
        "license_gate",
        "adapter_contract_gate",
        "provider_admission_gate",
        "health_gate",
        "fallback_gate",
    )
    vision_gate_passed = (
        "license_gate",
        "adapter_contract_gate",
        "provider_admission_gate",
        "health_gate",
    )

    activation_gates = (
        _activation_gate(
            provider_ref=spatial_provider,
            domain_id=DOMAIN_SPATIAL_EVIDENCE,
            domain_profile_ref=spatial_profile.profile_ref,
            gates_passed=spatial_gate_passed,
        ),
        _activation_gate(
            provider_ref=vision_provider,
            domain_id=DOMAIN_VISION_OCR,
            domain_profile_ref=vision_profile["profile_ref"],
            gates_passed=vision_gate_passed,
        ),
        _activation_gate(
            provider_ref=ocr_provider,
            domain_id=DOMAIN_VISION_OCR,
            domain_profile_ref=vision_profile["profile_ref"],
            gates_passed=("license_gate", "adapter_contract_gate"),
        ),
    )

    health_loops = (
        _health_loop(provider_ref=spatial_provider, domain_id=DOMAIN_SPATIAL_EVIDENCE),
        _health_loop(provider_ref=vision_provider, domain_id=DOMAIN_VISION_OCR),
        _health_loop(provider_ref=ocr_provider, domain_id=DOMAIN_VISION_OCR),
    )

    fallback_executors = (
        _fallback_executor(
            provider_ref=spatial_provider,
            domain_id=DOMAIN_SPATIAL_EVIDENCE,
            fallback_provider_refs=("provider_vins_fusion",),
        ),
        _fallback_executor(
            provider_ref=vision_provider,
            domain_id=DOMAIN_VISION_OCR,
            fallback_provider_refs=("vision_provider_mock_fixture",),
        ),
        _fallback_executor(
            provider_ref=ocr_provider,
            domain_id=DOMAIN_VISION_OCR,
            fallback_provider_refs=("ocr_provider_mock_fixture",),
        ),
    )

    output_dispatches = (
        _output_dispatch(
            provider_ref=spatial_provider,
            domain_id=DOMAIN_SPATIAL_EVIDENCE,
            synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
            output_candidate_types=("PoseCandidate", "SLAMHealthCandidate"),
        ),
        _output_dispatch(
            provider_ref=vision_provider,
            domain_id=DOMAIN_VISION_OCR,
            synthesis_entrypoint=MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
            output_candidate_types=("DetectionCandidate", "TrackingCandidate"),
        ),
        _output_dispatch(
            provider_ref=ocr_provider,
            domain_id=DOMAIN_VISION_OCR,
            synthesis_entrypoint=MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
            output_candidate_types=("ocr_result_candidate", "roi_candidate"),
        ),
    )

    runtime_decisions = (
        _runtime_decision(
            provider_ref=spatial_provider,
            domain_id=DOMAIN_SPATIAL_EVIDENCE,
            decision_type="composite_runtime_candidate",
            decision_candidate_ref=activation_gates[0].gate_ref,
        ),
        _runtime_decision(
            provider_ref=vision_provider,
            domain_id=DOMAIN_VISION_OCR,
            decision_type="composite_runtime_candidate",
            decision_candidate_ref=activation_gates[1].gate_ref,
        ),
    )

    planning_decision = ProviderRuntimeSkeletonPlanningDecision(
        decision_ref="provider_runtime_skeleton_planning_decision_v1",
        skeleton_ref=RUNTIME_SKELETON_REF,
        shared_governance_source_ref=SHARED_GOVERNANCE_SOURCE_REF,
        domain_profile_refs=(
            spatial_profile.profile_ref,
            vision_profile["profile_ref"],
        ),
        runtime_execution_allowed=False,
        provider_activation_allowed=False,
        fallback_execution_allowed=False,
        output_dispatch_allowed=False,
        real_provider_connected=False,
        final_decision=FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    )

    return {
        "registry_id": REGISTRY_ID,
        "runtime_skeleton": candidate_to_dict(skeleton),
        "runtime_registries": [
            candidate_to_dict(spatial_registry),
            candidate_to_dict(vision_registry),
        ],
        "activation_gates": [candidate_to_dict(g) for g in activation_gates],
        "health_loops": [candidate_to_dict(h) for h in health_loops],
        "fallback_executor_candidates": [
            candidate_to_dict(f) for f in fallback_executors
        ],
        "output_dispatch_candidates": [
            candidate_to_dict(d) for d in output_dispatches
        ],
        "runtime_decisions": [candidate_to_dict(d) for d in runtime_decisions],
        "planning_decision": candidate_to_dict(planning_decision),
        "domain_profiles": {
            DOMAIN_SPATIAL_EVIDENCE: {
                "profile_ref": spatial_profile.profile_ref,
                "synthesis_entrypoint": spatial_profile.synthesis_entrypoint,
                "provider_refs": list(spatial_profile.provider_refs),
                "supported_output_candidate_types": list(
                    spatial_profile.supported_output_candidate_types
                ),
            },
            DOMAIN_VISION_OCR: {
                "profile_ref": vision_profile["profile_ref"],
                "synthesis_entrypoint": vision_profile["synthesis_entrypoint"],
                "provider_refs": list(vision_profile["provider_refs"]),
                "supported_output_candidate_types": list(
                    vision_profile["supported_output_candidate_types"]
                ),
            },
        },
        "control_chain": [
            "DomainProfile",
            "RuntimeProviderRegistry",
            "ProviderActivationGate",
            "ProviderRuntimeHealthLoop",
            "ProviderFallbackExecutorCandidate",
            "ProviderOutputDispatchCandidate",
            "ProviderRuntimeDecision",
            "Candidate Output / Synthesis",
        ],
    }
