# -*- coding: utf-8 -*-
"""SLAM Offline Real Backend Adapter Trial — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.slam_offline_backend_adapter_trial.slam_offline_backend_adapter_trial_types_v1 import (
    ADAPTER_PROFILE_REF,
    DOMAIN_ID,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_CASES,
    GPL_TECHNICAL_REFERENCE_ONLY_STUBS,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_FAMILY,
    MODEL_ID,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    OFFLINE_BACKEND_FORMAT_STUBS,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    SOURCE_CHAIN,
    OfflineSLAMAdapterTrialConfig,
    OfflineSLAMBackendOutputFile,
    OfflineSLAMBackendOutputParser,
    OfflineSLAMParsedEvidenceBundle,
    OfflineSLAMTrialInputManifest,
    OfflineSLAMTrialPlanningDecision,
    OfflineSLAMTrialReviewPolicy,
    candidate_to_dict,
)

REGISTRY_ID = "slam_offline_backend_adapter_trial_registry_v1"
TRIAL_REF = "slam_offline_backend_adapter_trial_v1"

BACKEND_FORMAT_SPECS: Tuple[Tuple[str, str, Tuple[str, ...], str], ...] = (
    (
        "rtab_map_export_stub",
        "RTAB-Map export placeholder",
        ("pose_trace", "local_map_snapshot"),
        "rtab_map_export_record_schema_v1",
    ),
    (
        "kimera_export_stub",
        "Kimera export placeholder",
        ("pose_trace", "mesh_snapshot"),
        "kimera_export_record_schema_v1",
    ),
    (
        "hydra_scene_graph_stub",
        "Hydra scene graph placeholder",
        ("scene_graph_nodes", "anchor_trace"),
        "hydra_scene_graph_record_schema_v1",
    ),
    (
        "orb_slam3_trajectory_stub",
        "ORB-SLAM3 trajectory placeholder",
        ("trajectory_pose", "keyframe_pose"),
        "orb_slam3_trajectory_record_schema_v1",
    ),
    (
        "openvins_trajectory_stub",
        "OpenVINS trajectory placeholder",
        ("vio_pose", "imu_aligned_pose"),
        "openvins_trajectory_record_schema_v1",
    ),
    (
        "generic_tum_trajectory_stub",
        "Generic TUM trajectory placeholder",
        ("tum_pose_line",),
        "generic_tum_trajectory_record_schema_v1",
    ),
    (
        "generic_json_spatial_trace_stub",
        "Generic JSON spatial trace placeholder",
        ("json_pose_record", "json_anchor_record"),
        "generic_json_spatial_trace_record_schema_v1",
    ),
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "offline_backend_format_stubs": OFFLINE_BACKEND_FORMAT_STUBS,
    "gpl_technical_reference_only_stubs": GPL_TECHNICAL_REFERENCE_ONLY_STUBS,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(OFFLINE_BACKEND_FORMAT_STUBS) < 7:
        issues.append("offline_backend_format_stubs_incomplete")
    return len(issues) == 0, issues


def _is_gpl_stub(backend_format_stub: str) -> bool:
    return backend_format_stub in GPL_TECHNICAL_REFERENCE_ONLY_STUBS


def _pose_candidate(*, ref: str, source_chain: Tuple[str, ...]) -> Dict[str, Any]:
    return {
        "candidate_type": "PoseCandidate",
        "pose_ref": ref,
        "source_method": "offline_parser_stub",
        "source_refs": list(source_chain),
        "candidate_only": True,
    }


def build_slam_offline_backend_adapter_trial_matrix_v1() -> Dict[str, Any]:
    output_files: List[OfflineSLAMBackendOutputFile] = []
    parsers: List[OfflineSLAMBackendOutputParser] = []
    manifests: List[OfflineSLAMTrialInputManifest] = []
    configs: List[OfflineSLAMAdapterTrialConfig] = []
    bundles: List[OfflineSLAMParsedEvidenceBundle] = []

    for backend_format_stub, label, record_types, schema_ref in BACKEND_FORMAT_SPECS:
        file_ref = f"offline_file_{backend_format_stub}"
        source_chain = (SOURCE_CHAIN, TRIAL_REF, MODEL_ID, backend_format_stub, file_ref)
        gpl_only = _is_gpl_stub(backend_format_stub)

        output_files.append(
            OfflineSLAMBackendOutputFile(
                file_ref=file_ref,
                backend_format_stub=backend_format_stub,
                file_kind="offline_export_stub",
                source_backend_label=label,
                source_chain=source_chain,
                offline_only=True,
                live_runtime_forbidden=True,
                technical_reference_only=gpl_only,
                commercial_runtime_candidate=False if gpl_only else False,
            )
        )
        parsers.append(
            OfflineSLAMBackendOutputParser(
                parser_ref=f"parser_{backend_format_stub}",
                backend_format_stub=backend_format_stub,
                parser_status="planning_stub",
                supported_record_types=record_types,
                output_record_schema_ref=schema_ref,
                offline_only=True,
                live_runtime_forbidden=True,
            )
        )
        manifests.append(
            OfflineSLAMTrialInputManifest(
                manifest_ref=f"manifest_{backend_format_stub}",
                trial_ref=TRIAL_REF,
                model_id=MODEL_ID,
                backend_format_stub=backend_format_stub,
                input_files=(file_ref,),
                input_mode="offline_file",
                offline_only=True,
                live_camera_forbidden=True,
                live_imu_forbidden=True,
                ros_runtime_forbidden=True,
            )
        )
        configs.append(
            OfflineSLAMAdapterTrialConfig(
                config_ref=f"config_{backend_format_stub}",
                trial_ref=TRIAL_REF,
                model_id=MODEL_ID,
                model_family=MODEL_FAMILY,
                domain_id=DOMAIN_ID,
                model_management_protocol_ref=MODEL_MANAGEMENT_PROTOCOL_REF,
                model_admission_standard_ref=MODEL_ADMISSION_STANDARD_REF,
                adapter_profile_ref=ADAPTER_PROFILE_REF,
                output_candidate_contract_ref=OUTPUT_CANDIDATE_CONTRACT_REF,
                field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
                backend_format_stub=backend_format_stub,
                offline_only=True,
                provider_runtime_activation_allowed=False,
                commercial_runtime_approved=False,
            )
        )

        output_types: Tuple[str, ...]
        if backend_format_stub in ("hydra_scene_graph_stub",):
            output_types = ("SpatialAnchorCandidate", "LocalMapCandidate")
        elif backend_format_stub in ("openvins_trajectory_stub", "orb_slam3_trajectory_stub", "generic_tum_trajectory_stub"):
            output_types = ("PoseCandidate", "MotionCandidate")
        else:
            output_types = ("PoseCandidate", "LocalMapCandidate")

        bundles.append(
            OfflineSLAMParsedEvidenceBundle(
                bundle_ref=f"parsed_bundle_{backend_format_stub}",
                trial_ref=TRIAL_REF,
                model_id=MODEL_ID,
                source_chain=source_chain,
                field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
                output_candidate_types=output_types,
                pose_candidates=(
                    _pose_candidate(ref=f"pose_{backend_format_stub}", source_chain=source_chain),
                )
                if "PoseCandidate" in output_types
                else (),
                motion_candidates=(),
                spatial_anchor_candidates=(),
                local_map_candidates=(),
                slam_health_candidates=(),
                map_drift_candidates=(),
                relocalization_candidates=(),
                direct_action_allowed=False,
                direct_speech_allowed=False,
                direct_fact_write_allowed=False,
            )
        )

    review_policy = OfflineSLAMTrialReviewPolicy(
        policy_ref="slam_offline_trial_review_policy_v1",
        trial_ref=TRIAL_REF,
        review_mode="offline_parse_and_adapter_mapping_review",
        offline_parse_only=True,
        adapter_mapping_required=True,
        field_synthesis_entrypoint_locked=FIELD_SYNTHESIS_ENTRYPOINT,
        provider_runtime_activation_forbidden=True,
        commercial_runtime_approval_forbidden=True,
    )

    planning_decision = OfflineSLAMTrialPlanningDecision(
        decision_ref="slam_offline_backend_adapter_trial_planning_decision_v1",
        trial_ref=TRIAL_REF,
        model_id=MODEL_ID,
        model_family=MODEL_FAMILY,
        domain_id=DOMAIN_ID,
        model_management_protocol_ref=MODEL_MANAGEMENT_PROTOCOL_REF,
        model_admission_standard_ref=MODEL_ADMISSION_STANDARD_REF,
        adapter_profile_ref=ADAPTER_PROFILE_REF,
        output_candidate_contract_ref=OUTPUT_CANDIDATE_CONTRACT_REF,
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        offline_backend_format_stub_count=len(OFFLINE_BACKEND_FORMAT_STUBS),
        not_independent_slam_flow=True,
        offline_only=True,
        provider_runtime_activation_allowed=False,
        commercial_runtime_approved=False,
        candidate_only_enforced=True,
        final_decision=FINAL_DECISION_READY_FOR_CASES,
    )

    return {
        "registry_id": REGISTRY_ID,
        "trial_ref": TRIAL_REF,
        "model_binding": {
            "model_id": MODEL_ID,
            "model_family": MODEL_FAMILY,
            "domain_id": DOMAIN_ID,
            "model_management_protocol_ref": MODEL_MANAGEMENT_PROTOCOL_REF,
            "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
            "adapter_profile_ref": ADAPTER_PROFILE_REF,
            "output_candidate_contract_ref": OUTPUT_CANDIDATE_CONTRACT_REF,
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        },
        "offline_backend_output_files": [candidate_to_dict(x) for x in output_files],
        "offline_backend_output_parsers": [candidate_to_dict(x) for x in parsers],
        "trial_input_manifests": [candidate_to_dict(x) for x in manifests],
        "adapter_trial_configs": [candidate_to_dict(x) for x in configs],
        "parsed_evidence_bundles": [candidate_to_dict(x) for x in bundles],
        "trial_review_policy": candidate_to_dict(review_policy),
        "planning_decision": candidate_to_dict(planning_decision),
        "trial_pipeline": [
            "OfflineSLAMBackendOutputFile",
            "OfflineSLAMBackendOutputParser",
            "OfflineSLAMTrialInputManifest",
            "OfflineSLAMAdapterTrialConfig",
            "OfflineSLAMParsedEvidenceBundle",
            FIELD_SYNTHESIS_ENTRYPOINT,
        ],
    }
