# -*- coding: utf-8 -*-
"""
决策控制器（Decision Controller）

v1.8.3a 阶段 C: 决策闭环（SPEAK / WAIT / YIELD / RISK_LV1）
v1.8.3: 集成风险评估（LV2 → LV1）

核心原则：
- 风险判断优先于一切调度
- LV2 只建模，不触发语音
- LV1 可抢占，但不打断用户说话
- threat 只作为"语义标注"，永不直接驱动 action
"""

from typing import Dict, Any, Optional
from core.scene_state_builder import SceneState
from core.speech_gate import SpeechGate
from core.risk_assessor import assess_risk, RiskLevel, RiskResult, MotionState


class UserState:
    """用户状态（简化版）"""
    def __init__(self):
        self.is_speaking = False


def decide(
    scene_state: SceneState,
    speech_gate: SpeechGate,
    user_state: UserState,
    motion_state: Optional[MotionState] = None
) -> Dict[str, Any]:
    """
    决策函数（v1.8.3a 阶段 C）

    说明：
    - 本函数只返回"决策意图"，不调用 TTS
    - threat 字段仅为语义标注，不影响 action 判断
    """

    # 决策 0：风险评估（最高优先级）
    risk = assess_risk(scene_state, motion_state)

    if risk.level == RiskLevel.IMMEDIATE:
        # LV1：立即风险（允许抢占，但不打断用户）
        if user_state.is_speaking:
            decision = {
                "action": "YIELD",
                "reason": "user_speaking_risk_pending",
                "risk_result": risk,
            }
        else:
            decision = {
                "action": "RISK_LV1",
                "reason": f"immediate_risk_{risk.reason}",
                "risk_result": risk,
                # 明确声明：LV1 不走 speech_gate
                "bypass_speech_gate": True,
            }

        # 威胁语义仅做透传，不参与决策
        decision["threat"] = risk.threat
        return decision

    elif risk.level == RiskLevel.POTENTIAL:
        # LV2：潜在威胁，只建模、不说话
        decision = {
            "action": "WAIT",
            "reason": f"lv2_risk_{risk.reason}",
            "wait_mode": "RISK_LV2_BACKGROUND",
            "risk_result": risk,
        }
        decision["threat"] = risk.threat
        return decision

    # 决策 1：用户优先
    if user_state.is_speaking:
        return {
            "action": "YIELD",
            "reason": "user_speaking"
        }

    # 决策 2：speech_gate 拦截
    can_speak, gate_reason = speech_gate.can_speak(
        scene_hash=scene_state.scene_hash,
        user_speaking=user_state.is_speaking
    )

    if not can_speak:
        return {
            "action": "WAIT",
            "reason": f"speech_gate_blocked_{gate_reason}"
        }

    # 决策 3：正常播报
    return {
        "action": "SPEAK",
        "reason": "normal_scene"
    }
