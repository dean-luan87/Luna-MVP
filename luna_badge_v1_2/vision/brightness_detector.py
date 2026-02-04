"""
Brightness Detector (v1.3.0)

模块 A：亮度检测 + 补光建议

功能：
- 从当前帧估算亮度（0~1）
- 判断亮度等级（DARK/NORMAL/BRIGHT）
- 根据迟滞阈值，输出是否需要开启补光灯（仅开/关）

说明：
- 不直接控制硬件，只给出建议；硬件控制在 FillLightController 或上层完成
"""

from dataclasses import dataclass
from typing import Literal, Optional

import cv2
import numpy as np

BrightnessLevel = Literal["DARK", "NORMAL", "BRIGHT"]


@dataclass
class BrightnessState:
    """亮度评估结果结构体"""
    value: float                  # 0.0 ~ 1.0
    level: BrightnessLevel        # DARK / NORMAL / BRIGHT
    need_fill_light: bool         # 是否建议开启补光灯


class BrightnessDetector:
    """
    亮度检测 + 补光建议模块（A 模块）

    功能：
    - 从当前帧估算亮度（0~1）
    - 判断亮度等级（DARK/NORMAL/BRIGHT）
    - 根据迟滞阈值，输出是否需要开启补光灯（仅开/关）

    说明：
    - 不直接控制硬件，只给出建议；硬件控制在 FillLightController 或上层完成
    """

    def __init__(
        self,
        on_threshold: float = 0.35,
        off_threshold: float = 0.45,
        sample_interval_frames: int = 5,
        resize_width: int = 160,
        resize_height: int = 120,
    ):
        assert 0.0 <= on_threshold < off_threshold <= 1.0, \
            "on_threshold 必须小于 off_threshold，且在 [0,1] 内"

        self.on_threshold = on_threshold
        self.off_threshold = off_threshold
        self.sample_interval_frames = sample_interval_frames
        self.resize_width = resize_width
        self.resize_height = resize_height

        # 内部状态
        self._frame_counter: int = 0
        self._last_brightness: float = 1.0
        self._last_level: BrightnessLevel = "BRIGHT"
        self._fill_light_on: bool = False  # 当前补光灯状态（由上层同步）

    # ------------------------------------------------------------------ #
    # 对外主接口
    # ------------------------------------------------------------------ #

    def update(self, frame, fill_light_on: Optional[bool] = None) -> BrightnessState:
        """
        主入口：
        - 输入当前帧
        - （可选）告知当前补光灯状态 fill_light_on（用于防抖逻辑）
        - 返回 BrightnessState
        """

        if fill_light_on is not None:
            self._fill_light_on = fill_light_on

        self._frame_counter += 1

        # 达到采样间隔才重新计算亮度，否则复用上一结果
        if self._frame_counter >= self.sample_interval_frames:
            self._frame_counter = 0
            brightness = self._compute_brightness(frame)
            self._last_brightness = brightness
            self._last_level = self._classify_level(brightness)
        else:
            brightness = self._last_brightness

        need_fill = self._decide_fill_light(self._last_brightness, self._fill_light_on)

        return BrightnessState(
            value=self._last_brightness,
            level=self._last_level,
            need_fill_light=need_fill,
        )

    # ------------------------------------------------------------------ #
    # 亮度计算
    # ------------------------------------------------------------------ #

    def _compute_brightness(self, frame) -> float:
        """
        将帧缩小 + 转灰度 + 求平均亮度，映射到 [0,1]
        """

        # 假定输入为 BGR
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 降采样以降低计算量
        small = cv2.resize(gray, (self.resize_width, self.resize_height))

        # 计算平均灰度
        mean_val = float(np.mean(small))  # 0~255

        # 映射到 0~1
        brightness = mean_val / 255.0

        # 限制范围
        brightness = max(0.0, min(1.0, brightness))

        return brightness

    # ------------------------------------------------------------------ #
    # 等级划分
    # ------------------------------------------------------------------ #

    def _classify_level(self, brightness: float) -> BrightnessLevel:
        if brightness < 0.30:
            return "DARK"
        elif brightness > 0.65:
            return "BRIGHT"
        else:
            return "NORMAL"

    # ------------------------------------------------------------------ #
    # 补光开关决策（仅开/关建议）
    # ------------------------------------------------------------------ #

    def _decide_fill_light(self, brightness: float, current_on: bool) -> bool:
        """
        根据当前亮度和补光状态，决定是否"应该处于开启状态"。

        - 当前未开灯：亮度 < on_threshold → 建议开灯
        - 当前已开灯：亮度 > off_threshold → 建议关灯
        - 中间区间：保持现状
        """

        if not current_on:
            # 当前未开灯 → 只有在非常暗时才开
            if brightness < self.on_threshold:
                return True
            else:
                return False
        else:
            # 当前已开灯 → 只有在明显变亮时才关
            if brightness > self.off_threshold:
                return False
            else:
                return True

