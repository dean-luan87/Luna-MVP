# -*- coding: utf-8 -*-
"""
D1 Phase 2：SimRunner 专用 A3 Headless 适配器。
仅用于 mode=recompute；禁止墙钟，仅用 virtual_ts。
本文件为 simulation 内唯一允许 import a3 的模块（见 guard 白名单）。
"""
from __future__ import annotations

from typing import Any, Dict

from a3.config import from_flat_dict
from a3.engine import A3Engine
from a3.types import A3Signals, ControlMode, SafetyLevel


def _view_confidence_for_replay(o: dict) -> float:
    fq = str(o.get("frame_quality") or "").strip().upper()
    if fq == "NONE":
        return 1.0
    v = o.get("vc")
    if v is None:
        return 1.0
    return max(0.0, min(1.0, float(v)))


def _obs_to_signals(obs_dict: dict) -> A3Signals:
    o = obs_dict if isinstance(obs_dict.get("motion"), (int, float)) else (obs_dict.get("obs") or {})
    # stress_v2 / trace 常用 complexity_raw, path_instability, motion_instability；兼容 complexity, path, motion
    risk_density = float(o.get("complexity") or o.get("complexity_raw") or 0.0)
    path_instability_val = o.get("path_instability")
    if path_instability_val is not None and isinstance(path_instability_val, (int, float)):
        path_instability_out = max(0.0, min(1.0, float(path_instability_val)))
        path_stability = 1.0 - path_instability_out
    else:
        path_val = o.get("path", 0.0)
        path_stability = 1.0 - float(path_val) if isinstance(path_val, (int, float)) else 1.0
        path_stability = max(0.0, min(1.0, path_stability))
        path_instability_out = float(o["path"]) if "path" in o and isinstance(o.get("path"), (int, float)) else None
    branch_val = o.get("branch", 0.0)
    branch_count = int(branch_val) if isinstance(branch_val, (int, float)) else 0
    roi_count = int(o.get("roi", 0) or 0)
    branch_load = None
    if "branch" in o and isinstance(o.get("branch"), (int, float)):
        b = float(o["branch"])
        if 0 <= b <= 1:
            branch_load = b
    if branch_load is None and "branch_load" in o and isinstance(o.get("branch_load"), (int, float)):
        branch_load = max(0.0, min(1.0, float(o["branch_load"])))
    motion_val = float(o.get("motion_instability") or o.get("motion") or 0.0)
    return A3Signals(
        risk_density=risk_density,
        redline_hit=bool(o.get("redline_hit", False)),
        path_stability=path_stability,
        path_instability=path_instability_out,
        branch_count=min(max(branch_count, 0), 32),
        branch_load=branch_load,
        roi_count=min(max(roi_count, 0), 24),
        occlusion_ratio=float(o.get("occlusion", 0.0) or 0.0),
        recent_speak_rate=float(o.get("speak_rate", 0.0) or 0.0),
        rejected_rate=float(o.get("reject_rate", 0.0) or 0.0),
        has_goal=True,
        view_confidence=_view_confidence_for_replay(o),
        frame_quality=str(o.get("frame_quality", "GOOD") or "GOOD"),
        motion_instability=motion_val,
    )


class A3HeadlessAdapter:
    """
    Headless A3：base_config + patch_config 合并后驱动 A3Engine。
    仅用 virtual_ts，禁止墙钟；reset() 保证可重复。
    """

    def __init__(self, base_config: dict, patch_config: dict):
        merged = {"enabled": True, **(base_config or {}), **(patch_config or {})}
        self._config = from_flat_dict(merged)
        self._engine: A3Engine | None = None
        self._seq: int = 0
        self._did_dump_smoothing: bool = False

    def reset(self) -> None:
        self._engine = None
        self._seq = 0

    def tick(self, obs_dict: dict, virtual_ts: float) -> dict:
        if self._engine is None:
            now_ms = int(virtual_ts * 1000) if virtual_ts is not None else 0
            self._engine = A3Engine(self._config, initial_now_ms=now_ms)
            if not self._did_dump_smoothing:
                sm = self._config.smoothing
                print(
                    "[A3] smoothing config (engine init): peak_hold_frames=%s peak_decay=%s alpha_high=%s alpha_switch_at=%s"
                    % (getattr(sm, "peak_hold_frames", None), getattr(sm, "peak_decay", None), getattr(sm, "alpha_high", None), getattr(sm, "alpha_switch_at", None))
                )
                self._did_dump_smoothing = True
        now_ms = int(virtual_ts * 1000)
        if isinstance(obs_dict.get("obs"), dict):
            signals = _obs_to_signals(obs_dict)
        else:
            signals = _obs_to_signals(obs_dict if isinstance(obs_dict.get("motion"), (int, float)) else {"obs": obs_dict})
        mode = self._engine.tick(signals, now_ms=now_ms)
        seq = obs_dict.get("seq", self._seq)
        self._seq = seq + 1
        debug = getattr(mode, "debug", None) or {}
        # 决策用风险 = 最终用于 _classify_safety 的 ema（hold + conditional alpha 之后），与 threshold 同口径
        risk_used = float(debug.get("ema", getattr(mode, "complexity_score", 0.0)))
        threshold = float(debug.get("threshold_safe_to_caution", 0.38))
        out: Dict[str, Any] = {
            "seq": seq,
            "safety_level": mode.safety_level.value if isinstance(mode.safety_level, SafetyLevel) else str(mode.safety_level),
            "control_mode": mode.control_mode.value if isinstance(mode.control_mode, ControlMode) else str(mode.control_mode),
            "pal_lookahead_m": float(mode.pal_lookahead_m),
            "complexity_score": float(getattr(mode, "complexity_score", 0.0)),
            "risk_used_for_decision": risk_used,
            "threshold_safe_to_caution": threshold,
        }
        if getattr(mode, "debug", None):
            out["a3_debug"] = {k: float(v) for k, v in mode.debug.items()}
        return out
