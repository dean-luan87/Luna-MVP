# -*- coding: utf-8 -*-
"""Text normalization candidate builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def build_text_normalization_candidates(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    observations: List[Dict[str, Any]],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Build TextNormalizationCandidate from cached correction results. No LLM."""
    overrides = case_overrides or {}
    if raw_output.get("_blocked"):
        return []

    results: List[Dict[str, Any]] = []
    raw_norm = raw_output.get("raw_normalization_payload") or {}
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")

    for obs in observations:
        original = raw_norm.get("raw_text") or obs.get("text", "")
        normalized = raw_norm.get("normalized_text") or obs.get("normalized_text")
        if not normalized and not overrides.get("force_normalization"):
            continue
        if overrides.get("force_normalization") and not normalized:
            normalized = original.replace(" ", "")

        ambiguity = overrides.get("ambiguity_status", "clear")
        if overrides.get("ambiguous"):
            ambiguity = "ambiguous"
        correction_conf = "low" if execution_mode in ("cached_output", "adapter_stub") else "medium"
        if ambiguity == "ambiguous":
            correction_conf = "low"

        norm_id = f"tnc_{uuid.uuid4().hex[:12]}"
        results.append({
            "text_normalization_candidate_id": norm_id,
            "source_text_observation_ref": obs.get("text_observation_candidate_id"),
            "original_text": original,
            "normalized_text": normalized or original,
            "normalization_method": overrides.get("normalization_method", "cached_correction"),
            "correction_confidence": correction_conf,
            "ambiguity_status": ambiguity,
            "alternatives": overrides.get("alternatives", []),
            "warning_codes": ["no_llm_text_correction"] + list(obs.get("warning_codes") or []),
            "missing_information": [],
            "source_refs": [obs.get("text_observation_candidate_id"), adapter_input.get("adapter_input_id")],
            "evidence_refs": [adapter_input.get("model_ref")],
            "traceability_refs": list(obs.get("traceability_refs") or []) + [norm_id],
            "candidate_only": True,
        })
    return results
