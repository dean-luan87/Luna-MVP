#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理器
支持动态配置路径和语音包路径，支持OTA更新
"""

import os
import json
import yaml
import logging
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = "config", speech_path: str = "speech"):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置路径
            speech_path: 语音路径
        """
        self.config_path = config_path
        self.speech_path = speech_path
        self.config_cache = {}
        self.speech_cache = {}
        
        # 确保目录存在
        os.makedirs(self.config_path, exist_ok=True)
        os.makedirs(self.speech_path, exist_ok=True)
        
        logger.info(f"✅ 配置管理器初始化完成: config_path={config_path}, speech_path={speech_path}")
    
    def load_config(self, filename: str, config_type: str = "config") -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            filename: 配置文件名
            config_type: 配置类型 (config/speech)
            
        Returns:
            Dict[str, Any]: 配置数据
        """
        try:
            # 确定文件路径
            if config_type == "config":
                file_path = os.path.join(self.config_path, filename)
                cache = self.config_cache
            elif config_type == "speech":
                file_path = os.path.join(self.speech_path, filename)
                cache = self.speech_cache
            else:
                raise ValueError(f"不支持的配置类型: {config_type}")
            
            # 检查缓存
            if filename in cache:
                logger.debug(f"📦 从缓存加载配置: {filename}")
                return cache[filename]
            
            # 加载文件
            if not os.path.exists(file_path):
                logger.warning(f"⚠️ 配置文件不存在: {file_path}")
                return {}
            
            # 根据文件扩展名选择加载方式
            if filename.endswith(('.yaml', '.yml')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
            elif filename.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            else:
                logger.error(f"❌ 不支持的配置文件格式: {filename}")
                return {}
            
            # 缓存配置
            cache[filename] = config_data
            
            logger.info(f"✅ 配置文件加载成功: {file_path}")
            return config_data
            
        except Exception as e:
            logger.error(f"❌ 配置文件加载失败: {e}")
            return {}
    
    def save_config(self, filename: str, config_data: Dict[str, Any], config_type: str = "config") -> bool:
        """
        保存配置文件
        
        Args:
            filename: 配置文件名
            config_data: 配置数据
            config_type: 配置类型 (config/speech)
            
        Returns:
            bool: 是否保存成功
        """
        try:
            # 确定文件路径
            if config_type == "config":
                file_path = os.path.join(self.config_path, filename)
                cache = self.config_cache
            elif config_type == "speech":
                file_path = os.path.join(self.speech_path, filename)
                cache = self.speech_cache
            else:
                raise ValueError(f"不支持的配置类型: {config_type}")
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 根据文件扩展名选择保存方式
            if filename.endswith(('.yaml', '.yml')):
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True, indent=2)
            elif filename.endswith('.json'):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, ensure_ascii=False, indent=2)
            else:
                logger.error(f"❌ 不支持的配置文件格式: {filename}")
                return False
            
            # 更新缓存
            cache[filename] = config_data
            
            logger.info(f"✅ 配置文件保存成功: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 配置文件保存失败: {e}")
            return False
    
    def get_config_path(self, config_type: str = "config") -> str:
        """
        获取配置路径
        
        Args:
            config_type: 配置类型 (config/speech)
            
        Returns:
            str: 配置路径
        """
        if config_type == "config":
            return self.config_path
        elif config_type == "speech":
            return self.speech_path
        else:
            raise ValueError(f"不支持的配置类型: {config_type}")
    
    def set_config_path(self, path: str, config_type: str = "config"):
        """
        设置配置路径
        
        Args:
            path: 新路径
            config_type: 配置类型 (config/speech)
        """
        try:
            if config_type == "config":
                self.config_path = path
                self.config_cache.clear()
            elif config_type == "speech":
                self.speech_path = path
                self.speech_cache.clear()
            else:
                raise ValueError(f"不支持的配置类型: {config_type}")
            
            # 确保目录存在
            os.makedirs(path, exist_ok=True)
            
            logger.info(f"✅ 配置路径已更新: {config_type}={path}")
            
        except Exception as e:
            logger.error(f"❌ 设置配置路径失败: {e}")
    
    def reload_config(self, filename: str, config_type: str = "config") -> Dict[str, Any]:
        """
        重新加载配置文件
        
        Args:
            filename: 配置文件名
            config_type: 配置类型 (config/speech)
            
        Returns:
            Dict[str, Any]: 配置数据
        """
        try:
            # 清除缓存
            if config_type == "config":
                self.config_cache.pop(filename, None)
            elif config_type == "speech":
                self.speech_cache.pop(filename, None)
            
            # 重新加载
            return self.load_config(filename, config_type)
            
        except Exception as e:
            logger.error(f"❌ 重新加载配置失败: {e}")
            return {}
    
    def reload_all_configs(self):
        """重新加载所有配置"""
        try:
            self.config_cache.clear()
            self.speech_cache.clear()
            logger.info("✅ 所有配置已重新加载")
            
        except Exception as e:
            logger.error(f"❌ 重新加载所有配置失败: {e}")
    
    def list_config_files(self, config_type: str = "config") -> List[str]:
        """
        列出配置文件
        
        Args:
            config_type: 配置类型 (config/speech)
            
        Returns:
            List[str]: 配置文件列表
        """
        try:
            if config_type == "config":
                path = self.config_path
            elif config_type == "speech":
                path = self.speech_path
            else:
                raise ValueError(f"不支持的配置类型: {config_type}")
            
            if not os.path.exists(path):
                return []
            
            files = []
            for file in os.listdir(path):
                if file.endswith(('.yaml', '.yml', '.json')):
                    files.append(file)
            
            return files
            
        except Exception as e:
            logger.error(f"❌ 列出配置文件失败: {e}")
            return []
    
    def backup_config(self, filename: str, config_type: str = "config") -> bool:
        """
        备份配置文件
        
        Args:
            filename: 配置文件名
            config_type: 配置类型 (config/speech)
            
        Returns:
            bool: 是否备份成功
        """
        try:
            import shutil
            from datetime import datetime
            
            # 确定文件路径
            if config_type == "config":
                file_path = os.path.join(self.config_path, filename)
            elif config_type == "speech":
                file_path = os.path.join(self.speech_path, filename)
            else:
                raise ValueError(f"不支持的配置类型: {config_type}")
            
            if not os.path.exists(file_path):
                logger.warning(f"⚠️ 配置文件不存在: {file_path}")
                return False
            
            # 创建备份文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{filename}.backup_{timestamp}"
            backup_path = os.path.join(os.path.dirname(file_path), backup_filename)
            
            shutil.copy2(file_path, backup_path)
            
            logger.info(f"✅ 配置文件已备份: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 备份配置文件失败: {e}")
            return False
    
    def get_cache_status(self) -> Dict[str, Any]:
        """
        获取缓存状态
        
        Returns:
            Dict[str, Any]: 缓存状态信息
        """
        return {
            "config_cache_size": len(self.config_cache),
            "speech_cache_size": len(self.speech_cache),
            "config_path": self.config_path,
            "speech_path": self.speech_path
        }

# 全局配置管理器实例
_global_config_manager: Optional[ConfigManager] = None

def get_config_manager() -> ConfigManager:
    """获取全局配置管理器实例"""
    global _global_config_manager
    if _global_config_manager is None:
        _global_config_manager = ConfigManager()
    return _global_config_manager

def load_config(filename: str, config_type: str = "config") -> Dict[str, Any]:
    """加载配置"""
    manager = get_config_manager()
    return manager.load_config(filename, config_type)

def save_config(filename: str, config_data: Dict[str, Any], config_type: str = "config") -> bool:
    """保存配置"""
    manager = get_config_manager()
    return manager.save_config(filename, config_data, config_type)

# 使用示例
if __name__ == "__main__":
    # 创建配置管理器
    config_manager = ConfigManager()
    
    # 测试配置加载
    config_data = config_manager.load_config("system_config.yaml", "config")
    print(f"配置数据: {config_data}")
    
    # 测试配置保存
    test_config = {"test": "value", "number": 42}
    config_manager.save_config("test_config.yaml", test_config, "config")
    
    # 测试路径设置
    config_manager.set_config_path("/tmp/test_config", "config")
    
    # 获取缓存状态
    cache_status = config_manager.get_cache_status()
    print(f"缓存状态: {cache_status}")
    
    print("✅ 配置管理器测试完成")
