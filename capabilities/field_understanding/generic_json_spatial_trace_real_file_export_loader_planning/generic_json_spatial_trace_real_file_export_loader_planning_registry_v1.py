# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Real File Export Loader Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.generic_json_spatial_trace_real_file_export_loader_planning.generic_json_spatial_trace_real_file_export_loader_planning_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXPORT_FILE_SOURCE_GO_KEYS,
    EXPORT_FILE_SOURCE_REFS,
    ExternalExportFileSourcePolicy,
    ExternalExportFormatAdmissionPolicy,
    ExternalExportLoaderBoundaryPolicy,
    ExternalExportLoaderPlanningDecision,
    ExternalExportLoaderSafetyPolicy,
    ExternalExportLoaderScenarioPolicy,
    ExternalExportToJSONTraceMappingPolicy,
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
    REAL_FILE_REPLAY_PLANNING_REF,
    RealFileExportLoaderPlanningProfile,
    RTAB_GRAPH_EXPORT_FIXTURE_REF,
    RTAB_ODOMETRY_EXPORT_FIXTURE_REF,
    RTAB_TRAJECTORY_EXPORT_FIXTURE_REF,
    RUNTIME_TRIAL_MODE,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TUM_TRAJECTORY_INGEST_REF,
    UNIVERSAL_BLOCKED_OPERATIONS,
    candidate_to_dict,
)

REGISTRY_ID = "generic_json_spatial_trace_real_file_export_loader_planning_registry_v1"
PROFILE_REF = "generic_json_spatial_trace_real_file_export_loader_planning_profile_v1"

_PARSER_ARTIFACT_REL = (
    "_tmp_eval_out/generic_json_spatial_trace_parser_v1_smoke_v0/"
    "generic_json_spatial_trace_parser_run_and_review_v1.json"
)
_TUM_INGEST_ARTIFACT_REL = (
    "_tmp_eval_out/generic_tum_trajectory_ingest_v1_smoke_v0/"
    "generic_tum_trajectory_ingest_run_and_review_v1.json"
)
_RTAB_TRAJECTORY_ARTIFACT_REL = (
    "_tmp_eval_out/rtab_map_trajectory_export_ingest_v1_smoke_v0/"
    "rtab_map_trajectory_export_ingest_run_and_review_v1.json"
)
_RTAB_ODOMETRY_ARTIFACT_REL = (
    "_tmp_eval_out/rtab_map_odometry_export_ingest_v1_smoke_v0/"
    "rtab_map_odometry_export_ingest_run_and_review_v1.json"
)
_RTAB_GRAPH_ARTIFACT_REL = (
    "_tmp_eval_out/rtab_map_graph_export_ingest_v1_smoke_v0/"
    "rtab_map_graph_export_ingest_run_and_review_v1.json"
)
_REPLAY_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/generic_json_spatial_trace_real_file_replay_planning_v1_smoke_v0/"
    "generic_json_spatial_trace_real_file_replay_planning_review_v1.json"
)
_REPLAY_DRYRUN_ARTIFACT_REL = (
    "_tmp_eval_out/generic_json_spatial_trace_real_file_replay_dryrun_v1_smoke_v0/"
    "generic_json_spatial_trace_real_file_replay_dryrun_run_and_review_v1.json"
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
        "phase_ref": TUM_TRAJECTORY_INGEST_REF,
        "artifact_rel": _TUM_INGEST_ARTIFACT_REL,
        "expected_go": "GENERIC_TUM_TRAJECTORY_TO_JSON_SPATIAL_TRACE_INGEST_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_tum_trajectory_ingest/"
            "generic_tum_trajectory_ingest_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": RTAB_TRAJECTORY_EXPORT_FIXTURE_REF,
        "artifact_rel": _RTAB_TRAJECTORY_ARTIFACT_REL,
        "expected_go": "RTAB_MAP_TRAJECTORY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_trajectory_export_ingest/"
            "rtab_map_trajectory_export_ingest_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": RTAB_ODOMETRY_EXPORT_FIXTURE_REF,
        "artifact_rel": _RTAB_ODOMETRY_ARTIFACT_REL,
        "expected_go": "RTAB_MAP_ODOMETRY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_odometry_export_ingest/"
            "rtab_map_odometry_export_ingest_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": RTAB_GRAPH_EXPORT_FIXTURE_REF,
        "artifact_rel": _RTAB_GRAPH_ARTIFACT_REL,
        "expected_go": "RTAB_MAP_GRAPH_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_graph_export_ingest/"
            "rtab_map_graph_export_ingest_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": REAL_FILE_REPLAY_PLANNING_REF,
        "artifact_rel": _REPLAY_PLANNING_ARTIFACT_REL,
        "expected_go": "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_CONTROLLED_REPLAY_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_json_spatial_trace_real_file_replay_planning/"
            "generic_json_spatial_trace_real_file_replay_planning_types_v1.py"
        ),
        "require_go": True,
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
        "require_dryrun_go": True,
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

