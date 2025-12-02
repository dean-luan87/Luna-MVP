# stability_checker.py
from collections import deque


class StabilityChecker:
    """
    计算亮度稳定度（帧间差异）
    用于判断是否需要提升抽帧频率。
    """

    def __init__(self, window_size=5):
        self.window_size = window_size
        self.buffer = deque(maxlen=window_size)

    def update(self, current_luma):
        self.buffer.append(current_luma)

        if len(self.buffer) < 2:
            return 0

        avg = sum(self.buffer) / len(self.buffer)
        stability = abs(current_luma - avg)

        return stability  # 数值越大，光照越不稳定










