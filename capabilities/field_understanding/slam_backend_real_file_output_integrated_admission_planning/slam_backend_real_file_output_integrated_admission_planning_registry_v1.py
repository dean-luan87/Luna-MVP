# -*- coding: utf-8 -*-
"""SLAM Backend Real File Output Integrated Admission Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.slam_backend_real_file_output_integrated_admission_planning.slam_backend_real_file_output_integrated_admission_planning_types_v1 import (
    ALLOWED_USE_VALUES,
    BACKEND_SOURCE_IDS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    GENERIC_JSON_PARSER_PHASE_REF,
    GENERIC_JSON_PARSER_REF,
    GENERIC_TUM_DRYRUN_REF,
    GOVERNANCE_CLOSURE_REF,
    INTEGRATED_SCENARIO_REFS,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    LICENSE_BOUNDARY_VALUES,
    LICENSE_OPEN_VERIFIED,
    LICENSE_TECHNICAL_REFERENCE_ONLY,
    MODEL_ADMISSION_GOVERNANCE_REF,
    PLANNING_GOVERNANCE_RULES,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF,
    RUNTIME_TRIAL_MODE,
    SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_REF,
    SOURCE_FAMILY,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    SLAMBackendIntegratedScenarioPolicy,
    SLAMBackendLicenseBoundaryPolicy,
    SLAMBackendOutputFormatAdmissionPolicy,
    SLAMBackendOutputSourcePolicy,
    SLAMBackendRealFileOutputAdmissionPlanningProfile,
    SLAMBackendReplayBoundaryPolicy,
    SLAMBackendSafetyBoundaryPolicy,
    SLAMBackendToGenericJSONTraceMappingPolicy,
    candidate_to_dict,
)

REGISTRY_ID = "slam_backend_real_file_output_integrated_admission_planning_registry_v1"
PROFILE_REF = "slam_backend_real_file_output_integrated_admission_planning_profile_v1"

# --------------------------------------------------------------------------- #
# Backend output source policies
# --------------------------------------------------------------------------- #
_SOURCE_POLICIES: Tuple[SLAMBackendOutputSourcePolicy, ...] = (
    SLAMBackendOutputSourcePolicy(
        source_id="generic_tum_trajectory",
        backend_family="generic_trajectory",
        output_type="trajectory",
        priority="P0",
        candidate_types=("pose", "motion"),
        allowed_use="baseline_reuse",
        license_boundary=LICENSE_OPEN_VERIFIED,
        source_chain_required=True,
        confidence_required=True,
        license_ref_required=True,
        backend_origin_required=True,
        adapter_required=True,
        native_output_direct_to_field_blocked=True,
        status="already_dryrun_verified",
        upstream_ref=GENERIC_TUM_DRYRUN_REF,
        note="Baseline reuse of sealed TUM real-file loader dry-run.",
    ),
    SLAMBackendOutputSourcePolicy(
        source_id="rtab_map_multi_export",
        backend_family="rgbd_graph_slam",
        output_type="trajectory / odometry / graph",
        priority="P0",
        candidate_types=("pose", "motion", "health", "anchor", "relocalization", "drift"),
        allowed_use="baseline_reuse",
        license_boundary=LICENSE_OPEN_VERIFIED,
        source_chain_required=True,
        confidence_required=True,
        license_ref_required=True,
        backend_origin_required=True,
        adapter_required=True,
        native_output_direct_to_field_blocked=True,
        status="already_integrated_closure_verified",
        upstream_ref=RTAB_MULTI_EXPORT_CLOSURE_REF,
        note="Baseline reuse of sealed RTAB multi-export spatial evidence closure.",
    ),
    SLAMBackendOutputSourcePolicy(
        source_id="openvins_trajectory_export",
        backend_family="vio",
        output_type="trajectory / imu_visual_odometry",
        priority="P1",
        candidate_types=("pose", "motion", "health"),
        allowed_use="adapter_planning_only",
        license_boundary=LICENSE_TECHNICAL_REFERENCE_ONLY,
        source_chain_required=True,
        confidence_required=True,
        license_ref_required=True,
        backend_origin_required=True,
        adapter_required=True,
        native_output_direct_to_field_blocked=True,
        note="No GPL code copy / no runtime dependency unless license cleared; VIO pose not field identity.",
    ),
    SLAMBackendOutputSourcePolicy(
        source_id="orb_slam3_trajectory_export",
        backend_family="visual_slam",
        output_type="keyframe trajectory / camera trajectory / map point summary",
        priority="P1",
        candidate_types=("pose", "motion", "anchor", "drift", "relocalization_hint"),
        allowed_use="adapter_planning_only",
        license_boundary=LICENSE_TECHNICAL_REFERENCE_ONLY,
        source_chain_required=True,
        confidence_required=True,
        license_ref_required=True,
        backend_origin_required=True,
        adapter_required=True,
        native_output_direct_to_field_blocked=True,
        note="GPL-3.0; technical reference only, no code copy / no runtime dependency unless cleared.",
    ),
    SLAMBackendOutputSourcePolicy(
        source_id="kimera_metric_semantic_output",
        backend_family="metric_semantic_slam",
        output_type="pose graph / semantic mesh / object landmarks",
        priority="P2",
        candidate_types=("pose", "anchor", "region", "scene_relation", "semantic_place"),
        allowed_use="observation_and_adapter_planning",
        license_boundary=LICENSE_OPEN_VERIFIED,
        source_chain_required=True,
        confidence_required=True,
        license_ref_required=True,
        backend_origin_required=True,
        adapter_required=True,
        native_output_direct_to_field_blocked=True,
        note="Semantic output must remain candidate, not fact.",
    ),
    SLAMBackendOutputSourcePolicy(
        source_id="hydra_scene_graph_output",
        backend_family="scene_graph_slam",
        output_type="dynamic scene graph / places / objects / agents / rooms",
        priority="P2",
        candidate_types=("anchor", "scene_relation", "semantic_place", "field_structure_candidate"),
        allowed_use="observation_and_adapter_planning",
        license_boundary=LICENSE_OPEN_VERIFIED,
        source_chain_required=True,
        confidence_required=True,
        license_ref_required=True,
        backend_origin_required=True,
        adapter_required=True,
        native_output_direct_to_field_blocked=True,
        note="Scene graph does not define final Luna Field identity.",
    ),
    SLAMBackendOutputSourcePolicy(
        source_id="neural_or_gaussian_slam_export",
        backend_family="neural_gaussian_slam",
        output_type="camera trajectory / sparse dense map / gaussian map metadata",
        priority="P3",
        candidate_types=("pose", "motion", "local_map", "uncertainty_hint"),
        allowed_use="observation_only",
        license_boundary=LICENSE_TECHNICAL_REFERENCE_ONLY,
        source_chain_required=True,
        confidence_required=True,
        license_ref_required=True,
        backend_origin_required=True,
        adapter_required=True,
        native_output_direct_to_field_blocked=True,
        note="Heavy runtime not admitted; export output only.",
    ),
)

# --------------------------------------------------------------------------- #
# Integrated scenarios
# --------------------------------------------------------------------------- #
_SCENARIO_POLICIES: Tuple[SLAMBackendIntegratedScenarioPolicy, ...] = (
    SLAMBackendIntegratedScenarioPolicy(
        scenario_ref="generic_trajectory_and_rtab_baseline_reuse",
        input_summary="TUM + RTAB sealed outputs",
        output_plan="verified baseline references (no re-run)",
        requirement="do not re-run; verify closure refs only",
    ),
    SLAMBackendIntegratedScenarioPolicy(
        scenario_ref="vio_trajectory_output_admission_planning",
        input_summary="OpenVINS-like trajectory export schema",
        output_plan="pose / motion / health candidate mapping",
        requirement="VIO must not override field identity",
    ),
    SLAMBackendIntegratedScenarioPolicy(
        scenario_ref="visual_slam_keyframe_output_admission_planning",
        input_summary="ORB-SLAM3-like trajectory / keyframe / relocalization export schema",
        output_plan="pose / motion / anchor / relocalization / drift",
        requirement="GPL/incompatible license technical_reference only; no code copy",
    ),
    SLAMBackendIntegratedScenarioPolicy(
        scenario_ref="metric_semantic_slam_output_admission_planning",
        input_summary="Kimera-like semantic mesh / object landmark / pose graph output",
        output_plan="semantic anchor / region / scene_relation candidate",
        requirement="semantic label is not fact; must not directly define Field",
    ),
    SLAMBackendIntegratedScenarioPolicy(
        scenario_ref="scene_graph_slam_output_admission_planning",
        input_summary="Hydra-like dynamic scene graph output",
        output_plan="field_structure_candidate / scene_relation_candidate / semantic_place_candidate",
        requirement="scene graph is field evidence, not final field identity",
    ),
    SLAMBackendIntegratedScenarioPolicy(
        scenario_ref="neural_gaussian_slam_output_observation_planning",
        input_summary="Neural/Gaussian SLAM export metadata",
        output_plan="pose / local_map / uncertainty_hint",
        requirement="observation-only; no heavy runtime admitted",
    ),
    SLAMBackendIntegratedScenarioPolicy(
        scenario_ref="multi_backend_spatial_evidence_replay_path_planning",
        input_summary="multi-backend candidate refs",
        output_plan="spatial_evidence_candidate_bundle -> spatial_odometry_fusion_candidate -> Field/Task/Guidance",
        requirement="candidate-only",
    ),
    SLAMBackendIntegratedScenarioPolicy(
        scenario_ref="invalid_slam_backend_output_blocked",
        input_summary=(
            "missing source_chain / unclear license marked commercial-ready / backend native direct "
            "to field_synthesis / relocalization restores runtime trust / semantic label writes fact "
            "/ SLAM output overrides field identity"
        ),
        output_plan="blocked / rejected",
        requirement="must be blocked",
        blocked_scenario=True,
    ),
)

# --------------------------------------------------------------------------- #
# Upstream sealed GO artifacts
# --------------------------------------------------------------------------- #
_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": GENERIC_TUM_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/generic_tum_real_file_loader_dryrun_v1_smoke_v0/"
            "generic_tum_real_file_loader_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "GENERIC_TUM_REAL_FILE_LOADER_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_tum_real_file_loader_dryrun/"
            "generic_tum_real_file_loader_dryrun_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "tum_real_file_loader_dryrun_go_verified",
    },
    {
        "phase_ref": RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_real_file_loader_integrated_dryrun_v1_smoke_v0/"
            "rtab_map_real_file_loader_integrated_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_REAL_FILE_LOADER_INTEGRATED_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_real_file_loader_integrated_dryrun/"
            "rtab_map_real_file_loader_integrated_dryrun_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": RTAB_MULTI_EXPORT_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_multi_export_spatial_evidence_replay_integrated_closure_v1_smoke_v0/"
            "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_MULTI_EXPORT_SPATIAL_EVIDENCE_REPLAY_INTEGRATED_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_multi_export_spatial_evidence_replay_integrated_closure/"
            "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "rtab_multi_export_spatial_evidence_replay_closure_go_verified",
    },
    {
        "phase_ref": GENERIC_JSON_PARSER_PHASE_REF,
        "artifact_rel": (
            "_tmp_eval_out/generic_json_spatial_trace_parser_v1_smoke_v0/"
            "generic_json_spatial_trace_parser_run_and_review_v1.json"
        ),
        "expected_go": "GENERIC_JSON_SPATIAL_TRACE_PARSER_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_json_spatial_trace_parser/"
            "generic_json_spatial_trace_parser_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "generic_json_spatial_trace_parser_go_verified",
    },
    {
        "phase_ref": SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/slam_spatial_evidence_chain_closure_v1_smoke_v0/"
            "slam_spatial_evidence_chain_closure_review_v1.json"
        ),
        "expected_go": "SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/slam_spatial_evidence_chain_closure/"
            "slam_spatial_evidence_chain_closure_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "slam_spatial_evidence_chain_field_alignment_closure_go_verified",
    },
    {
        "phase_ref": FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
            "field_task_guidance_safety_chain_closure_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "field_task_guidance_safety_chain_closure_go_verified",
    },
    {
        "phase_ref": GOVERNANCE_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"
        ),
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
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "module_rel": (
            "capabilities/midplatform/interface_layer_governance/"
            "interface_layer_governance_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "interface_layer_governance_verified",
    },
    {
        "phase_ref": MODEL_ADMISSION_GOVERNANCE_REF,
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/model_admission_governance/"
            "model_admission_governance_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "model_admission_governance_verified",
    },
)


def build_planning_profile_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        SLAMBackendRealFileOutputAdmissionPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id="Phase-SLAM-Backend-Real-File-Output-Integrated-Admission-Planning-v1-001",
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            rtab_multi_export_closure_ref=RTAB_MULTI_EXPORT_CLOSURE_REF,
            generic_json_spatial_trace_parser_ref=GENERIC_JSON_PARSER_REF,
            slam_spatial_evidence_chain_field_alignment_closure_ref=(
                SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_REF
            ),
            field_task_guidance_safety_chain_closure_ref=(
                FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF
            ),
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            source_family=SOURCE_FAMILY,
            target_internal_format=TARGET_INTERNAL_FORMAT,
            target_entrypoint=TARGET_ENTRYPOINT,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            backend_source_ids=BACKEND_SOURCE_IDS,
            governance_rules=PLANNING_GOVERNANCE_RULES,
        )
    )


def build_license_boundary_policy_v1() -> Dict[str, Any]:
    tech_ref = tuple(
        p.source_id for p in _SOURCE_POLICIES
        if p.license_boundary == LICENSE_TECHNICAL_REFERENCE_ONLY
    )
    return candidate_to_dict(
        SLAMBackendLicenseBoundaryPolicy(
            policy_ref="slam_backend_license_boundary_policy_v1",
            gpl_or_incompatible_backend_technical_reference_only=True,
            no_gpl_code_copy=True,
            no_runtime_dependency_unless_cleared=True,
            commercial_use_unknown_until_license_verified=True,
            technical_reference_backends=tech_ref,
        )
    )


def build_format_admission_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        SLAMBackendOutputFormatAdmissionPolicy(
            policy_ref="slam_backend_output_format_admission_policy_v1",
            adapter_required=all(p.adapter_required for p in _SOURCE_POLICIES),
            source_chain_required=all(p.source_chain_required for p in _SOURCE_POLICIES),
            confidence_required=all(p.confidence_required for p in _SOURCE_POLICIES),
            file_origin_required=True,
            backend_origin_required=all(p.backend_origin_required for p in _SOURCE_POLICIES),
            license_ref_required=all(p.license_ref_required for p in _SOURCE_POLICIES),
            generic_json_output_required=True,
            generic_json_parser_required=True,
        )
    )


def build_mapping_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        SLAMBackendToGenericJSONTraceMappingPolicy(
            policy_ref="slam_backend_to_generic_json_trace_mapping_policy_v1",
            pose_candidate_mapping_supported=True,
            motion_candidate_mapping_supported=True,
            health_candidate_mapping_supported=True,
            anchor_candidate_mapping_supported=True,
            relocalization_candidate_mapping_supported=True,
            drift_candidate_mapping_supported=True,
            scene_relation_candidate_mapping_supported=True,
            field_structure_candidate_mapping_supported=True,
            local_map_uncertainty_hint_mapping_supported=True,
            semantic_label_not_fact=True,
            scene_graph_not_final_field_identity=True,
        )
    )


def build_replay_boundary_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        SLAMBackendReplayBoundaryPolicy(
            policy_ref="slam_backend_replay_boundary_policy_v1",
            backend_native_output_direct_to_field_blocked=True,
            vio_slam_pose_not_field_identity=True,
            gps_does_not_override_field_identity=True,
            relocalization_does_not_restore_runtime_trust=True,
            drift_remains_uncertainty_evidence=True,
            health_candidate_only=True,
            field_task_guidance_candidate_only=True,
            heavy_neural_gaussian_runtime_not_admitted=True,
        )
    )


def build_safety_boundary_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        SLAMBackendSafetyBoundaryPolicy(
            policy_ref="slam_backend_safety_boundary_policy_v1",
            no_live_sensor=True,
            no_ros=True,
            no_camera=True,
            no_imu=True,
            no_real_gps=True,
            no_map_api=True,
            no_navigation_action_speech_fact_write=True,
            controlled_trial_governance_template_referenced=(
                CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF is not None
            ),
            commercial_runtime_approval_not_implied=True,
        )
    )


def build_backend_registered_map() -> Dict[str, bool]:
    registered = {p.source_id for p in _SOURCE_POLICIES}
    return {
        "generic_tum_trajectory_registered": "generic_tum_trajectory" in registered,
        "rtab_map_multi_export_registered": "rtab_map_multi_export" in registered,
        "openvins_trajectory_export_registered": "openvins_trajectory_export" in registered,
        "orb_slam3_trajectory_export_registered": "orb_slam3_trajectory_export" in registered,
        "kimera_metric_semantic_output_registered": "kimera_metric_semantic_output" in registered,
        "hydra_scene_graph_output_registered": "hydra_scene_graph_output" in registered,
        "neural_gaussian_slam_export_registered": "neural_or_gaussian_slam_export" in registered,
    }


def build_scenario_support_map() -> Dict[str, bool]:
    refs = {s.scenario_ref for s in _SCENARIO_POLICIES}
    blocked = {
        s.scenario_ref for s in _SCENARIO_POLICIES if s.blocked_scenario
    }
    return {
        "generic_trajectory_and_rtab_baseline_reuse_supported": (
            "generic_trajectory_and_rtab_baseline_reuse" in refs
        ),
        "vio_trajectory_output_admission_supported": (
            "vio_trajectory_output_admission_planning" in refs
        ),
        "visual_slam_keyframe_output_admission_supported": (
            "visual_slam_keyframe_output_admission_planning" in refs
        ),
        "metric_semantic_slam_output_admission_supported": (
            "metric_semantic_slam_output_admission_planning" in refs
        ),
        "scene_graph_slam_output_admission_supported": (
            "scene_graph_slam_output_admission_planning" in refs
        ),
        "neural_gaussian_slam_observation_supported": (
            "neural_gaussian_slam_output_observation_planning" in refs
        ),
        "multi_backend_spatial_evidence_replay_path_supported": (
            "multi_backend_spatial_evidence_replay_path_planning" in refs
        ),
        "invalid_slam_backend_output_blocked": (
            "invalid_slam_backend_output_blocked" in blocked
        ),
    }


def build_slam_backend_planning_matrix_v1() -> Dict[str, Any]:
    return {
        "registry_id": REGISTRY_ID,
        "slam_backend_planning_profile": build_planning_profile_v1(),
        "slam_backend_output_source_policies": [candidate_to_dict(p) for p in _SOURCE_POLICIES],
        "slam_backend_source_policy_count": len(_SOURCE_POLICIES),
        "license_boundary_policy": build_license_boundary_policy_v1(),
        "format_admission_policy": build_format_admission_policy_v1(),
        "mapping_policy": build_mapping_policy_v1(),
        "replay_boundary_policy": build_replay_boundary_policy_v1(),
        "safety_boundary_policy": build_safety_boundary_policy_v1(),
        "integrated_scenario_policies": [candidate_to_dict(s) for s in _SCENARIO_POLICIES],
        "integrated_scenario_count": len(_SCENARIO_POLICIES),
        "backend_registered_map": build_backend_registered_map(),
        "scenario_support_map": build_scenario_support_map(),
        "candidate_mapping_support_map": {
            "pose_candidate_mapping_supported": True,
            "motion_candidate_mapping_supported": True,
            "health_candidate_mapping_supported": True,
            "anchor_candidate_mapping_supported": True,
            "relocalization_candidate_mapping_supported": True,
            "drift_candidate_mapping_supported": True,
            "scene_relation_candidate_mapping_supported": True,
            "field_structure_candidate_mapping_supported": True,
            "local_map_uncertainty_hint_mapping_supported": True,
        },
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
    }


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []

    if len(_SOURCE_POLICIES) < 7:
        issues.append("slam_backend_source_policy_count_lt_7")
    if len(_SCENARIO_POLICIES) != 8:
        issues.append("integrated_scenario_count_not_8")

    seen = set()
    for p in _SOURCE_POLICIES:
        if p.source_id in seen:
            issues.append(f"duplicate_source_id:{p.source_id}")
        seen.add(p.source_id)
        if p.priority not in ("P0", "P1", "P2", "P3"):
            issues.append(f"invalid_priority:{p.source_id}:{p.priority}")
        if p.allowed_use not in ALLOWED_USE_VALUES:
            issues.append(f"invalid_allowed_use:{p.source_id}:{p.allowed_use}")
        if p.license_boundary not in LICENSE_BOUNDARY_VALUES:
            issues.append(f"invalid_license_boundary:{p.source_id}:{p.license_boundary}")
        if not (
            p.source_chain_required
            and p.confidence_required
            and p.license_ref_required
            and p.backend_origin_required
            and p.adapter_required
            and p.native_output_direct_to_field_blocked
        ):
            issues.append(f"admission_required_flags_not_all_true:{p.source_id}")
        if not p.candidate_types:
            issues.append(f"candidate_types_empty:{p.source_id}")

    expected = set(BACKEND_SOURCE_IDS)
    actual = {p.source_id for p in _SOURCE_POLICIES}
    for sid in expected - actual:
        issues.append(f"expected_backend_not_registered:{sid}")

    if "invalid_slam_backend_output_blocked" not in INTEGRATED_SCENARIO_REFS:
        issues.append("invalid_slam_backend_output_blocked_scenario_missing")

    blocked = next(
        (s for s in _SCENARIO_POLICIES if s.scenario_ref == "invalid_slam_backend_output_blocked"),
        None,
    )
    if blocked is None or not blocked.blocked_scenario:
        issues.append("invalid_slam_backend_output_must_be_blocked_scenario")

    return len(issues) == 0, issues
