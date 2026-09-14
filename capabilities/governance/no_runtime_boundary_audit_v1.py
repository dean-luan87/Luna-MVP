# -*- coding: utf-8 -*-
"""No-Runtime Boundary Audit v1 — domain profiles for Luna Validation Factory."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

AUDIT_ID = "no_runtime_boundary_audit_v1"

COMMON_FIELDS: Tuple[str, ...] = (
    "live_camera_enabled_now",
    "frame_capture_executed_now",
    "arbitrary_image_read_executed_now",
    "vision_model_invoked_now",
    "ocr_provider_invoked_now",
    "navigation_action_triggered_now",
    "task_state_committed_now",
    "tts_invoked_now",
    "llm_invoked_now",
    "world_model_written_now",
    "memory_written_now",
    "user_facing_output_generated_now",
    "runtime_enabled_now",
    "execution_window_opened_now",
)

PROFILE_FIELDS: Dict[str, Tuple[str, ...]] = {
    "vision_no_runtime_profile": (
        "live_camera_enabled_now",
        "camera_runtime_enabled_now",
        "frame_capture_executed_now",
        "arbitrary_image_read_executed_now",
        "vision_model_invoked_now",
    ),
    "ocr_no_runtime_profile": ("ocr_provider_invoked_now",),
    "navigation_no_runtime_profile": (
        "real_navigation_runtime_enabled_now",
        "navigation_action_triggered_now",
        "map_write_executed_now",
        "gps_strong_anchor_committed_now",
        "route_commit_executed_now",
    ),
    "task_no_runtime_profile": ("task_state_committed_now", "tts_invoked_now", "llm_invoked_now"),
    "voice_no_runtime_profile": ("tts_invoked_now", "user_facing_output_generated_now"),
    "memory_worldmodel_no_write_profile": ("world_model_written_now", "memory_written_now", "scene_delta_generated_now"),
    "full_no_runtime_profile": COMMON_FIELDS,
}


def audit_boundary(
    snapshot: Dict[str, Any],
    *,
    profile: str = "full_no_runtime_profile",
) -> Dict[str, Any]:
    fields = PROFILE_FIELDS.get(profile, PROFILE_FIELDS["full_no_runtime_profile"])
    violations = [
        {"field": f, "value": snapshot.get(f)}
        for f in fields
        if snapshot.get(f) is True
    ]
    return {
        "audit_id": AUDIT_ID,
        "profile": profile,
        "fields_checked": list(fields),
        "violations": violations,
        "audit_pass": len(violations) == 0,
    }


def build_contract_document(*, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    m = dict(meta or {})
    return {
        "contract_id": "no_runtime_boundary_audit_contract_v1",
        "version": "v1",
        "profiles": {k: list(v) for k, v in PROFILE_FIELDS.items()},
        "entrypoint": "audit_boundary(snapshot, profile=...)",
        **m,
    }
