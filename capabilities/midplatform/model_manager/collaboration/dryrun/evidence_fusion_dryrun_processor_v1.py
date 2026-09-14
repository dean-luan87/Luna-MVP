# -*- coding: utf-8 -*-
"""Evidence Fusion DryRun Processor — evidence set, not answers v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.collaboration.evidence_fusion_processor_v1 import (
    build_fusion_candidate,
    build_parallel_fusion_candidate,
    build_pipeline_fusion_candidate,
)

PARALLEL_EVIDENCE_MOCK: List[Dict[str, Any]] = [
    {"candidate_id": "candidate_1", "hypothesis": "commercial_area", "source_role": "scene_hypothesis", "evidence_type": "scene_hypothesis_candidate"},
    {"candidate_id": "candidate_2", "hypothesis": "indoor_public_space", "source_role": "visual_reasoning", "evidence_type": "scene_hypothesis_candidate"},
    {"candidate_id": "candidate_3", "hypothesis": "entrance_structure", "source_role": "grounding", "evidence_type": "spatial_structure_candidate"},
]


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_pipeline_fusion_dryrun(
    *,
    execution_plan: Dict[str, Any],
) -> Dict[str, Any]:
    """Pipeline dryrun fusion from filled slots."""
    filled = execution_plan.get("filled_slots") or []
    fusion = {
        "fusion_id": _uid("fus"),
        "fusion_type": "pipeline_accumulation",
        "collaboration_plan_id": execution_plan.get("plan_id"),
        "evidence_slots": [
            {
                "slot_id": s.get("slot_id"),
                "capability": s.get("capability"),
                "provider_role": s.get("role"),
                "model_id": s.get("filled_model_id"),
                "evidence_type": {
                    "text_detector": "region_candidate",
                    "ocr": "text_candidate",
                    "vlm_context": "scene_context_candidate",
                }.get(s.get("role", ""), "evidence_candidate"),
                "status": "pending",
                "depends_on": s.get("depends_on", []),
            }
            for s in filled
        ],
        "fusion_candidate": True,
        "not_answer_fusion": True,
        "requires_validation": True,
        "candidate_only": True,
        "not_fact": True,
    }
    return fusion


def build_parallel_fusion_dryrun(
    *,
    execution_plan: Dict[str, Any],
    mock_evidence: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Parallel dryrun — evidence set, not merged answer."""
    evidence_set = mock_evidence or PARALLEL_EVIDENCE_MOCK
    fusion = {
        "fusion_id": _uid("fus"),
        "fusion_type": "parallel_collection",
        "collaboration_plan_id": execution_plan.get("plan_id"),
        "evidence_set": evidence_set,
        "evidence_set_count": len(evidence_set),
        "produces_single_answer": False,
        "not_merged_hypothesis": True,
        "example_not_output": "这里是商场",
        "fusion_candidate": True,
        "not_answer_fusion": True,
        "not_voting": True,
        "requires_validation": True,
        "validation_owner": "L2_5_Decision_Validation",
        "candidate_only": True,
        "not_fact": True,
    }
    return fusion


def build_validation_review_for_fusion(
    fusion: Dict[str, Any],
) -> Dict[str, Any]:
    """Decision Validation stub for fusion candidate."""
    return {
        "review_id": _uid("fvr"),
        "fusion_ref": fusion.get("fusion_id"),
        "validation_status": "accepted_as_evidence_collection",
        "not_fact_admission": True,
        "candidate_only": True,
        "not_fact": True,
    }
