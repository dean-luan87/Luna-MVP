"""
将视觉提示转换成最终可播报提示 (v1.2.0)
负责语言优化、合并提示、优先级处理
"""

from typing import List, Optional, Dict, Any
from utils.logger import vision_log


class NavHintBuilder:
    """导航提示构建器"""
    
    def __init__(self):
        """初始化导航提示构建器"""
        pass
    
    def merge_hints(self, hints: List[str]) -> Optional[str]:
        """
        合并多个提示为单个可播报文本
        
        Args:
            hints: 提示文本列表
        
        Returns:
            合并后的提示文本，如果没有提示则返回None
        """
        if not hints:
            return None
        
        # 去重
        unique_hints = []
        seen = set()
        for hint in hints:
            if hint not in seen:
                unique_hints.append(hint)
                seen.add(hint)
        
        if not unique_hints:
            return None
        
        # 按优先级排序
        priority_sorted = sorted(unique_hints, key=self._priority_key)
        
        # 合并提示
        if len(priority_sorted) == 1:
            return priority_sorted[0]
        elif len(priority_sorted) <= 3:
            return "；".join(priority_sorted)
        else:
            # 只保留前3个最重要的提示
            return "；".join(priority_sorted[:3]) + "等"
    
    def _priority_key(self, text: str) -> int:
        """
        计算提示的优先级
        
        Args:
            text: 提示文本
        
        Returns:
            优先级数字（越小优先级越高）
        """
        text_lower = text.lower()
        
        # 优先级：危险 > 台阶 > 障碍物 > 红绿灯 > 标识牌 > 设施
        if "危险" in text or "critical" in text_lower or "high" in text_lower:
            return 1
        if "台阶" in text or "step" in text_lower or "stair" in text_lower:
            return 2
        if "障碍" in text or "obstacle" in text_lower:
            return 3
        if "红灯" in text or "red" in text_lower:
            return 4
        if "绿灯" in text or "green" in text_lower:
            return 5
        if "标识" in text or "sign" in text_lower:
            return 6
        if "设施" in text or "facility" in text_lower:
            return 7
        
        return 8
    
    def optimize_language(self, hint: str) -> str:
        """
        优化语言表达
        
        Args:
            hint: 原始提示文本
        
        Returns:
            优化后的提示文本
        """
        # 去除冗余词汇
        hint = hint.replace("方向方向", "方向")
        hint = hint.replace("米处", "米")
        hint = hint.replace("  ", " ")
        
        # 统一单位表达
        hint = hint.replace("厘米", "cm")
        
        return hint.strip()
    
    def build_final_hint(self, vision_bundle: Dict[str, Any]) -> Optional[str]:
        """
        从视觉结果包构建最终提示
        
        Args:
            vision_bundle: 视觉结果包
        
        Returns:
            最终提示文本
        """
        from .nav_guide_generator import VisualGuideGenerator
        
        generator = VisualGuideGenerator()
        tips = generator.generate_all(vision_bundle)
        
        if not tips:
            return None
        
        merged = self.merge_hints(tips)
        if merged:
            merged = self.optimize_language(merged)
        
        vision_log("HINT_BUILT", {"hint": merged})
        
        return merged

