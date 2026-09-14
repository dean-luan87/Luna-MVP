# -*- coding: utf-8 -*-
"""Attention-Gated RI DryRun metrics v1."""

from __future__ import annotations

from typing import Any, Dict

_METRICS: Dict[str, int] = {
    "gate_applied": 0,
    "regions_blocked": 0,
    "capabilities_blocked": 0,
    "efficiency_computed": 0,
    "scene_graph_merged": 0,
}


def reset_attention_gated_ri_dryrun_metrics() -> None:
    for k in _METRICS:
        _METRICS[k] = 0


def record_gate_applied(*, blocked_count: int, capabilities_blocked: int) -> None:
    _METRICS["gate_applied"] += 1
    _METRICS["regions_blocked"] += blocked_count
    _METRICS["capabilities_blocked"] += capabilities_blocked


def record_efficiency_computed() -> None:
    _METRICS["efficiency_computed"] += 1


def record_scene_graph_merged() -> None:
    _METRICS["scene_graph_merged"] += 1


def get_attention_gated_ri_dryrun_metrics() -> Dict[str, Any]:
    return dict(_METRICS)
