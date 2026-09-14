"""
视觉导航与主导航（路径导航）的合并策略 (v1.2.0)
"""

from typing import Optional
from utils.logger import vision_log


class NavMergeStrategy:
    """导航合并策略"""
    
    def __init__(self):
        """初始化导航合并策略"""
        pass
    
    def merge(self, visual_hint: Optional[str], path_hint: Optional[str]) -> Optional[str]:
        """
        合并视觉提示和路径提示
        
        Args:
            visual_hint: 视觉提示文本
            path_hint: 路径导航提示文本
        
        Returns:
            合并后的提示文本
        """
        if not visual_hint and not path_hint:
            return None
        
        if not visual_hint:
            return path_hint
        
        if not path_hint:
            return visual_hint
        
        # 合并策略：路径提示 + 视觉提示
        merged = f"{path_hint}；注意：{visual_hint}"
        
        vision_log("NAV_MERGED", {
            "visual_hint": visual_hint,
            "path_hint": path_hint,
            "merged": merged
        })
        
        return merged
    
    def prioritize(self, visual_hint: Optional[str], path_hint: Optional[str]) -> Optional[str]:
        """
        优先级合并：如果视觉提示包含危险信息，优先使用视觉提示
        
        Args:
            visual_hint: 视觉提示文本
            path_hint: 路径导航提示文本
        
        Returns:
            优先级合并后的提示文本
        """
        if not visual_hint and not path_hint:
            return None
        
        if not visual_hint:
            return path_hint
        
        if not path_hint:
            return visual_hint
        
        # 检查视觉提示是否包含危险信息
        danger_keywords = ["危险", "台阶", "障碍", "红灯", "critical", "hazard"]
        has_danger = any(keyword in visual_hint for keyword in danger_keywords)
        
        if has_danger:
            # 危险信息优先
            return f"⚠️ {visual_hint}；路径：{path_hint}"
        else:
            # 正常合并
            return self.merge(visual_hint, path_hint)
    
    def format_for_tts(self, hint: Optional[str]) -> Optional[str]:
        """
        格式化提示文本，使其更适合TTS播报
        
        Args:
            hint: 原始提示文本
        
        Returns:
            格式化后的提示文本
        """
        if not hint:
            return None
        
        # 替换特殊符号
        hint = hint.replace("；", "，")
        hint = hint.replace("⚠️", "注意")
        hint = hint.replace("→", "到")
        hint = hint.replace("←", "从")
        
        # 去除多余空格
        hint = " ".join(hint.split())
        
        return hint



