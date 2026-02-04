"""
Auto Recovery Manager
1.4.1-failsafe.4: 自动恢复管理
当系统稳定一段时间后自动从 safe/degraded 恢复到 normal
"""
import time
import threading
from typing import Optional

from core.logging.log_manager import LogManager
from core.config.config_center import ConfigCenter
from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.health_events import HealthEvent


class AutoRecoveryManager(threading.Thread):
    """
    自动恢复管理 v1
    
    功能：
    - 定期检查 FailSafeManager 状态和最近严重事件时间
    - 满足"稳定时长"条件时自动调用 reset_mode()
    - 默认不自动重启线程，仅做模式恢复
    
    设计原则：
    - 保守策略（默认 15 秒稳定期）
    - 可配置（可通过配置完全关闭）
    - 非阻塞
    - 防御性编程
    """
    
    def __init__(self):
        """初始化自动恢复管理器"""
        super().__init__(daemon=True, name="AutoRecoveryManager")
        self.logger = LogManager.get_logger("AutoRecoveryManager")
        self.running = False
        self._stop_event = threading.Event()
        
        # 从配置读取参数
        cfg = ConfigCenter.get("failsafe.recovery", {}) or {}
        self.enabled: bool = cfg.get("enabled", True)
        self.stable_duration_sec: float = cfg.get("stable_duration_sec", 15.0)
        self.check_interval_sec: float = cfg.get("check_interval_sec", 1.0)
        self.auto_restart_enabled: bool = cfg.get("auto_restart_enabled", False)
        
        self.failsafe = FailSafeManager.get_instance()
        
        self.recovery_count = 0
        self.last_recovery_time = 0.0

    def start_manager(self) -> None:
        """启动自动恢复管理器"""
        if not self.enabled:
            self.logger.info("[AutoRecovery] Disabled by config")
            return
        
        if not self.running:
            self.running = True
            self._stop_event.clear()
            self.start()
            self.logger.info(f"[AutoRecovery] started (stable_duration={self.stable_duration_sec}s, check_interval={self.check_interval_sec}s)")

    def stop_manager(self, timeout: float = 2.0) -> None:
        """
        停止自动恢复管理器
        
        Args:
            timeout: 等待线程结束的超时时间（秒）
        """
        if self.running:
            self.running = False
            self._stop_event.set()
            self.join(timeout=timeout)
            self.logger.info("[AutoRecovery] stopped")

    def run(self) -> None:
        """自动恢复主循环"""
        self.logger.debug("[AutoRecovery] run loop started")
        
        while self.running and not self._stop_event.is_set():
            try:
                self._check_and_recover()
            except Exception as e:
                self.logger.exception(f"[AutoRecovery] error: {e}")
            
            # 等待检查间隔
            self._stop_event.wait(self.check_interval_sec)
        
        self.logger.debug("[AutoRecovery] run loop ended")

    def _check_and_recover(self) -> None:
        """
        检查恢复条件并执行恢复
        
        逻辑：
        1. 检查是否处于保护模式
        2. 检查最近严重事件时间
        3. 如果稳定时间达标，执行恢复
        """
        # 若当前没有任何保护模式，则不需要恢复
        if not self.failsafe.has_active_protection():
            return

        now = time.time()

        # 严重事件集合（触发 safe 模式的那些）
        critical_types = [
            HealthEvent.CAMERA_DEAD,
            HealthEvent.CAMERA_STALE,
            HealthEvent.INFER_DEAD,
            HealthEvent.INFER_STALE,
            HealthEvent.THREAD_HANG,
        ]

        last_critical_ts = self.failsafe.get_last_event_time(critical_types)
        if last_critical_ts == 0:
            # 没有严重事件记录，属于异常情况，保守起见不恢复
            self.logger.debug("[AutoRecovery] No critical events found, skipping recovery")
            return

        elapsed = now - last_critical_ts
        if elapsed < self.stable_duration_sec:
            # 稳定时间未达标，不恢复
            self.logger.debug(f"[AutoRecovery] Not stable enough ({elapsed:.1f}s < {self.stable_duration_sec}s)")
            return

        # 条件满足 → 恢复到 NORMAL
        self.logger.warning(
            f"[AutoRecovery] Stable for {elapsed:.1f}s, resetting FailSafeManager to NORMAL"
        )
        self.failsafe.reset_mode()
        self.recovery_count += 1
        self.last_recovery_time = now

        # 如后续版本启用线程软重启，可在此调用
        if self.auto_restart_enabled:
            self._try_soft_restart_workers()

    def _try_soft_restart_workers(self) -> None:
        """
        v1 默认不启用，仅预留接口
        
        未来可按需实现：
        - 重启 CameraStreamWorker
        - 重启 VisionInferWorker
        - 等
        """
        self.logger.info("[AutoRecovery] soft restart is enabled, but no workers are wired yet")

    def get_stats(self) -> dict:
        """
        获取统计信息
        
        Returns:
            包含恢复次数等统计信息的字典
        """
        return {
            "enabled": self.enabled,
            "running": self.running,
            "recovery_count": self.recovery_count,
            "last_recovery_time": self.last_recovery_time,
            "stable_duration_sec": self.stable_duration_sec,
            "check_interval_sec": self.check_interval_sec,
            "auto_restart_enabled": self.auto_restart_enabled,
        }
















