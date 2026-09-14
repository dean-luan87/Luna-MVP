# -*- coding: utf-8 -*-
"""RTAB-Map Offline Export Ingest Planning — matrix + review (compressed)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.rtab_map_offline_export_ingest_planning.rtab_map_offline_export_ingest_planning_registry_v1 import (
    FORBIDDEN_ARCHITECTURE_RULES,
    INGEST_PIPELINE,
    MODEL_BINDING,
    OBSERVATION_EXPORT_SUBSETS,
    P0_EXPORT_SUBSETS,
    P1_EXPORT_SUBSETS,
    P2_EXPORT_SUBSETS,
    PLANNING_REF,
    REGISTRY_ID,
    SUBSET_PLANNING_DIMENSIONS,
    validate_registry,
    validate_subset_entry_shape,
)
from capabilities.field_understanding.rtab_map_offline_export_ingest_planning.rtab_map_offline_export_ingest_planning_types_v1 import (
    ADAPTER_PROFILE_REF,
    EXPORT_SUBSET_REFS,
    FINAL_DECISION_READY_FOR_SUBSET_FIXTURE,
    FINAL_DECISION_REVIEW_BLOCKED,
    GENERIC_JSON_PARSER_REF,
    MODEL_ADMISSION_STANDARD_REF,
    NON_EXECUTION_FLAGS,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    PHASE_ID,
    PLANNING_PRINCIPLE_ZH,
    RTABMapExportSubsetPlanningEntry,
    RTABMapOfflineExportIngestPlanningDecision,
    SOURCE_INTERNAL_STANDARD,
    TARGET_ENTRYPOINT,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "rtab_map_offline_export_ingest_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "rtab_map_offline_export_ingest_planning_review_v1.json"

FINAL_DECISION_GO = FINAL_DECISION_READY_FOR_SUBSET_FIXTURE

STEP_FILES = (
    "capabilities/field_understanding/rtab_map_offline_export_ingest_planning/rtab_map_offline_export_ingest_planning_types_v1.py",
    "capabilities/field_understanding/rtab_map_offline_export_ingest_planning/rtab_map_offline_export_ingest_planning_registry_v1.py",
    "capabilities/field_understanding/rtab_map_offline_export_ingest_planning/review_rtab_map_offline_export_ingest_planning_v1.py",
)

RUNTIME_BINDING_PATTERNS = (
    "cv2.VideoCapture",
    "rospy",
    "ros::",
    "rtabmap::",
    "import rtabmap",
)


def build_export_subset_entries_v1() -> Tuple[RTABMapExportSubsetPlanningEntry, ...]:
    return (
        RTABMapExportSubsetPlanningEntry(
            subset_ref="trajectory_export_subset",
            source_export_kind="rtabmap_trajectory_txt_or_tum_compatible",
            expected_fields=(
                "timestamp",
                "tx",
                "ty",
                "tz",
                "qx",
                "qy",
                "qz",
                "qw",
                "session_id",
            ),
            required_fields=("timestamp", "tx", "ty", "tz", "qx", "qy", "qz", "qw"),
            optional_fields=("session_id", "label", "covariance_hint"),
            luna_candidate_mapping={
                "PoseCandidate": "high",
                "MotionCandidate": "high",
            },
            generic_json_trace_mapping={
                "pose": "candidate_type=pose with timestamp_ms and pose payload",
                "motion": "companion motion from consecutive trajectory samples",
            },
            lossy_conversion_notes=(
                "RTAB-Map trajectory export may omit covariance; Luna keeps confidence placeholder.",
                "Quaternion normalization required before JSON trace emit.",
            ),
            unsupported_fields=(
                "rtabmap_database_binary",
                "ros_tf_tree",
                "raw_keyframe_images",
            ),
            offline_feasibility="high",
            parser_priority="p0",
            risk_level="low",
        ),
        RTABMapExportSubsetPlanningEntry(
            subset_ref="odometry_export_subset",
            source_export_kind="rtabmap_odometry_log_export",
            expected_fields=(
                "timestamp",
                "odom_pose",
                "linear_velocity",
                "angular_velocity",
                "tracking_state",
                "odom_frame_id",
            ),
            required_fields=("timestamp", "odom_pose", "tracking_state"),
            optional_fields=("linear_velocity", "angular_velocity", "odom_frame_id", "covariance"),
            luna_candidate_mapping={
                "PoseCandidate": "high",
                "MotionCandidate": "high",
                "SLAMHealthCandidate": "medium",
            },
            generic_json_trace_mapping={
                "pose": "odom_pose mapped to pose JSON trace item",
                "motion": "velocity fields mapped to motion JSON trace item",
                "health": "tracking_state mapped to health JSON trace item when degraded",
            },
            lossy_conversion_notes=(
                "Odometry tracking_state is mapped to SLAMHealthCandidate degraded/normal hints.",
                "Velocity may be absent in some exports; motion item becomes optional.",
            ),
            unsupported_fields=(
                "wheel_odometry_raw_packets",
                "imu_raw_stream",
                "rtabmap_database_nodes",
            ),
            offline_feasibility="high",
            parser_priority="p0",
            risk_level="low",
        ),
        RTABMapExportSubsetPlanningEntry(
            subset_ref="graph_export_subset",
            source_export_kind="rtabmap_pose_graph_export",
            expected_fields=(
                "node_id",
                "pose",
                "edge_from",
                "edge_to",
                "constraint_type",
                "loop_closure_flag",
                "drift_hint",
            ),
            required_fields=("node_id", "pose"),
            optional_fields=(
                "edge_from",
                "edge_to",
                "constraint_type",
                "loop_closure_flag",
                "drift_hint",
                "relocalization_event",
            ),
            luna_candidate_mapping={
                "SpatialAnchorCandidate": "high",
                "RelocalizationCandidate": "medium",
                "MapDriftCandidate": "medium",
            },
            generic_json_trace_mapping={
                "anchor": "graph node pose as anchor JSON trace item",
                "relocalization": "loop_closure_flag or relocalization_event to relocalization trace",
                "drift": "drift_hint to drift JSON trace item",
            },
            lossy_conversion_notes=(
                "Full pose graph topology is not preserved in Luna standard; only candidate subsets.",
                "Loop closure events may be collapsed to relocalization candidate hints.",
            ),
            unsupported_fields=(
                "full_g2o_graph_binary",
                "visual_word_index",
                "bag_of_words_vectors",
            ),
            offline_feasibility="medium",
            parser_priority="p1",
            risk_level="medium",
        ),
        RTABMapExportSubsetPlanningEntry(
            subset_ref="local_map_metadata_subset",
            source_export_kind="rtabmap_local_map_metadata_export",
            expected_fields=(
                "map_id",
                "node_count",
                "edge_count",
                "map_bounds",
                "last_updated_timestamp",
                "map_quality_hint",
            ),
            required_fields=("map_id", "last_updated_timestamp"),
            optional_fields=(
                "node_count",
                "edge_count",
                "map_bounds",
                "map_quality_hint",
                "working_memory_size",
            ),
            luna_candidate_mapping={
                "LocalMapCandidate": "high",
            },
            generic_json_trace_mapping={
                "local_map": "metadata-only local_map JSON trace item without geometry payload",
            },
            lossy_conversion_notes=(
                "Only local map metadata enters Luna; geometry stays external.",
                "No direct long-term map write from RTAB-Map export.",
            ),
            unsupported_fields=(
                "dense_point_cloud",
                "mesh_vertices",
                "texture_atlases",
            ),
            offline_feasibility="medium",
            parser_priority="p2",
            risk_level="medium",
        ),
        RTABMapExportSubsetPlanningEntry(
            subset_ref="occupancy_or_pointcloud_metadata_subset",
            source_export_kind="rtabmap_occupancy_or_pointcloud_metadata_export",
            expected_fields=(
                "grid_resolution",
                "grid_origin",
                "occupied_cell_count",
                "point_count",
                "sensor_modality",
                "export_timestamp",
            ),
            required_fields=("export_timestamp",),
            optional_fields=(
                "grid_resolution",
                "grid_origin",
                "occupied_cell_count",
                "point_count",
                "sensor_modality",
                "bounding_box",
            ),
            luna_candidate_mapping={
                "LocalMapCandidate": "medium",
                "SpatialAnchorCandidate": "low",
            },
            generic_json_trace_mapping={
                "local_map": "occupancy metadata as local_map placeholder trace",
                "anchor": "grid_origin or bounding_box anchor placeholder only",
            },
            lossy_conversion_notes=(
                "Occupancy grid and point cloud raw payloads are observation-only metadata.",
                "Large spatial payloads must not enter candidate bundle directly.",
            ),
            unsupported_fields=(
                "occupancy_grid_cells",
                "point_cloud_xyz_rgb",
                "octomap_binary",
                "ply_mesh_full",
            ),
            offline_feasibility="low",
            parser_priority="observation",
            risk_level="high",
        ),
    )


def build_planning_decision_v1() -> RTABMapOfflineExportIngestPlanningDecision:
    return RTABMapOfflineExportIngestPlanningDecision(
        decision_ref="rtab_map_offline_export_ingest_planning_decision_v1",
        planning_ref=PLANNING_REF,
        model_id=MODEL_BINDING["model_id"],
        model_family=MODEL_BINDING["model_family"],
        domain_id=MODEL_BINDING["domain_id"],
        model_management_protocol_ref=MODEL_BINDING["model_management_protocol_ref"],
        model_admission_standard_ref=MODEL_BINDING["model_admission_standard_ref"],
        source_internal_standard=SOURCE_INTERNAL_STANDARD,
        target_entrypoint=TARGET_ENTRYPOINT,
        adapter_profile_ref=ADAPTER_PROFILE_REF,
        output_candidate_contract_ref=OUTPUT_CANDIDATE_CONTRACT_REF,
        p0_export_subsets=P0_EXPORT_SUBSETS,
        p1_export_subsets=P1_EXPORT_SUBSETS,
        p2_export_subsets=P2_EXPORT_SUBSETS,
        observation_export_subsets=OBSERVATION_EXPORT_SUBSETS,
        recommended_first_subset_fixture="trajectory_export_subset",
        ingest_pipeline=INGEST_PIPELINE,
        architecture_principle_locked=True,
        offline_planning_only=True,
        no_runtime_activation=True,
        final_decision=FINAL_DECISION_READY_FOR_SUBSET_FIXTURE,
    )


def build_rtab_map_offline_export_ingest_planning_matrix_v1() -> Dict[str, Any]:
    entries = build_export_subset_entries_v1()
    decision = build_planning_decision_v1()
    return {
        "registry_id": REGISTRY_ID,
        "planning_ref": PLANNING_REF,
        "phase_id": PHASE_ID,
        "model_binding": dict(MODEL_BINDING),
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "forbidden_architecture_rules": list(FORBIDDEN_ARCHITECTURE_RULES),
        "export_subset_entries": [candidate_to_dict(entry) for entry in entries],
        "planning_decision": candidate_to_dict(decision),
        "ingest_pipeline": list(INGEST_PIPELINE),
    }


def validate_planning_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_rtab_map_offline_export_ingest_planning_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    binding = matrix.get("model_binding") or {}
    for key, expected in MODEL_BINDING.items():
        if binding.get(key) != expected:
            issues.append(f"model_binding.{key}: expected={expected!r}, actual={binding.get(key)!r}")

    entries = matrix.get("export_subset_entries") or []
    if len(entries) != 5:
        issues.append(f"export_subset_entry_count:{len(entries)}")

    subset_refs = {entry.get("subset_ref") for entry in entries}
    for subset_ref in EXPORT_SUBSET_REFS:
        if subset_ref not in subset_refs:
            issues.append(f"missing_export_subset:{subset_ref}")

    for entry in entries:
        ok, part = validate_subset_entry_shape(entry)
        if not ok:
            issues.extend([f"{entry.get('subset_ref')}.{err}" for err in part])

        serialized = json.dumps(entry, ensure_ascii=False).lower()
        if "rtabmap_database" in serialized and entry.get("subset_ref"):
            if "unsupported_fields" not in serialized:
                pass
        for forbidden in ("occupancy_grid_cells", "point_cloud_xyz_rgb", "ros_tf_tree"):
            if forbidden in (entry.get("expected_fields") or ()):
                issues.append(f"{entry.get('subset_ref')}.forbidden_field_in_expected:{forbidden}")

    decision = matrix.get("planning_decision") or {}
    if tuple(decision.get("p0_export_subsets") or ()) != P0_EXPORT_SUBSETS:
        issues.append("decision.p0_export_subsets_mismatch")
    if tuple(decision.get("p1_export_subsets") or ()) != P1_EXPORT_SUBSETS:
        issues.append("decision.p1_export_subsets_mismatch")
    if tuple(decision.get("p2_export_subsets") or ()) != P2_EXPORT_SUBSETS:
        issues.append("decision.p2_export_subsets_mismatch")
    if tuple(decision.get("observation_export_subsets") or ()) != OBSERVATION_EXPORT_SUBSETS:
        issues.append("decision.observation_export_subsets_mismatch")
    if decision.get("source_internal_standard") != SOURCE_INTERNAL_STANDARD:
        issues.append("decision.source_internal_standard_not_generic_json")
    if decision.get("target_entrypoint") != TARGET_ENTRYPOINT:
        issues.append("decision.target_entrypoint_not_field_synthesis_v1")
    if decision.get("recommended_first_subset_fixture") not in P0_EXPORT_SUBSETS:
        issues.append("decision.recommended_first_subset_not_p0")
    if decision.get("architecture_principle_locked") is not True:
        issues.append("decision.architecture_principle_not_locked")
    if decision.get("offline_planning_only") is not True:
        issues.append("decision.offline_planning_only_required")
    if decision.get("no_runtime_activation") is not True:
        issues.append("decision.no_runtime_activation_required")
    if decision.get("final_decision") != FINAL_DECISION_READY_FOR_SUBSET_FIXTURE:
        issues.append("decision.final_decision_not_ready")

    flags = matrix.get("non_execution_flags") or {}
    for flag in (
        "no_rtabmap_runtime",
        "no_rtabmap_database_read",
        "no_ros_runtime",
        "no_provider_runtime_activation",
        "no_long_term_map_write",
        "no_commercial_runtime_approval",
    ):
        if flags.get(flag) is not True:
            issues.append(f"non_execution.{flag}_required")

    pipeline = matrix.get("ingest_pipeline") or []
    if SOURCE_INTERNAL_STANDARD not in pipeline:
        issues.append("ingest_pipeline_missing_generic_json_spatial_trace")
    if TARGET_ENTRYPOINT not in pipeline:
        issues.append("ingest_pipeline_missing_field_synthesis_v1")
    if GENERIC_JSON_PARSER_REF not in pipeline:
        issues.append("ingest_pipeline_missing_generic_json_parser")

    return len(issues) == 0 and registry_ok, issues


def review_architecture_rules(matrix: Dict[str, Any]) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    entries = matrix.get("export_subset_entries") or []
    decision = matrix.get("planning_decision") or {}
    flags = matrix.get("non_execution_flags") or {}

    no_database_as_standard = all(
        "rtabmap_database" not in (entry.get("required_fields") or ())
        and "rtabmap_database" not in (entry.get("expected_fields") or ())
        for entry in entries
    )
    no_ros_as_standard = all(
        "ros_" not in field
        for entry in entries
        for field in (entry.get("required_fields") or ()) + (entry.get("expected_fields") or ())
    )
    no_raw_pointcloud = all(
        "point_cloud_xyz_rgb" in (entry.get("unsupported_fields") or ())
        or "dense_point_cloud" in (entry.get("unsupported_fields") or ())
        for entry in entries
        if entry.get("subset_ref") == "occupancy_or_pointcloud_metadata_subset"
        or entry.get("subset_ref") == "local_map_metadata_subset"
    )
    no_long_term_map_write = flags.get("no_long_term_map_write") is True
    no_json_bypass = decision.get("source_internal_standard") == SOURCE_INTERNAL_STANDARD
    no_synthesis_bypass = decision.get("target_entrypoint") == TARGET_ENTRYPOINT
    no_runtime = decision.get("no_runtime_activation") is True
    no_commercial = flags.get("no_commercial_runtime_approval") is True

    checks = {
        "rtabmap_database_not_luna_standard": no_database_as_standard,
        "ros_topic_not_luna_standard": no_ros_as_standard,
        "no_raw_pointcloud_in_candidate": no_raw_pointcloud,
        "no_occupancy_map_long_term_write": no_long_term_map_write,
        "no_generic_json_spatial_trace_bypass": no_json_bypass,
        "no_field_synthesis_v1_bypass": no_synthesis_bypass,
        "no_provider_runtime_activation": flags.get("no_provider_runtime_activation") is True,
        "no_commercial_runtime_approval": no_commercial,
    }

    for key, ok in checks.items():
        if ok:
            passed.append(f"architecture.{key}=true")
        else:
            failed.append(f"architecture.{key}=false")

    return checks, passed, failed


def review_priority_partition(decision: Dict[str, Any]) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    checks = {
        "p0_trajectory_and_odometry": tuple(decision.get("p0_export_subsets") or ()) == P0_EXPORT_SUBSETS,
        "p1_graph_subset": tuple(decision.get("p1_export_subsets") or ()) == P1_EXPORT_SUBSETS,
        "p2_local_map_metadata": tuple(decision.get("p2_export_subsets") or ()) == P2_EXPORT_SUBSETS,
        "observation_occupancy_pointcloud_metadata": tuple(
            decision.get("observation_export_subsets") or ()
        )
        == OBSERVATION_EXPORT_SUBSETS,
        "recommended_first_subset_is_p0": decision.get("recommended_first_subset_fixture")
        == "trajectory_export_subset",
    }

    for key, ok in checks.items():
        if ok:
            passed.append(f"priority.{key}=true")
        else:
            failed.append(f"priority.{key}=false")

    return checks, passed, failed


def review_non_execution_boundary() -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    flags = dict(NON_EXECUTION_FLAGS)
    boundary = {
        "no_rtabmap_runtime": flags.get("no_rtabmap_runtime") is True,
        "no_rtabmap_database_read": flags.get("no_rtabmap_database_read") is True,
        "no_ros_runtime": flags.get("no_ros_runtime") is True,
        "no_live_camera": flags.get("no_live_camera") is True,
        "no_live_imu": flags.get("no_live_imu") is True,
        "no_provider_runtime_activation": flags.get("no_provider_runtime_activation") is True,
        "runtime_activation_allowed": flags.get("runtime_activation_allowed") is False,
    }

    planning_root = _REPO_ROOT / "capabilities" / "field_understanding" / "rtab_map_offline_export_ingest_planning"
    for py_path in planning_root.rglob("*.py"):
        if py_path.name == "review_rtab_map_offline_export_ingest_planning_v1.py":
            continue
        text = py_path.read_text(encoding="utf-8").lower()
        for pattern in RUNTIME_BINDING_PATTERNS:
            if pattern.lower() in text:
                failed.append(f"boundary.runtime_binding={py_path.name}:{pattern}")

    for key, ok in boundary.items():
        if key == "runtime_activation_allowed":
            if ok:
                passed.append("boundary.runtime_activation_allowed=false")
            else:
                failed.append("boundary.runtime_activation_allowed=true")
        elif ok:
            passed.append(f"boundary.{key}=true")
        else:
            failed.append(f"boundary.{key}=false")

    return boundary, passed, failed


def review_rtab_map_offline_export_ingest_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_rtab_map_offline_export_ingest_planning_matrix_v1()
    matrix_ok, matrix_issues = validate_planning_matrix_v1(matrix)
    registry_ok, registry_issues = validate_registry()

    entries = matrix.get("export_subset_entries") or []
    decision = matrix.get("planning_decision") or {}

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

    architecture_review, p, f = review_architecture_rules(matrix)
    all_passed.extend(p)
    all_failed.extend(f)

    priority_review, p, f = review_priority_partition(decision)
    all_passed.extend(p)
    all_failed.extend(f)

    boundary_review, p, f = review_non_execution_boundary()
    all_passed.extend(p)
    all_failed.extend(f)

    blocker_count = len(all_failed)
    review_ok = (
        matrix_ok
        and registry_ok
        and all(architecture_review.values())
        and all(priority_review.values())
        and all(boundary_review.values())
        and blocker_count == 0
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RTAB-Map Offline Export Ingest Planning Matrix + Review",
        "lifecycle_variant": "compressed_matrix_review",
        "planning_principle_zh": matrix.get("planning_principle_zh"),
        "model_binding": matrix.get("model_binding"),
        "ingest_pipeline": matrix.get("ingest_pipeline"),
        "forbidden_architecture_rules": list(FORBIDDEN_ARCHITECTURE_RULES),
        "matrix_review_ok": matrix_ok,
        "export_subset_entry_count": len(entries),
        "export_subset_refs": [entry.get("subset_ref") for entry in entries],
        "subset_planning_dimension_count": len(SUBSET_PLANNING_DIMENSIONS),
        "architecture_review": architecture_review,
        "priority_review": priority_review,
        "boundary_review": boundary_review,
        "planning_decision": decision,
        "conclusions": {
            "p0_export_subsets": list(decision.get("p0_export_subsets") or ()),
            "p1_export_subsets": list(decision.get("p1_export_subsets") or ()),
            "p2_export_subsets": list(decision.get("p2_export_subsets") or ()),
            "observation_export_subsets": list(decision.get("observation_export_subsets") or ()),
            "recommended_first_subset_fixture": decision.get("recommended_first_subset_fixture"),
            "source_internal_standard": decision.get("source_internal_standard"),
            "target_entrypoint": decision.get("target_entrypoint"),
            "next_step_hint": (
                "Build P0 trajectory_export_subset or odometry_export_subset fixture "
                "and convert to Generic JSON Spatial Trace"
            ),
        },
        "export_subset_entries": entries,
        "blocker_count": blocker_count,
        "failed_checks": all_failed,
        "passed_checks": all_passed,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_REVIEW_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_rtab_map_offline_export_ingest_planning_v1()
    print(
        json.dumps(
            {
                "matrix_review_ok": result["matrix_review_ok"],
                "export_subset_entry_count": result["export_subset_entry_count"],
                "p0_export_subsets": result["conclusions"]["p0_export_subsets"],
                "p1_export_subsets": result["conclusions"]["p1_export_subsets"],
                "p2_export_subsets": result["conclusions"]["p2_export_subsets"],
                "observation_export_subsets": result["conclusions"]["observation_export_subsets"],
                "recommended_first_subset_fixture": result["conclusions"]["recommended_first_subset_fixture"],
                "source_internal_standard": result["conclusions"]["source_internal_standard"],
                "target_entrypoint": result["conclusions"]["target_entrypoint"],
                "blocker_count": result["blocker_count"],
                "output_review_file": result.get("output_review_file"),
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
