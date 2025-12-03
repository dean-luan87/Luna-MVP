"""
内存泄漏监控测试：
- 自动化环境中做 60 秒压力循环，监控 RSS 变化
- 对应 QA 清单中的 IT-02 / Memory 部分
"""
import time
import pytest
import psutil
import os

from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.health_events import HealthEvent
from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager


@pytest.fixture(scope="function", autouse=True)
def init_env():
    """初始化测试环境"""
    ConfigCenter.init(env="dev")
    LogManager.init()
    yield
    # 清理
    try:
        FailSafeManager._instance = None
    except:
        pass


def test_memory_leak_trend():
    """
    内存泄漏趋势测试
    
    对应 QA 清单：IT-02（内存部分）
    
    要求：在 60 秒压力下，内存增长不超过 20%
    """
    fm = FailSafeManager.get_instance()
    fm.reset_mode()

    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss

    duration = 60  # 自动化测试设为 60 秒
    start = time.time()

    while time.time() - start < duration:
        # 周期性触发 emergency / degraded
        fm.on_health_event(HealthEvent.CAMERA_STALE)
        fm.on_health_event(HealthEvent.HIGH_CPU)
        time.sleep(0.2)

    mem_after = process.memory_info().rss
    growth_ratio = (mem_after - mem_before) / max(mem_before, 1)

    # 要求：在 60 秒压力下，内存增长不超过 20%
    assert growth_ratio < 0.2, f"Memory growth too high: {growth_ratio:.2%}"

