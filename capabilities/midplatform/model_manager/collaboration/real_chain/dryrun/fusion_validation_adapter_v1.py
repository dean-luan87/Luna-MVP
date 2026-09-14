# -*- coding: utf-8 -*-
"""Fusion Validation Adapter — fusion → validation → fact admission candidate v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.collaboration.real_chain.evidence_fusion_adapter_v1 import (
    build_chain_fusion_candidate,
    build_fact_admission_candidate,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_fusion_and_validation(
    *,
    evidence_packages: List[Dict[str, Any]],
    chain_id: str = "shopfront_text_detection_ocr_qwen_context_v1",
    validation_status: str = "accepted_as_evidence_collection",
) -> Dict[str, Any]:
    fusion = build_chain_fusion_candidate(evidence_packages=evidence_packages, chain_id=chain_id)
    validation = {
        "validation_id": _uid("val"),
        "fusion_ref": fusion.get("fusion_id"),
        "validation_status": validation_status,
        "not_fact_admission": validation_status != "accepted_for_fact_review",
        "candidate_only": True,
        "not_fact": True,
    }
    fact_admission = build_fact_admission_candidate(
        fusion,
        validation_status="accepted_for_fact_review" if validation_status == "accepted_for_fact_review" else validation_status,
    )
    return {
        "fusion_candidate": fusion,
        "validation_review": validation,
        "fact_admission_candidate": fact_admission,
    }


def run_ocr_failure_validation(
    *,
    ocr_failure_package: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "validation_id": _uid("val"),
        "validation_status": "request_more_evidence",
        "evidence_incomplete": True,
        "ocr_failure_acknowledged": ocr_failure_package.get("evidence_type") == "ocr_failure_candidate",
        "not_qwen_guess": True,
        "l2_replan_candidate": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_evidence_conflict_validation(
    *,
    ocr_text: str,
    qwen_hypothesis: str,
    qwen_confidence: float = 0.9,
) -> Dict[str, Any]:
    """Case E: evidence conflict — Qwen confidence cannot override OCR."""
    conflict = {
        "conflict_id": _uid("ec"),
        "evidence_conflict_candidate": True,
        "conflict_type": "semantic_mismatch",
        "ocr_evidence": ocr_text,
        "qwen_hypothesis": qwen_hypothesis,
        "qwen_confidence": qwen_confidence,
        "not_confidence_override": True,
        "forbidden": "qwen_confidence_overrides_ocr",
        "candidate_only": True,
    }
    validation = {
        "validation_id": _uid("val"),
        "conflict_ref": conflict.get("conflict_id"),
        "validation_status": "requires_human_review",
        "resolution": "request_more_evidence",
        "not_confidence_based": True,
        "candidate_only": True,
    }
    return {"evidence_conflict": conflict, "validation_review": validation}


def run_context_challenge_validation(
    *,
    ocr_text: str,
    context_payload: Dict[str, Any],
) -> Dict[str, Any]:
    """Case D: context allowed as candidate, not as fact."""
    return {
        "validation_id": _uid("val"),
        "validation_status": "accepted_as_context_candidate",
        "ocr_text": ocr_text,
        "context_evidence_allowed": True,
        "fact_restaurant_true": False,
        "restaurant_fact_forbidden": context_payload.get("restaurant_fact") is not True,
        "context_is_candidate_only": True,
        "candidate_only": True,
        "not_fact": True,
    }
