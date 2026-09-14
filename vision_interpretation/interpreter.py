from __future__ import annotations

from typing import List

from .schema import VisionInterpretation, RawTextCandidate, InterpretedMeaning
from .rules import interpret_exit_candidates


def interpret_ocr(
    roi_kind: str,
    raw_text_candidates: List[RawTextCandidate],
) -> VisionInterpretation:
    meanings: List[InterpretedMeaning] = []
    uncertainty = 1.0

    if roi_kind == "exit_area":
        meanings.extend(interpret_exit_candidates(raw_text_candidates))
        if meanings:
            uncertainty = 0.3

    return VisionInterpretation(
        roi_kind=roi_kind,
        raw_text_candidates=raw_text_candidates,
        interpreted_meanings=meanings,
        uncertainty=uncertainty,
        source="ocr_semantic_v0",
    )