_EXPORT_FILE_SOURCE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "source_ref": "tum_trajectory_file",
        "source_format": "TUM trajectory text",
        "source_zh": "真实或本地 TUM trajectory 文本文件",
        "priority": "P0",
        "expected_fields": ("timestamp", "tx", "ty", "tz", "qx", "qy", "qz", "qw"),
        "output_candidate_types": ("pose", "motion"),
        "target_converter": "generic_tum_trajectory_to_json_spatial_trace",
        "prohibited_operations": (
            "direct_candidate_bundle_write",
            "bypass_generic_json_spatial_trace_parser",
        ),
        "go_key": "tum_trajectory_file_supported",
    },
    {
        "source_ref": "rtab_map_trajectory_export_file",
        "source_format": "RTAB trajectory export",
        "source_zh": "RTAB-Map trajectory export 离线文件",
        "priority": "P0",
        "expected_fields": ("node_id", "timestamp", "pose", "confidence", "source_chain"),
        "output_candidate_types": ("pose", "motion"),
        "target_converter": "rtab_map_trajectory_export_to_json_spatial_trace",
        "prohibited_operations": (
            "rtab_database_read",
            "ros_topic_read",
            "live_rtab_runtime",
        ),
        "go_key": "rtab_trajectory_export_file_supported",
    },
    {
        "source_ref": "rtab_map_odometry_export_file",
        "source_format": "RTAB odometry export",
        "source_zh": "RTAB-Map odometry export 离线文件",
        "priority": "P1",
        "expected_fields": (
            "node_id",
            "timestamp",
            "odom_pose",
            "tracking_state",
            "confidence",
            "source_chain",
        ),
        "output_candidate_types": ("pose", "motion", "health"),
        "target_converter": "rtab_map_odometry_export_to_json_spatial_trace",
        "prohibited_operations": (
            "live_odometry",
            "live_sensor_trigger",
            "direct_action_safety_decision",
        ),
        "go_key": "rtab_odometry_export_file_supported",
    },
    {
        "source_ref": "rtab_map_graph_export_file",
        "source_format": "RTAB graph export",
        "source_zh": "RTAB-Map graph export 离线文件",
        "priority": "P1",
        "expected_fields": (
            "nodes",
            "edges",
            "loop_closure_hint",
            "confidence",
            "source_chain",
        ),
        "output_candidate_types": ("anchor", "relocalization", "drift"),
        "target_converter": "rtab_map_graph_export_to_json_spatial_trace",
        "prohibited_operations": (
            "relocalization_runtime_trust_restore",
            "real_relocalization",
            "map_fact_write",
        ),
        "go_key": "rtab_graph_export_file_supported",
    },
    {
        "source_ref": "luna_generic_json_spatial_trace_file",
        "source_format": "Luna Generic JSON Spatial Trace",
        "source_zh": "Luna 标准 Generic JSON Spatial Trace 文件",
        "priority": "P0",
        "expected_fields": (
            "trace_id",
            "candidate_type",
            "confidence",
            "source_chain",
            "field_synthesis_entrypoint",
        ),
        "output_candidate_types": ("passthrough_validation",),
        "target_converter": "none_required",
        "prohibited_operations": (
            "backend_native_bypass",
            "unsupported_candidate_type",
        ),
        "go_key": "luna_generic_json_spatial_trace_file_supported",
    },
)

