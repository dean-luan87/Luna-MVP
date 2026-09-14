# -*- coding: utf-8 -*-
"""Field simulation input view builder v1."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.field_simulation_planning_items_v1 import build_simulation_input_view as _build


def build_field_simulation_input_view(
    *,
    dryrun_result: Dict[str, Any],
    hardened_result: Optional[Dict[str, Any]] = None,
    reusable_case: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Map EnhancedFieldScene / HardenedResult / ReusableCase to FieldSimulationInputView."""
    return _build(
        dryrun_result=dryrun_result,
        hardened_result=hardened_result,
        reusable_case=reusable_case,
    )
