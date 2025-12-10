#!/usr/bin/env python3
"""
系统循环集成点
v1.4.2: 整合 RecoveryCenter, SafeMode, 心跳机制
"""
import time
import logging
from typing import Callable, Optional

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from core.system.system_recovery_center import RecoveryCenter
from core.system.safe_mode import SafeModeManager, SafeModeContext

logger = logging.getLogger(__name__)


class SystemLoop:
    """
    系统循环：整合恢复中心、安全模式、心跳机制
    """
    
    def __init__(
        self,
        recovery_center: Optional[RecoveryCenter] = None,
        safe_mode: Optional[SafeModeManager] = None,
        get_cpu_load: Optional[Callable[[], float]] = None,
        tts_say: Optional[Callable[[str], None]] = None,
        restart_vision: Optional[Callable[[], None]] = None,
        restart_speech: Optional[Callable[[], None]] = None,
        restart_navigation: Optional[Callable[[], None]] = None,
    ):
        """
        初始化系统循环
        
        Args:
            recovery_center: 恢复中心（如果为 None 则自动创建）
            safe_mode: 安全模式（如果为 None 则自动创建）
            get_cpu_load: 获取 CPU 负载的函数
            tts_say: TTS 播报函数
            restart_vision: 重启视觉模块的函数
            restart_speech: 重启语音模块的函数
            restart_navigation: 重启导航模块的函数
        """
        # 默认 CPU 负载获取函数
        if get_cpu_load is None:
            get_cpu_load = self._default_get_cpu_load
        
        # 默认 TTS 函数
        if tts_say is None:
            tts_say = self._default_tts_say
        
        # 创建恢复中心
        if recovery_center is None:
            def enter_safe_mode():
                if safe_mode:
                    safe_mode.enter()
            
            recovery_center = RecoveryCenter(
                get_cpu_load=get_cpu_load,
                safe_mode_enter=enter_safe_mode,
                restart_vision=restart_vision,
                restart_speech=restart_speech,
            )
        
        # 创建安全模式
        if safe_mode is None:
            safe_mode = SafeModeManager(tts_say=tts_say)
        
        self.recovery_center = recovery_center
        self.safe_mode = safe_mode
        self.restart_navigation = restart_navigation
        
        # 注册模块
        self._register_modules()
        
        # 循环状态
        self.last_tick_ts = 0.0
        self.tick_interval = 1.0  # 每秒 tick 一次
        
        logger.info("[SYSTEM_LOOP] Initialized")
    
    def _register_modules(self):
        """注册需要监控的模块"""
        self.recovery_center.register_module("vision", timeout_seconds=5.0)
        self.recovery_center.register_module("speech", timeout_seconds=5.0)
        self.recovery_center.register_module("navigation", timeout_seconds=10.0)
        logger.info("[SYSTEM_LOOP] Modules registered: vision, speech, navigation")
    
    def _default_get_cpu_load(self) -> float:
        """默认 CPU 负载获取函数"""
        if PSUTIL_AVAILABLE:
            try:
                return psutil.cpu_percent(interval=0.1) / 100.0
            except Exception as e:
                logger.warning(f"[SYSTEM_LOOP] Failed to get CPU load: {e}")
                return 0.5
        return 0.5
    
    def _default_tts_say(self, text: str) -> None:
        """默认 TTS 函数"""
        logger.info(f"[SYSTEM_LOOP] TTS: {text}")
    
    def tick(self) -> None:
        """
        系统循环 tick（应该每 1 秒调用一次）
        """
        now = time.time()
        
        # 检查是否需要 tick
        if now - self.last_tick_ts < self.tick_interval:
            return
        
        self.last_tick_ts = now
        
        # 恢复中心 tick
        self.recovery_center.tick()
        
        # 检查导航模块心跳（如果需要重启）
        health = self.recovery_center.get_health_status()
        nav_healthy = health["modules"].get("navigation", {}).get("healthy", True)
        
        if not nav_healthy and self.restart_navigation:
            logger.warning("[SYSTEM_LOOP] Navigation module unhealthy, attempting restart")
            try:
                self.restart_navigation()
                self.recovery_center.update_heartbeat("navigation")
            except Exception as e:
                logger.exception(f"[SYSTEM_LOOP] Failed to restart navigation: {e}")
                # 导航模块重启失败，进入安全模式
                self.safe_mode.enter()
    
    def update_heartbeat(self, module_name: str) -> None:
        """
        更新模块心跳
        
        Args:
            module_name: 模块名称（vision/speech/navigation）
        """
        self.recovery_center.update_heartbeat(module_name)
        logger.debug(f"[SYSTEM_LOOP] Heartbeat updated: {module_name}")
    
    def get_health_status(self) -> dict:
        """获取系统健康状态"""
        return self.recovery_center.get_health_status()
    
    def is_safe_mode_active(self) -> bool:
        """检查是否处于安全模式"""
        return self.safe_mode.is_active()
    
    def handle_safe_mode_frame(self, obstacle_distance: Optional[float]) -> None:
        """
        在安全模式下处理帧
        
        Args:
            obstacle_distance: 障碍物距离（米）
        """
        if not self.safe_mode.is_active():
            return
        
        ctx = SafeModeContext(obstacle_distance=obstacle_distance)
        self.safe_mode.handle_frame(ctx)




