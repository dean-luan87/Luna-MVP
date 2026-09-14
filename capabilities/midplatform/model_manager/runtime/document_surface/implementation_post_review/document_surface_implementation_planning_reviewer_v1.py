# -*- coding: utf-8 -*-
"""Document Surface Implementation — planning reviewer v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_implementation_options_v1 import (
    FIRST_REAL_IMPLEMENTATION_CANDIDATE,
    evaluate_implementation_options,
)


def review_implementation_planning() -> Dict[str, Any]:
    options = evaluate_implementation_options()
    deferred = options.get("deferred_candidates") or []
    return {
        "review_id": "document_surface_implementation_planning_review_v1",
        "options_evaluated_count": options.get("options_evaluated_count"),
        "option_a_recommended": options.get("first_real_implementation_candidate") == FIRST_REAL_IMPLEMENTATION_CANDIDATE,
        "deferred_candidates": deferred,
        "deferred_count": len(deferred),
        "vlm_not_first_runtime": options.get("vlm_not_first_runtime") is True,
        "no_model_execution": options.get("no_model_execution") is True,
        "passed": (
            options.get("first_real_implementation_candidate") == FIRST_REAL_IMPLEMENTATION_CANDIDATE
            and len(deferred) >= 3
            and options.get("no_model_execution") is True
        ),
    }
