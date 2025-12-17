"""
Delay Strategy

延迟策略（视角驱动）

⚠️ 禁止出现固定 800ms 这种绝对延迟
所有延迟必须基于视角状态动态计算
"""

from typing import Protocol
from .vision_rhythm_context import VisionRhythmContext
from ..calibration.expression_params import ExpressionParams


class DelayStrategy(Protocol):
    """
    延迟策略接口
    
    必须是「视角驱动函数」，不是常量
    """
    
    def compute_delay_ms(
        self,
        ctx: VisionRhythmContext,
        expression: ExpressionParams
    ) -> int:
        """
        计算延迟毫秒数
        
        Args:
            ctx: 视角节奏上下文
            expression: 表达参数
            
        Returns:
            int: 延迟毫秒数
        """
        ...


class VisionAdaptiveDelayStrategy:
    """
    视角自适应延迟策略
    
    延迟规则（必须基于视角状态）：
    - IF vision_state == TURNING → delay = 0 (or block)
    - IF visual_confidence < 0.6 → delay = 0
    - IF speed > 1.2 m/s → delay = 100 ms
    - IF speed 0.5–1.2 m/s → delay = 200 ms
    - IF speed < 0.5 m/s → delay = 300 ms
    """
    
    def compute_delay_ms(
        self,
        ctx: VisionRhythmContext,
        expression: ExpressionParams
    ) -> int:
        """
        计算延迟毫秒数（视角驱动）
        
        Args:
            ctx: 视角节奏上下文
            expression: 表达参数
            
        Returns:
            int: 延迟毫秒数
        """
        # 视觉转弯中 → 延迟 0（实际上应该被阻断，这里是兜底）
        if ctx.is_vision_turning:
            return 0
        
        # 视觉置信度低 → 不延迟，立即输出
        if ctx.visual_confidence < 0.6:
            return 0
        
        # 根据速度动态计算延迟
        speed = ctx.speed_mps
        
        if speed > 1.2:
            # 高速 → 短延迟
            return 100
        elif speed >= 0.5:
            # 中速 → 中等延迟
            return 200
        else:
            # 低速 → 长延迟
            return 300
