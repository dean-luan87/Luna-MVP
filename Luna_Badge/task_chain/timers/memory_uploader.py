#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 记忆上传器
T+1天在WiFi环境下将缓存数据上传至云端
"""

import json
import logging
import time
import subprocess
import platform
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable
import requests

logger = logging.getLogger(__name__)


class MemoryUploader:
    """记忆上传器（T+1 + WiFi-only）"""
    
    def __init__(self,
                 upload_api_url: str,
                 upload_func: Optional[Callable] = None,
                 wifi_check_interval: int = 60):
        """初始化上传器
        
        Args:
            upload_api_url: 上传API地址
            upload_func: 自定义上传函数
            wifi_check_interval: WiFi检查间隔（秒）
        """
        self.upload_api_url = upload_api_url
        self.upload_func = upload_func or self._default_upload_func
        self.wifi_check_interval = wifi_check_interval
        
        logger.info(f"☁️ 记忆上传器初始化完成（API: {upload_api_url}）")
    
    def check_wifi_connected(self) -> bool:
        """检查WiFi是否连接
        
        Returns:
            是否已连接WiFi
        """
        try:
            system = platform.system()
            
            if system == "Darwin":  # macOS
                # 方法1: 使用 networksetup
                try:
                    result = subprocess.run(
                        ["networksetup", "-getairportnetwork", "en0"],
                        capture_output=True,
                        text=True,
                        timeout=3
                    )
                    if result.returncode == 0 and "You are not associated" not in result.stdout:
                        logger.debug("📶 WiFi已连接（macOS via networksetup）")
                        return True
                except:
                    pass
                
                # 方法2: 尝试使用 airport（如果存在）
                try:
                    airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
                    if Path(airport_path).exists():
                        result = subprocess.run(
                            [airport_path, "-I"],
                            capture_output=True,
                            text=True,
                            timeout=3
                        )
                        connected = "SSID:" in result.stdout and "off" not in result.stdout.lower()
                        if connected:
                            logger.debug("📶 WiFi已连接（macOS via airport）")
                        return connected
                except:
                    pass
                
                # 如果都失败，在开发环境假设已连接
                logger.warning("⚠️ macOS WiFi检测失败，假设已连接（开发模式）")
                return True
            
            elif system == "Linux":  # Linux/RV1126
                result = subprocess.run(
                    ["nmcli", "-t", "-f", "TYPE,STATE", "device", "status"],
                    capture_output=True,
                    text=True
                )
                # 检查是否有WiFi设备且状态为connected
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'wifi' in line.lower() and 'connected' in line.lower():
                        logger.debug("📶 WiFi已连接（Linux）")
                        return True
                return False
            
            else:
                logger.warning(f"⚠️ 不支持的系统：{system}，假设WiFi已连接")
                return True  # 假设已连接
                
        except Exception as e:
            logger.error(f"❌ 检查WiFi连接失败：{e}")
            return False
    
    def should_upload(self, memory_date: str) -> bool:
        """检查是否应该上传（T+1机制）
        
        Args:
            memory_date: 记忆日期
            
        Returns:
            是否应该上传
        """
        try:
            memory_dt = datetime.strptime(memory_date, "%Y-%m-%d")
            now = datetime.now()
            
            # T+1机制：至少间隔1天
            days_diff = (now.date() - memory_dt.date()).days
            
            if days_diff >= 1:
                logger.info(f"✅ 记忆满足T+1条件：{days_diff}天前")
                return True
            else:
                logger.debug(f"⏳ 记忆未满足T+1条件：{days_diff}天前")
                return False
                
        except Exception as e:
            logger.error(f"❌ 检查上传条件失败：{e}")
            return False
    
    def upload_memory_batch(self, memories: List[Dict]) -> bool:
        """批量上传记忆
        
        Args:
            memories: 记忆列表
            
        Returns:
            是否成功
        """
        if not memories:
            logger.info("📭 没有需要上传的记忆")
            return True
        
        # 检查WiFi
        if not self.check_wifi_connected():
            logger.warning("⚠️ WiFi未连接，跳过上传")
            return False
        
        try:
            logger.info(f"📤 开始上传 {len(memories)} 个记忆...")
            
            # 调用上传函数
            result = self.upload_func(memories)
            
            if result.get("success"):
                logger.info("✅ 上传成功")
                return True
            else:
                logger.error(f"❌ 上传失败：{result.get('error')}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 上传失败：{e}")
            return False
    
    def _default_upload_func(self, memories: List[Dict]) -> Dict:
        """默认上传函数
        
        Args:
            memories: 记忆列表
            
        Returns:
            上传结果
        """
        try:
            # 准备上传数据
            upload_data = {
                "timestamp": datetime.now().isoformat(),
                "memories": memories
            }
            
            # 发送HTTP POST请求
            response = requests.post(
                self.upload_api_url,
                json=upload_data,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "response": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def upload_pending_memories(self, retry_on_failure: bool = True) -> Dict:
        """上传待上传的记忆
        
        Args:
            retry_on_failure: 失败是否重试
            
        Returns:
            上传结果统计
        """
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        
        from memory_store.tools.memory_collector import MemoryCollector
        
        collector = MemoryCollector()
        
        # 获取昨天的日期（T+1）
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        
        # 收集待上传记忆
        pending = collector.collect_pending_memories(date=yesterday_str)
        
        if not pending:
            logger.info("📭 今天没有需要上传的记忆")
            return {
                "success": True,
                "uploaded_count": 0,
                "pending_count": 0
            }
        
        # 检查WiFi和上传条件
        if not self.check_wifi_connected():
            logger.warning("⚠️ WiFi未连接，取消上传")
            return {
                "success": False,
                "error": "WiFi not connected",
                "pending_count": len(pending)
            }
        
        # 验证上传条件
        for memory_item in pending:
            memory_date = memory_item["data"].get("date")
            if memory_date and not self.should_upload(memory_date):
                logger.warning(f"⚠️ 记忆日期不满足T+1条件：{memory_date}")
                continue
        
        # 执行上传
        success = self.upload_memory_batch([m["data"] for m in pending])
        
        if success:
            # 标记为已上传
            for memory_item in pending:
                collector.mark_as_uploaded(memory_item["file"])
        
        return {
            "success": success,
            "uploaded_count": len(pending) if success else 0,
            "pending_count": len(pending),
            "uploaded_at": datetime.now().isoformat()
        }


# 模拟上传函数（用于测试）
def mock_upload_func(memories: List[Dict]) -> Dict:
    """模拟上传函数"""
    logger.info(f"📤 模拟上传 {len(memories)} 个记忆到云端...")
    time.sleep(0.5)  # 模拟网络延迟
    return {"success": True, "mock": True}


# 测试函数
if __name__ == "__main__":
    import logging
    import sys
    from pathlib import Path
    
    # 添加路径
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 初始化上传器
    uploader = MemoryUploader(
        upload_api_url="https://api.luna-project.com/v1/user/memory",
        upload_func=mock_upload_func
    )
    
    # 测试WiFi检测
    print("=" * 60)
    print("📶 测试WiFi检测")
    print("=" * 60)
    print(f"WiFi已连接: {uploader.check_wifi_connected()}")
    
    # 测试上传条件
    print("\n⏰ 测试上传条件（T+1）")
    print("=" * 60)
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"昨天的记忆是否应上传: {uploader.should_upload(yesterday)}")
    print(f"今天的记忆是否应上传: {uploader.should_upload(today)}")
    
    # 测试上传
    print("\n☁️ 测试上传记忆")
    print("=" * 60)
    result = uploader.upload_pending_memories(retry_on_failure=False)
    print(json.dumps(result, indent=2, ensure_ascii=False))


