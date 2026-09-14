# -*- coding: utf-8 -*-
"""RTAB-Map Odometry Real File Loader Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.rtab_map_odometry_real_file_loader_planning.rtab_map_odometry_real_file_loader_planning_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXPORT_LOADER_PLANNING_REF,
    FIELD_ALIASES,
    FINAL_DECISION_GO,
    GENERIC_JSON_PARSER_REF,
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    GOVERNANCE_CLOSURE_REF,
    HEALTH_SEVERITY_BY_STATUS,
    HEALTH_STATUS_DEGRADED_STATES,
    HEALTH_STATUS_LOST_STATES,
    HEALTH_STATUS_OK_STATES,
    INTERFACE_LAYER_GOVERNANCE_REF,
    LOADER_PLANNING_GOVERNANCE_RULES,
    LOADER_PLANNING_PRINCIPLE_ZH,
    LOADER_SCENARIO_GO_KEYS,
    LOADER_SCENARIO_REFS,
    MODEL_ADMISSION_GOVERNANCE_REF,
    ODOMETRY_QUALITY_DEGRADED_THRESHOLD,
    PHASE_ID,
    REAL_FILE_REPLAY_DRYRUN_REF,
    RECORD_REQUIRED_FIELDS,
    RTABMapOdometryExportFilePolicy,
    RTABMapOdometryFormatAdmissionPolicy,
    RTABMapOdometryHealthMappingPolicy,
    RTABMapOdometryLoaderBoundaryPolicy,
    RTABMapOdometryLoaderSafetyPolicy,
    RTABMapOdometryLoaderScenarioPolicy,
    RTABMapOdometryRealFileLoaderPlanningDecision,
    RTABMapOdometryRealFileLoaderPlanningProfile,
    RTABMapOdometryToJSONTraceMappingPolicy,
    RTAB_ODOMETRY_FIXTURE_REF,
    RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
    RTAB_TRAJECTORY_LOADER_PLANNING_REF,
    RUNTIME_TRIAL_MODE,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    SOURCE_FORMAT,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TUM_REAL_FILE_LOADER_DRYRUN_REF,
    UNIVERSAL_BLOCKED_OPERATIONS,
    candidate_to_dict,
)

REGISTRY_ID = "rtab_map_odometry_real_file_loader_planning_registry_v1"
PROFILE_REF = "rtab_map_odometry_real_file_loader_planning_profile_v1"

_RTAB_ODOMETRY_FIXTURE_ARTIFACT_REL = (
    "_tmp_eval_out/rtab_map_odometry_export_ingest_v1_smoke_v0/"
    "rtab_map_odometry_export_ingest_run_and_review_v1.json"
)
_RTAB_TRAJECTORY_LOADER_DRYRUN_ARTIFACT_REL = (
    "_tmp_eval_out/rtab_map_trajectory_real_file_loader_dryrun_v1_smoke_v0/"
    "rtab_map_trajectory_real_file_loader_dryrun_run_and_review_v1.json"
)
_RTAB_TRAJECTORY_LOADER_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/rtab_map_trajectory_real_file_loader_planning_v1_smoke_v0/"
    "rtab_map_trajectory_real_file_loader_planning_review_v1.json"
)
_EXPORT_LOADER_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/generic_json_spatial_trace_real_file_export_loader_planning_v1_smoke_v0/"
    "generic_json_spatial_trace_real_file_export_loader_planning_review_v1.json"
)
_PARSER_ARTIFACT_REL = (
    "_tmp_eval_out/generic_json_spatial_trace_parser_v1_smoke_v0/"
    "generic_json_spatial_trace_parser_run_and_review_v1.json"
)
_REPLAY_DRYRUN_ARTIFACT_REL = (
    "_tmp_eval_out/generic_json_spatial_trace_real_file_replay_dryrun_v1_smoke_v0/"
    "generic_json_spatial_trace_real_file_replay_dryrun_run_and_review_v1.json"
)
_TUM_LOADER_DRYRUN_ARTIFACT_REL = (
    "_tmp_eval_out/generic_tum_real_file_loader_dryrun_v1_smoke_v0/"
    "generic_tum_real_file_loader_dryrun_run_and_review_v1.json"
)
_GOVERNANCE_CLOSURE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"
)
_INTERFACE_ARTIFACT_REL = (
    "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
    "interface_layer_governance_review_v1.json"
)
_MODEL_ADMISSION_ARTIFACT_REL = (
    "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
    "model_admission_governance_run_and_review_v1.json"
)

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": RTAB_ODOMETRY_FIXTURE_REF,
        "artifact_rel": _RTAB_ODOMETRY_FIXTURE_ARTIFACT_REL,
        "expected_go": "RTAB_MAP_ODOMETRY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_odometry_export_ingest/"
            "rtab_map_odometry_export_ingest_types_v1.py"
        ),
        "require_go": True,
        "require_odometry_fixture_go": True,
    },
    {
        "phase_ref": RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
        "artifact_rel": _RTAB_TRAJECTORY_LOADER_DRYRUN_ARTIFACT_REL,
        "expected_go": "RTAB_MAP_TRAJECTORY_REAL_FILE_LOADER_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_trajectory_real_file_loader_dryrun/"
            "rtab_map_trajectory_real_file_loader_dryrun_types_v1.py"
        ),
        "require_go": True,
        "require_trajectory_loader_dryrun_go": True,
    },
    {
        "phase_ref": RTAB_TRAJECTORY_LOADER_PLANNING_REF,
        "artifact_rel": _RTAB_TRAJECTORY_LOADER_PLANNING_ARTIFACT_REL,
        "expected_go": "RTAB_MAP_TRAJECTORY_REAL_FILE_LOADER_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_trajectory_real_file_loader_planning/"
            "rtab_map_trajectory_real_file_loader_planning_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": EXPORT_LOADER_PLANNING_REF,
        "artifact_rel": _EXPORT_LOADER_PLANNING_ARTIFACT_REL,
        "expected_go": "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_EXPORT_LOADER_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_json_spatial_trace_real_file_export_loader_planning/"
            "generic_json_spatial_trace_real_file_export_loader_planning_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        "artifact_rel": _PARSER_ARTIFACT_REL,
        "expected_go": "GENERIC_JSON_SPATIAL_TRACE_PARSER_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_json_spatial_trace_parser/"
            "generic_json_spatial_trace_parser_types_v1.py"
        ),
        "require_go": True,
        "require_parser_go": True,
    },
    {
        "phase_ref": REAL_FILE_REPLAY_DRYRUN_REF,
        "artifact_rel": _REPLAY_DRYRUN_ARTIFACT_REL,
        "expected_go": "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_CONTROLLED_REPLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_json_spatial_trace_real_file_replay_dryrun/"
            "generic_json_spatial_trace_real_file_replay_dryrun_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": TUM_REAL_FILE_LOADER_DRYRUN_REF,
        "artifact_rel": _TUM_LOADER_DRYRUN_ARTIFACT_REL,
        "expected_go": "GENERIC_TUM_REAL_FILE_LOADER_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_tum_real_file_loader_dryrun/"
            "generic_tum_real_file_loader_dryrun_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": GOVERNANCE_CLOSURE_REF,
        "artifact_rel": _GOVERNANCE_CLOSURE_ARTIFACT_REL,
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_governance_closure/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": INTERFACE_LAYER_GOVERNANCE_REF,
        "artifact_rel": _INTERFACE_ARTIFACT_REL,
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "module_rel": (
            "capabilities/midplatform/interface_layer_governance/"
            "interface_layer_governance_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": MODEL_ADMISSION_GOVERNANCE_REF,
        "artifact_rel": _MODEL_ADMISSION_ARTIFACT_REL,
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/model_admission_governance/"
            "model_admission_governance_types_v1.py"
        ),
        "require_go": True,
    },
)

_SCENARIO_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "scenario_ref": "rtab_odometry_basic_pose_motion_health_loader_planning",
        "input_description": "3 条有效 RTAB odometry record，其中 1 条 degraded",
        "output_planning_target": "three_pose_plus_two_motion_plus_one_health_generic_json_spatial_trace",
        "scenario_requirements": (
            "candidate_only",
            "node_id_timestamp_pose_tracking_state_required",
        ),
        "blocked_operations": (),
        "allowed_next_step": "rtab_odometry_real_file_loader_dryrun_planning_only",
        "go_key": "rtab_odometry_basic_pose_motion_health_loader_planning_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rtab_odometry_health_degraded_mapping_planning",
        "input_description": "tracking_state = degraded / low_confidence",
        "output_planning_target": "health_candidate_degraded",
        "scenario_requirements": (
            "health_candidate_risk_only",
            "must_not_directly_block_or_allow_action",
        ),
        "blocked_operations": ("direct_action_from_health",),
        "allowed_next_step": "rtab_odometry_real_file_loader_dryrun_planning_only",
        "go_key": "rtab_odometry_health_degraded_mapping_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rtab_odometry_lost_tracking_mapping_planning",
        "input_description": "tracking_state = lost / failed",
        "output_planning_target": "health_candidate_severity_above_degraded",
        "scenario_requirements": (
            "severity_higher_than_degraded",
            "must_not_trigger_runtime_shutdown_or_navigation_decision",
        ),
        "blocked_operations": ("runtime_shutdown_from_health", "real_navigation"),
        "allowed_next_step": "rtab_odometry_real_file_loader_dryrun_planning_only",
        "go_key": "rtab_odometry_lost_tracking_mapping_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rtab_odometry_alias_field_compatibility_planning",
        "input_description": "使用 id / stamp / tx / tracking_status / quality 等别名字段",
        "output_planning_target": (
            "alias_normalized_to_node_id_timestamp_ms_pose_tracking_state_odometry_quality"
        ),
        "scenario_requirements": (
            "alias_mapped_before_conversion",
            "must_still_enter_generic_json_spatial_trace_parser",
        ),
        "blocked_operations": (),
        "allowed_next_step": "rtab_odometry_real_file_loader_dryrun_planning_only",
        "go_key": "rtab_odometry_alias_field_compatibility_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rtab_odometry_to_replay_path_planning",
        "input_description": "converted pose/motion/health JSON trace",
        "output_planning_target": (
            "generic_json_parser_to_candidate_bundle_to_field_task_guidance_replay_path"
        ),
        "scenario_requirements": (
            "health_candidate_may_influence_risk_candidate",
            "health_must_not_directly_trigger_action",
            "candidate_only",
        ),
        "blocked_operations": (
            "backend_native_direct_to_field_synthesis",
            "direct_action_from_health",
        ),
        "allowed_next_step": "rtab_odometry_real_file_loader_dryrun_planning_only",
        "go_key": "rtab_odometry_to_replay_path_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "invalid_or_unsafe_rtab_odometry_export_blocked",
        "input_description": (
            "缺 tracking_state / 缺 source_chain / quaternion invalid / backend-native RTAB "
            "odometry object / 试图读 RTAB database 或 ROS topic"
        ),
        "output_planning_target": "blocked_rejected",
        "scenario_requirements": ("must_not_enter_converter_or_parser_path",),
        "blocked_operations": (
            "rtab_database_read",
            "ros_topic_read",
            "converter_path",
            "parser_path",
            "field_synthesis_direct",
        ),
        "allowed_next_step": "rejection_only",
        "go_key": "invalid_or_unsafe_rtab_odometry_export_blocked",
        "blocked_scenario": True,
    },
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "loader_scenario_refs": LOADER_SCENARIO_REFS,
    "loader_scenario_go_keys": LOADER_SCENARIO_GO_KEYS,
    "record_required_fields": RECORD_REQUIRED_FIELDS,
    "loader_planning_governance_rules": LOADER_PLANNING_GOVERNANCE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
    "universal_blocked_operations": UNIVERSAL_BLOCKED_OPERATIONS,
}


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(LOADER_SCENARIO_REFS) != 6:
        issues.append("loader_scenario_refs_count_not_6")
    if len(LOADER_SCENARIO_GO_KEYS) != 6:
        issues.append("loader_scenario_go_keys_count_not_6")
    if len(RECORD_REQUIRED_FIELDS) != 8:
        issues.append("record_required_fields_count_not_8")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 11:
        issues.append("sealed_upstream_phase_refs_count_not_11")
    if len(LOADER_PLANNING_GOVERNANCE_RULES) != 16:
        issues.append("loader_planning_governance_rules_count_not_16")
    return len(issues) == 0, issues


def _merge_blocked(*ops: str) -> Tuple[str, ...]:
    merged = list(UNIVERSAL_BLOCKED_OPERATIONS)
    for op in ops:
        if op not in merged:
            merged.append(op)
    return tuple(merged)


def build_loader_planning_profile_v1() -> RTABMapOdometryRealFileLoaderPlanningProfile:
    return RTABMapOdometryRealFileLoaderPlanningProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        generic_json_spatial_trace_parser_ref=GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        rtab_trajectory_real_file_loader_dryrun_ref=RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
        rtab_odometry_fixture_ref=RTAB_ODOMETRY_FIXTURE_REF,
        source_format=SOURCE_FORMAT,
        target_internal_format=TARGET_INTERNAL_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        pipeline_stages=(
            "rtab_map_odometry_export_file",
            "format_admission",
            "rtab_odometry_to_json_trace_converter_planning",
            "pose_motion_health_candidate_planning",
            "generic_json_spatial_trace",
            "generic_json_spatial_trace_parser",
            "spatial_evidence_candidate_bundle",
            "field_task_guidance_candidate_replay_path",
        ),
        loader_scenario_refs=LOADER_SCENARIO_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=LOADER_PLANNING_GOVERNANCE_RULES,
    )


def build_rtab_odometry_export_file_policy_v1() -> RTABMapOdometryExportFilePolicy:
    return RTABMapOdometryExportFilePolicy(
        policy_ref="rtab_map_odometry_export_file_policy_v1",
        source_format=SOURCE_FORMAT,
        source_zh="RTAB-Map odometry export 离线文件",
        priority="P1",
        record_required_fields=RECORD_REQUIRED_FIELDS,
        field_aliases=FIELD_ALIASES,
        output_candidate_types=("pose", "motion", "health"),
        target_converter="rtab_map_odometry_export_to_json_spatial_trace",
        prohibited_operations=(
            "rtab_database_read",
            "ros_topic_read",
            "live_rtab_runtime",
        ),
        blocked_operations=_merge_blocked(
            "rtab_database_read", "ros_topic_read", "live_rtab_runtime"
        ),
        requires_format_admission=True,
        requires_file_origin_metadata=True,
        requires_source_chain=True,
        requires_tracking_state=True,
        source_chain=SOURCE_CHAIN,
        supported=True,
    )


def build_health_mapping_policy_v1() -> RTABMapOdometryHealthMappingPolicy:
    return RTABMapOdometryHealthMappingPolicy(
        policy_ref="rtab_map_odometry_health_mapping_policy_v1",
        health_candidate_mapping_required=True,
        health_candidate_candidate_only=True,
        provider="rtab_map_odometry",
        ok_states=HEALTH_STATUS_OK_STATES,
        degraded_states=HEALTH_STATUS_DEGRADED_STATES,
        lost_states=HEALTH_STATUS_LOST_STATES,
        severity_by_status=HEALTH_SEVERITY_BY_STATUS,
        odometry_quality_degraded_threshold=ODOMETRY_QUALITY_DEGRADED_THRESHOLD,
        degraded_health_does_not_directly_block_or_allow_action=True,
        lost_health_does_not_trigger_runtime_shutdown=True,
        health_does_not_trigger_speech_navigation_fact_write=True,
        source_chain=SOURCE_CHAIN,
    )


def build_shared_loader_policies_v1() -> Dict[str, Any]:
    return {
        "format_admission_policy": candidate_to_dict(
            RTABMapOdometryFormatAdmissionPolicy(
                policy_ref="rtab_map_odometry_format_admission_policy_v1",
                format_admission_required=True,
                node_id_required=True,
                timestamp_required=True,
                pose_required=True,
                confidence_required=True,
                tracking_state_required=True,
                source_chain_required=True,
                file_origin_metadata_required=True,
                quaternion_validation_required=True,
                rtab_database_read_blocked=True,
                ros_topic_blocked=True,
                live_rtab_runtime_blocked=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "mapping_policy": candidate_to_dict(
            RTABMapOdometryToJSONTraceMappingPolicy(
                policy_ref="rtab_map_odometry_to_json_trace_mapping_policy_v1",
                target_internal_format=TARGET_INTERNAL_FORMAT,
                generic_json_output_required=True,
                generic_json_parser_required=True,
                parser_ref=GENERIC_JSON_PARSER_REF,
                target_entrypoint=TARGET_ENTRYPOINT,
                pose_trace_id_template="rtab_odom_pose_{node_id}",
                motion_trace_id_template="rtab_odom_motion_{from_node_id}_{to_node_id}",
                health_trace_id_template="rtab_odom_health_{node_id}",
                motion_generated_only_from_consecutive_records=True,
                field_aliases=FIELD_ALIASES,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "health_mapping_policy": candidate_to_dict(build_health_mapping_policy_v1()),
        "boundary_policy": candidate_to_dict(
            RTABMapOdometryLoaderBoundaryPolicy(
                policy_ref="rtab_map_odometry_loader_boundary_policy_v1",
                backend_native_output_direct_to_field_blocked=True,
                conversion_execution_allowed=False,
                parser_must_remain_entry_validator=True,
                parser_ref=GENERIC_JSON_PARSER_REF,
                target_entrypoint=TARGET_ENTRYPOINT,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "safety_policy": candidate_to_dict(
            RTABMapOdometryLoaderSafetyPolicy(
                policy_ref="rtab_map_odometry_loader_safety_policy_v1",
                rtab_database_read_blocked=True,
                ros_topic_blocked=True,
                live_rtab_runtime_blocked=True,
                backend_native_direct_to_field_blocked=True,
                health_candidate_candidate_only=True,
                degraded_health_does_not_directly_block_or_allow_action=True,
                lost_health_does_not_trigger_runtime_shutdown=True,
                health_does_not_trigger_speech_navigation_fact_write=True,
                field_task_guidance_replay_candidate_only=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_loader_scenario_policies_v1() -> Tuple[RTABMapOdometryLoaderScenarioPolicy, ...]:
    return tuple(
        RTABMapOdometryLoaderScenarioPolicy(
            scenario_ref=spec["scenario_ref"],
            input_description=spec["input_description"],
            output_planning_target=spec["output_planning_target"],
            scenario_requirements=spec["scenario_requirements"],
            blocked_operations=_merge_blocked(*spec["blocked_operations"]),
            allowed_next_step=spec["allowed_next_step"],
            source_chain=SOURCE_CHAIN,
            supported=not spec["blocked_scenario"],
            blocked_scenario=spec["blocked_scenario"],
        )
        for spec in _SCENARIO_SPECS
    )


def build_loader_scenario_go_map(
    scenarios: Tuple[RTABMapOdometryLoaderScenarioPolicy, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for spec, scenario in zip(_SCENARIO_SPECS, scenarios):
        if spec["blocked_scenario"]:
            result[spec["go_key"]] = scenario.blocked_scenario is True
        else:
            result[spec["go_key"]] = scenario.supported is True
    return result


def build_loader_planning_decision_v1(
    *,
    rtab_trajectory_real_file_loader_dryrun_go_verified: bool,
    rtab_odometry_fixture_go_verified: bool,
    generic_json_spatial_trace_parser_go_verified: bool,
    controlled_trial_governance_template_ref_ok: bool,
) -> RTABMapOdometryRealFileLoaderPlanningDecision:
    return RTABMapOdometryRealFileLoaderPlanningDecision(
        decision_ref="rtab_map_odometry_real_file_loader_planning_decision_v1",
        profile_ref=PROFILE_REF,
        planning_profile_count=1,
        rtab_odometry_export_file_policy_count=1,
        health_mapping_policy_count=1,
        loader_scenario_count=len(LOADER_SCENARIO_REFS),
        rtab_trajectory_real_file_loader_dryrun_go_verified=rtab_trajectory_real_file_loader_dryrun_go_verified,
        rtab_odometry_fixture_go_verified=rtab_odometry_fixture_go_verified,
        generic_json_spatial_trace_parser_go_verified=generic_json_spatial_trace_parser_go_verified,
        controlled_trial_governance_template_ref_ok=controlled_trial_governance_template_ref_ok,
        final_decision=FINAL_DECISION_GO,
    )


def build_rtab_map_odometry_real_file_loader_planning_matrix_v1() -> Dict[str, Any]:
    profile = build_loader_planning_profile_v1()
    export_file_policy = build_rtab_odometry_export_file_policy_v1()
    scenarios = build_loader_scenario_policies_v1()
    shared = build_shared_loader_policies_v1()
    decision = build_loader_planning_decision_v1(
        rtab_trajectory_real_file_loader_dryrun_go_verified=True,
        rtab_odometry_fixture_go_verified=True,
        generic_json_spatial_trace_parser_go_verified=True,
        controlled_trial_governance_template_ref_ok=True,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "loader_planning_principle_zh": LOADER_PLANNING_PRINCIPLE_ZH,
        "rtab_map_odometry_real_file_loader_planning_profile": candidate_to_dict(profile),
        "rtab_odometry_export_file_policy": candidate_to_dict(export_file_policy),
        "loader_scenario_policies": [candidate_to_dict(s) for s in scenarios],
        "shared_loader_policies": shared,
        "loader_planning_decision": candidate_to_dict(decision),
        "loader_scenario_go_map": build_loader_scenario_go_map(scenarios),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "rtab_odometry_fixture_artifact_rel": _RTAB_ODOMETRY_FIXTURE_ARTIFACT_REL,
        "rtab_trajectory_loader_dryrun_artifact_rel": _RTAB_TRAJECTORY_LOADER_DRYRUN_ARTIFACT_REL,
        "parser_artifact_rel": _PARSER_ARTIFACT_REL,
        "loader_planning_governance_rules": list(LOADER_PLANNING_GOVERNANCE_RULES),
        "universal_blocked_operations": list(UNIVERSAL_BLOCKED_OPERATIONS),
        "next_phase_ref": "Phase-RTAB-Map-Odometry-Real-File-Loader-DryRun-v1-001",
    }
