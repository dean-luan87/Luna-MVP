# -*- coding: utf-8 -*-
"""Information Efficiency Score — information_value / compute_cost v1."""

from __future__ import annotations

from typing import Any, Dict

CAPABILITY_COST = {
    "understand_region_ownership": 1,
    "understand_region_text": 3,
    "understand_region_visual": 4,
    "understand_region_layout": 2,
    "understand_region_context": 2,
    "text_recognition": 3,
    "visual_reasoning": 4,
}


def compute_information_efficiency(
    *,
    gated_ri: Dict[str, Any],
    traditional_region_count: int,
    effective_information_units: int = 3,
) -> Dict[str, Any]:
    """
    Compare Luna attention-gated path vs traditional full-image processing.

    Traditional: 100 regions → cost 100, effective info 3
    Luna: 3 regions → cost 3, effective info 3
  """
    luna_cost = max(gated_ri.get("compute_cost", 0), 1)
    luna_value = gated_ri.get("information_value", 0.0)
    luna_efficiency = round(luna_value / luna_cost, 4)

    traditional_cost = max(traditional_region_count * 3, 1)
    traditional_value = float(effective_information_units)
    traditional_efficiency = round(traditional_value / traditional_cost, 4)

    return {
        "metric_id": "information_efficiency_score",
        "luna": {
            "regions_processed": gated_ri.get("activated_region_count", 0),
            "regions_skipped": gated_ri.get("blocked_region_count", 0),
            "compute_cost": luna_cost,
            "effective_information_units": round(luna_value, 2),
            "efficiency_score": luna_efficiency,
        },
        "traditional_baseline": {
            "regions_processed": traditional_region_count,
            "compute_cost": traditional_cost,
            "effective_information_units": effective_information_units,
            "efficiency_score": traditional_efficiency,
        },
        "luna_more_efficient": luna_efficiency > traditional_efficiency,
        "cost_reduction_ratio": round(traditional_cost / luna_cost, 2) if luna_cost else 0,
        "candidate_only": True,
    }
