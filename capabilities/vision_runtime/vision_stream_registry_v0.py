# -*- coding: utf-8 -*-
"""Vision stream registry v0 — read-only registration above video_frame_envelope_v0."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional


def build_vision_stream_registry_v0(
    *,
    stream_id: str,
    source_video_ref: str,
    fps_source: float,
    width: int,
    height: int,
    total_frames_seen: int,
    sampled_frame_count: int,
    sampling_policy_ref: str,
    envelopes: List[Dict[str, Any]],
    source_type: str = "offline_video",
    created_from_phase: str = "Vision-VideoFrame-Minimal-Ingest-001",
) -> Dict[str, Any]:
    """Build ``vision_stream_registry_v0`` JSON object."""
    w, h = int(width), int(height)
    if (w <= 0 or h <= 0) and envelopes:
        e0 = envelopes[0]
        w = int(e0.get("width") or w)
        h = int(e0.get("height") or h)
    return {
        "schema_version": "vision_stream_registry_v0",
        "stream_id": stream_id,
        "source_type": source_type,
        "source_video_ref": source_video_ref,
        "fps_source": float(fps_source),
        "width": w,
        "height": h,
        "total_frames_seen": int(total_frames_seen),
        "sampled_frame_count": int(sampled_frame_count),
        "sampling_policy_ref": str(Path(sampling_policy_ref).resolve()) if sampling_policy_ref else "",
        "created_from_phase": created_from_phase,
    }