_SCENARIO_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "scenario_ref": "tum_file_loader_to_json_trace_planning",
        "input_description": "真实或本地 TUM 文件",
        "output_planning_target": "tum_rows_to_pose_motion_json_trace",
        "scenario_requirements": (
            "quaternion_validation_required",
            "source_chain_inject_or_preserve",
            "file_origin_metadata_preserve",
        ),
        "blocked_operations": (),
        "allowed_next_step": "tum_real_file_loader_dryrun_planning_only",
        "go_key": "tum_file_loader_to_json_trace_planning_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rtab_trajectory_file_loader_to_json_trace_planning",
        "input_description": "RTAB trajectory export file",
        "output_planning_target": "trajectory_records_to_pose_motion_json_trace",
        "scenario_requirements": (
            "node_id_required",
            "timestamp_required",
            "pose_required",
            "source_chain_required",
        ),
        "blocked_operations": ("rtab_database_read", "ros_topic_read"),
        "allowed_next_step": "rtab_trajectory_loader_dryrun_planning_only",
        "go_key": "rtab_trajectory_loader_to_json_trace_planning_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rtab_odometry_file_loader_to_json_trace_planning",
        "input_description": "RTAB odometry export file",
        "output_planning_target": "odometry_records_to_pose_motion_health_json_trace",
        "scenario_requirements": (
            "tracking_state_degraded_health_candidate_only",
            "must_not_directly_block_or_allow_action",
        ),
        "blocked_operations": ("direct_action_from_health", "live_odometry"),
        "allowed_next_step": "rtab_odometry_loader_dryrun_planning_only",
        "go_key": "rtab_odometry_loader_to_json_trace_planning_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rtab_graph_file_loader_to_json_trace_planning",
        "input_description": "RTAB graph export file",
        "output_planning_target": "nodes_edges_to_anchor_relocalization_drift_json_trace",
        "scenario_requirements": (
            "loop_closure_relocalization_drift_candidate_only",
            "must_not_restore_runtime_trust",
        ),
        "blocked_operations": ("relocalization_runtime_trust_restore", "map_fact_write"),
        "allowed_next_step": "rtab_graph_loader_dryrun_planning_only",
        "go_key": "rtab_graph_loader_to_json_trace_planning_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "generic_json_trace_passthrough_loader_planning",
        "input_description": "Luna Generic JSON Spatial Trace 文件",
        "output_planning_target": "schema_validation_and_parser_replay_planning",
        "scenario_requirements": (
            "no_duplicate_conversion",
            "must_not_bypass_parser",
        ),
        "blocked_operations": ("duplicate_conversion", "bypass_parser"),
        "allowed_next_step": "real_file_controlled_replay_dryrun_path",
        "go_key": "generic_json_trace_passthrough_loader_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "invalid_or_unsafe_export_file_blocked",
        "input_description": (
            "缺 source_chain、格式不明、unsupported candidate_type、试图直进 field_synthesis"
        ),
        "output_planning_target": "blocked_rejected",
        "scenario_requirements": ("must_not_enter_converter_or_parser_path",),
        "blocked_operations": ("converter_path", "parser_path", "field_synthesis_direct"),
        "allowed_next_step": "rejection_only",
        "go_key": "invalid_or_unsafe_export_file_blocked",
        "blocked_scenario": True,
    },
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "export_file_source_refs": EXPORT_FILE_SOURCE_REFS,
    "export_file_source_go_keys": EXPORT_FILE_SOURCE_GO_KEYS,
    "loader_scenario_refs": LOADER_SCENARIO_REFS,
    "loader_scenario_go_keys": LOADER_SCENARIO_GO_KEYS,
    "loader_planning_governance_rules": LOADER_PLANNING_GOVERNANCE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
    "universal_blocked_operations": UNIVERSAL_BLOCKED_OPERATIONS,
}


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(EXPORT_FILE_SOURCE_REFS) != 5:
        issues.append("export_file_source_refs_count_not_5")
    if len(LOADER_SCENARIO_REFS) != 6:
        issues.append("loader_scenario_refs_count_not_6")
    if len(EXPORT_FILE_SOURCE_GO_KEYS) != 5:
        issues.append("export_file_source_go_keys_count_not_5")
    if len(LOADER_SCENARIO_GO_KEYS) != 6:
        issues.append("loader_scenario_go_keys_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 11:
        issues.append("sealed_upstream_phase_refs_count_not_11")
    if len(LOADER_PLANNING_GOVERNANCE_RULES) != 14:
        issues.append("loader_planning_governance_rules_count_not_14")
    return len(issues) == 0, issues


def _merge_blocked(*ops: str) -> Tuple[str, ...]:
    merged = list(UNIVERSAL_BLOCKED_OPERATIONS)
    for op in ops:
        if op not in merged:
            merged.append(op)
    return tuple(merged)


def build_export_loader_planning_profile_v1() -> RealFileExportLoaderPlanningProfile:
    return RealFileExportLoaderPlanningProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        generic_json_spatial_trace_parser_ref=GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        real_file_replay_dryrun_ref=REAL_FILE_REPLAY_DRYRUN_REF,
        target_internal_format=TARGET_INTERNAL_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        pipeline_stages=(
            "external_export_file",
            "format_admission",
            "export_to_json_trace_converter_planning",
            "generic_json_spatial_trace",
            "generic_json_spatial_trace_parser",
            "real_file_controlled_replay_dryrun_path",
        ),
        export_file_source_refs=EXPORT_FILE_SOURCE_REFS,
        loader_scenario_refs=LOADER_SCENARIO_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=LOADER_PLANNING_GOVERNANCE_RULES,
    )


