from .c_thresholds import CThresholdProfile, DEFAULT_C_THRESHOLD_PROFILE


THRESHOLD_REGISTRY = {
    "default": DEFAULT_C_THRESHOLD_PROFILE,
    # 场景级
    "indoor_safe": CThresholdProfile(
        obstacle_near_m=2.5,
        obstacle_critical_m=0.8,
        approach_speed_fast_mps=1.2,
    ),
    "outdoor_open": CThresholdProfile(
        obstacle_near_m=3.5,
        obstacle_critical_m=1.2,
        approach_speed_fast_mps=1.8,
    ),
    # 用户偏好级（不是调参）
    "user_conservative": CThresholdProfile(
        obstacle_near_m=4.0,
        obstacle_critical_m=1.5,
        approach_speed_fast_mps=1.0,
    ),
}
