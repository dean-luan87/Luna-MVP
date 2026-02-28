from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from .types import A3Signals, EnvironmentMode, SafetyLevel, ControlMode, PerceptionState
from .gates import roi_gate
from .config import A3Config, A3ModulationV1
from modulation.modulator_v1 import ModulatorV1, ModulatorV1Params

# Stage 2: fixed-point determinism (A3_FIXEDPOINT=1)
try:
    from runtime.a3_fixedpoint import (
        SCORE_SCALE,
        ALPHA_SCALE,
        q,
        dq,
        clamp_i,
        ema_step_i,
        view_conf_gate_q,
    )
except Exception:
    SCORE_SCALE = 1000
    ALPHA_SCALE = 1000
    q = dq = clamp_i = ema_step_i = view_conf_gate_q = None  # type: ignore


def _clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def _use_fixedpoint() -> bool:
    return os.environ.get("A3_FIXEDPOINT", "1").strip().lower() in ("1", "true", "yes")


def _view_conf_gate(view_conf: float, floor: float, k: float) -> float:
    """B2 gate: floor + (1-floor)*view_conf^k. k=1,floor=0.5 → 0.5+0.5*view_conf（旧逻辑）"""
    if view_conf <= 0.0:
        return floor
    if view_conf >= 1.0:
        return 1.0
    return floor + (1.0 - floor) * (view_conf ** k)


@dataclass
class _A3State:
    ema: float = 0.0
    last_mode: ControlMode = ControlMode.ASSISTED
    last_safety: SafetyLevel = SafetyLevel.SAFE
    last_change_ms: int = 0
    # Peak Hold 状态（仅当 smoothing.peak_hold_frames > 0 时使用）
    peak_hold_value: float = 0.0
    peak_hold_counter: int = 0
    # Stage 2 fixed-point: authoritative int state (used when A3_FIXEDPOINT=1)
    ema_q: int = 0
    peak_hold_value_q: int = 0


