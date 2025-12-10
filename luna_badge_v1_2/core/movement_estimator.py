"""
Movement Estimator
根据 Optical Flow / IMU（预留）判断：
- 用户速度（慢走 / 快走 / 小跑）
- 是否旋转
"""


class MovementEstimator:
    def estimate_speed(self, flow_result):
        """
        输出：
        { 'speed_mps': float }
        TODO：光流速度估计算法
        """
        return {"speed_mps": 0.0}

    def is_rotating(self, flow_result):
        """
        判断是否处于高旋转状态
        """
        return False














