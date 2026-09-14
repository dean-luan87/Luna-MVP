# 📌 Cursor 指令：创建 1.3.0 的 ABC 模块与 Pipeline

请按照以下结构，在 `luna_badge_v1_2/vision/` 目录下创建或覆盖对应文件：

## 📁 文件结构

```
luna_badge_v1_2/vision/
    ├── brightness_detector.py      (A模块)
    ├── scene_complexity.py         (C模块)
    ├── frame_scheduler.py          (B模块)
    └── vision_pipeline.py          (Pipeline - ABC集成版)
```

---

## =====================================================
# A1. brightness_detector.py
# =====================================================

```python
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
```

---

## =====================================================
# B1. frame_scheduler.py
# =====================================================

```python
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
```

---

## =====================================================
# C1. scene_complexity.py
# =====================================================

```python
"""
Scene Complexity Estimator (v1.3.0)

环境复杂度评估模块（C 模块）

功能：
- 对每一帧图像评估其"复杂程度"，输出 0~1 的浮点数
  - 0 表示非常简单（空旷、静止）
  - 1 表示非常复杂（结构多、运动多）

评估依据：
- 边缘密度（结构复杂度）
- 帧间差异（动态复杂度）
- 灰度方差（整体纹理/对比度）

设计特点：
- 不依赖 YOLO 结果，只看画面本身（轻量级）
- 可在 YOLO 之前先判断是否需要提高处理频率
- 使用下采样和灰度处理，计算开销小
"""

from typing import Optional

import cv2
import numpy as np


class SceneComplexityEstimator:
    """
    环境复杂度评估模块（C 模块）

    功能：
    - 对每一帧图像评估其"复杂程度"，输出 0~1 的浮点数
      - 0 表示非常简单（空旷、静止）
      - 1 表示非常复杂（结构多、运动多）

    评估依据：
    - 边缘密度（结构复杂度）
    - 帧间差异（动态复杂度）
    - 灰度方差（整体纹理/对比度）
    """

    def __init__(
        self,
        resize_width: int = 80,
        resize_height: int = 60,
        canny_threshold1: int = 50,
        canny_threshold2: int = 150,
        weight_edges: float = 0.4,
        weight_motion: float = 0.4,
        weight_contrast: float = 0.2,
        smoothing_alpha: float = 0.5,
    ):
        """
        初始化环境复杂度评估器

        Args:
            resize_width: 下采样宽度（默认 80）
            resize_height: 下采样高度（默认 60）
            canny_threshold1: Canny 边缘检测低阈值（默认 50）
            canny_threshold2: Canny 边缘检测高阈值（默认 150）
            weight_edges: 边缘密度权重（默认 0.4）
            weight_motion: 运动复杂度权重（默认 0.4）
            weight_contrast: 对比度权重（默认 0.2）
            smoothing_alpha: 时间平滑系数（默认 0.5，越大越敏感）
        """
        self.resize_width = resize_width
        self.resize_height = resize_height
        self.canny_threshold1 = canny_threshold1
        self.canny_threshold2 = canny_threshold2

        # 各项权重
        self.weight_edges = weight_edges
        self.weight_motion = weight_motion
        self.weight_contrast = weight_contrast

        # 平滑系数
        self.smoothing_alpha = smoothing_alpha

        # 内部状态
        self._prev_gray_small: Optional[np.ndarray] = None
        self._last_complexity: float = 0.0

    # ------------------------------------------------------------------ #
    # 对外主接口
    # ------------------------------------------------------------------ #

    def evaluate(self, frame) -> float:
        """
        输入一帧 BGR 图像，返回复杂度分数 [0,1]

        Args:
            frame: 输入图像帧（BGR 格式，numpy array）

        Returns:
            float: 复杂度分数，范围 [0, 1]
                - ~0.1 → 很简单（空路、没什么变化）
                - ~0.5 → 中等（有些人/车/纹理）
                - ~0.8 → 很复杂（人车密集 / 大量运动）
        """
        # 1. 转灰度 + 下采样
        gray_small = self._preprocess(frame)

        # 2. 边缘密度
        edge_density = self._compute_edge_density(gray_small)

        # 3. 帧间差异（运动量）
        motion_score = self._compute_motion_score(gray_small)

        # 4. 对比度/纹理强度
        contrast_score = self._compute_contrast_score(gray_small)

        # 5. 线性加权得到原始复杂度
        raw = (
            self.weight_edges * edge_density
            + self.weight_motion * motion_score
            + self.weight_contrast * contrast_score
        )

        # 6. 限制到 [0,1]
        raw = self._clamp(raw, 0.0, 1.0)

        # 7. 时间平滑
        complexity = (
            self.smoothing_alpha * raw
            + (1.0 - self.smoothing_alpha) * self._last_complexity
        )

        complexity = self._clamp(complexity, 0.0, 1.0)

        # 更新内部状态
        self._last_complexity = complexity
        self._prev_gray_small = gray_small

        return float(complexity)

    # ------------------------------------------------------------------ #
    # 子步骤：预处理
    # ------------------------------------------------------------------ #

    def _preprocess(self, frame) -> np.ndarray:
        """
        转灰度 + resize 到较小尺寸

        Args:
            frame: 输入 BGR 图像

        Returns:
            np.ndarray: 下采样后的灰度图像
        """
        # 防御性检查
        if frame is None or frame.size == 0:
            raise ValueError("输入帧为空")
        
        # 如果已经是灰度图，直接使用
        if len(frame.shape) == 2:
            gray = frame
        elif len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            raise ValueError(f"不支持的图像格式: shape={frame.shape}")
        
        small = cv2.resize(gray, (self.resize_width, self.resize_height))
        return small

    # ------------------------------------------------------------------ #
    # 子步骤：边缘密度
    # ------------------------------------------------------------------ #

    def _compute_edge_density(self, gray_small: np.ndarray) -> float:
        """
        计算边缘密度（结构复杂度）

        Args:
            gray_small: 下采样后的灰度图像

        Returns:
            float: 边缘密度分数 [0, 1]
        """
        edges = cv2.Canny(
            gray_small,
            self.canny_threshold1,
            self.canny_threshold2,
        )
        edge_pixels = np.count_nonzero(edges)
        total_pixels = edges.size

        if total_pixels == 0:
            return 0.0

        density = edge_pixels / float(total_pixels)

        # 一般密度不会超过 0.3 左右，这里简单乘一个系数再 clamp
        normalized = density * 2.0  # 放大一点，便于参与 0~1 组合
        return self._clamp(normalized, 0.0, 1.0)

    # ------------------------------------------------------------------ #
    # 子步骤：帧间差异（运动复杂度）
    # ------------------------------------------------------------------ #

    def _compute_motion_score(self, gray_small: np.ndarray) -> float:
        """
        计算帧间差异（动态复杂度）

        Args:
            gray_small: 当前帧下采样后的灰度图像

        Returns:
            float: 运动分数 [0, 1]，0 表示无变化，1 表示变化很大
        """
        if self._prev_gray_small is None:
            return 0.0

        # 计算绝对差
        diff = cv2.absdiff(gray_small, self._prev_gray_small)
        mean_diff = float(np.mean(diff))  # 0~255

        # 映射到 0~1
        score = mean_diff / 255.0
        return self._clamp(score, 0.0, 1.0)

    # ------------------------------------------------------------------ #
    # 子步骤：对比度 / 纹理强度
    # ------------------------------------------------------------------ #

    def _compute_contrast_score(self, gray_small: np.ndarray) -> float:
        """
        计算对比度/纹理强度

        Args:
            gray_small: 下采样后的灰度图像

        Returns:
            float: 对比度分数 [0, 1]
        """
        var = float(np.var(gray_small))  # 理论范围大约 0~(255^2)
        normalized = var / (255.0 * 255.0)
        return self._clamp(normalized, 0.0, 1.0)

    # ------------------------------------------------------------------ #
    # 工具函数
    # ------------------------------------------------------------------ #

    @staticmethod
    def _clamp(value: float, vmin: float, vmax: float) -> float:
        """
        将值限制在指定范围内

        Args:
            value: 输入值
            vmin: 最小值
            vmax: 最大值

        Returns:
            float: 限制后的值
        """
        return max(vmin, min(vmax, value))
```

