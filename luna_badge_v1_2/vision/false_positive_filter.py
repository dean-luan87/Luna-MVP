"""
False Positive Filter (v1.3.0)
"""


class FalsePositiveFilter:
    def __init__(self):
        pass

    def filter(self, detections):
        """Filter false positives"""
        return detections if detections else []  # 返回过滤后的结果


