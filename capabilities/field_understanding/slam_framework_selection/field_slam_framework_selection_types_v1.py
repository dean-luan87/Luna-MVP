# -*- coding: utf-8 -*-
"""Field SLAM Framework Selection — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Field-SLAM-Framework-Selection-v1-001"
SCOPE = "field_slam_framework_selection_matrix_only"
SOURCE_CHAIN = "field_slam_framework_selection_v1"

FINAL_DECISION_MATRIX_READY = "FIELD_SLAM_FRAMEWORK_SELECTION_MATRIX_READY_FOR_REVIEW"

SELECTION_STRATEGY_NOTE = (
    "P0 does not bind a specific SLAM runtime. Evidence-based framework matrix first; "
    "frameworks are classified as technical_reference_candidate or commercial_runtime_candidate. "
    "Luna Field Spatial Evidence Provider interface remains independent."
)
SELECTION_STRATEGY_NOTE_ZH = (
    "P0 不绑定具体 SLAM runtime。先做 Evidence-Based Framework Matrix；"
    "框架身份分为 technical_reference_candidate 与 commercial_runtime_candidate；"
    "Luna 场空间证据提供者接口保持独立。"
)

FRAMEWORK_REPLACEABILITY_GOVERNANCE_ID = "framework_replaceability_governance_v1"
FRAMEWORK_REPLACEABILITY_GOVERNANCE_NOTE = (
    "Luna binds the Field Spatial Evidence Contract, not any specific SLAM/VIO/SceneGraph "
    "framework. All backends are replaceable evidence suppliers governed through adapter "
    "contract, license gate, and runtime admission."
)
FRAMEWORK_REPLACEABILITY_GOVERNANCE_NOTE_ZH = (
    "Luna 绑定场空间证据契约，不绑定具体 SLAM/VIO/SceneGraph 框架。"
    "所有 backend 都是可替换的证据供应商，须经 adapter contract、license gate、runtime admission 治理。"
)
FRAMEWORK_REPLACEABILITY_GOVERNANCE_RULES: Tuple[str, ...] = (
    "no_direct_dependency_on_framework_internal_structures",
    "all_framework_outputs_map_to_luna_standard_candidates",
    "frameworks_must_not_enter_decision_speech_or_fact_layer",
    "gpl_or_unknown_license_not_irreplaceable_runtime_dependency",
    "commercial_runtime_requires_license_gate_pass_record",
    "adapter_must_support_disabled_degraded_fallback",
    "capability_slot_allows_multiple_backend_candidates",
    "backend_switch_must_not_change_field_understanding_main_chain",
)

NEXT_PHASE_ADAPTER_CONTRACT_PLANNING = "Phase-Field-SLAM-Adapter-Contract-Planning-v1-001"
FINAL_DECISION_HANDOFF_READY = (
    "FIELD_SLAM_FRAMEWORK_SELECTION_HANDOFF_READY_FOR_ADAPTER_CONTRACT_PLANNING"
)

BACKEND_ADMISSION_PIPELINE: Tuple[str, ...] = (
    "framework_selection",
    "license_gate",
    "adapter_contract",
    "output_mapping",
    "static_validation",
    "dryrun_trace",
    "verifier",
    "post_review",
    "runtime_admission",
)

LUNA_SPATIAL_EVIDENCE_CONTRACT_TYPES: Tuple[str, ...] = (
    "PoseCandidate",
    "MotionCandidate",
    "SpatialAnchorCandidate",
    "LocalMapCandidate",
    "SLAMHealthCandidate",
    "MapDriftCandidate",
    "RelocalizationCandidate",
)

GENERIC_SLAM_ADAPTER_CONTRACT_ID = "generic_slam_adapter_contract_v1"
SPATIAL_EVIDENCE_PROVIDER_ROLE = "SpatialEvidenceProvider"

SLAM_FRAMEWORK_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "framework_ref",
    "framework_name",
    "framework_group",
    "open_source_status",
    "license_type",
    "license_risk",
    "commercial_modification_risk",
    "primary_role_for_luna",
    "technical_reference_candidate",
    "commercial_runtime_candidate",
    "runtime_priority",
    "observation_priority",
    "source_refs",
    "notes",
    "candidate_only",
)

SLAM_FRAMEWORK_EVALUATION_FIELDS: Tuple[str, ...] = (
    "evaluation_ref",
    "framework_ref",
    "pose_candidate_fit",
    "motion_candidate_fit",
    "spatial_anchor_fit",
    "local_map_fit",
    "slam_health_fit",
    "map_drift_fit",
    "relocalization_fit",
    "field_synthesis_fit",
    "wearable_fit",
    "runtime_weight",
    "engineering_risk",
    "semantic_extension_fit",
    "static_dynamic_split_fit",
    "action_semantic_map_fit",
    "recommended_priority",
    "rationale",
    "candidate_only",
)

SLAM_FRAMEWORK_SELECTION_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "recommended_p0_technical",
    "recommended_p0_commercial_safe",
    "recommended_p1",
    "recommended_p2",
    "recommended_observation",
    "deferred",
    "blocked",
    "rationale_refs",
    "license_gate_required",
    "adapter_contract_required",
    "final_decision",
    "candidate_only",
)

MATRIX_OBJECT_TYPES: Tuple[str, ...] = (
    "SLAMFrameworkCandidate",
    "SLAMFrameworkEvaluation",
    "SLAMFrameworkSelectionDecision",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "architecture_definition_only": True,
    "no_slam_runtime_binding": True,
    "no_slam_framework_execution": True,
    "no_camera_runtime": True,
    "no_model_execution": True,
    "no_ros_runtime": True,
    "no_benchmark_execution": True,
    "no_graph_eqa_runtime": True,
    "no_adapter_implementation": True,
    "no_commercial_final_selection": True,
    "matrix_review_only": True,
}


@dataclass(frozen=True)
class SLAMFrameworkCandidate:
    framework_ref: str
    framework_name: str
    framework_group: str
    open_source_status: str
    license_type: str
    license_risk: str
    commercial_modification_risk: str
    primary_role_for_luna: str
    technical_reference_candidate: bool
    commercial_runtime_candidate: bool
    runtime_priority: str
    observation_priority: str
    source_refs: Tuple[str, ...]
    notes: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMFrameworkEvaluation:
    evaluation_ref: str
    framework_ref: str
    pose_candidate_fit: str
    motion_candidate_fit: str
    spatial_anchor_fit: str
    local_map_fit: str
    slam_health_fit: str
    map_drift_fit: str
    relocalization_fit: str
    field_synthesis_fit: str
    wearable_fit: str
    runtime_weight: str
    engineering_risk: str
    semantic_extension_fit: str
    static_dynamic_split_fit: str
    action_semantic_map_fit: str
    recommended_priority: str
    rationale: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMFrameworkSelectionDecision:
    decision_ref: str
    recommended_p0_technical: Tuple[str, ...]
    recommended_p0_commercial_safe: Tuple[str, ...]
    recommended_p1: Tuple[str, ...]
    recommended_p2: Tuple[str, ...]
    recommended_observation: Tuple[str, ...]
    deferred: Tuple[str, ...]
    blocked: Tuple[str, ...]
    rationale_refs: Tuple[str, ...]
    license_gate_required: bool
    adapter_contract_required: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
