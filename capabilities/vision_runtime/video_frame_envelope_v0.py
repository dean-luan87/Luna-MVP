# -*- coding: utf-8 -*-
"""Minimal video frame envelope (evaluation trace)."""

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional


def build_video_frame_envelope_v0(
    *,
    frame_id: str,
    stream_id: str,
    source_video_ref: str,
    frame_index: int,
    timestamp_ms: int,
    width: int,
    height: int,
    fps_source: float,
    image_ref: str,
    frame_fingerprint: str,
    sampled: bool = True,
    reason_codes: Optional[List[str]] = None,
    observed_at_ms: Optional[int] = None,
    valid_until_ms: Optional[int] = None,
) -> Dict[str, Any]:
    return {
        "schema_version": "video_frame_envelope_v0",
        "frame_id": frame_id,
        "stream_id": stream_id,
        "source_video_ref": source_video_ref,
        "frame_index": int(frame_index),
        "timestamp_ms": int(timestamp_ms),
        "width": int(width),
        "height": int(height),
        "fps_source": float(fps_source),
        "image_ref": image_ref,
        "frame_fingerprint": frame_fingerprint,
        "sampling_decision": {
            "sampled": bool(sampled),
            "reason_codes": list(reason_codes or []),
        },
        "stcm_anchor": {
            "observed_at_ms": int(observed_at_ms if observed_at_ms is not None else timestamp_ms),
            "valid_until_ms": valid_until_ms,
            "coordinate_space": "frame_pixel",
        },
    }


def fingerprint_png_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
