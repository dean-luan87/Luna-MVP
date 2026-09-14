# -*- coding: utf-8 -*-
"""Field SLAM Adapter Contract Planning — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Field-SLAM-Adapter-Contract-Planning-v1-001"
SCOPE = "field_slam_adapter_contract_planning_only"
SOURCE_CHAIN = "field_slam_adapter_contract_v1"

ADAPTER_CONTRACT_PRINCIPLE_EN = (
    "Any SLAM/VIO/SceneGraph backend must be adapted into Luna standard spatial evidence "
    "candidates before entering Field Synthesis."
)
ADAPTER_CONTRACT_PRINCIPLE_ZH = (
    "任何 SLAM/VIO/SceneGraph 后端必须先被适配成 Luna 标准空间证据候选，才能进入 Field Synthesis。"
)

GENERIC_SLAM_ADAPTER_CONTRACT_ID = "generic_slam_adapter_contract_v1"
FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
SPATIAL_EVIDENCE_PROVIDER_ROLE = "SpatialEvidenceProvider"

FINAL_DECISION_READY_FOR_DRYRUN_CASES = (
    "FIELD_SLAM_ADAPTER_CONTRACT_PLANNING_READY_FOR_DRYRUN_CASES"
)

GENERIC_SLAM_ADAPTER_CONTRACT_FIELDS: Tuple[str, ...] = (
    "adapter_ref",
    "backend_ref",
    "backend_name",
    "backend_role",
    "supported_input_modes",
    "supported_output_candidates",
    "required_output_candidates",
    "field_synthesis_entrypoint",
    "license_gate_ref",
    "runtime_isolation_ref",
    "adapter_status",
    "candidate_only",
)

SLAM_BACKEND_OUTPUT_MAPPING_FIELDS: Tuple[str, ...] = (
    "mapping_ref",
    "adapter_ref",
    "backend_ref",
    "backend_output_name",
    "luna_candidate_type",
    "mapping_status",
    "confidence_policy",
    "degradation_policy",
    "source_refs_required",
    "candidate_only_enforced",
    "candidate_only",
)

LICENSE_GATE_POLICY_FIELDS: Tuple[str, ...] = (
    "license_gate_ref",
    "backend_ref",
    "license_type",
    "license_risk",
    "commercial_runtime_allowed",
    "technical_reference_allowed",
    "required_actions",
    "blocked_usage_modes",
    "review_status",
    "candidate_only",
)

RUNTIME_ISOLATION_POLICY_FIELDS: Tuple[str, ...] = (
    "isolation_ref",
    "backend_ref",
    "isolation_mode",
    "data_exchange_mode",
    "process_boundary_required",
    "source_code_contamination_risk",
    "runtime_dependency_risk",
    "allowed_for_internal_dev",
    "allowed_for_commercial_runtime",
    "candidate_only",
)

BACKEND_ADMISSION_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "admission_ref",
    "backend_ref",
    "adapter_ref",
    "admission_stage",
    "license_gate_passed",
    "adapter_contract_passed",
    "output_mapping_passed",
    "static_validation_passed",
    "dryrun_required",
    "runtime_admission_allowed",
    "blocked_reasons",
    "candidate_only",
)

SPATIAL_EVIDENCE_PROVIDER_REGISTRATION_FIELDS: Tuple[str, ...] = (
    "provider_ref",
    "backend_ref",
    "adapter_ref",
    "provider_role",
    "enabled_by_default",
    "fallback_provider_refs",
    "supported_candidate_types",
    "health_signal_required",
    "disable_policy",
    "candidate_only",
)

ADAPTER_PLANNING_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "planned_adapters",
    "technical_reference_backends",
    "commercial_runtime_backends",
    "blocked_runtime_backends",
    "observation_backends",
    "license_gate_required",
    "runtime_isolation_required",
    "output_mapping_required",
    "dryrun_required_next",
    "final_decision",
    "candidate_only",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "architecture_definition_only": True,
    "no_camera_runtime": True,
    "no_model_execution": True,
    "no_slam_execution": True,
    "no_slam_framework_binding": True,
    "no_real_adapter_runtime": True,
    "no_runtime_admission": True,
    "no_commercial_runtime": True,
    "no_ros_runtime": True,
    "no_benchmark_runtime": True,
    "no_speech_output": True,
    "no_navigation_output": True,
    "no_fact_layer_write": True,
    "no_world_model_entry_write": True,
    "no_long_term_map_write": True,
}


@dataclass(frozen=True)
class GenericSLAMAdapterContract:
    adapter_ref: str
    backend_ref: str
    backend_name: str
    backend_role: str
    supported_input_modes: Tuple[str, ...]
    supported_output_candidates: Tuple[str, ...]
    required_output_candidates: Tuple[str, ...]
    field_synthesis_entrypoint: str
    license_gate_ref: str
    runtime_isolation_ref: str
    adapter_status: str
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMBackendOutputMapping:
    mapping_ref: str
    adapter_ref: str
    backend_ref: str
    backend_output_name: str
    luna_candidate_type: str
    mapping_status: str
    confidence_policy: str
    degradation_policy: str
    source_refs_required: bool
    candidate_only_enforced: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class LicenseGatePolicy:
    license_gate_ref: str
    backend_ref: str
    license_type: str
    license_risk: str
    commercial_runtime_allowed: bool
    technical_reference_allowed: bool
    required_actions: Tuple[str, ...]
    blocked_usage_modes: Tuple[str, ...]
    review_status: str
    candidate_only: bool = True


@dataclass(frozen=True)
class RuntimeIsolationPolicy:
    isolation_ref: str
    backend_ref: str
    isolation_mode: str
    data_exchange_mode: str
    process_boundary_required: bool
    source_code_contamination_risk: str
    runtime_dependency_risk: str
    allowed_for_internal_dev: bool
    allowed_for_commercial_runtime: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class BackendAdmissionCandidate:
    admission_ref: str
    backend_ref: str
    adapter_ref: str
    admission_stage: str
    license_gate_passed: bool
    adapter_contract_passed: bool
    output_mapping_passed: bool
    static_validation_passed: bool
    dryrun_required: bool
    runtime_admission_allowed: bool
    blocked_reasons: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SpatialEvidenceProviderRegistration:
    provider_ref: str
    backend_ref: str
    adapter_ref: str
    provider_role: str
    enabled_by_default: bool
    fallback_provider_refs: Tuple[str, ...]
    supported_candidate_types: Tuple[str, ...]
    health_signal_required: bool
    disable_policy: str
    candidate_only: bool = True


@dataclass(frozen=True)
class AdapterPlanningDecision:
    decision_ref: str
    planned_adapters: Tuple[str, ...]
    technical_reference_backends: Tuple[str, ...]
    commercial_runtime_backends: Tuple[str, ...]
    blocked_runtime_backends: Tuple[str, ...]
    observation_backends: Tuple[str, ...]
    license_gate_required: bool
    runtime_isolation_required: bool
    output_mapping_required: bool
    dryrun_required_next: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
