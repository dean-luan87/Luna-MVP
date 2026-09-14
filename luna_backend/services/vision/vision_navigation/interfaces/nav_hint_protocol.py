"""
视觉提示协议：用于定义导航语句输出标准 (v1.2.0)
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class NavHintProtocol(ABC):
    """导航提示协议基类"""
    
    @abstractmethod
    def build(self, visual_result: Dict[str, Any]) -> Optional[str]:
        """
        构建导航提示
        
        Args:
            visual_result: 视觉检测结果
        
        Returns:
            导航提示文本
        """
        pass


class StandardNavHintProtocol(NavHintProtocol):
    """标准导航提示协议"""
    
    def build(self, visual_result: Dict[str, Any]) -> Optional[str]:
        """
        使用标准协议构建导航提示
        
        Args:
            visual_result: 视觉检测结果
        
        Returns:
            导航提示文本
        """
        from ..vision_navigation.nav_hint_builder import NavHintBuilder
        
        builder = NavHintBuilder()
        return builder.build_final_hint(visual_result)


class CompactNavHintProtocol(NavHintProtocol):
    """紧凑型导航提示协议（更简洁）"""
    
    def build(self, visual_result: Dict[str, Any]) -> Optional[str]:
        """
        使用紧凑协议构建导航提示
        
        Args:
            visual_result: 视觉检测结果
        
        Returns:
            导航提示文本（更简洁）
        """
        from ..vision_navigation.nav_hint_builder import NavHintBuilder
        
        builder = NavHintBuilder()
        hint = builder.build_final_hint(visual_result)
        
        if hint:
            # 简化表达
            hint = hint.replace("方向", "")
            hint = hint.replace("检测到", "")
            hint = hint.replace("标识", "")
        
        return hint


class DetailedNavHintProtocol(NavHintProtocol):
    """详细型导航提示协议（更详细）"""
    
    def build(self, visual_result: Dict[str, Any]) -> Optional[str]:
        """
        使用详细协议构建导航提示
        
        Args:
            visual_result: 视觉检测结果
        
        Returns:
            导航提示文本（更详细）
        """
        from ..vision_navigation.nav_guide_generator import VisualGuideGenerator
        
        generator = VisualGuideGenerator()
        tips = generator.generate_all(visual_result)
        
        if tips:
            return "。".join(tips) + "。"
        
        return None



