#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
状态跟踪器
"""

import json
import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class StateTracker:
    """状态跟踪器"""
    
    def __init__(self):
        """初始化状态跟踪器"""
        self.states = {}
        self.state_file = "luna_states.json"
        self.auto_save = True
        
        logger.info("✅ 状态跟踪器初始化完成")
    
    def initialize(self, state_file: str = "luna_states.json", auto_save: bool = True) -> bool:
        """
        初始化状态跟踪器
        
        Args:
            state_file: 状态文件路径
            auto_save: 是否自动保存
            
        Returns:
            bool: 是否初始化成功
        """
        try:
            self.state_file = state_file
            self.auto_save = auto_save
            
            # 加载状态文件
            self.load()
            
            logger.info(f"✅ 状态跟踪器初始化成功: state_file={state_file}, auto_save={auto_save}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 状态跟踪器初始化失败: {e}")
            return False
    
    def set_flag(self, key: str, value: Any):
        """
        设置状态标志
        
        Args:
            key: 状态键名
            value: 状态值
        """
        try:
            self.states[key] = value
            logger.debug(f"📊 状态标志已设置: {key} = {value}")
            
            # 自动保存
            if self.auto_save:
                self.save()
                
        except Exception as e:
            logger.error(f"❌ 状态标志设置失败: {e}")
    
    def get_flag(self, key: str, default: Any = None) -> Any:
        """
        获取状态标志
        
        Args:
            key: 状态键名
            default: 默认值
            
        Returns:
            Any: 状态值
        """
        try:
            return self.states.get(key, default)
            
        except Exception as e:
            logger.error(f"❌ 状态标志获取失败: {e}")
            return default
    
    def reset_flag(self, key: str):
        """
        重置状态标志
        
        Args:
            key: 状态键名
        """
        try:
            if key in self.states:
                del self.states[key]
                logger.debug(f"📊 状态标志已重置: {key}")
                
                # 自动保存
                if self.auto_save:
                    self.save()
                    
        except Exception as e:
            logger.error(f"❌ 状态标志重置失败: {e}")
    
    def clear_all(self):
        """清除所有状态标志"""
        try:
            self.states.clear()
            logger.info("📊 所有状态标志已清除")
            
            # 自动保存
            if self.auto_save:
                self.save()
                
        except Exception as e:
            logger.error(f"❌ 状态标志清除失败: {e}")
    
    def save(self) -> bool:
        """
        保存状态到文件
        
        Returns:
            bool: 是否保存成功
        """
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.states, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"📊 状态已保存到文件: {self.state_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 状态保存失败: {e}")
            return False
    
    def load(self) -> bool:
        """
        从文件加载状态
        
        Returns:
            bool: 是否加载成功
        """
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    self.states = json.load(f)
                logger.debug(f"📊 状态已从文件加载: {self.state_file}")
            else:
                self.states = {}
                logger.debug(f"📊 状态文件不存在，使用空状态: {self.state_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 状态加载失败: {e}")
            self.states = {}
            return False
    
    def export_states(self, output_file: str) -> bool:
        """
        导出状态到文件
        
        Args:
            output_file: 输出文件路径
            
        Returns:
            bool: 是否导出成功
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.states, f, ensure_ascii=False, indent=2)
            
            logger.info(f"📊 状态已导出到文件: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 状态导出失败: {e}")
            return False
    
    def import_states(self, input_file: str) -> bool:
        """
        从文件导入状态
        
        Args:
            input_file: 输入文件路径
            
        Returns:
            bool: 是否导入成功
        """
        try:
            if os.path.exists(input_file):
                with open(input_file, 'r', encoding='utf-8') as f:
                    imported_states = json.load(f)
                
                self.states.update(imported_states)
                logger.info(f"📊 状态已从文件导入: {input_file}")
                
                # 自动保存
                if self.auto_save:
                    self.save()
                
                return True
            else:
                logger.warning(f"⚠️ 状态文件不存在: {input_file}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 状态导入失败: {e}")
            return False
    
    def get_all_states(self) -> Dict[str, Any]:
        """
        获取所有状态
        
        Returns:
            Dict[str, Any]: 所有状态
        """
        return self.states.copy()
    
    def get_state_count(self) -> int:
        """
        获取状态数量
        
        Returns:
            int: 状态数量
        """
        return len(self.states)
    
    def has_flag(self, key: str) -> bool:
        """
        检查是否存在状态标志
        
        Args:
            key: 状态键名
            
        Returns:
            bool: 是否存在
        """
        return key in self.states

# 使用示例
if __name__ == "__main__":
    # 创建状态跟踪器
    state_tracker = StateTracker()
    
    # 初始化状态跟踪器
    if state_tracker.initialize():
        print("✅ 状态跟踪器初始化成功")
        
        # 测试状态操作
        state_tracker.set_flag("test_flag", True)
        state_tracker.set_flag("counter", 42)
        
        # 获取状态
        test_flag = state_tracker.get_flag("test_flag")
        counter = state_tracker.get_flag("counter")
        print(f"测试标志: {test_flag}")
        print(f"计数器: {counter}")
        
        # 检查状态
        has_flag = state_tracker.has_flag("test_flag")
        print(f"是否存在测试标志: {has_flag}")
        
        # 获取状态数量
        count = state_tracker.get_state_count()
        print(f"状态数量: {count}")
        
        # 导出状态
        state_tracker.export_states("test_states.json")
        
        # 重置状态
        state_tracker.reset_flag("test_flag")
        
        # 清除所有状态
        state_tracker.clear_all()
    else:
        print("❌ 状态跟踪器初始化失败")
