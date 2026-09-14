# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-002 — YOLO Stage-1 trial runner skeleton (no detector execution).
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from capabilities.guarded_trial.yolo_stage1_trial_precheck_v0 import build_yolo_stage1_trial_id_v0


def build_yolo_stage1_trial_runner_plan_v0(
    *,
    trial_id: str,
    max_frames_planned: int = 10,
    detector_execution_enabled: bool = False,
    camera_execution_enabled: bool = False,
) -> Dict[str, Any]:
    return {
        "runner_id": f"yolo_runner_{uuid.uuid4().hex[:12]}",
        "trial_id": trial_id,
        "runner_mode": "skeleton_only",
        "max_frames_planned": int(max_frames_planned),
        "detector_execution_enabled": bool(detector_execution_enabled),
        "camera_execution_enabled": bool(camera_execution_enabled),
        "request_trace_enabled": True,
        "abort_on_detector_error": True,
        "rollback_on_abort": True,
        "execution_result": "not_executed_skeleton_only",
    }


def run_yolo_stage1_trial_runner_skeleton_v0(
    *,
    trial_id: Optional[str] = None,
    max_frames_planned: int = 10,
) -> Dict[str, Any]:
    """
    Returns runner skeleton record only; never calls detector or camera.
    """
    tid = trial_id or build_yolo_stage1_trial_id_v0(prefix="yolo_s1_run")
    return build_yolo_stage1_trial_runner_plan_v0(
        trial_id=tid,
        max_frames_planned=max_frames_planned,
        detector_execution_enabled=False,
        camera_execution_enabled=False,
    )
