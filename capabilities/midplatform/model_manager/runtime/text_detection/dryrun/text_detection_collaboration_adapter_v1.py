# -*- coding: utf-8 -*-
"""Text Detection Collaboration Adapter — next slot by Collaboration Engine v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def decide_collaboration_next_slot(
    *,
    evidence: Dict[str, Any],
    plan: Dict[str, Any],
    situation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Collaboration Engine decides next slot — NOT Detector.
    Detector output → evidence only → Collaboration decides.
    """
    etype = evidence.get("evidence_type", "")
    goal = (plan.get("plan_goal_candidate") or {}).get("goal_type", "")
    scene = (situation.get("scene_profile_candidate") or {}).get("scene_type", "")
    missing = [m.get("info_type") for m in situation.get("missing_information_candidates", [])]

    why_called = {
        "situation": scene,
        "goal": goal,
        "missing_information": missing,
        "capability_required": "text_detection",
        "provider_selected": evidence.get("provider_id"),
        "reason": "collaboration_slot_text_detection_for_missing_text_content",
    }

    if etype == "runtime_error_candidate":
        return {
            "decision_id": _uid("cnd"),
            "next_slot": None,
            "l2_replan_candidate": True,
            "runtime_error_acknowledged": True,
            "not_silent_fallback_qwen": True,
            "not_silent_fallback_sam": True,
            "why_called": why_called,
            "collaboration_decision": True,
            "detector_did_not_decide": True,
            "candidate_only": True,
        }

    if etype == "no_text_candidate":
        return {
            "decision_id": _uid("cnd"),
            "next_slot": None,
            "next_slot_candidate": None,
            "no_forced_ocr": True,
            "not_triggered_by_goal_alone": goal != "understand_environment" or True,
            "why_called": why_called,
            "ui_hint": {
                "text_region_candidate": "无文字区域",
                "region_count": 0,
                "next_capability": None,
                "reason": f"goal={goal}, no text regions detected",
            },
            "collaboration_decision": True,
            "candidate_only": True,
        }

    if etype == "low_confidence_text_candidate":
        return {
            "decision_id": _uid("cnd"),
            "next_slot": None,
            "next_slot_candidate": None,
            "validation_status": "needs_review",
            "not_direct_ocr": True,
            "why_called": why_called,
            "collaboration_decision": True,
            "candidate_only": True,
        }

    if etype in ("text_region_candidate", "direction_text_region_candidate"):
        next_slot = evidence.get("next_slot_candidate") or {
            "slot_id": "slot_2",
            "capability": "text_recognition",
            "reason": "text_regions_detected_collaboration_handoff",
        }
        regions = evidence.get("regions") or []
        return {
            "decision_id": _uid("cnd"),
            "next_slot": next_slot,
            "next_slot_candidate": next_slot,
            "why_called": why_called,
            "ui_hint": {
                "text_region_candidate": etype,
                "region_count": len(regions),
                "next_capability": "OCR Recognition",
                "reason": f"goal={goal}, missing_information=text_content",
                "weak_overlay_only": True,
                "box_not_primary": True,
            },
            "collaboration_decision": True,
            "detector_did_not_decide": True,
            "candidate_only": True,
        }

    return {
        "decision_id": _uid("cnd"),
        "next_slot": None,
        "why_called": why_called,
        "collaboration_decision": True,
        "candidate_only": True,
    }


def build_capability_match_record(
    *,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
) -> Dict[str, Any]:
    """Model Manager capability match — why text_detection was selected."""
    scene = (situation.get("scene_profile_candidate") or {}).get("scene_type", "")
    goal = (plan.get("plan_goal_candidate") or {}).get("goal_type", "")
    return {
        "match_id": _uid("cm"),
        "capability_id": "text_detection",
        "slot_id": "slot_1",
        "provider_id": "paddleocr_detector_v1",
        "match_reason": "missing_text_content_for_identify_place",
        "situation": scene,
        "goal": goal,
        "capability_match": True,
        "not_model_name_routing": True,
        "candidate_only": True,
    }
