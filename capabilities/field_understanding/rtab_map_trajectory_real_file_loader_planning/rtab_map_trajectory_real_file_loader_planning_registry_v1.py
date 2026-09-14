# -*- coding: utf-8 -*-
"""RTAB-Map Trajectory Real File Loader Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.rtab_map_trajectory_real_file_loader_planning.rtab_map_trajectory_real_file_loader_planning_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXPORT_LOADER_PLANNING_REF,
    FIELD_ALIASES,
    FINAL_DECISION_GO,
    GENERIC_JSON_PARSER_REF,
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    LOADER_PLANNING_GOVERNANCE_RULES,
    LOADER_PLANNING_PRINCIPLE_ZH,
    LOADER_SCENARIO_GO_KEYS,
    LOADER_SCENARIO_REFS,
    MODEL_ADMISSION_GOVERNANCE_REF,
    PHASE_ID,
    REAL_FILE_REPLAY_DRYRUN_REF,
    RECORD_REQUIRED_FIELDS,
    RTABMapTrajectoryExportFilePolicy,
    RTABMapTrajectoryFormatAdmissionPolicy,
    RTABMapTrajectoryLoaderBoundaryPolicy,
    RTABMapTrajectoryLoaderSafetyPolicy,
    RTABMapTrajectoryLoaderScenarioPolicy,
    RTABMapTrajectoryRealFileLoaderPlanningDecision,
    RTABMapTrajectoryRealFileLoaderPlanningProfile,
    RTABMapTrajectoryToJSONTraceMappingPolicy,
    RTAB_TRAJECTORY_FIXTURE_REF,
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

REGISTRY_ID = "rtab_map_trajectory_real_file_loader_planning_registry_v1"
PROFILE_REF = "rtab_map_trajectory_real_file_loader_planning_profile_v1"

_EXPORT_LOADER_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/generic_json_spatial_trace_real_file_export_loader_planning_v1_smoke_v0/"
    "generic_json_spatial_trace_real_file_export_loader_planning_review_v1.json"
)
_RTAB_TRAJECTORY_FIXTURE_ARTIFACT_REL = (
    "_tmp_eval_out/rtab_map_trajectory_export_ingest_v1_smoke_v0/"
    "rtab_map_trajectory_export_ingest_run_and_review_v1.json"
)
_REPLAY_DRYRUN_ARTIFACT_REL = (
    "_tmp_eval_out/generic_json_spatial_trace_real_file_replay_dryrun_v1_smoke_v0/"
    "generic_json_spatial_trace_real_file_replay_dryrun_run_and_review_v1.json"
)
_PARSER_ARTIFACT_REL = (
    "_tmp_eval_out/generic_json_spatial_trace_parser_v1_smoke_v0/"
    "generic_json_spatial_trace_parser_run_and_review_v1.json"
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
        "phase_ref": EXPORT_LOADER_PLANNING_REF,
        "artifact_rel": _EXPORT_LOADER_PLANNING_ARTIFACT_REL,
        "expected_go": "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_EXPORT_LOADER_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_json_spatial_trace_real_file_export_loader_planning/"
            "generic_json_spatial_trace_real_file_export_loader_planning_types_v1.py"
        ),
        "require_go": True,
        "require_export_loader_planning_go": True,
    },
    {
        "phase_ref": RTAB_TRAJECTORY_FIXTURE_REF,
        "artifact_rel": _RTAB_TRAJECTORY_FIXTURE_ARTIFACT_REL,
        "expected_go": "RTAB_MAP_TRAJECTORY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_trajectory_export_ingest/"
            "rtab_map_trajectory_export_ingest_types_v1.py"
        ),
        "require_go": True,
        "require_rtab_trajectory_fixture_go": True,
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
        "phase_ref": TUM_REAL_FILE_LOADER_DRYRUN_REF,
        "artifact_rel": _TUM_LOADER_DRYRUN_ARTIFACT_REL,
        "expected_go": "GENERIC_TUM_REAL_FILE_LOADER_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_tum_real_file_loader_dryrun/"
            "generic_tum_real_file_loader_dryrun_types_v1.py"
        ),
        "require_go": True,
        "require_tum_loader_dryrun_go": True,
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
        "scenario_ref": "rtab_trajectory_basic_pose_motion_loader_planning",
        "input_description": "3 条有效 RTAB trajectory record",
        "output_planning_target": "three_pose_plus_two_motion_generic_json_spatial_trace",
        "scenario_requirements": (
            "candidate_only",
            "node_id_timestamp_pose_required",
        ),
        "blocked_operations": (),
        "allowed_next_step": "rtab_trajectory_real_file_loader_dryrun_planning_only",
        "go_key": "rtab_trajectory_basic_pose_motion_loader_planning_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rtab_trajectory_with_field_origin_metadata_planning",
        "input_description": "含 file_origin / export_session_id / source_chain 的 trajectory export",
        "output_planning_target": "metadata_preserved_generic_json_spatial_trace",
        "scenario_requirements": (
            "source_chain_must_not_be_lost",
            "file_origin_metadata_preserved",
        ),
        "blocked_operations": (),
        "allowed_next_step": "rtab_trajectory_real_file_loader_dryrun_planning_only",
        "go_key": "rtab_trajectory_with_field_origin_metadata_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rtab_trajectory_field_alias_compatibility_planning",
        "input_description": "使用 tx/ty/tz、stamp、id 等别名字段",
        "output_planning_target": "alias_mapped_to_standard_pose_timestamp_node_id",
        "scenario_requirements": (
            "alias_mapped_pose_timestamp_node_id",
            "must_still_enter_generic_json_spatial_trace_parser",
        ),
        "blocked_operations": (),
        "allowed_next_step": "rtab_trajectory_real_file_loader_dryrun_planning_only",
        "go_key": "rtab_trajectory_field_alias_compatibility_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rtab_trajectory_to_replay_path_planning",
        "input_description": "converted pose/motion JSON trace",
        "output_planning_target": (
            "generic_json_parser_to_candidate_bundle_to_field_task_guidance_replay_path"
        ),
        "scenario_requirements": (
            "must_not_enter_field_synthesis_directly",
            "candidate_only",
        ),
        "blocked_operations": ("backend_native_direct_to_field_synthesis",),
        "allowed_next_step": "rtab_trajectory_real_file_loader_dryrun_planning_only",
        "go_key": "rtab_trajectory_to_replay_path_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "invalid_or_unsafe_rtab_trajectory_export_blocked",
        "input_description": (
            "缺 node_id / 缺 source_chain / quaternion invalid / unsupported native RTAB object / "
            "试图读 RTAB database 或 ROS topic"
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
        "go_key": "invalid_or_unsafe_rtab_trajectory_export_blocked",
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
    if len(LOADER_SCENARIO_REFS) != 5:
        issues.append("loader_scenario_refs_count_not_5")
    if len(LOADER_SCENARIO_GO_KEYS) != 5:
        issues.append("loader_scenario_go_keys_count_not_5")
    if len(RECORD_REQUIRED_FIELDS) != 7:
        issues.append("record_required_fields_count_not_7")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 9:
        issues.append("sealed_upstream_phase_refs_count_not_9")
    if len(LOADER_PLANNING_GOVERNANCE_RULES) != 14:
        issues.append("loader_planning_governance_rules_count_not_14")
    return len(issues) == 0, issues


def _merge_blocked(*ops: str) -> Tuple[str, ...]:
    merged = list(UNIVERSAL_BLOCKED_OPERATIONS)
    for op in ops:
        if op not in merged:
            merged.append(op)
    return tuple(merged)


def build_loader_planning_profile_v1() -> RTABMapTrajectoryRealFileLoaderPlanningProfile:
    return RTABMapTrajectoryRealFileLoaderPlanningProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        generic_json_spatial_trace_parser_ref=GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        tum_real_file_loader_dryrun_ref=TUM_REAL_FILE_LOADER_DRYRUN_REF,
        rtab_trajectory_fixture_ref=RTAB_TRAJECTORY_FIXTURE_REF,
        source_format=SOURCE_FORMAT,
        target_internal_format=TARGET_INTERNAL_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        pipeline_stages=(
            "rtab_map_trajectory_export_file",
            "format_admission",
            "rtab_trajectory_to_json_trace_converter_planning",
            "generic_json_spatial_trace",
            "generic_json_spatial_trace_parser",
            "spatial_evidence_candidate_bundle",
            "field_task_guidance_candidate_replay_path",
        ),
        loader_scenario_refs=LOADER_SCENARIO_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=LOADER_PLANNING_GOVERNANCE_RULES,
    )


def build_rtab_trajectory_export_file_policy_v1() -> RTABMapTrajectoryExportFilePolicy:
    return RTABMapTrajectoryExportFilePolicy(
        policy_ref="rtab_map_trajectory_export_file_policy_v1",
        source_format=SOURCE_FORMAT,
        source_zh="RTAB-Map trajectory export 离线文件",
        priority="P0",
        record_required_fields=RECORD_REQUIRED_FIELDS,
        field_aliases=FIELD_ALIASES,
        output_candidate_types=("pose", "motion"),
        target_converter="rtab_map_trajectory_export_to_json_spatial_trace",
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
        source_chain=SOURCE_CHAIN,
        supported=True,
    )


def build_shared_loader_policies_v1() -> Dict[str, Any]:
    return {
        "format_admission_policy": candidate_to_dict(
            RTABMapTrajectoryFormatAdmissionPolicy(
                policy_ref="rtab_map_trajectory_format_admission_policy_v1",
                format_admission_required=True,
                node_id_required=True,
                timestamp_required=True,
                pose_required=True,
                confidence_required=True,
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
            RTABMapTrajectoryToJSONTraceMappingPolicy(
                policy_ref="rtab_map_trajectory_to_json_trace_mapping_policy_v1",
                target_internal_format=TARGET_INTERNAL_FORMAT,
                generic_json_output_required=True,
                generic_json_parser_required=True,
                parser_ref=GENERIC_JSON_PARSER_REF,
                target_entrypoint=TARGET_ENTRYPOINT,
                pose_trace_id_template="rtab_traj_pose_{node_id}",
                motion_trace_id_template="rtab_traj_motion_{from_node_id}_{to_node_id}",
                motion_generated_only_from_consecutive_records=True,
                field_aliases=FIELD_ALIASES,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "boundary_policy": candidate_to_dict(
            RTABMapTrajectoryLoaderBoundaryPolicy(
                policy_ref="rtab_map_trajectory_loader_boundary_policy_v1",
                backend_native_output_direct_to_field_blocked=True,
                conversion_execution_allowed=False,
                parser_must_remain_entry_validator=True,
                parser_ref=GENERIC_JSON_PARSER_REF,
                target_entrypoint=TARGET_ENTRYPOINT,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "safety_policy": candidate_to_dict(
            RTABMapTrajectoryLoaderSafetyPolicy(
                policy_ref="rtab_map_trajectory_loader_safety_policy_v1",
                rtab_database_read_blocked=True,
                ros_topic_blocked=True,
                live_rtab_runtime_blocked=True,
                backend_native_direct_to_field_blocked=True,
                field_task_guidance_replay_candidate_only=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_loader_scenario_policies_v1() -> Tuple[RTABMapTrajectoryLoaderScenarioPolicy, ...]:
    return tuple(
        RTABMapTrajectoryLoaderScenarioPolicy(
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
    scenarios: Tuple[RTABMapTrajectoryLoaderScenarioPolicy, ...],
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
    export_loader_planning_go_verified: bool,
    rtab_trajectory_fixture_go_verified: bool,
    generic_json_spatial_trace_parser_go_verified: bool,
    tum_real_file_loader_dryrun_go_verified: bool,
    controlled_trial_governance_template_ref_ok: bool,
) -> RTABMapTrajectoryRealFileLoaderPlanningDecision:
    return RTABMapTrajectoryRealFileLoaderPlanningDecision(
        decision_ref="rtab_map_trajectory_real_file_loader_planning_decision_v1",
        profile_ref=PROFILE_REF,
        planning_profile_count=1,
        rtab_trajectory_export_file_policy_count=1,
        loader_scenario_count=len(LOADER_SCENARIO_REFS),
        export_loader_planning_go_verified=export_loader_planning_go_verified,
        rtab_trajectory_fixture_go_verified=rtab_trajectory_fixture_go_verified,
        generic_json_spatial_trace_parser_go_verified=generic_json_spatial_trace_parser_go_verified,
        tum_real_file_loader_dryrun_go_verified=tum_real_file_loader_dryrun_go_verified,
        controlled_trial_governance_template_ref_ok=controlled_trial_governance_template_ref_ok,
        final_decision=FINAL_DECISION_GO,
    )


def build_rtab_map_trajectory_real_file_loader_planning_matrix_v1() -> Dict[str, Any]:
    profile = build_loader_planning_profile_v1()
    export_file_policy = build_rtab_trajectory_export_file_policy_v1()
    scenarios = build_loader_scenario_policies_v1()
    shared = build_shared_loader_policies_v1()
    decision = build_loader_planning_decision_v1(
        export_loader_planning_go_verified=True,
        rtab_trajectory_fixture_go_verified=True,
        generic_json_spatial_trace_parser_go_verified=True,
        tum_real_file_loader_dryrun_go_verified=True,
        controlled_trial_governance_template_ref_ok=True,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "loader_planning_principle_zh": LOADER_PLANNING_PRINCIPLE_ZH,
        "rtab_map_trajectory_real_file_loader_planning_profile": candidate_to_dict(profile),
        "rtab_trajectory_export_file_policy": candidate_to_dict(export_file_policy),
        "loader_scenario_policies": [candidate_to_dict(s) for s in scenarios],
        "shared_loader_policies": shared,
        "loader_planning_decision": candidate_to_dict(decision),
        "loader_scenario_go_map": build_loader_scenario_go_map(scenarios),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "rtab_trajectory_fixture_artifact_rel": _RTAB_TRAJECTORY_FIXTURE_ARTIFACT_REL,
        "tum_loader_dryrun_artifact_rel": _TUM_LOADER_DRYRUN_ARTIFACT_REL,
        "parser_artifact_rel": _PARSER_ARTIFACT_REL,
        "loader_planning_governance_rules": list(LOADER_PLANNING_GOVERNANCE_RULES),
        "universal_blocked_operations": list(UNIVERSAL_BLOCKED_OPERATIONS),
        "next_phase_ref": "Phase-RTAB-Map-Trajectory-Real-File-Loader-DryRun-v1-001",
    }
