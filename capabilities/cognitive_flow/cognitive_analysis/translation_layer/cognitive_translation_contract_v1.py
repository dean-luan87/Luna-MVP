"""Contract descriptor for the A3 Evidence Context Translation Layer Skeleton v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .cognitive_translation_types_v1 import ALLOWED_PRIMITIVE_TYPES_V1


TRANSLATION_LAYER_CONTRACT_ID_V1 = "LUNA-A3-EVIDENCE-CONTEXT-TRANSLATION-CONTRACT-V1"

NEGATIVE_GUARD_IDS_V1 = (
    "Guard-1-evidence-to-fact-forbidden",
    "Guard-2-evidence-to-decision-forbidden",
    "Guard-3-provenance-required",
    "Guard-4-external-model-identity-not-cognitive-entity",
    "Guard-5-context-snapshot-field-state-mutation-forbidden",
)


@dataclass(frozen=True)
class CognitiveTranslationContractV1:
    contract_id: str
    input_fields: Tuple[str, ...]
    output_fields: Tuple[str, ...]
    allowed_primitive_types: Tuple[str, ...]
    forbidden_outcomes: Tuple[str, ...]
    negative_guard_ids: Tuple[str, ...]
    candidate_only: bool
    runtime_authorized: bool


def build_cognitive_translation_contract_v1() -> CognitiveTranslationContractV1:
    """Return the static contract; this function does not translate or call external systems."""
    return CognitiveTranslationContractV1(
        contract_id=TRANSLATION_LAYER_CONTRACT_ID_V1,
        input_fields=(
            "evidence_refs",
            "context_refs",
            "provenance_refs",
            "source_capability_refs",
            "trace_ref",
        ),
        output_fields=(
            "candidate_id",
            "primitive_type",
            "source_refs",
            "context_refs",
            "confidence",
            "uncertainty",
            "provenance",
            "trace_ref",
            "candidate_status",
        ),
        allowed_primitive_types=ALLOWED_PRIMITIVE_TYPES_V1,
        forbidden_outcomes=("fact", "decision", "action", "state", "memory"),
        negative_guard_ids=NEGATIVE_GUARD_IDS_V1,
        candidate_only=True,
        runtime_authorized=False,
    )
