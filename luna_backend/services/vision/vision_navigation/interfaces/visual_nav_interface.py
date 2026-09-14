"""
视觉导航与主导航接口 (v1.2.0)
使得 navigation_routes 可以直接调用视觉导航
"""

from typing import Dict, Any, Optional
from utils.logger import vision_log
from config.error_codes import ERR


class VisualNavigationInterface:
    """视觉导航接口"""
    
    def __init__(self):
        """初始化视觉导航接口"""
        from ..vision_navigation.nav_hint_builder import NavHintBuilder
        from ..vision_navigation.nav_merge_strategy import NavMergeStrategy
        
        self.hint_builder = NavHintBuilder()
        self.merge_strategy = NavMergeStrategy()
    
    def process(self, vision_data: Dict[str, Any], path_nav_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        处理视觉数据并生成导航提示
        
        Args:
            vision_data: 视觉检测结果数据
            path_nav_hint: 路径导航提示（可选）
        
        Returns:
            包含导航提示的结果字典
        """
        try:
            # 构建视觉提示
            visual_hint = self.hint_builder.build_final_hint(vision_data)
            
            # 合并视觉提示和路径提示
            final_hint = self.merge_strategy.prioritize(visual_hint, path_nav_hint)
            
            # 格式化用于TTS
            tts_hint = self.merge_strategy.format_for_tts(final_hint)
            
            result = {
                "visual_hint": visual_hint,
                "path_hint": path_nav_hint,
                "merged_hint": final_hint,
                "tts_hint": tts_hint,
                "has_visual_guidance": visual_hint is not None
            }
            
            vision_log("VISUAL_NAV_PROCESSED", {
                "has_visual_hint": visual_hint is not None,
                "has_path_hint": path_nav_hint is not None
            })
            
            return result
            
        except Exception as e:
            vision_log("VISUAL_NAV_ERROR", {"error": str(e)})
            return {
                "visual_hint": None,
                "path_hint": path_nav_hint,
                "merged_hint": path_nav_hint,
                "tts_hint": path_nav_hint,
                "has_visual_guidance": False,
                "error": str(e)
            }
    
    def generate_step_guidance(self, step_info: Dict[str, Any]) -> Optional[str]:
        """
        生成台阶导航指引
        
        Args:
            step_info: 台阶信息
        
        Returns:
            台阶导航指引文本
        """
        from ..vision_navigation.nav_guide_generator import VisualGuideGenerator
        
        generator = VisualGuideGenerator()
        return generator.generate_step_tip(step_info)
    
    def generate_hazard_guidance(self, hazard_info: Dict[str, Any]) -> Optional[str]:
        """
        生成危险导航指引
        
        Args:
            hazard_info: 危险信息
        
        Returns:
            危险导航指引文本
        """
        from ..vision_navigation.nav_guide_generator import VisualGuideGenerator
        
        generator = VisualGuideGenerator()
        return generator.generate_obstacle_tip(hazard_info)



