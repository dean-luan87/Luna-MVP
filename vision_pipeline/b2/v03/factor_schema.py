# vision_pipeline/b2/v03/factor_schema.py
# Factor Snapshot 标准化字段定义
# 关键场景：电梯 / 集市 / 对向骑车

from __future__ import annotations
from typing import Dict, Any, Optional, Literal


# =========================
# 场景一：电梯（Elevator）
# =========================

def build_env_elevator(
    scene_type: Literal["indoor", "outdoor", "unknown"],
    enclosure_type: Literal["open", "semi", "enclosed"],
    enclosure_confidence: float,
    is_elevator: bool,
    elevator_confidence: float,
    elevator_state: Literal["entering", "inside", "exiting", "unknown"],
) -> Dict[str, Any]:
    """
    电梯场景的 env 因子结构
    """
    return {
        "scene_type": scene_type,
        "enclosure": {
            "type": enclosure_type,
            "confidence": enclosure_confidence,
        },
        "vertical_transport": {
            "is_elevator": is_elevator,
            "confidence": elevator_confidence,
            "state": elevator_state,
        },
    }


def build_motion_elevator(
    speed: float,
    acc_z: Optional[float],
    motion_pattern: Literal["steady", "vertical_shift", "stop_start"],
) -> Dict[str, Any]:
    """
    电梯场景的 motion 辅助因子
    """
    return {
        "speed": speed,
        "acc_z": acc_z,
        "motion_pattern": motion_pattern,
    }


# =========================
# 场景二：集市 / 人群密集流动（Market / Crowd Surge）
# =========================

def build_people_market(
    count: Optional[int],
    density_value: float,
    density_delta: float,
    motion_type: Literal["static", "bidirectional", "crossing", "chaotic"],
    motion_confidence: float,
    is_market: bool,
    market_confidence: float,
) -> Dict[str, Any]:
    """
    集市场景的 people 因子结构
    """
    return {
        "count": count,
        "density": {
            "value": density_value,
            "delta": density_delta,
        },
        "motion_pattern": {
            "type": motion_type,
            "confidence": motion_confidence,
        },
        "crowd_scene": {
            "is_market": is_market,
            "confidence": market_confidence,
        },
    }


def build_env_market(
    has_stalls: bool,
    has_tents: bool,
    structures_confidence: float,
) -> Dict[str, Any]:
    """
    集市场景的 env 辅助字段
    """
    return {
        "temporary_structures": {
            "stalls": has_stalls,
            "tents": has_tents,
            "confidence": structures_confidence,
        },
    }


# =========================
# 场景三：对向骑车 / 横穿（Opposite Cycling / Crossing）
# =========================

def build_people_crossing(
    count: Optional[int],
    density_value: float,
    motion_type: Literal["unidirectional", "bidirectional", "crossing"],
    motion_confidence: float,
    opposite_flow_detected: bool,
    opposite_flow_confidence: float,
) -> Dict[str, Any]:
    """
    对向骑车场景的 people 因子结构
    """
    return {
        "count": count,
        "density": {
            "value": density_value,
            "delta": 0.0,  # 对向流不一定是密度变化
        },
        "motion_pattern": {
            "type": motion_type,
            "confidence": motion_confidence,
        },
        "opposite_flow": {
            "detected": opposite_flow_detected,
            "confidence": opposite_flow_confidence,
        },
    }


def build_event_crossing(
    event_type: Optional[Literal["near_miss", "collision_risk"]],
    severity: float,
    triggered_by: str = "people_motion",
) -> Dict[str, Any]:
    """
    对向骑车升级为风险事件的 event 因子结构
    """
    return {
        "type": event_type,
        "severity": severity,
        "triggered_by": triggered_by,
    }


# =========================
# 标准字段结构说明（用于文档/标注共识）
# =========================

FACTOR_SCHEMA_DOC = """
Factor Snapshot 标准化字段定义

一、env 因子（环境）
-------------------
- scene_type: "indoor" | "outdoor" | "unknown"
- enclosure.type: "open" | "semi" | "enclosed"
- vertical_transport.is_elevator: bool
- vertical_transport.state: "entering" | "inside" | "exiting" | "unknown"
- temporary_structures.stalls: bool
- temporary_structures.tents: bool

二、people 因子（人群）
-------------------
- count: int | None
- density.value: float（相对密度）
- density.delta: float（相比前一段时间的变化）
- motion_pattern.type: "static" | "bidirectional" | "crossing" | "chaotic" | "unidirectional"
- motion_pattern.confidence: float
- crowd_scene.is_market: bool
- crowd_scene.confidence: float
- opposite_flow.detected: bool
- opposite_flow.confidence: float

三、motion 因子（运动）
-------------------
- speed: float
- acc_z: float | None（垂直加速度）
- motion_pattern: "steady" | "vertical_shift" | "stop_start"

四、event 因子（事件）
-------------------
- type: None | "near_miss" | "collision_risk"
- severity: float（0~1）
- triggered_by: str（触发来源）

关键场景映射：
- 电梯：env.vertical_transport.is_elevator = True
- 集市：people.crowd_scene.is_market = True + people.motion_pattern.type = "crossing"
- 对向骑车：people.motion_pattern.type = "bidirectional" + people.opposite_flow.detected = True
"""

