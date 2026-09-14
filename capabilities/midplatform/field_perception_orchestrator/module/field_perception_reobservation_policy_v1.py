from __future__ import annotations

from typing import Any, Dict, Mapping


def build_field_perception_reobservation_policy_v1(
    information_gap: Mapping[str, Any],
    temporal_context: Mapping[str, Any],
) -> Dict[str, Any]:
    fast_change = bool(temporal_context.get("fast_changing_scene", False))
    return {
        "schema_version": "field_perception_reobservation_policy_v1",
        "reobserve_condition": {
            "rule": "reobserve_when_evidence_stale_or_conflicted",
            "max_interval_ms": 800 if fast_change else 2000,
            "trigger_on_conflict": True,
            "trigger_on_stale": True,
            "enabled": bool(information_gap.get("need_visual_invocation", False)),
        },
    }
