"""
FailSafe 应急保障体系
1.4.1-failsafe: 系统健康监控和应急模式切换
"""
from core.failsafe.health_events import HealthEvent
from core.failsafe.health_monitor import HealthMonitor

__all__ = [
    "HealthEvent",
    "HealthMonitor",
]

