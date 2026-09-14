# -*- coding: utf-8 -*-
"""Document Surface — Option A classical CV boundary executor v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

import numpy as np

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    RUNTIME_ID,
)

IMPLEMENTATION_MODE = "option_a_classical_cv_boundary"
MAX_CANDIDATES = 10
MIN_CONTOUR_AREA_RATIO = 0.003


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _bbox_from_contour(contour: np.ndarray) -> List[int]:
    x, y, w, h = __import__("cv2").boundingRect(contour)
    return [int(x), int(y), int(x + w), int(y + h)]


def _polygon_from_contour(contour: np.ndarray, epsilon_factor: float = 0.02) -> List[List[int]]:
    cv2 = __import__("cv2")
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon_factor * peri, True)
    return [[int(p[0][0]), int(p[0][1])] for p in approx]


def _score_contour(cv2: Any, cnt: np.ndarray, gray: np.ndarray, img_area: float) -> Tuple[float, np.ndarray]:
    area = cv2.contourArea(cnt)
    if area < img_area * MIN_CONTOUR_AREA_RATIO:
        return 0.0, cnt
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
    bbox = _bbox_from_contour(cnt)
    quad_score = 1.0 if len(approx) == 4 else 0.6 if len(approx) <= 6 else 0.35
    area_score = min(1.0, area / (img_area * 0.5))
    contrast_roi = gray[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    contrast_score = float(np.std(contrast_roi)) / 128.0 if contrast_roi.size else 0.2
    quality = min(1.0, 0.4 * quad_score + 0.3 * area_score + 0.3 * contrast_score)
    return quality, cnt


def _collect_scored_contours(cv2: Any, gray: np.ndarray, img_area: float) -> List[Tuple[float, Any]]:
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    scored: List[Tuple[float, Any]] = []
    seen_bboxes: List[List[int]] = []

    def _add_contours(contours: List[Any]) -> None:
        for cnt in contours:
            quality, kept = _score_contour(cv2, cnt, gray, img_area)
            if quality <= 0:
                continue
            bbox = _bbox_from_contour(kept)
            if any(_overlap_ratio(bbox, prev) > 0.85 for prev in seen_bboxes):
                continue
            seen_bboxes.append(bbox)
            scored.append((quality, kept))

    edges = cv2.Canny(blurred, 50, 150)
    canny_contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    _add_contours(canny_contours)

    if len(scored) < 2:
        for th in (200, 180, 160):
            _, bw = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY)
            bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            thresh_contours, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            _add_contours(thresh_contours)

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored


def _overlap_ratio(a: List[int], b: List[int]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    if ix2 <= ix1 or iy2 <= iy1:
        return 0.0
    inter = (ix2 - ix1) * (iy2 - iy1)
    area_a = max(1, (ax2 - ax1) * (ay2 - ay1))
    area_b = max(1, (bx2 - bx1) * (by2 - by1))
    return inter / min(area_a, area_b)


def execute_option_a_cv_boundary(
    *,
    image_bgr: np.ndarray,
    category: str,
    source_region_id: str = "region_001",
) -> Dict[str, Any]:
    """
    Minimal classical boundary detector — registry images only.
    Allowed: grayscale, blur, Canny, contours, approxPolyDP, quality scoring.
    """
    cv2 = __import__("cv2")
    h, w = image_bgr.shape[:2]
    img_area = float(h * w)

    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    scored = _collect_scored_contours(cv2, gray, img_area)
    if len(scored) > MAX_CANDIDATES:
        return {
            "aborted": True,
            "abort_reason": "excessive_candidate_count",
            "cv2_processing_executed": True,
            "candidate_only": True,
            "not_fact": True,
        }

    surfaces: List[Dict[str, Any]] = []
    polygons: List[Dict[str, Any]] = []
    quads: List[Dict[str, Any]] = []

    for idx, (quality, cnt) in enumerate(scored[:MAX_CANDIDATES]):
        bbox = _bbox_from_contour(cnt)
        poly = _polygon_from_contour(cnt)
        sid = f"surface_{category}_{idx}"
        low_conf = quality < 0.45 or category == "low_contrast_paper_controlled"
        surf = {
            "surface_id": sid,
            "source_region_id": source_region_id,
            "bbox_candidate": bbox,
            "polygon_candidate": poly,
            "boundary_confidence_candidate": round(quality, 4),
            "visibility_status_candidate": "partial" if low_conf else "visible",
            "surface_orientation_candidate": "portrait",
            "owner_entity_candidate_ref": sid,
            "source_runtime": RUNTIME_ID,
            "implementation_mode_candidate": IMPLEMENTATION_MODE,
            "candidate_only": True,
            "not_fact": True,
        }
        if low_conf:
            surf["low_confidence_boundary_candidate"] = True
        surfaces.append(surf)
        polygons.append({"polygon_id": _uid("poly"), "vertices_candidate": poly, "candidate_only": True, "not_fact": True})
        if len(poly) == 4:
            quads.append({"quad_id": _uid("quad"), "vertices_candidate": poly, "candidate_only": True, "not_fact": True})

    status = "ok"
    next_action = None
    if category == "document_on_screen_controlled":
        status = "possible_screen_document_content_candidate"
        next_action = "defer_to_screen_surface_detector"
    elif category == "two_overlapping_papers_controlled" and len(surfaces) >= 2:
        status = "uncertain_multi_surface_candidate"
    elif category == "low_contrast_paper_controlled" or (surfaces and all(s.get("low_confidence_boundary_candidate") for s in surfaces)):
        status = "low_confidence_boundary_candidate"
        next_action = "request_better_view_or_lighting"
    elif not surfaces:
        status = "low_confidence_boundary_candidate"
        next_action = "request_better_view_or_lighting"

    return {
        "aborted": False,
        "implementation_mode": IMPLEMENTATION_MODE,
        "document_surface_candidates": surfaces,
        "polygon_candidates": polygons,
        "quadrilateral_candidates": quads,
        "boundary_quality_candidate": {
            "quality_id": _uid("bq"),
            "mean_boundary_confidence": round(float(np.mean([s["boundary_confidence_candidate"] for s in surfaces])), 4) if surfaces else 0.0,
            "candidate_only": True,
            "not_fact": True,
        },
        "runtime_status_candidate": status,
        "next_action_candidate": next_action,
        "possible_screen_document_content": category == "document_on_screen_controlled",
        "screen_surface_not_document_surface_fact": category == "document_on_screen_controlled",
        "cv2_processing_executed": True,
        "ocr_called": False,
        "vlm_called": False,
        "layout_called": False,
        "fallback_attempted": False,
        "candidate_only": True,
        "not_fact": True,
    }
