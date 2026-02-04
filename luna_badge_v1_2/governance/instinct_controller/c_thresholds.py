from dataclasses import dataclass


@dataclass(frozen=True)
class CThresholdProfile:
    """
    Phase-1 阈值配置
    原则：
    - 只描述“触发条件”
    - 不表达决策意图
    - 不包含任何 Authority / 能力信息
    """
    obstacle_near_m: float
    obstacle_critical_m: float
    approach_speed_fast_mps: float


DEFAULT_C_THRESHOLD_PROFILE = CThresholdProfile(
    obstacle_near_m=3.0,
    obstacle_critical_m=1.0,
    approach_speed_fast_mps=1.5,
)
