"""
Expression Profile (C-5)

表达理解画像

一句话定义：
C-5 是「表达理解层」，不是语言生成器，也不是情感引擎
它只做一件事：
在"要说什么"已经确定之后，决定"怎么说用户才听得懂"
"""

from dataclasses import dataclass
from typing import Literal


DistanceStyle = Literal["metric", "step", "relative"]
DirectionStyle = Literal["degree", "relative"]
LanguageLevel = Literal["simple", "normal", "professional"]


@dataclass
class ExpressionProfile:
    """
    表达理解画像（一期版本）
    
    职责：
    - 定义用户能理解的表达方式
    - 不改变事实，只改变表达形式
    - 一期：静态配置
    - 二期：由情感引擎动态生成
    """
    # 距离表达方式
    distance_style: DistanceStyle = "metric"  # "metric" | "step" | "relative"
    
    # 方向表达方式
    direction_style: DirectionStyle = "degree"  # "degree" | "relative"
    
    # 语言复杂度
    language_level: LanguageLevel = "normal"  # "simple" | "normal" | "professional"
    
    # 是否允许抽象词
    allow_abstract: bool = False
    
    # 是否允许省略精度
    allow_fuzzy: bool = False
    
    @staticmethod
    def default():
        """
        默认画像
        
        Returns:
            ExpressionProfile: 默认表达画像
        """
        return ExpressionProfile(
            distance_style="metric",
            direction_style="degree",
            language_level="normal",
            allow_abstract=False,
            allow_fuzzy=False
        )
    
    @staticmethod
    def vision_impaired_default():
        """
        视障用户默认画像
        
        Returns:
            ExpressionProfile: 视障用户表达画像
        """
        return ExpressionProfile(
            distance_style="step",
            direction_style="relative",
            language_level="simple",
            allow_abstract=False,
            allow_fuzzy=True
        )
    
    @staticmethod
    def toy_default():
        """
        玩具用户默认画像
        
        Returns:
            ExpressionProfile: 玩具用户表达画像
        """
        return ExpressionProfile(
            distance_style="metric",
            direction_style="degree",
            language_level="normal",
            allow_abstract=True,
            allow_fuzzy=False
        )
    
    @staticmethod
    def professional_default():
        """
        专业用户默认画像
        
        Returns:
            ExpressionProfile: 专业用户表达画像
        """
        return ExpressionProfile(
            distance_style="metric",
            direction_style="degree",
            language_level="professional",
            allow_abstract=True,
            allow_fuzzy=False
        )
