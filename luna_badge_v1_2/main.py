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
from core.speed.vision_infer_worker import VisionInferWorker
from core.speed.speed_context import SpeedContext
from core.failsafe.health_monitor import HealthMonitor
from core.failsafe.fail_safe_manager import FailSafeManager


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

    # 5. 启动 Speed Engine 线程（1.4.1-speed.1 + speed.2 + speed.3）
    # 注册 CameraStreamWorker（1.4.1-speed.2）
    cam_index = ConfigCenter.get("system.camera.index", 0)
    fps_limit = ConfigCenter.get("system.camera.fps_limit", 20)
    camera_worker = CameraStreamWorker(cam_index=cam_index, fps_limit=fps_limit)
    SpeedThreadPool.register(camera_worker)
    SpeedContext.set_camera_worker(camera_worker)
    logger.info(f"CameraStreamWorker registered (cam_index={cam_index}, fps_limit={fps_limit})")
    
    # 注册 VisionInferWorker（1.4.1-speed.3 + speed.4）
    try:
        from core.yolo_detector import YoloDetector
        
        # 加载 heavy 模型
        heavy_model = YoloDetector()
        
        # 尝试加载 light 模型（可选）
        light_model = None
        try:
            # 如果有专门的 light 模型加载函数，可以在这里调用
            # 目前暂时使用 None，后续可以扩展
            # from core.vision.model_loader import load_yolo_light_model
            # light_model = load_yolo_light_model()
            pass
        except Exception as e:
            logger.debug(f"Light model not available: {e}")
        
        infer_interval = ConfigCenter.get("system.vision.infer_interval", 0.1)  # 默认 10 FPS
        infer_worker = VisionInferWorker(
            heavy_model=heavy_model,
            light_model=light_model,
            infer_interval=infer_interval
        )
        SpeedThreadPool.register(infer_worker)
        SpeedContext.set_infer_worker(infer_worker)  # 1.4.1-failsafe.3: 注册到 SpeedContext
        logger.info(f"VisionInferWorker registered (infer_interval={infer_interval}s, light_model={'available' if light_model else 'not available'})")
    except Exception as e:
        logger.warning(f"VisionInferWorker registration failed: {e}")
        logger.warning("系统将使用旧推理逻辑（fallback）")
    
    ThreadController.start_speed_threads()
    logger.info(f"Speed Engine: {ThreadController.get_worker_count()} workers started")
    
    # 6. 启动 FailSafe 健康监控和应急管理（1.4.1-failsafe.1 + failsafe.2）
    try:
        camera_timeout = ConfigCenter.get("failsafe.health_monitor.camera_timeout", 0.5)
        infer_timeout = ConfigCenter.get("failsafe.health_monitor.infer_timeout", 0.8)
        cpu_threshold = ConfigCenter.get("failsafe.health_monitor.cpu_threshold", 80.0)
        mem_threshold = ConfigCenter.get("failsafe.health_monitor.mem_threshold", 85.0)
        
        # 1. 创建 HealthMonitor
        health_monitor = HealthMonitor(
            camera_timeout=camera_timeout,
            infer_timeout=infer_timeout,
            cpu_threshold=cpu_threshold,
            mem_threshold=mem_threshold,
        )
        
        # 2. 挂接 FailSafeManager
        fail_safe_manager = FailSafeManager.attach_to_health_monitor(health_monitor)
        
        # 3. 启动监控
        health_monitor.start_monitor()
        logger.info(f"HealthMonitor started (camera_timeout={camera_timeout}s, infer_timeout={infer_timeout}s)")
        logger.info("FailSafeManager attached and ready")
    except Exception as e:
        logger.warning(f"FailSafe system initialization failed: {e}")
        logger.warning("系统将在无健康监控模式下运行")

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

