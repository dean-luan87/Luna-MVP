# -*- coding: utf-8 -*-
"""Real frame input loader v1."""

from __future__ import annotations

import base64
import struct
import uuid
from pathlib import Path
from typing import Any, Dict, Tuple

# Minimal 1x1 PNG (valid image bytes for controlled dryrun fixtures)
_MIN_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


def _write_minimal_png(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(_MIN_PNG_B64))


def load_real_frame_input_package(
    *,
    frame_input_id: str,
    image_path: str,
    frame_ref: str,
    frame_width: int,
    frame_height: int,
    timestamp: str,
    test_case_id: str,
    source_ref: str,
    camera_ref: str | None = None,
    expected_scene_notes: str | None = None,
    work_dir: str | None = None,
) -> Tuple[Dict[str, Any], list[str]]:
    """Load or materialize RealFrameInputPackage. No camera/video."""
    failure_points: list[str] = []
    path = Path(image_path)
    if not path.is_file() and work_dir:
        path = Path(work_dir) / f"{test_case_id}_frame.png"
        _write_minimal_png(path)
        failure_points.append("image_path_materialized_minimal_fixture")

    if not path.is_file():
        failure_points.append("image_path_unreadable")
        return {}, failure_points

    pkg = {
        "frame_input_id": frame_input_id,
        "image_path": str(path.resolve()),
        "frame_ref": frame_ref,
        "frame_width": int(frame_width),
        "frame_height": int(frame_height),
        "timestamp": timestamp,
        "camera_ref": camera_ref,
        "source_ref": source_ref,
        "test_case_id": test_case_id,
        "expected_scene_notes": expected_scene_notes,
        "candidate_only": True,
    }
    return pkg, failure_points
