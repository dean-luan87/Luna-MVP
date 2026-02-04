"""
Frame Scheduler (v1.3.0)

模块 B：动态抽帧调度器

根据：
- 场景复杂度 scene_complexity (0~1)
- 用户移动速度 motion_speed (0~1)
- 亮度 brightness (0~1)
- （可选）是否转头 is_turning
- （可选）静态环境 + 记忆可复用 static_stable

决定本轮摄像处理建议的 FPS。

设计目标：
- 简单可控、可在 RV1126 等设备上稳定运行
- 默认给出安全合理的变化范围（2 ~ 15 fps）
- 预留接口给未来 1.4/2.0 版本增加更多因子
"""

from typing import Optional


class FrameScheduler:
    """
    动态抽帧调度器（B 模块）

    根据：
    - 场景复杂度 scene_complexity (0~1)
    - 用户移动速度 motion_speed (0~1)
    - 亮度 brightness (0~1)
    - （可选）是否转头 is_turning
    - （可选）静态环境 + 记忆可复用 static_stable

    决定本轮摄像处理建议的 FPS。

    设计目标：
    - 简单可控、可在 RV1126 等设备上稳定运行
    - 默认给出安全合理的变化范围（2 ~ 15 fps）
    - 预留接口给未来 1.4/2.0 版本增加更多因子
    """

    def __init__(
        self,
        min_fps: int = 2,
        max_fps: int = 15,
        base_fps: int = 6,
        complexity_weight: float = 6.0,
        speed_weight: float = 4.0,
        smoothing_alpha: float = 0.5,
    ):
        self.min_fps = min_fps
        self.max_fps = max_fps
        self.base_fps = base_fps

        self.complexity_weight = complexity_weight
        self.speed_weight = speed_weight
        self.smoothing_alpha = smoothing_alpha

        # 当前 FPS（初始用 base_fps）
        self.current_fps: float = float(base_fps)

    # ---------------------------------------------------------- #
    # 对外主接口
    # ---------------------------------------------------------- #

    def suggest_fps(
        self,
        scene_complexity: float,
        motion_speed: float,
        brightness: float,
        is_turning: bool = False,
        static_stable: bool = False,
    ) -> int:
        """
        返回建议 FPS（整数）。

        参数说明：
        - scene_complexity: 0~1，0=极简单，1=极复杂
        - motion_speed: 0~1，0=静止，1=快速移动/小跑
        - brightness: 0~1，0=全黑，1=非常亮
        - is_turning: 是否处于大幅转头阶段（未来可由方向模块提供）
        - static_stable: 是否静态稳定且可复用记忆（未来由静态地图模块提供）
        """

        # 1. 输入清洗（防止乱值）
        sc = self._clamp(scene_complexity, 0.0, 1.0)
        ms = self._clamp(motion_speed, 0.0, 1.0)
        br = self._clamp(brightness, 0.0, 1.0)

        # 2. 从基准 FPS 出发
        target_fps = float(self.base_fps)

        # 3. 场景复杂度影响
        complexity_factor = self.complexity_weight * sc
        target_fps += complexity_factor

        # 4. 移动速度影响
        speed_factor = self.speed_weight * ms
        target_fps += speed_factor

        # 5. 亮度影响（暗环境略微提高 FPS）
        brightness_boost = 0.0
        if br < 0.25:
            brightness_boost = 2.0
        elif br < 0.40:
            brightness_boost = 1.0
        target_fps += brightness_boost

        # 6. 静态 + 记忆可复用 → 降 FPS
        static_adjust = 0.0
        if static_stable and sc < 0.3 and ms < 0.3:
            static_adjust = -2.0
        target_fps += static_adjust

        # 7. 转头阶段暂时不做额外处理（未来可扩展）
        # if is_turning:
        #     ...

        # 8. 限制在 [min_fps, max_fps]
        target_fps = self._clamp(target_fps, float(self.min_fps), float(self.max_fps))

        # 9. 做一次平滑，避免频繁跳变
        new_fps = (
            self.smoothing_alpha * target_fps
            + (1.0 - self.smoothing_alpha) * self.current_fps
        )
        new_fps = self._clamp(new_fps, float(self.min_fps), float(self.max_fps))

        # 更新内部状态
        self.current_fps = new_fps

        # 返回整数 FPS
        return int(round(new_fps))

    # ---------------------------------------------------------- #
    # 抽帧判断
    # ---------------------------------------------------------- #

    def should_process(self, frame_count: int, suggested_fps: int) -> bool:
        """
        根据建议的 FPS 和当前帧计数，判断是否应该处理这一帧

        Args:
            frame_count: 当前帧计数（从 1 开始）
            suggested_fps: 建议的 FPS

        Returns:
            bool: True 表示应该处理这一帧，False 表示跳过
        """
        if suggested_fps <= 0:
            return False

        # 假设输入帧率为 15 fps（摄像头实际帧率）
        # 如果建议 FPS 是 15，则每帧都处理
        # 如果建议 FPS 是 5，则每 3 帧处理一次（15/5=3）
        input_fps = 15.0
        interval = max(1, int(round(input_fps / suggested_fps)))
        return (frame_count % interval) == 0

    # ---------------------------------------------------------- #
    # 工具函数
    # ---------------------------------------------------------- #

    @staticmethod
    def _clamp(value: float, vmin: float, vmax: float) -> float:
        return max(vmin, min(vmax, value))

