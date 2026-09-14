# -*- coding: utf-8 -*-
"""ROI-local OCR geometry → original image coordinates (Phase-OCR-ROI-Evidence-Coordinate-Lift-001)."""

from __future__ import annotations

import copy
import json
from typing import Any, Dict, List, Optional, Tuple

LIFT_MODE_ROI_CROP = "roi_crop"


def normalize_local_polygon_v0(poly: Any) -> Optional[List[List[float]]]:
    """RapidOCR-style quad: ``[[x,y], ...]`` with at least 3 points."""
    if poly is None:
        return None
    if not isinstance(poly, (list, tuple)):
        return None
    pts: List[List[float]] = []
    for p in poly:
        if not isinstance(p, (list, tuple)) or len(p) < 2:
            return None
        try:
            pts.append([float(p[0]), float(p[1])])
        except (TypeError, ValueError):
            return None
    if len(pts) < 3:
        return None
    return pts


def local_bbox_xyxy_from_polygon_v0(pts: List[List[float]]) -> List[float]:
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return [round(min(xs), 4), round(min(ys), 4), round(max(xs), 4), round(max(ys), 4)]


def lift_point_to_original_v0(x: float, y: float, transform: Dict[str, Any]) -> Tuple[float, float]:
    """``original = offset + local / scale`` (local = resized ROI crop pixels)."""
    ox = float(transform.get("offset_x") or 0.0)
    oy = float(transform.get("offset_y") or 0.0)
    sx = float(transform.get("scale_x") or 1.0)
    sy = float(transform.get("scale_y") or 1.0)
    if sx == 0.0:
        sx = 1.0
    if sy == 0.0:
        sy = 1.0
    return round(ox + float(x) / sx, 4), round(oy + float(y) / sy, 4)


def lift_bbox_xyxy_to_original_v0(bbox: List[float], transform: Dict[str, Any]) -> List[float]:
    x0, y0, x1, y1 = float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
    c00 = lift_point_to_original_v0(x0, y0, transform)
    c01 = lift_point_to_original_v0(x0, y1, transform)
    c10 = lift_point_to_original_v0(x1, y0, transform)
    c11 = lift_point_to_original_v0(x1, y1, transform)
    xs = [c00[0], c01[0], c10[0], c11[0]]
    ys = [c00[1], c01[1], c10[1], c11[1]]
    bb = [min(xs), min(ys), max(xs), max(ys)]
    return [round(bb[0], 4), round(bb[1], 4), round(bb[2], 4), round(bb[3], 4)]


def should_apply_roi_coordinate_lift_v0(input_pack: Optional[Dict[str, Any]]) -> bool:
    if not isinstance(input_pack, dict):
        return False
    pol = input_pack.get("processing_policy") if isinstance(input_pack.get("processing_policy"), dict) else {}
    if str(pol.get("strategy") or "") not in ("roi", "roi_list"):
        return False
    units = input_pack.get("input_units")
    if not isinstance(units, list) or not units:
        return False
    return all(isinstance(u, dict) and str(u.get("unit_type") or "") == "roi" for u in units)


