# -*- coding: utf-8 -*-
"""OCR / Text Model availability checker v1."""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple


def check_ocr_text_availability(
    *,
    matrix: Dict[str, Any],
    case_overrides: Dict[str, Any] | None = None,
    inspect_subtype: str = "ocr",
) -> Tuple[Dict[str, Any], str, List[str]]:
    """Classify OCR/text availability without downloading or installing."""
    avail = copy.deepcopy(matrix)
    if case_overrides:
        avail.update({k: v for k, v in case_overrides.items() if k in avail or k.endswith("_available") or k.endswith("_authorized")})

    warnings: List[str] = []
    ocr = bool(avail.get("local_ocr_available"))
    region = bool(avail.get("local_text_region_available"))
    weights = bool(avail.get("local_weights_available"))
    deps = bool(avail.get("dependencies_available"))
    rapid_cached = bool(avail.get("rapidocr_cached_output_available"))
    paddle_cached = bool(avail.get("paddleocr_cached_output_available"))
    region_cached = bool(avail.get("text_region_cached_output_available"))
    stub = bool(avail.get("adapter_stub_available"))

    runner_ok = ocr or region
    if runner_ok and weights and deps:
        mode = "local_real_model"
    elif runner_ok and not weights:
        mode = "blocked_by_missing_weight"
        warnings.append("missing_weight_no_download")
    elif runner_ok and weights and not deps:
        mode = "blocked_by_missing_dependency"
        warnings.append("missing_dependency_no_install")
    elif inspect_subtype == "rapidocr" and rapid_cached:
        mode = "cached_output"
    elif inspect_subtype == "paddleocr" and paddle_cached:
        mode = "cached_output"
    elif inspect_subtype == "text_region" and region_cached:
        mode = "cached_output"
    elif inspect_subtype == "text_enhancement" and (rapid_cached or paddle_cached):
        mode = "cached_output"
    elif rapid_cached or paddle_cached or region_cached:
        mode = "cached_output"
    elif stub:
        mode = "adapter_stub"
    else:
        mode = "blocked_by_authorization"
        warnings.append("no_execution_path_without_authorization")

    return avail, mode, warnings
