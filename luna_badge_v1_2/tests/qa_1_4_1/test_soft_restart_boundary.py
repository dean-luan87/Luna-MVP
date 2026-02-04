"""
Soft Restart 边界测试：

当前 1.4.1 要求：
- AutoRecoveryManager 默认 auto_restart_enabled = False
- 即使配置开启，现阶段 _try_soft_restart_workers 只打日志不重启

对应用例：
- 确认不会"乱重启线程"
"""
import pytest

from core.failsafe.auto_recovery import AutoRecoveryManager
from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager


@pytest.fixture(scope="function", autouse=True)
def init_env():
    """初始化测试环境"""
    ConfigCenter.init(env="dev")
    LogManager.init()
    yield


def test_auto_restart_flag_default_false():
    """
    验证 auto_restart_enabled 默认值为 False
    
    对应 QA 清单：CFG-02（行为边界）
    """
    arm = AutoRecoveryManager()
    assert arm.auto_restart_enabled is False, "auto_restart_enabled must be false by default"


def test_soft_restart_no_effect_for_now():
    """
    即使手动开启 auto_restart_enabled，
    _try_soft_restart_workers 也不应真正重启任何 Worker（当前版本行为 = 打日志）。
    
    这里只验证调用过程不抛异常。
    
    对应 QA 清单：CFG-02（行为边界）
    """
    arm = AutoRecoveryManager()
    arm.auto_restart_enabled = True
    
    # 不应抛异常
    try:
        arm._try_soft_restart_workers()
        # 如果执行到这里，说明没有抛出异常
        assert True, "Soft restart should not throw exception"
    except Exception as e:
        pytest.fail(f"Soft restart should not throw exception: {e}")
















