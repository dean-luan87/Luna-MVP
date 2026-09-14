# -*- coding: utf-8 -*-
"""SLAM video limited runner skeleton v1 — no real ORB-SLAM backend."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional


def _video_metadata(path: Path) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "file_name": path.name,
        "file_size_bytes": path.stat().st_size if path.is_file() else None,
        "extension": path.suffix.lower(),
    }
    try:
        from PIL import Image  # noqa: WPS433

        # PIL cannot read video; keep file stats only
        _ = Image
    except ImportError:
        pass
    return meta


def run_slam_video_limited_runner(
    *,
    asset_manifest: Dict[str, Any],
    output_dir: Path,
    job_id: str,
) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    local_path = asset_manifest.get("local_path") or asset_manifest.get("local_path_or_browser_file_name")
    asset_type = asset_manifest.get("asset_type", "video")
    path = Path(str(local_path)) if local_path else None

    metadata: Optional[Dict[str, Any]] = None
    if path and path.is_file():
        metadata = _video_metadata(path)

    return {
        "status": "completed_limited",
        "status_reason": "slam_limited_placeholder_no_real_backend",
        "no_boundary_violation": True,
        "failure_recorded": False,
        "runner_note": "real_slam_backend_not_connected",
        "no_gt_limited_mode": True,
        "no_ate": True,
        "not_comparable_to_gt_benchmark": True,
        "limited_mode": True,
        "asset_type": asset_type,
        "video_metadata": metadata,
        "trajectory": None,
        "ground_truth": None,
        "diagnostics": {
            "trajectory_visualization": "unavailable_without_runner_output",
            "tracking_lost_ratio": None,
            "smoothness_proxy": None,
            "failure_timeline": [],
        },
        "job_id": job_id,
        "message": (
            "SLAM limited route: video/frame_sequence registered. "
            "Real ORB-SLAM/VINS/Kimera not connected. No ATE, no fake trajectory."
        ),
    }
