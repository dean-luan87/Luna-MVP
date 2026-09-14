# -*- coding: utf-8 -*-
"""vision_provider_input_pack_v0 builder (stub crops + coordinate transforms)."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Dict, List


PACK_SCHEMA_VERSION = "vision_provider_input_pack_v0"


def build_coordinate_transform_v0(
    *,
    bbox: List[int],
    source_frame_width: int,
    source_frame_height: int,
) -> Dict[str, Any]:
    x1, y1, x2, y2 = (int(v) for v in bbox)
    tw = max(1, x2 - x1)
    th = max(1, y2 - y1)
    return {
        "mode": "frame_roi_crop",
        "offset_x": x1,
        "offset_y": y1,
        "scale_x": 1.0,
        "scale_y": 1.0,
        "source_frame_width": int(source_frame_width),
        "source_frame_height": int(source_frame_height),
        "transformed_width": tw,
        "transformed_height": th,
    }


def build_input_unit_v0(
    *,
    roi: Dict[str, Any],
    crop_image_ref: str,
    frame_w: int,
    frame_h: int,
) -> Dict[str, Any]:
    bbox = list(roi.get("bbox_in_frame") or [])
    return {
        "unit_id": f"unit_{uuid.uuid4().hex[:12]}",
        "unit_type": "frame_roi",
        "roi_id": str(roi.get("roi_id") or ""),
        "bbox_in_frame": bbox,
        "image_ref": crop_image_ref,
        "coordinate_transform": build_coordinate_transform_v0(
            bbox=bbox, source_frame_width=frame_w, source_frame_height=frame_h
        ),
        "task_hint": str(roi.get("task_hint") or "general_context"),
    }


def build_pack_for_frame_v0(
    *,
    pack_id: str,
    source_frame_id: str,
    source_image_ref: str,
    governance_root: str,
    rois: List[Dict[str, Any]],
    crop_refs_by_roi_id: Dict[str, str],
    frame_w: int,
    frame_h: int,
) -> Dict[str, Any]:
    units: List[Dict[str, Any]] = []
    for roi in rois:
        rid = str(roi.get("roi_id") or "")
        crop_path = crop_refs_by_roi_id.get(rid, "")
        units.append(build_input_unit_v0(roi=roi, crop_image_ref=crop_path, frame_w=frame_w, frame_h=frame_h))
    chain = [
        f"frame_input_governance_ref:{governance_root}",
        f"frame_id:{source_frame_id}",
        "roi_proposal_stub_created",
        "roi_crop_generated",
        "coordinate_transform_recorded",
        "vision_provider_input_pack_built",
    ]
    return {
        "schema_version": PACK_SCHEMA_VERSION,
        "pack_id": pack_id,
        "source_frame_id": source_frame_id,
        "source_image_ref": source_image_ref,
        "input_units": units,
        "source_chain": chain,
    }
