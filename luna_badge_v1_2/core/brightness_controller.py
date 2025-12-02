"""
Brightness Controller (MVP 精简版)

功能：
- 基于 LightSenseEngine 输出的亮度等级（L0~L5）
- 仅决定补光 ON / OFF
- 不包含档位、偏好、状态机、延迟机制
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional


# 占位：避免循环依赖
class LightSenseEnginePlaceholder:
    def process(self, frame):
        return {
            "luma": 80.0,
            "dark_ratio": 0.2,
            "bright_ratio": 0.1,
            "level": "L3",
            "stability": 5.0,
            "scene": "indoor",
        }


@dataclass
class BrightnessAnalysis:
    luma: float
    dark_ratio: float
    bright_ratio: float
    level: str
    stability: float
    scene: str
    flash_on: bool  # True = 开补光，False = 关补光


class BrightnessController:
    """
    MVP 亮度控制器：
    - 不做复杂策略
    - 只根据亮度等级 L0~L5 决定是否开补光
    """

    def __init__(self, lightsense: Optional[Any] = None):
        self.lightsense = lightsense or LightSenseEnginePlaceholder()

    # ------------------ 主入口 ------------------ #

    def analyze(self, frame: Any) -> BrightnessAnalysis:
        info = self.lightsense.process(frame)

        level = str(info.get("level", "L3")).upper()

        flash_on = self._should_turn_on_flash(level)

        return BrightnessAnalysis(
            luma=info.get("luma", 0.0),
            dark_ratio=info.get("dark_ratio", 0.0),
            bright_ratio=info.get("bright_ratio", 0.0),
            level=level,
            stability=info.get("stability", 0.0),
            scene=info.get("scene", "unknown"),
            flash_on=flash_on,
        )

    # ------------------ 补光逻辑 ------------------ #

    def _should_turn_on_flash(self, level: str) -> bool:
        """
        MVP 补光规则：
        L0/L1/L2 → ON
        L3/L4/L5 → OFF
        """
        if level in ("L0", "L1", "L2"):
            return True
        return False

    # ------------------ 控制硬件 ------------------ #

    def control_hardware_light(self, analysis: BrightnessAnalysis):
        """
        硬件控制占位：
        - 后续接 GPIO / PWM
        """
        if analysis.flash_on:
            print("[Flash] ON")
        else:
            print("[Flash] OFF")
