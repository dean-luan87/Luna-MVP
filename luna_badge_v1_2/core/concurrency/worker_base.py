"""
Worker 基类
提供通用的 Worker 模板，用于后续 SpeedEngine 等场景
"""
import threading
import time
from abc import ABC, abstractmethod
from typing import Optional
import logging

# 使用标准 logging，避免循环依赖
# 在实际使用时，Worker 可以通过 LogManager.get_logger() 获取日志器
logger = logging.getLogger(__name__)


class WorkerBase(ABC):
    """
    Worker 基类
    
    提供通用的 Worker 模板，子类只需实现 tick() 方法
    """
    
    def __init__(self, name: str, daemon: bool = True, interval: float = 0.0):
        """
        初始化 Worker
        
        Args:
            name: Worker 名称
            daemon: 是否为守护线程
            interval: tick 间隔（秒），0 表示不等待
        """
        self._name = name
        self._daemon = daemon
        self._interval = interval
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        logger.debug(f"WorkerBase '{name}' created (daemon={daemon}, interval={interval})")

    def start(self) -> None:
        """启动 Worker"""
        if self._thread and self._thread.is_alive():
            logger.warning(f"Worker '{self._name}' is already running")
            return

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run_loop,
            name=self._name,
            daemon=self._daemon
        )
        self._thread.start()
        logger.info(f"Worker '{self._name}' started")

    def stop(self, timeout: float | None = None) -> None:
        """
        停止 Worker
        
        Args:
            timeout: 等待线程结束的超时时间（秒），None 表示无限等待
        """
        if not self._thread or not self._thread.is_alive():
            logger.warning(f"Worker '{self._name}' is not running")
            return

        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=timeout)
        logger.info(f"Worker '{self._name}' stopped")

    def is_running(self) -> bool:
        """
        检查 Worker 是否正在运行
        
        Returns:
            True 如果 Worker 正在运行
        """
        return self._thread is not None and self._thread.is_alive()

    def _run_loop(self) -> None:
        """Worker 主循环"""
        logger.debug(f"Worker '{self._name}' run loop started")
        
        while not self._stop_event.is_set():
            try:
                self.tick()
            except Exception as e:
                logger.exception(f"Worker '{self._name}' tick error: {e}")
            
            if self._interval > 0:
                # 使用 wait 可以更及时响应 stop 信号
                self._stop_event.wait(self._interval)
        
        logger.debug(f"Worker '{self._name}' run loop ended")

    @abstractmethod
    def tick(self) -> None:
        """
        子类实现具体逻辑
        
        这个方法会被循环调用，子类应该实现具体的业务逻辑
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement tick()")

