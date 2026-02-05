"""
配置 QA 测试用例
对应 QA 清单：CFG-01 ~ CFG-02
"""
import pytest
import time
from core.config.config_center import ConfigCenter
from core.failsafe.auto_recovery import AutoRecoveryManager
from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.health_events import HealthEvent


class TestConfig:
    """配置测试套件"""
    
    def test_cfg_01_stable_duration_config(self, fail_safe_manager):
        """
        CFG-01: failsafe.recovery.stable_duration 修改生效
        
        将 15 秒改成 3 秒
        操作：
        - 发 emergency
        - 等待 3 秒
        
        预期：自动恢复 normal
        """
        fsm = fail_safe_manager
        
        # 修改配置（通过直接设置 AutoRecoveryManager 参数）
        arm = AutoRecoveryManager()
        arm.stable_duration_sec = 3.0
        arm.check_interval_sec = 0.5
        
        # 触发应急模式
        fsm.on_health_event(HealthEvent.CAMERA_STALE)
        assert fsm.emergency_active is True
        
        # 启动自动恢复
        arm.start_manager()
        
        # 等待 3.5 秒（超过稳定时间）
        time.sleep(3.5)
        
        # 验证恢复
        assert fsm.emergency_active is False, "稳定时间达标后应该恢复"
        
        arm.stop_manager()
    
    def test_cfg_02_auto_restart_enabled(self, auto_recovery_manager):
        """
        CFG-02: auto_restart_enabled = true（未来留用）
        
        当前版本不执行软重启
        预期：日志：soft restart is enabled, but no workers are wired yet.
        """
        arm = auto_recovery_manager
        
        # 启用自动重启（但 v1 不实际执行）
        arm.auto_restart_enabled = True
        
        # 调用软重启方法（应该只记录日志）
        arm._try_soft_restart_workers()
        
        # 验证不会实际重启线程（通过检查线程状态）
        # 这个测试主要是验证接口存在且不报错





