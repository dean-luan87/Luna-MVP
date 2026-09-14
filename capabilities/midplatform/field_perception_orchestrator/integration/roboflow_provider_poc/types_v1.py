from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Tuple

from capabilities.midplatform.core.cognitive_state_formation.cognitive_hypothesis_types_v1 import (
    CognitiveHypothesisCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_core_types_v1 import (
    DecisionCandidateV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_active_observation_control_types_v1 import (
    EvidenceSufficiencyCandidateV1,
    NextCycleIngressCandidateV1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_module_types_v1 import (
    OCRRawEvidenceV1,
    OCRStructuredEvidenceEnvelopeV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_evidence_types_v1 import (
    VisualDetectionEvidenceCandidateV1,
)


PROVIDER_REF = "provider:roboflow:vision:poc:v1"
PROVIDER_CONTRACT_REF = "provider-contract:roboflow:vision-evidence:v1"
PROVIDER_CONTRACT_VERSION = "v1"
ADAPTER_REF = "adapter:roboflow:vision-evidence:v1"
WORKFLOW_REF = "workflow:roboflow:lei-luan:custom-workflow:v1"
MODEL_ASSET_REF = "model-asset:rf-detr-small:roboflow-v1"
REAL_MODE_ENV = "ROBOFLOW_REAL_MODE"


@dataclass(frozen=True)
class RoboflowProviderRequestV1:
    request_id: str
    observation_request_ref: str
    capability_requirement_ref: str
    provider_admission_ref: str
    runtime_admission_ref: str
    capability_model_binding_ref: str
    model_provider_binding_ref: str
    provider_ref: str
    provider_contract_ref: str
    workflow_ref: str
    model_refs: Tuple[str, ...]
    image_ref: str
    frame_ref: str
    roi_ref: str
    requested_capabilities: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    grant_refs: Tuple[str, ...] = ()
    constraint_refs: Tuple[str, ...] = ()
    invalidation_refs: Tuple[str, ...] = ()
    real_mode: bool = False
    candidate_only: bool = True
    goal_ref: str = ""
    concern_ref: str = ""
    workflow_output_mapping: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RoboflowNativeResultV1:
    """Adapter-private representation of a Roboflow response."""

    result_id: str
    http_status: int
    # Adapter-private native SDK result. It may be a mapping or the official
    # one-image workflow result sequence; it never crosses into Luna records.
    payload: Any
    provider_ref: str
    workflow_ref: str
    model_refs: Tuple[str, ...]
    request_id: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    actual_provider_response: bool
    workflow_output_mapping: Mapping[str, str] = field(default_factory=dict)
    error_class: str = ""
    error_detail: str = ""
    response_shape_diagnostics: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RoboflowNormalizedProviderResultV1:
    result_id: str
    accepted: bool
    provider_ref: str
    workflow_ref: str
    model_refs: Tuple[str, ...]
    frame_ref: str
    roi_ref: str
    detection_evidence: Tuple[VisualDetectionEvidenceCandidateV1, ...]
    ocr_evidence: Tuple[OCRRawEvidenceV1, ...]
    ocr_envelope: Optional[OCRStructuredEvidenceEnvelopeV1]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    error_class: str = ""
    error_detail: str = ""
    actual_provider_response: bool = False
    raw_roboflow_payload_not_canonical: bool = True
    candidate_only: bool = True
    truth_declared: bool = False
    field_mutation: bool = False
    current_world_mutation: bool = False


@dataclass(frozen=True)
class RoboflowCognitiveLoopResultV1:
    concern_ref: str
    goal_refs: Tuple[str, ...]
    requirement_ref: str
    provider_result: RoboflowNormalizedProviderResultV1
    current_world_candidate: Optional[CurrentWorldCandidateV1]
    hypothesis_candidate: Optional[CognitiveHypothesisCandidateV1]
    sufficiency_candidate: Optional[EvidenceSufficiencyCandidateV1]
    next_observation_candidate: Optional[NextCycleIngressCandidateV1]
    decision_candidate: Optional[DecisionCandidateV1]
    information_gap: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    cognitive_source_owner: str = "A"
    candidate_only: bool = True
    world_truth_declared: bool = False
    field_mutation: bool = False
    task_created: bool = False
    action_executed: bool = False
    provider_autonomous_reobservation: bool = False
    reobservation_policy: Mapping[str, Any] = field(default_factory=dict)
    accepted: bool = True
    failure_class: str = ""
    failure_reason: str = ""


@dataclass(frozen=True)
class RoboflowPoCVerificationRecordV1:
    mode: str
    structural_checks: Mapping[str, bool] = field(default_factory=dict)
    real_provider_checks: Mapping[str, bool] = field(default_factory=dict)
    actual_provider_response: bool = False
    raw_roboflow_payload_not_canonical: bool = True
    provider_invocation: bool = False
    observation_execution: bool = False
    task_execution: bool = False
    action_execution: bool = False
    source_mutation: bool = False
    world_truth_declared: bool = False


__all__ = [
    "ADAPTER_REF",
    "MODEL_ASSET_REF",
    "PROVIDER_CONTRACT_REF",
    "PROVIDER_CONTRACT_VERSION",
    "PROVIDER_REF",
    "RoboflowCognitiveLoopResultV1",
    "RoboflowNativeResultV1",
    "RoboflowNormalizedProviderResultV1",
    "RoboflowPoCVerificationRecordV1",
    "RoboflowProviderRequestV1",
    "WORKFLOW_REF",
]
