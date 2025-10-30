#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna 后台上传管理器
实现WiFi环境检测和t+1上传机制
"""

import json
import logging
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable
import subprocess
import platform

logger = logging.getLogger(__name__)


class BackgroundUploader:
    """后台上传管理器（t+1机制）"""
    
    def __init__(self, 
                 cache_manager,
                 upload_func: Callable,
                 wifi_check_interval: int = 30,
                 upload_check_interval: int = 300):
        """初始化上传管理器
        
        Args:
            cache_manager: 缓存管理器实例
            upload_func: 上传函数
            wifi_check_interval: WiFi检测间隔（秒）
            upload_check_interval: 上传检查间隔（秒）
        """
        self.cache_manager = cache_manager
        self.upload_func = upload_func
        
        self.wifi_check_interval = wifi_check_interval
        self.upload_check_interval = upload_check_interval
        
        self.is_running = False
        self.upload_thread = None
        
        # 状态
        self.is_wifi_connected = False
        self.last_upload_time = None
        
        logger.info("☁️ 后台上传管理器初始化完成")
    
    def start(self):
        """启动后台上传服务"""
        if self.is_running:
            logger.warning("⚠️ 上传服务已在运行")
            return
        
        self.is_running = True
        self.upload_thread = threading.Thread(target=self._upload_loop, daemon=True)
        self.upload_thread.start()
        
        logger.info("🚀 后台上传服务已启动")
    
    def stop(self):
        """停止后台上传服务"""
        self.is_running = False
        
        if self.upload_thread:
            self.upload_thread.join(timeout=5)
        
        logger.info("🛑 后台上传服务已停止")
    
    def _upload_loop(self):
        """上传循环"""
        while self.is_running:
            try:
                # 检测WiFi连接
                self.is_wifi_connected = self._check_wifi_connected()
                
                if self.is_wifi_connected:
                    # 检查是否需要上传
                    if self._should_upload():
                        # 执行上传
                        self._perform_upload()
                else:
                    logger.debug("📶 WiFi未连接，跳过上传检查")
                
                # 等待
                time.sleep(self.upload_check_interval)
                
            except Exception as e:
                logger.error(f"❌ 上传循环错误：{e}")
                time.sleep(self.upload_check_interval)
    
    def _check_wifi_connected(self) -> bool:
        """检查WiFi是否连接
        
        Returns:
            是否已连接WiFi
        """
        try:
            system = platform.system()
            
            if system == "Darwin":  # macOS
                result = subprocess.run(
                    ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                    capture_output=True,
                    text=True
                )
                return "SSID:" in result.stdout
            
            elif system == "Linux":  # Linux/RV1126
                result = subprocess.run(
                    ["nmcli", "-t", "-f", "TYPE", "device", "status"],
                    capture_output=True,
                    text=True
                )
                return "wifi" in result.stdout.lower()
            
            else:
                logger.warning(f"⚠️ 不支持的系统：{system}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 检查WiFi连接失败：{e}")
            return False
    
    def _should_upload(self) -> bool:
        """检查是否应该上传（t+1机制）
        
        Returns:
            是否应该上传
        """
        # 检查上传队列
        upload_queue = self.cache_manager.get_upload_queue()
        
        if not upload_queue:
            return False
        
        # 检查上次上传时间
        cache_stats = self.cache_manager.get_cache_stats()
        last_upload_time = cache_stats.get("last_upload_time")
        
        if not last_upload_time:
            # 从未上传过，立即上传
            return True
        
        # t+1机制：上次上传后至少1小时
        try:
            last_upload = datetime.fromisoformat(last_upload_time)
            time_diff = datetime.now() - last_upload
            
            # 至少间隔1小时才上传
            if time_diff >= timedelta(hours=1):
                return True
        except:
            pass
        
        return False
    
    def _perform_upload(self):
        """执行上传"""
        try:
            logger.info("📤 开始上传数据...")
            
            # 导出待上传数据
            upload_package = self.cache_manager.export_cache_for_upload()
            
            if not upload_package["maps"] and not upload_package["scenes"] and not upload_package["behaviors"]:
                logger.info("📭 没有需要上传的数据")
                return
            
            # 调用上传函数
            upload_result = self.upload_func(upload_package)
            
            if upload_result.get("success"):
                # 标记为已上传
                self._mark_all_as_uploaded()
                
                # 更新上传时间
                self._update_upload_time()
                
                logger.info(f"✅ 上传成功：{upload_package['metadata']}")
            else:
                logger.error(f"❌ 上传失败：{upload_result.get('error')}")
                
        except Exception as e:
            logger.error(f"❌ 执行上传失败：{e}")
    
    def _mark_all_as_uploaded(self):
        """标记所有数据为已上传"""
        maps_cache = self.cache_manager._load_cache(self.cache_manager.maps_cache_file)
        scenes_cache = self.cache_manager._load_cache(self.cache_manager.scenes_cache_file)
        behavior_cache = self.cache_manager._load_cache(self.cache_manager.user_behavior_cache_file)
        
        # 标记地图
        for map_item in maps_cache.get("maps", []):
            if not map_item.get("uploaded"):
                map_item["uploaded"] = True
                map_item["uploaded_at"] = datetime.now().isoformat()
        
        # 标记场景
        for scene_item in scenes_cache.get("scenes", []):
            if not scene_item.get("uploaded"):
                scene_item["uploaded"] = True
                scene_item["uploaded_at"] = datetime.now().isoformat()
        
        # 标记行为
        for behavior_item in behavior_cache.get("behaviors", []):
            if not behavior_item.get("uploaded"):
                behavior_item["uploaded"] = True
                behavior_item["uploaded_at"] = datetime.now().isoformat()
        
        # 保存
        self.cache_manager._save_cache(self.cache_manager.maps_cache_file, maps_cache)
        self.cache_manager._save_cache(self.cache_manager.scenes_cache_file, scenes_cache)
        self.cache_manager._save_cache(self.cache_manager.user_behavior_cache_file, behavior_cache)
    
    def _update_upload_time(self):
        """更新上传时间"""
        last_upload = self.cache_manager._load_cache(self.cache_manager.last_upload_file)
        last_upload["last_upload_time"] = datetime.now().isoformat()
        last_upload["upload_count"] = last_upload.get("upload_count", 0) + 1
        self.cache_manager._save_cache(self.cache_manager.last_upload_file, last_upload)
    
    def force_upload_now(self) -> bool:
        """强制立即上传（手动触发）
        
        Returns:
            是否成功
        """
        try:
            logger.info("🔄 强制立即上传...")
            self._perform_upload()
            return True
        except Exception as e:
            logger.error(f"❌ 强制上传失败：{e}")
            return False
    
    def get_status(self) -> Dict:
        """获取上传器状态
        
        Returns:
            状态信息
        """
        cache_stats = self.cache_manager.get_cache_stats()
        
        return {
            "is_running": self.is_running,
            "is_wifi_connected": self.is_wifi_connected,
            "last_upload_time": cache_stats.get("last_upload_time"),
            "upload_count": cache_stats.get("upload_count"),
            "pending_uploads": {
                "maps": cache_stats.get("unuploaded_maps"),
                "scenes": cache_stats.get("unuploaded_scenes"),
                "behaviors": cache_stats.get("unuploaded_behaviors")
            }
        }


def mock_upload_function(upload_package: Dict) -> Dict:
    """模拟上传函数（用于测试）
    
    Args:
        upload_package: 上传数据包
        
    Returns:
        上传结果
    """
    try:
        # 模拟网络延迟
        time.sleep(0.5)
        
        # 模拟上传成功
        logger.info("📤 模拟上传到云端...")
        
        return {
            "success": True,
            "uploaded_at": datetime.now().isoformat(),
            "data_size": json.dumps(upload_package).__len__()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# 测试函数
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 导入缓存管理器
    from core.memory_cache_manager import MemoryCacheManager
    
    # 初始化缓存和上传器
    cache_manager = MemoryCacheManager()
    uploader = BackgroundUploader(
        cache_manager=cache_manager,
        upload_func=mock_upload_function,
        wifi_check_interval=10,
        upload_check_interval=60
    )
    
    # 添加一些测试数据
    print("=" * 60)
    print("📝 添加测试数据")
    print("=" * 60)
    cache_manager.cache_map({"map_id": "test_map", "path_name": "测试路径"})
    cache_manager.cache_scene({"scene_id": "test_scene", "location": "测试位置"})
    cache_manager.record_navigation_event("test_event", {"data": "test"})
    
    # 显示状态
    print("\n📊 上传器状态")
    print("=" * 60)
    status = uploader.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    # 测试强制上传
    print("\n🔄 测试强制上传")
    print("=" * 60)
    uploader.force_upload_now()
    
    # 再次显示状态
    print("\n📊 上传后的状态")
    print("=" * 60)
    status = uploader.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))


