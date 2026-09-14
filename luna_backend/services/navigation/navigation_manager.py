"""
导航管理器服务层 (v1.2.0)
封装NavigationManager，提供统一的导航服务接口
"""

import sys
import os

# 添加Luna_Badge路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "Luna_Badge"))

from typing import Dict, Any, Optional, List
from core.logger import logger

try:
    from core.navigation_manager import NavigationManager as CoreNavigationManager
except ImportError:
    CoreNavigationManager = None


class NavigationManager:
    """导航管理器服务类"""
    
    def __init__(self):
        """初始化导航管理器"""
        self.manager: Optional[CoreNavigationManager] = None
        self._init_manager()
    
    def _init_manager(self):
        """初始化核心导航管理器"""
        try:
            if CoreNavigationManager:
                # 创建TTS回调函数
                def tts_callback(text: str, style: str = "calm"):
                    """TTS播报回调"""
                    try:
                        from services.tts.tts_engine import get_tts_engine
                        tts_engine = get_tts_engine()
                        if tts_engine:
                            tts_engine.synthesize(text, style=style)
                    except:
                        pass
                
                self.manager = CoreNavigationManager(tts_callback=tts_callback)
                logger.info("✅ 导航管理器初始化成功", module="Navigation")
            else:
                logger.warn("导航管理器模块未找到", module="Navigation")
        except Exception as e:
            logger.error("导航管理器初始化失败", details={"error": str(e)}, module="Navigation")
    
    def start(self, destination: str, route_segments: Optional[List] = None) -> bool:
        """开始导航"""
        if not self.manager:
            return False
        try:
            return self.manager.start_navigation(destination, route_segments)
        except Exception as e:
            logger.error("启动导航失败", details={"error": str(e)}, module="Navigation")
            return False
    
    def update(self, lat: float, lng: float, detected_hazards: Optional[List] = None):
        """更新位置"""
        if not self.manager:
            return
        try:
            self.manager.update_position(lat, lng, detected_hazards)
        except Exception as e:
            logger.error("更新位置失败", details={"error": str(e)}, module="Navigation")
    
    def pause(self, reason: str = "用户暂停"):
        """暂停导航"""
        if not self.manager:
            return
        try:
            self.manager.pause_navigation(reason)
        except Exception as e:
            logger.error("暂停导航失败", details={"error": str(e)}, module="Navigation")
    
    def resume(self):
        """恢复导航"""
        if not self.manager:
            return
        try:
            self.manager.resume_navigation()
        except Exception as e:
            logger.error("恢复导航失败", details={"error": str(e)}, module="Navigation")
    
    def cancel(self, reason: str = "用户取消"):
        """取消导航"""
        if not self.manager:
            return
        try:
            self.manager.cancel_navigation(reason)
        except Exception as e:
            logger.error("取消导航失败", details={"error": str(e)}, module="Navigation")
    
    def complete(self):
        """完成导航"""
        if not self.manager:
            return
        try:
            self.manager.complete_navigation()
        except Exception as e:
            logger.error("完成导航失败", details={"error": str(e)}, module="Navigation")
    
    def status(self) -> Dict[str, Any]:
        """获取导航状态"""
        if not self.manager:
            return {"status": "not_initialized"}
        try:
            return self.manager.get_status() or {"status": "idle"}
        except Exception as e:
            logger.error("获取导航状态失败", details={"error": str(e)}, module="Navigation")
            return {"status": "error", "error": str(e)}


# 全局实例
_navigation_manager: Optional[NavigationManager] = None

def get_navigation_manager() -> NavigationManager:
    """获取全局导航管理器实例"""
    global _navigation_manager
    if _navigation_manager is None:
        _navigation_manager = NavigationManager()
    return _navigation_manager



