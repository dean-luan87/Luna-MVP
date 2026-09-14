from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Tuple


def build_ocr_manager_enhancement_candidates_v1(
    raw_evidence: Sequence[Mapping[str, Any]],
) -> Tuple[Dict[str, Any], ...]:
    candidates = []
    for index, item in enumerate(raw_evidence):
        raw_text = str(item.get("raw_text") or "")
        evidence_id = str(item.get("evidence_id") or f"raw_{index}")
        if raw_text and raw_text[-1].isalnum():
            candidates.append(
                {
                    "enhancement_id": f"enh_punctuation_{index}",
                    "enhancement_type": "punctuation_correction_candidate",
                    "original_text_ref": evidence_id,
                    "candidate_text": f"{raw_text}.",
                    "confidence": 0.6,
                    "enhancement_is_evidence_candidate": True,
                    "interpretation_authority": False,
                    "fact_promotion_allowed": False,
                }
            )
        if any("a" <= ch.lower() <= "z" for ch in raw_text) and any(
            "\u4e00" <= ch <= "\u9fff" for ch in raw_text
        ):
            candidates.append(
                {
                    "enhancement_id": f"enh_mixed_lang_{index}",
                    "enhancement_type": "mixed_language_candidate",
                    "original_text_ref": evidence_id,
                    "candidate_text": raw_text,
                    "confidence": 0.7,
                    "enhancement_is_evidence_candidate": True,
                    "interpretation_authority": False,
                    "fact_promotion_allowed": False,
                }
            )
        if "?" in raw_text or "*" in raw_text:
            candidates.append(
                {
                    "enhancement_id": f"enh_uncertain_char_{index}",
                    "enhancement_type": "uncertain_character_candidate",
                    "original_text_ref": evidence_id,
                    "candidate_text": raw_text.replace("*", "x").replace("?", "?"),
                    "confidence": 0.4,
                    "enhancement_is_evidence_candidate": True,
                    "interpretation_authority": False,
                    "fact_promotion_allowed": False,
                }
            )
    return tuple(candidates)
