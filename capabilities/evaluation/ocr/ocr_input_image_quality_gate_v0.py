# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-004 — OCR Input Image Quality Gate & Pixel Scale Validation v0.

Evaluation Tools only:
- Not runtime / not whitebox
- No MidPlatform/SceneDelta/WorldContext/Qwen/TTS
- Does not invoke OCR providers (pure image stats + heuristics)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ImageQualityGateConfigV0:
    # Image size bounds
    min_width: int = 240
    # Many OCR fixtures/datasets are short but wide (e.g., text strips). Allow lower height.
    min_height: int = 160
    max_width: int = 4096
    max_height: int = 4096
    # Allow smaller megapixels for text-strip datasets; rely on text-scale heuristics too.
    min_megapixels: float = 0.05  # ~ 320x160
    max_megapixels: float = 12.0  # ~ 4000x3000

    # Blur: Laplacian variance thresholds (image-dependent; keep conservative)
    blur_no_go_threshold: float = 25.0
    blur_conditional_threshold: float = 60.0

    # Contrast / brightness thresholds (0..255 grayscale)
    contrast_std_no_go: float = 18.0
    contrast_std_conditional: float = 28.0
    brightness_low: float = 55.0
    # White backgrounds are common for OCR; treat only very bright as overexposed.
    brightness_high: float = 235.0

    # Text-ish heuristics
    text_area_ratio_low: float = 0.01
    text_area_ratio_high: float = 0.65
    min_text_component_height_px: int = 16
    max_text_component_height_px: int = 220

    # Skew angle (degrees)
    skew_conditional_deg: float = 10.0
    skew_no_go_deg: float = 25.0


def _load_image_gray_np(path: str) -> Tuple["Any", int, int]:
    import cv2  # type: ignore

    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("image_read_failed")
    h, w = img.shape[:2]
    return img, int(w), int(h)


def _laplacian_variance(gray: "Any") -> float:
    import cv2  # type: ignore

    lap = cv2.Laplacian(gray, cv2.CV_64F)
    v = float(lap.var())
    return v


def _contrast_std(gray: "Any") -> float:
    import numpy as np  # type: ignore

    return float(np.std(gray))


def _brightness_mean(gray: "Any") -> float:
    import numpy as np  # type: ignore

    return float(np.mean(gray))


def _exposure_status(gray: "Any", mean: float, cfg: ImageQualityGateConfigV0) -> Tuple[str, Dict[str, Any]]:
    """
    Exposure should not be judged by mean alone for OCR.
    We use a weak saturation ratio heuristic:
    - overexposed: too many near-white pixels AND low contrast
    - underexposed: too many near-black pixels AND low contrast
    """
    import numpy as np  # type: ignore

    g = gray
    total = float(g.size) if hasattr(g, "size") else 1.0
    pct_white = float(np.mean(g >= 250))
    pct_black = float(np.mean(g <= 5))
    info = {"pct_near_white": pct_white, "pct_near_black": pct_black, "mean": float(mean)}

    # If almost the entire image saturates, it's a risk.
    if pct_black >= 0.985 and mean < cfg.brightness_low:
        return "underexposed", info
    if pct_white >= 0.985 and mean > cfg.brightness_high:
        return "overexposed", info
    return "normal", info


def _estimate_text_mask(gray: "Any") -> Tuple["Any", float]:
    """
    Approximate text area using adaptive threshold + morphology.
    Returns (binary_mask, text_area_ratio).
    """
    import cv2  # type: ignore
    import numpy as np  # type: ignore

    # Normalize & binarize (dark text on light bg typical; robust-ish to inverse with Otsu + invert check)
    g = gray
    # Otsu threshold
    _, th = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Decide invert by comparing foreground density
    fg_ratio = float(np.mean(th == 0))
    if fg_ratio < 0.15:  # likely dark text => foreground should be small; invert to make text=1
        bin_ = (th == 0).astype(np.uint8)
    else:
        bin_ = (th == 255).astype(np.uint8)

    # Morph close to connect strokes
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    bin_ = cv2.morphologyEx(bin_, cv2.MORPH_CLOSE, k, iterations=1)

    ratio = float(np.mean(bin_ > 0))
    return bin_, ratio


