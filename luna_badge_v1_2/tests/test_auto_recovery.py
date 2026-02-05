#!/usr/bin/env python3
"""
1.4.1-failsafe.4 AutoRecoveryManager 测试脚本
按照任务说明创建的基础测试
"""
import sys
import time
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager
from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.health_events import HealthEvent
from core.failsafe.auto_recovery import AutoRecoveryManager
from core.speed.speed_context import SpeedContext


def test_auto_recovery_basic():
    """测试 AutoRecoveryManager 基本功能"""
    print("=" * 60)
    print("1.4.1-failsafe.4 AutoRecoveryManager 基础测试")
    print("=" * 60)
    
    # 初始化基础设施
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    fsm = FailSafeManager.get_instance()
    
    # 手动模拟进入 emergency 模式
    print("\n模拟进入应急模式...")
    fsm.on_health_event(HealthEvent.CAMERA_STALE)
    assert fsm.emergency_active is True, "应急模式应该被激活"
    assert SpeedContext.get_mode() == "safe", "SpeedContext 应该设置为 safe"
    print("✅ 应急模式已激活")
    
    # 启动 AutoRecoveryManager，缩短稳定时间以便测试
    print("\n启动 AutoRecoveryManager（稳定时间：1 秒）...")
    arm = AutoRecoveryManager()
    arm.stable_duration_sec = 1.0  # 缩短稳定时间便于测试
    arm.check_interval_sec = 0.5  # 缩短检查间隔
    arm.start_manager()
    
    # 等待恢复
    print("\n等待自动恢复（2 秒）...")
    time.sleep(2.0)
    
    # 验证恢复
    assert fsm.emergency_active is False, "应急模式应该被自动恢复"
    assert fsm.degraded_active is False, "降级模式应该被自动恢复"
    assert SpeedContext.get_mode() == "normal", "SpeedContext 应该恢复为 normal"
    print("✅ 自动恢复成功")
    
    # 停止 AutoRecoveryManager
    arm.stop_manager()
    time.sleep(0.5)
    
    # 显示统计信息
    stats = arm.get_stats()
    print("\n统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ AutoRecoveryManager 基础测试通过")


def test_auto_recovery_stable_duration():
    """测试稳定时间要求"""
    print("\n" + "=" * 60)
    print("测试：稳定时间要求")
    print("=" * 60)
    
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    fsm = FailSafeManager.get_instance()
    
    # 进入应急模式
    fsm.on_health_event(HealthEvent.CAMERA_STALE)
    assert fsm.emergency_active is True
    
    # 启动 AutoRecoveryManager（稳定时间：3 秒）
    arm = AutoRecoveryManager()
    arm.stable_duration_sec = 3.0
    arm.check_interval_sec = 0.5
    arm.start_manager()
    
    # 等待 1 秒（未达到稳定时间）
    print("\n等待 1 秒（未达到稳定时间）...")
    time.sleep(1.0)
    assert fsm.emergency_active is True, "稳定时间未达标，不应恢复"
    print("✅ 稳定时间未达标，未恢复")
    
    # 等待更长时间（达到稳定时间）
    print("\n继续等待 2.5 秒（达到稳定时间）...")
    time.sleep(2.5)
    assert fsm.emergency_active is False, "稳定时间达标，应该恢复"
    print("✅ 稳定时间达标，已恢复")
    
    arm.stop_manager()
    time.sleep(0.5)
    
    print("\n✅ 稳定时间要求测试通过")


def test_auto_recovery_event_reset():
    """测试新事件重置稳定计时"""
    print("\n" + "=" * 60)
    print("测试：新事件重置稳定计时")
    print("=" * 60)
    
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    fsm = FailSafeManager.get_instance()
    
    # 进入应急模式
    fsm.on_health_event(HealthEvent.CAMERA_STALE)
    assert fsm.emergency_active is True
    
    # 启动 AutoRecoveryManager（稳定时间：2 秒）
    arm = AutoRecoveryManager()
    arm.stable_duration_sec = 2.0
    arm.check_interval_sec = 0.5
    arm.start_manager()
    
    # 等待 1.5 秒
    print("\n等待 1.5 秒...")
    time.sleep(1.5)
    
    # 触发新事件（应该重置计时）
    print("\n触发新事件（重置计时）...")
    fsm.on_health_event(HealthEvent.INFER_STALE)
    assert fsm.emergency_active is True, "新事件后应仍在应急模式"
    
    # 再等待 2.5 秒（应该恢复）
    print("\n继续等待 2.5 秒（达到新的稳定时间）...")
    time.sleep(2.5)
    assert fsm.emergency_active is False, "稳定时间达标，应该恢复"
    print("✅ 新事件重置计时，稳定后恢复")
    
    arm.stop_manager()
    time.sleep(0.5)
    
    print("\n✅ 事件重置计时测试通过")


def test_auto_recovery_disabled():
    """测试禁用自动恢复"""
    print("\n" + "=" * 60)
    print("测试：禁用自动恢复")
    print("=" * 60)
    
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    fsm = FailSafeManager.get_instance()
    
    # 进入应急模式
    fsm.on_health_event(HealthEvent.CAMERA_STALE)
    assert fsm.emergency_active is True
    
    # 创建禁用的 AutoRecoveryManager
    arm = AutoRecoveryManager()
    arm.enabled = False
    arm.start_manager()
    
    # 等待一段时间
    print("\n等待 3 秒（自动恢复已禁用）...")
    time.sleep(3.0)
    
    # 应该仍在应急模式（因为自动恢复被禁用）
    assert fsm.emergency_active is True, "自动恢复已禁用，不应恢复"
    print("✅ 自动恢复已禁用，未恢复")
    
    arm.stop_manager()
    time.sleep(0.5)
    
    print("\n✅ 禁用自动恢复测试通过")


def test_fail_safe_manager_query_methods():
    """测试 FailSafeManager 的查询方法"""
    print("\n" + "=" * 60)
    print("测试：FailSafeManager 查询方法")
    print("=" * 60)
    
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    fsm = FailSafeManager.get_instance()
    fsm.reset_mode()  # 确保初始状态
    
    # 测试 has_active_protection
    assert fsm.has_active_protection() is False, "初始状态应该没有保护"
    print("✅ has_active_protection() 正常")
    
    # 触发事件
    fsm.on_health_event(HealthEvent.CAMERA_STALE)
    assert fsm.has_active_protection() is True, "应急模式应该有保护"
    print("✅ 应急模式下 has_active_protection() 返回 True")
    
    # 测试 get_last_event_time
    last_ts = fsm.get_last_event_time()
    assert last_ts > 0, "应该有事件时间戳"
    print(f"✅ get_last_event_time() 返回: {last_ts:.2f}")
    
    # 测试指定类型查询
    critical_types = [HealthEvent.CAMERA_STALE, HealthEvent.INFER_STALE]
    last_critical_ts = fsm.get_last_event_time(critical_types)
    assert last_critical_ts > 0, "应该找到严重事件时间戳"
    print(f"✅ get_last_event_time(critical_types) 返回: {last_critical_ts:.2f}")
    
    fsm.reset_mode()
    
    print("\n✅ FailSafeManager 查询方法测试通过")


if __name__ == "__main__":
    try:
        test_auto_recovery_basic()
        test_auto_recovery_stable_duration()
        test_auto_recovery_event_reset()
        test_auto_recovery_disabled()
        test_fail_safe_manager_query_methods()
        
        print("\n" + "=" * 60)
        print("✅ 所有 1.4.1-failsafe.4 测试通过")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # 清理
        SpeedContext.set_mode("normal")
















