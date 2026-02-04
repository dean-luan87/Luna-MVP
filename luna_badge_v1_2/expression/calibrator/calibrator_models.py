"""
Calibrator Models (C-2.5)

校准器输入输出数据模型
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from .protocol import ExpressionProtocol
from ..context.embodiment_profiles import EmbodimentProfile


@dataclass
class CalibratorInput:
    """
    校准器输入
    
    Input：intent + embodiment + (optional) emotion_params + user_profile_stub
    """
    intent: Dict[str, Any]
    embodiment: EmbodimentProfile
    emotion_params: Optional[Dict[str, Any]] = None
    user_profile_stub: Optional[Dict[str, Any]] = None


@dataclass
class CalibratorOutput:
    """
    校准器输出
    
    Output：protocol + verbosity_level + lexicon_profile + reason
    """
    protocol: ExpressionProtocol
    verbosity_level: int  # 0-3
    lexicon_profile: str
    reason: str
    
    # 可选扩展字段
    extra: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.extra is None:
            self.extra = {}
