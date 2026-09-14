# -*- coding: utf-8 -*-
"""Stub OCR provider — no real OCR; consumes OCRProviderInputPack when provided."""

from __future__ import annotations

import json
import os
from collections import Counter
from typing import Any, Dict, List, Optional


def _parse_ct(unit: Dict[str, Any]) -> Dict[str, Any]:
    raw = unit.get("coordinate_transform")
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            o = json.loads(raw)
            return o if isinstance(o, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


def _local_to_original_polygon(local_quad: List[List[float]], ct: Dict[str, Any]) -> List[List[float]]:
    ox = float(ct.get("offset_x") or 0)
    oy = float(ct.get("offset_y") or 0)
    sx = float(ct.get("scale_x") or 1.0)
    sy = float(ct.get("scale_y") or 1.0)
    out: List[List[float]] = []
    for pt in local_quad:
        if len(pt) < 2:
            continue
        lx, ly = float(pt[0]), float(pt[1])
        out.append([round(ox + lx * sx, 4), round(oy + ly * sy, 4)])
    return out


def _build_tile_stub_text_items(units: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for idx, unit in enumerate(units):
        if not isinstance(unit, dict) or unit.get("unit_type") != "tile":
            continue
        uid = str(unit.get("unit_id") or f"tile_{idx}")
        w = int(unit.get("width") or 0)
        h = int(unit.get("height") or 0)
        ct = _parse_ct(unit)
        local_bbox = [0, 0, w, h]
        orig_bb = unit.get("bbox_in_original")
        if not isinstance(orig_bb, list) or len(orig_bb) != 4:
            orig_bb = [
                int(ct.get("offset_x") or 0),
                int(ct.get("offset_y") or 0),
                int(ct.get("offset_x") or 0) + w,
                int(ct.get("offset_y") or 0) + h,
            ]
        local_poly = [[0.0, 0.0], [float(w), 0.0], [float(w), float(h)], [0.0, float(h)]]
        orig_poly = _local_to_original_polygon(local_poly, ct)
        items.append(
            {
                "tile_id": uid,
                "unit_id": uid,
                "text": f"MOCK_TEXT_TILE_{idx}",
                "score": 1.0,
                "local_bbox": local_bbox,
                "original_bbox": [int(x) for x in orig_bb] if all(isinstance(x, (int, float)) for x in orig_bb) else orig_bb,
                "local_polygon": local_poly,
                "original_polygon": orig_poly,
                "coordinate_transform_applied": True,
                "source_unit_ref": uid,
            }
        )
    return items


def run_ocr_provider_stub_v0(
    *,
    trace_id: str,
    request_id: str,
    input_pack: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    mode = (os.environ.get("LUNA_OCR_STUB_MODE") or "success").strip().lower()
    base: Dict[str, Any] = {
        "provider": "ocr_stub",
        "stub_mode": mode,
        "trace_id": trace_id,
        "request_id": request_id,
    }
    if input_pack:
        base["input_pack_id"] = input_pack.get("pack_id")
        units = input_pack.get("input_units") if isinstance(input_pack.get("input_units"), list) else []
        base["input_unit_count"] = len(units)
        if units and isinstance(units[0], dict):
            base["first_unit_type"] = units[0].get("unit_type")
            base["first_unit_id"] = units[0].get("unit_id")
        base["unit_type_counts"] = dict(Counter(str(u.get("unit_type") or "") for u in units if isinstance(u, dict)))

    pol = input_pack.get("processing_policy") if isinstance(input_pack, dict) and isinstance(input_pack.get("processing_policy"), dict) else {}
    units_list = input_pack.get("input_units") if isinstance(input_pack, dict) and isinstance(input_pack.get("input_units"), list) else []
    use_tile_stub = (
        isinstance(input_pack, dict)
        and str(pol.get("strategy") or "") == "tile"
        and units_list
        and all(isinstance(u, dict) and u.get("unit_type") == "tile" for u in units_list)
    )
    use_multi_roi_stub = (
        isinstance(input_pack, dict)
        and str(pol.get("strategy") or "") == "roi_list"
        and len(units_list) >= 2
        and all(isinstance(u, dict) and u.get("unit_type") == "roi" for u in units_list)
    )

    text_items: List[Dict[str, Any]]
    if use_tile_stub:
        text_items = _build_tile_stub_text_items(units_list)
    elif use_multi_roi_stub:
        text_items = []
        for idx, u in enumerate(units_list):
            if not isinstance(u, dict):
                continue
            rid = str(u.get("roi_id") or f"roi_{idx:03d}")
            text_items.append(
                {
                    "text": f"MOCK_TEXT_{rid}",
                    "score": 1.0,
                    "polygon": None,
                    "unit_id": str(u.get("unit_id") or ""),
                    "roi_id": rid,
                    "source_unit_ref": str(u.get("image_ref") or ""),
                }
            )
    else:
        text_items = [{"text": "MOCK_TEXT", "score": 1.0, "polygon": None}]

    if mode == "empty":
        text_items = []
        base["text_items"] = text_items
        base["text_joined"] = ""
        base["status"] = "empty"
        return base
    if mode == "error":
        base["text_items"] = []
        base["text_joined"] = ""
        base["status"] = "error"
        base["error"] = "stub_simulated_error"
        return base
    if mode == "timeout":
        base["text_items"] = text_items
        base["text_joined"] = " | ".join(str(x.get("text") or "") for x in text_items) if text_items else ""
        base["status"] = "timeout"
        base["error"] = "stub_simulated_timeout"
        return base

    base["text_items"] = text_items
    base["text_joined"] = " | ".join(str(x.get("text") or "") for x in text_items) if text_items else ""
    if use_tile_stub:
        base["tile_evidence_items"] = list(text_items)
    base["status"] = "success"
    return base
