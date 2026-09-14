# -*- coding: utf-8 -*-
"""Tracking / Optical Flow model availability checker v1."""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple


def check_tracking_opticalflow_availability(
    *,
    matrix: Dict[str, Any],
    case_overrides: Dict[str, Any] | None = None,
    inspect_subtype: str = "tracking",
) -> Tuple[Dict[str, Any], str, List[str]]:
    """Classify tracking/optical flow availability without downloading or installing."""
    avail = copy.deepcopy(matrix)
    if case_overrides:
        avail.update({k: v for k, v in case_overrides.items() if k in avail or k.endswith("_available") or k.endswith("_authorized")})

    warnings: List[str] = []
    tracker = bool(avail.get("local_tracker_available"))
    flow = bool(avail.get("local_flow_adapter_available"))
    weights = bool(avail.get("local_weights_available"))
    deps = bool(avail.get("dependencies_available"))
    cached_track = bool(avail.get("cached_tracking_output_available"))
    cached_flow = bool(avail.get("cached_flow_output_available"))
    stub = bool(avail.get("adapter_stub_available"))

    runner_ok = tracker or flow
    if runner_ok and weights and deps:
        mode = "local_real_model" if tracker else "local_adapter"
    elif runner_ok and not weights:
        mode = "blocked_by_missing_weight"
        warnings.append("missing_weight_no_download")
    elif runner_ok and weights and not deps:
        mode = "blocked_by_missing_dependency"
        warnings.append("missing_dependency_no_install")
    elif inspect_subtype == "optical_flow" and cached_flow:
        mode = "cached_output"
    elif cached_track or cached_flow:
        mode = "cached_output"
    elif stub:
        mode = "adapter_stub"
    else:
        mode = "blocked_by_authorization"
        warnings.append("no_execution_path_without_authorization")

    return avail, mode, warnings
