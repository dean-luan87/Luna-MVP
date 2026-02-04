from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional, Tuple

from .types import A3Signals, EnvironmentMode, SafetyLevel, ControlMode, PerceptionState
from .gates import roi_gate
from .config import A3Config


def _clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


@dataclass
class _A3State:
    ema: float = 0.0
    last_mode: ControlMode = ControlMode.ASSISTED
    last_safety: SafetyLevel = SafetyLevel.SAFE
    last_change_ms: int = 0


class A3Engine:
    """
    A3-v0: read-only environment mode selector.
    - No side effects.
    - Deterministic given signals + config + internal EMA state.
    """

    def __init__(self, config: A3Config):
        self.cfg = config
        now_ms = int(time.time() * 1000)
        self.state = _A3State(ema=0.0, last_change_ms=now_ms)

    def tick(self, signals: A3Signals, now_ms: Optional[int] = None) -> EnvironmentMode:
        if now_ms is None:
            now_ms = int(time.time() * 1000)

        if not self.cfg.enabled:
            return EnvironmentMode(
                complexity_score=0.0,
                safety_level=SafetyLevel.SAFE,
                control_mode=ControlMode.ASSISTED,
                allowed_errors=True,
                advice_budget_scale=1.0,
                pal_lookahead_m=5.0,
                updated_at_ms=now_ms,
                debug={},
            )

        raw, debug = self._compute_raw_complexity(signals)
        view_conf = _clamp01(getattr(signals, "view_confidence", 1.0))
        raw_effective = _clamp01(raw * (0.5 + 0.5 * view_conf))
        ema = self._ema(raw_effective)
        safety = self._classify_safety(ema, signals)
        control = self._classify_control_mode(safety, signals)
        if view_conf < 0.4:
            control = ControlMode.GUARDED

        if getattr(signals, "frame_quality", "GOOD") != "GOOD" and self.state.last_safety == SafetyLevel.SAFE:
            safety = SafetyLevel.SAFE

        control, safety = self._apply_hold(control, safety, now_ms)

        advice_scale, lookahead = self._map_outputs(safety, control, signals)

        return EnvironmentMode(
            complexity_score=ema,
            safety_level=safety,
            control_mode=control,
            allowed_errors=(control != ControlMode.GUARDED),
            advice_budget_scale=advice_scale,
            pal_lookahead_m=lookahead,
            updated_at_ms=now_ms,
            debug=debug | {
                "raw": raw,
                "raw_effective": raw_effective,
                "ema": ema,
                "view_confidence": view_conf,
            },
        )

    def _compute_raw_complexity(self, s: A3Signals) -> Tuple[float, dict]:
        w = self.cfg.weights
        roi_max_count = 5.0

        risk = _clamp01(s.risk_density)
        redline = 1.0 if s.redline_hit else 0.0
        occl = _clamp01(s.occlusion_ratio)

        roi_load = 0.0
        if roi_gate(getattr(s, "frame_quality", "GOOD"), _clamp01(getattr(s, "view_confidence", 1.0))):
            roi_norm = min(max(s.roi_count, 0), roi_max_count) / float(roi_max_count)
            roi_load = _clamp01(roi_norm)

        # Path v0：vision 提供时用 vision，否则用 nav 的 1-path_stability
        path_instability = getattr(s, "path_instability", None)
        if path_instability is None or path_instability < 0:
            path_instability = 1.0 - _clamp01(s.path_stability)
        else:
            path_instability = _clamp01(path_instability)

        # Branch v0：vision 提供 branch_load 时直接用，否则用 branch_count 归一化
        branch_load = getattr(s, "branch_load", None)
        if branch_load is None or branch_load < 0:
            branch_load = min(max(s.branch_count, 0), self.cfg.branch_count_cap) / float(self.cfg.branch_count_cap)
        else:
            branch_load = _clamp01(branch_load)

        speak = _clamp01(s.recent_speak_rate)
        reject = _clamp01(s.rejected_rate)
        motion = _clamp01(getattr(s, "motion_instability", 0.0))

        perception_degraded = getattr(s, "perception_state", PerceptionState.NORMAL) == PerceptionState.DEGRADED
        if perception_degraded:
            occl = 0.0
            roi_load = 0.0

        components = {
            "risk_density": risk * w.risk_density,
            "redline_hit": redline * w.redline_hit,
            "occlusion_ratio": occl * w.occlusion_ratio,
            "roi_load": roi_load * w.roi_load,
            "path_instability": path_instability * w.path_instability,
            "motion_instability": motion * w.motion_instability,
            "branch_load": branch_load * w.branch_load,
            "speak_pressure": speak * w.speak_pressure,
            "reject_pressure": reject * w.reject_pressure,
        }
        raw = sum(components.values())
        raw = _clamp01(raw)
        debug = {k: float(v) for k, v in components.items()}
        return raw, debug

    def _ema(self, raw: float) -> float:
        alpha = self.cfg.smoothing.alpha
        self.state.ema = _clamp01(alpha * raw + (1.0 - alpha) * self.state.ema)
        return self.state.ema

    def _classify_safety(self, ema: float, s: A3Signals) -> SafetyLevel:
        t = self.cfg.thresholds

        if s.redline_hit:
            return SafetyLevel.DANGER

        last = self.state.last_safety
        if last == SafetyLevel.SAFE:
            if ema >= (t.safe_to_caution + t.hysteresis):
                return SafetyLevel.CAUTION
            return SafetyLevel.SAFE

        if last == SafetyLevel.CAUTION:
            if ema >= (t.caution_to_danger + t.hysteresis):
                return SafetyLevel.DANGER
            if ema < (t.safe_to_caution - t.hysteresis):
                return SafetyLevel.SAFE
            return SafetyLevel.CAUTION

        if ema < (t.caution_to_danger - t.hysteresis):
            return SafetyLevel.CAUTION
        return SafetyLevel.DANGER

    def _classify_control_mode(self, safety: SafetyLevel, s: A3Signals) -> ControlMode:
        if safety == SafetyLevel.DANGER:
            return ControlMode.GUARDED
        if safety == SafetyLevel.CAUTION and s.has_goal:
            return ControlMode.SHARED
        return ControlMode.ASSISTED

    def _apply_hold(self, control: ControlMode, safety: SafetyLevel, now_ms: int) -> Tuple[ControlMode, SafetyLevel]:
        t = self.cfg.thresholds
        held_ms = now_ms - self.state.last_change_ms

        last_control = self.state.last_mode
        last_safety = self.state.last_safety
        severity = {ControlMode.ASSISTED: 0, ControlMode.SHARED: 1, ControlMode.GUARDED: 2}

        if severity[control] > severity[last_control]:
            self.state.last_mode = control
            self.state.last_safety = safety
            self.state.last_change_ms = now_ms
            return control, safety

        if severity[control] < severity[last_control] and held_ms < t.min_mode_hold_ms:
            return last_control, last_safety

        if control != last_control or safety != last_safety:
            self.state.last_mode = control
            self.state.last_safety = safety
            self.state.last_change_ms = now_ms
        return control, safety

    def _map_outputs(self, safety: SafetyLevel, control: ControlMode, s: A3Signals) -> Tuple[float, float]:
        p = self.cfg.output_policy

        if safety == SafetyLevel.SAFE:
            advice = p.advice_scale_safe
            look = p.lookahead_safe_m
        elif safety == SafetyLevel.CAUTION:
            advice = p.advice_scale_caution
            look = p.lookahead_caution_m
        else:
            advice = p.advice_scale_danger
            look = p.lookahead_danger_m

        if s.redline_hit:
            look += p.lookahead_redline_boost_m

        if control == ControlMode.GUARDED:
            advice = min(advice, 0.5)

        return float(advice), float(look)
