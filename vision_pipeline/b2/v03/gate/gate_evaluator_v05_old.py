# vision_pipeline/b2/v03/gate/gate_evaluator_v05.py
"""
B2 Gate v0.5 - Gate Evaluator（最终工程版）

目标：
- 纯函数 + 配置驱动
- 每一帧都能生成完整 Gate Trace
- 不依赖 B2 具体实现，可复用

============================================================
Gate Authority Table — B2 v0.4.2 (Frozen)
============================================================

Gate 决策维度（只此四项）：

1. 是否允许 B 输出（can_trigger）
2. B 的运行模式（ACTIVE / READ_ONLY / SUSPENDED）
3. 是否允许写入 timeline / trace
4. 是否允许向 C 发送 advisory

------------------------------------------------------------
Gate Mode 权限表
------------------------------------------------------------

[ACTIVE]
- B 可以计算 impact
- B 可以输出 advisory（advisory_only = True）
- B 可以写 timeline / trace
- B 不得确认风险（禁止 certainty 语义）
- B 不得覆盖 C 的即时判断

[READ_ONLY]
- B 可以计算 impact（用于内部观察）
- B **不得**向 C 发送 advisory
- B **不得**写 timeline
- B **只允许**写 trace（用于审计）
- 用途：证据未稳定、视角不充分

[SUSPENDED]
- B **不得**计算 impact
- B **不得**输出任何 decision
- B **不得**写 timeline
- B **只写** gate trace（说明为什么沉默）
- 用途：视角污染 / 距离过近 / 严重不可信

------------------------------------------------------------
Gate 绝对裁决项（任何情况下优先）
------------------------------------------------------------

- camera_shake            → SUSPENDED
- too_close (进入 C 主导) → SUSPENDED
- missing_view_state      → READ_ONLY（v0.4.2 起）
- insufficient_evidence   → READ_ONLY

------------------------------------------------------------
禁止事项（一旦出现 = 架构错误）
------------------------------------------------------------

- Gate = SUSPENDED 但仍有 B 输出
- Gate = READ_ONLY 但写 timeline
- Gate 未 ACTIVE 却向 C 发送 advisory
- 没有 view_state 却 ACTIVE
- B 输出"确认性风险结论"

============================================================

一句话架构裁定：
Gate decides whether B may speak, and how.
B suggests possible risks.
C verifies and decides action.

（中文版：Gate 决定能不能说、怎么说；B 负责提醒；C 负责确认与行动。）

详细权限表：见 GATE_AUTHORITY_TABLE.md

后续版本只允许 新增，不允许修改已有语义
"""

from typing import Dict, Any, Tuple, Optional
import yaml
import time
from pathlib import Path


