# -*- coding: utf-8 -*-
"""Model Conflict Processor — conflict candidate, no score voting v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_model_conflict_candidate(
    *,
    provider_hypotheses: List[Dict[str, Any]],
    capability_id: str = "unknown_scene_reasoning",
) -> Dict[str, Any]:
    """
    Case C: Conflicting provider outputs → model_conflict_candidate.
    Forbidden: highest_score_wins, majority_vote, auto_merge.
    """
    conflicts: List[Dict[str, Any]] = []
    for i, a in enumerate(provider_hypotheses):
        for b in provider_hypotheses[i + 1:]:
            if a.get("hypothesis_candidate") != b.get("hypothesis_candidate"):
                conflicts.append({
                    "provider_a": a.get("model_id"),
                    "hypothesis_a": a.get("hypothesis_candidate"),
                    "provider_b": b.get("model_id"),
                    "hypothesis_b": b.get("hypothesis_candidate"),
                })

    return {
        "conflict_id": _uid("mcc"),
        "capability_id": capability_id,
        "conflicting_providers": provider_hypotheses,
        "conflicts": conflicts,
        "conflict_count": len(conflicts),
        "model_conflict_candidate": True,
        "not_auto_resolved": True,
        "not_score_voting": True,
        "forbidden_resolution": ["majority_vote", "highest_score_wins", "auto_merge_hypothesis"],
        "validation_action": "request_more_evidence",
        "validation_owner": "L2_5_Decision_Validation",
        "requires_validation": True,
        "no_fact_admission": True,
        "candidate_only": True,
        "not_fact": True,
    }


def build_conflict_validation_review(
    conflict: Dict[str, Any],
) -> Dict[str, Any]:
    """Validation layer response to model conflict — planning stub."""
    return {
        "review_id": _uid("cvr"),
        "conflict_ref": conflict.get("conflict_id"),
        "validation_status": "request_more_evidence",
        "not_auto_resolved": conflict.get("not_auto_resolved") is True,
        "not_score_voting": conflict.get("not_score_voting") is True,
        "suggested_actions": [
            {"action": "request_additional_ocr_evidence"},
            {"action": "request_grounding_evidence"},
            {"action": "defer_fact_admission"},
        ],
        "candidate_only": True,
        "not_fact": True,
    }
