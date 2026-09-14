# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Real File Controlled Replay Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.generic_json_spatial_trace_real_file_replay_planning.generic_json_spatial_trace_real_file_replay_planning_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_STATUS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FINAL_DECISION_GO,
    GENERIC_JSON_PARSER_REF,
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    GOVERNANCE_CLOSURE_REF,
    INPUT_SOURCE_GO_KEYS,
    ISSUANCE_PACKAGE_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    REPLAY_PLANNING_GOVERNANCE_RULES,
    REPLAY_PLANNING_PRINCIPLE_ZH,
    REPLAY_SCENARIO_GO_KEYS,
    REPLAY_SCENARIO_REFS,
    REAL_FILE_INPUT_SOURCE_REFS,
    RealFileFormatAdmissionPolicy,
    RealFileInputSourcePolicy,
    RealFileReplayBoundaryPolicy,
    RealFileReplayObservationLogPolicy,
    RealFileReplayPlanningDecision,
    RealFileReplaySafetyPolicy,
    RealFileReplayScenarioPolicy,
    GenericJSONSpatialTraceRealFileReplayPlanningProfile,
    RUNTIME_TRIAL_MODE,
    SEALED_UPSTREAM_PHASE_REFS,
    SLAM_SPATIAL_EVIDENCE_CHAIN_REF,
    SOURCE_CHAIN,
    TARGET_ENTRYPOINT,
    UNIVERSAL_BLOCKED_OPERATIONS,
    candidate_to_dict,
)

REGISTRY_ID = "generic_json_spatial_trace_real_file_replay_planning_registry_v1"
PROFILE_REF = "generic_json_spatial_trace_real_file_replay_planning_profile_v1"
OBSERVATION_LOG_POLICY_REF = "real_file_replay_observation_log_policy_v1"

_PARSER_ARTIFACT_REL = (
    "_tmp_eval_out/generic_json_spatial_trace_parser_v1_smoke_v0/"
    "generic_json_spatial_trace_parser_run_and_review_v1.json"
)
_SLAM_CHAIN_ARTIFACT_REL = (
    "_tmp_eval_out/slam_spatial_evidence_chain_closure_v1_smoke_v0/"
    "slam_spatial_evidence_chain_closure_review_v1.json"
)
_CHAIN_CLOSURE_ARTIFACT_REL = (
    "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
    "field_task_guidance_safety_chain_closure_review_v1.json"
)
_GOVERNANCE_CLOSURE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"
)
_ISSUANCE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_issuance_package_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_issuance_package_review_v1.json"
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
        "phase_ref": SLAM_SPATIAL_EVIDENCE_CHAIN_REF,
        "artifact_rel": _SLAM_CHAIN_ARTIFACT_REL,
        "expected_go": "SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/slam_spatial_evidence_chain_closure/"
            "slam_spatial_evidence_chain_closure_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": PHASE_ONE_CHAIN_REF,
        "artifact_rel": _CHAIN_CLOSURE_ARTIFACT_REL,
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
            "field_task_guidance_safety_chain_closure_types_v1.py"
        ),
        "require_go": True,
        "require_phase_one_chain_sealed": True,
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
        "require_governance_sealed": True,
    },
    {
        "phase_ref": ISSUANCE_PACKAGE_REF,
        "artifact_rel": _ISSUANCE_ARTIFACT_REL,
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_ISSUANCE_PACKAGE_GO",
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_issuance_package/"
            "phase_one_environment_cognition_runtime_trial_issuance_package_types_v1.py"
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

_INPUT_SOURCE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "source_ref": "generic_json_spatial_trace_file",
        "source_zh": "Luna 标准 JSON trace 文件",
        "priority": "P0",
        "allowed_plan_operations": (
            "schema_validation_planning",
            "parser_replay_planning",
        ),
        "blocked_operations": (
            "direct_candidate_bundle_write",
            "direct_field_synthesis_entry",
        ),
        "go_key": "generic_json_spatial_trace_file_supported",
    },
    {
        "source_ref": "tum_trajectory_converted_json_trace_file",
        "source_zh": "真实 TUM trajectory 经 ingest 转换后的 JSON trace",
        "priority": "P0",
        "allowed_plan_operations": ("pose_motion_replay_planning",),
        "blocked_operations": ("bypass_generic_json_spatial_trace_parser",),
        "go_key": "tum_converted_json_trace_file_supported",
    },
    {
        "source_ref": "rtab_map_trajectory_export_converted_json_trace_file",
        "source_zh": "RTAB trajectory export 转换后的 JSON trace",
        "priority": "P0",
        "allowed_plan_operations": ("pose_motion_replay_planning",),
        "blocked_operations": ("rtab_database_read", "ros_topic_read"),
        "go_key": "rtab_trajectory_converted_json_trace_file_supported",
    },
    {
        "source_ref": "rtab_map_odometry_export_converted_json_trace_file",
        "source_zh": "RTAB odometry export 转换后的 JSON trace",
        "priority": "P1",
        "allowed_plan_operations": ("pose_motion_health_replay_planning",),
        "blocked_operations": ("live_odometry", "live_sensor_trigger"),
        "go_key": "rtab_odometry_converted_json_trace_file_supported",
    },
    {
        "source_ref": "rtab_map_graph_export_converted_json_trace_file",
        "source_zh": "RTAB graph export 转换后的 JSON trace",
        "priority": "P1",
        "allowed_plan_operations": (
            "anchor_relocalization_drift_replay_planning",
        ),
        "blocked_operations": ("relocalization_runtime_trust_restore",),
        "go_key": "rtab_graph_converted_json_trace_file_supported",
    },
)

