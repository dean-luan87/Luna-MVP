"""
Calibrator Engine (C-2.5)

校准器引擎（一期规则版）

专业/口语/共识/引导的选择逻辑
"""

from typing import Optional
from .calibrator_models import CalibratorInput, CalibratorOutput
from .protocol import ExpressionProtocol
from .hooks_emotion_engine import EmotionEngineHooks


class CalibratorEngine:
    """
    校准器引擎
    
    职责：
    - 根据 intent + embodiment + emotion_params 选择协议
    - 一期：规则驱动
    - 二期：情感引擎只影响参数，不直接产出语言
    """
    
    def __init__(self, emotion_hooks: Optional[EmotionEngineHooks] = None):
        """
        初始化校准器引擎
        
        Args:
            emotion_hooks: 情感引擎钩子（可选，二期接口）
        """
        self.emotion_hooks = emotion_hooks
    
    def calibrate(self, input_data: CalibratorInput) -> CalibratorOutput:
        """
        校准输入，生成输出
        
        一期规则版：
        - 根据 embodiment 和 intent 选择协议
        - 专业/口语/共识/引导的选择逻辑（写死）
        
        Args:
            input_data: 校准器输入
            
        Returns:
            CalibratorOutput: 校准器输出
        """
        # 一期规则版（简化）
        # 根据 embodiment 选择协议
        if input_data.embodiment.name == "blind":
            protocol = ExpressionProtocol.GUIDED
            verbosity_level = 2
            lexicon_profile = "blind_navigation"
            reason = "blind_embodiment"
        elif input_data.embodiment.name == "toy":
            protocol = ExpressionProtocol.COLLOQUIAL
            verbosity_level = 1
            lexicon_profile = "toy_companion"
            reason = "toy_embodiment"
        else:
            protocol = ExpressionProtocol.CONSENSUS
            verbosity_level = 1
            lexicon_profile = "default"
            reason = "default_embodiment"
        
        # 二期：如果有情感引擎钩子，可以调整参数
        if self.emotion_hooks:
            adjusted_params = self.emotion_hooks.adjust_calibration_params(
                protocol=protocol,
                verbosity_level=verbosity_level,
                input_data=input_data
            )
            if adjusted_params:
                protocol = adjusted_params.get("protocol", protocol)
                verbosity_level = adjusted_params.get("verbosity_level", verbosity_level)
                reason += "+emotion_adjusted"
        
        return CalibratorOutput(
            protocol=protocol,
            verbosity_level=verbosity_level,
            lexicon_profile=lexicon_profile,
            reason=reason
        )
