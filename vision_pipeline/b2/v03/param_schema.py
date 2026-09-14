# vision_pipeline/b2/v03/param_schema.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional

ParamType = Literal["binary", "float", "categorical"]


@dataclass(frozen=True)
class ParamSpec:
    """
    稳定参数定义（用于训练/统计/可视化/回归）
    """
    pid: str                    # stable param id, e.g. "people.density.value"
    ptype: ParamType
    desc: str
    lo: Optional[float] = None  # for float
    hi: Optional[float] = None
    categories: Optional[list[str]] = None  # for categorical


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))

