# -*- coding: utf-8 -*-
"""SLAM Spatial Evidence Adapter Skeleton — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.slam_spatial_evidence_adapter.slam_spatial_evidence_adapter_types_v1 import (
    ALLOWED_INPUT_MODES,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    GENERIC_SLAM_ADAPTER_CONTRACT_REF,
    MOCK_BACKEND_KINDS,
    RESERVED_CANDIDATE_TYPES,
    RESERVED_INPUT_MODES,
    SOURCE_CHAIN,
    SUPPORTED_CANDIDATE_TYPES,
    SLAMAdapterHealthReport,
    SLAMAdapterInputEnvelope,
    SLAMAdapterMappingRule,
    SLAMAdapterOutputBundle,
    SLAMAdapterPlanningDecision,
    SLAMBackendOutputFrame,
    SLAMSpatialEvidenceAdapter,
    MockSLAMBackendOutput,
    candidate_to_dict,
)

REGISTRY_ID = "slam_spatial_evidence_adapter_registry_v1"

ADAPTER_REFS: Tuple[str, ...] = (
    "adapter_mock_vio_pose_motion",
    "adapter_mock_visual_slam_anchor_localmap",
    "adapter_mock_rgbd_localmap_health",
    "adapter_mock_metric_semantic_anchor_graph",
    "adapter_mock_scene_graph_field_structure",
)

FORBIDDEN_ADAPTER_POLICIES: Tuple[str, ...] = (
    "direct_action_from_slam_candidate",
    "direct_speech_from_slam_candidate",
    "direct_fact_write_from_local_map",
    "persistent_map_write_from_adapter",
    "commercial_runtime_without_license_gate",
    "real_backend_bypass_adapter_contract",
    "vision_ocr_candidate_pollution",
    "runtime_trust_restore_from_relocalization",
    "ready_for_action_from_high_drift",
    "destination_confirm_from_spatial_anchor",
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "mock_backend_kinds": MOCK_BACKEND_KINDS,
    "allowed_input_modes": ALLOWED_INPUT_MODES,
    "reserved_input_modes": RESERVED_INPUT_MODES,
    "supported_candidate_types": SUPPORTED_CANDIDATE_TYPES,
    "reserved_candidate_types": RESERVED_CANDIDATE_TYPES,
    "adapter_refs": ADAPTER_REFS,
    "forbidden_adapter_policies": FORBIDDEN_ADAPTER_POLICIES,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for domain, values in REGISTRY.items():
        if not values:
            issues.append(f"registry_domain_missing:{domain}")
    if len(ADAPTER_REFS) < 5:
        issues.append("adapter_refs_incomplete")
    if len(SUPPORTED_CANDIDATE_TYPES) < 7:
        issues.append("supported_candidate_types_incomplete")
    return len(issues) == 0, issues


def _pose_candidate(
    *,
    pose_ref: str,
    source_method: str,
    source_refs: Tuple[str, ...],
) -> Dict[str, Any]:
    return {
        "candidate_type": "PoseCandidate",
        "pose_ref": pose_ref,
        "source_method": source_method,
        "source_refs": list(source_refs),
        "pose_confidence": 0.72,
        "candidate_only": True,
    }


def _motion_candidate(*, motion_ref: str, source_refs: Tuple[str, ...]) -> Dict[str, Any]:
    return {
        "candidate_type": "MotionCandidate",
        "motion_ref": motion_ref,
        "source_refs": list(source_refs),
        "action_ready": False,
        "candidate_only": True,
    }


def _anchor_candidate(*, anchor_ref: str, source_refs: Tuple[str, ...]) -> Dict[str, Any]:
    return {
        "candidate_type": "SpatialAnchorCandidate",
        "anchor_ref": anchor_ref,
        "source_refs": list(source_refs),
        "confirm_destination": False,
        "candidate_only": True,
    }


def _local_map_candidate(*, local_map_ref: str, source_refs: Tuple[str, ...]) -> Dict[str, Any]:
    return {
        "candidate_type": "LocalMapCandidate",
        "local_map_ref": local_map_ref,
        "source_refs": list(source_refs),
        "persistent_map": False,
        "long_term_fact": False,
        "candidate_only": True,
    }


def _health_candidate(*, health_ref: str, source_refs: Tuple[str, ...]) -> Dict[str, Any]:
    return {
        "candidate_type": "SLAMHealthCandidate",
        "health_ref": health_ref,
        "source_refs": list(source_refs),
        "degradation_effect": "confidence_downweight",
        "needs_more_observation": True,
        "candidate_only": True,
    }


def _drift_candidate(*, drift_ref: str, drift_risk: str, source_refs: Tuple[str, ...]) -> Dict[str, Any]:
    return {
        "candidate_type": "MapDriftCandidate",
        "drift_ref": drift_ref,
        "drift_risk": drift_risk,
        "source_refs": list(source_refs),
        "ready_for_action_decision": False,
        "candidate_only": True,
    }


def _relocalization_candidate(
    *, relocalization_ref: str, source_refs: Tuple[str, ...]
) -> Dict[str, Any]:
    return {
        "candidate_type": "RelocalizationCandidate",
        "relocalization_ref": relocalization_ref,
        "source_refs": list(source_refs),
        "restore_runtime_trust": False,
        "candidate_only": True,
    }


def _backend_output(
    *,
    backend_ref: str,
    backend_kind: str,
    backend_label: str,
    frame_ref: str,
) -> MockSLAMBackendOutput:
    return MockSLAMBackendOutput(
        backend_ref=backend_ref,
        backend_kind=backend_kind,
        backend_label=backend_label,
        output_mode="mock_trace",
        frame_refs=(frame_ref,),
        source_chain=(SOURCE_CHAIN, backend_ref, frame_ref),
        real_backend_connected=False,
        runtime_execution_allowed=False,
        provider_activation_allowed=False,
        commercial_runtime_candidate=False,
        technical_reference_only=True,
    )


def _output_frame(
    *,
    frame_ref: str,
    backend_ref: str,
    backend_kind: str,
) -> SLAMBackendOutputFrame:
    return SLAMBackendOutputFrame(
        frame_ref=frame_ref,
        timestamp=f"{frame_ref}_ts",
        backend_ref=backend_ref,
        backend_kind=backend_kind,
        pose_fields=("position_delta_m", "rotation_delta_deg", "heading_delta_deg"),
        motion_fields=("motion_state", "speed_band", "stability_level"),
        anchor_fields=("anchor_type", "relative_position_band", "stability_score"),
        local_map_fields=("anchor_refs", "static_structure_refs", "drift_risk"),
        health_fields=("tracking_status", "feature_quality", "imu_quality"),
        drift_fields=("drift_risk", "suspected_drift_source"),
        relocalization_fields=("match_score", "relocalization_status"),
        source_refs=(backend_ref, frame_ref),
    )


def _input_envelope(
    *,
    envelope_ref: str,
    backend_output_ref: str,
    backend_kind: str,
    input_mode: str,
) -> SLAMAdapterInputEnvelope:
    return SLAMAdapterInputEnvelope(
        envelope_ref=envelope_ref,
        backend_output_ref=backend_output_ref,
        backend_kind=backend_kind,
        source_method=f"{backend_kind}_mock_fixture",
        license_status="technical_reference_only",
        runtime_status="planning_only",
        input_mode=input_mode,
        recorded_offline_stub_enabled=False,
        license_gate_required=True,
        adapter_contract_required=True,
        real_backend_connected=False,
        camera_connected=False,
        imu_connected=False,
        ros_connected=False,
    )


def _mapping_rule(
    *,
    mapping_ref: str,
    adapter_ref: str,
    backend_field: str,
    luna_candidate_type: str,
) -> SLAMAdapterMappingRule:
    return SLAMAdapterMappingRule(
        mapping_ref=mapping_ref,
        adapter_ref=adapter_ref,
        backend_field=backend_field,
        luna_candidate_type=luna_candidate_type,
        mapping_status="planned",
        confidence_policy="preserve_backend_confidence_with_downweight",
        degradation_policy="confidence_or_needs_more_observation_only",
        source_refs_required=True,
        candidate_only_enforced=True,
    )


def _adapter(
    *,
    adapter_ref: str,
    backend_kind: str,
    adapter_label: str,
    supported_candidate_types: Tuple[str, ...],
) -> SLAMSpatialEvidenceAdapter:
    return SLAMSpatialEvidenceAdapter(
        adapter_ref=adapter_ref,
        backend_kind=backend_kind,
        adapter_label=adapter_label,
        supported_candidate_types=supported_candidate_types,
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        adapter_contract_ref=GENERIC_SLAM_ADAPTER_CONTRACT_REF,
        license_gate_required=True,
        adapter_contract_required=True,
        real_backend_connected=False,
        runtime_execution_allowed=False,
        provider_activation_allowed=False,
        commercial_runtime_candidate=False,
        technical_reference_only=True,
        camera_connected=False,
        imu_connected=False,
        ros_connected=False,
        direct_action_allowed=False,
        direct_speech_allowed=False,
        direct_fact_write_allowed=False,
    )


def build_slam_spatial_evidence_adapter_matrix_v1() -> Dict[str, Any]:
    specs = (
        (
            "adapter_mock_vio_pose_motion",
            "mock_vio",
            "Mock VIO Pose + Motion Adapter",
            ("mock_vio_backend", "mock_vio_frame_01"),
            "mock_trace",
            ("PoseCandidate", "MotionCandidate"),
            ("position_delta_m", "motion_state"),
        ),
        (
            "adapter_mock_visual_slam_anchor_localmap",
            "mock_visual_slam",
            "Mock Visual SLAM Anchor + LocalMap Adapter",
            ("mock_visual_slam_backend", "mock_visual_slam_frame_01"),
            "synthetic_frame",
            ("SpatialAnchorCandidate", "LocalMapCandidate"),
            ("anchor_type", "anchor_refs"),
        ),
        (
            "adapter_mock_rgbd_localmap_health",
            "mock_rgbd_slam",
            "Mock RGBD LocalMap + Health Adapter",
            ("mock_rgbd_backend", "mock_rgbd_frame_01"),
            "manual_fixture",
            ("LocalMapCandidate", "SLAMHealthCandidate"),
            ("static_structure_refs", "tracking_status"),
        ),
        (
            "adapter_mock_metric_semantic_anchor_graph",
            "mock_metric_semantic_slam",
            "Mock Metric Semantic Anchor + Graph Placeholder Adapter",
            ("mock_metric_semantic_backend", "mock_metric_semantic_frame_01"),
            "mock_trace",
            ("SpatialAnchorCandidate", "SemanticFieldObjectCandidate"),
            ("relative_position_band", "semantic_object_placeholder"),
        ),
        (
            "adapter_mock_scene_graph_field_structure",
            "mock_scene_graph",
            "Mock Scene Graph Field Structure Adapter",
            ("mock_scene_graph_backend", "mock_scene_graph_frame_01"),
            "synthetic_frame",
            ("FieldGraphCandidate", "SpatialAnchorCandidate"),
            ("graph_node_refs", "anchor_type"),
        ),
    )

    mock_backend_outputs: List[MockSLAMBackendOutput] = []
    backend_output_frames: List[SLAMBackendOutputFrame] = []
    input_envelopes: List[SLAMAdapterInputEnvelope] = []
    mapping_rules: List[SLAMAdapterMappingRule] = []
    adapters: List[SLAMSpatialEvidenceAdapter] = []
    output_bundles: List[SLAMAdapterOutputBundle] = []
    health_reports: List[SLAMAdapterHealthReport] = []

    for (
        adapter_ref,
        backend_kind,
        adapter_label,
        backend_frame_refs,
        input_mode,
        candidate_types,
        backend_fields,
    ) in specs:
        backend_ref, frame_ref = backend_frame_refs
        mock_backend_outputs.append(
            _backend_output(
                backend_ref=backend_ref,
                backend_kind=backend_kind,
                backend_label=adapter_label,
                frame_ref=frame_ref,
            )
        )
        backend_output_frames.append(
            _output_frame(
                frame_ref=frame_ref,
                backend_ref=backend_ref,
                backend_kind=backend_kind,
            )
        )
        input_envelopes.append(
            _input_envelope(
                envelope_ref=f"envelope_{adapter_ref}",
                backend_output_ref=backend_ref,
                backend_kind=backend_kind,
                input_mode=input_mode,
            )
        )
        for backend_field, candidate_type in zip(backend_fields, candidate_types):
            mapping_rules.append(
                _mapping_rule(
                    mapping_ref=f"mapping_{adapter_ref}_{candidate_type.lower()}",
                    adapter_ref=adapter_ref,
                    backend_field=backend_field,
                    luna_candidate_type=candidate_type,
                )
            )
        adapters.append(
            _adapter(
                adapter_ref=adapter_ref,
                backend_kind=backend_kind,
                adapter_label=adapter_label,
                supported_candidate_types=candidate_types,
            )
        )

        source_chain = (SOURCE_CHAIN, backend_ref, adapter_ref, frame_ref)
        pose_candidates: Tuple[Dict[str, Any], ...] = ()
        motion_candidates: Tuple[Dict[str, Any], ...] = ()
        spatial_anchor_candidates: Tuple[Dict[str, Any], ...] = ()
        local_map_candidates: Tuple[Dict[str, Any], ...] = ()
        slam_health_candidates: Tuple[Dict[str, Any], ...] = ()
        map_drift_candidates: Tuple[Dict[str, Any], ...] = ()
        relocalization_candidates: Tuple[Dict[str, Any], ...] = ()

        if "PoseCandidate" in candidate_types:
            pose_candidates = (
                _pose_candidate(
                    pose_ref=f"pose_{adapter_ref}",
                    source_method=f"{backend_kind}_mock_fixture",
                    source_refs=source_chain,
                ),
            )
        if "MotionCandidate" in candidate_types:
            motion_candidates = (
                _motion_candidate(
                    motion_ref=f"motion_{adapter_ref}",
                    source_refs=source_chain,
                ),
            )
        if "SpatialAnchorCandidate" in candidate_types:
            spatial_anchor_candidates = (
                _anchor_candidate(
                    anchor_ref=f"anchor_{adapter_ref}",
                    source_refs=source_chain,
                ),
            )
        if "LocalMapCandidate" in candidate_types:
            local_map_candidates = (
                _local_map_candidate(
                    local_map_ref=f"local_map_{adapter_ref}",
                    source_refs=source_chain,
                ),
            )
        if "SLAMHealthCandidate" in candidate_types:
            slam_health_candidates = (
                _health_candidate(
                    health_ref=f"health_{adapter_ref}",
                    source_refs=source_chain,
                ),
            )
        if backend_kind == "mock_vio":
            map_drift_candidates = (
                _drift_candidate(
                    drift_ref=f"drift_{adapter_ref}",
                    drift_risk="high",
                    source_refs=source_chain,
                ),
            )
            relocalization_candidates = (
                _relocalization_candidate(
                    relocalization_ref=f"reloc_{adapter_ref}",
                    source_refs=source_chain,
                ),
            )

        output_types = tuple(
            t for t in candidate_types if t in SUPPORTED_CANDIDATE_TYPES
        ) or ("SpatialAnchorCandidate",)
        output_bundles.append(
            SLAMAdapterOutputBundle(
                bundle_ref=f"bundle_{adapter_ref}",
                adapter_ref=adapter_ref,
                source_chain=source_chain,
                field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
                output_candidate_types=output_types,
                pose_candidates=pose_candidates,
                motion_candidates=motion_candidates,
                spatial_anchor_candidates=spatial_anchor_candidates,
                local_map_candidates=local_map_candidates,
                slam_health_candidates=slam_health_candidates,
                map_drift_candidates=map_drift_candidates,
                relocalization_candidates=relocalization_candidates,
                direct_action_allowed=False,
                direct_speech_allowed=False,
                direct_fact_write_allowed=False,
            )
        )
        health_reports.append(
            SLAMAdapterHealthReport(
                report_ref=f"health_report_{adapter_ref}",
                adapter_ref=adapter_ref,
                adapter_status="planning_ready",
                translation_ok=True,
                mapping_rules_applied=len(backend_fields),
                backend_runtime_health_claimed=False,
                adapter_health_only=True,
            )
        )

    planning_decision = SLAMAdapterPlanningDecision(
        decision_ref="slam_spatial_evidence_adapter_planning_decision_v1",
        planned_adapters=ADAPTER_REFS,
        supported_candidate_types=SUPPORTED_CANDIDATE_TYPES,
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        real_backend_connected=False,
        runtime_execution_allowed=False,
        provider_activation_allowed=False,
        camera_connected=False,
        imu_connected=False,
        ros_connected=False,
        license_gate_required=True,
        adapter_contract_required=True,
        direct_action_allowed=False,
        direct_speech_allowed=False,
        direct_fact_write_allowed=False,
        candidate_only_enforced=True,
        final_decision=FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    )

    return {
        "registry_id": REGISTRY_ID,
        "mock_backend_outputs": [candidate_to_dict(x) for x in mock_backend_outputs],
        "backend_output_frames": [candidate_to_dict(x) for x in backend_output_frames],
        "input_envelopes": [candidate_to_dict(x) for x in input_envelopes],
        "mapping_rules": [candidate_to_dict(x) for x in mapping_rules],
        "adapters": [candidate_to_dict(x) for x in adapters],
        "output_bundles": [candidate_to_dict(x) for x in output_bundles],
        "health_reports": [candidate_to_dict(x) for x in health_reports],
        "planning_decision": candidate_to_dict(planning_decision),
        "translation_chain": [
            "MockSLAMBackendOutput",
            "SLAMBackendOutputFrame",
            "SLAMAdapterInputEnvelope",
            "SLAMAdapterMappingRule",
            "SLAMSpatialEvidenceAdapter",
            "SLAMAdapterOutputBundle",
            FIELD_SYNTHESIS_ENTRYPOINT,
        ],
    }
