# -*- coding: utf-8 -*-
"""Qwen-VL Teacher — evidence normalizer v1 (parsed payload → teacher_evidence_candidate)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_types_v1 import (
    POLICY_REF,
    PROVIDER_ID,
    TEACHER_ROLE,
    candidate_meta,
)

REAL_PROVIDER_POLICY_REF = "qwen_vl_real_provider_policy_v1"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _scene(situation: Dict[str, Any]) -> str:
    return (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")


def _detect_policy_signals(payload: Dict[str, Any], text: str, l1_scene: str) -> Dict[str, Any]:
    tools = list(payload.get("tools_suggested") or [])
    clues = payload.get("task_clue_candidates") or []
    for clue in clues:
        tools.extend(clue.get("tools_suggested") or [])
    lower = (text or "").lower()
    if "slam" in tools or ("slam" in lower and ("text" in lower or "ocr" in lower or "文字" in text)):
        return {"teacher_suggests": "slam_for_text", "policy_risk_candidates": ["tool_mismatch"]}

    claims = payload.get("named_entity_claims") or []
    if claims or "starbucks" in lower or "星巴克" in text:
        return {
            "unsupported_claim": True,
            "hallucination_risk": True,
            "supporting_ocr_evidence": False,
            "policy_risk_candidates": ["unsupported_claim"],
        }

    hypotheses = payload.get("scene_hypothesis_candidates") or []
    if hypotheses and hypotheses[0].get("scene_type") and l1_scene != "unknown_scene":
        return {"proposed_scene_type": hypotheses[0]["scene_type"]}

    return {}


def normalize_teacher_evidence(
    *,
    parsed_response: Dict[str, Any],
    situation_candidate: Dict[str, Any],
    plan_candidate: Optional[Dict[str, Any]] = None,
    raw_envelope: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Transform parsed Qwen output into teacher_evidence_candidate — never fact/decision."""
    evidence_id = _uid("qtec")
    payload = parsed_response.get("structured_payload") or {}
    text = parsed_response.get("text_content") or ""
    l1_scene = _scene(situation_candidate)
    signals = _detect_policy_signals(payload, text, l1_scene)

    hypotheses = payload.get("scene_hypothesis_candidates") or []
    clues = payload.get("task_clue_candidates") or []
    attention = payload.get("visual_attention_candidates") or []

    evidence_type = "scene_hypothesis_candidate"
    if attention:
        evidence_type = "visual_attention_candidate"
    elif clues and not hypotheses:
        evidence_type = "task_clue_candidate"

    uncertainty = float(payload.get("uncertainty") or 0.5)
    confidence = 0.5
    if hypotheses:
        confidence = float(hypotheses[0].get("confidence_candidate") or hypotheses[0].get("confidence") or 0.5)

    suggestion_text = payload.get("supporting_reason") or text[:300]
    tools_suggested = list(payload.get("tools_suggested") or [])
    for clue in clues:
        tools_suggested.extend(clue.get("tools_suggested") or [])

    evidence: Dict[str, Any] = {
        "teacher_id": evidence_id,
        "evidence_id": evidence_id,
        "teacher_provider": PROVIDER_ID,
        "provider_id": PROVIDER_ID,
        "teacher_role": TEACHER_ROLE,
        "evidence_type": evidence_type,
        "output_type": evidence_type,
        "scene_hypothesis_candidate": {
            "scene_hypothesis_candidates": hypotheses,
            "candidate_only": True,
            "not_fact": True,
        },
        "visual_attention_candidate": attention[0] if attention else None,
        "task_clue_candidate": clues[0] if clues else None,
        "perception_output_optional": {
            "scene_hypothesis_candidates": hypotheses,
            "visual_attention_candidates": attention,
            "task_clue_candidates": clues,
            "uncertainty": uncertainty,
            "candidate_only": True,
            "not_fact": True,
        },
        "confidence_candidate": confidence,
        "confidence": confidence,
        "uncertainty": uncertainty,
        "supporting_reason": payload.get("supporting_reason", ""),
        "tools_suggested": tools_suggested,
        "suggestion_text": suggestion_text,
        "named_entity_claims": payload.get("named_entity_claims") or [],
        "does_not_override_l1_scene": True,
        "does_not_override_l2_selected_plan": True,
        "no_runner_invocation": True,
        "no_fact_write": True,
        "requires_policy_review": True,
        "parse_status": parsed_response.get("parse_status"),
        "provider_metadata": parsed_response.get("provider_metadata"),
        "raw_response_ref": (raw_envelope or {}).get("request_id"),
        **signals,
        **candidate_meta(
            trace_refs=[
                {"stage": "raw_teacher_response", "ref": (raw_envelope or {}).get("request_id")},
                {"stage": "evidence_normalizer", "ref": evidence_id},
            ],
            policy_refs=[POLICY_REF, REAL_PROVIDER_POLICY_REF],
        ),
    }
    return evidence
