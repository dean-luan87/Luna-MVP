# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Real File Controlled Replay Planning — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-Planning-v1-001"
SCOPE = "generic_json_spatial_trace_real_file_replay_planning_review_only"
SOURCE_CHAIN = "generic_json_spatial_trace_real_file_replay_planning_v1"

REPLAY_PLANNING_PRINCIPLE_ZH = (
    "从治理链回到真实数据 / 模型输出接入。定义 Generic JSON Spatial Trace real file "
    "controlled replay 规划基线：真实离线文件或导出 trace 作为输入，仅做 planning + matrix review，"
    "不执行 replay，不启动 runtime。"
)

GENERIC_JSON_SPATIAL_TRACE_PARSER_REF = "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001"
SLAM_SPATIAL_EVIDENCE_CHAIN_REF = "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001"
PHASE_ONE_CHAIN_REF = "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
ISSUANCE_PACKAGE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Issuance-Package-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
GENERIC_JSON_PARSER_REF = "generic_json_spatial_trace_parser_v1"
TARGET_ENTRYPOINT = "field_synthesis_v1"
OUTPUT_CANDIDATE_CONTRACT_REF = "spatial_evidence_candidate_bundle"
FUSION_CANDIDATE_REF = "spatial_odometry_fusion_candidate"

PHASE_ONE_CHAIN_STATUS = "sealed"
CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_STATUS = "sealed"
RUNTIME_TRIAL_MODE = "real_file_controlled_replay_planning_only"
CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED = True

FINAL_DECISION_GO = "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_CONTROLLED_REPLAY_PLANNING_GO"
FINAL_DECISION_BLOCKED = "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_CONTROLLED_REPLAY_PLANNING_BLOCKED"

NEXT_PHASE_REF = (
    "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-DryRun-v1-001"
)

PIPELINE_STAGES: Tuple[str, ...] = (
    "real_file_or_exported_trace",
    "generic_json_spatial_trace_file_loader_planning",
    "generic_json_spatial_trace_parser",
    "spatial_evidence_candidate_bundle",
    "spatial_odometry_fusion_candidate",
    "field_task_guidance_candidate_replay_path",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "GenericJSONSpatialTraceRealFileReplayPlanningProfile",
    "RealFileInputSourcePolicy",
    "RealFileFormatAdmissionPolicy",
    "RealFileReplayBoundaryPolicy",
    "RealFileReplayScenarioPolicy",
    "RealFileReplaySafetyPolicy",
    "RealFileReplayObservationLogPolicy",
    "RealFileReplayPlanningDecision",
)

REAL_FILE_INPUT_SOURCE_REFS: Tuple[str, ...] = (
    "generic_json_spatial_trace_file",
    "tum_trajectory_converted_json_trace_file",
    "rtab_map_trajectory_export_converted_json_trace_file",
    "rtab_map_odometry_export_converted_json_trace_file",
    "rtab_map_graph_export_converted_json_trace_file",
)

INPUT_SOURCE_GO_KEYS: Tuple[str, ...] = (
    "generic_json_spatial_trace_file_supported",
    "tum_converted_json_trace_file_supported",
    "rtab_trajectory_converted_json_trace_file_supported",
    "rtab_odometry_converted_json_trace_file_supported",
    "rtab_graph_converted_json_trace_file_supported",
)

REPLAY_SCENARIO_REFS: Tuple[str, ...] = (
    "real_file_pose_motion_replay_low_risk",
    "real_file_odometry_health_replay",
    "real_file_anchor_relocalization_drift_replay",
    "real_file_spatial_odometry_fusion_replay",
    "real_file_field_task_guidance_replay_path",
    "invalid_or_untrusted_file_blocked",
)

REPLAY_SCENARIO_GO_KEYS: Tuple[str, ...] = (
    "real_file_pose_motion_replay_low_risk_supported",
    "real_file_odometry_health_replay_supported",
    "real_file_anchor_relocalization_drift_replay_supported",
    "real_file_spatial_odometry_fusion_replay_supported",
    "real_file_field_task_guidance_replay_path_supported",
    "invalid_or_untrusted_file_blocked",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    SLAM_SPATIAL_EVIDENCE_CHAIN_REF,
    PHASE_ONE_CHAIN_REF,
    GOVERNANCE_CLOSURE_REF,
    ISSUANCE_PACKAGE_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
)

