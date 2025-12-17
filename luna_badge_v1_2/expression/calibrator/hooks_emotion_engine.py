"""
Emotion Engine Hooks (C-2.5)

二期接口（空实现）

情感引擎只影响"表达策略"，不直接产出语言
"""

from typing import Optional, Dict, Any
from .protocol import ExpressionProtocol
from .calibrator_models import CalibratorInput


class EmotionEngineHooks:
    """
    情感引擎钩子（二期接口）
    
    职责：
    - 通过参数影响协议/词库/冗余度
    - 不得产生文本
    - 只提供策略参数
    """
    
    def __init__(self):
        """初始化情感引擎钩子（空实现）"""
        pass
    
    def adjust_calibration_params(
        self,
        protocol: ExpressionProtocol,
        verbosity_level: int,
        input_data: CalibratorInput
    ) -> Optional[Dict[str, Any]]:
        """
        调整校准参数（二期接口）
        
        注意：
        - 不直接产出语言
        - 只影响协议/词库/冗余度
        
        Args:
            protocol: 当前协议
            verbosity_level: 当前冗余度级别
            input_data: 校准器输入
            
        Returns:
            Optional[Dict[str, Any]]: 调整后的参数（如果不需要调整则返回 None）
        """
        # 二期实现：根据 emotion_params 调整参数
        # 一期：返回 None（不调整）
        return None
