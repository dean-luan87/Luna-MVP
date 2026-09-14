# -*- coding: utf-8 -*-
"""Evidence Fusion Adapter — real chain evidence set, not answer synthesis v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_evidence_package(
    *,
    slot_id: str,
    provider_id: str,
    evidence_type: str,
    payload: Dict[str, Any],
    status: str = "collected",
) -> Dict[str, Any]:
    return {
        "package_id": _uid("ep"),
        "slot_id": slot_id,
        "provider_id": provider_id,
        "evidence_type": evidence_type,
        "payload": payload,
        "status": status,
        "candidate_only": True,
        "not_fact": True,
    }


def build_chain_fusion_candidate(
    *,
    evidence_packages: List[Dict[str, Any]],
    chain_id: str = "shopfront_text_detection_ocr_qwen_context_v1",
) -> Dict[str, Any]:
    """Evidence Set → fusion_candidate → Validation. NOT answer synthesis."""
    evidence_set = [
        {
            "slot_id": p.get("slot_id"),
            "evidence_type": p.get("evidence_type"),
            "summary": p.get("payload", {}).get("summary", ""),
            "provider_id": p.get("provider_id"),
        }
        for p in evidence_packages
        if p.get("status") == "collected"
    ]
    return {
        "fusion_id": _uid("rcf"),
        "chain_id": chain_id,
        "evidence_packages": evidence_packages,
        "evidence_set": evidence_set,
        "evidence_set_count": len(evidence_set),
        "fusion_candidate": True,
        "not_answer_fusion": True,
        "not_merged_answer": True,
        "forbidden_example": "这是一家餐厅",
        "requires_validation": True,
        "fact_admission_candidate": False,
        "validation_owner": "L2_5_Decision_Validation",
        "candidate_only": True,
        "not_fact": True,
    }


def build_fact_admission_candidate(
    fusion: Dict[str, Any],
    *,
    validation_status: str = "accepted_as_evidence_collection",
) -> Dict[str, Any]:
    """Post-validation fact admission candidate — still not auto-fact."""
    return {
        "admission_id": _uid("fac"),
        "fusion_ref": fusion.get("fusion_id"),
        "validation_status": validation_status,
        "fact_admission_candidate": validation_status == "accepted_for_fact_review",
        "not_auto_fact": True,
        "candidate_only": True,
        "not_fact": True,
    }
