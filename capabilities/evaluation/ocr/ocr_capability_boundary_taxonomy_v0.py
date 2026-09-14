# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-006 — OCR capability boundary taxonomy v0 (Evaluation Tools).

Defines:
- content type taxonomy
- quality perturbation profiles
- expected routing labels (evaluation-only)
- boundary test case schema
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, List, Literal, Optional


OcrContentType = Literal[
    "zh_plain_text",
    "zh_traditional_text",
    "en_plain_text",
    "digits",
    "symbols_and_punctuation",
    "mixed_zh_en_digit",
    "artistic_text",
    "stylized_digits",
    "icon_text_mix",
    "multi_panel_layout",
    "product_label",
    "signboard",
    "document_text",
    "vertical_text",
    "multi_line_text",
    "handwritten_style",
    "low_quality_text",
    "decorative_graphic_non_text",
]


SizeScale = Literal[
    "tiny_text",
    "small_text",
    "normal_text",
    "large_text",
    "oversized_image_small_text",
]
BlurLevel = Literal["none", "mild", "medium", "heavy"]
ContrastLevel = Literal["high", "normal", "low", "very_low"]
BrightnessLevel = Literal["normal", "underexposed", "overexposed"]
CompressionLevel = Literal["none_png", "mild_jpeg", "heavy_jpeg"]
BackgroundType = Literal["white", "textured", "photo_background", "gradient", "noisy"]
LayoutComplexity = Literal["single_line", "multi_line", "multi_column", "grid", "artistic_order", "mixed_icon_text"]


@dataclasses.dataclass(frozen=True)
class OcrQualityPerturbationV0:
    size_scale: SizeScale
    blur: BlurLevel
    contrast: ContrastLevel
    brightness: BrightnessLevel
    compression: CompressionLevel
    skew_angle: int  # degrees
    background: BackgroundType
    layout_complexity: LayoutComplexity


OcrExpectedRouting = Literal[
    "rapidocr_primary",
    "paddleocr_candidate",
    "cnocr_candidate",
    "ocr_vl_candidate",
    "layout_branch",
    "visual_symbol_branch",
    "visual_glyph_branch",
    "reject_low_quality",
    "manual_review",
]


@dataclasses.dataclass(frozen=True)
class OcrExpectedMetricsV0:
    cer_max: float
    chinese_recall_min: Optional[float]
    empty_output_allowed: bool
    garbled_score_max: float


@dataclasses.dataclass(frozen=True)
class OcrBoundaryTestCaseV0:
    case_id: str
    content_type: OcrContentType
    language: str  # zh/en/mixed
    text: str
    quality_profile: OcrQualityPerturbationV0
    expected_ocr_route: OcrExpectedRouting
    expected_metrics: OcrExpectedMetricsV0
    expected_failure_mode: Optional[str]
    ground_truth_text: str
    should_enter_mainline_ocr: bool
    should_enter_layout_branch: bool
    should_enter_symbol_branch: bool
    should_enter_glyph_branch: bool
    generation_status: str = "generated"  # generated | manual_sample_required


def testcase_to_dict_v0(tc: OcrBoundaryTestCaseV0) -> Dict[str, Any]:
    d = dataclasses.asdict(tc)
    d["quality_profile"] = dataclasses.asdict(tc.quality_profile)
    d["expected_metrics"] = dataclasses.asdict(tc.expected_metrics)
    return d


def build_default_expected_metrics_v0(*, content_type: OcrContentType) -> OcrExpectedMetricsV0:
    if content_type in ("zh_plain_text", "mixed_zh_en_digit", "en_plain_text", "digits"):
        return OcrExpectedMetricsV0(cer_max=0.15, chinese_recall_min=0.8, empty_output_allowed=False, garbled_score_max=0.10)
    if content_type in ("symbols_and_punctuation",):
        return OcrExpectedMetricsV0(cer_max=0.35, chinese_recall_min=None, empty_output_allowed=True, garbled_score_max=0.25)
    # hard cases default: allow weaker
    return OcrExpectedMetricsV0(cer_max=0.50, chinese_recall_min=0.5, empty_output_allowed=True, garbled_score_max=0.35)

