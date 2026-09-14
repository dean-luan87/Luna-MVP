# -*- coding: utf-8 -*-
"""Lightweight real OCR input constraints — Phase-OCR-Lightweight-Real-Provider-Adapter-001."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple

LIGHTWEIGHT_ALLOWED_UNIT_TYPES = frozenset({"full_image", "downscaled_full_image", "roi"})


def lightweight_max_edge_px_v0() -> int:
    return max(64, int(os.environ.get("LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX", "512")))


def evaluate_lightweight_provider_input_pack_v0(input_pack: Optional[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Non-tile packs; single full/downscale unit **or** multiple ``roi`` units when ``strategy=roi_list``."""
    reasons: List[str] = []
    if not isinstance(input_pack, dict):
        return False, ["input_pack_not_dict"]
    pol = input_pack.get("processing_policy") if isinstance(input_pack.get("processing_policy"), dict) else {}
    if str(pol.get("strategy") or "") == "tile":
        return False, ["lightweight_rejects_tile_strategy"]
    strategy = str(pol.get("strategy") or "")
    units = input_pack.get("input_units")
    if not isinstance(units, list) or len(units) < 1:
        return False, ["lightweight_requires_at_least_one_input_unit"]
    if strategy == "roi_list":
        if len(units) < 2:
            return False, ["roi_list_requires_at_least_two_input_units"]
        for u in units:
            if not isinstance(u, dict):
                return False, ["input_unit_not_dict"]
            if str(u.get("unit_type") or "") != "roi":
                return False, [f"roi_list_requires_roi_unit:{u.get('unit_id') or 'unknown'}"]
    else:
        if len(units) != 1:
            return False, ["lightweight_requires_exactly_one_input_unit"]
        u = units[0]
        if not isinstance(u, dict):
            return False, ["input_unit_not_dict"]
        ut = str(u.get("unit_type") or "")
        if ut == "tile":
            return False, ["lightweight_rejects_tile_unit"]
        if ut not in LIGHTWEIGHT_ALLOWED_UNIT_TYPES:
            return False, [f"unsupported_unit_type:{ut or 'empty'}"]

    cap = lightweight_max_edge_px_v0()
    for u in units:
        if not isinstance(u, dict):
            return False, ["input_unit_not_dict"]
        if strategy != "roi_list":
            ut = str(u.get("unit_type") or "")
            if ut == "tile":
                return False, ["lightweight_rejects_tile_unit"]
            if ut not in LIGHTWEIGHT_ALLOWED_UNIT_TYPES:
                return False, [f"unsupported_unit_type:{ut or 'empty'}"]
        w, h = int(u.get("width") or 0), int(u.get("height") or 0)
        if w <= 0 or h <= 0:
            return False, ["invalid_unit_dimensions"]
        if w > cap or h > cap:
            return False, [f"edge_exceeds_lightweight_cap:{cap}_got_{w}x{h}"]
        ir = str(u.get("image_ref") or "").strip()
        if not ir.startswith("/"):
            return False, ["image_ref_must_be_absolute"]
    return True, []
