"""Controlled B1 evidence references and case metadata.

The real fixture is an already-produced YOLO11n evidence reference.  It does
not load a frame or invoke a provider.  Structured detection fields remain
available through the source object while the Gateway contract carries only
canonical evidence references downstream.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_evidence_types_v1 import (
    ObservationGatewayEvidenceHandoffCandidateV1,
    VisualDetectionEvidenceCandidateV1,
)


CASE_IDS = tuple(f"B1-{index:02d}" for index in range(1, 24))


def build_visual_evidence_reference_v1(
    case_id: str,
    *,
    synthetic: bool = False,
    contradiction: bool = False,
) -> VisualDetectionEvidenceCandidateV1:
    provider_ref = "provider:synthetic-vision" if synthetic else "yolo_candidate_adapter"
    model_ref = "model:synthetic-vision-v1" if synthetic else "model-asset:yolo11n:weights-v1"
    prefix = "synthetic" if synthetic else "yolo11n"
    return VisualDetectionEvidenceCandidateV1(
        evidence_id=f"visual-evidence:{prefix}:{case_id}:001",
        provider_ref=provider_ref,
        model_ref=model_ref,
        frame_ref=f"{prefix}-frame:{case_id}",
        detection_ref=f"{prefix}-detection:{case_id}:001",
        class_candidate="person",
        bbox=(20.0, 30.0, 180.0, 300.0),
        confidence=0.91,
        region_ref="region:authorized-single-frame",
        temporal_ref=f"frame-temporal:{case_id}",
        uncertainty_refs=(f"uncertainty:{case_id}",),
        contradiction_refs=(f"contradiction:{case_id}",) if contradiction else (),
        trace_ref=f"trace:{prefix}:evidence:{case_id}",
        provenance_refs=(
            f"provenance:model-manager:{case_id}",
            f"provenance:provider:{case_id}",
            f"provenance:frame:{case_id}",
        ),
        candidate_only=True,
        truth_declared=False,
        fact_admitted=False,
        field_mutation=False,
        current_world_mutation=False,
        intent_created=False,
        task_created=False,
        natural_language_conclusion_ref="",
    )


def build_gateway_handoff_v1(
    evidence: VisualDetectionEvidenceCandidateV1,
    *,
    synthetic: bool = False,
) -> ObservationGatewayEvidenceHandoffCandidateV1:
    prefix = "synthetic" if synthetic else "yolo11n"
    return ObservationGatewayEvidenceHandoffCandidateV1(
        handoff_id=f"gateway-handoff:{prefix}:{evidence.evidence_id}",
        ingress_type="VISION",
        evidence_refs=(evidence.evidence_id,),
        provider_ref=evidence.provider_ref,
        source_frame_ref=evidence.frame_ref,
        raw_output_refs=(evidence.detection_ref,),
        trace_ref=f"trace:{prefix}:gateway:{evidence.evidence_id}",
        provenance_refs=evidence.provenance_refs,
        candidate_only=True,
        gateway_admission=False,
        semantic_authority=False,
    )


def build_b1_cases_v1() -> Tuple[Dict[str, Any], ...]:
    titles = {
        "B1-01": "real visual evidence accepted by Gateway",
        "B1-02": "Gateway admission does not grant truth",
        "B1-03": "structured detection refs preserved",
        "B1-04": "Context handoff created",
        "B1-05": "Context Foundation candidate created",
        "B1-06": "CurrentWorldCandidate created",
        "B1-07": "Current World is candidate-only",
        "B1-08": "reverse provenance trace complete",
        "B1-09": "temporal refs preserved",
        "B1-10": "uncertainty refs preserved",
        "B1-11": "contradiction refs preserved",
        "B1-12": "no automatic Field Event",
        "B1-13": "explicit field-relevant candidate exposes Field Event handoff",
        "B1-14": "Reducer eligibility is not mutation",
        "B1-15": "no direct Field State mutation",
        "B1-16": "no direct Current World mutation",
        "B1-17": "no Intent Decision Task mutation",
        "B1-18": "no semantic compression",
        "B1-19": "no OCR SLAM VLM",
        "B1-20": "duplicate or replayed evidence is bounded",
        "B1-21": "synthetic Context World regression preserved",
        "B1-22": "real versus synthetic governance compatibility",
        "B1-23": "real YOLO evidence end-to-end Gateway to Current World candidate",
    }
    return tuple(
        {
            "case_id": case_id,
            "title": titles[case_id],
            "field_relevant": case_id in {"B1-13", "B1-14"},
            "field_event_admission": case_id in {"B1-13", "B1-14"},
            "contradiction": case_id == "B1-11",
            "duplicate": case_id == "B1-20",
            # Controlled admission metadata for the explicit field-event
            # cases. These are test input timestamps, not provider-derived
            # claims about the source frame.
            "occurred_at": "2026-08-13T00:00:00Z",
            "observed_at": "2026-08-13T00:00:00Z",
            "received_at": "2026-08-13T00:00:00Z",
            "valid_from": "2026-08-13T00:00:00Z",
        }
        for case_id in CASE_IDS
    )


__all__ = [
    "CASE_IDS",
    "build_b1_cases_v1",
    "build_gateway_handoff_v1",
    "build_visual_evidence_reference_v1",
]
