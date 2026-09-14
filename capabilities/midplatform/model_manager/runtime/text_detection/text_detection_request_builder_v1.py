# -*- coding: utf-8 -*-
"""Text Detection Request Builder — slot → runtime request v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_text_detection_request(
    *,
    image_ref: str = "image_fixture",
    slot_id: str = "slot_1",
    capability: str = "text_detection",
    provider_id: str = "paddleocr_detector_v1",
    situation: Optional[Dict[str, Any]] = None,
    plan: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build runtime request from collaboration slot binding — no task semantics in request."""
    scene = ((situation or {}).get("scene_profile_candidate") or {}).get("scene_type", "unknown")
    goal = ((plan or {}).get("plan_goal_candidate") or {}).get("goal_type", "unknown")

    return {
        "request_id": _uid("tdr"),
        "slot_id": slot_id,
        "capability": capability,
        "provider_id": provider_id,
        "image_ref": image_ref,
        "runtime_mode": "text_detection_only",
        "detect_text_regions": True,
        "identify_place": False,
        "run_ocr": False,
        "scene_hint_for_logging_only": scene,
        "goal_hint_for_logging_only": goal,
        "not_task_decider": True,
        "candidate_only": True,
    }
