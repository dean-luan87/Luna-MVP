"""
Speed Engine 线程池管理器
1.4.1-speed.1: 线程基础框架
"""
from typing import List
import logging

from core.speed.worker_base import WorkerBase

# 延迟初始化 logger，避免循环依赖
logger = logging.getLogger("SpeedThreadPool")


class SpeedThreadPool:
    """
    SpeedEngine 使用的线程池管理器。
    1.4.1-speed.1 仅支持注册/启动/停止，不做并行调度。
    """
    
    workers: List[WorkerBase] = []

    @classmethod
    def register(cls, worker: WorkerBase):
        """
        注册 Worker
        
        Args:
            worker: WorkerBase 实例
        """
        cls.workers.append(worker)
        logger.debug(f"Registered worker: {worker.name}")

    @classmethod
    def start_all(cls):
        """启动所有注册的 Worker"""
        logger.info(f"Starting {len(cls.workers)} workers...")
        for w in cls.workers:
            w.start_worker()

    @classmethod
    def stop_all(cls):
        """停止所有注册的 Worker"""
        logger.info(f"Stopping {len(cls.workers)} workers...")
        for w in cls.workers:
            w.stop_worker()
        # 等待所有线程结束
        for w in cls.workers:
            if w.is_alive():
                w.join(timeout=2.0)

    @classmethod
    def get_worker_count(cls) -> int:
        """获取注册的 Worker 数量"""
        return len(cls.workers)

    @classmethod
    def clear(cls):
        """清空所有 Worker（用于测试）"""
        cls.workers.clear()

