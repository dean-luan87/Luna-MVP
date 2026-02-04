"""
情绪调节语气策略 (EmotionToneStrategy) v1.2.0
当检测到用户情绪异常时，调整导航语气和速度
"""

from ..base_strategy import BaseStrategy


class EmotionToneStrategy(BaseStrategy):
    """情绪调节语气策略"""
    
    STRATEGY_NAME = "EMOTION_TONE"
    
    def should_execute(self) -> bool:
        """
        判断是否应该执行情绪调节
        
        条件：
        - 检测到焦虑或恐慌情绪
        """
        return self.ctx.emotion_state in ["anxious", "panic"]
    
    def execute(self) -> dict:
        """
        执行情绪调节策略
        
        Returns:
            策略执行结果
        """
        self.log("NAV:EMOTION_DETECTED", {
            "emotion_state": self.ctx.emotion_state,
            "position": self.ctx.position,
        })
        
        # 根据情绪状态生成安抚性提示
        if self.ctx.emotion_state == "panic":
            # 恐慌状态：强烈安抚
            text = "不要紧张，我一直在这里陪着你。我们慢慢走，不着急，安全第一。"
            action = "TONE_CALM_SEVERE"
            tone_speed = "slow"  # 语速放慢
            tone_pitch = "low"  # 音调降低
        elif self.ctx.emotion_state == "anxious":
            # 焦虑状态：温和安抚
            text = "不要紧，我一直在这里陪着你，我们慢慢走就可以了。"
            action = "TONE_SOFT"
            tone_speed = "normal"  # 正常语速
            tone_pitch = "normal"  # 正常音调
        else:
            # 其他情绪状态
            text = "我会一直陪伴您，请放心前行。"
            action = "TONE_NORMAL"
            tone_speed = "normal"
            tone_pitch = "normal"
        
        return {
            "success": True,
            "action": action,
            "text": text,
            "emotion_state": self.ctx.emotion_state,
            "tone_speed": tone_speed,
            "tone_pitch": tone_pitch,
        }



