# vision_pipeline/b2/v03/param_stats.py
from __future__ import annotations
from typing import List, Dict
import numpy as np


def collect_param_series(
    param_vectors: List[Dict[str, float]],
) -> Dict[str, List[float]]:
    series: Dict[str, List[float]] = {}
    for pv in param_vectors:
        for k, v in pv.items():
            series.setdefault(k, []).append(float(v))
    return series


def compute_param_stats(series: Dict[str, List[float]]) -> Dict[str, Dict[str, float]]:
    stats = {}
    for k, values in series.items():
        arr = np.array(values)
        stats[k] = {
            "mean": float(arr.mean()),
            "std": float(arr.std()),
            "min": float(arr.min()),
            "max": float(arr.max()),
        }
    return stats