_SCENARIO_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "scenario_ref": "real_file_pose_motion_replay_low_risk",
        "input_trace_types": ("pose", "motion"),
        "output_planning_target": "spatial_evidence_candidate_bundle_replay_candidate",
        "target_field_scenarios": ("mall_find_entrance", "home_return"),
        "scenario_requirements": ("candidate_only",),
        "blocked_operations": (),
        "allowed_next_step": "controlled_replay_dryrun_planning_only",
        "go_key": "real_file_pose_motion_replay_low_risk_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "real_file_odometry_health_replay",
        "input_trace_types": ("pose", "motion", "health"),
        "output_planning_target": "field_task_replay_path_health_candidate_risk",
        "target_field_scenarios": (),
        "scenario_requirements": (
            "health_must_not_directly_block_or_allow_action",
            "health_generates_candidate_risk_only",
        ),
        "blocked_operations": ("direct_action_from_health",),
        "allowed_next_step": "controlled_replay_dryrun_planning_only",
        "go_key": "real_file_odometry_health_replay_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "real_file_anchor_relocalization_drift_replay",
        "input_trace_types": ("anchor", "relocalization", "drift"),
        "output_planning_target": "anchor_relocalization_drift_candidate_replay",
        "target_field_scenarios": (),
        "scenario_requirements": ("relocalization_must_not_restore_runtime_trust",),
        "blocked_operations": ("relocalization_runtime_trust_restore",),
        "allowed_next_step": "controlled_replay_dryrun_planning_only",
        "go_key": "real_file_anchor_relocalization_drift_replay_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "real_file_spatial_odometry_fusion_replay",
        "input_trace_types": ("gps_stub", "slam_local_odometry", "graph_anchor_candidate"),
        "output_planning_target": "spatial_odometry_fusion_candidate_replay",
        "target_field_scenarios": (),
        "scenario_requirements": (
            "gps_must_not_override_field_identity",
            "conflict_generates_conflict_candidate",
        ),
        "blocked_operations": ("gps_override_field_identity",),
        "allowed_next_step": "controlled_replay_dryrun_planning_only",
        "go_key": "real_file_spatial_odometry_fusion_replay_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "real_file_field_task_guidance_replay_path",
        "input_trace_types": ("spatial_evidence_candidate_refs",),
        "output_planning_target": "field_task_guidance_candidate_replay_path",
        "target_field_scenarios": (),
        "scenario_requirements": (
            "guidance_candidate_must_not_become_runtime_navigation",
            "candidate_only",
        ),
        "blocked_operations": ("runtime_navigation",),
        "allowed_next_step": "controlled_replay_dryrun_planning_only",
        "go_key": "real_file_field_task_guidance_replay_path_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "invalid_or_untrusted_file_blocked",
        "input_trace_types": (
            "schema_invalid",
            "missing_source_chain",
            "untrusted_file_source",
            "unsupported_candidate_type",
        ),
        "output_planning_target": "blocked_rejected",
        "target_field_scenarios": (),
        "scenario_requirements": ("must_not_enter_parser_replay_path",),
        "blocked_operations": ("parser_replay_path",),
        "allowed_next_step": "rejection_only",
        "go_key": "invalid_or_untrusted_file_blocked",
        "blocked_scenario": True,
    },
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "real_file_input_source_refs": REAL_FILE_INPUT_SOURCE_REFS,
    "input_source_go_keys": INPUT_SOURCE_GO_KEYS,
    "replay_scenario_refs": REPLAY_SCENARIO_REFS,
    "replay_scenario_go_keys": REPLAY_SCENARIO_GO_KEYS,
    "replay_planning_governance_rules": REPLAY_PLANNING_GOVERNANCE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
    "universal_blocked_operations": UNIVERSAL_BLOCKED_OPERATIONS,
}


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(REAL_FILE_INPUT_SOURCE_REFS) != 5:
        issues.append("real_file_input_source_refs_count_not_5")
    if len(REPLAY_SCENARIO_REFS) != 6:
        issues.append("replay_scenario_refs_count_not_6")
    if len(INPUT_SOURCE_GO_KEYS) != 5:
        issues.append("input_source_go_keys_count_not_5")
    if len(REPLAY_SCENARIO_GO_KEYS) != 6:
        issues.append("replay_scenario_go_keys_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 8:
        issues.append("sealed_upstream_phase_refs_count_not_8")
    if len(REPLAY_PLANNING_GOVERNANCE_RULES) != 14:
        issues.append("replay_planning_governance_rules_count_not_14")
    return len(issues) == 0, issues


def _merge_blocked(*ops: str) -> Tuple[str, ...]:
    merged = list(UNIVERSAL_BLOCKED_OPERATIONS)
    for op in ops:
        if op not in merged:
            merged.append(op)
    return tuple(merged)


def build_replay_planning_profile_v1() -> GenericJSONSpatialTraceRealFileReplayPlanningProfile:
    return GenericJSONSpatialTraceRealFileReplayPlanningProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        generic_json_spatial_trace_parser_ref=GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        target_entrypoint=TARGET_ENTRYPOINT,
        phase_one_chain_status=PHASE_ONE_CHAIN_STATUS,
        controlled_runtime_trial_governance_status=CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_STATUS,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        pipeline_stages=(
            "real_file_or_exported_trace",
            "generic_json_spatial_trace_file_loader_planning",
            "generic_json_spatial_trace_parser",
            "spatial_evidence_candidate_bundle",
            "spatial_odometry_fusion_candidate",
            "field_task_guidance_candidate_replay_path",
        ),
        real_file_input_source_refs=REAL_FILE_INPUT_SOURCE_REFS,
        replay_scenario_refs=REPLAY_SCENARIO_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=REPLAY_PLANNING_GOVERNANCE_RULES,
        candidate_only_source_chain_required=CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    )