REPLAY_PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "real_file_replay_planning_is_not_replay_execution",
    "real_file_replay_planning_is_not_runtime_activation",
    "real_file_must_pass_source_admission_before_parsing",
    "generic_json_spatial_trace_parser_must_be_reused",
    "external_backend_native_file_must_not_enter_field_synthesis_directly",
    "all_source_chain_and_file_origin_metadata_must_be_preserved",
    "unsupported_candidate_type_must_be_rejected",
    "missing_source_chain_must_be_rejected",
    "relocalization_must_not_restore_runtime_trust",
    "gps_gnss_hint_must_not_override_field_identity",
    "field_task_guidance_replay_remains_candidate_only",
    "no_live_sensor_no_real_gps_no_real_map_api_no_ros_no_camera_no_imu",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

UNIVERSAL_BLOCKED_OPERATIONS: Tuple[str, ...] = (
    "replay_execution",
    "runtime_activation",
    "direct_action",
    "direct_speech_tts",
    "direct_fact_write",
    "real_navigation",
    "live_sensor_trigger",
    "ros_topic_read",
    "rtab_database_read",
    "live_camera",
    "live_imu",
    "live_gps_gnss",
    "real_map_api",
    "backend_native_direct_to_field_synthesis",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "real_file_controlled_replay_planning_only": True,
    "real_file_replay_execution_allowed": False,
    "runtime_activation_allowed": False,
    "trial_runtime_started": False,
    "live_sensor_connected": False,
    "real_navigation_started": False,
    "real_map_api_connected": False,
    "real_gps_connected": False,
    "ros_connected": False,
    "camera_connected": False,
    "imu_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
    "runtime_activation_deferred": True,
}


@dataclass(frozen=True)
class GenericJSONSpatialTraceRealFileReplayPlanningProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    generic_json_spatial_trace_parser_ref: str
    target_entrypoint: str
    phase_one_chain_status: str
    controlled_runtime_trial_governance_status: str
    runtime_trial_mode: str
    pipeline_stages: Tuple[str, ...]
    real_file_input_source_refs: Tuple[str, ...]
    replay_scenario_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    candidate_only_source_chain_required: bool = True


@dataclass(frozen=True)
class RealFileInputSourcePolicy:
    source_ref: str
    source_zh: str
    priority: str
    allowed_plan_operations: Tuple[str, ...]
    blocked_operations: Tuple[str, ...]
    requires_parser_reuse: bool
    requires_source_admission: bool
    requires_file_origin_metadata: bool
    source_chain: str
    supported: bool = True


@dataclass(frozen=True)
class RealFileFormatAdmissionPolicy:
    policy_ref: str
    real_file_source_admission_required: bool
    file_origin_metadata_required: bool
    source_chain_required: bool
    unsupported_candidate_type_rejected: bool
    missing_source_chain_rejected: bool
    source_chain: str


@dataclass(frozen=True)
class RealFileReplayBoundaryPolicy:
    policy_ref: str
    generic_json_parser_reused: bool
    backend_native_output_direct_to_field_blocked: bool
    parser_ref: str
    target_entrypoint: str
    output_candidate_contract_ref: str
    source_chain: str


@dataclass(frozen=True)
class RealFileReplayScenarioPolicy:
    scenario_ref: str
    input_trace_types: Tuple[str, ...]
    output_planning_target: str
    target_field_scenarios: Tuple[str, ...]
    scenario_requirements: Tuple[str, ...]
    blocked_operations: Tuple[str, ...]
    allowed_next_step: str
    source_chain: str
    supported: bool = True
    blocked_scenario: bool = False


@dataclass(frozen=True)
class RealFileReplaySafetyPolicy:
    policy_ref: str
    relocalization_does_not_restore_runtime_trust: bool
    gps_does_not_override_field_identity: bool
    candidate_only_replay_path_enforced: bool
    health_generates_candidate_risk_only: bool
    source_chain: str


@dataclass(frozen=True)
class RealFileReplayObservationLogPolicy:
    policy_ref: str
    log_file_origin_metadata: bool
    log_source_admission_result: bool
    log_parser_replay_planning_status: bool
    log_blocked_operations: bool
    source_chain: str


@dataclass(frozen=True)
class RealFileReplayPlanningDecision:
    decision_ref: str
    profile_ref: str
    planning_profile_count: int
    real_file_input_source_policy_count: int
    replay_scenario_count: int
    controlled_trial_governance_template_ref_ok: bool
    phase_one_chain_sealed_verified: bool
    controlled_runtime_trial_governance_sealed_verified: bool
    generic_json_spatial_trace_parser_go_verified: bool
    final_decision: str
    real_file_replay_execution_allowed: bool = False
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
