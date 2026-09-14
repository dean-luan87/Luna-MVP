# -*- coding: utf-8 -*-
"""Interface Layer Governance Protocol — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.interface_layer_governance.interface_layer_governance_types_v1 import (
    ACTIVE_INTERNAL_STANDARD_REFS,
    CORE_INTERFACE_GOVERNANCE_RULES,
    FIELD_SYNTHESIS_ENTRYPOINT,
    MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
    INTERFACE_PROFILE_REFS,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    PLANNING_OBJECT_TYPES,
    PLANNED_INTERNAL_STANDARD_REFS,
    PROVIDER_GOVERNANCE_REF,
    PROTOCOL_ID,
    PROTOCOL_NAME,
    SHARED_INGEST_CHAIN,
    SOURCE_CHAIN,
    ExternalBackendInterfaceStandard,
    InterfaceAdapterProfile,
    InterfaceAdmissionPolicy,
    InterfaceLifecycleDecision,
    InternalStandardFormatRef,
    CandidateSchemaMappingRef,
    FINAL_DECISION_BASELINE_READY,
    candidate_to_dict,
)

REGISTRY_ID = "interface_layer_governance_registry_v1"
PROTOCOL_REF = "interface_layer_governance_protocol_v1"

INTERFACE_PROFILE_TO_STANDARD: Dict[str, str] = {
    "spatial_evidence_ingest_interface": "generic_json_spatial_trace",
    "vision_evidence_ingest_interface": "generic_vision_detection_segmentation_trace",
    "ocr_evidence_ingest_interface": "generic_text_evidence_trace",
    "audio_asr_evidence_ingest_interface": "generic_speech_evidence_trace",
    "scene_graph_world_model_interface": "generic_field_graph_trace",
}

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "interface_profile_refs": INTERFACE_PROFILE_REFS,
    "active_internal_standard_refs": ACTIVE_INTERNAL_STANDARD_REFS,
    "planned_internal_standard_refs": PLANNED_INTERNAL_STANDARD_REFS,
    "core_interface_governance_rules": CORE_INTERFACE_GOVERNANCE_RULES,
    "planning_object_types": PLANNING_OBJECT_TYPES,
    "shared_ingest_chain": SHARED_INGEST_CHAIN,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(CORE_INTERFACE_GOVERNANCE_RULES) != 8:
        issues.append("core_interface_governance_rules_count_not_8")
    if len(INTERFACE_PROFILE_REFS) != 5:
        issues.append("interface_profile_refs_count_not_5")
    if len(PLANNING_OBJECT_TYPES) != 6:
        issues.append("planning_object_types_count_not_6")
    if "generic_json_spatial_trace" not in ACTIVE_INTERNAL_STANDARD_REFS:
        issues.append("generic_json_spatial_trace_not_active")
    return len(issues) == 0, issues


def build_interface_layer_governance_baseline_matrix_v1() -> Dict[str, Any]:
    external_standard = ExternalBackendInterfaceStandard(
        standard_ref="external_backend_ingest_interface_standard_v1",
        protocol_id=PROTOCOL_ID,
        protocol_name=PROTOCOL_NAME,
        governance_level="L1 Midplatform System Protocols",
        model_management_protocol_ref=MODEL_MANAGEMENT_PROTOCOL_REF,
        ingest_chain=SHARED_INGEST_CHAIN,
        core_rules=CORE_INTERFACE_GOVERNANCE_RULES,
    )

    adapter_profiles = (
        InterfaceAdapterProfile(
            adapter_profile_ref="slam_spatial_evidence_adapter",
            interface_profile_ref="spatial_evidence_ingest_interface",
            external_format_refs=(
                "generic_tum_trajectory",
                "rtab_map_trajectory_export_subset",
                "rtab_map_odometry_export_subset",
            ),
            internal_standard_format_ref="generic_json_spatial_trace",
            adapter_role="spatial_evidence_interface_adapter",
        ),
        InterfaceAdapterProfile(
            adapter_profile_ref="vision_detection_adapter",
            interface_profile_ref="vision_evidence_ingest_interface",
            external_format_refs=("coco_detection_export", "segmentation_mask_export"),
            internal_standard_format_ref="generic_vision_detection_segmentation_trace",
            adapter_role="vision_evidence_interface_adapter",
        ),
        InterfaceAdapterProfile(
            adapter_profile_ref="ocr_text_evidence_adapter",
            interface_profile_ref="ocr_evidence_ingest_interface",
            external_format_refs=("ocr_engine_json_export",),
            internal_standard_format_ref="generic_text_evidence_trace",
            adapter_role="ocr_evidence_interface_adapter",
        ),
        InterfaceAdapterProfile(
            adapter_profile_ref="asr_speech_evidence_adapter",
            interface_profile_ref="audio_asr_evidence_ingest_interface",
            external_format_refs=("asr_transcript_json_export",),
            internal_standard_format_ref="generic_speech_evidence_trace",
            adapter_role="speech_evidence_interface_adapter",
        ),
        InterfaceAdapterProfile(
            adapter_profile_ref="scene_graph_field_adapter",
            interface_profile_ref="scene_graph_world_model_interface",
            external_format_refs=("hydra_scene_graph_export", "kimera_semantic_mesh_export"),
            internal_standard_format_ref="generic_field_graph_trace",
            adapter_role="field_graph_interface_adapter",
        ),
    )

    internal_standards = (
        InternalStandardFormatRef(
            format_ref="generic_json_spatial_trace",
            interface_profile_ref="spatial_evidence_ingest_interface",
            format_status="active_sealed_baseline",
            parser_ref="generic_json_spatial_trace_parser_v1",
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        ),
        InternalStandardFormatRef(
            format_ref="generic_vision_detection_segmentation_trace",
            interface_profile_ref="vision_evidence_ingest_interface",
            format_status="planned",
            parser_ref="generic_vision_trace_parser_v1_planned",
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        ),
        InternalStandardFormatRef(
            format_ref="generic_text_evidence_trace",
            interface_profile_ref="ocr_evidence_ingest_interface",
            format_status="planned",
            parser_ref="generic_text_evidence_trace_parser_v1_planned",
            field_synthesis_entrypoint=MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
        ),
        InternalStandardFormatRef(
            format_ref="generic_speech_evidence_trace",
            interface_profile_ref="audio_asr_evidence_ingest_interface",
            format_status="planned",
            parser_ref="generic_speech_evidence_trace_parser_v1_planned",
            field_synthesis_entrypoint=MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
        ),
        InternalStandardFormatRef(
            format_ref="generic_field_graph_trace",
            interface_profile_ref="scene_graph_world_model_interface",
            format_status="planned",
            parser_ref="generic_field_graph_trace_parser_v1_planned",
            field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        ),
    )

    candidate_mappings = (
        CandidateSchemaMappingRef(
            mapping_ref="spatial_evidence_candidate_mapping_v1",
            internal_standard_format_ref="generic_json_spatial_trace",
            candidate_schema_ref="spatial_evidence_candidate_bundle",
            domain_profile_ref="spatial_evidence",
            synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        ),
        CandidateSchemaMappingRef(
            mapping_ref="vision_evidence_candidate_mapping_v1_planned",
            internal_standard_format_ref="generic_vision_detection_segmentation_trace",
            candidate_schema_ref="vision_evidence_candidate_bundle",
            domain_profile_ref="vision_evidence",
            synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        ),
        CandidateSchemaMappingRef(
            mapping_ref="text_evidence_candidate_mapping_v1_planned",
            internal_standard_format_ref="generic_text_evidence_trace",
            candidate_schema_ref="text_evidence_candidate_bundle",
            domain_profile_ref="text_evidence",
            synthesis_entrypoint=MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
        ),
        CandidateSchemaMappingRef(
            mapping_ref="speech_evidence_candidate_mapping_v1_planned",
            internal_standard_format_ref="generic_speech_evidence_trace",
            candidate_schema_ref="speech_evidence_candidate_bundle",
            domain_profile_ref="speech_evidence",
            synthesis_entrypoint=MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
        ),
        CandidateSchemaMappingRef(
            mapping_ref="field_graph_candidate_mapping_v1_planned",
            internal_standard_format_ref="generic_field_graph_trace",
            candidate_schema_ref="field_graph_candidate_bundle",
            domain_profile_ref="field_graph",
            synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        ),
    )

    admission_policy = InterfaceAdmissionPolicy(
        policy_ref="interface_admission_policy_v1",
        model_management_protocol_ref=MODEL_MANAGEMENT_PROTOCOL_REF,
        provider_governance_ref=PROVIDER_GOVERNANCE_REF,
        direct_main_chain_write_forbidden=True,
        private_ingest_entrypoint_forbidden=True,
        runtime_activation_default_false=True,
        commercial_runtime_approval_default_false=True,
        version_lineage_required=True,
    )

    lifecycle_decision = InterfaceLifecycleDecision(
        decision_ref="interface_layer_governance_lifecycle_decision_v1",
        protocol_ref=PROTOCOL_REF,
        active_internal_standard_refs=ACTIVE_INTERNAL_STANDARD_REFS,
        planned_internal_standard_refs=PLANNED_INTERNAL_STANDARD_REFS,
        sealed_spatial_evidence_standard="generic_json_spatial_trace",
        architecture_principle_locked=True,
        baseline_planning_only=True,
        no_runtime_activation=True,
        final_decision=FINAL_DECISION_BASELINE_READY,
    )

    return {
        "registry_id": REGISTRY_ID,
        "protocol_ref": PROTOCOL_REF,
        "source_chain": SOURCE_CHAIN,
        "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
        "interface_profile_to_standard": dict(INTERFACE_PROFILE_TO_STANDARD),
        "external_backend_interface_standard": candidate_to_dict(external_standard),
        "interface_adapter_profiles": [candidate_to_dict(x) for x in adapter_profiles],
        "internal_standard_format_refs": [candidate_to_dict(x) for x in internal_standards],
        "candidate_schema_mapping_refs": [candidate_to_dict(x) for x in candidate_mappings],
        "interface_admission_policy": candidate_to_dict(admission_policy),
        "interface_lifecycle_decision": candidate_to_dict(lifecycle_decision),
    }
