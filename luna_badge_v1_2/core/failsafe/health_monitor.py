"""
Health Monitor
1.4.1-failsafe.1: 系统健康监控引擎
监控系统各组件健康状态，产生事件但不干预业务
"""
import time
import threading
from typing import Optional, Callable

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from core.logging.log_manager import LogManager
from core.speed.speed_context import SpeedContext
from core.speed.speed_thread_pool import SpeedThreadPool
from core.failsafe.health_events import HealthEvent


class HealthMonitor(threading.Thread):
    """
    健康监控引擎
    
    功能：
    - 监控摄像头帧写入时间
    - 监控 YOLO 推理更新时间
    - 监控线程心跳
    - 监控 CPU / 内存占用
    - 超阈值时产生事件（通过回调派发）
    
    特性：
    - 独立监控线程，不干预业务
    - 只负责检测和事件派发
    - 不直接调用任何导航或推理逻辑
    """
    
    def __init__(
        self,
        camera_timeout: float = 0.5,
        infer_timeout: float = 0.8,
        heartbeat_timeout: float = 1.2,
        cpu_threshold: float = 80.0,
        mem_threshold: float = 85.0,
        check_interval: float = 0.1,
        now_fn: Optional[Callable[[], float]] = None,
    ):
        """
        初始化健康监控器
        
        Args:
            camera_timeout: 摄像头超时时间（秒），默认 0.5 秒
            infer_timeout: 推理超时时间（秒），默认 0.8 秒
            heartbeat_timeout: 心跳超时时间（秒），默认 1.2 秒
            cpu_threshold: CPU 使用率阈值（%），默认 80%
            mem_threshold: 内存使用率阈值（%），默认 85%
            check_interval: 检查间隔（秒），默认 0.1 秒
        """
        super().__init__(daemon=True, name="HealthMonitor")
        self.logger = LogManager.get_logger("HealthMonitor")
        # [v1.4.9 P0-2-B] 时间源注入点：默认 wall clock；Replay 下绑定 ReplayClock.now()
        self._now: Callable[[], float] = now_fn or time.time
        
        self.running = False
        self._stop_event = threading.Event()
        
        self.camera_timeout = camera_timeout
        self.infer_timeout = infer_timeout
        self.heartbeat_timeout = heartbeat_timeout
        self.cpu_threshold = cpu_threshold
        self.mem_threshold = mem_threshold
        self.check_interval = check_interval

        # --------------------------------------------------------------
        # [1.4.X frozen] FailSafe 触发阈值（配置可调，但结构语义冻结）
        #
        # 这些阈值属于“对用户可感知”的稳定性行为面：触发降级/应急的频率会影响系统
        # 是否进入应急播报与降级模式。
        #
        # 配置键（存在于 config/default.yaml）：
        # - failsafe.health_monitor.camera_timeout
        # - failsafe.health_monitor.infer_timeout
        # - failsafe.health_monitor.heartbeat_timeout
        # - failsafe.health_monitor.cpu_threshold
        # - failsafe.health_monitor.mem_threshold
        # - failsafe.health_monitor.check_interval
        #
        # 注意：本模块构造函数提供默认值；若上层未从 ConfigCenter 注入，
        # 则将使用硬编码默认值（这会影响“可配置性”，但不应改变语义结构）。
        # --------------------------------------------------------------
        
        self.last_check = 0.0
        self.event_callback: Optional[Callable[[str], None]] = None
        
        # 事件计数（用于统计）
        self.event_counts: dict[str, int] = {}
        
        if not PSUTIL_AVAILABLE:
            self.logger.warning("psutil not available, CPU/memory monitoring will be disabled")

    def set_callback(self, cb: Callable[[str], None]) -> None:
        """
        设置事件回调函数
        
        Args:
            cb: 回调函数，接收事件类型字符串
        """
        self.event_callback = cb
        self.logger.debug("Event callback set")

    def start_monitor(self) -> None:
        """启动监控"""
        if not self.running:
            self.running = True
            self._stop_event.clear()
            self.start()
            self.logger.info("[HealthMonitor] started")

    def stop_monitor(self, timeout: float = 2.0) -> None:
        """
        停止监控
        
        Args:
            timeout: 等待线程结束的超时时间（秒）
        """
        if self.running:
            self.running = False
            self._stop_event.set()
            self.join(timeout=timeout)
            self.logger.info("[HealthMonitor] stopped")

    def emit(self, event: str) -> None:
        """
        派发健康事件
        
        Args:
            event: 事件类型（HealthEvent 常量）
        """
        # 统计事件
        self.event_counts[event] = self.event_counts.get(event, 0) + 1
        
        # 调用回调
        if self.event_callback:
            try:
                self.event_callback(event)
            except Exception as e:
                self.logger.exception(f"Event callback error: {e}")
        
        self.logger.warning(f"[HealthMonitor] Event: {event}")

    def run(self) -> None:
        """监控主循环"""
        self.logger.debug("[HealthMonitor] run loop started")
        
        while self.running and not self._stop_event.is_set():
            try:
                now = self._now()
                self.last_check = now
                
                # 1. Camera 超时（无新帧）
                cam = SpeedContext.camera_worker
                if cam is not None:
                    try:
                        last_write_ts = cam.buffer.last_write_ts
                        if last_write_ts > 0 and (now - last_write_ts) > self.camera_timeout:
                            self.emit(HealthEvent.CAMERA_STALE)
                    except Exception as e:
                        self.logger.debug(f"Camera check error: {e}")
                
                # 2. YOLO 推理超时
                if SpeedContext.last_yolo_ts > 0:
                    if (now - SpeedContext.last_yolo_ts) > self.infer_timeout:
                        self.emit(HealthEvent.INFER_STALE)
                
                # 3. 线程心跳检测
                try:
                    for w in SpeedThreadPool.workers:
                        if hasattr(w, 'last_heartbeat') and w.last_heartbeat > 0:
                            if (now - w.last_heartbeat) > self.heartbeat_timeout:
                                self.emit(HealthEvent.THREAD_HANG)
                except Exception as e:
                    self.logger.debug(f"Thread heartbeat check error: {e}")
                
                # 4. 系统 CPU 检测
                if PSUTIL_AVAILABLE:
                    try:
                        cpu_percent = psutil.cpu_percent(interval=0.0)  # 非阻塞
                        if cpu_percent > self.cpu_threshold:
                            self.emit(HealthEvent.HIGH_CPU)
                    except Exception as e:
                        self.logger.debug(f"CPU check error: {e}")
                
                # 5. 系统内存检测
                if PSUTIL_AVAILABLE:
                    try:
                        mem_percent = psutil.virtual_memory().percent
                        if mem_percent > self.mem_threshold:
                            self.emit(HealthEvent.HIGH_MEM)
                    except Exception as e:
                        self.logger.debug(f"Memory check error: {e}")
                
            except Exception as e:
                self.logger.exception(f"HealthMonitor check error: {e}")
            
            # 等待检查间隔
            self._stop_event.wait(self.check_interval)
        
        self.logger.debug("[HealthMonitor] run loop ended")

    def get_stats(self) -> dict:
        """
        获取统计信息
        
        Returns:
            包含事件计数等统计信息的字典
        """
        return {
            "running": self.running,
            "last_check": self.last_check,
            "event_counts": dict(self.event_counts),
            "has_callback": self.event_callback is not None,
        }

    # ------------------------------------------------------------------
    # [v1.4.9 P0-2-B] Replay determinism support (explicit reset)
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """重置统计与计数（用于 Replay/测试，不改变监控语义）。"""
        self.last_check = 0.0
        self.event_counts.clear()
