from __future__ import annotations

from typing import List

from .schema import RawTextCandidate, InterpretedMeaning


def interpret_exit_candidates(
    raw_text_candidates: List[RawTextCandidate],
) -> List[InterpretedMeaning]:
    meanings: List[InterpretedMeaning] = []
    for c in raw_text_candidates:
        if "exit" in c.text.lower():
            meanings.append(
                InterpretedMeaning(
                    meaning="exit_sign",
                    confidence=0.7,
                    ambiguity=["fire_exit", "shop_exit"],
                    evidence={"rule": "contains_exit"},
                )
            )
    return meanings
