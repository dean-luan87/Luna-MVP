from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


S3_SCHEMA_VERSION = "a-route-s3-real-vision-evidence-schema-v1"
S3_CONTRACT_VERSION = "a-route-s3-real-vision-evidence-contract-v1"
OWNER = "Field Perception Orchestrator / Vision Provider Integration"
CAPABILITY_KIND = "VISION_DETECTION"

ERROR_CODES = (
    "MISSING_OBSERVATION_DEMAND",
    "INVALID_CAPABILITY_REQUIREMENT",
    "PROVIDER_NOT_ADMITTED",
    "MODEL_NOT_AVAILABLE",
    "INVALID_FRAME_REF",
    "PROVIDER_INVOCATION_FAILED",
    "INVALID_PROVIDER_OUTPUT",
    "EVIDENCE_MAPPING_FAILED",
    "DUPLICATE_INFERENCE_REQUEST",
    "DUPLICATE_EVIDENCE",
    "SESSION_BUDGET_EXHAUSTED",
    "SESSION_REVOKED",
    "TRACE_MISSING",
)


@dataclass(frozen=True)
class VisionProviderAdmissionCandidateV1:
    admission_id: str
    observation_demand_ref: str
    observation_request_ref: str
    capability_requirement_ref: str
    required_capability_kind: str
    provider_session_ref: str
    provider_candidate_ref: str
    model_candidate_ref: str
    model_admission_ref: str
    region_scope_candidate: str
    expected_evidence: Tuple[str, ...]
    bounded: bool
    provider_autonomous_execution: bool
    provider_invocation_authorized: bool
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    mutation_authority: bool = False
    # Canonical cognitive-flow references are supplied by the upstream
    # binding/admission seams.  These fields are references only; FPO does
    # not own their lifecycle or mutate their source records.
    canonical_capability_model_binding_ref: str = ""
    canonical_capability_model_binding_version: str = ""
    canonical_runtime_admission_ref: str = ""
    canonical_runtime_admission_version: str = ""
    canonical_model_provider_binding_ref: str = ""
    canonical_model_provider_binding_version: str = ""
    canonical_invalidation_refs: Tuple[str, ...] = ()
    canonical_chain_validated: bool = False


@dataclass(frozen=True)
class ProviderNativeDetectionRecordV1:
    detection_id: str
    provider_name: str
    provider_version: str
    model_ref: str
    frame_ref: str
    class_id: Optional[int]
    class_label: str
    bbox: Tuple[float, float, float, float]
    confidence: float
    region_ref: str
    frame_dimensions: Tuple[int, int]
    inference_timestamp: int
    provider_trace_ref: str
    provider_output_ref: str


@dataclass(frozen=True)
class VisualDetectionEvidenceCandidateV1:
    evidence_id: str
    provider_ref: str
    model_ref: str
    frame_ref: str
    detection_ref: str
    class_candidate: str
    bbox: Tuple[float, float, float, float]
    confidence: float
    region_ref: str
    temporal_ref: str
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    truth_declared: bool = False
    fact_admitted: bool = False
    field_mutation: bool = False
    current_world_mutation: bool = False
    intent_created: bool = False
    task_created: bool = False
    natural_language_conclusion_ref: str = ""
    schema_version: str = S3_SCHEMA_VERSION
    contract_version: str = S3_CONTRACT_VERSION


@dataclass(frozen=True)
class ObservationGatewayEvidenceHandoffCandidateV1:
    handoff_id: str
    ingress_type: str
    evidence_refs: Tuple[str, ...]
    provider_ref: str
    source_frame_ref: str
    raw_output_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    gateway_admission: bool = False
    semantic_authority: bool = False


@dataclass(frozen=True)
class VisionProviderAdapterResultV1:
    accepted: bool
    invocation_performed: bool
    detector_mode: str
    error_code: str
    provider: str
    model_ref: str
    frame_ref: str
    detections: Tuple[ProviderNativeDetectionRecordV1, ...]
    evidence: Tuple[VisualDetectionEvidenceCandidateV1, ...]
    admission_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    region_scope_candidate: str
    execution_scope_mode: str
    region_scope_enforced: bool
    region_scope_limitation: str
    gateway_handoff: Optional[ObservationGatewayEvidenceHandoffCandidateV1]
    duplicate: bool = False
    candidate_only: bool = True
    provider_autonomous_execution: bool = False
    semantic_interpretation: bool = False
    semantic_compression: bool = False
    provider_semantic_authority: bool = False
    fact_admission: bool = False
    field_mutation: bool = False
    current_world_mutation: bool = False
    ocr_invocation: bool = False
    slam_invocation: bool = False
    vlm_invocation: bool = False
    provider_error_stage: str = ""
    provider_error_detail: str = ""


__all__ = [
    "CAPABILITY_KIND",
    "ERROR_CODES",
    "OWNER",
    "ProviderNativeDetectionRecordV1",
    "ObservationGatewayEvidenceHandoffCandidateV1",
    "S3_CONTRACT_VERSION",
    "S3_SCHEMA_VERSION",
    "VisionProviderAdapterResultV1",
    "VisionProviderAdmissionCandidateV1",
    "VisualDetectionEvidenceCandidateV1",
]
