"""
Luna Badge v1.4.1 — 自动化 QA 主入口
运行方式：pytest tests/qa_1_4_1/test_entry.py -s
"""
import time
import pytest

from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.health_events import HealthEvent
from core.failsafe.auto_recovery import AutoRecoveryManager
from core.speed.speed_context import SpeedContext
from core.logging.log_manager import LogManager
from core.config.config_center import ConfigCenter

from tests.qa_1_4_1.mock_utils import (
    freeze_camera_stream, unfreeze_camera_stream,
    freeze_infer_stream, unfreeze_infer_stream,
    simulate_high_cpu, simulate_high_mem,
)


@pytest.fixture(scope="module", autouse=True)
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


def test_camera_stale_emergency():
    """
    触发 CAMERA_STALE → 必须进入 emergency 模式
    """
    fm = FailSafeManager.get_instance()
    fm.reset_mode()

    fm.on_health_event(HealthEvent.CAMERA_STALE)
    time.sleep(0.2)

    assert fm.emergency_active, "Should enter emergency mode"
    assert SpeedContext.get_mode() == "safe", "SpeedContext should be safe mode"


def test_high_cpu_degraded():
    """
    触发 HIGH_CPU → degraded 模式
    """
    fm = FailSafeManager.get_instance()
    fm.reset_mode()

    fm.on_health_event(HealthEvent.HIGH_CPU)
    time.sleep(0.1)

    assert fm.degraded_active, "Should enter degraded mode"
    assert SpeedContext.get_mode() == "degraded"


def test_emergency_voice_throttle():
    """
    短时间多次 emergency 播报，触发节流
    """
    fm = FailSafeManager.get_instance()
    fm.reset_mode()

    fm.on_health_event(HealthEvent.CAMERA_STALE)
    time.sleep(0.1)
    first_ts = fm.get_last_event_time()

    # 再次短时间触发
    fm.on_health_event(HealthEvent.CAMERA_STALE)
    time.sleep(0.1)
    second_ts = fm.get_last_event_time()

    assert second_ts >= first_ts, "Event timestamp should update"
    # 实际播报节流在日志中验证，由 Logger 输出节流提示


def test_auto_recovery():
    """
    emergency → 等待稳定窗口 → 自动恢复
    """
    fm = FailSafeManager.get_instance()
    fm.reset_mode()

    fm.on_health_event(HealthEvent.CAMERA_STALE)
    assert fm.emergency_active

    # 启动 AutoRecovery，但把稳定窗口缩小
    arm = AutoRecoveryManager()
    arm.stable_duration_sec = 2
    arm.check_interval_sec = 0.5
    arm.start_manager()

    # 模拟无新错误发生
    time.sleep(3)

    assert not fm.emergency_active, "Should auto recover to normal"
    assert SpeedContext.get_mode() == "normal"

    arm.stop_manager()


def test_recovery_resets_when_new_error():
    """
    窗口未满期间发生新错误 → 自动恢复时间重置
    """
    fm = FailSafeManager.get_instance()
    fm.reset_mode()

    # 第一次触发 emergency
    fm.on_health_event(HealthEvent.CAMERA_STALE)
    assert fm.emergency_active

    arm = AutoRecoveryManager()
    arm.stable_duration_sec = 4
    arm.check_interval_sec = 0.5
    arm.start_manager()

    time.sleep(2)

    # 在窗口内再次触发严重错误 → 重置窗口
    fm.on_health_event(HealthEvent.CAMERA_STALE)

    # 再等 3 秒不够恢复（窗口重置后需等满 4 秒）
    time.sleep(3)

    assert fm.emergency_active, "Should NOT recover yet"

    arm.stop_manager()





