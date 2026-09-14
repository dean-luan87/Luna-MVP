# -*- coding: utf-8
"""Situation case library builder — deterministic stub v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

POLICY_REF = "network_assisted_situation_learning_policy_v1"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_case_record(
    candidate: Dict[str, Any],
    review: Dict[str, Any],
    *,
    case_type: str = "custom",
    case_title: str = "",
) -> Dict[str, Any]:
    cid = _uid("scr")
    return {
        "case_id": cid,
        "case_type": case_type,
        "case_title": case_title or f"{candidate.get('proposed_scene_type', 'case')} reference",
        "canonical_scene_type": candidate.get("proposed_scene_type"),
        "environment_type": candidate.get("proposed_environment_type"),
        "visual_clues": candidate.get("proposed_attention_targets", []),
        "task_clues": candidate.get("proposed_task_clues", []),
        "attention_targets": candidate.get("proposed_attention_targets", []),
        "recommended_tools": candidate.get("proposed_needed_tools", []),
        "noop_tools": candidate.get("proposed_noop_tools", []),
        "missing_information_patterns": candidate.get("proposed_missing_information", []),
        "negative_examples": [],
        "source_refs": candidate.get("source_refs", []),
        "accepted_from_learning_candidate_refs": [candidate.get("learning_candidate_id")],
        "review_status": candidate.get("review_status", "accepted_as_case"),
        "policy_refs": [POLICY_REF, review.get("review_id", "")],
        "candidate_only": True,
        "not_fact": True,
        "source_ref": cid,
        "provenance_ref": candidate.get("provenance_ref"),
        "created_from": "accept_candidate_as_case_record",
        "trace_refs": candidate.get("trace_refs", []),
    }


def accept_candidate_as_case_record(
    candidate: Dict[str, Any],
    review: Dict[str, Any],
    **kwargs: Any,
) -> Optional[Dict[str, Any]]:
    if review.get("policy_decision") != "accept_as_case_candidate":
        return None
    if candidate.get("review_status") != "accepted_as_case":
        return None
    return build_case_record(candidate, review, **kwargs)


def merge_similar_cases(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen: Dict[str, Dict[str, Any]] = {}
    for case in cases:
        key = f"{case.get('canonical_scene_type')}::{','.join(case.get('task_clues', []))}"
        if key not in seen:
            seen[key] = case
    return list(seen.values())


def build_training_dataset_candidate(
    case_records: List[Dict[str, Any]],
) -> Dict[str, Any]:
    did = _uid("stdc")
    return {
        "dataset_candidate_id": did,
        "case_refs": [c.get("case_id") for c in case_records],
        "input_feature_spec": {
            "scene_type": "canonical_scene_type",
            "visual_clues": "visual_clues",
            "task_clues": "task_clues",
        },
        "output_label_spec": {
            "recommended_tools": "recommended_tools",
            "noop_tools": "noop_tools",
            "attention_targets": "attention_targets",
        },
        "allowed_training_use": ["situation_understanding_model"],
        "blocked_training_use": ["direct_fact_prediction", "runner_invocation", "tool_install"],
        "review_status": "pending_human_approval",
        "requires_human_approval": True,
        "provenance_refs": [c.get("provenance_ref") for c in case_records if c.get("provenance_ref")],
        "candidate_only": True,
        "not_fact": True,
        "source_ref": did,
        "created_from": "build_training_dataset_candidate",
        "policy_refs": [POLICY_REF],
        "trace_refs": [],
        "no_model_training_in_planning": True,
    }