def _estimate_text_component_height_stats(mask: "Any") -> Dict[str, Any]:
    import cv2  # type: ignore
    import numpy as np  # type: ignore

    m = (mask > 0).astype("uint8")
    num, labels, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    heights: List[int] = []
    for i in range(1, int(num)):
        x, y, w, h, area = stats[i].tolist()
        if area < 18:
            continue
        if w < 3 or h < 6:
            continue
        if w > 0.9 * m.shape[1] or h > 0.9 * m.shape[0]:
            continue
        heights.append(int(h))
    if not heights:
        return {"count": 0, "p50": None, "p90": None, "min": None, "max": None}
    hs = np.array(heights, dtype=np.int32)
    return {
        "count": int(len(heights)),
        "p50": float(np.percentile(hs, 50)),
        "p90": float(np.percentile(hs, 90)),
        "min": int(hs.min()),
        "max": int(hs.max()),
    }


def _estimate_skew_angle_deg(gray: "Any") -> Optional[float]:
    """
    Weak skew estimate via Hough lines on Canny edges. Returns absolute dominant angle in degrees.
    """
    import cv2  # type: ignore
    import numpy as np  # type: ignore

    g = gray
    edges = cv2.Canny(g, 80, 180)
    lines = cv2.HoughLinesP(edges, 1, math.pi / 180.0, threshold=100, minLineLength=60, maxLineGap=10)
    if lines is None or len(lines) < 6:
        return None
    angles: List[float] = []
    for ln in lines[:200]:
        x1, y1, x2, y2 = ln[0].tolist()
        dx = float(x2 - x1)
        dy = float(y2 - y1)
        if abs(dx) < 1.0:
            continue
        ang = math.degrees(math.atan2(dy, dx))
        # fold to [-45,45]
        while ang < -45:
            ang += 90
        while ang > 45:
            ang -= 90
        angles.append(ang)
    if not angles:
        return None
    a = np.array(angles, dtype=np.float32)
    med = float(np.median(a))
    return float(abs(med))


def _estimate_jpeg_blockiness(gray: "Any") -> Optional[float]:
    """
    Very weak compression artifact heuristic:
    compare edge strength at 8x8 block boundaries vs non-boundary.
    Returns blockiness_score in [0,1] (higher = more blocky). None if too small.
    """
    import numpy as np  # type: ignore

    h, w = gray.shape[:2]
    if h < 24 or w < 24:
        return None
    g = gray.astype(np.float32)
    # vertical differences
    dv = np.abs(g[:, 1:] - g[:, :-1])
    dh = np.abs(g[1:, :] - g[:-1, :])
    # boundary indices (every 8 pixels)
    vb = [i for i in range(8, w - 1, 8)]
    hb = [i for i in range(8, h - 1, 8)]
    if not vb or not hb:
        return None
    v_boundary = float(np.mean(dv[:, [i - 1 for i in vb]]))
    v_non = float(np.mean(dv))
    h_boundary = float(np.mean(dh[[i - 1 for i in hb], :]))
    h_non = float(np.mean(dh))
    # normalize
    eps = 1e-6
    score = 0.5 * ((v_boundary - v_non) / (v_non + eps) + (h_boundary - h_non) / (h_non + eps))
    # map to [0,1]
    score = max(0.0, min(1.0, 0.5 + 0.25 * score))
    return float(score)


