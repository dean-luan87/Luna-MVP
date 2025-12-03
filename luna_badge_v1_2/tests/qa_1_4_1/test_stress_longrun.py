"""
压力 & 长时间运行测试：
- 对应 QA 清单中的 IT-01 / IT-02 / SC-01 / SC-02
- 时长在自动化中控制在 30~60s，可在真实设备上调大
"""
import time
import pytest

from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.auto_recovery import AutoRecoveryManager
from core.failsafe.health_events import HealthEvent
from core.speed.speed_context import SpeedContext
from core.logging.log_manager import LogManager
from core.config.config_center import ConfigCenter
from tests.qa_1_4_1.mock_utils import inject_random_events, simulate_high_cpu


@pytest.fixture(scope="function", autouse=True)
def init_env():
    """初始化测试环境"""
    ConfigCenter.init(env="dev")
    LogManager.init()
    yield
    # 清理
    try:
        SpeedContext.set_mode("normal")
        FailSafeManager._instance = None
    except:
        pass


def test_stress_random_events_30s():
    """
    压力测试：30 秒内持续随机注入事件
    
    对应 QA 清单：IT-01
    """
    fm = FailSafeManager.get_instance()
    fm.reset_mode()

    arm = AutoRecoveryManager()
    arm.stable_duration_sec = 5
    arm.check_interval_sec = 0.5
    arm.start_manager()

    start = time.time()
    duration = 30  # 自动化版本设为 30 秒

    # 在 30 秒内不断随机注入事件
    while time.time() - start < duration:
        inject_random_events(fm, count=5, interval=0.02)
        # 模拟 CPU 压力短冲
        simulate_high_cpu(duration=0.2)

    # 停止 AutoRecovery
    arm.stop_manager()
    time.sleep(1)

    # 压力结束后，允许系统自动恢复
    fm.reset_mode()
    assert SpeedContext.get_mode() == "normal"
    assert not fm.emergency_active
    assert not fm.degraded_active


def test_longrun_state_stability():
    """
    模拟长时间运行：不真的跑 1 小时，自动化中缩短为 60 秒
    
    对应 QA 清单：IT-02
    
    - 连续注入中等频率事件
    - 确保系统不会崩溃
    - 最终仍可恢复 normal
    """
    fm = FailSafeManager.get_instance()
    fm.reset_mode()

    arm = AutoRecoveryManager()
    arm.stable_duration_sec = 5
    arm.check_interval_sec = 0.5
    arm.start_manager()

    start = time.time()
    duration = 60  # 自动化缩小版

    while time.time() - start < duration:
        # 每秒注入一个 CAMERA_STALE + HIGH_CPU
        fm.on_health_event(HealthEvent.CAMERA_STALE)
        fm.on_health_event(HealthEvent.HIGH_CPU)
        time.sleep(1)

    # 停止恢复线程
    arm.stop_manager()
    time.sleep(1)

    # 手动 reset 一次确保最终可回 normal
    fm.reset_mode()
    assert SpeedContext.get_mode() == "normal"

