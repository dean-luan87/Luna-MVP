"""
FailSafe 应急保障体系
1.4.1-failsafe: 系统健康监控和应急模式切换
"""
from core.failsafe.health_events import HealthEvent
from core.failsafe.health_monitor import HealthMonitor
from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.emergency_voice import EmergencyVoiceLayer
from core.failsafe.degraded_hooks import DegradedHooks
from core.failsafe.auto_recovery import AutoRecoveryManager

__all__ = [
    "HealthEvent",
    "HealthMonitor",
    "FailSafeManager",
    "EmergencyVoiceLayer",
    "DegradedHooks",
    "AutoRecoveryManager",
]