def _unit_transform_dict_v0(unit: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    raw = unit.get("coordinate_transform")
    if isinstance(raw, dict):
        d = raw
    elif isinstance(raw, str) and raw.strip():
        try:
            o = json.loads(raw)
            d = o if isinstance(o, dict) else {}
        except json.JSONDecodeError:
            return None
    else:
        return None
    if str(d.get("mode") or "") != LIFT_MODE_ROI_CROP:
        return None
    for k in ("offset_x", "offset_y", "scale_x", "scale_y"):
        if k not in d:
            return None
    return d


def _roi_unit_and_transform(input_pack: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    tf = input_pack.get("coordinate_transform") if isinstance(input_pack.get("coordinate_transform"), dict) else None
    units = input_pack.get("input_units") if isinstance(input_pack.get("input_units"), list) else None
    if not tf or not units or not isinstance(units[0], dict):
        return None, None
    u0 = units[0]
    if str(tf.get("mode") or "") != LIFT_MODE_ROI_CROP:
        return None, None
    for k in ("offset_x", "offset_y", "scale_x", "scale_y"):
        if k not in tf:
            return None, None
    return u0, tf


def enrich_text_items_multi_roi_lift_v0(
    text_items: List[Any],
    *,
    input_pack: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    report: Dict[str, Any] = {
        "roi_coordinate_lift_applied": False,
        "provider_geometry_available": False,
        "original_geometry_recorded": False,
        "provider_geometry_unavailable": False,
    }
    units_in = input_pack.get("input_units") if isinstance(input_pack.get("input_units"), list) else []
    if not units_in:
        report["coordinate_lift_skipped"] = "missing_input_units"
        out = [dict(x) for x in text_items if isinstance(x, dict)]
        return out, report

    by_ref: Dict[str, Dict[str, Any]] = {}
    by_uid: Dict[str, Dict[str, Any]] = {}
    for u in units_in:
        if not isinstance(u, dict):
            continue
        ref = str(u.get("image_ref") or "")
        uid = str(u.get("unit_id") or "")
        if ref:
            by_ref[ref] = u
        if uid:
            by_uid[uid] = u

    out: List[Dict[str, Any]] = []
    any_local = False
    any_lifted = False
    any_original = False

    for raw in text_items:
        if not isinstance(raw, dict):
            continue
        it = dict(raw)
        u: Optional[Dict[str, Any]] = None
        ref = str(it.get("source_unit_ref") or "")
        if ref and ref in by_ref:
            u = by_ref[ref]
        uid = str(it.get("unit_id") or "")
        if u is None and uid and uid in by_uid:
            u = by_uid[uid]

        if u is None:
            it.setdefault("coordinate_lift_applied", False)
            it.setdefault("no_provider_geometry", True)
            out.append(it)
            continue

        tf = _unit_transform_dict_v0(u)
        roi_bbox = u.get("bbox_in_original")
        if tf is None or not isinstance(roi_bbox, list) or len(roi_bbox) != 4:
            it.setdefault("coordinate_lift_applied", False)
            it.setdefault("no_provider_geometry", True)
            out.append(it)
            continue

        source_unit_ref = str(u.get("image_ref") or u.get("unit_id") or "")
        poly_src = it.get("local_polygon") if it.get("local_polygon") is not None else it.get("polygon")
        pts = normalize_local_polygon_v0(poly_src)
        local_bbox: Optional[List[float]] = None
        local_polygon: Optional[List[List[float]]] = None
        if pts:
            local_polygon = pts
            local_bbox = local_bbox_xyxy_from_polygon_v0(pts)
            any_local = True
        elif isinstance(it.get("local_bbox"), list) and len(it.get("local_bbox")) == 4:
            try:
                local_bbox = [float(x) for x in it["local_bbox"]]  # type: ignore[arg-type]
                any_local = True
            except (TypeError, ValueError):
                local_bbox = None

        it["local_bbox"] = local_bbox
        it["local_polygon"] = local_polygon
        it["roi_bbox_in_original"] = [int(float(roi_bbox[i])) for i in range(4)]
        it["source_unit_ref"] = source_unit_ref
        it["unit_id"] = it.get("unit_id") or u.get("unit_id")
        it["roi_id"] = it.get("roi_id") or u.get("roi_id")

        if local_polygon is not None:
            orig_poly = [list(lift_point_to_original_v0(p[0], p[1], tf)) for p in local_polygon]
            it["original_polygon"] = orig_poly
            it["original_bbox"] = local_bbox_xyxy_from_polygon_v0(orig_poly)
            it["coordinate_lift_applied"] = True
            any_lifted = True
            any_original = True
        elif local_bbox is not None:
            it["original_bbox"] = lift_bbox_xyxy_to_original_v0(local_bbox, tf)
            it["original_polygon"] = None
            it["coordinate_lift_applied"] = True
            any_lifted = True
            any_original = True
        else:
            it["original_polygon"] = None
            it["original_bbox"] = None
            it["coordinate_lift_applied"] = False
            it["no_provider_geometry"] = True

        out.append(it)

    report["provider_geometry_available"] = bool(any_local)
    report["roi_coordinate_lift_applied"] = bool(any_lifted)
    report["original_geometry_recorded"] = bool(any_original)
    report["provider_geometry_unavailable"] = bool(len(out) > 0 and not any_local)
    return out, report


def enrich_text_items_with_roi_lift_v0(
    text_items: List[Any],
    *,
    input_pack: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Returns (enriched_items, lift_audit_fragment).

    Never fabricates original geometry: without valid local polygon/bbox from provider, originals stay null.
    """
    pol = input_pack.get("processing_policy") if isinstance(input_pack.get("processing_policy"), dict) else {}
    if str(pol.get("strategy") or "") == "roi_list":
        return enrich_text_items_multi_roi_lift_v0(text_items, input_pack=input_pack)

    u0, tf = _roi_unit_and_transform(input_pack)
    report: Dict[str, Any] = {
        "roi_coordinate_lift_applied": False,
        "provider_geometry_available": False,
        "original_geometry_recorded": False,
        "provider_geometry_unavailable": False,
    }
    if u0 is None or tf is None:
        report["coordinate_lift_skipped"] = "missing_roi_transform_or_mode"
        out = [dict(x) for x in text_items if isinstance(x, dict)]
        any_local = any(
            normalize_local_polygon_v0(d.get("local_polygon") if d.get("local_polygon") is not None else d.get("polygon")) is not None
            or (isinstance(d.get("local_bbox"), list) and len(d.get("local_bbox") or []) == 4)
            for d in out
        )
        report["provider_geometry_available"] = bool(any_local)
        report["provider_geometry_unavailable"] = bool(len(out) > 0 and not any_local)
        return out, report

    roi_bbox = u0.get("bbox_in_original")
    if not isinstance(roi_bbox, list) or len(roi_bbox) != 4:
        report["coordinate_lift_skipped"] = "invalid_roi_bbox_in_original"
        out = [dict(x) for x in text_items if isinstance(x, dict)]
        any_local = any(
            normalize_local_polygon_v0(d.get("local_polygon") if d.get("local_polygon") is not None else d.get("polygon")) is not None
            or (isinstance(d.get("local_bbox"), list) and len(d.get("local_bbox") or []) == 4)
            for d in out
        )
        report["provider_geometry_available"] = bool(any_local)
        report["provider_geometry_unavailable"] = bool(len(out) > 0 and not any_local)
        return out, report

    source_unit_ref = str(u0.get("image_ref") or u0.get("unit_id") or "")

    out: List[Dict[str, Any]] = []
    any_local = False
    any_lifted = False
    any_original = False

    for raw in text_items:
        if not isinstance(raw, dict):
            continue
        it = dict(raw)
        poly_src = it.get("local_polygon") if it.get("local_polygon") is not None else it.get("polygon")
        pts = normalize_local_polygon_v0(poly_src)
        local_bbox: Optional[List[float]] = None
        local_polygon: Optional[List[List[float]]] = None
        if pts:
            local_polygon = pts
            local_bbox = local_bbox_xyxy_from_polygon_v0(pts)
            any_local = True
        elif isinstance(it.get("local_bbox"), list) and len(it.get("local_bbox")) == 4:
            try:
                local_bbox = [float(x) for x in it["local_bbox"]]  # type: ignore[arg-type]
                any_local = True
            except (TypeError, ValueError):
                local_bbox = None

        it["local_bbox"] = local_bbox
        it["local_polygon"] = local_polygon
        it["roi_bbox_in_original"] = [int(float(roi_bbox[i])) for i in range(4)]
        it["source_unit_ref"] = source_unit_ref

        if local_polygon is not None:
            orig_poly = [list(lift_point_to_original_v0(p[0], p[1], tf)) for p in local_polygon]
            it["original_polygon"] = orig_poly
            it["original_bbox"] = local_bbox_xyxy_from_polygon_v0(orig_poly)
            it["coordinate_lift_applied"] = True
            any_lifted = True
            any_original = True
        elif local_bbox is not None:
            it["original_bbox"] = lift_bbox_xyxy_to_original_v0(local_bbox, tf)
            it["original_polygon"] = None
            it["coordinate_lift_applied"] = True
            any_lifted = True
            any_original = True
        else:
            it["original_polygon"] = None
            it["original_bbox"] = None
            it["coordinate_lift_applied"] = False
            it["no_provider_geometry"] = True

        out.append(it)

    report["provider_geometry_available"] = bool(any_local)
    report["roi_coordinate_lift_applied"] = bool(any_lifted)
    report["original_geometry_recorded"] = bool(any_original)
    report["provider_geometry_unavailable"] = bool(len(out) > 0 and not any_local)
    return out, report


def apply_roi_coordinate_lift_to_provider_result_v0(
    provider_out: Dict[str, Any],
    input_pack: Optional[Dict[str, Any]],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Deep-copy provider_out, replace ``text_items`` when ROI lift applies; always returns lift report (possibly empty)."""
    empty_report: Dict[str, Any] = {
        "roi_coordinate_lift_applied": False,
        "provider_geometry_available": False,
        "original_geometry_recorded": False,
        "provider_geometry_unavailable": False,
    }
    if not isinstance(provider_out, dict) or not should_apply_roi_coordinate_lift_v0(input_pack):
        return provider_out, empty_report

    pack = input_pack if isinstance(input_pack, dict) else {}
    items_in = provider_out.get("text_items") if isinstance(provider_out.get("text_items"), list) else []
    enriched, report = enrich_text_items_with_roi_lift_v0(items_in, input_pack=pack)

    out = copy.deepcopy(provider_out)
    out["text_items"] = enriched
    if enriched:
        out["text_joined"] = " | ".join(str(x.get("text") or "") for x in enriched if str(x.get("text") or "").strip())
    return out, report


def merge_roi_lift_audit_v0(audit: Dict[str, Any], lift_report: Dict[str, Any]) -> None:
    for k in (
        "roi_coordinate_lift_applied",
        "provider_geometry_available",
        "original_geometry_recorded",
        "provider_geometry_unavailable",
        "coordinate_lift_skipped",
    ):
        if k in lift_report:
            audit[k] = lift_report[k]
