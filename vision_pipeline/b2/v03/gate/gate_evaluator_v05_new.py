# vision_pipeline/b2/v03/gate/gate_evaluator_v05.py
"""
B2 Gate v0.5 - Gate Evaluator（完整修复版）

v0.5 FIXES:
- True hysteresis (enter/exit thresholds)
- Min-hold frames per mode
- Cooldown after switch
- Trace fields that explain "why not switching"
"""

from __future__ import annotations

import os
import yaml
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
from pathlib import Path


@dataclass
class GateRuntimeState:
    """Persistent state to enforce hysteresis / min-hold / cooldown."""
    last_mode: str = "READ_ONLY"
    last_blocked_by: Optional[str] = None
    # Frames since entering the current mode
    residence_frames: int = 0
    # Cooldown frames remaining after a mode switch
    cooldown_remaining: int = 0
    # Book-keeping for debugging/metrics
    hysteresis_hold_hits: int = 0
    min_hold_hits: int = 0
    cooldown_hits: int = 0


class GateEvaluatorV05:
    def __init__(self, config_path: Optional[str] = None):
        if config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
        else:
            # Use default config
            default_config_path = Path(__file__).parent / "gate_config.yaml"
            if default_config_path.exists():
                with open(default_config_path, "r", encoding="utf-8") as f:
                    self.config = yaml.safe_load(f)
            else:
                self.config = self._get_default_config()
        
        self.state = GateRuntimeState()

    def _get_default_config(self) -> Dict[str, Any]:
        """Default config if file not found"""
        return {
            "version": "0.5",
            "runtime_policy": {
                "cooldown_frames_after_switch": 15,
                "min_hold_frames": {
                    "ACTIVE": 20,
                    "READ_ONLY": 10,
                    "SUSPENDED": 10,
                }
            },
            "hard_gates": {
                "camera_stability": {
                    "enabled": True,
                    "enter_threshold": 0.65,
                    "exit_threshold": 0.55,
                    "block_reason": "camera_shake",
                    "human_readable": "镜头晃动过大，无法稳定感知环境"
                },
                "distance_range": {
                    "enabled": True,
                    "range_min_m": 2.0,
                    "block_reason": "too_close",
                    "human_readable": "观察距离过近，进入 C 主导范围"
                }
            },
            "soft_gates": {
                "evidence_continuity": {
                    "enabled": True,
                    "consecutive_frames": 6,
                    "downgrade_reason": "insufficient_evidence",
                    "human_readable": "证据尚未稳定，仅允许只读"
                }
            },
            "stability_score": {
                "missing_view_state_default_mode": "READ_ONLY",
                "missing_view_state_human_readable": "缺少 view_state，仅允许只读（保守）"
            }
        }

    def evaluate(
        self,
        *,
        stability_score: Optional[float],
        range_m: Optional[float],
        visibility_score: Optional[float] = None,
        evidence_ok: bool = True,
        frame_id: Optional[int] = None,
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Returns: (mode, reason, gate_eval_dict)

        v0.5 FIXES:
        - True hysteresis (enter/exit thresholds)
        - Min-hold frames per mode
        - Cooldown after switch
        - Trace fields that explain "why not switching"
        """

        # -----------------------------
        # 0) Missing view_state policy
        # -----------------------------
        if stability_score is None or range_m is None:
            missing_cfg = self.config.get("stability_score", {})
            default_mode = str(missing_cfg.get("missing_view_state_default_mode", "READ_ONLY")).upper()
            hr = missing_cfg.get("missing_view_state_human_readable", "缺少 view_state，仅允许只读（保守）")
            desired_mode = default_mode
            desired_reason = hr
            desired_blocked = "missing_view_state"
            details = {
                "stability_score": stability_score,
                "range_m": range_m,
                "visibility_score": visibility_score,
                "frame_id": frame_id,
            }
            mode, reason, gate_dict = self._apply_runtime_policy(
                desired_mode=desired_mode,
                desired_reason=desired_reason,
                desired_blocked_by=desired_blocked,
                details=details,
            )
            return mode, reason, gate_dict

        # normalize
        stability_score = float(stability_score)
        range_m = float(range_m)
        visibility_score = 0.75 if visibility_score is None else float(visibility_score)

        # -----------------------------
        # 1) Hard gates (semantic)
        # -----------------------------
        # 1.1 too close => SUSPENDED (C territory)
        too_close_cfg = self.config.get("hard_gates", {}).get("distance_range", {}) or {}
        if range_m <= float(too_close_cfg.get("range_min_m", 2.0)):
            desired_mode = "SUSPENDED"
            desired_reason = str(too_close_cfg.get("human_readable", "观察距离过近，进入 C 主导范围"))
            desired_blocked = "too_close"
            details = {"range_m": range_m, "frame_id": frame_id}
            return self._apply_runtime_policy(desired_mode, desired_reason, desired_blocked, details)

        # 1.2 camera shake => hysteresis around stability_score
        shake_cfg = self.config.get("hard_gates", {}).get("camera_stability", {}) or {}
        enter_thr = float(shake_cfg.get("enter_threshold", 0.65))
        exit_thr = float(shake_cfg.get("exit_threshold", 0.55))
        # Enforce ordering (defensive)
        if exit_thr > enter_thr:
            exit_thr = enter_thr

        # Determine desired based on hysteresis + last mode
        # If we are ACTIVE, only exit when stability < exit_thr.
        # If we are not ACTIVE, only enter when stability >= enter_thr.
        if self.state.last_mode == "ACTIVE":
            if stability_score < exit_thr:
                desired_mode = "SUSPENDED"
                desired_reason = str(shake_cfg.get("human_readable", "镜头晃动过大，无法稳定感知环境"))
                desired_blocked = "camera_shake"
            else:
                desired_mode = "ACTIVE"
                desired_reason = "B2 正常工作"
                desired_blocked = None
        else:
            if stability_score >= enter_thr:
                desired_mode = "ACTIVE"
                desired_reason = "B2 正常工作"
                desired_blocked = None
            else:
                desired_mode = "SUSPENDED"
                desired_reason = str(shake_cfg.get("human_readable", "镜头晃动过大，无法稳定感知环境"))
                desired_blocked = "camera_shake"

        # -----------------------------
        # 2) Soft gates (semantic)
        # -----------------------------
        if desired_mode == "ACTIVE" and (not evidence_ok):
            soft_cfg = self.config.get("soft_gates", {}).get("evidence_continuity", {}) or {}
            desired_mode = "READ_ONLY"
            desired_reason = str(soft_cfg.get("human_readable", "证据尚未稳定，仅允许只读"))
            desired_blocked = "insufficient_evidence"

        details = {
            "stability_score": stability_score,
            "range_m": range_m,
            "visibility_score": visibility_score,
            "hysteresis": {
                "enter_threshold": enter_thr,
                "exit_threshold": exit_thr,
                "rule": "ACTIVE exits if stability < exit_threshold; non-ACTIVE enters if stability >= enter_threshold",
            },
            "frame_id": frame_id,
        }

        return self._apply_runtime_policy(desired_mode, desired_reason, desired_blocked, details)

    # -----------------------------
    # Runtime Policy (anti-jitter)
    # -----------------------------
    def _apply_runtime_policy(
        self,
        desired_mode: str,
        desired_reason: str,
        desired_blocked_by: Optional[str],
        details: Dict[str, Any],
    ) -> Tuple[str, str, Dict[str, Any]]:
        desired_mode = str(desired_mode).upper()

        cfg = self.config.get("runtime_policy", {}) or {}
        cooldown_after_switch = int(cfg.get("cooldown_frames_after_switch", 15))
        min_hold = cfg.get("min_hold_frames", {}) or {}
        min_hold_active = int(min_hold.get("ACTIVE", 20))
        min_hold_read_only = int(min_hold.get("READ_ONLY", 10))
        min_hold_suspended = int(min_hold.get("SUSPENDED", 10))

        # Update residence each call
        self.state.residence_frames += 1
        if self.state.cooldown_remaining > 0:
            self.state.cooldown_remaining -= 1

        current_mode = self.state.last_mode

        # Decide if switching is allowed
        transition_blocked_by = None
        if desired_mode != current_mode:
            # 1) Cooldown blocks any switch
            if self.state.cooldown_remaining > 0:
                transition_blocked_by = "cooldown"
                self.state.cooldown_hits += 1
                desired_mode = current_mode
                desired_reason = "切换冷却中，保持当前模式"
                desired_blocked_by = self.state.last_blocked_by

            # 2) Min-hold blocks early switch
            if transition_blocked_by is None:
                min_req = {
                    "ACTIVE": min_hold_active,
                    "READ_ONLY": min_hold_read_only,
                    "SUSPENDED": min_hold_suspended,
                }.get(current_mode, 10)
                if self.state.residence_frames < min_req:
                    transition_blocked_by = "min_hold"
                    self.state.min_hold_hits += 1
                    desired_mode = current_mode
                    desired_reason = f"最小驻留未满足（{self.state.residence_frames}/{min_req}帧），保持当前模式"
                    desired_blocked_by = self.state.last_blocked_by

        # If we kept current mode because of hysteresis (semantic), record it
        # We treat "hysteresis_hold" as: desired_mode determined by hysteresis rule but equals current mode
        hysteresis_hold = False
        if desired_mode == current_mode and details.get("hysteresis"):
            # If near boundary, likely held by hysteresis; we do not overfit here—just record "eligible"
            hysteresis_hold = True

        # Apply switch if allowed and changed
        switched = False
        if desired_mode != self.state.last_mode:
            switched = True
            self.state.last_mode = desired_mode
            self.state.last_blocked_by = desired_blocked_by
            self.state.residence_frames = 0
            self.state.cooldown_remaining = cooldown_after_switch
        else:
            self.state.last_blocked_by = desired_blocked_by

        if hysteresis_hold and (not switched) and transition_blocked_by is None:
            # only count hysteresis holds when no runtime policy blocked switching
            self.state.hysteresis_hold_hits += 1

        mode = self.state.last_mode
        reason = desired_reason

        gate_eval = {
            "can_trigger": mode == "ACTIVE",
            "blocked_by": desired_blocked_by if mode != "ACTIVE" else None,
            "human_readable": reason if mode != "ACTIVE" else "B2 正常工作",
            "details": details,
            "runtime_profile": {
                "mode": mode,
                "transition": {
                    "desired_mode": desired_mode,
                    "switched": switched,
                    "blocked_by": transition_blocked_by,
                    "residence_frames": self.state.residence_frames,
                    "cooldown_remaining": self.state.cooldown_remaining,
                },
                "counters": {
                    "hysteresis_hold_hits": self.state.hysteresis_hold_hits,
                    "min_hold_hits": self.state.min_hold_hits,
                    "cooldown_hits": self.state.cooldown_hits,
                },
            },
        }

        return mode, reason, gate_eval
