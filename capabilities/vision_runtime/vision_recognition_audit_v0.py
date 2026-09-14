# -*- coding: utf-8 -*-
"""Audit helpers for Vision recognition adapter selection (skeleton)."""

from __future__ import annotations

from typing import Any, Dict


def build_vision_recognition_adapter_selection_audit_v0(
    *,
    selected_provider: str,
    full_frame_direct_to_provider: bool = False,
) -> Dict[str, Any]:
    return {
        "schema": "vision_recognition_adapter_selection_audit_v0",
        "vision_provider_selection_executed": True,
        "selected_provider": selected_provider,
        "real_provider_invoked": False,
        "yolo_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "full_frame_direct_to_provider": bool(full_frame_direct_to_provider),
    }