def build_real_file_input_source_policies_v1() -> Tuple[RealFileInputSourcePolicy, ...]:
    return tuple(
        RealFileInputSourcePolicy(
            source_ref=spec["source_ref"],
            source_zh=spec["source_zh"],
            priority=spec["priority"],
            allowed_plan_operations=spec["allowed_plan_operations"],
            blocked_operations=_merge_blocked(*spec["blocked_operations"]),
            requires_parser_reuse=True,
            requires_source_admission=True,
            requires_file_origin_metadata=True,
            source_chain=SOURCE_CHAIN,
            supported=True,
        )
        for spec in _INPUT_SOURCE_SPECS
    )


def build_shared_replay_policies_v1() -> Dict[str, Any]:
    return {
        "format_admission_policy": candidate_to_dict(
            RealFileFormatAdmissionPolicy(
                policy_ref="real_file_format_admission_policy_v1",
                real_file_source_admission_required=True,
                file_origin_metadata_required=True,
                source_chain_required=True,
                unsupported_candidate_type_rejected=True,
                missing_source_chain_rejected=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "replay_boundary_policy": candidate_to_dict(
            RealFileReplayBoundaryPolicy(
                policy_ref="real_file_replay_boundary_policy_v1",
                generic_json_parser_reused=True,
                backend_native_output_direct_to_field_blocked=True,
                parser_ref=GENERIC_JSON_PARSER_REF,
                target_entrypoint=TARGET_ENTRYPOINT,
                output_candidate_contract_ref=OUTPUT_CANDIDATE_CONTRACT_REF,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "safety_policy": candidate_to_dict(
            RealFileReplaySafetyPolicy(
                policy_ref="real_file_replay_safety_policy_v1",
                relocalization_does_not_restore_runtime_trust=True,
                gps_does_not_override_field_identity=True,
                candidate_only_replay_path_enforced=True,
                health_generates_candidate_risk_only=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "observation_log_policy": candidate_to_dict(
            RealFileReplayObservationLogPolicy(
                policy_ref=OBSERVATION_LOG_POLICY_REF,
                log_file_origin_metadata=True,
                log_source_admission_result=True,
                log_parser_replay_planning_status=True,
                log_blocked_operations=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_replay_scenario_policies_v1() -> Tuple[RealFileReplayScenarioPolicy, ...]:
    return tuple(
        RealFileReplayScenarioPolicy(
            scenario_ref=spec["scenario_ref"],
            input_trace_types=spec["input_trace_types"],
            output_planning_target=spec["output_planning_target"],
            target_field_scenarios=spec["target_field_scenarios"],
            scenario_requirements=spec["scenario_requirements"],
            blocked_operations=_merge_blocked(*spec["blocked_operations"]),
            allowed_next_step=spec["allowed_next_step"],
            source_chain=SOURCE_CHAIN,
            supported=not spec["blocked_scenario"],
            blocked_scenario=spec["blocked_scenario"],
        )
        for spec in _SCENARIO_SPECS
    )


def build_input_source_go_map(
    policies: Tuple[RealFileInputSourcePolicy, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for spec, policy in zip(_INPUT_SOURCE_SPECS, policies):
        result[spec["go_key"]] = policy.supported is True
    return result


def build_replay_scenario_go_map(
    scenarios: Tuple[RealFileReplayScenarioPolicy, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for spec, scenario in zip(_SCENARIO_SPECS, scenarios):
        if spec["blocked_scenario"]:
            result[spec["go_key"]] = scenario.blocked_scenario is True
        else:
            result[spec["go_key"]] = scenario.supported is True
    return result


def build_replay_planning_decision_v1(
    *,
    controlled_trial_governance_template_ref_ok: bool,
    phase_one_chain_sealed_verified: bool,
    controlled_runtime_trial_governance_sealed_verified: bool,
    generic_json_spatial_trace_parser_go_verified: bool,
) -> RealFileReplayPlanningDecision:
    return RealFileReplayPlanningDecision(
        decision_ref="real_file_replay_planning_decision_v1",
        profile_ref=PROFILE_REF,
        planning_profile_count=1,
        real_file_input_source_policy_count=len(REAL_FILE_INPUT_SOURCE_REFS),
        replay_scenario_count=len(REPLAY_SCENARIO_REFS),
        controlled_trial_governance_template_ref_ok=controlled_trial_governance_template_ref_ok,
        phase_one_chain_sealed_verified=phase_one_chain_sealed_verified,
        controlled_runtime_trial_governance_sealed_verified=controlled_runtime_trial_governance_sealed_verified,
        generic_json_spatial_trace_parser_go_verified=generic_json_spatial_trace_parser_go_verified,
        final_decision=FINAL_DECISION_GO,
    )


def build_generic_json_spatial_trace_real_file_replay_planning_matrix_v1() -> Dict[str, Any]:
    profile = build_replay_planning_profile_v1()
    input_sources = build_real_file_input_source_policies_v1()
    scenarios = build_replay_scenario_policies_v1()
    shared = build_shared_replay_policies_v1()
    decision = build_replay_planning_decision_v1(
        controlled_trial_governance_template_ref_ok=True,
        phase_one_chain_sealed_verified=True,
        controlled_runtime_trial_governance_sealed_verified=True,
        generic_json_spatial_trace_parser_go_verified=True,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "replay_planning_principle_zh": REPLAY_PLANNING_PRINCIPLE_ZH,
        "generic_json_spatial_trace_real_file_replay_planning_profile": candidate_to_dict(profile),
        "real_file_input_source_policies": [candidate_to_dict(p) for p in input_sources],
        "replay_scenario_policies": [candidate_to_dict(s) for s in scenarios],
        "shared_replay_policies": shared,
        "replay_planning_decision": candidate_to_dict(decision),
        "input_source_go_map": build_input_source_go_map(input_sources),
        "replay_scenario_go_map": build_replay_scenario_go_map(scenarios),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "governance_closure_artifact_rel": _GOVERNANCE_CLOSURE_ARTIFACT_REL,
        "parser_artifact_rel": _PARSER_ARTIFACT_REL,
        "replay_planning_governance_rules": list(REPLAY_PLANNING_GOVERNANCE_RULES),
        "universal_blocked_operations": list(UNIVERSAL_BLOCKED_OPERATIONS),
        "next_phase_ref": "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-DryRun-v1-001",
    }
