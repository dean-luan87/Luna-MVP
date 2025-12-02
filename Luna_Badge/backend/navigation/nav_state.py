#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一导航状态管理（规范要求）
提供统一的导航状态接口，包含active、destination、current_step、last_update
"""

import logging
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class NavigationStatus(Enum):
    """导航状态枚举"""
    INACTIVE = "inactive"  # 未激活
    ACTIVE = "active"      # 进行中
    PAUSED = "paused"      # 已暂停
    CANCELLED = "cancelled"  # 已取消
    COMPLETED = "completed"  # 已完成


@dataclass
class NavigationState:
    """
    统一导航状态（规范要求）
    包含active、destination、current_step、last_update
    """
    active: bool = False
    destination: str = ""
    current_step: int = 0
    last_update: float = field(default_factory=time.time)
    status: NavigationStatus = NavigationStatus.INACTIVE
    route_segments: list = field(default_factory=list)
    start_time: float = 0.0
    pause_reason: Optional[str] = None
    cancel_reason: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "active": self.active,
            "destination": self.destination,
            "current_step": self.current_step,
            "last_update": self.last_update,
            "status": self.status.value,
            "route_segments": self.route_segments,
            "start_time": self.start_time,
            "pause_reason": self.pause_reason,
            "cancel_reason": self.cancel_reason
        }
    
    def update(self, **kwargs):
        """更新状态"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.last_update = time.time()


class NavigationStateManager:
    """
    统一导航状态管理器（规范要求）
    提供全局导航状态访问接口
    """
    
    def __init__(self):
        """初始化导航状态管理器"""
        self._state = NavigationState()
        logger.info("NavigationStateManager初始化完成", extra={"module": "navigation", "meta": {"component": "nav_state"}})
    
    def start(self, destination: str, route_segments: list = None) -> bool:
        """
        启动导航
        
        Args:
            destination: 目的地
            route_segments: 路径段列表
        
        Returns:
            bool: 是否成功启动
        """
        if self._state.active:
            logger.warning("导航已在进行中", extra={"module": "navigation", "meta": {"component": "nav_state"}})
            return False
        
        self._state.update(
            active=True,
            destination=destination,
            current_step=0,
            status=NavigationStatus.ACTIVE,
            route_segments=route_segments or [],
            start_time=time.time()
        )
        
        logger.info(f"导航已启动: {destination}", extra={"module": "navigation", "meta": {
            "component": "nav_state",
            "destination": destination
        }})
        
        return True
    
    def pause(self, reason: str = "用户暂停") -> bool:
        """
        暂停导航
        
        Args:
            reason: 暂停原因
        
        Returns:
            bool: 是否成功暂停
        """
        if not self._state.active:
            logger.warning("导航未激活，无法暂停", extra={"module": "navigation", "meta": {"component": "nav_state"}})
            return False
        
        self._state.update(
            active=False,
            status=NavigationStatus.PAUSED,
            pause_reason=reason
        )
        
        logger.info(f"导航已暂停: {reason}", extra={"module": "navigation", "meta": {
            "component": "nav_state",
            "reason": reason
        }})
        
        return True
    
    def resume(self) -> bool:
        """
        恢复导航
        
        Returns:
            bool: 是否成功恢复
        """
        if self._state.status != NavigationStatus.PAUSED:
            logger.warning("导航未暂停，无法恢复", extra={"module": "navigation", "meta": {"component": "nav_state"}})
            return False
        
        self._state.update(
            active=True,
            status=NavigationStatus.ACTIVE,
            pause_reason=None
        )
        
        logger.info("导航已恢复", extra={"module": "navigation", "meta": {"component": "nav_state"}})
        
        return True
    
    def cancel(self, reason: str = "用户取消") -> bool:
        """
        取消导航
        
        Args:
            reason: 取消原因
        
        Returns:
            bool: 是否成功取消
        """
        self._state.update(
            active=False,
            status=NavigationStatus.CANCELLED,
            cancel_reason=reason
        )
        
        logger.info(f"导航已取消: {reason}", extra={"module": "navigation", "meta": {
            "component": "nav_state",
            "reason": reason
        }})
        
        return True
    
    def complete(self) -> bool:
        """
        完成导航
        
        Returns:
            bool: 是否成功完成
        """
        self._state.update(
            active=False,
            status=NavigationStatus.COMPLETED
        )
        
        logger.info("导航已完成", extra={"module": "navigation", "meta": {"component": "nav_state"}})
        
        return True
    
    def update_step(self, step: int) -> bool:
        """
        更新当前步骤
        
        Args:
            step: 步骤索引
        
        Returns:
            bool: 是否成功更新
        """
        if not self._state.active:
            return False
        
        self._state.update(current_step=step)
        
        return True
    
    def get_state(self) -> NavigationState:
        """
        获取当前状态
        
        Returns:
            NavigationState: 导航状态
        """
        return self._state
    
    def get_state_dict(self) -> Dict[str, Any]:
        """
        获取状态字典
        
        Returns:
            Dict: 状态字典
        """
        return self._state.to_dict()


# 全局导航状态管理器实例
_global_nav_state_manager: Optional[NavigationStateManager] = None


def get_nav_state_manager() -> NavigationStateManager:
    """
    获取全局导航状态管理器实例
    
    Returns:
        NavigationStateManager: 导航状态管理器
    """
    global _global_nav_state_manager
    
    if _global_nav_state_manager is None:
        _global_nav_state_manager = NavigationStateManager()
    
    return _global_nav_state_manager


if __name__ == "__main__":
    # 自检代码
    print("🧪 NavigationStateManager自检开始...")
    
    manager = NavigationStateManager()
    
    # 测试启动导航
    assert manager.start("测试目的地", [{"step": 1, "direction": "forward"}])
    assert manager.get_state().active == True
    assert manager.get_state().destination == "测试目的地"
    
    # 测试更新步骤
    assert manager.update_step(1)
    assert manager.get_state().current_step == 1
    
    # 测试暂停
    assert manager.pause("测试暂停")
    assert manager.get_state().status == NavigationStatus.PAUSED
    
    # 测试恢复
    assert manager.resume()
    assert manager.get_state().status == NavigationStatus.ACTIVE
    
    # 测试完成
    assert manager.complete()
    assert manager.get_state().status == NavigationStatus.COMPLETED
    
    print("✅ NavigationStateManager自检完成")


