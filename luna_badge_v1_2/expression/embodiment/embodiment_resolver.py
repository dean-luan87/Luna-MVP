"""
Embodiment Resolver (C-2.1)

身体形态解析器

⚠️ 注意：
这里不引入任何情感、用户画像、语言偏好
"""

from typing import Optional
from .embodiment_types import EmbodimentType
from .embodiment_context import EmbodimentContext


class EmbodimentResolver:
    """
    身体形态解析器
    
    职责：
    - 解析当前身体形态
    - 一期：从配置/启动参数返回
    - 二期：允许动态切换（比如同一账号多设备）
    """
    
    def __init__(self, default_embodiment: Optional[EmbodimentType] = None):
        """
        初始化解析器
        
        Args:
            default_embodiment: 默认身体类型（可选）
        """
        self.default_embodiment = default_embodiment or EmbodimentType.GENERIC
        self._current_embodiment: Optional[EmbodimentType] = None
    
    def resolve(self) -> EmbodimentContext:
        """
        解析当前身体形态
        
        一期：从配置/启动参数返回
        二期：允许动态切换（比如同一账号多设备）
        
        Returns:
            EmbodimentContext: 身体形态上下文
        """
        # 如果已设置，使用当前设置
        if self._current_embodiment:
            embodiment = self._current_embodiment
        else:
            embodiment = self.default_embodiment
        
        # 根据身体类型返回配置
        return self._get_context_for_embodiment(embodiment)
    
    def _get_context_for_embodiment(self, embodiment: EmbodimentType) -> EmbodimentContext:
        """
        根据身体类型获取上下文
        
        Args:
            embodiment: 身体类型
            
        Returns:
            EmbodimentContext: 身体形态上下文
        """
        if embodiment == EmbodimentType.BLIND_BADGE:
            return EmbodimentContext(
                embodiment=embodiment,
                has_screen=False,
                has_voice=True,
                has_haptics=True,
                mobility="wearable"
            )
        elif embodiment == EmbodimentType.TOY:
            return EmbodimentContext(
                embodiment=embodiment,
                has_screen=False,
                has_voice=True,
                has_haptics=False,
                mobility="handheld"
            )
        elif embodiment == EmbodimentType.MOBILE_APP:
            return EmbodimentContext(
                embodiment=embodiment,
                has_screen=True,
                has_voice=True,
                has_haptics=True,
                mobility="handheld"
            )
        elif embodiment == EmbodimentType.DESKTOP:
            return EmbodimentContext(
                embodiment=embodiment,
                has_screen=True,
                has_voice=False,
                has_haptics=False,
                mobility="static"
            )
        else:  # GENERIC
            return EmbodimentContext(
                embodiment=embodiment,
                has_screen=True,
                has_voice=True,
                has_haptics=False,
                mobility="static"
            )
    
    def set_embodiment(self, embodiment: EmbodimentType) -> None:
        """
        设置身体类型（用于动态切换）
        
        Args:
            embodiment: 身体类型
        """
        self._current_embodiment = embodiment
    
    def get_current_embodiment(self) -> Optional[EmbodimentType]:
        """获取当前身体类型"""
        return self._current_embodiment
