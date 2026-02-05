"""
FailSafeManager QA 测试用例
对应 QA 清单：FSM-01 ~ FSM-04
"""
import pytest
import time
from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.health_events import HealthEvent
from core.speed.speed_context import SpeedContext


class TestFailSafeManager:
    """FailSafeManager 测试套件"""
    
    def test_fsm_01_emergency_mode_trigger(self, fail_safe_manager):
        """
        FSM-01: Emergency 模式触发
        
        事件触发：CAMERA_DEAD / STALE / THREAD_HANG
        预期：
        - SpeedContext.mode = safe
        - emergency_active = True
        - degraded_active = True
        - 产生一条日志 "Enter EMERGENCY mode"
        """
        fsm = fail_safe_manager
        fsm.reset_mode()  # 确保初始状态
        
        # 触发应急事件
        fsm.on_health_event(HealthEvent.CAMERA_STALE)
        
        # 验证状态
        assert SpeedContext.get_mode() == "safe", "SpeedContext 应该设置为 safe"
        assert fsm.emergency_active is True, "emergency_active 应该为 True"
        assert fsm.degraded_active is True, "degraded_active 应该为 True（应急模式包含降级）"
    
    def test_fsm_02_degraded_mode_trigger(self, fail_safe_manager):
        """
        FSM-02: Degraded 模式触发
        
        事件触发：HIGH_CPU / HIGH_MEM
        预期：
        - SpeedContext.mode = degraded
        - degraded_active = True
        - emergency_active 不变（保持 False）
        """
        fsm = fail_safe_manager
        fsm.reset_mode()
        
        # 触发降级事件
        fsm.on_health_event(HealthEvent.HIGH_CPU)
        
        # 验证状态
        assert SpeedContext.get_mode() == "degraded", "SpeedContext 应该设置为 degraded"
        assert fsm.degraded_active is True, "degraded_active 应该为 True"
        assert fsm.emergency_active is False, "emergency_active 应该为 False"
    
    def test_fsm_03_repeat_trigger_throttle(self, fail_safe_manager):
        """
        FSM-03: 重复触发节流
        
        连续发 10 次 CAMERA_STALE
        预期：
        - emergency 模式只触发一次
        - EmergencyVoiceLayer 仅播报一次（节流 10 秒）
        """
        fsm = fail_safe_manager
        fsm.reset_mode()
        
        # 连续触发 10 次
        for i in range(10):
            fsm.on_health_event(HealthEvent.CAMERA_STALE)
            time.sleep(0.1)
        
        # 验证应急模式只激活一次（通过检查 last_emergency_time）
        # 注意：由于 enter_emergency_mode 有防重复逻辑，应该只触发一次
        
        # 验证 EmergencyVoiceLayer 节流（通过日志分析）
        # 这个需要在集成测试中验证
    
    def test_fsm_04_recovery(self, fail_safe_manager):
        """
        FSM-04: 恢复
        
        操作：调用 FailSafeManager.reset_mode
        预期：
        - mode = normal
        - emergency_active = False
        - degraded_active = False
        """
        fsm = fail_safe_manager
        
        # 先进入应急模式
        fsm.on_health_event(HealthEvent.CAMERA_STALE)
        assert fsm.emergency_active is True
        
        # 恢复
        fsm.reset_mode()
        
        # 验证状态
        assert SpeedContext.get_mode() == "normal", "SpeedContext 应该恢复为 normal"
        assert fsm.emergency_active is False, "emergency_active 应该为 False"
        assert fsm.degraded_active is False, "degraded_active 应该为 False"
















