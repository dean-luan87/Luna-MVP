# -*- coding: utf-8 -*-
"""Model Admission Governance Standard — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.model_admission_governance.model_admission_governance_types_v1 import (
    DEFAULT_LIFECYCLE_VARIANT,
    DRYRUN_LIFECYCLE_TEMPLATE_REF,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    MODEL_OPERATIONS,
    MODEL_TYPES,
    SHARED_ADMISSION_LIFECYCLE_CHAIN,
    SHARED_ADAPTER_CONTRACT_REF,
    SHARED_RUNTIME_GOVERNANCE_REF,
    SOURCE_CHAIN,
    ModelAdmissionPlanningDecision,
    ModelAdmissionStandard,
    ModelAdapterContractRef,
    ModelCapabilityProfile,
    ModelProviderAdmissionRef,
    ModelRegistryEntry,
    ModelRuntimeGovernanceRef,
    ModelSourceLicenseGate,
    candidate_to_dict,
)

REGISTRY_ID = "model_admission_governance_registry_v1"
STANDARD_REF = "model_admission_governance_standard_v1"

SAMPLE_MODEL_IDS: Tuple[str, ...] = (
    "sample_slam_spatial_evidence_model",
    "sample_supervision_detection_model",
    "sample_viewpoint_search_model",
    "sample_ocr_text_evidence_model",
    "sample_asr_speech_evidence_model",
    "sample_world_model_prediction_model",
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "model_types": MODEL_TYPES,
    "model_operations": MODEL_OPERATIONS,
    "lifecycle_chain": SHARED_ADMISSION_LIFECYCLE_CHAIN,
    "sample_model_ids": SAMPLE_MODEL_IDS,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for domain, values in REGISTRY.items():
        if not values:
            issues.append(f"registry_domain_missing:{domain}")
    if len(SAMPLE_MODEL_IDS) < 6:
        issues.append("sample_model_ids_incomplete")
    if len(SHARED_ADMISSION_LIFECYCLE_CHAIN) < 10:
        issues.append("shared_admission_lifecycle_chain_incomplete")
    return len(issues) == 0, issues


def _sample_spec(
    *,
    model_id: str,
    model_family: str,
    model_role: str,
    domain_id: str,
    model_type: str,
    adapter_profile_ref: str,
    output_candidate_contract_ref: str,
    capability_tags: Tuple[str, ...],
    output_candidate_types: Tuple[str, ...],
    input_modalities: Tuple[str, ...],
) -> Dict[str, Any]:
    source_chain = (SOURCE_CHAIN, model_id, adapter_profile_ref)
    return {
        "model_id": model_id,
        "model_family": model_family,
        "model_role": model_role,
        "domain_id": domain_id,
        "model_type": model_type,
        "adapter_profile_ref": adapter_profile_ref,
        "output_candidate_contract_ref": output_candidate_contract_ref,
        "capability_tags": capability_tags,
        "output_candidate_types": output_candidate_types,
        "input_modalities": input_modalities,
        "source_chain": source_chain,
    }


def build_model_admission_governance_matrix_v1() -> Dict[str, Any]:
    specs = (
        _sample_spec(
            model_id="sample_slam_spatial_evidence_model",
            model_family="slam",
            model_role="spatial_evidence_provider",
            domain_id="spatial_evidence",
            model_type="slam",
            adapter_profile_ref="slam_spatial_evidence_adapter",
            output_candidate_contract_ref="spatial_evidence_candidate_bundle",
            capability_tags=("pose", "motion", "local_map", "health"),
            output_candidate_types=("PoseCandidate", "MotionCandidate", "LocalMapCandidate"),
            input_modalities=("mock_trace", "synthetic_frame"),
        ),
        _sample_spec(
            model_id="sample_supervision_detection_model",
            model_family="supervision",
            model_role="detection_provider",
            domain_id="vision",
            model_type="vision",
            adapter_profile_ref="supervision_detection_adapter",
            output_candidate_contract_ref="vision_detection_candidate_bundle",
            capability_tags=("detection", "tracking"),
            output_candidate_types=("DetectionCandidate", "TrackingCandidate"),
            input_modalities=("synthetic_frame",),
        ),
        _sample_spec(
            model_id="sample_viewpoint_search_model",
            model_family="viewpoint_search",
            model_role="search_provider",
            domain_id="vision",
            model_type="search",
            adapter_profile_ref="viewpoint_search_adapter",
            output_candidate_contract_ref="viewpoint_search_candidate_bundle",
            capability_tags=("viewpoint_search", "retrieval"),
            output_candidate_types=("ViewpointCandidate", "RetrievalCandidate"),
            input_modalities=("manual_fixture",),
        ),
        _sample_spec(
            model_id="sample_ocr_text_evidence_model",
            model_family="ocr",
            model_role="text_evidence_provider",
            domain_id="vision_ocr",
            model_type="ocr",
            adapter_profile_ref="ocr_text_evidence_adapter",
            output_candidate_contract_ref="ocr_evidence_candidate_bundle",
            capability_tags=("ocr", "text_extraction"),
            output_candidate_types=("ocr_result_candidate", "roi_candidate"),
            input_modalities=("synthetic_frame",),
        ),
        _sample_spec(
            model_id="sample_asr_speech_evidence_model",
            model_family="asr",
            model_role="speech_evidence_provider",
            domain_id="asr",
            model_type="asr",
            adapter_profile_ref="asr_speech_evidence_adapter",
            output_candidate_contract_ref="asr_evidence_candidate_bundle",
            capability_tags=("asr", "transcription"),
            output_candidate_types=("asr_transcript_candidate", "speech_segment_candidate"),
            input_modalities=("recorded_offline_stub",),
        ),
        _sample_spec(
            model_id="sample_world_model_prediction_model",
            model_family="world_model",
            model_role="prediction_provider",
            domain_id="shared",
            model_type="world_model",
            adapter_profile_ref="world_model_prediction_adapter",
            output_candidate_contract_ref="world_model_prediction_candidate_bundle",
            capability_tags=("prediction", "scene_understanding"),
            output_candidate_types=("WorldStateCandidate", "PredictionCandidate"),
            input_modalities=("mock_trace",),
        ),
    )

    registry_entries: List[ModelRegistryEntry] = []
    capability_profiles: List[ModelCapabilityProfile] = []
    license_gates: List[ModelSourceLicenseGate] = []
    adapter_contract_refs: List[ModelAdapterContractRef] = []
    provider_admission_refs: List[ModelProviderAdmissionRef] = []
    runtime_governance_refs: List[ModelRuntimeGovernanceRef] = []

    for spec in specs:
        model_id = spec["model_id"]
        registry_entries.append(
            ModelRegistryEntry(
                model_id=model_id,
                model_family=spec["model_family"],
                model_role=spec["model_role"],
                domain_id=spec["domain_id"],
                model_type=spec["model_type"],
                capability_profile_ref=f"capability_profile_{model_id}",
                adapter_contract_ref=SHARED_ADAPTER_CONTRACT_REF,
                provider_admission_ref=f"provider_admission_{model_id}",
                runtime_governance_ref=f"runtime_governance_{model_id}",
                license_gate_ref=f"license_gate_{model_id}",
                source_chain=spec["source_chain"],
                input_contract_ref=f"input_contract_{model_id}",
                output_candidate_contract_ref=spec["output_candidate_contract_ref"],
                domain_profile_ref=f"domain_profile_{spec['domain_id']}",
                lifecycle_variant=DEFAULT_LIFECYCLE_VARIANT,
                candidate_only_default=True,
                runtime_enabled_default=False,
                commercial_runtime_approved=False,
                registry_status="sample_registered",
                lineage_ref=f"lineage_{model_id}_v1",
            )
        )
        capability_profiles.append(
            ModelCapabilityProfile(
                profile_ref=f"capability_profile_{model_id}",
                model_id=model_id,
                model_type=spec["model_type"],
                capability_tags=spec["capability_tags"],
                input_modalities=spec["input_modalities"],
                output_candidate_types=spec["output_candidate_types"],
                latency_class="planning_only",
                compute_class="sample",
                offline_capable=True,
                wearable_fit="planning_tbd",
            )
        )
        license_gates.append(
            ModelSourceLicenseGate(
                license_gate_ref=f"license_gate_{model_id}",
                model_id=model_id,
                license_type="technical_reference_only",
                license_risk="planning_review_required",
                source_provenance_ref=f"source_provenance_{model_id}",
                commercial_runtime_approved=False,
                technical_reference_allowed=True,
                license_gate_required=True,
            )
        )
        adapter_contract_refs.append(
            ModelAdapterContractRef(
                adapter_contract_ref=SHARED_ADAPTER_CONTRACT_REF,
                model_id=model_id,
                adapter_profile_ref=spec["adapter_profile_ref"],
                contract_status="planned",
                adapter_contract_required=True,
                bypass_forbidden=True,
            )
        )
        provider_admission_refs.append(
            ModelProviderAdmissionRef(
                provider_admission_ref=f"provider_admission_{model_id}",
                model_id=model_id,
                provider_ref=f"provider_{model_id}",
                admission_stage="planning_only",
                provider_admission_required=True,
                bypass_forbidden=True,
                runtime_enabled_default=False,
            )
        )
        runtime_governance_refs.append(
            ModelRuntimeGovernanceRef(
                runtime_governance_ref=f"runtime_governance_{model_id}",
                model_id=model_id,
                shared_runtime_governance_ref=SHARED_RUNTIME_GOVERNANCE_REF,
                runtime_governance_required=True,
                bypass_forbidden=True,
                runtime_enabled_default=False,
            )
        )

    admission_standard = ModelAdmissionStandard(
        standard_ref=STANDARD_REF,
        standard_version="v1",
        lifecycle_chain=SHARED_ADMISSION_LIFECYCLE_CHAIN,
        supported_operations=MODEL_OPERATIONS,
        lifecycle_variant_default=DEFAULT_LIFECYCLE_VARIANT,
        dryrun_lifecycle_template_ref=DRYRUN_LIFECYCLE_TEMPLATE_REF,
        shared_runtime_governance_ref=SHARED_RUNTIME_GOVERNANCE_REF,
        domain_profile_allowed_fields=(
            "domain_profile_ref",
            "adapter_profile_ref",
            "candidate_schema_mapping_ref",
            "input_output_mapping_ref",
            "model_capability_profile_ref",
        ),
        domain_specific_lifecycle_forbidden=True,
        candidate_only_default=True,
        runtime_enabled_default=False,
        commercial_runtime_approved_default=False,
        lineage_required_for_update_replace_remove=True,
    )

    planning_decision = ModelAdmissionPlanningDecision(
        decision_ref="model_admission_governance_planning_decision_v1",
        standard_ref=STANDARD_REF,
        registered_model_ids=SAMPLE_MODEL_IDS,
        shared_lifecycle_required=True,
        domain_profile_allowed=True,
        domain_specific_lifecycle_forbidden=True,
        candidate_only_default=True,
        runtime_enabled_default=False,
        commercial_runtime_approved_default=False,
        lineage_required_for_update_replace_remove=True,
        dryrun_lifecycle_template_required=True,
        dryrun_lifecycle_template_ref=DRYRUN_LIFECYCLE_TEMPLATE_REF,
        final_decision=FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    )

    return {
        "registry_id": REGISTRY_ID,
        "model_admission_standard": candidate_to_dict(admission_standard),
        "registry_entries": [candidate_to_dict(entry) for entry in registry_entries],
        "capability_profiles": [candidate_to_dict(profile) for profile in capability_profiles],
        "license_gates": [candidate_to_dict(gate) for gate in license_gates],
        "adapter_contract_refs": [candidate_to_dict(ref) for ref in adapter_contract_refs],
        "provider_admission_refs": [candidate_to_dict(ref) for ref in provider_admission_refs],
        "runtime_governance_refs": [candidate_to_dict(ref) for ref in runtime_governance_refs],
        "planning_decision": candidate_to_dict(planning_decision),
        "shared_lifecycle_chain": list(SHARED_ADMISSION_LIFECYCLE_CHAIN),
        "dryrun_lifecycle_template_ref": DRYRUN_LIFECYCLE_TEMPLATE_REF,
    }
