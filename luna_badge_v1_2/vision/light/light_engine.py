# light_engine.py

from .brightness_meter import BrightnessMeter
from .histogram_analyzer import HistogramAnalyzer
from .light_level_classifier import LightLevelClassifier
from .stability_checker import StabilityChecker
from .scene_light_classifier import SceneLightClassifier


class LightSenseEngine:
    """
    统一光照感知引擎：
    - 提供光照等级
    - 提供场景分类
    - 提供稳定性
    - 为补光 / 抽帧 / 识别模式 提供输入
    """

    def __init__(self):
        self.meter = BrightnessMeter()
        self.hist = HistogramAnalyzer()
        self.leveler = LightLevelClassifier()
        self.stability = StabilityChecker()
        self.scene = SceneLightClassifier()

    def process(self, frame):
        """
        主流程：输入一帧 → 输出完整光照信息
        """
        luma = self.meter.compute_luma(frame)
        hist = self.hist.analyze(frame)
        dark_ratio = hist["dark_ratio"]
        bright_ratio = hist["bright_ratio"]

        level = self.leveler.classify(luma, dark_ratio, bright_ratio)
        stab = self.stability.update(luma)
        scene_type = self.scene.classify(level, dark_ratio, bright_ratio, stab)

        return {
            "luma": luma,
            "dark_ratio": dark_ratio,
            "bright_ratio": bright_ratio,
            "level": level,
            "stability": stab,
            "scene": scene_type
        }

