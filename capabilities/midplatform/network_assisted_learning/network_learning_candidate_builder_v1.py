# -*- coding: utf-8
"""Network learning candidate builder — deterministic stub v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

POLICY_REF = "network_assisted_situation_learning_policy_v1"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _base_meta(
    *,
    source_type: str,
    source_ref: str,
    created_from: str,
    provenance_ref: str,
) -> Dict[str, Any]:
    return {
        "source_type": source_type,
        "source_refs": [source_ref],
        "source_ref": source_ref,
        "provenance_ref": provenance_ref,
        "created_from": created_from,
        "policy_refs": [POLICY_REF],
        "candidate_only": True,
        "not_fact": True,
        "review_status": "pending_policy_review",
        "trace_refs": [{"stage": created_from, "ref": source_ref}],
    }


def build_provenance(
    origin_type: str,
    origin_ref: str,
    steps: Optional[List[str]] = None,
) -> Dict[str, Any]:
    pid = _uid("prv")
    return {
        "provenance_id": pid,
        "origin_type": origin_type,
        "origin_ref": origin_ref,
        "transformation_steps": steps or ["normalize_learning_candidate"],
        "policy_review_refs": [],
        "trace_refs": [{"stage": "provenance", "ref": pid}],
        "candidate_only": True,
        "not_fact": True,
    }


def build_external_source(
    source_type: str,
    source_name: str,
    trust_tier: str = "medium",
    allowed_usage: str = "case_candidate",
) -> Dict[str, Any]:
    sid = _uid("els")
    return {
        "source_id": sid,
        "source_type": source_type,
        "source_name": source_name,
        "collection_method": "deterministic_stub_v1",
        "license_or_usage_note": "planning_stub_only",
        "trust_tier": trust_tier,
        "allowed_usage": allowed_usage,
        "candidate_only": True,
        "not_fact": True,
        "source_ref": sid,
        "provenance_ref": sid,
        "review_status": "pending_policy_review",
        "created_from": source_type,
        "policy_refs": [POLICY_REF],
        "trace_refs": [],
    }


def build_from_teacher_label(teacher_payload: Dict[str, Any]) -> Dict[str, Any]:
    prov = build_provenance("teacher_model", teacher_payload.get("input_ref", "teacher_input"))
    tid = _uid("tlc")
    label = {
        "teacher_label_id": tid,
        "teacher_model_name": teacher_payload.get("teacher_model_name", "third_party_vlm_teacher_stub"),
        "teacher_model_version_optional": teacher_payload.get("teacher_model_version", "stub_v1"),
        "input_ref": teacher_payload.get("input_ref", ""),
        "scene_profile_candidate": teacher_payload.get("scene", "unknown_scene"),
        "task_clue_candidates": teacher_payload.get("task_clues", []),
        "attention_target_hints": teacher_payload.get("attention_targets", []),
        "model_need_hints": teacher_payload.get("needed_tools", []),
        "noop_model_hints": teacher_payload.get("noop_tools", []),
        "reasoning_summary": teacher_payload.get("reasoning_summary", ""),
        "confidence": teacher_payload.get("confidence", 0.75),
        "candidate_only": True,
        "not_fact": True,
        "requires_policy_review": True,
        "requires_human_review": False,
        "provenance_ref": prov["provenance_id"],
        "source_ref": tid,
        "review_status": "pending_policy_review",
        "created_from": "teacher_model",
        "policy_refs": [POLICY_REF],
        "trace_refs": [{"stage": "teacher_model_label", "ref": tid}],
    }
    candidate = normalize_learning_candidate(
        {
            "proposed_scene_type": teacher_payload.get("scene"),
            "proposed_task_clues": teacher_payload.get("task_clues", []),
            "proposed_attention_targets": teacher_payload.get("attention_targets", []),
            "proposed_needed_tools": teacher_payload.get("needed_tools", []),
            "proposed_noop_tools": teacher_payload.get("noop_tools", []),
            "evidence_summary": teacher_payload.get("reasoning_summary", ""),
            "confidence": teacher_payload.get("confidence", 0.75),
        },
        source_type="teacher_model",
        source_ref=tid,
        provenance_ref=prov["provenance_id"],
        created_from="build_from_teacher_label",
    )
    return {"teacher_label": label, "provenance": prov, "learning_candidate": candidate}


def build_from_web_reference(web_payload: Dict[str, Any]) -> Dict[str, Any]:
    prov = build_provenance("web_reference", web_payload.get("query_text", "web_query"))
    wid = _uid("wrc")
    web = {
        "web_reference_id": wid,
        "query_text": web_payload.get("query_text", ""),
        "source_title_optional": web_payload.get("source_title"),
        "source_uri_optional": web_payload.get("source_uri"),
        "extracted_clues": web_payload.get("extracted_clues", []),
        "scene_similarity_hints": web_payload.get("scene_similarity_hints", []),
        "usage_limit_note": "reference_only; no_direct_web_training",
        "trust_tier": web_payload.get("trust_tier", "unknown"),
        "candidate_only": True,
        "not_fact": True,
        "review_status": "pending_policy_review",
        "provenance_ref": prov["provenance_id"],
        "source_ref": wid,
        "created_from": "web_reference",
        "policy_refs": [POLICY_REF],
        "trace_refs": [],
    }
    candidate = normalize_learning_candidate(
        {
            "proposed_scene_type": web_payload.get("proposed_scene_type", "shopfront_sign"),
            "proposed_task_clues": web_payload.get("task_clues", []),
            "proposed_attention_targets": web_payload.get("attention_targets", []),
            "proposed_needed_tools": [],
            "proposed_noop_tools": [],
            "evidence_summary": "; ".join(web_payload.get("extracted_clues", [])),
            "confidence": 0.45,
            "risk_flags": ["web_trust_unknown"],
        },
        source_type="web_reference",
        source_ref=wid,
        provenance_ref=prov["provenance_id"],
        created_from="build_from_web_reference",
    )
    return {"web_reference": web, "provenance": prov, "learning_candidate": candidate}


def build_from_human_correction(correction_payload: Dict[str, Any]) -> Dict[str, Any]:
    prov = build_provenance("human_correction", correction_payload.get("correction_id", "hcorr"))
    cid = _uid("hcls")
    signal = {
        "signal_id": cid,
        "correction_text": correction_payload.get("correction_text", ""),
        "proposed_scene_type": correction_payload.get("proposed_scene_type"),
        "proposed_task_clues": correction_payload.get("proposed_task_clues", []),
        "proposed_needed_tools": correction_payload.get("proposed_needed_tools", []),
        "proposed_noop_tools": correction_payload.get("proposed_noop_tools", []),
        "candidate_only": True,
        "not_fact": True,
        "human_correction_not_ground_truth": True,
        "source_ref": cid,
        "provenance_ref": prov["provenance_id"],
        "review_status": "pending_policy_review",
        "created_from": "human_correction",
        "policy_refs": [POLICY_REF],
        "trace_refs": [],
    }
    candidate = normalize_learning_candidate(
        {
            "proposed_scene_type": correction_payload.get("proposed_scene_type"),
            "proposed_task_clues": correction_payload.get("proposed_task_clues", []),
            "proposed_needed_tools": correction_payload.get("proposed_needed_tools", []),
            "proposed_noop_tools": correction_payload.get("proposed_noop_tools", []),
            "evidence_summary": correction_payload.get("correction_text", ""),
            "confidence": 0.82,
        },
        source_type="human_correction",
        source_ref=cid,
        provenance_ref=prov["provenance_id"],
        created_from="build_from_human_correction",
    )
    return {"human_correction_signal": signal, "provenance": prov, "learning_candidate": candidate}


def build_from_test_trace(trace_payload: Dict[str, Any]) -> Dict[str, Any]:
    prov = build_provenance("test_trace", trace_payload.get("job_id", "test_trace"))
    tid = _uid("ttls")
    signal = {
        "signal_id": tid,
        "job_id": trace_payload.get("job_id"),
        "current_behavior": trace_payload.get("current_behavior", {}),
        "expected_behavior": trace_payload.get("expected_behavior", {}),
        "candidate_only": True,
        "not_fact": True,
        "source_ref": tid,
        "provenance_ref": prov["provenance_id"],
        "review_status": "pending_policy_review",
        "created_from": "test_trace",
        "policy_refs": [POLICY_REF],
        "trace_refs": [],
    }
    risk_flags = ["current_behavior_mismatch"] if trace_payload.get("current_behavior") else []
    candidate = normalize_learning_candidate(
        {
            "proposed_scene_type": trace_payload.get("expected_behavior", {}).get("scene"),
            "proposed_task_clues": trace_payload.get("expected_behavior", {}).get("task_clues", []),
            "proposed_needed_tools": trace_payload.get("expected_behavior", {}).get("needed_tools", []),
            "proposed_noop_tools": trace_payload.get("expected_behavior", {}).get("noop_tools", []),
            "proposed_missing_information": trace_payload.get("expected_behavior", {}).get("missing_information", []),
            "evidence_summary": f"regression from {trace_payload.get('job_id')}",
            "confidence": 0.88,
            "risk_flags": risk_flags,
        },
        source_type="test_trace",
        source_ref=tid,
        provenance_ref=prov["provenance_id"],
        created_from="build_from_test_trace",
    )
    return {"test_trace_signal": signal, "provenance": prov, "learning_candidate": candidate}


def normalize_learning_candidate(
    fields: Dict[str, Any],
    *,
    source_type: str,
    source_ref: str,
    provenance_ref: str,
    created_from: str,
) -> Dict[str, Any]:
    lid = _uid("slc")
    meta = _base_meta(
        source_type=source_type,
        source_ref=source_ref,
        created_from=created_from,
        provenance_ref=provenance_ref,
    )
    return {
        "learning_candidate_id": lid,
        "proposed_scene_type": fields.get("proposed_scene_type"),
        "proposed_environment_type": fields.get("proposed_environment_type"),
        "proposed_task_clues": fields.get("proposed_task_clues", []),
        "proposed_attention_targets": fields.get("proposed_attention_targets", []),
        "proposed_needed_tools": fields.get("proposed_needed_tools", []),
        "proposed_noop_tools": fields.get("proposed_noop_tools", []),
        "proposed_missing_information": fields.get("proposed_missing_information", []),
        "evidence_summary": fields.get("evidence_summary", ""),
        "confidence": fields.get("confidence", 0.5),
        "risk_flags": fields.get("risk_flags", []),
        **meta,
    }
