#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
冷却管理器
"""

import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class CooldownManager:
    """冷却管理器"""
    
    def __init__(self):
        """初始化冷却管理器"""
        self.cooldowns = {}
        self.global_enabled = True
        self.default_cooldown_time = 3
        
        logger.info("✅ 冷却管理器初始化完成")
    
    def initialize(self, config: Dict[str, Any] = None) -> bool:
        """
        初始化冷却管理器
        
        Args:
            config: 配置字典
            
        Returns:
            bool: 是否初始化成功
        """
        try:
            if config:
                self.global_enabled = config.get("global_enabled", True)
                self.default_cooldown_time = config.get("default_cooldown_time", 3)
            
            logger.info(f"✅ 冷却管理器初始化成功: global_enabled={self.global_enabled}, default_cooldown_time={self.default_cooldown_time}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 冷却管理器初始化失败: {e}")
            return False
    
    def can_trigger(self, event_key: str, cooldown_time: Optional[float] = None) -> bool:
        """
        检查是否可以触发事件
        
        Args:
            event_key: 事件键名
            cooldown_time: 冷却时间
            
        Returns:
            bool: 是否可以触发
        """
        try:
            if not self.global_enabled:
                return True
            
            # 使用默认冷却时间
            if cooldown_time is None:
                cooldown_time = self.default_cooldown_time
            
            # 检查冷却状态
            current_time = time.time()
            last_trigger_time = self.cooldowns.get(event_key, 0)
            
            if current_time - last_trigger_time >= cooldown_time:
                return True
            else:
                remaining_time = cooldown_time - (current_time - last_trigger_time)
                logger.debug(f"⏰ 事件 {event_key} 冷却中，剩余时间: {remaining_time:.2f}秒")
                return False
                
        except Exception as e:
            logger.error(f"❌ 冷却检查失败: {e}")
            return True
    
    def trigger(self, event_key: str, cooldown_time: Optional[float] = None):
        """
        触发事件并记录时间
        
        Args:
            event_key: 事件键名
            cooldown_time: 冷却时间
        """
        try:
            if not self.global_enabled:
                return
            
            # 使用默认冷却时间
            if cooldown_time is None:
                cooldown_time = self.default_cooldown_time
            
            # 记录触发时间
            self.cooldowns[event_key] = time.time()
            logger.debug(f"⏰ 事件 {event_key} 已触发，冷却时间: {cooldown_time}秒")
            
        except Exception as e:
            logger.error(f"❌ 事件触发失败: {e}")
    
    def get_remaining_time(self, event_key: str, cooldown_time: Optional[float] = None) -> float:
        """
        获取剩余冷却时间
        
        Args:
            event_key: 事件键名
            cooldown_time: 冷却时间
            
        Returns:
            float: 剩余冷却时间（秒）
        """
        try:
            if not self.global_enabled:
                return 0.0
            
            # 使用默认冷却时间
            if cooldown_time is None:
                cooldown_time = self.default_cooldown_time
            
            # 计算剩余时间
            current_time = time.time()
            last_trigger_time = self.cooldowns.get(event_key, 0)
            remaining_time = cooldown_time - (current_time - last_trigger_time)
            
            return max(0.0, remaining_time)
            
        except Exception as e:
            logger.error(f"❌ 剩余时间计算失败: {e}")
            return 0.0
    
    def reset_cooldown(self, event_key: str):
        """
        重置事件冷却时间
        
        Args:
            event_key: 事件键名
        """
        try:
            if event_key in self.cooldowns:
                del self.cooldowns[event_key]
                logger.debug(f"⏰ 事件 {event_key} 冷却时间已重置")
            
        except Exception as e:
            logger.error(f"❌ 冷却时间重置失败: {e}")
    
    def reset_all_cooldowns(self):
        """重置所有冷却时间"""
        try:
            self.cooldowns.clear()
            logger.info("⏰ 所有冷却时间已重置")
            
        except Exception as e:
            logger.error(f"❌ 冷却时间重置失败: {e}")
    
    def set_global_enabled(self, enabled: bool):
        """
        设置全局冷却启用状态
        
        Args:
            enabled: 是否启用
        """
        self.global_enabled = enabled
        logger.info(f"⏰ 全局冷却状态已设置: {enabled}")
    
    def set_default_cooldown_time(self, cooldown_time: float):
        """
        设置默认冷却时间
        
        Args:
            cooldown_time: 冷却时间（秒）
        """
        self.default_cooldown_time = cooldown_time
        logger.info(f"⏰ 默认冷却时间已设置: {cooldown_time}秒")
    
    def get_cooldown_status(self) -> Dict[str, Any]:
        """
        获取冷却状态
        
        Returns:
            Dict[str, Any]: 冷却状态信息
        """
        try:
            current_time = time.time()
            status = {}
            
            for event_key, last_trigger_time in self.cooldowns.items():
                remaining_time = self.default_cooldown_time - (current_time - last_trigger_time)
                status[event_key] = {
                    "last_trigger_time": last_trigger_time,
                    "remaining_time": max(0.0, remaining_time)
                }
            
            return {
                "global_enabled": self.global_enabled,
                "default_cooldown_time": self.default_cooldown_time,
                "active_cooldowns": status
            }
            
        except Exception as e:
            logger.error(f"❌ 冷却状态获取失败: {e}")
            return {}

# 使用示例
if __name__ == "__main__":
    # 创建冷却管理器
    cooldown_manager = CooldownManager()
    
    # 初始化冷却管理器
    if cooldown_manager.initialize():
        print("✅ 冷却管理器初始化成功")
        
        # 测试冷却功能
        event_key = "test_event"
        
        # 检查是否可以触发
        if cooldown_manager.can_trigger(event_key):
            print(f"✅ 事件 {event_key} 可以触发")
            cooldown_manager.trigger(event_key)
        else:
            print(f"❌ 事件 {event_key} 冷却中")
        
        # 获取剩余时间
        remaining_time = cooldown_manager.get_remaining_time(event_key)
        print(f"⏰ 剩余冷却时间: {remaining_time:.2f}秒")
        
        # 获取冷却状态
        status = cooldown_manager.get_cooldown_status()
        print(f"📊 冷却状态: {status}")
    else:
        print("❌ 冷却管理器初始化失败")
