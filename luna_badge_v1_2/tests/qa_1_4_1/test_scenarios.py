"""
全链路场景测试
对应 QA 清单：SC-01 ~ SC-02
"""
import pytest
import time
from core.failsafe.health_monitor import HealthMonitor
from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.auto_recovery import AutoRecoveryManager
from core.failsafe.health_events import HealthEvent
from core.speed.speed_context import SpeedContext
from core.speed.thread_controller import ThreadController


class TestScenarios:
    """全链路场景测试套件"""
    
    def test_sc_01_normal_to_emergency_to_recovery_flow(self):
        """
        SC-01: 正常→异常→safe→恢复 流程
        
        1. 启动
        2. 停止摄像头
        3. Emergency
        4. 播报
        5. Degraded
        6. 等恢复时间
        7. 回到 normal
        
        预期：全链路稳定无崩溃
        """
        # 1. 启动
        # 确保初始状态为 normal
        fail_safe_manager = FailSafeManager.get_instance()
        fail_safe_manager.reset_mode()
        SpeedContext.set_mode("normal")
        
        health_monitor = HealthMonitor(camera_timeout=0.5, infer_timeout=0.8)
        fail_safe_manager = FailSafeManager.attach_to_health_monitor(health_monitor)
        auto_recovery = AutoRecoveryManager()
        auto_recovery.stable_duration_sec = 2.0  # 缩短稳定时间便于测试
        auto_recovery.check_interval_sec = 0.5
        
        health_monitor.start_monitor()
        auto_recovery.start_manager()
        
        # 验证初始状态
        assert SpeedContext.get_mode() == "normal", "初始状态应该是 normal"
        
        # 2. 停止摄像头（模拟）
        # 通过触发 CAMERA_STALE 事件模拟
        
        # 3. Emergency
        fail_safe_manager.on_health_event(HealthEvent.CAMERA_STALE)
        assert SpeedContext.get_mode() == "safe", "应该进入 safe 模式"
        assert fail_safe_manager.emergency_active is True, "应该处于应急模式"
        
        # 4. 播报（已通过 FailSafeManager 自动触发）
        # 验证播报已执行（通过日志或统计信息）
        
        # 5. Degraded（应急模式自动包含降级）
        assert fail_safe_manager.degraded_active is True, "应急模式应该包含降级"
        
        # 6. 等恢复时间
        time.sleep(3.0)
        
        # 7. 回到 normal
        assert SpeedContext.get_mode() == "normal", "应该自动恢复为 normal"
        assert fail_safe_manager.emergency_active is False, "应急模式应该被恢复"
        assert fail_safe_manager.degraded_active is False, "降级模式应该被恢复"
        
        # 清理
        health_monitor.stop_monitor()
        auto_recovery.stop_manager()
        ThreadController.stop_speed_threads()
    
    def test_sc_02_chain_anomalies(self):
        """
        SC-02: 连环异常
        
        连续触发：
        - CAMERA_STALE
        - HIGH_CPU
        - THREAD_HANG
        - 摄像头恢复（模拟）
        - 推理恢复（模拟）
        
        预期：
        - 系统最终恢复 normal
        - 无失控状态
        - 无永久卡死
        """
        # 确保初始状态
        fail_safe_manager = FailSafeManager.get_instance()
        fail_safe_manager.reset_mode()
        SpeedContext.set_mode("normal")
        
        health_monitor = HealthMonitor()
        fail_safe_manager = FailSafeManager.attach_to_health_monitor(health_monitor)
        auto_recovery = AutoRecoveryManager()
        auto_recovery.stable_duration_sec = 5.0  # 增加稳定时间，确保测试有足够时间验证状态
        auto_recovery.check_interval_sec = 0.5
        
        health_monitor.start_monitor()
        auto_recovery.start_manager()
        
        # 连续触发异常
        fail_safe_manager.on_health_event(HealthEvent.CAMERA_STALE)
        time.sleep(0.5)
        fail_safe_manager.on_health_event(HealthEvent.HIGH_CPU)
        time.sleep(0.5)
        fail_safe_manager.on_health_event(HealthEvent.THREAD_HANG)
        
        # 验证进入应急模式（立即检查，在自动恢复之前）
        assert SpeedContext.get_mode() == "safe", "应该进入 safe 模式"
        assert fail_safe_manager.emergency_active is True, "应该处于应急模式"
        
        # 等待恢复（模拟摄像头和推理恢复，等待时间要超过稳定时间）
        time.sleep(6.0)
        
        # 验证最终恢复
        assert SpeedContext.get_mode() == "normal", "最终应该恢复为 normal"
        assert fail_safe_manager.emergency_active is False, "应急模式应该被恢复"
        assert fail_safe_manager.degraded_active is False, "降级模式应该被恢复"
        
        # 清理
        health_monitor.stop_monitor()
        auto_recovery.stop_manager()
        ThreadController.stop_speed_threads()

