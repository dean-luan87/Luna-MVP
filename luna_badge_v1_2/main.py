#!/usr/bin/env python3
"""
Luna Badge 主入口
按照《Luna Badge 项目结构与开发规范 v1.0》实现
只负责启动系统，不包含业务逻辑
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager
from core.concurrency.thread_pool import ThreadPool
from core.speed.thread_controller import ThreadController
from core.speed.speed_thread_pool import SpeedThreadPool
from core.speed.camera_stream_worker import CameraStreamWorker
from core.speed.speed_context import SpeedContext
from core.speed.speed_thread_pool import SpeedThreadPool
from core.speed.camera_stream_worker import CameraStreamWorker
from core.speed.speed_context import SpeedContext


def bootstrap():
    """
    系统启动函数
    按照规范：只做三件事
    1. 启动设备（camera / sensors）
    2. 启动视觉 pipeline
    3. 启动任务链系统
    """
    # 1. 初始化基础设施
    env = os.getenv("LUNA_ENV", "dev")
    ConfigCenter.init(env=env)
    LogManager.init()
    ThreadPool.init()

    logger = LogManager.get_logger(__name__)
    logger.info("=" * 60)
    logger.info("Luna Badge 1.4.1-core 启动")
    logger.info("=" * 60)
    logger.info(f"环境: {env}")
    logger.info(f"配置中心: 已初始化")
    logger.info(f"日志系统: 已初始化")
    logger.info(f"线程池: 已初始化")

    # 2. 启动设备（TODO: 后续实现）
    # camera = CameraManager()
    # sensors = SensorManager()
    # camera.start()
    # sensors.start()
    logger.info("设备管理: 待实现")

    # 3. 启动视觉 pipeline（TODO: 后续实现）
    # vision = VisionPipeline()
    # vision.start()
    logger.info("视觉 pipeline: 待实现")

    # 4. 启动任务链系统（TODO: 后续实现）
    # task_manager = TaskManager()
    # task_manager.start()
    logger.info("任务链系统: 待实现")

    # 5. 启动 Speed Engine 线程（1.4.1-speed.1 + speed.2）
    # 注册 CameraStreamWorker（1.4.1-speed.2）
    cam_index = ConfigCenter.get("system.camera.index", 0)
    fps_limit = ConfigCenter.get("system.camera.fps_limit", 20)
    camera_worker = CameraStreamWorker(cam_index=cam_index, fps_limit=fps_limit)
    SpeedThreadPool.register(camera_worker)
    SpeedContext.set_camera_worker(camera_worker)
    logger.info(f"CameraStreamWorker registered (cam_index={cam_index}, fps_limit={fps_limit})")
    
    ThreadController.start_speed_threads()
    logger.info(f"Speed Engine: {ThreadController.get_worker_count()} workers started")

    logger.info("=" * 60)
    logger.info("Luna Badge 1.4.1-core bootstrap 完成")
    logger.info("=" * 60)

    # 兼容模式：如果存在 realtime_server.py，可以继续使用
    # 这是为了保持向后兼容，后续版本会逐步迁移
    try:
        import realtime_server
        logger.info("检测到 realtime_server，可以在兼容模式下运行")
    except ImportError:
        logger.info("未检测到 realtime_server，使用新架构")


if __name__ == "__main__":
    try:
        bootstrap()
        # 主循环（TODO: 后续实现）
        import time
        logger = LogManager.get_logger(__name__)
        logger.info("系统运行中，按 Ctrl+C 退出...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger = LogManager.get_logger(__name__)
        logger.info("收到停止信号，正在关闭...")
        ThreadController.stop_speed_threads()
        ThreadPool.shutdown(wait=True)
        logger.info("系统已关闭")

