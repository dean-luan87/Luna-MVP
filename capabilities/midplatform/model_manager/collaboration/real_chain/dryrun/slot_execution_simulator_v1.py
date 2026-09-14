# -*- coding: utf-8 -*-
"""Slot Execution Simulator — deterministic runtime fixtures v1 (dryrun)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

FIXTURES: Dict[str, Dict[str, Any]] = {
    "detection_success": {
        "status": "completed",
        "evidence_type": "text_region_candidate",
        "payload": {
            "regions": [{"bbox": [120, 80, 340, 160], "label": "text_region"}],
            "region": "shopfront_area_candidate",
            "summary": "检测到招牌文字区域",
        },
    },
    "ocr_success_ashu": {
        "status": "completed",
        "evidence_type": "ocr_text_candidate",
        "payload": {"text": "阿叔阿姨的店", "confidence": 0.92, "summary": "阿叔阿姨的店"},
    },
    "ocr_success_jiahui": {
        "status": "completed",
        "evidence_type": "ocr_text_candidate",
        "payload": {"text": "嘉会湖", "confidence": 0.88, "summary": "嘉会湖"},
    },
    "ocr_failure_blurry": {
        "status": "failed",
        "evidence_type": "ocr_failure_candidate",
        "payload": {"failure_reason": "text_blurry", "confidence": 0.12, "summary": "文字模糊无法识别"},
    },
    "qwen_context_commercial": {
        "status": "completed",
        "evidence_type": "context_evidence_candidate",
        "payload": {
            "interpretation": "该文字可能对应店铺招牌区域",
            "context": "commercial_sign_candidate",
            "summary": "commercial_sign_candidate",
            "not_ocr": True,
        },
    },
    "qwen_context_restaurant": {
        "status": "completed",
        "evidence_type": "context_evidence_candidate",
        "payload": {
            "interpretation": "可能是一家餐饮店",
            "context": "restaurant_context_candidate",
            "not_fact": True,
            "restaurant_fact": False,
        },
    },
    "qwen_hypothesis_airport": {
        "status": "completed",
        "evidence_type": "scene_hypothesis_candidate",
        "payload": {
            "hypothesis": "可能是机场",
            "confidence": 0.90,
            "not_ocr_substitute": True,
        },
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def simulate_slot_execution(
    *,
    slot: Dict[str, Any],
    fixture_key: str,
    provider_override: Optional[str] = None,
) -> Dict[str, Any]:
    """Deterministic slot runtime — no real model inference."""
    fixture = FIXTURES.get(fixture_key, FIXTURES["detection_success"])
    provider_id = provider_override or slot.get("filled_provider_id", "")
    return {
        "provider_execution_id": _uid("pex"),
        "slot_id": slot.get("slot_id"),
        "capability": slot.get("capability"),
        "provider_id": provider_id,
        "fixture_key": fixture_key,
        "status": fixture.get("status", "completed"),
        "evidence_type": fixture.get("evidence_type"),
        "payload": dict(fixture.get("payload") or {}),
        "evidence_id": _uid("ev"),
        "runtime_simulated": True,
        "not_real_inference": True,
        "candidate_only": True,
        "not_fact": True,
    }


def simulate_pipeline_chain(
    *,
    bound_slots: List[Dict[str, Any]],
    fixture_map: Dict[str, str],
) -> List[Dict[str, Any]]:
    """Execute slots in pipeline order using fixtures."""
    results: List[Dict[str, Any]] = []
    for slot in sorted(bound_slots, key=lambda s: s.get("step", 0)):
        sid = slot.get("slot_id", "")
        key = fixture_map.get(sid, "detection_success")
        if key == "skip":
            continue
        override = slot.get("filled_provider_id")
        results.append(simulate_slot_execution(slot=slot, fixture_key=key, provider_override=override))
    return results