class A3Engine:
    """
    A3-v0: read-only environment mode selector.
    - No side effects.
    - Deterministic given signals + config + internal EMA state.
    """

    def __init__(self, config: A3Config, initial_now_ms: Optional[int] = None):
        self.cfg = config
        if initial_now_ms is not None:
            now_ms = initial_now_ms
        else:
            now_ms = int(time.time() * 1000)
        self.state = _A3State(ema=0.0, last_change_ms=now_ms)
        self._modulator: Optional[ModulatorV1] = None
        mod = getattr(config, "modulation", None)
        if isinstance(mod, A3ModulationV1) and getattr(mod, "enabled", False):
            self._modulator = ModulatorV1(
                ModulatorV1Params(
                    lam=mod.lam,
                    alpha_min=mod.alpha_min,
                    alpha_max=mod.alpha_max,
                    risk_density_alpha=mod.risk_density_alpha,
                )
            )

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

        # Stage 2: fixed-point path (A3_FIXEDPOINT=1) — all branching in integer domain
        if _use_fixedpoint() and q is not None and dq is not None and clamp_i is not None and ema_step_i is not None and view_conf_gate_q is not None:
            raw_q, debug = self._compute_raw_complexity_q(signals)
            view_conf = _clamp01(getattr(signals, "view_confidence", 1.0))
            view_conf_q = q(view_conf)
            floor = getattr(self.cfg, "view_conf_gate_floor", 0.5)
            floor_q = q(floor)
            k = getattr(self.cfg, "view_conf_gate_k", 1.0)
            gate_q = view_conf_gate_q(view_conf_q, floor_q, k)
            raw_effective_q = clamp_i((raw_q * gate_q) // SCORE_SCALE, 0, SCORE_SCALE)
            x_hold_q = self._apply_peak_hold_q(raw_effective_q)
            sm = self.cfg.smoothing
            alpha_eff = sm.alpha
            if getattr(sm, "alpha_high", None) is not None and dq(x_hold_q) >= getattr(sm, "alpha_switch_at", 0.85):
                alpha_eff = sm.alpha_high
            mod_debug_fp: Dict[str, Any] = {}
            if self._modulator is not None:
                alpha_eff = self._modulator.get_alpha(
                    alpha_base=alpha_eff,
                    signals=signals,
                    state=self.state,
                    debug=mod_debug_fp,
                )
            alpha_q = q(alpha_eff, ALPHA_SCALE)
            if self.state.ema_q == 0 and self.state.ema != 0.0:
                self.state.ema_q = q(self.state.ema)
            self.state.ema_q = ema_step_i(self.state.ema_q, x_hold_q, alpha_q, SCORE_SCALE)
            ema_float = dq(self.state.ema_q)
            self.state.ema = ema_float
            safety = self._classify_safety_q(self.state.ema_q, signals)
            control = self._classify_control_mode(safety, signals)
            if view_conf_q < q(0.4):
                control = ControlMode.GUARDED

            if getattr(signals, "frame_quality", "GOOD") != "GOOD" and self.state.last_safety == SafetyLevel.SAFE:
                safety = SafetyLevel.SAFE

            control, safety = self._apply_hold(control, safety, now_ms)
            advice_scale, lookahead = self._map_outputs(safety, control, signals)

            t = self.cfg.thresholds
            debug_extra_fp = {
                "raw_q": raw_q,
                "raw": dq(raw_q),
                "raw_effective_q": raw_effective_q,
                "raw_effective": dq(raw_effective_q),
                "x_hold_q": x_hold_q,
                "x_hold": dq(x_hold_q),
                "ema_q": self.state.ema_q,
                "ema": ema_float,
                "view_confidence": view_conf,
                "view_conf_gate_floor": floor,
                "view_conf_gate_k": k,
                "view_conf_gate_value": dq(gate_q),
                "peak_hold_value_q": self.state.peak_hold_value_q,
                "peak_hold_value": dq(self.state.peak_hold_value_q),
                "threshold_safe_to_caution": t.safe_to_caution,
                "threshold_caution_to_danger": t.caution_to_danger,
                "hysteresis": t.hysteresis,
            }
            if getattr(sm, "alpha_high", None) is not None:
                debug_extra_fp["alpha_effective"] = alpha_eff
            if mod_debug_fp:
                debug_extra_fp.update(mod_debug_fp)
            return EnvironmentMode(
                complexity_score=ema_float,
                safety_level=safety,
                control_mode=control,
                allowed_errors=(control != ControlMode.GUARDED),
                advice_budget_scale=advice_scale,
                pal_lookahead_m=lookahead,
                updated_at_ms=now_ms,
                debug=debug | debug_extra_fp,
            )

        raw, debug = self._compute_raw_complexity(signals)
        view_conf = _clamp01(getattr(signals, "view_confidence", 1.0))
        floor = getattr(self.cfg, "view_conf_gate_floor", 0.5)
        k = getattr(self.cfg, "view_conf_gate_k", 1.0)
        gate = _view_conf_gate(view_conf, floor, k)
        raw_effective_unclamped = raw * gate
        clamp_hit = raw_effective_unclamped >= 1.0
        raw_effective = _clamp01(raw_effective_unclamped)
        x_hold = self._apply_peak_hold(raw_effective)
        sm = self.cfg.smoothing
        alpha_eff = sm.alpha
        if getattr(sm, "alpha_high", None) is not None and x_hold >= getattr(sm, "alpha_switch_at", 0.85):
            alpha_eff = sm.alpha_high
        mod_debug: Dict[str, Any] = {}
        if self._modulator is not None:
            alpha_eff = self._modulator.get_alpha(
                alpha_base=alpha_eff,
                signals=signals,
                state=self.state,
                debug=mod_debug,
            )
        ema = self._ema(x_hold, alpha_override=alpha_eff)
        safety = self._classify_safety(ema, signals)
        control = self._classify_control_mode(safety, signals)
        if view_conf < 0.4:
            control = ControlMode.GUARDED

        if getattr(signals, "frame_quality", "GOOD") != "GOOD" and self.state.last_safety == SafetyLevel.SAFE:
            safety = SafetyLevel.SAFE

        control, safety = self._apply_hold(control, safety, now_ms)

        advice_scale, lookahead = self._map_outputs(safety, control, signals)

        t = self.cfg.thresholds
        debug_extra = {
            "raw": raw,
            "raw_effective": raw_effective,
            "x_hold": x_hold,
            "ema": ema,
            "view_confidence": view_conf,
            "view_conf_gate_floor": floor,
            "view_conf_gate_k": k,
            "view_conf_gate_value": gate,
            "clamp_hit": clamp_hit,
            "peak_hold_value": self.state.peak_hold_value,
            "threshold_safe_to_caution": t.safe_to_caution,
            "threshold_caution_to_danger": t.caution_to_danger,
            "hysteresis": t.hysteresis,
        }
        if getattr(sm, "alpha_high", None) is not None:
            debug_extra["alpha_effective"] = alpha_eff
        if mod_debug:
            debug_extra.update(mod_debug)
        return EnvironmentMode(
            complexity_score=ema,
            safety_level=safety,
            control_mode=control,
            allowed_errors=(control != ControlMode.GUARDED),
            advice_budget_scale=advice_scale,
            pal_lookahead_m=lookahead,
            updated_at_ms=now_ms,
            debug=debug | debug_extra,
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
        weighted_sum_before_clamp = sum(components.values())
        scale = getattr(self.cfg, "risk_scale_factor", 1.0)
        scaled_sum = weighted_sum_before_clamp * scale
        raw = _clamp01(scaled_sum)
        debug = {k: float(v) for k, v in components.items()}
        debug["weighted_sum_before_clamp"] = float(weighted_sum_before_clamp)
        debug["risk_scale_factor"] = float(scale)
        debug["scaled_sum_before_clamp"] = float(scaled_sum)
        # 量纲审计：raw feature（未乘权重），便于统计真实物理尺度
        debug["risk_density_raw"] = float(risk)
        debug["redline_hit_raw"] = float(redline)
        debug["path_instability_raw"] = float(path_instability)
        debug["motion_instability_raw"] = float(motion)
        debug["occlusion_ratio_raw"] = float(occl)
        debug["roi_load_raw"] = float(roi_load)
        return raw, debug

    def _compute_raw_complexity_q(self, s: A3Signals) -> Tuple[int, dict]:
        """Fixed-point raw complexity: all in integer domain. Returns (raw_q, debug with float shadows)."""
        if q is None:
            raw, debug = self._compute_raw_complexity(s)
            return q(raw), debug
        w = self.cfg.weights
        roi_max_count = 5.0

        risk = _clamp01(s.risk_density)
        redline = 1.0 if s.redline_hit else 0.0
        occl = _clamp01(s.occlusion_ratio)

        roi_load = 0.0
        if roi_gate(getattr(s, "frame_quality", "GOOD"), _clamp01(getattr(s, "view_confidence", 1.0))):
            roi_norm = min(max(s.roi_count, 0), roi_max_count) / float(roi_max_count)
            roi_load = _clamp01(roi_norm)

        path_instability = getattr(s, "path_instability", None)
        if path_instability is None or path_instability < 0:
            path_instability = 1.0 - _clamp01(s.path_stability)
        else:
            path_instability = _clamp01(path_instability)

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

        risk_q = q(risk)
        redline_q = SCORE_SCALE if s.redline_hit else 0
        occl_q = q(occl)
        roi_q = q(roi_load)
        path_q = q(path_instability)
        branch_q = q(branch_load)
        speak_q = q(speak)
        reject_q = q(reject)
        motion_q = q(motion)

        w_risk_q = q(w.risk_density)
        w_redline_q = q(w.redline_hit)
        w_occl_q = q(w.occlusion_ratio)
        w_roi_q = q(w.roi_load)
        w_path_q = q(w.path_instability)
        w_motion_q = q(w.motion_instability)
        w_branch_q = q(w.branch_load)
        w_speak_q = q(w.speak_pressure)
        w_reject_q = q(w.reject_pressure)

        weighted_sum_q = (
            (risk_q * w_risk_q + redline_q * w_redline_q + occl_q * w_occl_q + roi_q * w_roi_q
             + path_q * w_path_q + motion_q * w_motion_q + branch_q * w_branch_q
             + speak_q * w_speak_q + reject_q * w_reject_q)
            // SCORE_SCALE
        )
        scale_f = getattr(self.cfg, "risk_scale_factor", 1.0)
        scale_q = q(scale_f)
        scaled_sum_q = (weighted_sum_q * scale_q) // SCORE_SCALE
        raw_q = clamp_i(scaled_sum_q, 0, SCORE_SCALE)

        debug = {
            "risk_density": dq(risk_q * w_risk_q // SCORE_SCALE),
            "redline_hit": dq(redline_q * w_redline_q // SCORE_SCALE),
            "occlusion_ratio": dq(occl_q * w_occl_q // SCORE_SCALE),
            "roi_load": dq(roi_q * w_roi_q // SCORE_SCALE),
            "path_instability": dq(path_q * w_path_q // SCORE_SCALE),
            "motion_instability": dq(motion_q * w_motion_q // SCORE_SCALE),
            "branch_load": dq(branch_q * w_branch_q // SCORE_SCALE),
            "speak_pressure": dq(speak_q * w_speak_q // SCORE_SCALE),
            "reject_pressure": dq(reject_q * w_reject_q // SCORE_SCALE),
            "weighted_sum_before_clamp": dq(weighted_sum_q),
            "risk_scale_factor": scale_f,
            "scaled_sum_before_clamp": dq(scaled_sum_q),
            "risk_density_raw": risk,
            "redline_hit_raw": float(redline),
            "path_instability_raw": path_instability,
            "motion_instability_raw": motion,
            "occlusion_ratio_raw": occl,
            "roi_load_raw": roi_load,
        }
        return raw_q, debug

    def _apply_peak_hold(self, x: float) -> float:
        """clamp 后、EMA 前：峰值保持 2～3 帧缓慢衰减，给 EMA 时间累加。"""
        hold_frames = getattr(self.cfg.smoothing, "peak_hold_frames", 0) or 0
        if hold_frames <= 0:
            return x
        decay = getattr(self.cfg.smoothing, "peak_decay", 0.9)
        if x >= self.state.peak_hold_value:
            self.state.peak_hold_value = x
            self.state.peak_hold_counter = hold_frames
        else:
            self.state.peak_hold_counter -= 1
            if self.state.peak_hold_counter <= 0:
                self.state.peak_hold_value = _clamp01(self.state.peak_hold_value * decay)
        return max(x, self.state.peak_hold_value)

    def _apply_peak_hold_q(self, x_q: int) -> int:
        """Peak hold in fixed-point; state uses peak_hold_value_q and peak_hold_counter."""
        if q is None or clamp_i is None:
            return x_q
        hold_frames = getattr(self.cfg.smoothing, "peak_hold_frames", 0) or 0
        if hold_frames <= 0:
            return x_q
        decay = getattr(self.cfg.smoothing, "peak_decay", 0.9)
        decay_q = q(decay)
        if x_q >= self.state.peak_hold_value_q:
            self.state.peak_hold_value_q = x_q
            self.state.peak_hold_counter = hold_frames
        else:
            self.state.peak_hold_counter -= 1
            if self.state.peak_hold_counter <= 0:
                self.state.peak_hold_value_q = clamp_i(
                    (self.state.peak_hold_value_q * decay_q) // SCORE_SCALE, 0, SCORE_SCALE
                )
        return max(x_q, self.state.peak_hold_value_q)

    def _ema(self, raw: float, alpha_override: Optional[float] = None) -> float:
        alpha = alpha_override if alpha_override is not None else self.cfg.smoothing.alpha
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

    def _classify_safety_q(self, ema_q: int, s: A3Signals) -> SafetyLevel:
        """Safety classification in integer domain; thresholds quantized with SCORE_SCALE."""
        if q is None:
            return self._classify_safety(dq(ema_q), s)
        t = self.cfg.thresholds
        if s.redline_hit:
            return SafetyLevel.DANGER
        safe_to_caution_q = q(t.safe_to_caution)
        caution_to_danger_q = q(t.caution_to_danger)
        hysteresis_q = q(t.hysteresis)

        last = self.state.last_safety
        if last == SafetyLevel.SAFE:
            if ema_q >= (safe_to_caution_q + hysteresis_q):
                return SafetyLevel.CAUTION
            return SafetyLevel.SAFE

        if last == SafetyLevel.CAUTION:
            if ema_q >= (caution_to_danger_q + hysteresis_q):
                return SafetyLevel.DANGER
            if ema_q < (safe_to_caution_q - hysteresis_q):
                return SafetyLevel.SAFE
            return SafetyLevel.CAUTION

        if ema_q < (caution_to_danger_q - hysteresis_q):
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
