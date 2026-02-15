from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Any, Dict, Optional


@dataclass
class A3Weights:
    risk_density: float = 0.30
    redline_hit: float = 0.25
    occlusion_ratio: float = 0.12
    roi_load: float = 0.20
    path_instability: float = 0.30  # Path v0：权重 ≈ ROI 的 1.5 倍
    motion_instability: float = 0.30
    branch_load: float = 0.20  # Branch v0：权重 ≤ path，≤ motion，≈ ROI
    speak_pressure: float = 0.05
    reject_pressure: float = 0.03


@dataclass
class A3Thresholds:
    safe_to_caution: float = 0.38
    caution_to_danger: float = 0.68
    hysteresis: float = 0.06
    min_mode_hold_ms: int = 2000


@dataclass
class A3Smoothing:
    alpha: float = 0.25
    # Peak Hold（实验室/应力）：clamp 后、EMA 前，延长尖峰 2～3 帧衰减，仅 peak_hold_frames>0 启用
    peak_hold_frames: int = 0
    peak_decay: float = 0.9
    # Conditional alpha（可选）：高压段用 alpha_high 加快跟踪，仅 alpha_high 非 None 时启用
    alpha_high: Optional[float] = None
    alpha_switch_at: float = 0.85


@dataclass
class A3OutputPolicy:
    advice_scale_safe: float = 1.0
    advice_scale_caution: float = 0.7
    advice_scale_danger: float = 0.4
    lookahead_safe_m: float = 5.0
    lookahead_caution_m: float = 10.0
    lookahead_danger_m: float = 15.0
    lookahead_redline_boost_m: float = 5.0


@dataclass
class A3Config:
    enabled: bool = False
    weights: A3Weights = field(default_factory=A3Weights)
    thresholds: A3Thresholds = field(default_factory=A3Thresholds)
    smoothing: A3Smoothing = field(default_factory=A3Smoothing)
    output_policy: A3OutputPolicy = field(default_factory=A3OutputPolicy)
    roi_count_cap: int = 12
    branch_count_cap: int = 6
    # 量纲校准：weighted_sum 之后乘此因子再进 effective → EMA → 阈值判定；默认 1.0，不动阈值
    risk_scale_factor: float = 1.0


def from_flat_dict(flat: Dict[str, Any]) -> A3Config:
    """从扁平 key（如 weights.risk_density）合并到默认 config。仅接受已知字段。"""
    nested: Dict[str, Dict[str, Any]] = {}
    for k, v in flat.items():
        if "." not in k:
            continue
        top, rest = k.split(".", 1)
        if top not in nested:
            nested[top] = {}
        nested[top][rest] = v

    def sub(cls: type, d: Dict[str, Any]) -> Any:
        names = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in names})

    weights = sub(A3Weights, nested.get("weights", {}))
    thresholds = sub(A3Thresholds, nested.get("thresholds", {}))
    smoothing = sub(A3Smoothing, nested.get("smoothing", {}))
    output_policy = sub(A3OutputPolicy, nested.get("output_policy", {}))
    top_only = {"enabled", "roi_count_cap", "branch_count_cap", "risk_scale_factor"}
    top_d = {k: v for k, v in flat.items() if "." not in k and k in top_only}
    return A3Config(
        weights=weights,
        thresholds=thresholds,
        smoothing=smoothing,
        output_policy=output_policy,
        **top_d,
    )
