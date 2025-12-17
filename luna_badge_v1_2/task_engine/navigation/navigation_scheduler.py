"""
NavigationScheduler: 导航调度器

负责将导航事件转换为 TTS_ROUTER_* actions，并推送给 DecisionCore
"""

# ======================================================================
# [v1.4.9 P0-1 FREEZE] User-visible behavior mapping (DO NOT CHANGE)
#
# This module defines the canonical mapping from navigation events to
# TTS_ROUTER_* actions. Any behavior change here is considered a contract
# change and requires a version bump.
#
# Frozen mappings:
# - TurnEvent            -> Action(type="TTS_ROUTER_TURN")
# - StraightEvent        -> Action(type="TTS_ROUTER_STRAIGHT")
# - ObstacleEvent:
#     * distance < 1.5m  -> Action(type="TTS_ROUTER_SAFETY",
#                                 text="前方危险，请立即停下")
#     * distance >= 1.5m -> Action(type="TTS_ROUTER_OBSTACLE")
#
# Frozen parameters / invariants:
# - Safety threshold: 1.5 meters
# - Safety text: "前方危险，请立即停下" (must not change semantics)
# - Distances in payload are int meters (int(event.distance))
# ======================================================================

from dataclasses import dataclass
from typing import Optional, Dict, Any
from decision_core.decision_core import DecisionCore, Action


@dataclass
class TurnEvent:
    """转弯事件"""
    direction: str  # "left", "right", "slight_left", "hard_left" 等
    distance: float  # 距离（米）


@dataclass
class StraightEvent:
    """直行事件"""
    distance: float  # 距离（米）


@dataclass
class ObstacleEvent:
    """障碍物事件"""
    obstacle_type: str  # "human", "object", "stairs" 等
    distance: float  # 距离（米）
    direction: Optional[str] = None  # "front", "left", "right" 等


class NavigationScheduler:
    """
    导航调度器

    将导航事件转换为 TTS_ROUTER_* actions，并推送给 DecisionCore
    """

    def __init__(self, decision_core: Optional[DecisionCore] = None):
        """
        初始化导航调度器

        Args:
            decision_core: DecisionCore 实例（可选，如果提供则直接调用，否则需要外部设置）
        """
        self.core = decision_core

    def set_decision_core(self, decision_core: DecisionCore) -> None:
        """
        设置 DecisionCore 实例

        Args:
            decision_core: DecisionCore 实例
        """
        self.core = decision_core

    def process_turn_event(self, event: TurnEvent) -> None:
        """
        处理转弯事件

        Args:
            event: TurnEvent 对象
        """
        if not self.core:
            # 如果没有 DecisionCore，直接使用 TTS Router（向后兼容）
            from task_engine.tts.router_facade import get_tts_router_facade
            router = get_tts_router_facade()
            router.route_turn(
                direction=event.direction,
                distance=int(event.distance) if event.distance else None
            )
            return

        # Step 10: 转换为 TTS_ROUTER_TURN action
        action = Action(
            type="TTS_ROUTER_TURN",
            payload={
                "direction": event.direction,
                "distance": int(event.distance) if event.distance else None
            }
        )
        self.core.handle_action(action)

    def process_straight_event(self, event: StraightEvent) -> None:
        """
        处理直行事件

        Args:
            event: StraightEvent 对象
        """
        if not self.core:
            # 如果没有 DecisionCore，直接使用 TTS Router（向后兼容）
            from task_engine.tts.router_facade import get_tts_router_facade
            router = get_tts_router_facade()
            router.route_straight(
                distance=int(event.distance) if event.distance else None
            )
            return

        # Step 10: 转换为 TTS_ROUTER_STRAIGHT action
        action = Action(
            type="TTS_ROUTER_STRAIGHT",
            payload={
                "distance": int(event.distance) if event.distance else None
            }
        )
        self.core.handle_action(action)

    def process_obstacle_event(self, event: ObstacleEvent) -> None:
        """
        处理障碍物事件

        Args:
            event: ObstacleEvent 对象
        """
        # Step 11: 如果障碍物距离 < 1.5m，使用安全播报（TTS_ROUTER_SAFETY）
        if event.distance < 1.5:
            if not self.core:
                # 如果没有 DecisionCore，直接使用 TTS Router（向后兼容）
                from task_engine.tts.router_facade import get_tts_router_facade
                router = get_tts_router_facade()
                router.route_safety(
                    text="前方危险，请立即停下",
                    meta={"obstacle_type": event.obstacle_type, "distance": event.distance}
                )
                return

            # Step 11: 转换为 TTS_ROUTER_SAFETY action（高优先级安全播报）
            action = Action(
                type="TTS_ROUTER_SAFETY",
                payload={
                    "text": "前方危险，请立即停下",
                    "meta": {
                        "obstacle_type": event.obstacle_type,
                        "distance": event.distance,
                        "direction": event.direction or "前方"
                    }
                }
            )
            self.core.handle_action(action)
            return

        # 普通障碍物事件（距离 >= 1.5m），使用普通障碍物播报
        if not self.core:
            # 如果没有 DecisionCore，直接使用 TTS Router（向后兼容）
            from task_engine.tts.router_facade import get_tts_router_facade
            router = get_tts_router_facade()
            router.route_obstacle_warning(
                direction=event.direction or "前方",
                distance_m=int(event.distance) if event.distance else None,
                obstacle_type=event.obstacle_type
            )
            return

        # Step 10: 转换为 TTS_ROUTER_OBSTACLE action
        action = Action(
            type="TTS_ROUTER_OBSTACLE",
            payload={
                "type": event.obstacle_type,
                "distance": int(event.distance) if event.distance else None,
                "direction": event.direction or "前方"
            }
        )
        self.core.handle_action(action)

