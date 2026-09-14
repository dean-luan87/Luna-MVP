# -*- coding: utf-8 -*-
"""SLAM Backend Capability Observation — matrix + review + handoff (compressed)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_backend_capability_observation.slam_backend_capability_observation_registry_v1 import (
    MODEL_BINDING,
    OBSERVATION_DIMENSIONS,
    REGISTRY_ID,
    TRIAL_REF,
    validate_observation_entry_shape,
    validate_registry,
)
from capabilities.field_understanding.slam_backend_capability_observation.slam_backend_capability_observation_types_v1 import (
    ADAPTER_PROFILE_REF,
    FINAL_DECISION_HANDOFF_READY,
    FINAL_DECISION_READY_FOR_OFFLINE_PARSER_DECISION,
    FINAL_DECISION_REVIEW_BLOCKED,
    GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS,
    LUNA_CANDIDATE_TYPES,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_ID,
    MODEL_MANAGEMENT_CHAIN,
    NEXT_PHASE_GENERIC_JSON_PARSER,
    NON_EXECUTION_FLAGS,
    OBSERVATION_BACKEND_REFS,
    OBSERVATION_PRINCIPLE_ZH,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    PHASE_ID,
    SLAMBackendCapabilityObservationDecision,
    SLAMBackendCapabilityObservationEntry,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "slam_backend_capability_observation_v1_smoke_v0"
)
REVIEW_FILENAME = "slam_backend_capability_observation_review_v1.json"
HANDOFF_FILENAME = "slam_backend_capability_observation_handoff_v1.json"

FINAL_DECISION_GO = FINAL_DECISION_READY_FOR_OFFLINE_PARSER_DECISION

STEP_FILES = (
    "capabilities/field_understanding/slam_backend_capability_observation/slam_backend_capability_observation_types_v1.py",
    "capabilities/field_understanding/slam_backend_capability_observation/slam_backend_capability_observation_registry_v1.py",
    "capabilities/field_understanding/slam_backend_capability_observation/review_slam_backend_capability_observation_v1.py",
)

RUNTIME_BINDING_PATTERNS = (
    "cv2.VideoCapture",
    "rospy",
    "ros::",
    "import openvins",
    "orb_slam3.System",
    "rtabmap::",
)

_STUB = ("capability_observation_stub_v1",)


def _mapping(**kwargs: str) -> Dict[str, str]:
    base = {candidate_type: "not_applicable" for candidate_type in LUNA_CANDIDATE_TYPES}
    base.update(kwargs)
    return base


def build_observation_entries_v1() -> Tuple[SLAMBackendCapabilityObservationEntry, ...]:
    return (
        SLAMBackendCapabilityObservationEntry(
            observation_ref="obs_openvins",
            backend_ref="openvins",
            backend_name="OpenVINS",
            backend_family="vio_state_estimation",
            license_status="gpl_3_technical_reference_only",
            primary_inputs=(
                "camera_images",
                "imu_stream",
                "optional_stereo",
                "camera_imu_calibration",
            ),
            primary_outputs=(
                "vio_pose",
                "velocity_state",
                "imu_bias_state",
                "sliding_window_state_estimate",
            ),
            output_export_options=(
                "post_processed_trajectory",
                "euroc_dataset_replay_export",
                "tum_trajectory_subset_via_postprocess",
            ),
            luna_candidate_mapping=_mapping(
                PoseCandidate="high",
                MotionCandidate="high",
                SLAMHealthCandidate="high",
                MapDriftCandidate="medium",
                RelocalizationCandidate="medium",
                SpatialAnchorCandidate="low",
                LocalMapCandidate="low",
            ),
            dependencies_runtime_requirements=(
                "c++_build",
                "camera_imu_time_sync",
                "optional_ros_wrapper",
                "recorded_dataset_for_offline_trial",
            ),
            offline_trial_feasibility="medium",
            commercial_runtime_candidate=False,
            technical_reference_only=True,
            recommended_parser_path="technical_reference_only",
            source_refs=_STUB + ("openvins_official_gpl3_ref",),
            observation_notes=(
                "VIO-first backend; strongest for Pose/Motion/Health evidence patterns.",
                "GPL-3.0 blocks commercial runtime; use as technical reference only.",
                "Offline trial depends on recorded dataset export, not live camera/IMU.",
            ),
        ),
        SLAMBackendCapabilityObservationEntry(
            observation_ref="obs_orb_slam3",
            backend_ref="orb_slam3",
            backend_name="ORB-SLAM3",
            backend_family="visual_inertial_slam",
            license_status="gpl_3_technical_reference_only",
            primary_inputs=(
                "monocular_images",
                "stereo_images",
                "rgbd_images",
                "optional_imu",
            ),
            primary_outputs=(
                "camera_trajectory",
                "keyframes",
                "map_points",
                "multi_map_sessions",
                "relocalization_events",
            ),
            output_export_options=(
                "tum_trajectory_format",
                "euroc_tum_vi_examples",
                "keyframe_pose_dump",
                "map_point_export",
            ),
            luna_candidate_mapping=_mapping(
                PoseCandidate="medium",
                MotionCandidate="medium",
                LocalMapCandidate="high",
                RelocalizationCandidate="high",
                MapDriftCandidate="high",
                SLAMHealthCandidate="medium",
                SpatialAnchorCandidate="medium",
            ),
            dependencies_runtime_requirements=(
                "c++_build",
                "opencv",
                "dataset_with_known_format",
                "optional_ros_not_required_for_offline_trajectory",
            ),
            offline_trial_feasibility="medium",
            commercial_runtime_candidate=False,
            technical_reference_only=True,
            recommended_parser_path="technical_reference_only",
            source_refs=_STUB + ("orb_slam3_official_gpl3_ref",),
            observation_notes=(
                "Strong relocalization and multi-map reference; trajectory export is common.",
                "GPL-3.0 blocks commercial runtime; TUM trajectory is only a narrow slice of output.",
                "Useful to observe relocalization/local map patterns, not as Luna runtime binding.",
            ),
        ),
        SLAMBackendCapabilityObservationEntry(
            observation_ref="obs_rtab_map",
            backend_ref="rtab_map",
            backend_name="RTAB-Map",
            backend_family="graph_rgbd_slam",
            license_status="bsd_conditional_license_friendly",
            primary_inputs=(
                "rgbd_stream",
                "stereo_images",
                "lidar_scans",
                "wheel_odometry_optional",
            ),
            primary_outputs=(
                "pose_graph",
                "occupancy_grid",
                "point_cloud_map",
                "loop_closure_constraints",
                "trajectory",
            ),
            output_export_options=(
                "rtabmap_database_export",
                "pose_graph_export",
                "ply_point_cloud",
                "trajectory_txt",
                "ros_bag_offline_processing",
            ),
            luna_candidate_mapping=_mapping(
                LocalMapCandidate="high",
                PoseCandidate="medium",
                SpatialAnchorCandidate="medium",
                MapDriftCandidate="high",
                RelocalizationCandidate="medium",
                SLAMHealthCandidate="medium",
                FieldGraphCandidate="low",
            ),
            dependencies_runtime_requirements=(
                "rtabmap_library_or_standalone_app",
                "rgbd_or_stereo_input_for_rich_output",
                "offline_db_export_path_for_parser_trial",
            ),
            offline_trial_feasibility="high",
            commercial_runtime_candidate=False,
            technical_reference_only=False,
            recommended_parser_path="third_priority_offline_export",
            source_refs=_STUB + ("rtab_map_library_ref",),
            observation_notes=(
                "Graph RGB-D SLAM with rich offline export options beyond trajectory.",
                "License friendlier than GPL VIO stacks but still not auto commercial runtime.",
                "Good third-priority real export parser target after Luna internal standard.",
            ),
        ),
        SLAMBackendCapabilityObservationEntry(
            observation_ref="obs_kimera",
            backend_ref="kimera",
            backend_name="Kimera",
            backend_family="metric_semantic_vio_slam",
            license_status="bsd_2_clause_license_friendly",
            primary_inputs=(
                "stereo_images",
                "imu_stream",
                "camera_imu_calibration",
            ),
            primary_outputs=(
                "vio_pose",
                "pose_graph",
                "3d_mesh",
                "metric_semantic_reconstruction",
            ),
            output_export_options=(
                "trajectory_log",
                "mesh_export",
                "pose_graph_dump",
                "semantic_mesh_placeholder",
            ),
            luna_candidate_mapping=_mapping(
                PoseCandidate="medium",
                MotionCandidate="medium",
                LocalMapCandidate="high",
                SemanticFieldObjectCandidate="medium",
                SpatialAnchorCandidate="medium",
                SLAMHealthCandidate="medium",
                FieldGraphCandidate="low",
            ),
            dependencies_runtime_requirements=(
                "c++_build",
                "stereo_imu_dataset",
                "engineering_heavy_pipeline",
            ),
            offline_trial_feasibility="medium",
            commercial_runtime_candidate=False,
            technical_reference_only=False,
            recommended_parser_path="fourth_priority_scene_graph_observation",
            source_refs=_STUB + ("kimera_vio_bsd2_ref",),
            observation_notes=(
                "VIO + pose graph + mesh + metric-semantic reconstruction observation line.",
                "BSD-2-Clause is license friendly but engineering cost is high for P0 parser.",
                "Better as export/scene observation after internal JSON standard is established.",
            ),
        ),
        SLAMBackendCapabilityObservationEntry(
            observation_ref="obs_hydra",
            backend_ref="hydra",
            backend_name="Hydra",
            backend_family="metric_semantic_scene_graph",
            license_status="bsd_2_clause_license_friendly",
            primary_inputs=(
                "rgbd_images",
                "stereo_depth",
                "optional_semantic_labels",
            ),
            primary_outputs=(
                "layered_scene_graph",
                "3d_mesh",
                "places_objects_graph",
                "metric_map_layers",
            ),
            output_export_options=(
                "scene_graph_json_export",
                "mesh_ply_export",
                "layered_graph_snapshot",
            ),
            luna_candidate_mapping=_mapping(
                FieldGraphCandidate="high",
                SemanticFieldObjectCandidate="high",
                SpatialAnchorCandidate="medium",
                LocalMapCandidate="medium",
                PoseCandidate="low",
                MotionCandidate="low",
            ),
            dependencies_runtime_requirements=(
                "rgbd_or_depth_pipeline",
                "scene_graph_export_tooling",
                "not_pose_first_backend",
            ),
            offline_trial_feasibility="medium",
            commercial_runtime_candidate=False,
            technical_reference_only=False,
            recommended_parser_path="fourth_priority_scene_graph_observation",
            source_refs=_STUB + ("hydra_scene_graph_ref",),
            observation_notes=(
                "Scene graph / layered spatial structure reference for FieldGraph alignment.",
                "Outputs exceed trajectory-only formats; not suitable as first minimal parser.",
                "Observation value is semantic spatial graph, not wearable pose baseline.",
            ),
        ),
        SLAMBackendCapabilityObservationEntry(
            observation_ref="obs_generic_trajectory_json_trace",
            backend_ref="generic_trajectory_json_trace",
            backend_name="Generic Trajectory / JSON Trace",
            backend_family="luna_internal_fallback_format",
            license_status="luna_internal_no_third_party_license",
            primary_inputs=(
                "offline_exported_trace",
                "synthetic_fixture",
                "third_party_backend_export_normalized",
            ),
            primary_outputs=(
                "json_spatial_trace_bundle",
                "optional_tum_trajectory_subset",
                "multi_candidate_payload",
            ),
            output_export_options=(
                "generic_json_spatial_trace",
                "generic_tum_trajectory_subset",
                "source_chain_metadata",
                "confidence_and_time_window_fields",
            ),
            luna_candidate_mapping=_mapping(
                PoseCandidate="high",
                MotionCandidate="high",
                SpatialAnchorCandidate="high",
                LocalMapCandidate="high",
                SLAMHealthCandidate="high",
                MapDriftCandidate="high",
                RelocalizationCandidate="high",
                FieldGraphCandidate="high",
                SemanticFieldObjectCandidate="high",
            ),
            dependencies_runtime_requirements=(
                "no_third_party_slam_runtime",
                "offline_file_only",
                "adapter_mapping_to_spatial_evidence_candidate_bundle",
            ),
            offline_trial_feasibility="high",
            commercial_runtime_candidate=False,
            technical_reference_only=False,
            recommended_parser_path="first_priority_offline_parser",
            source_refs=_STUB + ("luna_generic_json_spatial_trace_schema_ref",),
            observation_notes=(
                "Luna internal fallback format; can carry pose, motion, anchors, maps, health, "
                "drift, relocalization, field graph, and semantic placeholders in one trace.",
                "Preferred over TUM because Luna needs more than timestamp tx ty tz qx qy qz qw.",
                "TUM remains useful as ingest subset, not as the sole internal standard.",
            ),
        ),
    )


def build_observation_decision_v1() -> SLAMBackendCapabilityObservationDecision:
    return SLAMBackendCapabilityObservationDecision(
        decision_ref="slam_backend_capability_observation_decision_v1",
        trial_ref=TRIAL_REF,
        model_id=MODEL_BINDING["model_id"],
        model_family=MODEL_BINDING["model_family"],
        domain_id=MODEL_BINDING["domain_id"],
        model_management_protocol_ref=MODEL_BINDING["model_management_protocol_ref"],
        model_admission_standard_ref=MODEL_BINDING["model_admission_standard_ref"],
        adapter_profile_ref=MODEL_BINDING["adapter_profile_ref"],
        output_candidate_contract_ref=MODEL_BINDING["output_candidate_contract_ref"],
        best_first_batch_offline_parser_backend="generic_trajectory_json_trace",
        technical_reference_only_backends=GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS,
        generic_tum_parser_necessary=True,
        generic_tum_parser_role=(
            "secondary_trajectory_subset_ingest_for_gpl_backends_and_simple_exports"
        ),
        generic_json_spatial_trace_preferred_internal_standard=True,
        recommended_internal_standard_format="generic_json_spatial_trace",
        next_phase_minimal_real_output_parser="generic_json_spatial_trace_parser_v1",
        parser_priority_order=(
            "generic_json_spatial_trace_parser_v1",
            "generic_tum_trajectory_parser_v1",
            "rtab_map_offline_export_parser_v1",
            "kimera_hydra_scene_graph_observation_parser_v1",
        ),
        observation_rationale_refs=(
            "obs_generic_trajectory_json_trace",
            "obs_openvins",
            "obs_orb_slam3",
            "obs_rtab_map",
            "obs_kimera",
            "obs_hydra",
        ),
        not_independent_slam_flow=True,
        offline_observation_only=True,
        no_runtime_activation=True,
        final_decision=FINAL_DECISION_READY_FOR_OFFLINE_PARSER_DECISION,
    )


def build_slam_backend_capability_observation_matrix_v1() -> Dict[str, Any]:
    entries = build_observation_entries_v1()
    decision = build_observation_decision_v1()
    return {
        "registry_id": REGISTRY_ID,
        "trial_ref": TRIAL_REF,
        "phase_id": PHASE_ID,
        "model_binding": dict(MODEL_BINDING),
        "model_management_chain": list(MODEL_MANAGEMENT_CHAIN),
        "observation_principle_zh": OBSERVATION_PRINCIPLE_ZH,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "luna_candidate_types": list(LUNA_CANDIDATE_TYPES),
        "observation_entries": [candidate_to_dict(entry) for entry in entries],
        "observation_decision": candidate_to_dict(decision),
        "matrix_pipeline": [
            "SLAMBackendCapabilityObservationEntry",
            "luna_candidate_mapping",
            "SLAMBackendCapabilityObservationDecision",
        ],
    }


def validate_observation_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_slam_backend_capability_observation_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    binding = matrix.get("model_binding") or {}
    for key, expected in MODEL_BINDING.items():
        if binding.get(key) != expected:
            issues.append(f"model_binding.{key}: expected={expected!r}, actual={binding.get(key)!r}")

    entries = matrix.get("observation_entries") or []
    if len(entries) != 6:
        issues.append(f"observation_entry_count:{len(entries)}")

    backend_refs = {entry.get("backend_ref") for entry in entries}
    for backend_ref in OBSERVATION_BACKEND_REFS:
        if backend_ref not in backend_refs:
            issues.append(f"missing_observation_backend:{backend_ref}")

    for entry in entries:
        ok, part = validate_observation_entry_shape(entry)
        if not ok:
            issues.extend([f"{entry.get('observation_ref')}.{err}" for err in part])
        if entry.get("backend_ref") in GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS:
            if entry.get("technical_reference_only") is not True:
                issues.append(f"{entry.get('backend_ref')}.technical_reference_only_required")
            if entry.get("commercial_runtime_candidate") is True:
                issues.append(f"{entry.get('backend_ref')}.commercial_runtime_candidate_forbidden")

    decision = matrix.get("observation_decision") or {}
    if decision.get("adapter_profile_ref") != ADAPTER_PROFILE_REF:
        issues.append("decision.adapter_profile_ref_mismatch")
    if decision.get("output_candidate_contract_ref") != OUTPUT_CANDIDATE_CONTRACT_REF:
        issues.append("decision.output_candidate_contract_ref_mismatch")
    if decision.get("best_first_batch_offline_parser_backend") != "generic_trajectory_json_trace":
        issues.append("decision.best_first_batch_offline_parser_backend_not_generic_json")
    if decision.get("generic_json_spatial_trace_preferred_internal_standard") is not True:
        issues.append("decision.generic_json_spatial_trace_not_preferred")
    if set(decision.get("technical_reference_only_backends") or ()) != set(GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS):
        issues.append("decision.technical_reference_only_backends_mismatch")
    if decision.get("not_independent_slam_flow") is not True:
        issues.append("decision.not_independent_slam_flow_required")
    if decision.get("offline_observation_only") is not True:
        issues.append("decision.offline_observation_only_required")
    if decision.get("no_runtime_activation") is not True:
        issues.append("decision.no_runtime_activation_required")
    if decision.get("final_decision") != FINAL_DECISION_READY_FOR_OFFLINE_PARSER_DECISION:
        issues.append("decision.final_decision_not_ready")

    flags = matrix.get("non_execution_flags") or {}
    for flag in (
        "no_parser_implementation",
        "no_third_party_slam_runtime",
        "no_live_camera",
        "no_live_imu",
        "no_ros_runtime",
        "no_provider_runtime_activation",
        "no_action_output",
        "no_speech_output",
        "no_fact_write",
    ):
        if flags.get(flag) is not True:
            issues.append(f"non_execution.{flag}_required")

    return len(issues) == 0 and registry_ok, issues


def _entry_by_ref(entries: List[Dict[str, Any]], backend_ref: str) -> Optional[Dict[str, Any]]:
    for entry in entries:
        if entry.get("backend_ref") == backend_ref:
            return entry
    return None


def review_observation_baseline(matrix: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    entries = matrix.get("observation_entries") or []
    decision = matrix.get("observation_decision") or {}

    if len(entries) == 6:
        passed.append("baseline.observation_entry_count=6")
    else:
        failed.append(f"baseline.observation_entry_count={len(entries)}")

    backend_refs = {entry.get("backend_ref") for entry in entries}
    if backend_refs == set(OBSERVATION_BACKEND_REFS):
        passed.append("baseline.all_observation_backends_present=true")
    else:
        failed.append(f"baseline.missing_backends={sorted(set(OBSERVATION_BACKEND_REFS) - backend_refs)!r}")

    if len(OBSERVATION_DIMENSIONS) >= 11:
        passed.append("baseline.observation_dimensions>=11")
    else:
        failed.append(f"baseline.observation_dimensions={len(OBSERVATION_DIMENSIONS)}")

    if decision:
        passed.append("baseline.observation_decision_present=true")
    else:
        failed.append("baseline.observation_decision_missing")

    baseline = {
        "observation_entry_count": len(entries),
        "observation_dimension_count": len(OBSERVATION_DIMENSIONS),
        "luna_candidate_type_count": len(LUNA_CANDIDATE_TYPES),
        "best_first_batch_offline_parser_backend": decision.get("best_first_batch_offline_parser_backend"),
        "technical_reference_only_backends": list(decision.get("technical_reference_only_backends") or ()),
        "next_phase_minimal_real_output_parser": decision.get("next_phase_minimal_real_output_parser"),
    }

    return len(failed) == 0, baseline, passed, failed


def review_model_binding(matrix: Dict[str, Any]) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    binding = matrix.get("model_binding") or {}
    decision = matrix.get("observation_decision") or {}

    checks = {
        "model_id_bound": binding.get("model_id") == MODEL_ID,
        "model_admission_standard_ref_bound": binding.get("model_admission_standard_ref")
        == MODEL_ADMISSION_STANDARD_REF,
        "adapter_profile_bound": binding.get("adapter_profile_ref") == ADAPTER_PROFILE_REF,
        "output_candidate_contract_bound": binding.get("output_candidate_contract_ref")
        == OUTPUT_CANDIDATE_CONTRACT_REF,
        "decision_model_binding_consistent": decision.get("model_id") == MODEL_ID
        and decision.get("model_admission_standard_ref") == MODEL_ADMISSION_STANDARD_REF
        and decision.get("adapter_profile_ref") == ADAPTER_PROFILE_REF
        and decision.get("output_candidate_contract_ref") == OUTPUT_CANDIDATE_CONTRACT_REF,
        "not_independent_slam_flow": decision.get("not_independent_slam_flow") is True,
        "model_management_chain_present": list(matrix.get("model_management_chain") or ())
        == list(MODEL_MANAGEMENT_CHAIN),
    }

    for key, ok in checks.items():
        if ok:
            passed.append(f"model_binding.{key}=true")
        else:
            failed.append(f"model_binding.{key}=false")

    return checks, passed, failed


def review_license_and_parser_conclusions(
    entries: List[Dict[str, Any]],
    decision: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    gpl_only = []
    for backend_ref in GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS:
        entry = _entry_by_ref(entries, backend_ref)
        if not entry:
            failed.append(f"license.missing_entry={backend_ref}")
            continue
        if entry.get("technical_reference_only") is True and entry.get("commercial_runtime_candidate") is False:
            gpl_only.append(backend_ref)
            passed.append(f"license.{backend_ref}_technical_reference_only=true")
        else:
            failed.append(f"license.{backend_ref}_not_technical_reference_only")

    checks = {
        "best_first_batch_is_generic_json_trace": decision.get("best_first_batch_offline_parser_backend")
        == "generic_trajectory_json_trace",
        "technical_reference_only_backends_match_gpl": tuple(
            decision.get("technical_reference_only_backends") or ()
        )
        == GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS,
        "generic_tum_parser_necessary_declared": decision.get("generic_tum_parser_necessary") is True,
        "generic_json_spatial_trace_preferred": decision.get(
            "generic_json_spatial_trace_preferred_internal_standard"
        )
        is True,
        "recommended_internal_standard_is_generic_json": decision.get("recommended_internal_standard_format")
        == "generic_json_spatial_trace",
        "next_phase_parser_is_generic_json": decision.get("next_phase_minimal_real_output_parser")
        == "generic_json_spatial_trace_parser_v1",
        "parser_priority_starts_with_generic_json": (
            (decision.get("parser_priority_order") or ("",))[0]
            == "generic_json_spatial_trace_parser_v1"
        ),
        "gpl_backends_not_first_parser_priority": all(
            backend_ref not in (decision.get("parser_priority_order") or ())[:1]
            for backend_ref in GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS
        ),
    }

    for key, ok in checks.items():
        if ok:
            passed.append(f"parser_decision.{key}=true")
        else:
            failed.append(f"parser_decision.{key}=false")

    checks["gpl_backends_technical_reference_only"] = len(gpl_only) == len(
        GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS
    )
    return checks, passed, failed


def review_luna_candidate_coverage(entries: List[Dict[str, Any]]) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    generic = _entry_by_ref(entries, "generic_trajectory_json_trace")
    if not generic:
        failed.append("candidate_coverage.generic_entry_missing")
        return {"generic_json_covers_all_candidates": False}, passed, failed

    mapping = generic.get("luna_candidate_mapping") or {}
    high_or_medium = {
        candidate_type
        for candidate_type in LUNA_CANDIDATE_TYPES
        if mapping.get(candidate_type) in ("high", "medium")
    }
    covers_all = len(high_or_medium) == len(LUNA_CANDIDATE_TYPES)

    checks = {
        "generic_json_covers_all_candidates": covers_all,
        "tum_subset_not_sole_standard": generic.get("recommended_parser_path")
        == "first_priority_offline_parser",
    }

    for key, ok in checks.items():
        if ok:
            passed.append(f"candidate_coverage.{key}=true")
        else:
            failed.append(f"candidate_coverage.{key}=false")

    return checks, passed, failed


def review_non_execution_boundary() -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    flags = dict(NON_EXECUTION_FLAGS)
    boundary = {
        "no_third_party_slam_runtime": flags.get("no_third_party_slam_runtime") is True,
        "no_parser_implementation": flags.get("no_parser_implementation") is True,
        "no_live_camera": flags.get("no_live_camera") is True,
        "no_live_imu": flags.get("no_live_imu") is True,
        "no_ros_runtime": flags.get("no_ros_runtime") is True,
        "no_provider_runtime_activation": flags.get("no_provider_runtime_activation") is True,
        "no_commercial_runtime_approval": flags.get("no_commercial_runtime_approval") is True,
        "no_action_output": flags.get("no_action_output") is True,
        "no_speech_output": flags.get("no_speech_output") is True,
        "no_fact_write": flags.get("no_fact_write") is True,
    }

    observation_root = _REPO_ROOT / "capabilities" / "field_understanding" / "slam_backend_capability_observation"
    for py_path in observation_root.rglob("*.py"):
        if py_path.name == "review_slam_backend_capability_observation_v1.py":
            continue
        text = py_path.read_text(encoding="utf-8").lower()
        for pattern in RUNTIME_BINDING_PATTERNS:
            if pattern.lower() in text:
                failed.append(f"boundary.runtime_binding={py_path.name}:{pattern}")

    for key, ok in boundary.items():
        if ok:
            passed.append(f"boundary.{key}=true")
        else:
            failed.append(f"boundary.{key}=false")

    return boundary, passed, failed


def build_observation_handoff_v1(
    *,
    review_result: Dict[str, Any],
    matrix: Dict[str, Any],
) -> Dict[str, Any]:
    decision = matrix.get("observation_decision") or {}
    conclusions = review_result.get("conclusions") or {}
    blockers: List[str] = []

    if review_result.get("final_decision") != FINAL_DECISION_GO:
        blockers.append(f"review_not_go:{review_result.get('final_decision')}")

    handoff_ready = len(blockers) == 0 and review_result.get("matrix_review_ok") is True

    return {
        "phase_id": PHASE_ID,
        "handoff_kind": "slam_backend_capability_observation_to_parser_decision",
        "model_management_chain": list(MODEL_MANAGEMENT_CHAIN),
        "model_binding": matrix.get("model_binding"),
        "observation_matrix_ref": TRIAL_REF,
        "review_final_decision": review_result.get("final_decision"),
        "conclusions": conclusions,
        "ready_for_next_phase": handoff_ready,
        "next_phase_id": NEXT_PHASE_GENERIC_JSON_PARSER,
        "next_phase_entrypoint": decision.get("next_phase_minimal_real_output_parser"),
        "parser_priority_order": list(decision.get("parser_priority_order") or ()),
        "technical_reference_only_backends": list(decision.get("technical_reference_only_backends") or ()),
        "forbidden_next_steps": (
            "no_slam_runtime_activation",
            "no_live_camera_imu_ros",
            "no_provider_runtime_activation",
            "no_commercial_runtime_approval",
            "no_generic_tum_as_sole_standard",
        ),
        "handoff_blockers": blockers,
        "final_decision": (
            FINAL_DECISION_HANDOFF_READY if handoff_ready else "SLAM_BACKEND_CAPABILITY_OBSERVATION_HANDOFF_BLOCKED"
        ),
    }


def review_slam_backend_capability_observation_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_slam_backend_capability_observation_matrix_v1()
    matrix_ok, matrix_issues = validate_observation_matrix_v1(matrix)
    registry_ok, registry_issues = validate_registry()

    entries = matrix.get("observation_entries") or []
    decision = matrix.get("observation_decision") or {}

    all_passed: List[str] = []
    all_failed: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            all_passed.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            all_failed.append(f"step.file_missing={rel}")

    if matrix_ok:
        all_passed.append("matrix_validation_ok=true")
    else:
        all_failed.extend(matrix_issues)

    if registry_ok:
        all_passed.append("registry_validation_ok=true")
    else:
        all_failed.extend(registry_issues)

    baseline_ok, baseline, p, f = review_observation_baseline(matrix)
    all_passed.extend(p)
    all_failed.extend(f)

    model_binding_review, p, f = review_model_binding(matrix)
    all_passed.extend(p)
    all_failed.extend(f)

    parser_decision_review, p, f = review_license_and_parser_conclusions(entries, decision)
    all_passed.extend(p)
    all_failed.extend(f)

    candidate_coverage_review, p, f = review_luna_candidate_coverage(entries)
    all_passed.extend(p)
    all_failed.extend(f)

    boundary_review, p, f = review_non_execution_boundary()
    all_passed.extend(p)
    all_failed.extend(f)

    blocker_count = len(all_failed)
    review_ok = (
        matrix_ok
        and registry_ok
        and baseline_ok
        and all(model_binding_review.values())
        and all(parser_decision_review.values())
        and all(candidate_coverage_review.values())
        and all(boundary_review.values())
        and blocker_count == 0
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "SLAM Backend Capability Observation Matrix + Review",
        "lifecycle_variant": "compressed_matrix_review_handoff",
        "observation_principle_zh": matrix.get("observation_principle_zh"),
        "model_binding": matrix.get("model_binding"),
        "model_management_chain": matrix.get("model_management_chain"),
        "matrix_review_ok": matrix_ok and baseline_ok,
        "observation_matrix": {
            "observation_entry_count": len(entries),
            "observation_backend_refs": [entry.get("backend_ref") for entry in entries],
            "observation_entries": entries,
        },
        "baseline": baseline,
        "model_binding_review": model_binding_review,
        "parser_decision_review": parser_decision_review,
        "candidate_coverage_review": candidate_coverage_review,
        "boundary_review": boundary_review,
        "conclusions": {
            "best_first_batch_offline_parser_backend": decision.get("best_first_batch_offline_parser_backend"),
            "technical_reference_only_backends": list(decision.get("technical_reference_only_backends") or ()),
            "generic_tum_parser_necessary": decision.get("generic_tum_parser_necessary"),
            "generic_tum_parser_role": decision.get("generic_tum_parser_role"),
            "generic_json_spatial_trace_preferred_internal_standard": decision.get(
                "generic_json_spatial_trace_preferred_internal_standard"
            ),
            "recommended_internal_standard_format": decision.get("recommended_internal_standard_format"),
            "next_phase_minimal_real_output_parser": decision.get("next_phase_minimal_real_output_parser"),
            "parser_priority_order": list(decision.get("parser_priority_order") or ()),
        },
        "blocker_count": blocker_count,
        "failed_checks": all_failed,
        "passed_checks": all_passed,
        "next_phase_hint": NEXT_PHASE_GENERIC_JSON_PARSER,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_REVIEW_BLOCKED,
    }

    handoff = build_observation_handoff_v1(review_result=result, matrix=matrix)
    result["handoff"] = handoff

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        review_path = out_root / REVIEW_FILENAME
        handoff_path = out_root / HANDOFF_FILENAME
        review_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        handoff_path.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        result["output_handoff_file"] = str(handoff_path)

    return result


def main() -> int:
    result = review_slam_backend_capability_observation_v1()
    print(
        json.dumps(
            {
                "matrix_review_ok": result["matrix_review_ok"],
                "observation_entry_count": result["baseline"]["observation_entry_count"],
                "model_management_chain": result.get("model_management_chain"),
                "best_first_batch_offline_parser_backend": result["conclusions"][
                    "best_first_batch_offline_parser_backend"
                ],
                "technical_reference_only_backends": result["conclusions"]["technical_reference_only_backends"],
                "generic_tum_parser_necessary": result["conclusions"]["generic_tum_parser_necessary"],
                "generic_json_spatial_trace_preferred_internal_standard": result["conclusions"][
                    "generic_json_spatial_trace_preferred_internal_standard"
                ],
                "next_phase_minimal_real_output_parser": result["conclusions"][
                    "next_phase_minimal_real_output_parser"
                ],
                "handoff_final_decision": result["handoff"]["final_decision"],
                "blocker_count": result["blocker_count"],
                "output_review_file": result.get("output_review_file"),
                "output_handoff_file": result.get("output_handoff_file"),
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
