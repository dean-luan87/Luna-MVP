# vision_pipeline/b2/v03/param_regression.py
from __future__ import annotations
from typing import List, Dict
import numpy as np


def build_regression_matrix(
    param_vectors: List[Dict[str, float]],
    errors: List[float],
):
    keys = sorted({k for pv in param_vectors for k in pv.keys()})
    X = []
    y = np.array(errors)

    for pv in param_vectors:
        X.append([pv.get(k, 0.0) for k in keys])

    return np.array(X), y, keys


def linear_regression(X, y):
    # 最小二乘：Xw = y
    w, *_ = np.linalg.lstsq(X, y, rcond=None)
    return w

