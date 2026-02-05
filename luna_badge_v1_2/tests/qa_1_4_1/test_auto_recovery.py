"""
AutoRecoveryManager QA 测试用例
对应 QA 清单：AR-01 ~ AR-03
"""
import pytest
import time
from core.failsafe.auto_recovery import AutoRecoveryManager
from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.health_events import HealthEvent
from core.speed.speed_context import SpeedContext


class TestAutoRecovery:
    """AutoRecoveryManager 测试套件"""
    
    def test_ar_01_normal_recovery(self, fail_safe_manager, auto_recovery_manager):
        """
        AR-01: 正常恢复
        
        操作：
        1. 发 CAMERA_STALE
        2. 进入 emergency
        3. 等待 stable_duration（默认 15 秒）
        
        预期：
        - 模式自动恢复 normal
        - emergency_active → False
        - degraded_active → False
        """
        fsm = fail_safe_manager
        arm = auto_recovery_manager
        
        # 缩短稳定时间便于测试
        arm.stable_duration_sec = 2.0
        arm.check_interval_sec = 0.5
        
        # 触发应急模式
        fsm.on_health_event(HealthEvent.CAMERA_STALE)
        assert fsm.emergency_active is True
        
        # 启动自动恢复
        arm.start_manager()
        
        # 等待恢复
        time.sleep(3.0)
        
        # 验证恢复
        assert fsm.emergency_active is False, "应急模式应该被自动恢复"
        assert fsm.degraded_active is False, "降级模式应该被自动恢复"
        assert SpeedContext.get_mode() == "normal", "SpeedContext 应该恢复为 normal"
        
        arm.stop_manager()
    
    def test_ar_02_recovery_reset(self, fail_safe_manager, auto_recovery_manager):
        """
        AR-02: 恢复被重置
        
        操作：
        1. 发 CAMERA_STALE
        2. 等待 10 秒
        3. 再发一次 CAMERA_STALE
        4. 再等 10 秒
        
        预期：
        - 不恢复（窗口被刷新）
        """
        fsm = fail_safe_manager
        arm = auto_recovery_manager
        
        # 缩短稳定时间便于测试
        arm.stable_duration_sec = 3.0
        arm.check_interval_sec = 0.5
        
        # 第一次触发
        fsm.on_health_event(HealthEvent.CAMERA_STALE)
        assert fsm.emergency_active is True
        
        arm.start_manager()
        
        # 等待 1.5 秒（未达到稳定时间）
        time.sleep(1.5)
        
        # 再次触发（重置计时）
        fsm.on_health_event(HealthEvent.CAMERA_STALE)
        
        # 再等待 1.5 秒（从新事件开始计时，应该未达到稳定时间）
        time.sleep(1.5)
        
        # 验证仍在应急模式（因为计时被重置）
        assert fsm.emergency_active is True, "新事件后应该仍在应急模式"
        
        # 继续等待达到稳定时间
        time.sleep(2.0)
        
        # 现在应该恢复了
        assert fsm.emergency_active is False, "稳定时间达标后应该恢复"
        
        arm.stop_manager()
    
    def test_ar_03_disabled_recovery(self, fail_safe_manager, auto_recovery_manager):
        """
        AR-03: 禁用自恢复（配置开关）
        
        failsafe.recovery.enabled = false
        操作：发事件
        预期：
        - 不自动恢复
        - 只是日志提示"AutoRecovery disabled"
        """
        fsm = fail_safe_manager
        arm = auto_recovery_manager
        
        # 禁用自动恢复
        arm.enabled = False
        
        # 触发应急模式
        fsm.on_health_event(HealthEvent.CAMERA_STALE)
        assert fsm.emergency_active is True
        
        # 启动自动恢复（应该不启动，因为已禁用）
        arm.start_manager()
        
        # 等待一段时间
        time.sleep(2.0)
        
        # 验证未恢复（因为自动恢复被禁用）
        assert fsm.emergency_active is True, "自动恢复已禁用，不应恢复"
        
        arm.stop_manager()
















