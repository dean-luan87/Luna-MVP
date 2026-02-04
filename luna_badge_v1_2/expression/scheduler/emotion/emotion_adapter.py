"""
Emotion Modulation Adapter

情感调制适配器（必须过滤视觉状态）

NON-NEGOTIABLE CORE RULE:

Vision is the primary clock of the system.

- Visual rhythm defines all timing decisions.
- Emotion can modulate, but never override.
- GPS is verification-only.
- Speech follows vision, never leads it.

Emotion Engine has NO authority over:
- delay time
- scheduling order
- interruption
- output triggering

⚠️ 任何实现不得违反以上规则，否则视为错误实现。

关键点：
- Adapter 是唯一允许情感进入 C-5 的入口
- 返回 None = 情感被拒绝
- 不允许在这里算 delay、插队、打断
"""

from typing import Optional
from .emotion_models import EmotionModulation
from .emotion_takeover_protocol import EmotionTakeoverLevel, decide_takeover_level
from ..vision_rhythm_context import VisionRhythmContext


class EmotionModulationAdapter:
    """
    情感调制适配器
    
    职责：
    - 过滤视觉状态
    - 决定是否允许情感调制
    - 返回 None = 情感被拒绝
    
    ⚠️ 不允许在这里：
    - 计算 delay
    - 插队
    - 打断
    - 触发播报
    """
    
    def adapt(
        self,
        vision_ctx: VisionRhythmContext,
        emotion: Optional[EmotionModulation]
    ) -> Optional[EmotionModulation]:
        """
        适配情感调制
        
        Args:
            vision_ctx: 视角节奏上下文
            emotion: 情感调制（可选）
            
        Returns:
            Optional[EmotionModulation]: 适配后的情感调制，如果被拒绝则返回 None
        """
        # 如果没有情感，直接返回 None
        if emotion is None:
            return None
        
        # 决定接管等级
        level = decide_takeover_level(
            vision_state=vision_ctx.vision_state,
            emotion_confidence=emotion.confidence
        )
        
        # 如果被忽略，返回 None
        if level == EmotionTakeoverLevel.IGNORE:
            return None
        
        # WEAK / STRONG 都不允许改节奏，只允许 bias
        # 直接返回情感调制（视觉状态已在 decide_takeover_level 中过滤）
        return emotion
