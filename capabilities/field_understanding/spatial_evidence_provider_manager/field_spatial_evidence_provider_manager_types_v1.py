# -*- coding: utf-8 -*-
"""Field Spatial Evidence Provider Manager Skeleton Planning — types v1.

SUPERSEDED_BY_SHARED_PROVIDER_RUNTIME_GOVERNANCE:
Use capabilities/midplatform/provider_runtime_governance/ instead.
This module remains as a reference only; do not extend independently.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Field-Spatial-Evidence-Provider-Manager-Skeleton-Planning-v1-001"
SCOPE = "spatial_evidence_provider_manager_skeleton_planning_only"
SOURCE_CHAIN = "spatial_evidence_provider_manager_v1"

MANAGER_PRINCIPLE_EN = (
    "Provider Manager Skeleton defines runtime governance shape, not runtime activation."
)
MANAGER_PRINCIPLE_ZH = "Provider Manager Skeleton 定义运行时治理形态，不代表运行时已启用。"

INHERITED_ADMISSION_PRINCIPLE_ZH = "能翻译，不等于能启用。"
INHERITED_MANAGER_PRINCIPLE_ZH = "能准入规划，不等于能 runtime enable。"

FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
MANAGER_REF = "spatial_evidence_provider_manager_v1"

FINAL_DECISION_READY_FOR_DRYRUN_CASES = (
    "FIELD_SPATIAL_EVIDENCE_PROVIDER_MANAGER_SKELETON_PLANNING_READY_FOR_DRYRUN_CASES"
)

SPATIAL_EVIDENCE_PROVIDER_MANAGER_FIELDS: Tuple[str, ...] = (
    "manager_ref",
    "manager_status",
    "managed_provider_refs",
    "default_enabled_provider_refs",
    "default_disabled_provider_refs",
    "field_synthesis_entrypoint",
    "runtime_activation_allowed",
    "provider_runtime_enabled",
    "candidate_only",
)

PROVIDER_REGISTRY_ENTRY_FIELDS: Tuple[str, ...] = (
    "registry_entry_ref",
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
    "supported_candidate_types",
    "candidate_only",
)

PROVIDER_ENABLE_REQUEST_FIELDS: Tuple[str, ...] = (
    "enable_request_ref",
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
    "provider_ref",
    "tracking_status",
    "drift_risk",
    "confidence",
    "source_freshness",
    "health_decision",
    "degradation_required",
    "disable_required",
    "candidate_only",
)

PROVIDER_FALLBACK_ROUTE_FIELDS: Tuple[str, ...] = (
    "fallback_route_ref",
    "provider_ref",
    "fallback_provider_refs",
    "fallback_mode",
    "trigger_conditions",
    "preserve_source_chain",
    "preserve_conflict_refs",
    "candidate_only",
)

PROVIDER_MANAGER_PLANNING_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "manager_ref",
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

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "architecture_definition_only": True,
    "no_runtime_activation": True,
    "no_provider_runtime_enabled": True,
    "no_real_provider_runtime": True,
    "no_real_slam_backend": True,
    "no_camera_runtime": True,
    "no_ros_runtime": True,
    "no_benchmark_runtime": True,
    "no_commercial_runtime_selection": True,
    "no_provider_manager_runtime": True,
    "no_provider_scheduling": True,
    "no_real_spatial_evidence_output": True,
    "no_speech_output": True,
    "no_navigation_output": True,
    "no_fact_layer_write": True,
}


@dataclass(frozen=True)
class SpatialEvidenceProviderManager:
    manager_ref: str
    manager_status: str
    managed_provider_refs: Tuple[str, ...]
    default_enabled_provider_refs: Tuple[str, ...]
    default_disabled_provider_refs: Tuple[str, ...]
    field_synthesis_entrypoint: str
    runtime_activation_allowed: bool
    provider_runtime_enabled: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderRegistryEntry:
    registry_entry_ref: str
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
    supported_candidate_types: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderEnableRequest:
    enable_request_ref: str
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
    provider_ref: str
    tracking_status: str
    drift_risk: str
    confidence: float
    source_freshness: str
    health_decision: str
    degradation_required: bool
    disable_required: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderFallbackRoute:
    fallback_route_ref: str
    provider_ref: str
    fallback_provider_refs: Tuple[str, ...]
    fallback_mode: str
    trigger_conditions: Tuple[str, ...]
    preserve_source_chain: bool
    preserve_conflict_refs: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ProviderManagerPlanningDecision:
    decision_ref: str
    manager_ref: str
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


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
