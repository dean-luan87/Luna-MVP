# -*- coding: utf-8 -*-
"""Qwen-VL Teacher — response parser v1 (raw API → parsed teacher payload)."""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional


def _extract_text_content(raw_response: Dict[str, Any]) -> str:
    if raw_response.get("error"):
        return ""
    output = raw_response.get("output") or {}
    choices = output.get("choices") or []
    if choices:
        message = choices[0].get("message") or {}
        content = message.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            texts = []
            for part in content:
                if isinstance(part, dict) and part.get("text"):
                    texts.append(part["text"])
                elif isinstance(part, str):
                    texts.append(part)
            return "\n".join(texts)
    if "text" in raw_response:
        return str(raw_response["text"])
    if "content" in raw_response:
        return str(raw_response["content"])
    return ""


def _parse_json_blob(text: str) -> Optional[Dict[str, Any]]:
    text = (text or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None


def parse_raw_teacher_response(raw_envelope: Dict[str, Any]) -> Dict[str, Any]:
    """Parse Qwen raw response into intermediate structured payload (not evidence yet)."""
    raw = raw_envelope.get("raw_response") or {}
    if raw_envelope.get("error") or raw.get("error"):
        return {
            "parse_status": "error",
            "parse_error": raw_envelope.get("error") or raw.get("error"),
            "text_content": "",
            "structured_payload": None,
            "candidate_only": True,
            "not_fact": True,
        }

    text = _extract_text_content(raw)
    structured = _parse_json_blob(text)

    if structured is None and text:
        structured = {
            "scene_hypothesis_candidates": [],
            "visual_attention_candidates": [],
            "task_clue_candidates": [],
            "tools_suggested": [],
            "named_entity_claims": [],
            "supporting_reason": text[:500],
            "uncertainty": 0.5,
            "free_text_fallback": True,
            "candidate_only": True,
            "not_fact": True,
        }
        lower = text.lower()
        if "starbucks" in lower or "星巴克" in text:
            structured["named_entity_claims"] = [{"name": "Starbucks", "claim_text": text[:200]}]
        if "slam" in lower:
            structured["tools_suggested"] = ["slam"]
            structured["task_clue_candidates"] = [{"clue_text": text[:200], "tools_suggested": ["slam"]}]

    return {
        "parse_status": "ok" if structured else "empty",
        "text_content": text,
        "structured_payload": structured,
        "provider_metadata": {
            "request_id": raw_envelope.get("request_id"),
            "model_id": raw_envelope.get("model_id"),
            "live_call": raw_envelope.get("live_call"),
            "recorded_fixture_id": raw_envelope.get("recorded_fixture_id"),
            "latency_ms": raw_envelope.get("latency_ms"),
            "usage": raw_envelope.get("usage"),
        },
        "candidate_only": True,
        "not_fact": True,
    }
