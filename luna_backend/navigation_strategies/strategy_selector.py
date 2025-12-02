"""
策略选择器 (v1.2.0)
从环境类型、视觉elements、hazard、step_index meta 来自动切换策略
"""

from typing import Dict, Any, Optional, List
from .base_strategy import NavigationStrategy
from .default_strategy import DefaultStrategy
from .street_strategy import StreetStrategy
from .subway_strategy import SubwayStrategy
from .indoor_strategy import IndoorStrategy
from .corridor_strategy import CorridorStrategy
from .hazard_strategy import HazardStrategy
from .reroute_strategy import RerouteStrategy


class StrategySelector:
    """
    负责根据当前环境 env 选择最合适的导航策略。
    
    优先级：
    1. HazardStrategy（最高优先级，立即停止）
    2. RerouteStrategy
    3. SubwayStrategy
    4. IndoorStrategy
    5. CorridorStrategy
    6. StreetStrategy
    7. DefaultStrategy（兜底）
    """
    
    def __init__(self):
        """初始化策略选择器"""
        # 注册所有策略（按优先级顺序）
        self.strategies: List[NavigationStrategy] = [
            HazardStrategy(),      # 1
            RerouteStrategy(),     # 2
            SubwayStrategy(),      # 3
            IndoorStrategy(),      # 4
            CorridorStrategy(),    # 5
            StreetStrategy(),      # 6
            DefaultStrategy(),     # 7
        ]
        
        self.current_strategy: Optional[NavigationStrategy] = None
    
    def select(self, env: Dict[str, Any]) -> NavigationStrategy:
        """
        返回第一个 is_applicable = True 的策略
        
        Args:
            env: 环境信息字典
        
        Returns:
            选中的策略
        """
        for s in self.strategies:
            if s.is_applicable(env):
                self.current_strategy = s
                return s
        
        # 如果没有策略适用，返回默认策略
        self.current_strategy = DefaultStrategy()
        return self.current_strategy
    
    def select_strategy(self, status: Dict[str, Any], env: Dict[str, Any]) -> NavigationStrategy:
        """
        选择最适合的策略（兼容方法）
        
        Args:
            status: 导航状态字典（未使用，保持兼容）
            env: 环境信息字典
        
        Returns:
            选中的策略
        """
        return self.select(env)
    
    def get_current_strategy(self) -> Optional[NavigationStrategy]:
        """
        获取当前策略
        
        Returns:
            当前策略
        """
        return self.current_strategy
    
    def get_next_action(self, status: Dict[str, Any], env: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取下一步动作建议（使用当前策略）
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            动作建议字典
        """
        strategy = self.select_strategy(status, env)
        return strategy.get_next_action(status, env)
    
    def should_advance_step(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        判断是否应该推进到下一步
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否应该推进
        """
        strategy = self.select_strategy(status, env)
        return strategy.should_advance_step(status, env)
    
    def should_reroute(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        判断是否应该重新规划路线
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否应该重新规划
        """
        strategy = self.select_strategy(status, env)
        return strategy.should_reroute(status, env)
    
    def should_pause(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        判断是否建议暂停
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否建议暂停
        """
        strategy = self.select_strategy(status, env)
        return strategy.should_pause(status, env)
    
    def suggest_switch(self, status: Dict[str, Any], env: Dict[str, Any]) -> Optional[str]:
        """
        建议切换到其他策略
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            建议的策略名称
        """
        if self.current_strategy:
            return self.current_strategy.suggest_switch(status, env)
        return None