---

## =====================================================
# Pipeline. vision_pipeline.py (ABC集成版)
# =====================================================

```python
"""
VisionPipeline v1.3.0（ABC集成版）

将三个模块串联：
A. BrightnessDetector
B. FrameScheduler
C. SceneComplexityEstimator

现在的愿景：
Pipeline 负责将输入帧流 → 各模块 → 返回抽帧建议、亮度状态、复杂度状态。

后续 D/E/F/G… 会逐步加入。
"""

from typing import Dict, Any

from .brightness_detector import BrightnessDetector
from .scene_complexity import SceneComplexityEstimator
from .frame_scheduler import FrameScheduler


class VisionPipeline:
    """
    VisionPipeline v1.3.0（ABC集成版）

    将三个模块串联：
    - A: BrightnessDetector（亮度检测）
    - B: FrameScheduler（抽帧调度）
    - C: SceneComplexityEstimator（环境复杂度）
    """

    def __init__(self):
        self.brightness_detector = BrightnessDetector()
        self.scene_complexity = SceneComplexityEstimator()
        self.frame_scheduler = FrameScheduler()

        self._last_output_fps = None
        self._frame_count = 0

    def process_frame(self, frame) -> Dict[str, Any]:
        """
        主接口：输入原始图像帧，输出抽帧建议与基础分析信息。
        
        注意：这是 ABC 集成版的简化接口。
        完整版 Pipeline 使用 process() 方法，包含更多模块。
        """
        """
        主接口：输入原始图像帧，输出抽帧建议与基础分析信息。

        Args:
            frame: 输入图像帧（BGR 格式，numpy array）

        Returns:
            dict: 包含以下字段
                - brightness: float, 亮度值 (0~1)
                - scene_complexity: float, 场景复杂度 (0~1)
                - suggested_fps: int, 建议的 FPS
                - should_process: bool, 是否应该处理这一帧
        """

        self._frame_count += 1

        # A. 亮度检测
        brightness_state = self.brightness_detector.update(frame)
        brightness_value = brightness_state.value

        # C. 环境复杂度
        scene_complexity = self.scene_complexity.evaluate(frame)

        # B. 抽帧建议
        suggested_fps = self.frame_scheduler.suggest_fps(
            scene_complexity=scene_complexity,
            motion_speed=0.0,     # 后续加入速度模块
            brightness=brightness_value,
            is_turning=False,     # 后续加入转头检测
            static_stable=False,  # 后续加入静态记忆模块
        )

        # 判断当前帧是否应该被处理
        should_process = self.frame_scheduler.should_process(
            self._frame_count, suggested_fps
        )

        return {
            "brightness": brightness_value,
            "scene_complexity": scene_complexity,
            "suggested_fps": suggested_fps,
            "should_process": should_process,
        }
```

