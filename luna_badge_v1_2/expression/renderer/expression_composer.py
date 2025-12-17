"""
Expression Composer (C-3.3)

句式生成器

只做三件事：
1. 参数填充
2. 单位/方向文本映射
3. 返回字符串

⚠️ 注意
- 不做情绪
- 不做多语言
- 不判断语义正确性
"""

from .template_models import ExpressionTemplate
from .render_profile import RenderProfile
from ..calibration.expression_params import ExpressionParams


class ExpressionComposer:
    """
    表达组合器
    
    职责：
    - 将模板和参数组合成最终文本
    - 处理单位/方向映射
    """
    
    def compose(
        self,
        template: ExpressionTemplate,
        params: ExpressionParams,
        profile: RenderProfile
    ) -> str:
        """
        组合表达文本
        
        Args:
            template: 表达模板
            params: 表达参数
            profile: 表达风格
            
        Returns:
            str: 生成的文本
        """
        text = template.pattern
        
        # 替换占位符
        text = text.replace("{direction}", self._direction(params))
        text = text.replace("{distance}", self._distance(params))
        text = text.replace("{unit}", self._unit(params))
        text = text.replace("{action}", self._action(params))
        
        return text
    
    def _distance(self, params: ExpressionParams) -> str:
        """
        格式化距离
        
        Args:
            params: 表达参数
            
        Returns:
            str: 距离文本
        """
        return str(int(round(params.distance_value)))
    
    def _unit(self, params: ExpressionParams) -> str:
        """
        格式化单位
        
        Args:
            params: 表达参数
            
        Returns:
            str: 单位文本
        """
        if params.distance_unit == "steps":
            return "步"
        if params.distance_unit == "meters":
            return "米"
        if params.distance_unit == "seconds":
            return "秒"
        return ""
    
    def _direction(self, params: ExpressionParams) -> str:
        """
        格式化方向
        
        Args:
            params: 表达参数
            
        Returns:
            str: 方向文本
        """
        # 根据 direction_reference 选择映射
        if params.direction_reference == "egocentric":
            # 自我中心：左手边 / 右手边
            mapping = {
                "turn_left": "左手边",
                "turn_right": "右手边",
                "go_straight": "前方",
                "stop": "停止"
            }
        else:
            # 绝对方向：左 / 右（不带"转"，因为模板中已有"转"）
            mapping = {
                "turn_left": "左",
                "turn_right": "右",
                "go_straight": "直行",
                "stop": "停止"
            }
        
        return mapping.get(params.action, "")
    
    def _action(self, params: ExpressionParams) -> str:
        """
        格式化动作
        
        Args:
            params: 表达参数
            
        Returns:
            str: 动作文本
        """
        mapping = {
            "turn_left": "左转",
            "turn_right": "右转",
            "go_straight": "直行",
            "stop": "停止"
        }
        return mapping.get(params.action, params.action)
