# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Real File Controlled Replay DryRun — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-DryRun-v1-001"
SCOPE = "generic_json_spatial_trace_real_file_replay_dryrun_v1"
SOURCE_CHAIN = "generic_json_spatial_trace_real_file_replay_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 Real File Controlled Replay Planning，读取本地受控样例文件执行 "
    "Generic JSON Spatial Trace controlled replay dry-run；允许离线 replay，不接 live runtime。"
)

PLANNING_REF = "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-Planning-v1-001"
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
RUNTIME_TRIAL_MODE = "real_file_controlled_replay_dryrun_only"

FINAL_DECISION_GO = "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_CONTROLLED_REPLAY_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_CONTROLLED_REPLAY_DRYRUN_BLOCKED"

NEXT_PHASE_REF = (
    "Phase-Generic-JSON-Spatial-Trace-Real-File-Export-Loader-Planning-v1-001"
)

SAMPLES_REL_DIR = (
    "capabilities/field_understanding/generic_json_spatial_trace_real_file_replay_dryrun/samples"
)

SAMPLE_FILES: Tuple[str, ...] = (
    "sample_pose_motion_trace.json",
    "sample_odometry_health_trace.json",
    "sample_anchor_relocalization_drift_trace.json",
    "sample_spatial_fusion_trace.json",
    "invalid_missing_source_chain_trace.json",
)

POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "real_file_pose_motion_low_risk_replay",
    "real_file_odometry_health_replay",
    "real_file_anchor_relocalization_drift_replay",
    "real_file_spatial_fusion_replay",
    "real_file_field_task_guidance_replay_path",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_missing_source_chain_rejected",
    "invalid_unsupported_candidate_type_rejected",
    "invalid_backend_native_direct_to_field_rejected",
    "invalid_runtime_escalation_rejected",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "GenericJSONSpatialTraceRealFileReplayDryRunCase",
    "RealFileReplayInputBundle",
    "RealFileSourceAdmissionResult",
    "RealFileReplayParsedTraceResult",
    "RealFileReplayCandidateBundleResult",
    "RealFileReplayPathTrace",
    "RealFileReplayDryRunReviewDecision",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "real_file_controlled_replay_dryrun_only": True,
    "real_file_replay_execution_allowed": True,
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
class GenericJSONSpatialTraceRealFileReplayDryRunCase:
    case_ref: str
    case_kind: str
    sample_file: str
    expected_outcome: str
    source_chain: str


@dataclass(frozen=True)
class RealFileReplayInputBundle:
    bundle_ref: str
    sample_file: str
    file_origin: Dict[str, Any]
    trace_items: Tuple[Dict[str, Any], ...]
    source_chain: str


@dataclass(frozen=True)
class RealFileSourceAdmissionResult:
    result_ref: str
    file_source_admitted: bool
    file_origin_metadata_present: bool
    controlled_samples_path_ok: bool
    rejection_reasons: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class RealFileReplayParsedTraceResult:
    result_ref: str
    parsed_count: int
    parse_errors: Tuple[str, ...]
    parsed_items: Tuple[Dict[str, Any], ...]
    source_chain: str


@dataclass(frozen=True)
class RealFileReplayCandidateBundleResult:
    result_ref: str
    candidate_bundle_mapping_ok: bool
    bundle_ref: str
    output_candidate_types: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class RealFileReplayPathTrace:
    trace_ref: str
    replay_path: str
    candidate_only: bool
    relocalization_does_not_restore_runtime_trust: bool
    gps_does_not_override_field_identity: bool
    runtime_navigation_started: bool
    source_chain: str


@dataclass(frozen=True)
class RealFileReplayDryRunReviewDecision:
    decision_ref: str
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    final_decision: str
    real_file_replay_execution_allowed: bool = True
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
