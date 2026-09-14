# -*- coding: utf-8 -*-
"""Fixed audit flags for minimal video frame ingest (no YOLO / OCR / VLM / writes)."""

from __future__ import annotations

from typing import Any, Dict


def build_default_video_frame_audit_v0(*, video_ingest_executed: bool = True) -> Dict[str, Any]:
    return {
        "schema": "video_frame_audit_v0",
        "video_ingest_executed": bool(video_ingest_executed),
        "real_camera_invoked": False,
        "yolo_invoked": False,
        "ocr_invoked": False,
        "vlm_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
    }
