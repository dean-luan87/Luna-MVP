"""Real controlled visual-evidence admission at the existing Gateway boundary.

This adapter consumes already-produced YOLO evidence. It never invokes a
provider and never grants semantic authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    ObservationCandidateV1,
    ObservationIngressCandidateV1,
    PerceptionEvidenceV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_static_validators_v1 import (
    validate_evidence,
    validate_ingress,
    validate_observation,
    validate_trace,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_trace_types_v1 import (
    ObservationGatewayTraceV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_evidence_types_v1 import (
    ObservationGatewayEvidenceHandoffCandidateV1,
    VisualDetectionEvidenceCandidateV1,
)


REAL_CONTROLLED_EVIDENCE = "REAL_CONTROLLED_EVIDENCE"
SYNTHETIC_EVIDENCE = "SYNTHETIC_EVIDENCE"


@dataclass(frozen=True)
class RealControlledVisualEvidenceAdmissionV1:
    mode: str
    gateway_admission: bool
    admission_state: str
    ingress: ObservationIngressCandidateV1 | None
    evidence: Tuple[PerceptionEvidenceV1, ...]
    observation: ObservationCandidateV1 | None
    source_visual_evidence: Tuple[VisualDetectionEvidenceCandidateV1, ...]
    handoff: ObservationGatewayEvidenceHandoffCandidateV1 | None
    trace: ObservationGatewayTraceV1
    errors: Tuple[str, ...] = ()
    candidate_only: bool = True
    truth_declared: bool = False
    fact_admitted: bool = False
    semantic_authority: bool = False
    idempotency_key: str = ""


def _empty_trace(key: str) -> ObservationGatewayTraceV1:
    return ObservationGatewayTraceV1(
        root_trace_id=f"root-trace:{key}",
        a_route_ingress_ref="not-formed",
        observation_trace_ref="not-formed",
        evidence_trace_refs=(),
        provider_trace_refs=(),
        source_input_refs=(),
        provenance_refs=(),
        correction_lineage=(),
        contradiction_lineage=(),
        temporal_lineage=(),
        reverse_lookup_path=(),
        authority_granted=False,
        candidate_only=True,
    )


def _canonical_evidence(
    source: VisualDetectionEvidenceCandidateV1,
    *,
    sensitivity: str,
) -> PerceptionEvidenceV1:
    return PerceptionEvidenceV1(
        evidence_id=source.evidence_id,
        evidence_type="visual_detection_evidence",
        source_provider=source.provider_ref,
        source_capability="VISION_DETECTION",
        source_model_ref=source.model_ref,
        source_region_ref=source.region_ref,
        source_temporal_ref=source.temporal_ref,
        raw_output_ref=source.detection_ref,
        confidence_candidate=source.confidence,
        quality_candidate=source.confidence,
        uncertainty_refs=source.uncertainty_refs,
        contradiction_refs=source.contradiction_refs,
        correction_refs=(),
        trace_ref=source.trace_ref,
        provenance_refs=source.provenance_refs,
        sensitivity=sensitivity,
        candidate_only=True,
        fact_declared=False,
    )


def admit_real_visual_evidence_v1(
    handoff: ObservationGatewayEvidenceHandoffCandidateV1,
    visual_evidence: Iterable[VisualDetectionEvidenceCandidateV1],
    *,
    mode: str = REAL_CONTROLLED_EVIDENCE,
    sensitivity: str = "SENSITIVE",
    observed_at_ref: Optional[str] = None,
    valid_from_ref: Optional[str] = None,
    seen_handoff_ids: Iterable[str] = (),
) -> RealControlledVisualEvidenceAdmissionV1:
    """Validate and admit an explicit evidence handoff at Gateway level."""

    source = tuple(visual_evidence)
    key = handoff.handoff_id if handoff is not None else "missing"
    if mode not in {REAL_CONTROLLED_EVIDENCE, SYNTHETIC_EVIDENCE}:
        return RealControlledVisualEvidenceAdmissionV1(mode=mode, gateway_admission=False, admission_state="REJECTED", ingress=None, evidence=(), observation=None, source_visual_evidence=source, handoff=handoff, trace=_empty_trace(key), errors=("INVALID_EVIDENCE_MODE",), idempotency_key=key)
    if handoff is None:
        return RealControlledVisualEvidenceAdmissionV1(mode=mode, gateway_admission=False, admission_state="REJECTED", ingress=None, evidence=(), observation=None, source_visual_evidence=(), handoff=None, trace=_empty_trace(key), errors=("MISSING_HANDOFF",), idempotency_key=key)
    if handoff.handoff_id in frozenset(seen_handoff_ids):
        return RealControlledVisualEvidenceAdmissionV1(mode=mode, gateway_admission=False, admission_state="REJECTED", ingress=None, evidence=(), observation=None, source_visual_evidence=source, handoff=handoff, trace=_empty_trace(key), errors=("DUPLICATE_REAL_EVIDENCE",), idempotency_key=key)
    if handoff.ingress_type != "VISION" or handoff.gateway_admission or handoff.semantic_authority or not handoff.candidate_only:
        return RealControlledVisualEvidenceAdmissionV1(mode=mode, gateway_admission=False, admission_state="REJECTED", ingress=None, evidence=(), observation=None, source_visual_evidence=source, handoff=handoff, trace=_empty_trace(key), errors=("INVALID_HANDOFF_BOUNDARY",), idempotency_key=key)
    by_id = {item.evidence_id: item for item in source}
    if not source or tuple(handoff.evidence_refs) != tuple(by_id) or any(
        item.candidate_only is not True
        or item.truth_declared
        or item.fact_admitted
        or not item.trace_ref
        or not item.provenance_refs
        for item in source
    ):
        return RealControlledVisualEvidenceAdmissionV1(mode=mode, gateway_admission=False, admission_state="REJECTED", ingress=None, evidence=(), observation=None, source_visual_evidence=source, handoff=handoff, trace=_empty_trace(key), errors=("HANDOFF_EVIDENCE_MISMATCH",), idempotency_key=key)

    canonical = tuple(_canonical_evidence(by_id[evidence_id], sensitivity=sensitivity) for evidence_id in handoff.evidence_refs)
    temporal = tuple(item.source_temporal_ref for item in canonical)
    source_temporal_ref = next(iter(temporal), "")
    observed = observed_at_ref or source_temporal_ref
    valid_from = valid_from_ref or observed
    ingress = ObservationIngressCandidateV1(
        ingress_id=f"gateway-ingress:{handoff.handoff_id}",
        ingress_type="VISION",
        provider_ref=handoff.provider_ref,
        source_ref=handoff.source_frame_ref,
        payload_ref=handoff.handoff_id,
        temporal_ref=source_temporal_ref,
        observed_at=observed,
        valid_from_candidate=valid_from,
        valid_until_candidate="",
        confidence_candidate=max(item.confidence_candidate for item in canonical),
        quality_candidate=max(item.quality_candidate for item in canonical),
        sensitivity=sensitivity,
        trace_ref=handoff.trace_ref,
        provenance_refs=tuple(
            dict.fromkeys(
                (
                    *handoff.provenance_refs,
                    *(ref for item in canonical for ref in item.provenance_refs),
                )
            )
        ),
        candidate_only=True,
    )
    observation = ObservationCandidateV1(
        observation_id=f"observation:{handoff.handoff_id}",
        observation_type="vision_observation_candidate",
        evidence_refs=tuple(item.evidence_id for item in canonical),
        subject_candidate=None,
        attribute_candidate=None,
        relation_candidate=None,
        spatial_refs=tuple(dict.fromkeys(item.source_region_ref for item in canonical if item.source_region_ref)),
        temporal_refs=tuple(dict.fromkeys(temporal)),
        uncertainty_refs=tuple(dict.fromkeys(ref for item in canonical for ref in item.uncertainty_refs)),
        contradiction_refs=tuple(dict.fromkeys(ref for item in canonical for ref in item.contradiction_refs)),
        correction_refs=(),
        admission_state="ADMITTED_OBSERVATION",
        routing_targets=("Context", "A Route Orchestration"),
        trace_ref=f"{handoff.trace_ref}:observation",
        provenance_refs=tuple(
            dict.fromkeys(
                (
                    *handoff.provenance_refs,
                    *(ref for item in canonical for ref in item.provenance_refs),
                )
            )
        ),
        sensitivity=sensitivity,
        candidate_only=True,
        truth_declared=False,
    )
    trace = ObservationGatewayTraceV1(
        root_trace_id=f"root-trace:{handoff.handoff_id}",
        a_route_ingress_ref=handoff.handoff_id,
        observation_trace_ref=observation.trace_ref,
        evidence_trace_refs=tuple(item.trace_ref for item in canonical),
        provider_trace_refs=tuple(dict.fromkeys(item.source_provider for item in canonical)),
        source_input_refs=tuple(
            dict.fromkeys(
                (
                    handoff.source_frame_ref,
                    handoff.handoff_id,
                    *handoff.raw_output_refs,
                    *(item.source_model_ref for item in canonical if item.source_model_ref),
                )
            )
        ),
        provenance_refs=tuple(
            dict.fromkeys(
                (
                    *handoff.provenance_refs,
                    *(ref for item in canonical for ref in item.provenance_refs),
                )
            )
        ),
        correction_lineage=(),
        contradiction_lineage=tuple(dict.fromkeys(ref for item in canonical for ref in item.contradiction_refs)),
        # Keep the canonical Gateway slot order used by ObservationGatewayEngineV1:
        # source temporal reference, observed-at reference, valid-from candidate.
        # Values may be equal when the source only supplies one temporal ref;
        # the semantic slots must not be collapsed by deduplication.
        temporal_lineage=(source_temporal_ref, observed, valid_from),
        reverse_lookup_path=(
            observation.observation_id,
            *observation.evidence_refs,
            *trace_refs(canonical),
            handoff.source_frame_ref,
            *(item.source_model_ref for item in canonical if item.source_model_ref),
            handoff.provider_ref,
        ),
        authority_granted=False,
        candidate_only=True,
    )
    errors = []
    if not validate_ingress(ingress):
        errors.append("INVALID_GATEWAY_INGRESS")
    if not all(validate_evidence(item) for item in canonical):
        errors.append("INVALID_GATEWAY_EVIDENCE")
    if not validate_observation(observation):
        errors.append("INVALID_GATEWAY_OBSERVATION")
    if not validate_trace(trace):
        errors.append("INVALID_GATEWAY_TRACE")
    accepted = not errors
    return RealControlledVisualEvidenceAdmissionV1(
        mode=mode,
        gateway_admission=accepted,
        admission_state="ADMITTED_OBSERVATION" if accepted else "REJECTED",
        ingress=ingress if accepted else None,
        evidence=canonical if accepted else (),
        observation=observation if accepted else None,
        source_visual_evidence=source,
        handoff=handoff,
        trace=trace,
        errors=tuple(errors),
        idempotency_key=key,
    )


def trace_refs(evidence: Iterable[PerceptionEvidenceV1]) -> Tuple[str, ...]:
    return tuple(item.trace_ref for item in evidence)


__all__ = [
    "REAL_CONTROLLED_EVIDENCE",
    "SYNTHETIC_EVIDENCE",
    "RealControlledVisualEvidenceAdmissionV1",
    "admit_real_visual_evidence_v1",
]
