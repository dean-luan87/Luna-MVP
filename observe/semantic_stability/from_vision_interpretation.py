from __future__ import annotations

from typing import List

from observe.semantic_stability.types import SemanticObservation
from vision_interpretation.schema import VisionInterpretation


def interpretation_to_semantic_observations(
    interpretation: VisionInterpretation,
) -> List[SemanticObservation]:
    observations: List[SemanticObservation] = []

    for m in interpretation.interpreted_meanings:
        observations.append(
            SemanticObservation(
                roi_kind=interpretation.roi_kind,
                meaning=m.meaning,
                confidence=m.confidence,
                ambiguity=m.ambiguity,
                uncertainty=interpretation.uncertainty,
                source="vision_interpretation",
            )
        )

    return observations
