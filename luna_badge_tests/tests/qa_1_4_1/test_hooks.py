"""
测试 DegradedHooks 与 SpeedContext 是否正确联动。
"""
import time
import pytest

from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.health_events import HealthEvent
from core.speed.speed_context import SpeedContext
from core.failsafe.degraded_hooks import DegradedHooks
from core.logging.log_manager import LogManager
from core.config.config_center import ConfigCenter


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


def test_degraded_hooks_switch_model():
    """测试降级时模型切换"""
    fm = FailSafeManager.get_instance()
    fm.reset_mode()

    fm.on_health_event(HealthEvent.HIGH_CPU)

    assert SpeedContext.get_mode() == "degraded"
    # 模型切换逻辑通过日志验证（ModelSwitcher.force_to_lightweight）


def test_degraded_hooks_restore():
    """测试降级恢复"""
    fm = FailSafeManager.get_instance()
    fm.reset_mode()

    # 进入 degraded
    fm.on_health_event(HealthEvent.HIGH_CPU)
    assert SpeedContext.get_mode() == "degraded"

    # 恢复
    fm.reset_mode()
    assert SpeedContext.get_mode() == "normal"





