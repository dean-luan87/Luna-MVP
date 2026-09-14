# -*- coding: utf-8 -*-
"""SLAM spatial mapping model availability checker v1."""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple


def check_slam_spatial_mapping_availability(
    *,
    matrix: Dict[str, Any],
    case_overrides: Dict[str, Any] | None = None,
) -> Tuple[Dict[str, Any], str, List[str]]:
    """Classify SLAM model availability without downloading or installing."""
    avail = copy.deepcopy(matrix)
    if case_overrides:
        avail.update({k: v for k, v in case_overrides.items() if k in avail or k.endswith("_available") or k.endswith("_authorized")})

    warnings: List[str] = []
    runner = bool(avail.get("local_slam_runner_available"))
    weights = bool(avail.get("local_slam_weights_available"))
    deps = bool(avail.get("slam_dependencies_available"))
    cached = bool(avail.get("cached_output_available"))
    stub = bool(avail.get("adapter_stub_available"))
    model_dl = bool(avail.get("model_download_authorized"))
    weight_dl = bool(avail.get("weight_download_authorized"))

    if runner and weights and deps:
        mode = "local_real_model"
    elif runner and not weights:
        mode = "blocked_by_missing_weight"
        warnings.append("missing_weight_no_download")
    elif runner and weights and not deps:
        mode = "blocked_by_missing_dependency"
        warnings.append("missing_dependency_no_install")
    elif not model_dl and not weight_dl and runner and not weights:
        mode = "blocked_by_missing_weight"
    elif cached:
        mode = "cached_output"
    elif stub:
        mode = "adapter_stub"
    elif not avail.get("model_download_authorized") and not runner:
        mode = "blocked_by_authorization"
        warnings.append("blocked_by_authorization")
    else:
        mode = "blocked_by_authorization"
        warnings.append("no_execution_path_without_authorization")

    return avail, mode, warnings
