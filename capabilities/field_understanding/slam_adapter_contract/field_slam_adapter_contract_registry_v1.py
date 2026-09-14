# -*- coding: utf-8 -*-
"""Field SLAM Adapter Contract Planning — registry and planning catalog v1."""

from __future__ import annotations

from typing import Dict, FrozenSet, List, Tuple

from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    AdapterPlanningDecision,
    BackendAdmissionCandidate,
    GenericSLAMAdapterContract,
    LicenseGatePolicy,
    RuntimeIsolationPolicy,
    SLAMBackendOutputMapping,
    SpatialEvidenceProviderRegistration,
    candidate_to_dict,
)

REGISTRY_ID = "field_slam_adapter_contract_registry_v1"

BACKEND_ROLES: Tuple[str, ...] = (
    "vio_pose_first",
    "visual_inertial_slam",
    "graph_rgbd_slam",
    "metric_semantic_slam",
    "scene_graph_backend",
    "embodied_scene_graph_qa",
    "custom_luna_backend",
)

INPUT_MODES: Tuple[str, ...] = (
    "monocular_camera",
    "stereo_camera",
    "rgbd_camera",
    "imu",
    "tof",
    "lidar",
    "wheel_odometry",
    "offline_trace",
    "mock",
)

OUTPUT_CANDIDATE_TYPES: Tuple[str, ...] = (
    "PoseCandidate",
    "MotionCandidate",
    "SpatialAnchorCandidate",
    "LocalMapCandidate",
    "SLAMHealthCandidate",
    "MapDriftCandidate",
    "RelocalizationCandidate",
    "SemanticFieldObjectCandidate",
    "FieldGraphCandidate",
    "SemanticMemoryMapCandidate",
)

ADAPTER_STATUSES: Tuple[str, ...] = (
    "planned",
    "dryrun_ready",
    "internal_only",
    "commercial_ready",
    "blocked",
    "disabled",
)

MAPPING_STATUSES: Tuple[str, ...] = (
    "mapped",
    "partially_mapped",
    "not_mapped",
    "observation_only",
    "blocked",
)

LICENSE_TYPES: Tuple[str, ...] = (
    "gpl_3",
    "gpl_v3",
    "bsd",
    "bsd_2_clause",
    "bsd_conditional",
    "mit",
    "apache_2",
    "custom",
    "unknown",
)

LICENSE_REVIEW_STATUSES: Tuple[str, ...] = (
    "unchecked",
    "reviewed_for_internal",
    "reviewed_for_commercial",
    "blocked",
    "needs_legal_review",
)

LICENSE_RISKS: Tuple[str, ...] = (
    "low",
    "medium",
    "high",
    "unknown",
)

ISOLATION_MODES: Tuple[str, ...] = (
    "none",
    "process_boundary",
    "service_boundary",
    "offline_reference_only",
    "mock_only",
    "disabled",
    "unknown",
)

DATA_EXCHANGE_MODES: Tuple[str, ...] = (
    "serialized_candidate",
    "ipc_message",
    "offline_snapshot",
    "mock_only",
    "none",
)

CONTAMINATION_RISKS: Tuple[str, ...] = (
    "low",
    "medium",
    "high",
    "unknown",
)

ADMISSION_STAGES: Tuple[str, ...] = (
    "technical_reference",
    "adapter_planning",
    "dryrun_candidate",
    "internal_runtime_candidate",
    "commercial_runtime_candidate",
    "blocked",
)

PROVIDER_ROLES: Tuple[str, ...] = (
    "pose_motion_provider",
    "local_map_provider",
    "relocalization_provider",
    "semantic_spatial_provider",
    "scene_graph_observation_provider",
    "mock_provider",
)

DISABLE_POLICIES: Tuple[str, ...] = (
    "disable_on_tracking_lost",
    "disable_on_high_drift",
    "disable_on_license_block",
    "disable_on_mapping_failure",
    "manual_disable",
    "always_disabled",
)

CONFIDENCE_POLICIES: Tuple[str, ...] = (
    "pass_through",
    "downweight_on_degraded",
    "reject_below_threshold",
    "unknown",
)

DEGRADATION_POLICIES: Tuple[str, ...] = (
    "disable_on_failure",
    "fallback_to_mock",
    "emit_health_only",
    "downweight_evidence",
    "unknown",
)

