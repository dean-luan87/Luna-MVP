"""
Render Profile (C-3.1)

表达风格 / 人格

⚠️ 注意
- 一期 Profile 固定
- 二期只允许"改值"，不允许改结构
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class RenderProfile:
    """
    RenderProfile 数据类
    
    表达风格参数：
    - verbosity: 详细程度（1=极简, 5=详细）
    - precision: 精确度（1=模糊, 5=精确）
    - tone: 语调（"neutral" / "friendly" / "serious"）
    - pace: 节奏（"slow" / "normal" / "fast"）
    - confirmation: 是否需要确认式表达
    """
    verbosity: int        # 1=极简, 5=详细
    precision: int        # 1=模糊, 5=精确
    tone: Literal["neutral", "friendly", "serious"]
    pace: Literal["slow", "normal", "fast"]
    confirmation: bool   # 是否需要确认式表达

    @staticmethod
    def default():
        """
        默认 Profile
        
        Returns:
            RenderProfile: 默认表达风格
        """
        return RenderProfile(
            verbosity=3,
            precision=3,
            tone="neutral",
            pace="normal",
            confirmation=False
        )
