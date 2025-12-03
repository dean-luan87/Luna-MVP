"""
Speed Engine 线程控制入口
1.4.1-speed.1: 线程基础框架
"""
from core.speed.speed_thread_pool import SpeedThreadPool
from core.logging.log_manager import LogManager


class ThreadController:
    """
    Speed Engine 线程控制入口
    """
    
    logger = LogManager.get_logger("ThreadController")

    @staticmethod
    def start_speed_threads():
        """启动所有 Speed Engine 线程"""
        ThreadController.logger.info("[ThreadController] Starting all speed workers...")
        SpeedThreadPool.start_all()

    @staticmethod
    def stop_speed_threads():
        """停止所有 Speed Engine 线程"""
        ThreadController.logger.warning("[ThreadController] Stopping all speed workers...")
        SpeedThreadPool.stop_all()

    @staticmethod
    def get_worker_count() -> int:
        """获取当前 Worker 数量"""
        return SpeedThreadPool.get_worker_count()

