"""
Embodiment Selector (C-2)

身体形态选择器
"""

from typing import Optional
from .embodiment_profiles import EmbodimentProfile, DistanceUnit, DirectionReference, Precision


class EmbodimentSelector:
    """
    身体形态选择器
    
    职责：
    - 根据上下文选择 EmbodimentProfile
    - 支持 blind / toy / default 切换
    """
    
    def __init__(self):
        """初始化选择器"""
        self._profiles: dict[str, EmbodimentProfile] = {}
        self._current_profile: Optional[EmbodimentProfile] = None
        
        # 初始化默认配置
        self._initialize_default_profiles()
    
    def _initialize_default_profiles(self) -> None:
        """初始化默认配置"""
        # Blind 配置
        self._profiles["blind"] = EmbodimentProfile(
            name="blind",
            distance_unit=DistanceUnit.STEP,  # 盲人用步数
            direction_reference=DirectionReference.BODY_RELATIVE,
            precision=Precision.MEDIUM
        )
        
        # Toy 配置
        self._profiles["toy"] = EmbodimentProfile(
            name="toy",
            distance_unit=DistanceUnit.METER,
            direction_reference=DirectionReference.BODY_RELATIVE,
            precision=Precision.COARSE
        )
        
        # Default 配置
        self._profiles["default"] = EmbodimentProfile(
            name="default",
            distance_unit=DistanceUnit.METER,
            direction_reference=DirectionReference.WORLD_RELATIVE,
            precision=Precision.MEDIUM
        )
    
    def select(self, profile_name: str) -> Optional[EmbodimentProfile]:
        """
        选择身体形态配置
        
        Args:
            profile_name: 配置名称（blind / toy / default）
            
        Returns:
            EmbodimentProfile: 如果找到，返回配置；否则返回 None
        """
        profile = self._profiles.get(profile_name)
        if profile:
            self._current_profile = profile
        return profile
    
    def get_current(self) -> Optional[EmbodimentProfile]:
        """获取当前配置"""
        return self._current_profile
    
    def register_profile(self, profile: EmbodimentProfile) -> None:
        """
        注册自定义配置
        
        Args:
            profile: 身体形态配置
        """
        self._profiles[profile.name] = profile
