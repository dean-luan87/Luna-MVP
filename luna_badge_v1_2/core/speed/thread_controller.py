"""
Speed Engine 线程控制入口
1.4.1-speed.1: 线程基础框架
"""
import logging

from core.speed.speed_thread_pool import SpeedThreadPool

# 延迟初始化 logger，避免循环依赖
_logger = logging.getLogger("ThreadController")


class ThreadController:
    """
    Speed Engine 线程控制入口
    """
    
    @staticmethod
    def _get_logger():
        """延迟获取 logger"""
        try:
            from core.logging.log_manager import LogManager
            return LogManager.get_logger("ThreadController")
        except (ImportError, RuntimeError):
            return _logger
    
    @property
    @staticmethod
    def logger():
        """获取 logger（兼容属性访问）"""
        return ThreadController._get_logger()

    @staticmethod
    def start_speed_threads():
        """启动所有 Speed Engine 线程"""
        logger = ThreadController._get_logger()
        logger.info("[ThreadController] Starting all speed workers...")
        SpeedThreadPool.start_all()

    @staticmethod
    def stop_speed_threads():
        """停止所有 Speed Engine 线程"""
        logger = ThreadController._get_logger()
        logger.warning("[ThreadController] Stopping all speed workers...")
        SpeedThreadPool.stop_all()

    @staticmethod
    def get_worker_count() -> int:
        """获取当前 Worker 数量"""
        return SpeedThreadPool.get_worker_count()

