# -*- coding: utf-8 -*-
"""
风险评估器（Risk Assessor）

v1.8.3: 最小化风险判断模块（安全版 + 参数化）

职责：
- 只判断，不说话
- 不引入 TTS
- 不引入 speech_gate
- 只是一个"判断器"

关键原则：
- 感知危险（LV2）≠ 触发警报
- 只有当 时间/路径/行为 满足条件 → 强制升级 LV1
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, Dict
import logging

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """风险级别"""
    SAFE = 0
    POTENTIAL = 1   # LV2：潜在风险，只算不说
    IMMEDIATE = 2   # LV1：立即风险，强制发声


# v1.8.3: 威胁语义结构（只做结构接入，不改变行为）
class ThreatLevel(Enum):
    """威胁级别（语义层）"""
    LV2 = "potential"  # 潜在威胁环境
    LV1 = "imminent"   # 即时威胁


@dataclass
class ThreatAssessment:
    """
    威胁评估（语义标注）

    v1.8.3: 威胁语义结果（不等于风险触发）
    - LV2: 潜在威胁，仅用于后台建模/警觉度/导航建议，不触发播报
    - LV1: 即将发生威胁，语义上等同现有 risk_result.level=IMMEDIATE
    """
    level: ThreatLevel
    risk_type: str  # 'water_edge' / 'road' / 'obstacle' / ...
    reason: str     # 威胁原因描述（debug/建模用途）


@dataclass
class RiskResult:
    """风险评估结果"""
    level: RiskLevel
    reason: Optional[str] = None  # 'water_edge' / 'road' / 'obstacle' / ...
    distance: Optional[float] = None  # meters
    ttc: Optional[float] = None  # time_to_collision (seconds)
    # v1.8.3: 威胁语义标注（向后兼容，默认 None）
    threat: Optional[ThreatAssessment] = None


class MotionState:
    """运动状态（简化版）"""

    def __init__(self):
        self.is_moving_towards_edge: bool = False
        self.estimated_ttc: Optional[float] = None
        self.estimated_distance: Optional[float] = None


# -----------------------------
# v1.8.3: 参数化配置（安全版）
# -----------------------------

@dataclass
class UpgradeCondition:
    """
    LV2 -> LV1 升级条件（最小集）
    - v1.8.3 默认：需要接近 + ttc<=3.0
    """
    ttc_threshold: float = 3.0
    require_moving_towards: bool = True


@dataclass
class ThreatStateConfig:
    """
    单一风险类型的配置
    - keywords: 识别 LV2 的关键词
    - upgrade: 何时升级 LV1
    """
    risk_type: str
    keywords: List[str]
    upgrade: UpgradeCondition


@dataclass
class RiskConfig:
    """
    风险评估配置（最小可配置版本）
    - 支持按风险类型独立配置 keywords + LV1 升级阈值
    - v1.8.3 默认值与旧逻辑一致
    """
    threat_states: Dict[str, ThreatStateConfig]

    @staticmethod
    def default() -> "RiskConfig":
        water_keywords = ["water", "水", "河", "湖", "池", "海", "edge", "边缘"]
        road_keywords = ["road", "路", "马路", "街道", "car", "车", "traffic", "交通"]

        return RiskConfig(
            threat_states={
                "water_edge": ThreatStateConfig(
                    risk_type="water_edge",
                    keywords=water_keywords,
                    upgrade=UpgradeCondition(ttc_threshold=3.0, require_moving_towards=True),
                ),
                "road": ThreatStateConfig(
                    risk_type="road",
                    keywords=road_keywords,
                    upgrade=UpgradeCondition(ttc_threshold=3.0, require_moving_towards=True),
                ),
            }
        )


def _match_keywords(all_text: str, keywords: List[str]) -> bool:
    # 统一：关键词匹配只做 substring 检测（v1.8.3 最小实现）
    return any(k.lower() in all_text for k in keywords)


def _assess_single_type(
    risk_type: str,
    detected: bool,
    motion_state: Optional[MotionState],
    cfg: ThreatStateConfig,
) -> Optional[RiskResult]:
    """
    针对单一 risk_type 的最小评估：
    - detected=False -> None（表示未命中该类型）
    - detected=True -> 返回 LV2 或 LV1
    """
    if not detected:
        return None

    upgrade = cfg.upgrade
    has_motion = motion_state is not None

    # v1.8.3：如果要求"接近"，但 motion_state 缺失或未接近，则不能 LV1
    moving_ok = True
    if upgrade.require_moving_towards:
        moving_ok = bool(has_motion and motion_state.is_moving_towards_edge)

    # LV1：需要满足 moving_ok + ttc<=threshold（且 ttc 存在）
    if moving_ok and has_motion and motion_state.estimated_ttc is not None:
        if motion_state.estimated_ttc <= upgrade.ttc_threshold:
            return RiskResult(
                level=RiskLevel.IMMEDIATE,
                reason=risk_type,
                ttc=motion_state.estimated_ttc,
                distance=motion_state.estimated_distance,
                threat=ThreatAssessment(
                    level=ThreatLevel.LV1,
                    risk_type=risk_type,
                    reason=f"moving_towards={motion_state.is_moving_towards_edge}, "
                           f"ttc={motion_state.estimated_ttc:.2f} <= {upgrade.ttc_threshold:.2f}"
                )
            )

    # LV2：命中语义但不满足 LV1（不触发警报）
    distance = motion_state.estimated_distance if has_motion else None
    return RiskResult(
        level=RiskLevel.POTENTIAL,
        reason=risk_type,
        distance=distance,
        threat=ThreatAssessment(
            level=ThreatLevel.LV2,
            risk_type=risk_type,
            reason="detected but not imminent"
        )
    )


def assess_risk(
    scene_state: Any,
    motion_state: Optional[MotionState] = None,
    config: Optional[RiskConfig] = None
) -> RiskResult:
    """
    v1.8.3: 风险评估函数（安全版 + 参数化）

    只判断，不说话

    Args:
        scene_state: 场景状态对象（需要包含 objects 和 signs）
        motion_state: 运动状态（可选）
        config: 风险配置（可选）。None 时使用默认配置（等同旧逻辑）。

    Returns:
        RiskResult: 风险评估结果
    """
    cfg = config or RiskConfig.default()

    # 提取场景信息
    objects = scene_state.objects if hasattr(scene_state, "objects") else []
    signs = scene_state.signs if hasattr(scene_state, "signs") else []

    # 合并所有文本用于关键词检测
    all_text = " ".join(objects + signs).lower()

    # 评估顺序：water_edge -> road
    # 说明：保持你原先的优先级（先水后路），避免行为变化
    water_cfg = cfg.threat_states.get("water_edge")
    if water_cfg:
        detected_water = _match_keywords(all_text, water_cfg.keywords)
        r = _assess_single_type("water_edge", detected_water, motion_state, water_cfg)
        if r is not None:
            return r

    road_cfg = cfg.threat_states.get("road")
    if road_cfg:
        detected_road = _match_keywords(all_text, road_cfg.keywords)
        r = _assess_single_type("road", detected_road, motion_state, road_cfg)
        if r is not None:
            return r

    # 安全
    return RiskResult(level=RiskLevel.SAFE)
