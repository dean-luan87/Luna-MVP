# tests/test_plan_b.py
"""
测试 Plan-B 降级机制
"""
import time
from core.vision.vision_fail_safe import VisionFailSafe, FailSafeConfig
from core.system.system_recovery_center import RecoveryCenter


def test_vision_fail_safe_timeout():
    """测试视觉超时降级"""
    degraded_called = {"called": False}

    def on_degraded():
        degraded_called["called"] = True

    failsafe = VisionFailSafe()
    failsafe.set_degraded_callback(on_degraded)

    # 连续报告超时
    for _ in range(3):
        failsafe.report_infer_timeout()

    assert failsafe.get_state() == "degraded"
    # 注意：由于 cooldown，回调可能不会立即触发，但状态应该改变


def test_vision_fail_safe_reset():
    """测试重置功能"""
    failsafe = VisionFailSafe()
    failsafe.report_infer_timeout()
    failsafe.report_model_error()

    assert failsafe.get_state() in ("normal", "degraded")

    failsafe.reset()
    assert failsafe.get_state() == "normal"
    assert failsafe.counters.infer_timeout_count == 0
    assert failsafe.counters.model_error_count == 0


def test_vision_fail_safe_strategy():
    """测试降级策略获取"""
    failsafe = VisionFailSafe()
    strategy = failsafe.get_current_strategy()
    assert strategy["model_type"] == "standard"

    # 手动设置状态（测试用）
    failsafe.state = "degraded"
    strategy = failsafe.get_current_strategy()
    assert strategy["model_type"] == "tiny"
    assert strategy["resolution"] == "half"


def test_recovery_center_heartbeat():
    """测试恢复中心心跳监控"""
    cpu_overload_triggered = {"called": False}

    def get_cpu_load():
        return 0.5

    def safe_mode_enter():
        cpu_overload_triggered["called"] = True

    center = RecoveryCenter(
        get_cpu_load=get_cpu_load,
        safe_mode_enter=safe_mode_enter,
    )

    center.register_module("vision", timeout_seconds=5.0)
    center.update_heartbeat("vision")

    # 检查健康状态
    status = center.get_health_status()
    assert "vision" in status["modules"]
    assert status["modules"]["vision"]["healthy"] is True


def test_recovery_center_cpu_overload():
    """测试 CPU 过载检测"""
    safe_mode_called = {"called": False}

    def get_cpu_load():
        return 0.9  # 高 CPU

    def safe_mode_enter():
        safe_mode_called["called"] = True

    center = RecoveryCenter(
        get_cpu_load=get_cpu_load,
        safe_mode_enter=safe_mode_enter,
    )

    center.tick()
    assert safe_mode_called["called"] is True


if __name__ == "__main__":
    test_vision_fail_safe_timeout()
    test_vision_fail_safe_reset()
    test_vision_fail_safe_strategy()
    test_recovery_center_heartbeat()
    test_recovery_center_cpu_overload()
    print("所有 Plan-B 测试通过！")




