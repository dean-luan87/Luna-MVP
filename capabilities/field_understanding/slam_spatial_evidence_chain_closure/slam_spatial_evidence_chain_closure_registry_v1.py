# -*- coding: utf-8 -*-
"""SLAM Spatial Evidence Chain Closure — registry + closure matrix v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.slam_spatial_evidence_chain_closure.slam_spatial_evidence_chain_closure_types_v1 import (
    ADAPTER_PROFILE_REF,
    CLOSURE_GOVERNANCE_RULES,
    DOMAIN_ID,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_CLOSURE_GO,
    INGEST_CHAIN_REFS,
    INTERFACE_LAYER_PROTOCOL_REF,
    INTERNAL_STANDARD_FORMAT,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_FAMILY,
    MODEL_ID,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    PHASE_ID,
    PLANNING_OBJECT_TYPES,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    SOURCE_INTERFACE_PROFILE,
    STANDARD_EVIDENCE_PIPELINE,
    TARGET_ENTRYPOINT,
    SLAMEvidenceCandidateCoverage,
    SLAMFieldAlignmentDecision,
    SLAMFusionReadinessMatrix,
    SLAMIngestChainRef,
    SLAMSpatialEvidenceChainClosure,
    candidate_to_dict,
)

REGISTRY_ID = "slam_spatial_evidence_chain_closure_registry_v1"
CLOSURE_REF = "slam_spatial_evidence_chain_closure_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "planning_object_types": PLANNING_OBJECT_TYPES,
    "ingest_chain_refs": INGEST_CHAIN_REFS,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
    "closure_governance_rules": CLOSURE_GOVERNANCE_RULES,
    "standard_evidence_pipeline": STANDARD_EVIDENCE_PIPELINE,
}

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, str], ...] = (
    {
        "phase_ref": "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/generic_json_spatial_trace_parser_v1_smoke_v0/"
            "generic_json_spatial_trace_parser_run_and_review_v1.json"
        ),
        "expected_go": "GENERIC_JSON_SPATIAL_TRACE_PARSER_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_json_spatial_trace_parser/"
            "generic_json_spatial_trace_parser_types_v1.py"
        ),
    },
    {
        "phase_ref": "Phase-Generic-TUM-Trajectory-To-JSON-Spatial-Trace-Ingest-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/generic_tum_trajectory_ingest_v1_smoke_v0/"
            "generic_tum_trajectory_ingest_run_and_review_v1.json"
        ),
        "expected_go": "GENERIC_TUM_TRAJECTORY_TO_JSON_SPATIAL_TRACE_INGEST_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_tum_trajectory_ingest/"
            "generic_tum_trajectory_ingest_types_v1.py"
        ),
    },
    {
        "phase_ref": "Phase-RTAB-Map-Trajectory-Export-To-JSON-Spatial-Trace-Fixture-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_trajectory_export_ingest_v1_smoke_v0/"
            "rtab_map_trajectory_export_ingest_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_TRAJECTORY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_trajectory_export_ingest/"
            "rtab_map_trajectory_export_ingest_types_v1.py"
        ),
    },
    {
        "phase_ref": "Phase-RTAB-Map-Odometry-Export-To-JSON-Spatial-Trace-Fixture-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_odometry_export_ingest_v1_smoke_v0/"
            "rtab_map_odometry_export_ingest_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_ODOMETRY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_odometry_export_ingest/"
            "rtab_map_odometry_export_ingest_types_v1.py"
        ),
    },
    {
        "phase_ref": "Phase-RTAB-Map-Graph-Export-To-JSON-Spatial-Trace-Fixture-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_graph_export_ingest_v1_smoke_v0/"
            "rtab_map_graph_export_ingest_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_GRAPH_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_graph_export_ingest/"
            "rtab_map_graph_export_ingest_types_v1.py"
        ),
    },
    {
        "phase_ref": "Phase-Spatial-Odometry-Fusion-Interface-GPS-SLAM-Planning-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/spatial_odometry_fusion_interface_v1_smoke_v0/"
            "spatial_odometry_fusion_interface_review_v1.json"
        ),
        "expected_go": "SPATIAL_ODOMETRY_FUSION_INTERFACE_PLANNING_READY_FOR_FIELD_PROTOCOL_ALIGNMENT",
        "module_rel": (
            "capabilities/field_understanding/spatial_odometry_fusion_interface/"
            "spatial_odometry_fusion_interface_types_v1.py"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "module_rel": (
            "capabilities/midplatform/interface_layer_governance/"
            "interface_layer_governance_types_v1.py"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/model_admission_governance/"
            "model_admission_governance_types_v1.py"
        ),
    },
)

_PIPELINE_SUFFIX: Tuple[str, ...] = (
    INTERNAL_STANDARD_FORMAT,
    "spatial_evidence_candidate_bundle",
    FIELD_SYNTHESIS_ENTRYPOINT,
)


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(PLANNING_OBJECT_TYPES) != 5:
        issues.append("planning_object_types_count_not_5")
    if len(INGEST_CHAIN_REFS) != 5:
        issues.append("ingest_chain_refs_count_not_5")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 8:
        issues.append("sealed_upstream_phase_refs_count_not_8")
    if len(CLOSURE_GOVERNANCE_RULES) != 10:
        issues.append("closure_governance_rules_count_not_10")
    return len(issues) == 0, issues


def build_ingest_chain_refs_v1() -> Tuple[SLAMIngestChainRef, ...]:
    common_tail = _PIPELINE_SUFFIX
    return (
        SLAMIngestChainRef(
            chain_ref="generic_tum_trajectory_chain",
            source_format_ref="generic_tum_trajectory",
            ingest_module_ref="generic_tum_trajectory_ingest_v1",
            upstream_phase_ref="Phase-Generic-TUM-Trajectory-To-JSON-Spatial-Trace-Ingest-v1-001",
            upstream_go_decision="GENERIC_TUM_TRAJECTORY_TO_JSON_SPATIAL_TRACE_INGEST_REVIEW_GO",
            pipeline=("generic_tum_trajectory", "generic_tum_trajectory_ingest_v1") + common_tail,
            output_candidate_types=("PoseCandidate", "MotionCandidate"),
            generic_json_spatial_trace_required=True,
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        ),
        SLAMIngestChainRef(
            chain_ref="rtab_map_trajectory_chain",
            source_format_ref="rtab_map_trajectory_export_subset",
            ingest_module_ref="rtab_map_trajectory_export_ingest_v1",
            upstream_phase_ref=(
                "Phase-RTAB-Map-Trajectory-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
            ),
            upstream_go_decision="RTAB_MAP_TRAJECTORY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
            pipeline=("rtab_map_trajectory_export_subset", "rtab_map_trajectory_export_ingest_v1")
            + common_tail,
            output_candidate_types=("PoseCandidate", "MotionCandidate"),
            generic_json_spatial_trace_required=True,
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        ),
        SLAMIngestChainRef(
            chain_ref="rtab_map_odometry_chain",
            source_format_ref="rtab_map_odometry_export_subset",
            ingest_module_ref="rtab_map_odometry_export_ingest_v1",
            upstream_phase_ref=(
                "Phase-RTAB-Map-Odometry-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
            ),
            upstream_go_decision="RTAB_MAP_ODOMETRY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
            pipeline=("rtab_map_odometry_export_subset", "rtab_map_odometry_export_ingest_v1")
            + common_tail,
            output_candidate_types=("PoseCandidate", "MotionCandidate", "SLAMHealthCandidate"),
            generic_json_spatial_trace_required=True,
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        ),
        SLAMIngestChainRef(
            chain_ref="rtab_map_graph_chain",
            source_format_ref="rtab_map_graph_export_subset",
            ingest_module_ref="rtab_map_graph_export_ingest_v1",
            upstream_phase_ref="Phase-RTAB-Map-Graph-Export-To-JSON-Spatial-Trace-Fixture-v1-001",
            upstream_go_decision="RTAB_MAP_GRAPH_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
            pipeline=("rtab_map_graph_export_subset", "rtab_map_graph_export_ingest_v1") + common_tail,
            output_candidate_types=(
                "SpatialAnchorCandidate",
                "RelocalizationCandidate",
                "MapDriftCandidate",
            ),
            generic_json_spatial_trace_required=True,
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        ),
        SLAMIngestChainRef(
            chain_ref="spatial_odometry_fusion_chain",
            source_format_ref="gps_stub+slam_local_odometry+rtab_graph_anchor",
            ingest_module_ref="spatial_odometry_fusion_interface_v1",
            upstream_phase_ref="Phase-Spatial-Odometry-Fusion-Interface-GPS-SLAM-Planning-v1-001",
            upstream_go_decision=(
                "SPATIAL_ODOMETRY_FUSION_INTERFACE_PLANNING_READY_FOR_FIELD_PROTOCOL_ALIGNMENT"
            ),
            pipeline=(
                "gps_gnss_coarse_position_stub",
                "generic_json_spatial_trace_pose_motion",
                "rtab_map_graph_export_subset",
                "spatial_odometry_fusion_interface_v1",
                "spatial_odometry_fusion_candidate",
                FIELD_SYNTHESIS_ENTRYPOINT,
            ),
            output_candidate_types=(
                "SpatialOdometryFusionCandidate",
                "ConflictCandidate",
                "MapAlignmentHintCandidate",
            ),
            generic_json_spatial_trace_required=True,
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        ),
    )


def build_candidate_coverage_v1(chains: Tuple[SLAMIngestChainRef, ...]) -> SLAMEvidenceCandidateCoverage:
    output_types = {ctype for chain in chains for ctype in chain.output_candidate_types}
    return SLAMEvidenceCandidateCoverage(
        coverage_ref="slam_evidence_candidate_coverage_v1",
        pose_supported="PoseCandidate" in output_types,
        motion_supported="MotionCandidate" in output_types,
        health_supported="SLAMHealthCandidate" in output_types,
        anchor_supported="SpatialAnchorCandidate" in output_types,
        relocalization_supported="RelocalizationCandidate" in output_types,
        drift_supported="MapDriftCandidate" in output_types,
        gps_gnss_stub_supported=True,
        spatial_odometry_fusion_supported="SpatialOdometryFusionCandidate" in output_types,
        conflict_candidate_supported="ConflictCandidate" in output_types,
        field_synthesis_entrypoint_locked=FIELD_SYNTHESIS_ENTRYPOINT,
    )


def build_fusion_readiness_matrix_v1() -> SLAMFusionReadinessMatrix:
    return SLAMFusionReadinessMatrix(
        matrix_ref="slam_fusion_readiness_matrix_v1",
        fusion_interface_ref="spatial_odometry_fusion_interface",
        fusion_scenario_count=5,
        gps_slam_division_locked=True,
        conflict_candidate_path_locked=True,
        alignment_hint_path_locked=True,
        field_protocol_alignment_next=True,
    )


def build_slam_spatial_evidence_chain_closure_matrix_v1() -> Dict[str, Any]:
    chains = build_ingest_chain_refs_v1()
    coverage = build_candidate_coverage_v1(chains)
    fusion_readiness = build_fusion_readiness_matrix_v1()

    closure = SLAMSpatialEvidenceChainClosure(
        closure_ref=CLOSURE_REF,
        phase_id=PHASE_ID,
        interface_layer_protocol_ref=INTERFACE_LAYER_PROTOCOL_REF,
        model_management_protocol_ref=MODEL_MANAGEMENT_PROTOCOL_REF,
        model_id=MODEL_ID,
        internal_standard_format=INTERNAL_STANDARD_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        standard_evidence_pipeline=STANDARD_EVIDENCE_PIPELINE,
        ingest_chain_refs=INGEST_CHAIN_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=CLOSURE_GOVERNANCE_RULES,
    )

    decision = SLAMFieldAlignmentDecision(
        decision_ref="slam_field_alignment_decision_v1",
        closure_ref=CLOSURE_REF,
        chain_count=len(chains),
        generic_json_spatial_trace_required=True,
        backend_native_output_direct_to_field_blocked=True,
        gps_does_not_override_field_identity=True,
        relocalization_does_not_restore_runtime_trust=True,
        runtime_activation_allowed=False,
        direct_action_allowed=False,
        direct_speech_allowed=False,
        direct_fact_write_allowed=False,
        final_decision=FINAL_DECISION_CLOSURE_GO,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "model_binding": {
            "model_id": MODEL_ID,
            "model_family": MODEL_FAMILY,
            "domain_id": DOMAIN_ID,
            "model_management_protocol_ref": MODEL_MANAGEMENT_PROTOCOL_REF,
            "interface_layer_protocol_ref": INTERFACE_LAYER_PROTOCOL_REF,
            "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
            "source_interface_profile": SOURCE_INTERFACE_PROFILE,
            "internal_standard_format": INTERNAL_STANDARD_FORMAT,
            "adapter_profile_ref": ADAPTER_PROFILE_REF,
            "target_entrypoint": TARGET_ENTRYPOINT,
        },
        "slam_spatial_evidence_chain_closure": candidate_to_dict(closure),
        "ingest_chain_refs": [candidate_to_dict(chain) for chain in chains],
        "candidate_coverage": candidate_to_dict(coverage),
        "fusion_readiness_matrix": candidate_to_dict(fusion_readiness),
        "field_alignment_decision": candidate_to_dict(decision),
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "standard_evidence_pipeline": list(STANDARD_EVIDENCE_PIPELINE),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
    }