def assess_ocr_input_image_quality_v0(
    *,
    image_path: str,
    cfg: Optional[ImageQualityGateConfigV0] = None,
) -> Dict[str, Any]:
    cfg = cfg or ImageQualityGateConfigV0()
    p = Path(image_path).expanduser()
    out: Dict[str, Any] = {
        "image_path": str(p),
        "image_quality_gate": "NO_GO",
        "recommended_preprocess": [],
        "reason": [],
    }
    if not p.is_file():
        out["reason"].append("missing_image")
        return out

    suffix = p.suffix.lower()
    out["extension"] = suffix
    out["size_bytes"] = int(p.stat().st_size)
    if out["size_bytes"] <= 0:
        out["reason"].append("empty_file")
        return out

    try:
        gray, w, h = _load_image_gray_np(str(p))
    except Exception as e:
        out["reason"].append(f"image_load_failed:{e!r}")
        return out

    mp = float(w * h) / 1_000_000.0
    out["image_width"] = int(w)
    out["image_height"] = int(h)
    out["megapixels"] = float(mp)

    # Basic bounds
    if w < cfg.min_width or h < cfg.min_height or mp < cfg.min_megapixels:
        out["reason"].append("too_small_resolution")
        out["recommended_preprocess"].append("upscale")
    if w > cfg.max_width or h > cfg.max_height or mp > cfg.max_megapixels:
        out["reason"].append("too_large_resolution")
        out["recommended_preprocess"].append("downscale")

    blur = _laplacian_variance(gray)
    out["blur_score"] = float(blur)
    if blur < cfg.blur_no_go_threshold:
        out["reason"].append("too_blurry")
    elif blur < cfg.blur_conditional_threshold:
        out["reason"].append("blurry_risk")

    cstd = _contrast_std(gray)
    out["contrast_score"] = float(cstd)
    if cstd < cfg.contrast_std_no_go:
        out["reason"].append("low_contrast")
    elif cstd < cfg.contrast_std_conditional:
        out["reason"].append("contrast_risk")

    bmean = _brightness_mean(gray)
    out["brightness_mean"] = float(bmean)
    estatus, einfo = _exposure_status(gray, bmean, cfg)
    out["brightness_status"] = estatus
    out["exposure_info"] = einfo
    if out["brightness_status"] in ("underexposed", "overexposed"):
        out["reason"].append(f"brightness_{out['brightness_status']}")

    # Compression artifacts (mainly meaningful for jpeg)
    blockiness = None
    if suffix in (".jpg", ".jpeg"):
        blockiness = _estimate_jpeg_blockiness(gray)
    out["compression_artifact_score"] = blockiness
    if blockiness is not None and blockiness >= 0.72:
        out["reason"].append("compression_artifact_high")

    mask, text_ratio = _estimate_text_mask(gray)
    out["text_area_ratio"] = float(text_ratio)
    if text_ratio < cfg.text_area_ratio_low:
        out["reason"].append("text_area_ratio_too_low")
        out["recommended_preprocess"].append("crop_required")
    elif text_ratio > cfg.text_area_ratio_high:
        out["reason"].append("text_area_ratio_too_high")

    comp_stats = _estimate_text_component_height_stats(mask)
    out["text_component_height_stats"] = comp_stats
    p50 = comp_stats.get("p50")
    if p50 is None:
        out["text_scale_status"] = "unknown"
        out["reason"].append("text_scale_unknown")
    else:
        if float(p50) < float(cfg.min_text_component_height_px):
            out["text_scale_status"] = "too_small"
            out["reason"].append("text_scale_too_small")
            out["recommended_preprocess"].append("upscale")
        elif float(p50) > float(cfg.max_text_component_height_px):
            out["text_scale_status"] = "too_large"
            out["reason"].append("text_scale_too_large")
            out["recommended_preprocess"].append("downscale")
        else:
            out["text_scale_status"] = "acceptable"

    skew = _estimate_skew_angle_deg(gray)
    out["skew_angle_deg"] = skew
    if skew is not None:
        if float(skew) >= cfg.skew_no_go_deg:
            out["reason"].append("skew_too_large")
        elif float(skew) >= cfg.skew_conditional_deg:
            out["reason"].append("skew_risk")
            out["recommended_preprocess"].append("deskew")

    # Decide gate
    reasons = list(dict.fromkeys(out["reason"]))  # stable unique
    out["reason"] = reasons
    out["recommended_preprocess"] = sorted(set([str(x) for x in out["recommended_preprocess"] if x]))

    no_go_markers = {
        "missing_image",
        "empty_file",
        "image_load_failed",
        "too_blurry",
        "low_contrast",
        "skew_too_large",
    }
    conditional_markers = {
        "blurry_risk",
        "contrast_risk",
        "brightness_underexposed",
        "brightness_overexposed",
        "compression_artifact_high",
        "text_area_ratio_too_low",
        "text_scale_unknown",
        "text_scale_too_small",
        "text_scale_too_large",
        "skew_risk",
        "too_small_resolution",
        "too_large_resolution",
    }

    def _has_prefix(prefix: str) -> bool:
        return any(str(r).startswith(prefix) for r in reasons)

    if _has_prefix("image_load_failed"):
        out["image_quality_gate"] = "NO_GO"
    elif any(r in no_go_markers for r in reasons):
        out["image_quality_gate"] = "NO_GO"
    elif any(r in conditional_markers for r in reasons):
        out["image_quality_gate"] = "CONDITIONAL_GO"
    else:
        out["image_quality_gate"] = "GO"

    # Scale action (single top-level recommendation)
    if out["image_quality_gate"] == "NO_GO":
        out["scale_action"] = "reject"
    else:
        if "crop_required" in out["recommended_preprocess"]:
            out["scale_action"] = "crop_required"
        elif "upscale" in out["recommended_preprocess"]:
            out["scale_action"] = "upscale"
        elif "downscale" in out["recommended_preprocess"]:
            out["scale_action"] = "downscale"
        else:
            out["scale_action"] = "accept"

    return out

