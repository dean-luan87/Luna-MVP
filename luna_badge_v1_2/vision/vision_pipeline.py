"""
Vision Pipeline (v1.3.0)

Luna Badge v1.3.0 完整视觉 Pipeline（骨架版）

负责：
- 按顺序调度所有视觉模块
- 进行抽帧判断
- 调用 YOLO / 分割 / 深度模型（通过 MultiModelManager）
- 输出结构化结果包
- 触发播报系统

Pipeline 处理流程：

摄像头输入
  ↓
OrientationFilter（是否转头）
  ↓
BrightnessDetector（亮度+补光）
  ↓
SceneComplexityEstimator（复杂度）
  ↓
SpeedEstimator（速度）
  ↓
FrameScheduler（调度跳帧）
  ↓
MultiModelManager（YOLO/Seg/Depth）
  ↓
DynamicHazardDetector（路况）
  ↓
FalsePositiveFilter（误报过滤）
  ↓
ScenePolicyManager（不同环境策略）
  ↓
BroadcastPolicy（播报）
  ↓
TTSManager（播报）
  ↓
输出结构化结果包（给导航系统）
"""

from typing import Dict, Any

from .brightness_detector import BrightnessDetector
from .frame_scheduler import FrameScheduler
from .scene_complexity import SceneComplexityEstimator
from .static_map_memory import StaticMapMemory
from .dynamic_hazard import DynamicHazardDetector
from .orientation_filter import OrientationFilter
from .speed_estimator import SpeedEstimator
from .multi_model_manager import MultiModelManager
from .false_positive_filter import FalsePositiveFilter
from .resolution_manager import ResolutionManager
from .stability_recovery import StabilityRecovery
from .scene_policy_manager import ScenePolicyManager

from ..audio.broadcast_policy import BroadcastPolicy
from ..audio.tts_manager import TTSManager


class VisionPipeline:
    """
    Luna Badge v1.3.0 完整视觉 Pipeline（骨架版）

    负责：
    - 按顺序调度所有视觉模块
    - 进行抽帧判断
    - 调用 YOLO / 分割 / 深度模型（通过 MultiModelManager）
    - 输出结构化结果包
    - 触发播报系统
    """

    def __init__(self):
        # 初始化所有模块（无逻辑）
        self.brightness_detector = BrightnessDetector()
        self.frame_scheduler = FrameScheduler()
        self.scene_complexity = SceneComplexityEstimator()
        self.static_memory = StaticMapMemory()
        self.hazard_detector = DynamicHazardDetector()
        self.orientation_filter = OrientationFilter()
        self.speed_estimator = SpeedEstimator()
        self.multi_model = MultiModelManager()
        self.false_positive_filter = FalsePositiveFilter()
        self.resolution_manager = ResolutionManager()
        self.stability = StabilityRecovery()
        self.scene_policy = ScenePolicyManager()

        # 音频模块
        self.broadcast_policy = BroadcastPolicy()
        self.tts = TTSManager()

        # 内部状态
        self.frame_index = 0
        self.current_fps = 6  # 由 FrameScheduler 决定

    # ------------------------------------------------------------------
    # 主入口：处理单帧画面，返回结构化结果包
    # ------------------------------------------------------------------
    def process(self, frame) -> Dict[str, Any]:
        """
        处理单帧画面，返回结构化结果包

        Args:
            frame: 输入图像帧（numpy array）

        Returns:
            Dict[str, Any]: 结构化结果包，包含：
                - brightness: 亮度值 (0~1)
                - brightness_level: 亮度等级 (DARK/NORMAL/BRIGHT)
                - need_fill_light: 是否需要补光
                - scene_complexity: 场景复杂度 (0~1)
                - motion_speed: 移动速度 (0~1)
                - fps: 当前处理帧率
                - skip_frame: 是否跳过本帧
                - detections: 模型检测结果
                - hazards: 动态路况危险列表
                - scene_type: 场景类型
                - policy: 场景策略配置
                - broadcast: 播报消息列表
        """
        self.frame_index += 1

        # A: 转头过滤（无逻辑，只占位）
        is_turning = False
        frame = self.orientation_filter.filter(frame, is_turning)

        # B: 亮度检测 + 补光建议
        brightness_state = self.brightness_detector.update(frame)

        # C: 环境复杂度
        scene_complexity = self.scene_complexity.evaluate(frame)

        # F: 用户移动速度估计
        motion_speed = self.speed_estimator.estimate()

        # D: 静态环境匹配（复用记忆）
        static_stable = self.static_memory.match(frame)

        # B: 抽帧调度器
        new_fps = self.frame_scheduler.suggest_fps(
            scene_complexity,
            motion_speed,
            brightness_state.value,
            is_turning=is_turning,
            static_stable=static_stable,
        )

        skip_frame = (self.frame_index % max(int(15 / max(new_fps, 1)), 1)) != 0
        self.current_fps = new_fps

        if skip_frame:
            return {
                "skip_frame": True,
                "fps": self.current_fps,
                "brightness": brightness_state.value,
                "brightness_level": brightness_state.level,
                "need_fill_light": brightness_state.need_fill_light,
                "scene_complexity": scene_complexity,
                "motion_speed": motion_speed,
            }

        # H: 多模型协作（YOLO, Segmentation, Depth…）
        model_output = self.multi_model.run_models(frame)

        # E: 提取动态路况
        hazards = self.hazard_detector.detect(model_output)

        # J: 误报过滤
        hazards = self.false_positive_filter.filter(hazards)

        # M: 场景策略（街道/医院/商场…）
        scene_type = self.scene_policy.detect_scene(frame)
        scene_policy = self.scene_policy.apply_policy(scene_type)

        # I: 播报策略
        broadcast_messages = self.broadcast_policy.decide(hazards, scene_type)

        # 执行播报
        for msg in broadcast_messages:
            self.tts.speak(msg)

        # 输出结构化结果包
        return {
            "skip_frame": False,
            "fps": self.current_fps,

            "brightness": brightness_state.value,
            "brightness_level": brightness_state.level,
            "need_fill_light": brightness_state.need_fill_light,

            "scene_complexity": scene_complexity,
            "motion_speed": motion_speed,

            "detections": model_output,
            "hazards": hazards,

            "scene_type": scene_type,
            "policy": scene_policy,

            "broadcast": broadcast_messages,
        }
