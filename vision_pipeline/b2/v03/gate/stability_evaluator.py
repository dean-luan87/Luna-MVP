# vision_pipeline/b2/v03/gate/stability_evaluator.py
"""
B2 Gate v0.5 - Stability Evaluator
计算 stability_score：此刻是否适合把"看到的东西"当成世界事实
"""

from typing import Optional, Dict, Any


def compute_stability_score(
    angular_velocity_deg_s: float,
    accel_variance: float,
    optical_flow_magnitude: Optional[float] = None,
    frame_to_frame_transform: Optional[float] = None
) -> float:
    """
    计算稳定性分数
    
    输出范围：0.0 ~ 1.0
    含义：此刻是否适合把"看到的东西"当成世界事实
    
    :param angular_velocity_deg_s: 角速度（度/秒），来自 IMU
    :param accel_variance: 加速度方差（m/s² variance），来自 IMU
    :param optical_flow_magnitude: 光流幅度（可选，兜底方案）
    :param frame_to_frame_transform: 帧间变换（可选，兜底方案）
    :return: stability_score (0.0 ~ 1.0)
    """
    
    # 首选：使用 IMU 数据
    if angular_velocity_deg_s is not None and accel_variance is not None:
        AV_MAX = 25.0        # deg/s，正常人转头上限
        ACC_VAR_MAX = 2.5    # m/s² variance，剧烈走动
        
        av_term = min(angular_velocity_deg_s / AV_MAX, 1.0)
        acc_term = min(accel_variance / ACC_VAR_MAX, 1.0)
        
        stability = 1.0 - (0.6 * av_term + 0.4 * acc_term)
        return round(max(stability, 0.0), 3)
    
    # 兜底：使用视觉估计（TODO: 完整实现）
    elif optical_flow_magnitude is not None:
        # 简化版本：光流越大，稳定性越低
        OF_MAX = 50.0  # 像素/帧，经验值
        of_term = min(optical_flow_magnitude / OF_MAX, 1.0)
        stability = 1.0 - of_term
        return round(max(stability, 0.0), 3)
    
    # 默认：假设稳定（保守）
    return 0.5


def compute_view_state(
    angular_velocity_deg_s: float,
    linear_velocity_m_s: float,
    accel_variance: float,
    pitch: float = 0.0,
    roll: float = 0.0,
    yaw_delta: float = 0.0,
    zoom_level: float = 1.0,
    fov_change: bool = False
) -> Dict[str, Any]:
    """
    计算完整的 view_state
    
    :return: view_state 字典
    """
    stability_score = compute_stability_score(
        angular_velocity_deg_s=angular_velocity_deg_s,
        accel_variance=accel_variance
    )
    
    # 计算 shake_level
    if angular_velocity_deg_s < 5.0:
        shake_level = "LOW"
    elif angular_velocity_deg_s < 15.0:
        shake_level = "MEDIUM"
    else:
        shake_level = "HIGH"
    
    return {
        "camera_motion": {
            "angular_velocity": round(angular_velocity_deg_s, 2),
            "linear_velocity": round(linear_velocity_m_s, 2),
            "shake_level": shake_level
        },
        "camera_pose": {
            "pitch": round(pitch, 2),
            "roll": round(roll, 2),
            "yaw_delta": round(yaw_delta, 2)
        },
        "fov_state": {
            "zoom_level": round(zoom_level, 2),
            "fov_change": fov_change
        },
        "stability_score": stability_score
    }
