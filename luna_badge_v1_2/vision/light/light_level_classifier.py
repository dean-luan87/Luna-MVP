# light_level_classifier.py


class LightLevelClassifier:
    """
    根据亮度 + 黑区占比 + 高光占比
    计算统一亮度等级 L0~L5。
    """

    def __init__(self):
        pass

    def classify(self, luma, dark_ratio, bright_ratio):
        """
        返回亮度等级:
        L0 极暗
        L1 暗光
        L2 微弱光
        L3 正常光
        L4 强光
        L5 过曝
        """

        # 过曝优先判定
        if bright_ratio > 0.40 or luma > 220:
            return "L5"

        # 极暗
        if luma < 20 or dark_ratio > 0.70:
            return "L0"

        # 暗光
        if 20 <= luma < 40 or dark_ratio > 0.50:
            return "L1"

        # 微弱光
        if 40 <= luma < 80:
            return "L2"

        # 正常光
        if 80 <= luma < 150 and bright_ratio < 0.20:
            return "L3"

        # 强光（逆光）
        if 150 <= luma < 220 or bright_ratio > 0.20:
            return "L4"

        return "L3"  # fallback

