class GateEvaluatorV05:
    """
    B2 Gate 评估器 v0.5（最终版）
    
    分层设计：
    - Layer A: Hard Gate（一票否决，SUSPENDED）
    - Layer B: Soft Gate（降级，READ_ONLY）
    - 全部通过 → ACTIVE
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化 Gate 评估器
        
        :param config_path: gate_config.yaml 路径，如果为 None 则使用默认配置
        """
        if config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                self.cfg = yaml.safe_load(f)
        else:
            # 使用默认配置
            self.cfg = self._get_default_config()
        
        self.last_trigger_ts: float = -1e9
        
        # v0.5 minimal ignition state (DO NOT REMOVE)
        self._stable_frame_count = 0
        self._last_active_ts = None
        self.current_mode = "READ_ONLY"
        self.last_mode_change_ts = None
        
        # v0.5 frozen constants
        self._MIN_STABLE_FRAMES = 30        # ~1s @30fps
        self._ACTIVE_MAX_DURATION = 1.0    # seconds
        
        # =====================================================
        # v0.5 Patch D: Hysteresis counters (Gate 抖动抑制)
        # =====================================================
        self._enter_active_counter = 0  # READ_ONLY → ACTIVE 计数器
        self._exit_active_counter = 0   # ACTIVE → READ_ONLY 计数器
        
        # v0.5 frozen thresholds (DO NOT CHANGE)
        self.ENTER_ACTIVE_THRESHOLD = 5   # 连续 5 帧满足条件才进入 ACTIVE
        self.EXIT_ACTIVE_THRESHOLD = 10   # 连续 10 帧不满足条件才退出 ACTIVE
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置（如果配置文件不存在）"""
        return {
            "version": "0.5",
            "hard_gates": {
                "camera_stability": {
                    "enabled": True,
                    "stability_score_min": 0.60,
                    "block_reason": "camera_shake",
                    "human_readable": "镜头晃动过大，无法稳定感知环境"
                },
                "camera_pose": {
                    "enabled": True,
                    "pitch_deg_max": 20,
                    "roll_deg_max": 15,
                    "block_reason": "camera_tilt",
                    "human_readable": "镜头角度异常（过度仰俯或倾斜）"
                },
                "distance_range": {
                    "enabled": True,
                    "min_m": 3.0,
                    "block_reason": "too_close",
                    "human_readable": "观察距离过近，进入 C 主导范围"
                },
                "visibility": {
                    "enabled": True,
                    "min_score": 0.40,
                    "block_reason": "low_visibility",
                    "human_readable": "当前视野可见度过低"
                },
                "runtime_yield": {
                    "enabled": True,
                    "block_reason": "yield_to_c",
                    "human_readable": "系统资源让渡给 C（性能或安全优先）"
                }
            },
            "soft_gates": {
                "evidence_continuity": {
                    "enabled": True,
                    "min_confirm_frames": 15,
                    "downgrade_reason": "insufficient_evidence",
                    "human_readable": "证据尚未稳定，仅允许只读"
                },
                "cooldown": {
                    "enabled": True,
                    "min_interval_sec": 3.0,
                    "downgrade_reason": "cooldown_active",
                    "human_readable": "处于冷却期，避免重复判断"
                },
                "confidence_floor": {
                    "enabled": True,
                    "min_final_confidence": 0.55,
                    "downgrade_reason": "low_confidence",
                    "human_readable": "整体置信度不足，仅记录不触发"
                }
            },
            "mode_mapping": {
                "hard_fail": "SUSPENDED",
                "soft_fail": "READ_ONLY",
                "pass": "ACTIVE"
            },
            "trace_labels": {
                "ACTIVE": "B2 正常工作",
                "READ_ONLY": "B2 只读运行（不产生新判断）",
                "SUSPENDED": "B2 暂停（视角或条件不可信）"
            }
        }
    
    # =========================
    # Public API
    # =========================
    def evaluate(
        self,
        *,
        stability_score: float,
        pitch_deg: float,
        roll_deg: float,
        range_m: float,
        visibility_score: float,
        allow_runtime: bool,
        evidence_frames: int,
        final_confidence: float,
        now_ts: float
    ) -> Tuple[str, Dict[str, Any]]:
        """
        评估 Gate 状态
        
        :param stability_score: 稳定性分数 (0.0 ~ 1.0)
        :param pitch_deg: 俯仰角（度）
        :param roll_deg: 横滚角（度）
        :param range_m: 距离（米）
        :param visibility_score: 可见度分数 (0.0 ~ 1.0)
        :param allow_runtime: 是否允许运行（资源检查）
        :param evidence_frames: 证据连续帧数
        :param final_confidence: 最终置信度 (0.0 ~ 1.0)
        :param now_ts: 当前时间戳
        :return: (gate_mode, gate_trace)
        """
        
        # ---------- Hard Gate ----------
        hard_fail = self._eval_hard_gate(
            stability_score,
            pitch_deg,
            roll_deg,
            range_m,
            visibility_score,
            allow_runtime
        )
        if hard_fail:
            # Hard Gate 失败，重置点火状态
            if self.current_mode == "ACTIVE":
                self.current_mode = "READ_ONLY"
                self._last_active_ts = None
            self._stable_frame_count = 0
            return "SUSPENDED", hard_fail
        
        # =================================================
        # v0.5 MINIMAL IGNITION LOGIC (NEW)
        # 在 Soft Gate 之前检查，允许短暂点火
        # =================================================
        
        is_stable = (
            stability_score is not None and stability_score >= 0.85 and
            visibility_score is not None and visibility_score >= 0.7 and
            range_m is not None and range_m >= 2.0
        )
        
        if is_stable:
            self._stable_frame_count += 1
        else:
            self._stable_frame_count = 0
        
        # =================================================
        # v0.5 Patch D: Hysteresis Logic (Gate 抖动抑制)
        # =================================================
        
        # -------------------------------------------------
        # ACTIVE → READ_ONLY (slow to exit)
        # -------------------------------------------------
        if self.current_mode == "ACTIVE":
            # 检查超时（原有逻辑）
            if self._last_active_ts is not None and (now_ts - self._last_active_ts) >= self._ACTIVE_MAX_DURATION:
                # 超时强制退出
                self.current_mode = "READ_ONLY"
                self.last_mode_change_ts = now_ts
                self._last_active_ts = None
                self._stable_frame_count = 0
                self._enter_active_counter = 0
                self._exit_active_counter = 0
                
                # 继续检查 Soft Gate
                soft_fail = self._eval_soft_gate(
                    evidence_frames,
                    final_confidence,
                    now_ts
                )
                if soft_fail:
                    return "READ_ONLY", soft_fail
                else:
                    return "READ_ONLY", {
                        "can_trigger": False,
                        "blocked_by": "active_timeout",
                        "details": {},
                        "human_readable": "ACTIVE 超时，自动回退 READ_ONLY",
                        "reason": "active_timeout"
                    }
            
            # Hysteresis: 检查是否应该退出 ACTIVE
            if not is_stable:
                self._exit_active_counter += 1
            else:
                self._exit_active_counter = 0  # 条件满足，重置计数器
            
            # 连续 EXIT_ACTIVE_THRESHOLD 帧不满足条件才退出
            if self._exit_active_counter >= self.EXIT_ACTIVE_THRESHOLD:
                self.current_mode = "READ_ONLY"
                self.last_mode_change_ts = now_ts
                self._exit_active_counter = 0
                self._enter_active_counter = 0
                self._last_active_ts = None
                
                # 继续检查 Soft Gate
                soft_fail = self._eval_soft_gate(
                    evidence_frames,
                    final_confidence,
                    now_ts
                )
                if soft_fail:
                    return "READ_ONLY", soft_fail
                else:
                    return "READ_ONLY", {
                        "can_trigger": False,
                        "blocked_by": "hysteresis_exit",
                        "details": {
                            "exit_counter": self.EXIT_ACTIVE_THRESHOLD,
                        },
                        "human_readable": f"连续 {self.EXIT_ACTIVE_THRESHOLD} 帧不满足条件，退出 ACTIVE",
                        "reason": "hysteresis_exit"
                    }
            else:
                # 仍在 ACTIVE，但可能处于退出过程中
                self.last_trigger_ts = now_ts
                return "ACTIVE", {
                    "can_trigger": True,
                    "blocked_by": None,
                    "details": {
                        "stability": stability_score,
                        "visibility": visibility_score,
                        "range_m": range_m,
                        "exit_counter": self._exit_active_counter,
                        "exit_threshold": self.EXIT_ACTIVE_THRESHOLD,
                    },
                    "human_readable": self.cfg["trace_labels"]["ACTIVE"],
                    "reason": "active_ongoing"
                }
        
        # -------------------------------------------------
        # READ_ONLY → ACTIVE (hard to enter)
        # -------------------------------------------------
        if self.current_mode == "READ_ONLY":
            # 检查是否满足进入 ACTIVE 的条件
            can_enter_active = (
                is_stable and
                self._stable_frame_count >= self._MIN_STABLE_FRAMES and
                self._last_active_ts is None
            )
            
            if can_enter_active:
                self._enter_active_counter += 1
            else:
                self._enter_active_counter = 0  # 条件不满足，重置计数器
            
            # 连续 ENTER_ACTIVE_THRESHOLD 帧满足条件才进入
            if self._enter_active_counter >= self.ENTER_ACTIVE_THRESHOLD:
                self.current_mode = "ACTIVE"
                self.last_mode_change_ts = now_ts
                self._last_active_ts = now_ts
                self._stable_frame_count = 0
                self._enter_active_counter = 0
                self._exit_active_counter = 0
                
                self.last_trigger_ts = now_ts
                return "ACTIVE", {
                    "can_trigger": True,
                    "blocked_by": None,
                    "details": {
                        "stability": stability_score,
                        "visibility": visibility_score,
                        "range_m": range_m,
                        "enter_counter": self.ENTER_ACTIVE_THRESHOLD,
                    },
                    "human_readable": f"连续 {self.ENTER_ACTIVE_THRESHOLD} 帧满足条件，进入 ACTIVE",
                    "reason": "hysteresis_enter"
                }
        
        # ---------- Soft Gate ----------
        soft_fail = self._eval_soft_gate(
            evidence_frames,
            final_confidence,
            now_ts
        )
        if soft_fail:
            # 更新状态
            if self.current_mode != "READ_ONLY":
                self.current_mode = "READ_ONLY"
                self.last_mode_change_ts = now_ts
            return "READ_ONLY", soft_fail
        
        # ---------- PASS (所有检查通过) ----------
        # 如果到达这里，说明 Soft Gate 也通过了，但之前没有点火
        # 这种情况不应该发生（因为如果稳定，应该已经点火了）
        # 但为了安全，仍然返回 ACTIVE
        if self.current_mode != "ACTIVE":
            self.current_mode = "ACTIVE"
            self.last_mode_change_ts = now_ts
        
        self.last_trigger_ts = now_ts
        return "ACTIVE", {
            "can_trigger": True,
            "blocked_by": None,
            "details": {},
            "human_readable": self.cfg["trace_labels"]["ACTIVE"]
        }
    
    # =========================
    # Hard Gate
    # =========================
    def _eval_hard_gate(
        self,
        stability_score: float,
        pitch_deg: float,
        roll_deg: float,
        range_m: float,
        visibility_score: float,
        allow_runtime: bool
    ) -> Optional[Dict[str, Any]]:
        """
        评估 Hard Gate（Layer A）
        
        :return: 如果被阻止，返回 gate_trace 字典；否则返回 None
        """
        
        for name, g in self.cfg["hard_gates"].items():
            if not g.get("enabled", False):
                continue
            
            if name == "camera_stability":
                if stability_score < g["stability_score_min"]:
                    return self._blocked(g, {
                        "stability_score": stability_score
                    })
            
            if name == "camera_pose":
                if abs(pitch_deg) > g["pitch_deg_max"] or abs(roll_deg) > g["roll_deg_max"]:
                    return self._blocked(g, {
                        "pitch_deg": pitch_deg,
                        "roll_deg": roll_deg
                    })
            
            if name == "distance_range":
                if range_m < g["min_m"]:
                    return self._blocked(g, {
                        "range_m": range_m
                    })
            
            if name == "visibility":
                if visibility_score < g["min_score"]:
                    return self._blocked(g, {
                        "visibility_score": visibility_score
                    })
            
            if name == "runtime_yield":
                if not allow_runtime:
                    return self._blocked(g, {})
        
        return None
    
    # =========================
    # Soft Gate
    # =========================
    def _eval_soft_gate(
        self,
        evidence_frames: int,
        final_confidence: float,
        now_ts: float
    ) -> Optional[Dict[str, Any]]:
        """
        评估 Soft Gate（Layer B）
        
        :return: 如果被降级，返回 gate_trace 字典；否则返回 None
        """
        
        for name, g in self.cfg["soft_gates"].items():
            if not g.get("enabled", False):
                continue
            
            if name == "evidence_continuity":
                if evidence_frames < g["min_confirm_frames"]:
                    return self._downgraded(g, {
                        "evidence_frames": evidence_frames
                    })
            
            if name == "cooldown":
                if (now_ts - self.last_trigger_ts) < g["min_interval_sec"]:
                    return self._downgraded(g, {
                        "since_last": now_ts - self.last_trigger_ts
                    })
            
            if name == "confidence_floor":
                if final_confidence < g["min_final_confidence"]:
                    return self._downgraded(g, {
                        "final_confidence": final_confidence
                    })
        
        return None
    
    # =========================
    # Helpers
    # =========================
    def _blocked(self, gate_cfg: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成 Hard Gate 阻止的 trace
        """
        return {
            "can_trigger": False,
            "blocked_by": gate_cfg["block_reason"],
            "details": details,
            "human_readable": gate_cfg["human_readable"]
        }
    
    def _downgraded(self, gate_cfg: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成 Soft Gate 降级的 trace
        """
        return {
            "can_trigger": False,
            "blocked_by": gate_cfg["downgrade_reason"],
            "details": details,
            "human_readable": gate_cfg["human_readable"]
        }
    
    def record_trigger(self, now_ts: float):
        """
        记录触发时间（用于 cooldown）
        """
        self.last_trigger_ts = now_ts
