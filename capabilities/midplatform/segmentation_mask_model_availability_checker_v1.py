# -*- coding: utf-8 -*-
"""Segmentation / Mask Model availability checker v1."""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple


def check_segmentation_mask_availability(
    *,
    matrix: Dict[str, Any],
    case_overrides: Dict[str, Any] | None = None,
    inspect_subtype: str = "segmentation",
) -> Tuple[Dict[str, Any], str, List[str]]:
    """Classify segmentation/mask availability without downloading or installing."""
    avail = copy.deepcopy(matrix)
    if case_overrides:
        avail.update({k: v for k, v in case_overrides.items() if k in avail or k.endswith("_available") or k.endswith("_authorized")})

    warnings: List[str] = []
    seg = bool(avail.get("local_segmentation_available"))
    freespace = bool(avail.get("local_freespace_available"))
    weights = bool(avail.get("local_weights_available"))
    deps = bool(avail.get("dependencies_available"))
    grounded_cached = bool(avail.get("grounded_sam_cached_output_available"))
    sam_cached = bool(avail.get("sam_cached_output_available"))
    freespace_cached = bool(avail.get("freespace_cached_output_available"))
    stub = bool(avail.get("adapter_stub_available"))

    runner_ok = seg or freespace
    if runner_ok and weights and deps:
        mode = "local_real_model"
    elif runner_ok and not weights:
        mode = "blocked_by_missing_weight"
        warnings.append("missing_weight_no_download")
    elif runner_ok and weights and not deps:
        mode = "blocked_by_missing_dependency"
        warnings.append("missing_dependency_no_install")
    elif inspect_subtype == "grounded_sam" and grounded_cached:
        mode = "cached_output"
    elif inspect_subtype == "sam" and sam_cached:
        mode = "cached_output"
    elif inspect_subtype == "freespace" and freespace_cached:
        mode = "cached_output"
    elif grounded_cached or sam_cached or freespace_cached:
        mode = "cached_output"
    elif stub:
        mode = "adapter_stub"
    else:
        mode = "blocked_by_authorization"
        warnings.append("no_execution_path_without_authorization")

    return avail, mode, warnings
