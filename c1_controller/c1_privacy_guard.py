"""
C1 隐私护栏（强规则，不可被模型推翻）

这是强规则，必须写死。
Class B 不允许用户强制开启镜头。
"""


class C1PrivacyGuard:
    """
    C1 隐私守卫
    
    职责：
    - 根据隐私场景分类决定是否允许视觉
    - 强制执行隐私规则（Class B 不允许用户强制开启）
    """
    
    @staticmethod
    def allow_camera(privacy_zone: str, user_override: bool) -> bool:
        """
        判断是否允许摄像头工作
        
        Args:
            privacy_zone: 隐私区域（A / B / C）
            user_override: 用户是否强制要求开启
        
        Returns:
            如果允许摄像头工作，返回 True；否则返回 False
        """
        if privacy_zone == "C":
            return False
        
        if privacy_zone == "B":
            return False   # 不允许用户强制开启
        
        return True
