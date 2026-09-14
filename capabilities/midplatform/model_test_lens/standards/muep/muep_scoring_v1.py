# -*- coding: utf-8 -*-
"""MUEP V1 unified scoring — task + robustness + structural."""

from __future__ import annotations

from typing import Mapping

MUEP_WEIGHTS = {
    "task": 0.6,
    "robustness": 0.25,
    "structural": 0.15,
}


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def compute_muep_final_score(
    task_score: float,
    robustness_score: float,
    structural_score: float,
) -> float:
    """final_score = 0.6*task + 0.25*robustness + 0.15*structural"""
    return clamp01(
        MUEP_WEIGHTS["task"] * clamp01(task_score)
        + MUEP_WEIGHTS["robustness"] * clamp01(robustness_score)
        + MUEP_WEIGHTS["structural"] * clamp01(structural_score)
    )


def build_muep_metrics_block(
    *,
    primary_metric_name: str,
    primary_metric_value: float,
    primary_metric_score_normalized: float,
    robustness: Mapping[str, float],
    structural_score: float,
    structural_notes: list[str] | None = None,
) -> dict:
    robustness_score = clamp01(float(robustness.get("robustness_score_normalized", 0.0)))
    structural_score_n = clamp01(structural_score)
    final_score = compute_muep_final_score(
        primary_metric_score_normalized,
        robustness_score,
        structural_score_n,
    )
    return {
        "layer_a_task": {
            "primary_metric_name": primary_metric_name,
            "primary_metric_value": primary_metric_value,
            "primary_metric_score_normalized": clamp01(primary_metric_score_normalized),
        },
        "layer_b_robustness": dict(robustness),
        "layer_c_structural": {
            "structural_quality_score_normalized": structural_score_n,
            "notes": structural_notes or [],
        },
        "final_score": final_score,
        "scoring_weights": dict(MUEP_WEIGHTS),
    }
