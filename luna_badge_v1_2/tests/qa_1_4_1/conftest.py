"""
pytest 配置和共享 fixtures
用于 1.4.1 QA 测试套件
"""
import pytest
import sys
import time
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager
from core.speed.thread_controller import ThreadController
from core.speed.speed_thread_pool import SpeedThreadPool
from core.speed.speed_context import SpeedContext


@pytest.fixture(scope="function", autouse=True)
def setup_test_environment():
    """每个测试函数执行前的设置"""
    # 初始化基础设施
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    # 清理 SpeedThreadPool
    SpeedThreadPool.clear()
    SpeedContext.set_mode("normal")
    
    yield
    
    # 测试后清理
    try:
        ThreadController.stop_speed_threads()
        SpeedThreadPool.clear()
        SpeedContext.set_mode("normal")
    except Exception:
        pass


@pytest.fixture
def mock_camera_worker():
    """创建模拟的 CameraStreamWorker"""
    from core.speed.camera_stream_worker import CameraStreamWorker
    from core.speed.speed_thread_pool import SpeedThreadPool
    from core.speed.speed_context import SpeedContext
    
    worker = CameraStreamWorker(cam_index=999, fps_limit=20)  # 使用无效摄像头索引
    SpeedThreadPool.register(worker)
    SpeedContext.set_camera_worker(worker)
    
    return worker


@pytest.fixture
def mock_infer_worker():
    """创建模拟的 VisionInferWorker"""
    from core.speed.vision_infer_worker import VisionInferWorker
    from core.speed.speed_thread_pool import SpeedThreadPool
    from core.speed.speed_context import SpeedContext
    
    # 创建模拟模型
    class MockModel:
        def detect(self, frame):
            return {"boxes": []}
    
    worker = VisionInferWorker(heavy_model=MockModel(), infer_interval=0.1)
    SpeedThreadPool.register(worker)
    SpeedContext.set_infer_worker(worker)
    
    return worker


@pytest.fixture
def health_monitor():
    """创建 HealthMonitor 实例"""
    from core.failsafe.health_monitor import HealthMonitor
    
    return HealthMonitor(
        camera_timeout=0.5,
        infer_timeout=0.8,
        cpu_threshold=80.0,
        mem_threshold=85.0,
    )


@pytest.fixture
def fail_safe_manager():
    """创建 FailSafeManager 实例"""
    from core.failsafe.fail_safe_manager import FailSafeManager
    
    # 重置单例
    FailSafeManager._instance = None
    return FailSafeManager.get_instance()


@pytest.fixture
def auto_recovery_manager():
    """创建 AutoRecoveryManager 实例"""
    from core.failsafe.auto_recovery import AutoRecoveryManager
    
    return AutoRecoveryManager()

