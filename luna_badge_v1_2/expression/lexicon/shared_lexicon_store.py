"""
Shared Lexicon Store (C Layer)

共识词库（一期先做内存版）
"""

from typing import Dict, Optional
from .lexicon_models import LexiconProfile


class SharedLexiconStore:
    """
    共享词库存储（一期先做内存版）
    
    职责：
    - 存储和管理词库配置
    - 提供词库查询接口
    """
    
    def __init__(self):
        """初始化词库存储"""
        self._profiles: Dict[str, LexiconProfile] = {}
        self._initialize_default_lexicons()
    
    def _initialize_default_lexicons(self) -> None:
        """初始化默认词库（空实现，一期先做骨架）"""
        # 一期：先做骨架，后续填充
        pass
    
    def get_profile(self, profile_name: str) -> Optional[LexiconProfile]:
        """
        获取词库配置
        
        Args:
            profile_name: 配置名称
            
        Returns:
            LexiconProfile: 如果找到，返回配置；否则返回 None
        """
        return self._profiles.get(profile_name)
    
    def register_profile(self, profile: LexiconProfile) -> None:
        """
        注册词库配置
        
        Args:
            profile: 词库配置
        """
        self._profiles[profile.name] = profile
    
    def lookup(self, profile_name: str, key: str) -> Optional[str]:
        """
        查找词库条目
        
        Args:
            profile_name: 配置名称
            key: 键
            
        Returns:
            str: 如果找到，返回值；否则返回 None
        """
        profile = self.get_profile(profile_name)
        if profile:
            return profile.entries.get(key)
        return None