def build_external_export_file_source_policies_v1() -> Tuple[ExternalExportFileSourcePolicy, ...]:
    return tuple(
        ExternalExportFileSourcePolicy(
            source_ref=spec["source_ref"],
            source_format=spec["source_format"],
            source_zh=spec["source_zh"],
            priority=spec["priority"],
            expected_fields=spec["expected_fields"],
            output_candidate_types=spec["output_candidate_types"],
            target_converter=spec["target_converter"],
            prohibited_operations=spec["prohibited_operations"],
            blocked_operations=_merge_blocked(*spec["prohibited_operations"]),
            requires_format_admission=True,
            requires_file_origin_metadata=True,
            requires_source_chain=True,
            source_chain=SOURCE_CHAIN,
            supported=True,
        )
        for spec in _EXPORT_FILE_SOURCE_SPECS
    )


def build_shared_loader_policies_v1() -> Dict[str, Any]:
    return {
        "format_admission_policy": candidate_to_dict(
            ExternalExportFormatAdmissionPolicy(
                policy_ref="external_export_format_admission_policy_v1",
                format_admission_required=True,
                file_origin_metadata_required=True,
                source_chain_required=True,
                unsupported_candidate_type_rejected=True,
                missing_source_chain_rejected=True,
                tum_quaternion_validation_required=True,
                rtab_node_id_required=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "mapping_policy": candidate_to_dict(
            ExternalExportToJSONTraceMappingPolicy(
                policy_ref="external_export_to_json_trace_mapping_policy_v1",
                target_internal_format=TARGET_INTERNAL_FORMAT,
                generic_json_output_required=True,
                generic_json_parser_required=True,
                parser_ref=GENERIC_JSON_PARSER_REF,
                target_entrypoint=TARGET_ENTRYPOINT,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "boundary_policy": candidate_to_dict(
            ExternalExportLoaderBoundaryPolicy(
                policy_ref="external_export_loader_boundary_policy_v1",
                backend_native_output_direct_to_field_blocked=True,
                conversion_execution_allowed=False,
                parser_must_remain_entry_validator=True,
                parser_ref=GENERIC_JSON_PARSER_REF,
                target_entrypoint=TARGET_ENTRYPOINT,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "safety_policy": candidate_to_dict(
            ExternalExportLoaderSafetyPolicy(
                policy_ref="external_export_loader_safety_policy_v1",
                rtab_loop_closure_does_not_restore_runtime_trust=True,
                gps_does_not_override_field_identity=True,
                tracking_state_degraded_health_candidate_only=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_loader_scenario_policies_v1() -> Tuple[ExternalExportLoaderScenarioPolicy, ...]:
    return tuple(
        ExternalExportLoaderScenarioPolicy(
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


def build_export_file_source_go_map(
    policies: Tuple[ExternalExportFileSourcePolicy, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for spec, policy in zip(_EXPORT_FILE_SOURCE_SPECS, policies):
        result[spec["go_key"]] = policy.supported is True
    return result


def build_loader_scenario_go_map(
    scenarios: Tuple[ExternalExportLoaderScenarioPolicy, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for spec, scenario in zip(_SCENARIO_SPECS, scenarios):
        if spec["blocked_scenario"]:
            result[spec["go_key"]] = scenario.blocked_scenario is True
        else:
            result[spec["go_key"]] = scenario.supported is True
    return result


def build_export_loader_planning_decision_v1(
    *,
    controlled_trial_governance_template_ref_ok: bool,
    real_file_replay_dryrun_go_verified: bool,
    generic_json_spatial_trace_parser_go_verified: bool,
) -> ExternalExportLoaderPlanningDecision:
    return ExternalExportLoaderPlanningDecision(
        decision_ref="external_export_loader_planning_decision_v1",
        profile_ref=PROFILE_REF,
        planning_profile_count=1,
        export_file_source_policy_count=len(EXPORT_FILE_SOURCE_REFS),
        loader_scenario_count=len(LOADER_SCENARIO_REFS),
        controlled_trial_governance_template_ref_ok=controlled_trial_governance_template_ref_ok,
        real_file_replay_dryrun_go_verified=real_file_replay_dryrun_go_verified,
        generic_json_spatial_trace_parser_go_verified=generic_json_spatial_trace_parser_go_verified,
        final_decision=FINAL_DECISION_GO,
    )


def build_generic_json_spatial_trace_real_file_export_loader_planning_matrix_v1() -> Dict[str, Any]:
    profile = build_export_loader_planning_profile_v1()
    export_sources = build_external_export_file_source_policies_v1()
    scenarios = build_loader_scenario_policies_v1()
    shared = build_shared_loader_policies_v1()
    decision = build_export_loader_planning_decision_v1(
        controlled_trial_governance_template_ref_ok=True,
        real_file_replay_dryrun_go_verified=True,
        generic_json_spatial_trace_parser_go_verified=True,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "loader_planning_principle_zh": LOADER_PLANNING_PRINCIPLE_ZH,
        "real_file_export_loader_planning_profile": candidate_to_dict(profile),
        "external_export_file_source_policies": [candidate_to_dict(p) for p in export_sources],
        "loader_scenario_policies": [candidate_to_dict(s) for s in scenarios],
        "shared_loader_policies": shared,
        "export_loader_planning_decision": candidate_to_dict(decision),
        "export_file_source_go_map": build_export_file_source_go_map(export_sources),
        "loader_scenario_go_map": build_loader_scenario_go_map(scenarios),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "replay_dryrun_artifact_rel": _REPLAY_DRYRUN_ARTIFACT_REL,
        "parser_artifact_rel": _PARSER_ARTIFACT_REL,
        "loader_planning_governance_rules": list(LOADER_PLANNING_GOVERNANCE_RULES),
        "universal_blocked_operations": list(UNIVERSAL_BLOCKED_OPERATIONS),
        "next_phase_ref": "Phase-Generic-TUM-Real-File-Loader-DryRun-v1-001",
    }
