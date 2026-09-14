#!/usr/bin/env python3
"""
1.4.1-failsafe.2 FailSafeManager 测试脚本
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
from core.failsafe.health_monitor import HealthMonitor
from core.speed.speed_context import SpeedContext


def test_fail_safe_manager_basic():
    """测试 FailSafeManager 基本功能"""
    print("=" * 60)
    print("1.4.1-failsafe.2 FailSafeManager 基础测试")
    print("=" * 60)
    
    # 初始化基础设施
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    # 创建 HealthMonitor 和 FailSafeManager
    hm = HealthMonitor(camera_timeout=0.1, infer_timeout=0.1)
    fsm = FailSafeManager.attach_to_health_monitor(hm)
    
    print("\n测试应急模式触发...")
    # 手动触发严重事件
    fsm.on_health_event(HealthEvent.CAMERA_STALE)
    
    assert fsm.emergency_active is True, "应急模式应该被激活"
    assert fsm.degraded_active is True, "降级模式应该被激活（应急模式包含降级）"
    assert SpeedContext.get_mode() == "safe", "SpeedContext 应该设置为 safe 模式"
    print("✅ 应急模式触发成功")
    
    print("\n测试降级模式触发...")
    # 重置状态
    fsm.reset_mode()
    assert fsm.emergency_active is False, "应急模式应该被重置"
    assert SpeedContext.get_mode() == "normal", "SpeedContext 应该重置为 normal"
    
    # 触发资源压力事件
    fsm.on_health_event(HealthEvent.HIGH_CPU)
    assert fsm.degraded_active is True, "降级模式应该被激活"
    assert fsm.emergency_active is False, "应急模式不应该被激活"
    print("✅ 降级模式触发成功")
    
    print("\n测试模式重置...")
    fsm.reset_mode()
    assert fsm.emergency_active is False, "应急模式应该被重置"
    assert fsm.degraded_active is False, "降级模式应该被重置"
    assert SpeedContext.get_mode() == "normal", "SpeedContext 应该重置为 normal"
    print("✅ 模式重置成功")
    
    # 显示统计信息
    stats = fsm.get_stats()
    print("\n统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ FailSafeManager 基础测试通过")


def test_fail_safe_manager_all_events():
    """测试所有事件类型的处理"""
    print("\n" + "=" * 60)
    print("测试：所有事件类型处理")
    print("=" * 60)
    
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    hm = HealthMonitor()
    fsm = FailSafeManager.attach_to_health_monitor(hm)
    
    # 测试严重事件（应该触发应急模式）
    severe_events = [
        HealthEvent.CAMERA_DEAD,
        HealthEvent.CAMERA_STALE,
        HealthEvent.INFER_DEAD,
        HealthEvent.INFER_STALE,
        HealthEvent.THREAD_HANG,
    ]
    
    print("\n测试严重事件（应急模式）...")
    for event in severe_events:
        fsm.reset_mode()
        fsm.on_health_event(event)
        assert fsm.emergency_active is True, f"{event} 应该触发应急模式"
        print(f"  ✅ {event} → 应急模式")
    
    # 测试资源压力事件（应该触发降级模式）
    resource_events = [
        HealthEvent.HIGH_CPU,
        HealthEvent.HIGH_MEM,
    ]
    
    print("\n测试资源压力事件（降级模式）...")
    for event in resource_events:
        fsm.reset_mode()
        fsm.on_health_event(event)
        assert fsm.degraded_active is True, f"{event} 应该触发降级模式"
        assert fsm.emergency_active is False, f"{event} 不应该触发应急模式"
        print(f"  ✅ {event} → 降级模式")
    
    print("\n✅ 所有事件类型处理测试通过")


def test_fail_safe_manager_priority():
    """测试模式优先级"""
    print("\n" + "=" * 60)
    print("测试：模式优先级")
    print("=" * 60)
    
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    hm = HealthMonitor()
    fsm = FailSafeManager.attach_to_health_monitor(hm)
    
    # 先触发降级模式
    fsm.reset_mode()
    fsm.on_health_event(HealthEvent.HIGH_CPU)
    assert fsm.degraded_active is True
    assert fsm.emergency_active is False
    print("✅ 降级模式已激活")
    
    # 再触发应急模式（应该覆盖降级模式）
    fsm.on_health_event(HealthEvent.CAMERA_STALE)
    assert fsm.emergency_active is True
    assert fsm.degraded_active is True  # 应急模式包含降级
    assert SpeedContext.get_mode() == "safe"
    print("✅ 应急模式覆盖降级模式")
    
    # 在应急模式下，资源压力事件不应该改变状态
    initial_mode = SpeedContext.get_mode()
    fsm.on_health_event(HealthEvent.HIGH_MEM)
    assert fsm.emergency_active is True, "应急模式应该保持"
    assert SpeedContext.get_mode() == initial_mode, "模式不应该改变"
    print("✅ 应急模式下资源压力事件不影响状态")
    
    print("\n✅ 模式优先级测试通过")


if __name__ == "__main__":
    try:
        test_fail_safe_manager_basic()
        test_fail_safe_manager_all_events()
        test_fail_safe_manager_priority()
        
        print("\n" + "=" * 60)
        print("✅ 所有 FailSafeManager 测试通过")
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





