# -*- coding: utf-8 -*-
"""Collaboration Conflict DryRun Processor — semantic conflict governance v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.collaboration.model_conflict_processor_v1 import (
    build_conflict_validation_review,
    build_model_conflict_candidate,
)


def _uid(prefix: str) -> str:
    from uuid import uuid4
    return f"{prefix}_{uuid4().hex[:10]}"


def build_semantic_conflict_dryrun(
    *,
    provider_evidence: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Case D: semantic conflict — forbidden highest confidence wins."""
    evidence = provider_evidence or [
        {"model_id": "qwen_vl", "hypothesis_candidate": "shopfront_sign", "evidence_type": "scene_hypothesis_candidate", "confidence": 0.82},
        {"model_id": "internvl2_5", "hypothesis_candidate": "restaurant_interior", "evidence_type": "scene_hypothesis_candidate", "confidence": 0.79},
    ]
    conflict = build_model_conflict_candidate(
        provider_hypotheses=evidence,
        capability_id="unknown_scene_reasoning",
    )
    conflict.update({
        "conflict_type": "semantic_conflict",
        "affected_evidence": "scene_hypothesis",
        "resolution": "request_more_evidence",
        "forbidden_resolution": ["highest_confidence_wins", "majority_vote"],
        "not_score_voting": True,
    })
    validation = build_conflict_validation_review(conflict)
    validation.update({
        "resolution": "request_more_evidence",
        "not_confidence_based": True,
    })
    return {
        "model_conflict_candidate": conflict,
        "validation_review": validation,
        "conflict_detected": conflict.get("conflict_count", 0) > 0,
        "not_auto_resolved": conflict.get("not_auto_resolved") is True,
        "not_confidence_voting": True,
        "candidate_only": True,
        "not_fact": True,
    }


def build_challenge_dryrun(
    *,
    selected_plan_capability: str = "precise_ocr",
    validation_confidence: float = 0.35,
) -> Dict[str, Any]:
    """Case C: Teacher challenge — alternative hypothesis, plan unchanged."""
    challenge = {
        "challenge_id": _uid("ch"),
        "trigger": "validation_confidence_low",
        "validation_confidence": validation_confidence,
        "confidence_threshold": 0.5,
        "original_selected_plan": selected_plan_capability,
        "selected_plan_unchanged": True,
        "override_plan": False,
        "teacher_challenger": "qwen_vl",
        "alternative_hypothesis_candidate": {
            "hypothesis": "可能不是店招，而是广告牌",
            "hypothesis_en": "possibly_advertisement_not_shopfront_sign",
            "evidence_type": "alternative_hypothesis_candidate",
            "challenger_role": "teacher_challenger",
        },
        "challenge_mode": True,
        "challenge_does_not_override_plan": True,
        "candidate_only": True,
        "not_fact": True,
    }
    validation = {
        "review_id": _uid("cvr"),
        "validation_status": "challenge_accepted_as_alternative",
        "selected_plan": selected_plan_capability,
        "selected_plan_overridden": False,
        "alternative_added": True,
        "candidate_only": True,
        "not_fact": True,
    }
    return {
        "challenge": challenge,
        "validation_review": validation,
        "plan_not_overridden": challenge.get("selected_plan_unchanged") is True,
        "alternative_hypothesis_present": True,
        "candidate_only": True,
        "not_fact": True,
    }
