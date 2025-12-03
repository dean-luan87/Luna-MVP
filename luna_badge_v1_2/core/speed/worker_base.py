"""
Speed Engine Worker 基类
1.4.1-speed.1: 线程基础框架
"""
import threading
import time
from typing import Optional
import logging

# 延迟初始化 logger，避免循环依赖


class WorkerBase(threading.Thread):
    """
    通用线程基类，负责：
    - 标准化启动/停止
    - 统一异常捕获
    - 心跳时间记录
    
    注意：这是 Speed Engine 专用的 WorkerBase，与 core/concurrency/worker_base.py 不同
    """
    
    def __init__(self, name: str):
        super().__init__(daemon=True)
        self.name = name
        self._running = False
        # 延迟初始化 logger
        self._logger = None
        self.last_heartbeat: Optional[float] = 0
    
    @property
    def logger(self):
        """延迟获取 logger"""
        if self._logger is None:
            try:
                from core.logging.log_manager import LogManager
                self._logger = LogManager.get_logger(self.name)
            except (ImportError, RuntimeError):
                # 如果 LogManager 未初始化，使用标准 logging
                self._logger = logging.getLogger(self.name)
        return self._logger

    def start_worker(self):
        """启动 Worker"""
        if not self._running:
            self._running = True
            self.start()
            self.logger.info(f"[WorkerBase] {self.name} started")

    def stop_worker(self):
        """停止 Worker"""
        self._running = False
        self.logger.warning(f"[WorkerBase] {self.name} stopping...")

    def run(self):
        """线程主循环"""
        try:
            while self._running:
                self.last_heartbeat = time.time()
                self.loop()
        except Exception as e:
            self.logger.exception(f"[WorkerBase] {self.name} crashed: {e}")
        finally:
            self.logger.warning(f"[WorkerBase] {self.name} exited")

    def loop(self):
        """
        子类必须实现，每次循环执行一次任务
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement loop()")

