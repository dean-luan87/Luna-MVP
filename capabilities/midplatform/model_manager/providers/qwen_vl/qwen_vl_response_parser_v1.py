# -*- coding: utf-8 -*-
"""Qwen-VL Provider — response parser v1 (Model Manager owned)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.response_parser_v1 import (
    parse_raw_teacher_response,
)


def parse_qwen_vl_provider_response(
    raw_envelope: Dict[str, Any],
    *,
    request_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Parse raw Qwen response into provider payload under Model Manager."""
    parsed = parse_raw_teacher_response(raw_envelope)
    if parsed.get("parse_status") == "error":
        return {
            "parse_status": "error",
            "provider_error_candidate": True,
            "error_type": "provider_parse_error",
            "error_detail": parsed.get("parse_error"),
            "candidate_only": True,
            "not_fact": True,
        }

    structured = parsed.get("structured_payload") or {}
    named_claims = structured.get("named_entity_claims") or []
    hypotheses = structured.get("scene_hypothesis_candidates") or []
    has_unsupported_claim = any(
        c.get("claim_type") == "unsupported_brand"
        or c.get("unsupported_claim")
        or (c.get("name") and not hypotheses)
        for c in named_claims
    )

    return {
        "parse_status": "ok",
        "structured_payload": structured,
        "text_content": parsed.get("text_content", ""),
        "named_entity_claims": named_claims,
        "has_unsupported_claim": has_unsupported_claim,
        "provider_type": "external_teacher",
        "model_id": (request_context or {}).get("model_id", "qwen_vl"),
        "candidate_only": True,
        "not_fact": True,
    }


def build_evidence_candidate_from_parsed(
  parsed: Dict[str, Any],
  *,
  situation: Dict[str, Any],
) -> Dict[str, Any]:
    """Convert parsed provider response to evidence candidate."""
    if parsed.get("parse_status") == "error":
        return {}

    structured = parsed.get("structured_payload") or {}
    scene = (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")
    hypotheses = structured.get("scene_hypothesis_candidates") or []

    return {
        "evidence_type": "teacher_evidence_candidate",
        "provider_id": parsed.get("model_id", "qwen_vl"),
        "managed_by": "model_manager",
        "teacher_role": "perception_teacher",
        "scene_hypothesis_candidate": {
            "scene_type": scene,
            "scene_hypothesis_candidates": hypotheses,
            "candidate_only": True,
            "not_fact": True,
        },
        "visual_reasoning_candidate": {
            "reasoning_summary": structured.get("supporting_reason", ""),
            "uncertainty": structured.get("uncertainty", 0.5),
            "candidate_only": True,
            "not_fact": True,
        },
        "visual_attention_candidate": structured.get("visual_attention_candidates"),
        "does_not_override_l2_selected_plan": True,
        "does_not_write_fact": True,
        "candidate_only": True,
        "not_fact": True,
    }
