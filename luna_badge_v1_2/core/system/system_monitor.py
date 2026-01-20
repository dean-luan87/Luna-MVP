import random
from infra.logging_manager import get_logger

logger = get_logger("system_monitor")


class SystemMonitor:
    """
    简化版系统监控：
    真机可以接 psutil；这里先返回 [0.1, 0.5] 范围内的随机值。
    """

    def cpu_usage(self) -> float:
        value = random.uniform(0.1, 0.5)
        logger.debug(f"[SYSTEM] cpu_usage={value:.2f}")
        return value















