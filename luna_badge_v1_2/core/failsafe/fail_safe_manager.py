"""
Fail Safe Manager
1.4.1-failsafe.2: 应急接管模块
接收 HealthMonitor 事件，执行应急策略（v1 仅做状态标记和日志）
"""
import time
from typing import List, Tuple, Optional

from core.logging.log_manager import LogManager
from core.speed.speed_context import SpeedContext
from core.failsafe.health_events import HealthEvent


class FailSafeManager:
    """
    FailSafeManager v1 职责：
    
    - 接收 HealthMonitor 上报的事件
    - 根据事件设置 SpeedContext 的模式（normal / safe / degraded）
    - 触发应急模式（仅限：日志 + 标记，后续版本再挂 TTS / 重启等）
    
    设计原则（v1）：
    - 不主动停止线程
    - 不主动重启线程
    - 不直接终止主循环
    - 不直接 exit() 程序
    - 只改变 SpeedContext 模式、产生日志、更新状态标记
    """
    
    _instance: Optional["FailSafeManager"] = None
    
    def __init__(self):
        """初始化 FailSafeManager"""
        self.logger = LogManager.get_logger("FailSafeManager")
        self.emergency_active = False
        self.degraded_active = False
        self.event_history: List[Tuple[float, str]] = []
        self.last_emergency_time = 0.0
        self.last_degraded_time = 0.0

    @classmethod
    def get_instance(cls) -> "FailSafeManager":
        """
        获取单例实例
        
        Returns:
            FailSafeManager 实例
        """
        if cls._instance is None:
            cls._instance = FailSafeManager()
        return cls._instance

    @classmethod
    def attach_to_health_monitor(cls, health_monitor) -> "FailSafeManager":
        """
        初始化并把自身挂到 HealthMonitor 的回调上
        
        Args:
            health_monitor: HealthMonitor 实例
        
        Returns:
            FailSafeManager 实例
        """
        inst = cls.get_instance()
        health_monitor.set_callback(inst.on_health_event)
        inst.logger.info("[FailSafeManager] attached to HealthMonitor")
        return inst

    def on_health_event(self, event: str) -> None:
        """
        健康事件入口，由 HealthMonitor 调用
        
        根据事件类型执行不同等级的降级/应急策略
        
        Args:
            event: 事件类型（HealthEvent 常量）
        """
        now = time.time()
        self.event_history.append((now, event))
        
        # 限制历史记录长度
        if len(self.event_history) > 100:
            self.event_history.pop(0)
        
        self.logger.warning(f"[FailSafeManager] Receive event: {event}")

        # 严重事件 → 进入应急模式
        if event in (
            HealthEvent.CAMERA_DEAD,
            HealthEvent.CAMERA_STALE,
            HealthEvent.INFER_DEAD,
            HealthEvent.INFER_STALE,
            HealthEvent.THREAD_HANG,
        ):
            self.enter_emergency_mode(reason=event)

        # 资源压力事件 → 进入降级模式
        elif event in (HealthEvent.HIGH_CPU, HealthEvent.HIGH_MEM):
            self.enter_degraded_mode(reason=event)

    # ====== 模式控制 ======

    def enter_emergency_mode(self, reason: str) -> None:
        """
        进入应急模式
        
        Args:
            reason: 触发原因（事件类型）
        """
        if self.emergency_active:
            # 已经在应急模式中，防止重复刷日志
            return

        self.emergency_active = True
        self.degraded_active = True  # 应急模式视为更强降级
        self.last_emergency_time = time.time()
        SpeedContext.set_mode("safe")

        self.logger.error(f"[FailSafeManager] Enter EMERGENCY mode, reason={reason}")

        # TODO: 未来版本在这里挂 TTS 播报，例如：
        #   "当前视觉识别异常，请原地停下，确认安全后再继续移动。"
        # 暂时只做日志 + 状态标记，不做语音和自动重启，降低风险。

    def enter_degraded_mode(self, reason: str) -> None:
        """
        进入降级模式
        
        Args:
            reason: 触发原因（事件类型）
        """
        if self.emergency_active:
            # 应急模式优先级更高，无需重复设置
            return
        if self.degraded_active:
            # 已经在降级模式中
            return

        self.degraded_active = True
        self.last_degraded_time = time.time()
        SpeedContext.set_mode("fast")  # 使用 "fast" 作为降级模式（或可以扩展为 "degraded"）
        
        # 注意：SpeedContext 目前只支持 "normal", "fast", "safe"
        # 如果需要 "degraded" 模式，需要在 SpeedContext 中扩展
        # 暂时使用 "fast" 作为降级模式的标记
        
        self.logger.warning(f"[FailSafeManager] Enter DEGRADED mode, reason={reason}")

        # TODO: 未来版本可以在这里：
        #   - 通知 ModelSwitcher 强制使用 light 模型
        #   - 暂停部分非关键视觉任务（如 OCR）
        #   - 降低 TTS 频率

    def reset_mode(self) -> None:
        """
        手动恢复正常模式（后续可由自动恢复逻辑调用）
        """
        if not self.emergency_active and not self.degraded_active:
            # 已经在正常模式
            return
        
        self.emergency_active = False
        self.degraded_active = False
        SpeedContext.set_mode("normal")
        self.logger.info("[FailSafeManager] Reset to NORMAL mode")

    def get_stats(self) -> dict:
        """
        获取统计信息
        
        Returns:
            包含当前状态等统计信息的字典
        """
        return {
            "emergency_active": self.emergency_active,
            "degraded_active": self.degraded_active,
            "current_mode": SpeedContext.get_mode(),
            "event_count": len(self.event_history),
            "last_emergency_time": self.last_emergency_time,
            "last_degraded_time": self.last_degraded_time,
        }

