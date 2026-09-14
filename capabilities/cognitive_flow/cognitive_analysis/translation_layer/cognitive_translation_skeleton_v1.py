"""Non-executing skeleton for the A3 Evidence Context Translation Layer v1."""

from __future__ import annotations

from .cognitive_translation_contract_v1 import NEGATIVE_GUARD_IDS_V1
from .cognitive_translation_types_v1 import (
    CognitivePrimitiveCandidateV1,
    CognitiveTranslationCandidateEnvelopeV1,
    CognitiveTranslationFlagsV1,
    CognitiveTranslationRequestEnvelopeV1,
)


FIXED_TRANSLATION_REQUEST_ID_V1 = "a3-translation-skeleton-fixed-request-v1"


def build_fixed_translation_request_v1() -> CognitiveTranslationRequestEnvelopeV1:
    """Return a fixed reference envelope; no real Evidence, Context, or model output is read."""
    return CognitiveTranslationRequestEnvelopeV1(
        translation_request_id=FIXED_TRANSLATION_REQUEST_ID_V1,
        evidence_refs=("evidence:fixture:translation:ocr-text-candidate:v1",),
        context_refs=("current_cognitive_context:fixture:translation:v1",),
        provenance_refs=("provenance:fixture:translation:v1",),
        source_capability_refs=("capability:fixture:ocr-provider:v1",),
        requested_primitive_type="semantic_candidate",
        trace_ref="trace:a3-translation-skeleton:fixed-fixture:v1",
    )


class CognitiveTranslationSkeletonV1:
    """Creates a not-executed primitive envelope without performing translation."""

    def translate(
        self,
        request: CognitiveTranslationRequestEnvelopeV1,
    ) -> CognitiveTranslationCandidateEnvelopeV1:
        """Return only reference-preserving candidate structure; no external capability is called."""
        candidate = CognitivePrimitiveCandidateV1(
            candidate_id=f"translation-candidate:{request.translation_request_id}",
            primitive_type=request.requested_primitive_type,
            source_refs=request.evidence_refs,
            context_refs=request.context_refs,
            confidence=None,
            uncertainty={
                "status": "not_evaluated",
                "reason_code": "translation_skeleton_not_executed",
            },
            provenance={
                "source_refs": request.provenance_refs,
                "source_capability_refs": request.source_capability_refs,
                "trace_ref": request.trace_ref,
            },
            trace_ref=request.trace_ref,
            candidate_status="translation_not_executed",
        )
        return CognitiveTranslationCandidateEnvelopeV1(
            request_ref=request.translation_request_id,
            cognitive_primitive_candidate=candidate,
            translation_flags=CognitiveTranslationFlagsV1(),
            negative_guard_refs=NEGATIVE_GUARD_IDS_V1,
        )
