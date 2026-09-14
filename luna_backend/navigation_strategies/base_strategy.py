"""
所有导航策略的基类 (v1.2.0)

Strategy 负责解释：
- 当前一步怎么执行
- 是否需要切换下一步
- 是否需要重新规划（偏航/滞后）
- 是否需要暂停/等待
- 当前环境特征是否满足此策略

注意：策略不直接写日志、不播报、不操作FSM，只返回"下一步建议"。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class NavigationStrategy(ABC):
    """所有导航策略的基类"""
    
    STRATEGY_NAME = "BASE"
    
    # === 策略是否适用（依据 environment 特征） ===
    
    @abstractmethod
    def is_applicable(self, env: Dict[str, Any]) -> bool:
        """
        判断策略是否适用于当前环境
        
        Args:
            env: 环境信息字典，包含 vision, navigation_raw 等
        
        Returns:
            是否适用
        """
        pass
    
    # === 当前应执行的 action（如：直行、左转、询问服务台） ===
    
    @abstractmethod
    def get_next_action(self, status: Dict[str, Any], env: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取下一步动作建议
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            动作建议字典，包含 action, description, reason 等
        """
        pass
    
    # === 是否应该推进到下一步 ===
    
    def should_advance_step(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        判断是否应该推进到下一步
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否应该推进
        """
        return False  # 默认不自动推进
    
    # === 是否应该重新规划路线（偏航、阻塞） ===
    
    def should_reroute(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        判断是否应该重新规划路线
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否应该重新规划
        """
        return False
    
    # === 是否建议暂停（红绿灯、楼梯口、扶梯口、拥挤区） ===
    
    def should_pause(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        判断是否建议暂停
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否建议暂停
        """
        return False
    
    # === 是否建议切换策略（如从室外 → 室内） ===
    
    def suggest_switch(self, status: Dict[str, Any], env: Dict[str, Any]) -> Optional[str]:
        """
        建议切换到其他策略
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            建议的策略名称，如果不需要切换则返回None
        """
        return None
    
    def should_complete(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        判断是否应该完成导航
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否应该完成
        """
        return False
    
    # === 策略的名字（用于日志和错误码定位） ===
    
    def name(self) -> str:
        """
        获取策略名称
        
        Returns:
            策略名称
        """
        return self.STRATEGY_NAME

