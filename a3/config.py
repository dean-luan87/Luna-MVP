from __future__ import annotations

from dataclasses import dataclass, field


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
