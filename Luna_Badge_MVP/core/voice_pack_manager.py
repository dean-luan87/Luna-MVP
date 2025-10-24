#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音包管理器
支持动态加载语音包和播报内容
"""

import os
import json
import yaml
import zipfile
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class VoicePackManager:
    """语音包管理器"""
    
    def __init__(self, voice_pack_path: str = "speech/voice_packs", 
                 default_voice_pack: str = "default"):
        """
        初始化语音包管理器
        
        Args:
            voice_pack_path: 语音包路径
            default_voice_pack: 默认语音包名称
        """
        self.voice_pack_path = voice_pack_path
        self.default_voice_pack = default_voice_pack
        self.current_voice_pack = default_voice_pack
        self.voice_pack_cache = {}
        
        # 确保目录存在
        os.makedirs(self.voice_pack_path, exist_ok=True)
        
        logger.info(f"✅ 语音包管理器初始化完成: voice_pack_path={voice_pack_path}")
    
    def load_voice_pack(self, voice_pack_name: str) -> Dict[str, Any]:
        """
        加载语音包
        
        Args:
            voice_pack_name: 语音包名称
            
        Returns:
            Dict[str, Any]: 语音包数据
        """
        try:
            # 检查缓存
            if voice_pack_name in self.voice_pack_cache:
                logger.debug(f"📦 从缓存加载语音包: {voice_pack_name}")
                return self.voice_pack_cache[voice_pack_name]
            
            # 构建语音包路径
            voice_pack_dir = os.path.join(self.voice_pack_path, voice_pack_name)
            
            if not os.path.exists(voice_pack_dir):
                logger.warning(f"⚠️ 语音包不存在: {voice_pack_dir}")
                return {}
            
            # 加载语音包配置
            config_file = os.path.join(voice_pack_dir, "voice_pack.yaml")
            if not os.path.exists(config_file):
                logger.warning(f"⚠️ 语音包配置文件不存在: {config_file}")
                return {}
            
            with open(config_file, 'r', encoding='utf-8') as f:
                voice_pack_data = yaml.safe_load(f)
            
            # 加载语音内容
            content_file = os.path.join(voice_pack_dir, "voice_content.yaml")
            if os.path.exists(content_file):
                with open(content_file, 'r', encoding='utf-8') as f:
                    voice_content = yaml.safe_load(f)
                voice_pack_data["content"] = voice_content
            
            # 缓存语音包
            self.voice_pack_cache[voice_pack_name] = voice_pack_data
            
            logger.info(f"✅ 语音包加载成功: {voice_pack_name}")
            return voice_pack_data
            
        except Exception as e:
            logger.error(f"❌ 语音包加载失败: {e}")
            return {}
    
    def install_voice_pack(self, voice_pack_file: str, voice_pack_name: str = None) -> bool:
        """
        安装语音包
        
        Args:
            voice_pack_file: 语音包文件路径
            voice_pack_name: 语音包名称
            
        Returns:
            bool: 是否安装成功
        """
        try:
            if not os.path.exists(voice_pack_file):
                logger.error(f"❌ 语音包文件不存在: {voice_pack_file}")
                return False
            
            # 确定语音包名称
            if not voice_pack_name:
                voice_pack_name = os.path.splitext(os.path.basename(voice_pack_file))[0]
            
            # 创建语音包目录
            voice_pack_dir = os.path.join(self.voice_pack_path, voice_pack_name)
            os.makedirs(voice_pack_dir, exist_ok=True)
            
            # 解压语音包
            if voice_pack_file.endswith('.zip'):
                with zipfile.ZipFile(voice_pack_file, 'r') as zip_ref:
                    zip_ref.extractall(voice_pack_dir)
            else:
                logger.error(f"❌ 不支持的语音包格式: {voice_pack_file}")
                return False
            
            # 清除缓存
            self.voice_pack_cache.pop(voice_pack_name, None)
            
            logger.info(f"✅ 语音包安装成功: {voice_pack_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 语音包安装失败: {e}")
            return False
    
    def uninstall_voice_pack(self, voice_pack_name: str) -> bool:
        """
        卸载语音包
        
        Args:
            voice_pack_name: 语音包名称
            
        Returns:
            bool: 是否卸载成功
        """
        try:
            voice_pack_dir = os.path.join(self.voice_pack_path, voice_pack_name)
            
            if not os.path.exists(voice_pack_dir):
                logger.warning(f"⚠️ 语音包不存在: {voice_pack_name}")
                return False
            
            # 删除语音包目录
            import shutil
            shutil.rmtree(voice_pack_dir)
            
            # 清除缓存
            self.voice_pack_cache.pop(voice_pack_name, None)
            
            logger.info(f"✅ 语音包卸载成功: {voice_pack_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 语音包卸载失败: {e}")
            return False
    
    def list_voice_packs(self) -> List[str]:
        """
        列出所有语音包
        
        Returns:
            List[str]: 语音包名称列表
        """
        try:
            if not os.path.exists(self.voice_pack_path):
                return []
            
            voice_packs = []
            for item in os.listdir(self.voice_pack_path):
                item_path = os.path.join(self.voice_pack_path, item)
                if os.path.isdir(item_path):
                    voice_packs.append(item)
            
            return voice_packs
            
        except Exception as e:
            logger.error(f"❌ 列出语音包失败: {e}")
            return []
    
    def set_current_voice_pack(self, voice_pack_name: str) -> bool:
        """
        设置当前语音包
        
        Args:
            voice_pack_name: 语音包名称
            
        Returns:
            bool: 是否设置成功
        """
        try:
            # 检查语音包是否存在
            if voice_pack_name not in self.list_voice_packs():
                logger.error(f"❌ 语音包不存在: {voice_pack_name}")
                return False
            
            # 加载语音包
            voice_pack_data = self.load_voice_pack(voice_pack_name)
            if not voice_pack_data:
                logger.error(f"❌ 语音包加载失败: {voice_pack_name}")
                return False
            
            # 设置当前语音包
            self.current_voice_pack = voice_pack_name
            
            logger.info(f"✅ 当前语音包已设置: {voice_pack_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 设置当前语音包失败: {e}")
            return False
    
    def get_current_voice_pack(self) -> Dict[str, Any]:
        """
        获取当前语音包
        
        Returns:
            Dict[str, Any]: 当前语音包数据
        """
        return self.load_voice_pack(self.current_voice_pack)
    
    def get_voice_content(self, event_key: str, voice_pack_name: str = None) -> Dict[str, Any]:
        """
        获取语音内容
        
        Args:
            event_key: 事件键名
            voice_pack_name: 语音包名称
            
        Returns:
            Dict[str, Any]: 语音内容
        """
        try:
            # 确定语音包名称
            if not voice_pack_name:
                voice_pack_name = self.current_voice_pack
            
            # 加载语音包
            voice_pack_data = self.load_voice_pack(voice_pack_name)
            if not voice_pack_data:
                return {}
            
            # 获取语音内容
            content = voice_pack_data.get("content", {})
            return content.get(event_key, {})
            
        except Exception as e:
            logger.error(f"❌ 获取语音内容失败: {e}")
            return {}
    
    def create_voice_pack(self, voice_pack_name: str, voice_pack_data: Dict[str, Any]) -> bool:
        """
        创建语音包
        
        Args:
            voice_pack_name: 语音包名称
            voice_pack_data: 语音包数据
            
        Returns:
            bool: 是否创建成功
        """
        try:
            # 创建语音包目录
            voice_pack_dir = os.path.join(self.voice_pack_path, voice_pack_name)
            os.makedirs(voice_pack_dir, exist_ok=True)
            
            # 保存语音包配置
            config_file = os.path.join(voice_pack_dir, "voice_pack.yaml")
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(voice_pack_data, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            # 保存语音内容
            if "content" in voice_pack_data:
                content_file = os.path.join(voice_pack_dir, "voice_content.yaml")
                with open(content_file, 'w', encoding='utf-8') as f:
                    yaml.dump(voice_pack_data["content"], f, default_flow_style=False, allow_unicode=True, indent=2)
            
            # 清除缓存
            self.voice_pack_cache.pop(voice_pack_name, None)
            
            logger.info(f"✅ 语音包创建成功: {voice_pack_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 语音包创建失败: {e}")
            return False
    
    def export_voice_pack(self, voice_pack_name: str, output_file: str) -> bool:
        """
        导出语音包
        
        Args:
            voice_pack_name: 语音包名称
            output_file: 输出文件路径
            
        Returns:
            bool: 是否导出成功
        """
        try:
            voice_pack_dir = os.path.join(self.voice_pack_path, voice_pack_name)
            
            if not os.path.exists(voice_pack_dir):
                logger.error(f"❌ 语音包不存在: {voice_pack_name}")
                return False
            
            # 创建ZIP文件
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(voice_pack_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, voice_pack_dir)
                        zipf.write(file_path, arcname)
            
            logger.info(f"✅ 语音包导出成功: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 语音包导出失败: {e}")
            return False
    
    def get_voice_pack_info(self, voice_pack_name: str) -> Dict[str, Any]:
        """
        获取语音包信息
        
        Args:
            voice_pack_name: 语音包名称
            
        Returns:
            Dict[str, Any]: 语音包信息
        """
        try:
            voice_pack_data = self.load_voice_pack(voice_pack_name)
            if not voice_pack_data:
                return {}
            
            return {
                "name": voice_pack_name,
                "version": voice_pack_data.get("version", "1.0.0"),
                "description": voice_pack_data.get("description", ""),
                "language": voice_pack_data.get("language", "zh-CN"),
                "voice_type": voice_pack_data.get("voice_type", "default"),
                "content_count": len(voice_pack_data.get("content", {}))
            }
            
        except Exception as e:
            logger.error(f"❌ 获取语音包信息失败: {e}")
            return {}

# 全局语音包管理器实例
_global_voice_pack_manager: Optional[VoicePackManager] = None

def get_voice_pack_manager() -> VoicePackManager:
    """获取全局语音包管理器实例"""
    global _global_voice_pack_manager
    if _global_voice_pack_manager is None:
        _global_voice_pack_manager = VoicePackManager()
    return _global_voice_pack_manager

def load_voice_pack(voice_pack_name: str) -> Dict[str, Any]:
    """加载语音包"""
    manager = get_voice_pack_manager()
    return manager.load_voice_pack(voice_pack_name)

def set_current_voice_pack(voice_pack_name: str) -> bool:
    """设置当前语音包"""
    manager = get_voice_pack_manager()
    return manager.set_current_voice_pack(voice_pack_name)

# 使用示例
if __name__ == "__main__":
    # 创建语音包管理器
    voice_pack_manager = VoicePackManager()
    
    # 测试语音包创建
    test_voice_pack = {
        "version": "1.0.0",
        "description": "测试语音包",
        "language": "zh-CN",
        "voice_type": "default",
        "content": {
            "system_startup": {
                "text_variants": ["系统启动完成", "初始化成功"],
                "style": "friendly"
            }
        }
    }
    
    voice_pack_manager.create_voice_pack("test_pack", test_voice_pack)
    
    # 测试语音包加载
    loaded_pack = voice_pack_manager.load_voice_pack("test_pack")
    print(f"语音包数据: {loaded_pack}")
    
    # 测试语音内容获取
    content = voice_pack_manager.get_voice_content("system_startup", "test_pack")
    print(f"语音内容: {content}")
    
    # 列出语音包
    packs = voice_pack_manager.list_voice_packs()
    print(f"语音包列表: {packs}")
    
    print("✅ 语音包管理器测试完成")