---

## ✅ 验证步骤

创建完成后，请运行以下测试验证：

### 方法1：独立测试各模块

```python
import sys
sys.path.insert(0, '.')

import numpy as np
from luna_badge_v1_2.vision.brightness_detector import BrightnessDetector
from luna_badge_v1_2.vision.scene_complexity import SceneComplexityEstimator
from luna_badge_v1_2.vision.frame_scheduler import FrameScheduler

# 创建模块
brightness_detector = BrightnessDetector()
scene_complexity = SceneComplexityEstimator()
frame_scheduler = FrameScheduler()

# 创建测试帧
test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

# A: 亮度检测
brightness_state = brightness_detector.update(test_frame)

# C: 环境复杂度
complexity = scene_complexity.evaluate(test_frame)

# B: 抽帧建议
suggested_fps = frame_scheduler.suggest_fps(
    scene_complexity=complexity,
    motion_speed=0.0,
    brightness=brightness_state.value,
    is_turning=False,
    static_stable=False,
)

should_process = frame_scheduler.should_process(1, suggested_fps)

result = {
    "brightness": brightness_state.value,
    "scene_complexity": complexity,
    "suggested_fps": suggested_fps,
    "should_process": should_process,
}

print(result)
# 预期输出类似：
# {
#     "brightness": 0.42,
#     "scene_complexity": 0.68,
#     "suggested_fps": 8,
#     "should_process": True
# }
```

### 方法2：使用完整版 Pipeline（如果已存在）

```python
import sys
sys.path.insert(0, '.')

import numpy as np
from luna_badge_v1_2.vision.vision_pipeline import VisionPipeline

# 创建 Pipeline
pipeline = VisionPipeline()

# 创建测试帧
test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

# 处理帧（完整版使用 process() 方法）
result = pipeline.process(test_frame)

# 输出结果
print(f"brightness: {result.get('brightness', 'N/A')}")
print(f"scene_complexity: {result.get('scene_complexity', 'N/A')}")
print(f"fps: {result.get('fps', 'N/A')}")
```

---

## 📝 注意事项

1. **导入路径**：确保所有文件都在 `luna_badge_v1_2/vision/` 目录下
2. **依赖库**：需要安装 `opencv-python` 和 `numpy`
3. **测试**：创建后请运行验证步骤，确保没有导入错误

---

## 🎯 下一步

完成 ABC 模块后，可以继续开发：
- **D**: StaticMapMemory（静态场景记忆）
- **E**: DynamicHazardDetector（动态路况检测）

