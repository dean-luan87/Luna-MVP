# -*- coding: utf-8 -*-
"""Offline file sampling policy for video frames (stride + max cap)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class VideoFrameSamplingParamsV0:
    max_frames: int
    sample_stride: int
    max_width: int
    max_height: int
    decode_mode: str = "offline_file"
    realtime_claim: bool = False


def run_sampling_plan_v0(
    *,
    total_frames_in_source: int,
    params: VideoFrameSamplingParamsV0,
) -> Tuple[List[int], Dict[str, Any]]:
    """Return (sampled_indices, sampling_report).

    Indices are 0-based frame positions in decode order. Stride applies to index:
    sample when ``index % sample_stride == 0`` until ``max_frames`` samples collected
    or source exhausted (conceptually; caller iterates video).
    """
    stride = max(1, int(params.sample_stride))
    cap = max(1, int(params.max_frames))
    sampled: List[int] = []
    for i in range(int(total_frames_in_source)):
        if i % stride != 0:
            continue
        sampled.append(i)
        if len(sampled) >= cap:
            break
    skipped = max(0, total_frames_in_source - len(sampled))
    report: Dict[str, Any] = {
        "schema": "video_frame_sampling_report_v0",
        "total_frames_seen": int(total_frames_in_source),
        "sampled_frame_count": len(sampled),
        "skipped_frame_count": skipped,
        "sampling_stride": stride,
        "sampled_indices": sampled,
        "decode_mode": params.decode_mode,
        "realtime_claim": bool(params.realtime_claim),
        "max_width": int(params.max_width),
        "max_height": int(params.max_height),
    }
    return sampled, report
