# -*- coding: utf-8 -*-
"""Evidence Fusion Processor — evidence slots, not answer synthesis v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_pipeline_fusion_candidate(
    *,
    collaboration_plan: Dict[str, Any],
) -> Dict[str, Any]:
    """Pipeline fusion — accumulate evidence slots per step."""
    sequence = collaboration_plan.get("provider_sequence") or []
    slots: List[Dict[str, Any]] = []
    for step in sequence:
        role = step.get("provider_role", "")
        evidence_type = {
            "text_detector": "region_candidate",
            "ocr_engine": "text_candidate",
            "vlm_context_reasoner": "scene_context_candidate",
        }.get(role, "evidence_candidate")
        slots.append({
            "slot_id": _uid("slot"),
            "step": step.get("step"),
            "provider_role": role,
            "model_id": step.get("model_id"),
            "capability_id": step.get("capability_id"),
            "evidence_type": evidence_type,
            "status": "pending",
            "depends_on_step": step.get("depends_on", []),
        })

    return {
        "fusion_id": _uid("fus"),
        "fusion_type": "pipeline_accumulation",
        "collaboration_plan_id": collaboration_plan.get("plan_id"),
        "evidence_slots": slots,
        "slot_count": len(slots),
        "fusion_candidate": True,
        "not_answer_fusion": True,
        "not_voting": True,
        "requires_validation": True,
        "validation_owner": "L2_5_Decision_Validation",
        "candidate_only": True,
        "not_fact": True,
    }


def build_parallel_fusion_candidate(
    *,
    collaboration_plan: Dict[str, Any],
) -> Dict[str, Any]:
    """Parallel fusion — evidence collection plan, not merged hypothesis."""
    parallel = collaboration_plan.get("parallel_strategy") or {}
    providers = parallel.get("providers") or []
    slots: List[Dict[str, Any]] = []
    for prov in providers:
        role = prov.get("provider_role", "")
        evidence_type = {
            "scene_hypothesis": "scene_hypothesis_candidate",
            "grounding_structure": "spatial_structure_candidate",
        }.get(role, "evidence_candidate")
        slots.append({
            "slot_id": _uid("slot"),
            "provider_role": role,
            "model_id": prov.get("model_id"),
            "evidence_type": evidence_type,
            "status": "pending",
        })

    return {
        "fusion_id": _uid("fus"),
        "fusion_type": "parallel_collection",
        "collaboration_plan_id": collaboration_plan.get("plan_id"),
        "evidence_slots": slots,
        "evidence_collection_plan": True,
        "produces_single_answer": False,
        "fusion_candidate": True,
        "not_answer_fusion": True,
        "not_voting": True,
        "requires_validation": True,
        "candidate_only": True,
        "not_fact": True,
    }


def build_fusion_candidate(
    *,
    collaboration_plan: Dict[str, Any],
) -> Dict[str, Any]:
    """Dispatch fusion by collaboration mode."""
    mode = collaboration_plan.get("collaboration_mode", "pipeline")
    if mode == "parallel_evidence":
        return build_parallel_fusion_candidate(collaboration_plan=collaboration_plan)
    return build_pipeline_fusion_candidate(collaboration_plan=collaboration_plan)
