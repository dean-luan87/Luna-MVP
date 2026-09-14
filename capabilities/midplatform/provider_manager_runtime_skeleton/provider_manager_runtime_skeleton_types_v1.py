# -*- coding: utf-8 -*-
"""Provider Manager Runtime Skeleton — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001"
SCOPE = "provider_manager_runtime_skeleton_planning_only"
SOURCE_CHAIN = "provider_manager_runtime_skeleton_v1"

RUNTIME_SKELETON_PRINCIPLE_EN = (
    "Provider Manager Runtime Skeleton defines runtime control structure, "
    "not runtime execution."
)
RUNTIME_SKELETON_PRINCIPLE_ZH = (
    "Provider Manager Runtime Skeleton 定义运行时控制结构，不代表运行时已执行。"
)

INHERITED_ADMISSION_PRINCIPLE_ZH = "能翻译，不等于能启用。"
INHERITED_MANAGER_PRINCIPLE_ZH = "能准入规划，不等于能 runtime enable。"
INHERITED_SKELETON_PRINCIPLE_ZH = "能定义 runtime skeleton，不等于能 runtime execute。"

SHARED_GOVERNANCE_SOURCE_REF = "provider_runtime_governance_registry_v1"
RUNTIME_SKELETON_REF = "provider_manager_runtime_skeleton_v1"
MIDPLATFORM_SYNTHESIS_ENTRYPOINT = "midplatform_synthesis_v1"
FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"

FINAL_DECISION_READY_FOR_DRYRUN_CASES = (
    "PROVIDER_MANAGER_RUNTIME_SKELETON_PLANNING_READY_FOR_DRYRUN_CASES"
)
FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER = (
    "PROVIDER_MANAGER_RUNTIME_SKELETON_DRYRUN_CASES_READY_FOR_RUNNER"
)
FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER = (
    "PROVIDER_MANAGER_RUNTIME_SKELETON_DRYRUN_TRACE_READY_FOR_VERIFIER"
)
FINAL_DECISION_DRYRUN_RUNNER_UNEXPECTED_OUTCOME = (
    "PROVIDER_MANAGER_RUNTIME_SKELETON_DRYRUN_RUNNER_UNEXPECTED_OUTCOME"
)
FINAL_DECISION_DRYRUN_VERIFIER_GO = (
    "PROVIDER_MANAGER_RUNTIME_SKELETON_DRYRUN_VERIFIER_GO"
)
FINAL_DECISION_DRYRUN_VERIFIER_BLOCKED = (
    "PROVIDER_MANAGER_RUNTIME_SKELETON_DRYRUN_VERIFIER_BLOCKED"
)
FINAL_DECISION_POST_DRYRUN_REVIEW_GO = (
    "PROVIDER_MANAGER_RUNTIME_SKELETON_POST_DRYRUN_REVIEW_GO"
)
FINAL_DECISION_POST_DRYRUN_REVIEW_BLOCKED = (
    "PROVIDER_MANAGER_RUNTIME_SKELETON_POST_DRYRUN_REVIEW_BLOCKED"
)

DOMAIN_SHARED = "shared"
DOMAIN_SPATIAL_EVIDENCE = "spatial_evidence"
DOMAIN_VISION_OCR = "vision_ocr"

SUPPORTED_DOMAIN_IDS: Tuple[str, ...] = (
    DOMAIN_SHARED,
    DOMAIN_SPATIAL_EVIDENCE,
    DOMAIN_VISION_OCR,
)

ACTIVATION_GATE_REQUIRED_CHECKS: Tuple[str, ...] = (
    "license_gate",
    "adapter_contract_gate",
    "provider_admission_gate",
    "health_gate",
    "fallback_gate",
    "owner_approval_gate",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "architecture_definition_only": True,
    "no_runtime_execution": True,
    "no_provider_activation": True,
    "no_fallback_execution": True,
    "no_output_dispatch": True,
    "no_real_provider_connected": True,
    "no_provider_manager_runtime": True,
    "no_camera_runtime": True,
    "no_ros_runtime": True,
    "no_commercial_runtime_selection": True,
}

PROVIDER_MANAGER_RUNTIME_SKELETON_FIELDS: Tuple[str, ...] = (
    "skeleton_ref",
    "domain_id",
    "skeleton_status",
    "shared_governance_source_ref",
    "domain_profile_refs",
    "synthesis_entrypoints",
    "managed_domain_ids",
    "managed_provider_refs",
    "runtime_execution_allowed",
    "provider_activation_allowed",
    "real_provider_connected",
    "candidate_only",
)

RUNTIME_PROVIDER_REGISTRY_FIELDS: Tuple[str, ...] = (
    "registry_ref",
    "domain_id",
    "domain_profile_ref",
    "shared_governance_source_ref",
    "provider_refs",
    "supported_output_candidate_types",
    "registration_status",
    "runtime_execution_allowed",
    "provider_activation_allowed",
    "real_provider_connected",
    "candidate_only",
)

PROVIDER_ACTIVATION_GATE_FIELDS: Tuple[str, ...] = (
    "gate_ref",
    "domain_id",
    "provider_ref",
    "domain_profile_ref",
    "shared_governance_source_ref",
    "required_gates",
    "gates_passed",
    "all_gates_passed",
    "provider_activation_allowed",
    "activation_decision_candidate",
    "runtime_execution_allowed",
    "candidate_only",
)

PROVIDER_RUNTIME_HEALTH_LOOP_FIELDS: Tuple[str, ...] = (
    "health_loop_ref",
    "domain_id",
    "provider_ref",
    "loop_status",
    "monitored_signals",
    "health_decision_candidate",
    "runtime_disable_executed",
    "direct_runtime_disable_allowed",
    "runtime_execution_allowed",
    "candidate_only",
)

PROVIDER_FALLBACK_EXECUTOR_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "fallback_executor_ref",
    "domain_id",
    "provider_ref",
    "fallback_mode",
    "fallback_provider_refs",
    "preserve_source_chain",
    "preserve_conflict_refs",
    "fallback_execution_allowed",
    "fallback_executed",
    "runtime_execution_allowed",
    "candidate_only",
)

PROVIDER_OUTPUT_DISPATCH_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "dispatch_ref",
    "domain_id",
    "provider_ref",
    "synthesis_entrypoint",
    "output_candidate_types",
    "output_dispatch_allowed",
    "direct_action_allowed",
    "direct_speech_allowed",
    "direct_fact_write_allowed",
    "runtime_execution_allowed",
    "candidate_only",
)

PROVIDER_RUNTIME_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "domain_id",
    "provider_ref",
    "decision_type",
    "decision_status",
    "runtime_execution_allowed",
    "provider_activation_allowed",
    "fallback_execution_allowed",
    "output_dispatch_allowed",
    "decision_candidate_ref",
    "candidate_only",
)

PROVIDER_RUNTIME_SKELETON_PLANNING_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "skeleton_ref",
    "shared_governance_source_ref",
    "domain_profile_refs",
    "runtime_execution_allowed",
    "provider_activation_allowed",
    "fallback_execution_allowed",
    "output_dispatch_allowed",
    "real_provider_connected",
    "final_decision",
    "candidate_only",
)


@dataclass(frozen=True)
class ProviderManagerRuntimeSkeleton:
    skeleton_ref: str
    domain_id: str
    skeleton_status: str
    shared_governance_source_ref: str
    domain_profile_refs: Tuple[str, ...]
    synthesis_entrypoints: Tuple[str, ...]
    managed_domain_ids: Tuple[str, ...]
    managed_provider_refs: Tuple[str, ...]
    runtime_execution_allowed: bool
    provider_activation_allowed: bool
    real_provider_connected: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class RuntimeProviderRegistry:
    registry_ref: str
    domain_id: str
    domain_profile_ref: str
    shared_governance_source_ref: str
    provider_refs: Tuple[str, ...]
    supported_output_candidate_types: Tuple[str, ...]
    registration_status: str
    runtime_execution_allowed: bool
    provider_activation_allowed: bool
    real_provider_connected: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderActivationGate:
    gate_ref: str
    domain_id: str
    provider_ref: str
    domain_profile_ref: str
    shared_governance_source_ref: str
    required_gates: Tuple[str, ...]
    gates_passed: Tuple[str, ...]
    all_gates_passed: bool
    provider_activation_allowed: bool
    activation_decision_candidate: str
    runtime_execution_allowed: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderRuntimeHealthLoop:
    health_loop_ref: str
    domain_id: str
    provider_ref: str
    loop_status: str
    monitored_signals: Tuple[str, ...]
    health_decision_candidate: str
    runtime_disable_executed: bool
    direct_runtime_disable_allowed: bool
    runtime_execution_allowed: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderFallbackExecutorCandidate:
    fallback_executor_ref: str
    domain_id: str
    provider_ref: str
    fallback_mode: str
    fallback_provider_refs: Tuple[str, ...]
    preserve_source_chain: bool
    preserve_conflict_refs: bool
    fallback_execution_allowed: bool
    fallback_executed: bool
    runtime_execution_allowed: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderOutputDispatchCandidate:
    dispatch_ref: str
    domain_id: str
    provider_ref: str
    synthesis_entrypoint: str
    output_candidate_types: Tuple[str, ...]
    output_dispatch_allowed: bool
    direct_action_allowed: bool
    direct_speech_allowed: bool
    direct_fact_write_allowed: bool
    runtime_execution_allowed: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderRuntimeDecision:
    decision_ref: str
    domain_id: str
    provider_ref: str
    decision_type: str
    decision_status: str
    runtime_execution_allowed: bool
    provider_activation_allowed: bool
    fallback_execution_allowed: bool
    output_dispatch_allowed: bool
    decision_candidate_ref: str
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderRuntimeSkeletonPlanningDecision:
    decision_ref: str
    skeleton_ref: str
    shared_governance_source_ref: str
    domain_profile_refs: Tuple[str, ...]
    runtime_execution_allowed: bool
    provider_activation_allowed: bool
    fallback_execution_allowed: bool
    output_dispatch_allowed: bool
    real_provider_connected: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
