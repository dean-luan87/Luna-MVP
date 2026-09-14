# -*- coding: utf-8 -*-
"""Minimal ImageInputGate v0: metadata + size budget only; no OCR, no tile, no downscale."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _read_governance(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _probe_image(path: Path) -> Tuple[Optional[int], Optional[int], Optional[float], Optional[str]]:
    try:
        from PIL import Image

        with Image.open(path) as im:
            im.load()
            w, h = im.size
            mp = round((w * h) / 1_000_000.0, 6)
            return int(w), int(h), float(mp), None
    except Exception as e:
        return None, None, None, f"{type(e).__name__}:{e}"


def run_image_input_gate_v0(
    *,
    image_path: Path,
    governance_config_path: Path,
    allow_full_image: bool,
    enable_normalization_branch: bool = False,
    enable_tile_planner_branch: bool = False,
) -> Dict[str, Any]:
    gov = _read_governance(governance_config_path)
    sl = gov.get("size_limits") if isinstance(gov.get("size_limits"), dict) else {}
    max_w = int(sl.get("max_width_realtime") or 2048)
    max_h = int(sl.get("max_height_realtime") or 2048)
    max_mp = float(sl.get("max_megapixels_realtime") or 4.0)
    mp_tile = float(sl.get("max_megapixels_requires_tiling") or 8.0)

    reason_codes: List[str] = []
    w, h, mp, err = _probe_image(image_path)
    if err:
        return {
            "gate_verdict": "REJECT",
            "oversized": False,
            "width": w,
            "height": h,
            "megapixels": mp,
            "recommended_input_strategy": "downscale_required",
            "reason_codes": ["image_metadata_unreadable", err],
        }

    oversized = bool(w > max_w or h > max_h or (mp is not None and mp > max_mp))
    if oversized and not allow_full_image:
        reason_codes.append("oversized_disallows_full_image")
        reason_codes.append("reject_or_downscale_required")
        ds = gov.get("downscale_policy") if isinstance(gov.get("downscale_policy"), dict) else {}
        downscale_enabled = bool(ds.get("enabled", True))
        if mp is not None and mp >= mp_tile:
            strategy = "tile_required"
            tiling = gov.get("tiling_policy") if isinstance(gov.get("tiling_policy"), dict) else {}
            tiling_enabled = bool(tiling.get("enabled", True))
            if enable_tile_planner_branch and tiling_enabled:
                reason_codes.append("tile_path_selected")
                reason_codes.append("tile_planner_branch_enabled")
                return {
                    "gate_verdict": "CONDITIONAL_ALLOW",
                    "oversized": True,
                    "width": w,
                    "height": h,
                    "megapixels": mp,
                    "recommended_input_strategy": "tile",
                    "reason_codes": reason_codes,
                }
            if enable_normalization_branch and downscale_enabled:
                reason_codes.append("tile_recommended_for_future_pipeline")
                reason_codes.append("downscale_applied_as_minimal_fallback")
                return {
                    "gate_verdict": "CONDITIONAL_ALLOW",
                    "oversized": True,
                    "width": w,
                    "height": h,
                    "megapixels": mp,
                    "recommended_input_strategy": "downscale",
                    "reason_codes": reason_codes,
                }
        else:
            strategy = "downscale_required"
            if enable_normalization_branch and downscale_enabled:
                reason_codes.append("downscale_path_available")
                return {
                    "gate_verdict": "CONDITIONAL_ALLOW",
                    "oversized": True,
                    "width": w,
                    "height": h,
                    "megapixels": mp,
                    "recommended_input_strategy": "downscale",
                    "reason_codes": reason_codes,
                }
        return {
            "gate_verdict": "REJECT",
            "oversized": True,
            "width": w,
            "height": h,
            "megapixels": mp,
            "recommended_input_strategy": strategy,
            "reason_codes": reason_codes,
        }

    if oversized and allow_full_image:
        return {
            "gate_verdict": "CONDITIONAL_ALLOW",
            "oversized": True,
            "width": w,
            "height": h,
            "megapixels": mp,
            "recommended_input_strategy": "full_image_allowed",
            "reason_codes": ["oversized_but_full_image_explicitly_allowed"],
        }

    return {
        "gate_verdict": "ALLOW",
        "oversized": False,
        "width": w,
        "height": h,
        "megapixels": mp,
        "recommended_input_strategy": "roi_only",
        "reason_codes": [],
    }