FORBIDDEN_ADAPTER_POLICIES: Tuple[str, ...] = (
    "backend_direct_field_write",
    "backend_direct_action",
    "backend_direct_speech",
    "backend_direct_fact_write",
    "backend_bypass_adapter",
    "backend_bypass_license_gate",
    "backend_bypass_field_synthesis",
    "gpl_commercial_runtime_without_gate",
    "adapter_output_without_candidate_only",
)

GPL_LICENSE_TYPES: FrozenSet[str] = frozenset({"gpl_3", "gpl_v3"})

GPL_BLOCKED_USAGE_MODES: Tuple[str, ...] = (
    "closed_source_embedded_runtime",
    "commercial_distribution",
)

OBSERVATION_BACKEND_REFS: FrozenSet[str] = frozenset({"kimera", "hydra", "grapheqa"})

BLOCKED_RUNTIME_BACKEND_REFS: FrozenSet[str] = frozenset(
    {"openvins", "vins_fusion", "orb_slam3", "grapheqa"}
)

TECHNICAL_REFERENCE_BACKEND_REFS: Tuple[str, ...] = (
    "openvins",
    "vins_fusion",
    "orb_slam3",
    "rtab_map",
    "kimera",
    "hydra",
    "grapheqa",
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "backend_roles": BACKEND_ROLES,
    "input_modes": INPUT_MODES,
    "output_candidate_types": OUTPUT_CANDIDATE_TYPES,
    "adapter_statuses": ADAPTER_STATUSES,
    "mapping_statuses": MAPPING_STATUSES,
    "license_types": LICENSE_TYPES,
    "license_review_statuses": LICENSE_REVIEW_STATUSES,
    "license_risks": LICENSE_RISKS,
    "isolation_modes": ISOLATION_MODES,
    "data_exchange_modes": DATA_EXCHANGE_MODES,
    "contamination_risks": CONTAMINATION_RISKS,
    "admission_stages": ADMISSION_STAGES,
    "provider_roles": PROVIDER_ROLES,
    "disable_policies": DISABLE_POLICIES,
    "confidence_policies": CONFIDENCE_POLICIES,
    "degradation_policies": DEGRADATION_POLICIES,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    required_domains = tuple(REGISTRY.keys())
    for domain in required_domains:
        if domain not in REGISTRY or not REGISTRY[domain]:
            issues.append(f"registry_domain_missing:{domain}")
    if len(FORBIDDEN_ADAPTER_POLICIES) < 9:
        issues.append("forbidden_adapter_policies_incomplete")
    if len(OUTPUT_CANDIDATE_TYPES) < 10:
        issues.append("output_candidate_types_incomplete")
    return len(issues) == 0, issues


def build_generic_slam_adapter_contracts_v1() -> Tuple[GenericSLAMAdapterContract, ...]:
    return (
        GenericSLAMAdapterContract(
            adapter_ref="openvins_adapter",
            backend_ref="openvins",
            backend_name="OpenVINS",
            backend_role="vio_pose_first",
            supported_input_modes=("monocular_camera", "imu", "offline_trace", "mock"),
            supported_output_candidates=(
                "PoseCandidate",
                "MotionCandidate",
                "SLAMHealthCandidate",
            ),
            required_output_candidates=("PoseCandidate", "MotionCandidate"),
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
            license_gate_ref="license_gate_openvins",
            runtime_isolation_ref="isolation_openvins",
            adapter_status="planned",
        ),
        GenericSLAMAdapterContract(
            adapter_ref="vins_fusion_adapter",
            backend_ref="vins_fusion",
            backend_name="VINS-Fusion",
            backend_role="vio_pose_first",
            supported_input_modes=(
                "monocular_camera",
                "stereo_camera",
                "imu",
                "offline_trace",
                "mock",
            ),
            supported_output_candidates=(
                "PoseCandidate",
                "MotionCandidate",
                "SLAMHealthCandidate",
                "RelocalizationCandidate",
            ),
            required_output_candidates=("PoseCandidate", "MotionCandidate"),
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
            license_gate_ref="license_gate_vins_fusion",
            runtime_isolation_ref="isolation_vins_fusion",
            adapter_status="planned",
        ),
        GenericSLAMAdapterContract(
            adapter_ref="orb_slam3_adapter",
            backend_ref="orb_slam3",
            backend_name="ORB-SLAM3",
            backend_role="visual_inertial_slam",
            supported_input_modes=(
                "monocular_camera",
                "stereo_camera",
                "imu",
                "offline_trace",
                "mock",
            ),
            supported_output_candidates=(
                "PoseCandidate",
                "SpatialAnchorCandidate",
                "LocalMapCandidate",
                "RelocalizationCandidate",
                "SLAMHealthCandidate",
            ),
            required_output_candidates=("PoseCandidate", "LocalMapCandidate"),
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
            license_gate_ref="license_gate_orb_slam3",
            runtime_isolation_ref="isolation_orb_slam3",
            adapter_status="planned",
        ),
        GenericSLAMAdapterContract(
            adapter_ref="rtab_map_adapter",
            backend_ref="rtab_map",
            backend_name="RTAB-Map",
            backend_role="graph_rgbd_slam",
            supported_input_modes=(
                "rgbd_camera",
                "stereo_camera",
                "lidar",
                "wheel_odometry",
                "offline_trace",
                "mock",
            ),
            supported_output_candidates=(
                "PoseCandidate",
                "SpatialAnchorCandidate",
                "LocalMapCandidate",
                "MapDriftCandidate",
                "RelocalizationCandidate",
            ),
            required_output_candidates=("PoseCandidate", "LocalMapCandidate"),
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
            license_gate_ref="license_gate_rtab_map",
            runtime_isolation_ref="isolation_rtab_map",
            adapter_status="planned",
        ),
        GenericSLAMAdapterContract(
            adapter_ref="kimera_adapter",
            backend_ref="kimera",
            backend_name="Kimera",
            backend_role="metric_semantic_slam",
            supported_input_modes=(
                "stereo_camera",
                "rgbd_camera",
                "imu",
                "offline_trace",
                "mock",
            ),
            supported_output_candidates=(
                "PoseCandidate",
                "SpatialAnchorCandidate",
                "LocalMapCandidate",
                "SemanticFieldObjectCandidate",
                "MapDriftCandidate",
                "RelocalizationCandidate",
            ),
            required_output_candidates=("LocalMapCandidate", "SemanticFieldObjectCandidate"),
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
            license_gate_ref="license_gate_kimera",
            runtime_isolation_ref="isolation_kimera",
            adapter_status="planned",
        ),
        GenericSLAMAdapterContract(
            adapter_ref="hydra_adapter",
            backend_ref="hydra",
            backend_name="Hydra",
            backend_role="scene_graph_backend",
            supported_input_modes=("rgbd_camera", "offline_trace", "mock"),
            supported_output_candidates=(
                "FieldGraphCandidate",
                "SemanticMemoryMapCandidate",
                "SpatialAnchorCandidate",
            ),
            required_output_candidates=("FieldGraphCandidate",),
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
            license_gate_ref="license_gate_hydra",
            runtime_isolation_ref="isolation_hydra",
            adapter_status="planned",
        ),
        GenericSLAMAdapterContract(
            adapter_ref="grapheqa_adapter",
            backend_ref="grapheqa",
            backend_name="GraphEQA",
            backend_role="embodied_scene_graph_qa",
            supported_input_modes=("offline_trace", "mock"),
            supported_output_candidates=(
                "FieldGraphCandidate",
                "SemanticMemoryMapCandidate",
            ),
            required_output_candidates=("FieldGraphCandidate",),
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
            license_gate_ref="license_gate_grapheqa",
            runtime_isolation_ref="isolation_grapheqa",
            adapter_status="planned",
        ),
    )


def build_slam_backend_output_mappings_v1() -> Tuple[SLAMBackendOutputMapping, ...]:
    return (
        SLAMBackendOutputMapping(
            mapping_ref="mapping_openvins_odometry",
            adapter_ref="openvins_adapter",
            backend_ref="openvins",
            backend_output_name="odometry",
            luna_candidate_type="PoseCandidate",
            mapping_status="mapped",
            confidence_policy="pass_through",
            degradation_policy="downweight_evidence",
            source_refs_required=True,
            candidate_only_enforced=True,
        ),
        SLAMBackendOutputMapping(
            mapping_ref="mapping_openvins_tracking_quality",
            adapter_ref="openvins_adapter",
            backend_ref="openvins",
            backend_output_name="tracking_quality",
            luna_candidate_type="SLAMHealthCandidate",
            mapping_status="mapped",
            confidence_policy="downweight_on_degraded",
            degradation_policy="emit_health_only",
            source_refs_required=True,
            candidate_only_enforced=True,
        ),
        SLAMBackendOutputMapping(
            mapping_ref="mapping_vins_fusion_pose_state",
            adapter_ref="vins_fusion_adapter",
            backend_ref="vins_fusion",
            backend_output_name="pose_graph_state",
            luna_candidate_type="PoseCandidate",
            mapping_status="mapped",
            confidence_policy="pass_through",
            degradation_policy="downweight_evidence",
            source_refs_required=True,
            candidate_only_enforced=True,
        ),
        SLAMBackendOutputMapping(
            mapping_ref="mapping_orb_slam3_keyframe_map",
            adapter_ref="orb_slam3_adapter",
            backend_ref="orb_slam3",
            backend_output_name="keyframe_map_point_status",
            luna_candidate_type="LocalMapCandidate",
            mapping_status="mapped",
            confidence_policy="pass_through",
            degradation_policy="downweight_evidence",
            source_refs_required=True,
            candidate_only_enforced=True,
        ),
        SLAMBackendOutputMapping(
            mapping_ref="mapping_orb_slam3_relocalization",
            adapter_ref="orb_slam3_adapter",
            backend_ref="orb_slam3",
            backend_output_name="relocalization_status",
            luna_candidate_type="RelocalizationCandidate",
            mapping_status="mapped",
            confidence_policy="reject_below_threshold",
            degradation_policy="disable_on_failure",
            source_refs_required=True,
            candidate_only_enforced=True,
        ),
        SLAMBackendOutputMapping(
            mapping_ref="mapping_rtab_map_pose_graph",
            adapter_ref="rtab_map_adapter",
            backend_ref="rtab_map",
            backend_output_name="pose_graph",
            luna_candidate_type="PoseCandidate",
            mapping_status="mapped",
            confidence_policy="pass_through",
            degradation_policy="downweight_evidence",
            source_refs_required=True,
            candidate_only_enforced=True,
        ),
        SLAMBackendOutputMapping(
            mapping_ref="mapping_kimera_semantic_mesh",
            adapter_ref="kimera_adapter",
            backend_ref="kimera",
            backend_output_name="semantic_mesh",
            luna_candidate_type="SemanticFieldObjectCandidate",
            mapping_status="partially_mapped",
            confidence_policy="downweight_on_degraded",
            degradation_policy="downweight_evidence",
            source_refs_required=True,
            candidate_only_enforced=True,
        ),
        SLAMBackendOutputMapping(
            mapping_ref="mapping_hydra_scene_graph_node",
            adapter_ref="hydra_adapter",
            backend_ref="hydra",
            backend_output_name="scene_graph_node",
            luna_candidate_type="FieldGraphCandidate",
            mapping_status="observation_only",
            confidence_policy="downweight_on_degraded",
            degradation_policy="emit_health_only",
            source_refs_required=True,
            candidate_only_enforced=True,
        ),
        SLAMBackendOutputMapping(
            mapping_ref="mapping_grapheqa_observation",
            adapter_ref="grapheqa_adapter",
            backend_ref="grapheqa",
            backend_output_name="scene_graph_qa_observation",
            luna_candidate_type="SemanticMemoryMapCandidate",
            mapping_status="observation_only",
            confidence_policy="reject_below_threshold",
            degradation_policy="disable_on_failure",
            source_refs_required=True,
            candidate_only_enforced=True,
        ),
    )


def _gpl_license_gate(
    *,
    backend_ref: str,
    license_type: str,
) -> LicenseGatePolicy:
    return LicenseGatePolicy(
        license_gate_ref=f"license_gate_{backend_ref}",
        backend_ref=backend_ref,
        license_type=license_type,
        license_risk="high",
        commercial_runtime_allowed=False,
        technical_reference_allowed=True,
        required_actions=(
            "keep_off_commercial_runtime_path",
            "require_adapter_contract_before_any_runtime",
            "record_license_gate_review",
        ),
        blocked_usage_modes=GPL_BLOCKED_USAGE_MODES,
        review_status="reviewed_for_internal",
    )


def build_license_gate_policies_v1() -> Tuple[LicenseGatePolicy, ...]:
    return (
        _gpl_license_gate(backend_ref="openvins", license_type="gpl_3"),
        _gpl_license_gate(backend_ref="vins_fusion", license_type="gpl_v3"),
        _gpl_license_gate(backend_ref="orb_slam3", license_type="gpl_v3"),
        LicenseGatePolicy(
            license_gate_ref="license_gate_rtab_map",
            backend_ref="rtab_map",
            license_type="bsd_conditional",
            license_risk="medium",
            commercial_runtime_allowed=False,
            technical_reference_allowed=True,
            required_actions=(
                "verify_component_license_mix",
                "record_license_gate_review",
            ),
            blocked_usage_modes=("commercial_distribution",),
            review_status="needs_legal_review",
        ),
        LicenseGatePolicy(
            license_gate_ref="license_gate_kimera",
            backend_ref="kimera",
            license_type="bsd_2_clause",
            license_risk="low",
            commercial_runtime_allowed=False,
            technical_reference_allowed=True,
            required_actions=("record_license_gate_review",),
            blocked_usage_modes=(),
            review_status="reviewed_for_internal",
        ),
        LicenseGatePolicy(
            license_gate_ref="license_gate_hydra",
            backend_ref="hydra",
            license_type="bsd",
            license_risk="low",
            commercial_runtime_allowed=False,
            technical_reference_allowed=True,
            required_actions=("record_license_gate_review",),
            blocked_usage_modes=(),
            review_status="reviewed_for_internal",
        ),
        LicenseGatePolicy(
            license_gate_ref="license_gate_grapheqa",
            backend_ref="grapheqa",
            license_type="unknown",
            license_risk="high",
            commercial_runtime_allowed=False,
            technical_reference_allowed=True,
            required_actions=(
                "observation_only_usage",
                "record_license_gate_review",
            ),
            blocked_usage_modes=GPL_BLOCKED_USAGE_MODES + ("runtime_admission",),
            review_status="blocked",
        ),
    )


def _gpl_isolation(backend_ref: str) -> RuntimeIsolationPolicy:
    return RuntimeIsolationPolicy(
        isolation_ref=f"isolation_{backend_ref}",
        backend_ref=backend_ref,
        isolation_mode="offline_reference_only",
        data_exchange_mode="offline_snapshot",
        process_boundary_required=False,
        source_code_contamination_risk="high",
        runtime_dependency_risk="high",
        allowed_for_internal_dev=True,
        allowed_for_commercial_runtime=False,
    )


def build_runtime_isolation_policies_v1() -> Tuple[RuntimeIsolationPolicy, ...]:
    return (
        _gpl_isolation("openvins"),
        _gpl_isolation("vins_fusion"),
        _gpl_isolation("orb_slam3"),
        RuntimeIsolationPolicy(
            isolation_ref="isolation_rtab_map",
            backend_ref="rtab_map",
            isolation_mode="offline_reference_only",
            data_exchange_mode="offline_snapshot",
            process_boundary_required=False,
            source_code_contamination_risk="medium",
            runtime_dependency_risk="medium",
            allowed_for_internal_dev=True,
            allowed_for_commercial_runtime=False,
        ),
        RuntimeIsolationPolicy(
            isolation_ref="isolation_kimera",
            backend_ref="kimera",
            isolation_mode="offline_reference_only",
            data_exchange_mode="offline_snapshot",
            process_boundary_required=False,
            source_code_contamination_risk="low",
            runtime_dependency_risk="medium",
            allowed_for_internal_dev=True,
            allowed_for_commercial_runtime=False,
        ),
        RuntimeIsolationPolicy(
            isolation_ref="isolation_hydra",
            backend_ref="hydra",
            isolation_mode="mock_only",
            data_exchange_mode="mock_only",
            process_boundary_required=False,
            source_code_contamination_risk="low",
            runtime_dependency_risk="low",
            allowed_for_internal_dev=True,
            allowed_for_commercial_runtime=False,
        ),
        RuntimeIsolationPolicy(
            isolation_ref="isolation_grapheqa",
            backend_ref="grapheqa",
            isolation_mode="disabled",
            data_exchange_mode="none",
            process_boundary_required=False,
            source_code_contamination_risk="unknown",
            runtime_dependency_risk="high",
            allowed_for_internal_dev=False,
            allowed_for_commercial_runtime=False,
        ),
    )


def build_backend_admission_candidates_v1() -> Tuple[BackendAdmissionCandidate, ...]:
    return (
        BackendAdmissionCandidate(
            admission_ref="admission_openvins",
            backend_ref="openvins",
            adapter_ref="openvins_adapter",
            admission_stage="technical_reference",
            license_gate_passed=True,
            adapter_contract_passed=True,
            output_mapping_passed=True,
            static_validation_passed=True,
            dryrun_required=True,
            runtime_admission_allowed=False,
            blocked_reasons=("gpl_license_blocks_commercial_runtime",),
        ),
        BackendAdmissionCandidate(
            admission_ref="admission_vins_fusion",
            backend_ref="vins_fusion",
            adapter_ref="vins_fusion_adapter",
            admission_stage="technical_reference",
            license_gate_passed=True,
            adapter_contract_passed=True,
            output_mapping_passed=True,
            static_validation_passed=True,
            dryrun_required=True,
            runtime_admission_allowed=False,
            blocked_reasons=("gpl_license_blocks_commercial_runtime",),
        ),
        BackendAdmissionCandidate(
            admission_ref="admission_orb_slam3",
            backend_ref="orb_slam3",
            adapter_ref="orb_slam3_adapter",
            admission_stage="technical_reference",
            license_gate_passed=True,
            adapter_contract_passed=True,
            output_mapping_passed=True,
            static_validation_passed=True,
            dryrun_required=True,
            runtime_admission_allowed=False,
            blocked_reasons=("gpl_license_blocks_commercial_runtime",),
        ),
        BackendAdmissionCandidate(
            admission_ref="admission_rtab_map",
            backend_ref="rtab_map",
            adapter_ref="rtab_map_adapter",
            admission_stage="technical_reference",
            license_gate_passed=False,
            adapter_contract_passed=True,
            output_mapping_passed=True,
            static_validation_passed=True,
            dryrun_required=True,
            runtime_admission_allowed=False,
            blocked_reasons=("license_gate_needs_legal_review",),
        ),
        BackendAdmissionCandidate(
            admission_ref="admission_kimera",
            backend_ref="kimera",
            adapter_ref="kimera_adapter",
            admission_stage="adapter_planning",
            license_gate_passed=True,
            adapter_contract_passed=True,
            output_mapping_passed=True,
            static_validation_passed=True,
            dryrun_required=True,
            runtime_admission_allowed=False,
            blocked_reasons=("observation_backend_no_runtime_admission",),
        ),
        BackendAdmissionCandidate(
            admission_ref="admission_hydra",
            backend_ref="hydra",
            adapter_ref="hydra_adapter",
            admission_stage="adapter_planning",
            license_gate_passed=True,
            adapter_contract_passed=True,
            output_mapping_passed=True,
            static_validation_passed=True,
            dryrun_required=True,
            runtime_admission_allowed=False,
            blocked_reasons=("observation_backend_no_runtime_admission",),
        ),
        BackendAdmissionCandidate(
            admission_ref="admission_grapheqa",
            backend_ref="grapheqa",
            adapter_ref="grapheqa_adapter",
            admission_stage="technical_reference",
            license_gate_passed=False,
            adapter_contract_passed=True,
            output_mapping_passed=True,
            static_validation_passed=True,
            dryrun_required=True,
            runtime_admission_allowed=False,
            blocked_reasons=(
                "observation_only_backend",
                "unknown_license",
                "license_gate_blocked_commercial_runtime",
            ),
        ),
    )


def build_spatial_evidence_provider_registrations_v1() -> Tuple[SpatialEvidenceProviderRegistration, ...]:
    return (
        SpatialEvidenceProviderRegistration(
            provider_ref="provider_openvins",
            backend_ref="openvins",
            adapter_ref="openvins_adapter",
            provider_role="pose_motion_provider",
            enabled_by_default=False,
            fallback_provider_refs=("mock_spatial_provider",),
            supported_candidate_types=(
                "PoseCandidate",
                "MotionCandidate",
                "SLAMHealthCandidate",
            ),
            health_signal_required=True,
            disable_policy="disable_on_tracking_lost",
        ),
        SpatialEvidenceProviderRegistration(
            provider_ref="provider_vins_fusion",
            backend_ref="vins_fusion",
            adapter_ref="vins_fusion_adapter",
            provider_role="pose_motion_provider",
            enabled_by_default=False,
            fallback_provider_refs=("mock_spatial_provider",),
            supported_candidate_types=(
                "PoseCandidate",
                "MotionCandidate",
                "SLAMHealthCandidate",
                "RelocalizationCandidate",
            ),
            health_signal_required=True,
            disable_policy="disable_on_tracking_lost",
        ),
        SpatialEvidenceProviderRegistration(
            provider_ref="provider_orb_slam3",
            backend_ref="orb_slam3",
            adapter_ref="orb_slam3_adapter",
            provider_role="local_map_provider",
            enabled_by_default=False,
            fallback_provider_refs=("mock_spatial_provider",),
            supported_candidate_types=(
                "PoseCandidate",
                "SpatialAnchorCandidate",
                "LocalMapCandidate",
                "RelocalizationCandidate",
                "SLAMHealthCandidate",
            ),
            health_signal_required=True,
            disable_policy="disable_on_high_drift",
        ),
        SpatialEvidenceProviderRegistration(
            provider_ref="provider_rtab_map",
            backend_ref="rtab_map",
            adapter_ref="rtab_map_adapter",
            provider_role="relocalization_provider",
            enabled_by_default=False,
            fallback_provider_refs=("mock_spatial_provider",),
            supported_candidate_types=(
                "PoseCandidate",
                "SpatialAnchorCandidate",
                "LocalMapCandidate",
                "MapDriftCandidate",
                "RelocalizationCandidate",
            ),
            health_signal_required=False,
            disable_policy="disable_on_mapping_failure",
        ),
        SpatialEvidenceProviderRegistration(
            provider_ref="provider_kimera",
            backend_ref="kimera",
            adapter_ref="kimera_adapter",
            provider_role="semantic_spatial_provider",
            enabled_by_default=False,
            fallback_provider_refs=(),
            supported_candidate_types=(
                "PoseCandidate",
                "SpatialAnchorCandidate",
                "LocalMapCandidate",
                "SemanticFieldObjectCandidate",
                "MapDriftCandidate",
                "RelocalizationCandidate",
            ),
            health_signal_required=False,
            disable_policy="always_disabled",
        ),
        SpatialEvidenceProviderRegistration(
            provider_ref="provider_hydra",
            backend_ref="hydra",
            adapter_ref="hydra_adapter",
            provider_role="scene_graph_observation_provider",
            enabled_by_default=False,
            fallback_provider_refs=(),
            supported_candidate_types=(
                "FieldGraphCandidate",
                "SemanticMemoryMapCandidate",
                "SpatialAnchorCandidate",
            ),
            health_signal_required=False,
            disable_policy="always_disabled",
        ),
        SpatialEvidenceProviderRegistration(
            provider_ref="provider_grapheqa",
            backend_ref="grapheqa",
            adapter_ref="grapheqa_adapter",
            provider_role="scene_graph_observation_provider",
            enabled_by_default=False,
            fallback_provider_refs=(),
            supported_candidate_types=(
                "FieldGraphCandidate",
                "SemanticMemoryMapCandidate",
            ),
            health_signal_required=False,
            disable_policy="always_disabled",
        ),
    )


def build_adapter_planning_decision_v1() -> AdapterPlanningDecision:
    adapters = tuple(a.adapter_ref for a in build_generic_slam_adapter_contracts_v1())
    return AdapterPlanningDecision(
        decision_ref="adapter_planning_decision_v1",
        planned_adapters=adapters,
        technical_reference_backends=TECHNICAL_REFERENCE_BACKEND_REFS,
        commercial_runtime_backends=(),
        blocked_runtime_backends=tuple(sorted(BLOCKED_RUNTIME_BACKEND_REFS)),
        observation_backends=tuple(sorted(OBSERVATION_BACKEND_REFS)),
        license_gate_required=True,
        runtime_isolation_required=True,
        output_mapping_required=True,
        dryrun_required_next=True,
        final_decision=FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    )


def build_adapter_planning_matrix_v1() -> Dict[str, object]:
    adapters = build_generic_slam_adapter_contracts_v1()
    mappings = build_slam_backend_output_mappings_v1()
    license_gates = build_license_gate_policies_v1()
    isolations = build_runtime_isolation_policies_v1()
    admissions = build_backend_admission_candidates_v1()
    providers = build_spatial_evidence_provider_registrations_v1()
    decision = build_adapter_planning_decision_v1()
    return {
        "adapter_contracts": [candidate_to_dict(a) for a in adapters],
        "output_mappings": [candidate_to_dict(m) for m in mappings],
        "license_gates": [candidate_to_dict(l) for l in license_gates],
        "runtime_isolations": [candidate_to_dict(i) for i in isolations],
        "backend_admissions": [candidate_to_dict(a) for a in admissions],
        "provider_registrations": [candidate_to_dict(p) for p in providers],
        "decision": candidate_to_dict(decision),
    }
