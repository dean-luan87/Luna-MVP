# histogram_analyzer.py
import cv2
import numpy as np


class HistogramAnalyzer:
    """
    对帧亮度进行直方图统计：
    - 黑区占比（暗光）
    - 高光占比（过曝）
    """

    def __init__(self):
        # 区间阈值可调
        self.dark_threshold = 40       # Y < 40 视为暗区
        self.bright_threshold = 200    # Y > 200 视为强光区

    def analyze(self, frame):
        """
        返回：
        {
            "dark_ratio": 0.0 ~ 1.0,
            "bright_ratio": 0.0 ~ 1.0
        }
        """
        if frame is None:
            return {"dark_ratio": 1, "bright_ratio": 0}

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
        total = np.sum(hist)

        if total == 0:
            return {"dark_ratio": 1, "bright_ratio": 0}

        dark_ratio = float(np.sum(hist[:self.dark_threshold]) / total)
        bright_ratio = float(np.sum(hist[self.bright_threshold:]) / total)

        return {
            "dark_ratio": dark_ratio,
            "bright_ratio": bright_ratio
        }

























