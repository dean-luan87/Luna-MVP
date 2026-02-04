from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .types import InterpretationKey, SemanticObservation
from .from_vision_interpretation import interpretation_to_semantic_observations


def extract_interpretations(frame: Dict[str, Any]) -> List[Tuple[InterpretationKey, Dict[str, Any]]]:
    """
    Pull interpretations from timeline frame. Returns list of:
    (InterpretationKey, interpretation_dict)
    """
    dbg = frame.get("visual_semantic_debug") or {}
    roi_kind = dbg.get("roi_kind")
    interpretations = dbg.get("interpretations") or []
    out: List[Tuple[InterpretationKey, Dict[str, Any]]] = []
    if not roi_kind:
        return out

    for it in interpretations:
        meaning = (it.get("meaning") or "").strip()
        category = (it.get("category") or "").strip()
        if not meaning or not category:
            continue
        key = InterpretationKey(roi_kind=roi_kind, category=category, meaning=meaning)
        out.append((key, it))
    return out


def extract_semantic_observations(frame: Dict[str, Any]) -> List[SemanticObservation]:
    out: List[SemanticObservation] = []

    vision_interp = frame.get("vision_interpretation")
    if vision_interp:
        try:
            out.extend(
                interpretation_to_semantic_observations(
                    interpretation=_coerce_vision_interpretation(vision_interp)
                )
            )
        except Exception:
            pass

    dbg = frame.get("visual_semantic_debug") or {}
    roi_kind = dbg.get("roi_kind")
    interpretations = dbg.get("interpretations") or []
    if roi_kind:
        for it in interpretations:
            meaning = (it.get("meaning") or "").strip()
            category = (it.get("category") or "").strip()
            if not meaning:
                continue
            out.append(
                SemanticObservation(
                    roi_kind=roi_kind,
                    meaning=meaning,
                    confidence=float(it.get("confidence") or 0.0),
                    ambiguity=list(it.get("ambiguity") or []),
                    uncertainty=0.0,
                    source="visual_semantic_debug",
                    category=category or None,
                )
            )

    return out


def _coerce_vision_interpretation(data: Dict[str, Any]):
    from vision_interpretation.schema import VisionInterpretation, RawTextCandidate, InterpretedMeaning

    raw = [
        RawTextCandidate(
            text=r.get("text", ""),
            confidence=float(r.get("confidence") or 0.0),
            bbox=r.get("bbox"),
        )
        for r in data.get("raw_text_candidates", [])
    ]
    meanings = [
        InterpretedMeaning(
            meaning=m.get("meaning", ""),
            confidence=float(m.get("confidence") or 0.0),
            ambiguity=list(m.get("ambiguity") or []),
            evidence=m.get("evidence") or {},
        )
        for m in data.get("interpreted_meanings", [])
    ]
    return VisionInterpretation(
        roi_kind=data.get("roi_kind", ""),
        raw_text_candidates=raw,
        interpreted_meanings=meanings,
        uncertainty=float(data.get("uncertainty") or 0.0),
        source=data.get("source") or "vision_interpretation",
    )


def extract_validation_signals(frame: Dict[str, Any]) -> Dict[str, Any]:
    """
    v0: we don't have explicit confirmation/contradiction signals yet.
    """
    return {}
