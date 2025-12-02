# core/navigation/direction_evaluator.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import logging
import math

from .scene_context import FrameContext
from .scene_node import SceneNode, SceneNodeType
from .scene_node_layer import SceneNodeLayer

logger = logging.getLogger(__name__)


@dataclass
class DirectionResult:
    """方向评估结果，供上层导航 FSM 使用。"""
    primary_direction: str              # 'forward' / 'left' / 'right' / 'stop'
    confidence: float                   # 0-1
    deviation_deg: float                # 与"理想朝向"的偏差（如果有）
    is_deviation: bool                  # 是否偏航
    reasons: List[str] = field(default_factory=list)

    # 方便播报用的一些字段
    recommended_action: Optional[str] = None  # "稍微向左调整", "保持直行", ...
    environment_hint: Optional[str] = None    # "前方走廊较窄", "左侧有人群" 等


class DirectionEvaluator:
    """
    D 模块：根据 FrameContext + SceneNodeLayer 得出"当前应采取的方向"。

    设计原则：
    - 只负责"方向 + 偏航"的判断，不直接做导航决策；
    - 上层导航 FSM 决定是否要触发"转弯 / 调头"等动作；
    - 保留简单、稳定、可解释的逻辑，日后可换成更复杂的策略。
    """

    def __init__(self, ideal_heading_deg: Optional[float] = None):
        """
        ideal_heading_deg: 理想方向（例如路径规划给出的朝向），
        如果为空，就仅使用运动 + 视觉信息来判断"相对变化"。
        """
        self.ideal_heading_deg = ideal_heading_deg
        self._last_result: Optional[DirectionResult] = None

    def sync_env(self, scene_nodes: List[SceneNode]) -> None:
        """
        与环境节点同步，为未来"场景驱动方向修正"预留接口。
        当前版本只做简单日志记录。
        """
        if not scene_nodes:
            return
        types = {n.type for n in scene_nodes}
        logger.debug("[DirectionEvaluator] sync_env node_types=%s",
                     {t.name for t in types})

    # --- 对外主入口 ---
    def evaluate(self, frame_ctx: FrameContext,
                 scene_layer: SceneNodeLayer) -> DirectionResult:
        """
        核心入口：给出当前方向、偏航情况和简单建议。
        """
        reasons: List[str] = []

        # 1. 根据运动状态判断"是否在移动"
        if not frame_ctx.is_moving_forward():
            primary = "stop"
            reasons.append("速度过低，判定为停滞")
            deviation, is_dev = 0.0, False
        else:
            # 2. 根据转向角速度判断"当前动作"
            turning = frame_ctx.turning_direction()
            if turning == "left":
                primary = "left"
                reasons.append("检测到向左转动")
            elif turning == "right":
                primary = "right"
                reasons.append("检测到向右转动")
            else:
                primary = "forward"
                reasons.append("未检测到显著转向，判定为直行")

            # 3. 计算与理想朝向的偏差（如果有）
            deviation, is_dev = self._compute_deviation(frame_ctx, reasons)

        # 4. 根据环境节点修正（非常轻量的 rule）
        env_hint = self._environment_hint(scene_layer, reasons)

        # 5. 置信度合成：运动 × 姿态 × 历史方向
        confidence = self._estimate_confidence(frame_ctx, primary, deviation, is_dev)

        # 6. 给播报链路一个简单的建议文案
        recommended = self._build_recommendation(primary, deviation, is_dev)

        result = DirectionResult(
            primary_direction=primary,
            confidence=confidence,
            deviation_deg=deviation,
            is_deviation=is_dev,
            reasons=reasons,
            recommended_action=recommended,
            environment_hint=env_hint,
        )
        self._last_result = result
        logger.debug("[DirectionEvaluator] result=%s", result)
        return result

    # --- 细节逻辑 ---

    def _compute_deviation(self, frame_ctx: FrameContext,
                           reasons: List[str]) -> Tuple[float, bool]:
        """与理想朝向的偏差（-180~180）。"""
        if self.ideal_heading_deg is None:
            reasons.append("无理想朝向，仅根据运动方向判断")
            return 0.0, False

        delta = frame_ctx.camera_pose.heading_deg - self.ideal_heading_deg
        while delta > 180:
            delta -= 360
        while delta < -180:
            delta += 360

        abs_delta = abs(delta)
        is_dev = abs_delta > 15.0  # 超过 15 度认为偏航
        reasons.append(f"与理想方向偏差 {abs_delta:.1f}°")
        if is_dev:
            reasons.append("偏差超过 15°，判定为偏航")
        return delta, is_dev

    def _environment_hint(self, scene_layer: SceneNodeLayer,
                          reasons: List[str]) -> Optional[str]:
        """
        使用场景节点给出一些简单提示（后续可扩展成更复杂的策略）。
        """
        # 示例：前方最近的台阶
        stair = scene_layer.get_nearest(SceneNodeType.STAIR)
        if stair and (stair.distance_m is not None) and stair.distance_m < 3.0:
            msg = f"前方约 {stair.distance_m:.1f} 米有台阶"
            reasons.append("环境提示：" + msg)
            return msg

        crowd = scene_layer.get_nearest(SceneNodeType.CROWD)
        if crowd and (crowd.distance_m is not None) and crowd.distance_m < 4.0:
            msg = "前方人流较密集，请注意减速"
            reasons.append("环境提示：" + msg)
            return msg

        return None

    def _estimate_confidence(
        self,
        frame_ctx: FrameContext,
        primary: str,
        deviation: float,
        is_deviation: bool,
    ) -> float:
        """
        粗略估算置信度：后续可以替换为更复杂的模型，这里先 rule-based。
        """
        base = 0.6 * frame_ctx.motion_confidence + 0.4 * frame_ctx.pose_confidence

        # 偏航时略微降低置信度
        if is_deviation:
            base *= 0.8

        # 如果方向和历史一致，提高一点
        if frame_ctx.previous_direction == primary:
            base += 0.1 * frame_ctx.previous_direction_confidence

        # 限制在 [0,1]
        base = max(0.05, min(1.0, base))
        return base

    def _build_recommendation(
        self,
        primary: str,
        deviation: float,
        is_deviation: bool,
    ) -> str:
        if primary == "stop":
            return "已停止移动，请确认是否继续前进"

        if not is_deviation:
            if primary == "forward":
                return "保持直行"
            if primary == "left":
                return "继续向左转"
            if primary == "right":
                return "继续向右转"

        # 存在偏航时，给更明确的推荐
        if deviation > 0:
            # 当前朝向比理想偏左
            return "请稍微向右调整方向"
        else:
            return "请稍微向左调整方向"

