# -*- coding: utf-8 -*-
"""
OCR Tile Planner v0 — split oversized images into overlapping tiles with coordinate metadata.

No real OCR. Does not call PaddleOCR / RapidOCR.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from PIL import Image, ImageOps


def _axis_starts(length: int, window: int, overlap_ratio: float) -> List[int]:
    if length <= window:
        return [0]
    step = max(1, int(round(window * (1.0 - float(overlap_ratio)))))
    starts: List[int] = []
    pos = 0
    while pos + window < length:
        starts.append(pos)
        pos += step
    last = max(0, length - window)
    if not starts or starts[-1] != last:
        starts.append(last)
    # de-dupe preserve order
    out: List[int] = []
    seen = set()
    for s in starts:
        if s not in seen:
            out.append(s)
            seen.add(s)
    return out


def _read_tiling_policy(gov: Dict[str, Any]) -> Dict[str, Any]:
    tp = gov.get("tiling_policy") if isinstance(gov.get("tiling_policy"), dict) else {}
    return {
        "tile_max_side": int(tp.get("tile_max_side") or 1600),
        "tile_overlap_ratio": float(tp.get("tile_overlap_ratio") or 0.12),
        "max_tile_count_sync": int(tp.get("max_tile_count_sync") or 4),
        "max_tile_count_async": int(tp.get("max_tile_count_async") or 16),
        "requires_coordinate_reconstruction": bool(tp.get("requires_coordinate_reconstruction", True)),
    }


def prepare_image_for_tiling_v0(image_path: Path, work_dir: Path, decision: Dict[str, Any]) -> Tuple[Path, int, int, List[str]]:
    """EXIF + RGB normalize; save pre_tile_source.png. Returns path, W, H, chain."""
    work_dir.mkdir(parents=True, exist_ok=True)
    chain: List[str] = ["read_source"]
    im = Image.open(image_path)
    im.load()
    if decision.get("exif_transpose_required"):
        im = ImageOps.exif_transpose(im)
        chain.append("exif_transpose")
    if decision.get("rgb_convert_required") or im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
        chain.append("rgba_to_rgb_or_convert")
    out = work_dir / "pre_tile_source.png"
    im.save(out, format="PNG")
    chain.append("write_pre_tile_source_png")
    w, h = im.size
    return out.resolve(), int(w), int(h), chain


def plan_tiles_v0(
    *,
    source_image_path: Path,
    work_dir: Path,
    governance: Dict[str, Any],
    original_width: int,
    original_height: int,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Returns (tile_plan, input_units, per_tile_coordinate_transforms).
    Crops are written under work_dir/tiles/.
    """
    pol = _read_tiling_policy(governance)
    tile_max = max(64, pol["tile_max_side"])
    overlap = min(0.49, max(0.0, pol["tile_overlap_ratio"]))
    max_sync = max(1, pol["max_tile_count_sync"])

    W, H = int(original_width), int(original_height)
    tw = min(W, tile_max)
    th = min(H, tile_max)
    xs = _axis_starts(W, tw, overlap)
    ys = _axis_starts(H, th, overlap)
    raw_positions: List[Tuple[int, int, int, int]] = []
    for yi, y0 in enumerate(ys):
        for xi, x0 in enumerate(xs):
            raw_positions.append((yi, xi, x0, y0))

    truncated = False
    positions = raw_positions
    if len(positions) > max_sync:
        truncated = True
        positions = raw_positions[:max_sync]

    tiles_dir = work_dir / "tiles"
    tiles_dir.mkdir(parents=True, exist_ok=True)

    im = Image.open(source_image_path)
    im.load()
    if im.mode != "RGB":
        im = im.convert("RGB")

    units: List[Dict[str, Any]] = []
    transforms: List[Dict[str, Any]] = []

    for idx, (tile_row, tile_col, x0, y0) in enumerate(positions):
        x1 = x0 + tw
        y1 = y0 + th
        crop = im.crop((x0, y0, x1, y1))
        cw, ch = crop.size
        tile_path = tiles_dir / f"tile_r{tile_row}_c{tile_col}.png"
        crop.save(tile_path, format="PNG")

        ct: Dict[str, Any] = {
            "original_width": W,
            "original_height": H,
            "tile_bbox_in_original": [x0, y0, x1, y1],
            "tile_local_to_original_transform": "translate_scale",
            "offset_x": int(x0),
            "offset_y": int(y0),
            "scale_x": 1.0,
            "scale_y": 1.0,
            "transformed_width": int(cw),
            "transformed_height": int(ch),
        }

        unit: Dict[str, Any] = {
            "unit_id": f"tile_{idx+1:03d}",
            "unit_type": "tile",
            "image_ref": str(tile_path.resolve()),
            "bbox_in_original": [x0, y0, x1, y1],
            "tile_index": idx,
            "tile_row": int(tile_row),
            "tile_col": int(tile_col),
            "overlap_ratio": float(overlap),
            "width": int(cw),
            "height": int(ch),
            "megapixels": round((cw * ch) / 1_000_000.0, 6),
            "scale_ratio": 1.0,
            "coordinate_transform": json.dumps(ct, sort_keys=True),
            "provider_level_hint": "level_1",
            "ocr_allowed": True,
        }
        units.append(unit)
        transforms.append(ct)

    max_async = max(1, pol["max_tile_count_async"])
    covered_regions: List[List[int]] = []
    for u in units:
        bb = u.get("bbox_in_original")
        if isinstance(bb, list) and len(bb) == 4:
            covered_regions.append([int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])])

    uncovered_regions: List[List[int]] = []
    for k in range(len(units), len(raw_positions)):
        yi, xi, x0, y0 = raw_positions[k]
        uncovered_regions.append([int(x0), int(y0), int(x0 + tw), int(y0 + th)])

    raw_count = len(raw_positions)
    mat_count = len(units)
    coverage_complete = bool(raw_count > 0 and mat_count >= raw_count and not truncated)
    truncated_to_budget = bool(truncated)
    wh = float(W * H) if W and H else 1.0
    sum_areas = sum(float((u.get("width") or 0) * (u.get("height") or 0)) for u in units if isinstance(u, dict))
    coverage_ratio_estimate = round(min(1.0, sum_areas / wh), 6) if wh else 0.0

    async_completion_available = bool(truncated_to_budget and max_async > mat_count)

    tile_plan: Dict[str, Any] = {
        "schema_version": "ocr_tile_plan_v0",
        "original_width": W,
        "original_height": H,
        "tile_max_side": tile_max,
        "tile_overlap_ratio": overlap,
        "tile_window_width": tw,
        "tile_window_height": th,
        "axis_starts_x": xs,
        "axis_starts_y": ys,
        "raw_tile_count": raw_count,
        "materialized_tile_count": mat_count,
        "truncated_to_max_tile_count_sync": truncated,
        "truncated_to_budget": truncated_to_budget,
        "max_tile_count_applied": max_sync,
        "tile_budget_type": "sync",
        "coverage_complete": coverage_complete,
        "coverage_ratio_estimate": coverage_ratio_estimate,
        "coverage_ratio_method": "sum_of_materialized_tile_areas_over_image_area_capped",
        "covered_regions": covered_regions,
        "uncovered_regions": uncovered_regions,
        "requires_coordinate_reconstruction": pol["requires_coordinate_reconstruction"],
        "async_completion_available": async_completion_available,
    }
    return tile_plan, units, transforms
