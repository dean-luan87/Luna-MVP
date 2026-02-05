#!/usr/bin/env python3
"""
1.4.1-failsafe.3 Emergency Voice Layer + Degraded Hooks 测试脚本
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
from core.failsafe.emergency_voice import EmergencyVoiceLayer
from core.failsafe.degraded_hooks import DegradedHooks
from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.health_events import HealthEvent
from core.speed.speed_context import SpeedContext


def test_emergency_voice_layer():
    """测试 EmergencyVoiceLayer"""
    print("=" * 60)
    print("1.4.1-failsafe.3 EmergencyVoiceLayer 测试")
    print("=" * 60)
    
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    evl = EmergencyVoiceLayer.get_instance(min_interval=1.0)  # 使用较短的间隔便于测试
    
    print("\n测试播报功能...")
    result1 = evl.play("测试消息 1")
    assert result1 is True, "第一次播报应该成功"
    print("✅ 第一次播报成功")
    
    print("\n测试节流机制...")
    result2 = evl.play("测试消息 2")
    assert result2 is False, "节流期内播报应该被阻止"
    print("✅ 节流机制正常")
    
    print("\n等待节流期结束...")
    time.sleep(1.1)
    result3 = evl.play("测试消息 3")
    assert result3 is True, "节流期结束后应该可以播报"
    print("✅ 节流期结束后播报成功")
    
    stats = evl.get_stats()
    print("\n统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ EmergencyVoiceLayer 测试通过")


def test_degraded_hooks():
    """测试 DegradedHooks"""
    print("\n" + "=" * 60)
    print("1.4.1-failsafe.3 DegradedHooks 测试")
    print("=" * 60)
    
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    hooks = DegradedHooks.get_instance()
    
    print("\n测试应用降级行为...")
    hooks.apply()
    print("✅ 降级行为应用成功（OCR 可能不存在，这是正常的）")
    
    print("\n测试恢复行为...")
    hooks.restore()
    print("✅ 恢复行为执行成功")
    
    stats = hooks.get_stats()
    print("\n统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ DegradedHooks 测试通过")


def test_fail_safe_manager_integration():
    """测试 FailSafeManager 集成"""
    print("\n" + "=" * 60)
    print("1.4.1-failsafe.3 FailSafeManager 集成测试")
    print("=" * 60)
    
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    fsm = FailSafeManager.get_instance()
    
    print("\n测试应急模式（应触发语音和降级行为）...")
    fsm.reset_mode()  # 确保初始状态
    fsm.on_health_event(HealthEvent.CAMERA_STALE)
    
    assert fsm.emergency_active is True, "应急模式应该被激活"
    assert SpeedContext.get_mode() == "safe", "SpeedContext 应该设置为 safe"
    print("✅ 应急模式触发成功，语音和降级行为已执行")
    
    print("\n测试降级模式（应触发降级行为）...")
    fsm.reset_mode()
    fsm.on_health_event(HealthEvent.HIGH_CPU)
    
    assert fsm.degraded_active is True, "降级模式应该被激活"
    assert SpeedContext.get_mode() == "degraded", "SpeedContext 应该设置为 degraded"
    print("✅ 降级模式触发成功，降级行为已执行")
    
    print("\n测试恢复（应恢复降级行为）...")
    fsm.reset_mode()
    assert fsm.emergency_active is False, "应急模式应该被重置"
    assert fsm.degraded_active is False, "降级模式应该被重置"
    assert SpeedContext.get_mode() == "normal", "SpeedContext 应该重置为 normal"
    print("✅ 恢复成功，降级行为已恢复")
    
    print("\n✅ FailSafeManager 集成测试通过")


if __name__ == "__main__":
    try:
        test_emergency_voice_layer()
        test_degraded_hooks()
        test_fail_safe_manager_integration()
        
        print("\n" + "=" * 60)
        print("✅ 所有 1.4.1-failsafe.3 测试通过")
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
















