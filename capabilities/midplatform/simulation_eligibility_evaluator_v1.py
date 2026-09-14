# -*- coding: utf-8 -*-
"""Simulation eligibility evaluator v1."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.field_simulation_planning_items_v1 import (
    evaluate_simulation_eligibility as _evaluate,
)


def evaluate_simulation_eligibility(
    input_view: Dict[str, Any],
    dryrun_result: Dict[str, Any],
    reusable_case: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return _evaluate(input_view, dryrun_result, reusable_case)
