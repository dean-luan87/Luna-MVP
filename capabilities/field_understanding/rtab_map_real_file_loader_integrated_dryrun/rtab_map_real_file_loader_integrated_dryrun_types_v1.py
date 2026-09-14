# -*- coding: utf-8 -*-
"""RTAB-Map Real File Loader Integrated DryRun — types v1.

Integration-accelerated phase. Merges:
- RTAB odometry real file loader dry-run
- RTAB graph real file loader planning-lite + dry-run
- RTAB trajectory / odometry / graph multi-export closure
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-RTAB-Map-Real-File-Loader-Integrated-DryRun-v1-001"
SCOPE = "rtab_map_real_file_loader_integrated_dryrun_v1"
SOURCE_CHAIN = "rtab_map_real_file_loader_integrated_dryrun_v1"

INTEGRATED_PRINCIPLE_ZH = (
    "对 RTAB-Map real file loader 后续验证做整合加速：合并 RTAB odometry dry-run、RTAB graph "
    "planning-lite + dry-run、RTAB trajectory/odometry/graph multi-export closure。已封口治理链不再"
    "重复拆分，ControlledTrialGovernanceLifecycleTemplateV1 / Generic JSON Spatial Trace Parser / "
    "Interface Layer Governance / Model Admission Governance 直接复用。允许本地受控样例离线转换 / "
    "parser replay，不读 RTAB database，不接 ROS，不启动 RTAB live runtime。"
)

INTEGRATION_PRINCIPLES: Tuple[str, ...] = (
    "sealed_governance_chain_not_re_split",
    "controlled_trial_governance_template_reused",
    "generic_json_spatial_trace_parser_reused",
    "interface_layer_and_model_admission_governance_reused",
    "trajectory_only_closure_reference_verified",
    "odometry_enters_dry_run",
    "graph_planning_lite_plus_dry_run_same_phase",
    "final_output_rtab_real_file_loader_integrated_closure",
)

RTAB_TRAJECTORY_LOADER_DRYRUN_REF = (
    "Phase-RTAB-Map-Trajectory-Real-File-Loader-DryRun-v1-001"
)
RTAB_ODOMETRY_LOADER_PLANNING_REF = (
    "Phase-RTAB-Map-Odometry-Real-File-Loader-Planning-v1-001"
)
RTAB_TRAJECTORY_FIXTURE_REF = (
    "Phase-RTAB-Map-Trajectory-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
)
RTAB_ODOMETRY_FIXTURE_REF = (
    "Phase-RTAB-Map-Odometry-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
)
RTAB_GRAPH_FIXTURE_REF = (
    "Phase-RTAB-Map-Graph-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
)
GENERIC_JSON_SPATIAL_TRACE_PARSER_REF = "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001"
REAL_FILE_REPLAY_DRYRUN_REF = (
    "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-DryRun-v1-001"
)
TUM_REAL_FILE_LOADER_DRYRUN_REF = "Phase-Generic-TUM-Real-File-Loader-DryRun-v1-001"
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
GENERIC_JSON_PARSER_REF = "generic_json_spatial_trace_parser_v1"
SOURCE_FAMILY = "rtab_map_real_file_exports"
ODOMETRY_SOURCE_FORMAT = "rtab_map_odometry_export_file"
GRAPH_SOURCE_FORMAT = "rtab_map_graph_export_file"
TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
OUTPUT_CANDIDATE_CONTRACT_REF = "spatial_evidence_candidate_bundle"

RUNTIME_TRIAL_MODE = "rtab_real_file_loader_integrated_dryrun_only"

NODE_ID_ALIASES: Tuple[str, ...] = ("node_id", "id", "vertex_id")
TIMESTAMP_MS_ALIASES: Tuple[str, ...] = ("timestamp_ms",)
TIMESTAMP_SEC_ALIASES: Tuple[str, ...] = ("timestamp", "timestamp_sec", "stamp", "time")
TRANSLATION_ALIASES: Dict[str, Tuple[str, ...]] = {
    "x": ("x", "tx"),
    "y": ("y", "ty"),
    "z": ("z", "tz"),
}
ORIENTATION_FIELDS: Tuple[str, ...] = ("qx", "qy", "qz", "qw")
TRACKING_STATE_ALIASES: Tuple[str, ...] = (
    "tracking_state",
    "tracking_status",
    "state",
    "odom_state",
)
ODOMETRY_QUALITY_ALIASES: Tuple[str, ...] = (
    "odometry_quality",
    "quality",
    "odom_quality",
)

EDGE_TYPE_ALIASES: Tuple[str, ...] = ("edge_type", "edge_kind", "link_type", "constraint_type")
EDGE_FROM_ALIASES: Tuple[str, ...] = ("from_node_id", "from_id", "from")
EDGE_TO_ALIASES: Tuple[str, ...] = ("to_node_id", "to_id", "to")
LOOP_CLOSURE_ALIASES: Tuple[str, ...] = ("loop_closure", "lc_hint", "relocalization_hint")
DRIFT_HINT_ALIASES: Tuple[str, ...] = (
    "drift_score",
    "drift_hint",
    "loop_closure_drift_metric_m",
)
LOOP_CLOSURE_EDGE_TYPES: Tuple[str, ...] = ("loop_closure", "relocalization")
DRIFT_DRIFT_SCORE_THRESHOLD = 0.1

HEALTH_PROVIDER = "rtab_map_odometry"
HEALTH_STATUS_OK_STATES: Tuple[str, ...] = ("ok", "good", "tracked")
HEALTH_STATUS_DEGRADED_STATES: Tuple[str, ...] = ("degraded", "weak", "low_confidence")
HEALTH_STATUS_LOST_STATES: Tuple[str, ...] = ("lost", "failed", "not_tracked")
HEALTH_SEVERITY_BY_STATUS: Dict[str, str] = {
    "ok": "none",
    "degraded": "warning",
    "lost": "critical",
}
ODOMETRY_QUALITY_DEGRADED_THRESHOLD = 0.5

PROHIBITED_FILE_FLAGS: Tuple[str, ...] = (
    "direct_field_synthesis_write",
    "rtab_db_read",
    "ros_topic_read",
    "live_rtab_runtime",
    "restore_runtime_trust",
    "runtime_trust_restored",
)

PROHIBITED_EDGE_FLAGS: Tuple[str, ...] = (
    "restore_runtime_trust",
    "runtime_trust_restored",
)

FULL_CANDIDATE_TYPE_COVERAGE: Tuple[str, ...] = (
    "pose",
    "motion",
    "health",
    "anchor",
    "relocalization",
    "drift",
)

FINAL_DECISION_GO = "RTAB_MAP_REAL_FILE_LOADER_INTEGRATED_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "RTAB_MAP_REAL_FILE_LOADER_INTEGRATED_DRYRUN_BLOCKED"

NEXT_PHASE_REF = "Phase-RTAB-Map-Real-File-Loader-Baseline-Sealed-v1-001"

SAMPLES_REL_DIR = (
    "capabilities/field_understanding/rtab_map_real_file_loader_integrated_dryrun/samples"
)

SAMPLE_FILES: Tuple[str, ...] = (
    "sample_rtab_odometry_valid_with_degraded.json",
    "sample_rtab_odometry_lost_tracking.json",
    "sample_rtab_odometry_alias_fields.json",
    "sample_rtab_graph_valid_with_loop_closure.json",
    "sample_rtab_graph_drift_case.json",
    "sample_rtab_graph_alias_fields.json",
    "invalid_rtab_odometry_missing_tracking_state.json",
    "invalid_rtab_graph_missing_node_id.json",
    "invalid_rtab_graph_missing_source_chain.json",
    "invalid_rtab_graph_runtime_trust_restore_attempt.json",
    "invalid_rtab_native_db_ros_live_runtime.json",
)

POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "rtab_odometry_degraded_health_integrated_dryrun",
    "rtab_odometry_lost_health_integrated_dryrun",
    "rtab_odometry_alias_fields_integrated_dryrun",
    "rtab_graph_anchor_relocalization_integrated_dryrun",
    "rtab_graph_drift_integrated_dryrun",
    "rtab_graph_alias_fields_integrated_dryrun",
    "rtab_multi_export_candidate_type_coverage",
    "rtab_multi_export_field_task_guidance_replay_path",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_odometry_missing_tracking_state_rejected",
    "invalid_graph_missing_node_id_rejected",
    "invalid_graph_missing_source_chain_rejected",
    "invalid_graph_runtime_trust_restore_rejected",
    "invalid_rtab_db_ros_live_runtime_rejected",
    "invalid_direct_action_speech_navigation_fact_write_rejected",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RTABMapRealFileLoaderIntegratedDryRunProfile",
    "RTABIntegratedInputBundle",
    "RTABIntegratedSourceAdmissionResult",
    "RTABOdometryIntegratedDryRunResult",
    "RTABGraphPlanningLiteResult",
    "RTABGraphIntegratedDryRunResult",
    "RTABMultiExportCandidateBundleResult",
    "RTABIntegratedReplayPathResult",
    "RTABIntegratedClosureDecision",
)

INTEGRATED_GOVERNANCE_RULES: Tuple[str, ...] = (
    "integrated_dry_run_is_not_live_runtime",
    "planning_only_governance_chain_must_not_be_reopened",
    "local_file_read_only_under_controlled_samples_directory",
    "file_source_admission_must_run_before_record_parsing",
    "conversion_output_must_be_generic_json_spatial_trace",
    "generic_json_spatial_trace_parser_must_be_reused",
    "rtab_trajectory_odometry_graph_native_output_must_not_enter_field_synthesis_directly",
    "odometry_health_must_map_to_slam_health_candidate",
    "health_candidate_remains_candidate_only_evidence",
    "graph_relocalization_must_not_restore_runtime_trust",
    "graph_drift_remains_uncertainty_evidence",
    "graph_anchor_must_not_write_fact",
    "motion_candidate_only_from_consecutive_valid_records",
    "source_chain_file_origin_export_session_id_node_refs_must_be_preserved",
    "rtab_database_read_ros_topic_live_rtab_runtime_prohibited",
    "field_task_guidance_replay_remains_candidate_only",
    "no_live_sensor_no_real_gps_no_real_map_api_no_ros_no_camera_no_imu",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "integrated_dry_run_closes_rtab_real_file_loader_baseline_if_all_checks_pass",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "rtab_real_file_loader_integrated_dryrun_only": True,
    "planning_only_governance_chain_not_reopened": True,
    "real_file_conversion_execution_allowed": True,
    "real_file_replay_execution_allowed": True,
    "runtime_activation_allowed": False,
    "trial_runtime_started": False,
    "live_sensor_connected": False,
    "rtab_database_read_allowed": False,
    "ros_connected": False,
    "live_rtab_runtime_started": False,
    "real_navigation_started": False,
    "real_map_api_connected": False,
    "real_gps_connected": False,
    "camera_connected": False,
    "imu_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
    "runtime_activation_deferred": True,
}


@dataclass(frozen=True)
class RTABMapRealFileLoaderIntegratedDryRunProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    generic_json_spatial_trace_parser_ref: str
    rtab_trajectory_loader_dryrun_ref: str
    rtab_odometry_loader_planning_ref: str
    rtab_graph_fixture_ref: str
    source_family: str
    target_internal_format: str
    target_entrypoint: str
    runtime_trial_mode: str
    integration_principles: Tuple[str, ...]
    full_candidate_type_coverage: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RTABIntegratedInputBundle:
    bundle_ref: str
    sample_file: str
    source_format: str
    export_session_id: str
    file_origin: Dict[str, Any]
    source_chain_prefix: Tuple[str, ...]
    raw_record_count: int
    source_chain: str


@dataclass(frozen=True)
class RTABIntegratedSourceAdmissionResult:
    result_ref: str
    file_source_admitted: bool
    controlled_samples_path_ok: bool
    format_ref_ok: bool
    file_origin_metadata_present: bool
    source_chain_present: bool
    prohibited_flags_absent: bool
    rejection_reasons: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class RTABOdometryIntegratedDryRunResult:
    result_ref: str
    conversion_ok: bool
    pose_item_count: int
    motion_item_count: int
    health_item_count: int
    health_status: str
    severity: str
    health_candidate_maps_to_slam_health_candidate: bool
    candidate_bundle_mapping_ok: bool
    alias_field_mapping_used: bool
    source_chain: str


@dataclass(frozen=True)
class RTABGraphPlanningLiteResult:
    result_ref: str
    planning_lite_completed: bool
    node_required_fields_ok: bool
    edge_required_fields_ok: bool
    alias_support_ok: bool
    loop_closure_only_to_relocalization: bool
    drift_remains_uncertainty_evidence: bool
    anchor_does_not_write_fact: bool
    source_chain: str


@dataclass(frozen=True)
class RTABGraphIntegratedDryRunResult:
    result_ref: str
    conversion_ok: bool
    anchor_item_count: int
    relocalization_item_count: int
    drift_item_count: int
    relocalization_does_not_restore_runtime_trust: bool
    drift_remains_uncertainty_evidence: bool
    anchor_does_not_write_fact: bool
    candidate_bundle_mapping_ok: bool
    alias_field_mapping_used: bool
    source_chain: str


@dataclass(frozen=True)
class RTABMultiExportCandidateBundleResult:
    result_ref: str
    trajectory_scope_closed: bool
    odometry_scope_closed: bool
    graph_scope_closed: bool
    candidate_type_coverage: Tuple[str, ...]
    candidate_type_coverage_complete: bool
    multi_export_candidate_bundle_mapping_ok: bool
    source_chain: str


@dataclass(frozen=True)
class RTABIntegratedReplayPathResult:
    result_ref: str
    replay_path: str
    candidate_only: bool
    candidate_refs: Tuple[str, ...]
    field_task_guidance_replay_path_candidate_only: bool
    gps_does_not_override_field_identity: bool
    relocalization_does_not_restore_runtime_trust: bool
    health_does_not_trigger_action_speech_navigation_fact_write: bool
    direct_field_synthesis_write: bool
    runtime_navigation_started: bool
    source_chain: str


@dataclass(frozen=True)
class RTABIntegratedClosureDecision:
    decision_ref: str
    integrated_profile_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    trajectory_scope_closed: bool
    odometry_scope_closed: bool
    graph_scope_closed: bool
    rtab_trajectory_real_file_loader_dryrun_go_verified: bool
    rtab_odometry_real_file_loader_planning_go_verified: bool
    rtab_graph_fixture_go_verified: bool
    generic_json_spatial_trace_parser_go_verified: bool
    controlled_trial_governance_template_ref_ok: bool
    final_decision: str
    real_file_conversion_execution_allowed: bool = True
    real_file_replay_execution_allowed: bool = True
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
