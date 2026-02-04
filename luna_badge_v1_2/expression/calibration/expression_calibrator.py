"""
Expression Calibrator (C-2.3)

表达校准器

这是 C-2 的灵魂

你刚才说的这些：
- "5 米" → "几步远"
- "右转" → "右手边"
- 玩具说米，视障说步

👉 全部在这里完成
"""

from typing import Optional
from ..contracts.navigation_contract import NavigationExpressionContract
from ..embodiment.embodiment_context import EmbodimentContext
from ..embodiment.embodiment_types import EmbodimentType
from ..scene.scene_context import SceneContext
from ..scene.scene_types import SceneType
from .expression_params import ExpressionParams


class ExpressionCalibrator:
    """
    表达校准器
    
    职责：
    - 将 Contract 转换为 ExpressionParams
    - 根据 embodiment + scene 进行"换算"
    - 一期：规则驱动
    - 二期：引入"用户理解度""语言熟悉度"
    """
    
    def __init__(self, steps_per_meter: float = 1.4):
        """
        初始化校准器
        
        Args:
            steps_per_meter: 每米步数（默认 1.4，约 0.7 米/步）
        """
        self.steps_per_meter = steps_per_meter
    
    def calibrate(
        self,
        contract: NavigationExpressionContract,
        embodiment_ctx: EmbodimentContext,
        scene_ctx: SceneContext
    ) -> ExpressionParams:
        """
        校准表达参数
        
        示例规则：
        - BLIND_BADGE + NAVIGATION_SHORT:
            distance_unit = "steps"
            direction_reference = "egocentric"
        - TOY:
            distance_unit = "meters"
            direction_reference = "absolute"
        
        Args:
            contract: 导航合约
            embodiment_ctx: 身体形态上下文
            scene_ctx: 场景上下文
            
        Returns:
            ExpressionParams: 表达参数
        """
        # 基础参数
        action = contract.action
        distance_value = contract.distance_m
        
        # 根据身体类型和场景确定单位
        distance_unit, distance_value_calibrated = self._calibrate_distance(
            distance_value,
            embodiment_ctx,
            scene_ctx
        )
        
        # 根据身体类型确定方向参考系
        direction_reference = self._calibrate_direction_reference(
            embodiment_ctx,
            scene_ctx
        )
        
        # 横向提示（如果有 offset_m）
        lateral_hint = contract.offset_m is not None and abs(contract.offset_m) > 0.5
        
        # 紧急程度（根据 confidence 和场景）
        urgency_level = self._calibrate_urgency(
            contract.confidence,
            scene_ctx
        )
        
        return ExpressionParams(
            action=action,
            distance_value=distance_value_calibrated,
            distance_unit=distance_unit,
            direction_reference=direction_reference,
            lateral_hint=lateral_hint,
            urgency_level=urgency_level
        )
    
    def _calibrate_distance(
        self,
        distance_m: float,
        embodiment_ctx: EmbodimentContext,
        scene_ctx: SceneContext
    ) -> tuple[str, float]:
        """
        校准距离单位和数值
        
        Args:
            distance_m: 距离（米）
            embodiment_ctx: 身体形态上下文
            scene_ctx: 场景上下文
            
        Returns:
            tuple[str, float]: (距离单位, 校准后的距离值)
        """
        # BLIND_BADGE + NAVIGATION_SHORT: 使用步数
        if (embodiment_ctx.embodiment == EmbodimentType.BLIND_BADGE and
            scene_ctx.scene == SceneType.NAVIGATION_SHORT):
            distance_steps = distance_m * self.steps_per_meter
            return "steps", round(distance_steps, 1)
        
        # 其他情况：使用米
        return "meters", distance_m
    
    def _calibrate_direction_reference(
        self,
        embodiment_ctx: EmbodimentContext,
        scene_ctx: SceneContext
    ) -> str:
        """
        校准方向参考系
        
        Args:
            embodiment_ctx: 身体形态上下文
            scene_ctx: 场景上下文
            
        Returns:
            str: 方向参考系（"egocentric" | "absolute"）
        """
        # BLIND_BADGE: 使用自我中心（egocentric）
        if embodiment_ctx.embodiment == EmbodimentType.BLIND_BADGE:
            return "egocentric"
        
        # TOY / MOBILE_APP: 使用绝对方向（absolute）
        if embodiment_ctx.embodiment in {EmbodimentType.TOY, EmbodimentType.MOBILE_APP}:
            return "absolute"
        
        # 默认：自我中心
        return "egocentric"
    
    def _calibrate_urgency(
        self,
        confidence: float,
        scene_ctx: SceneContext
    ) -> int:
        """
        校准紧急程度（1-5）
        
        Args:
            confidence: 置信度
            scene_ctx: 场景上下文
            
        Returns:
            int: 紧急程度（1-5）
        """
        # 安全模式：最高紧急度
        if scene_ctx.scene == SceneType.SAFE_MODE:
            return 5
        
        # 根据置信度确定紧急度
        if confidence >= 0.9:
            return 4
        elif confidence >= 0.7:
            return 3
        elif confidence >= 0.5:
            return 2
        else:
            return 1
