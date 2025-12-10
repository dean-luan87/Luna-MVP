# scene_light_classifier.py


class SceneLightClassifier:
    """
    根据亮度等级 + 黑区/亮区比例
    判断大场景类型：
    - 室外晴天
    - 室外阴天
    - 夜晚街道
    - 室内（商场/医院）
    - 地铁站（暗光 + 稳定光）
    """

    def classify(self, level, dark_ratio, bright_ratio, stability):
        """
        返回场景字符串：
        "outdoor_sunny"
        "outdoor_cloudy"
        "indoor"
        "metro"
        "night"
        """

        # 夜晚（暗 + 高波动灯光）
        if level in ["L0", "L1"] and bright_ratio < 0.1:
            return "night"

        # 室外晴天
        if level in ["L4"] and bright_ratio > 0.20:
            return "outdoor_sunny"

        # 室外阴天
        if level == "L3" and bright_ratio < 0.20:
            return "outdoor_cloudy"

        # 地铁（暗 + 稳定）
        if level in ["L1", "L2"] and 0 <= stability <= 10:
            return "metro"

        # 默认室内
        return "indoor"














