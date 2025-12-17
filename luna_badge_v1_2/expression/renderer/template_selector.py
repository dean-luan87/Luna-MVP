"""
Template Selector (C-3.2)

模板选择器

⚠️ 一期只需简单规则
二期可改为权重 / 学习，但接口不变
"""

from .template_models import ExpressionTemplate
from .render_profile import RenderProfile
from typing import List


class TemplateSelector:
    """
    模板选择器
    
    职责：
    - 根据 action 和 profile 选择最合适的模板
    - 一期：规则驱动
    - 二期：权重 / 学习
    """
    
    def select(
        self,
        templates: List[ExpressionTemplate],
        action: str,
        profile: RenderProfile
    ) -> ExpressionTemplate:
        """
        选择模板
        
        选择规则：
        1. action 必须支持
        2. precision 落在模板区间
        3. 匹配度最高者优先
        
        Args:
            templates: 模板列表
            action: 动作类型
            profile: 表达风格
            
        Returns:
            ExpressionTemplate: 选中的模板
            
        Raises:
            RuntimeError: 没有匹配的模板
        """
        candidates = [
            t for t in templates
            if action in t.supported_actions
            and t.min_precision <= profile.precision <= t.max_precision
        ]
        
        if not candidates:
            raise RuntimeError(f"No template matched for action={action}, precision={profile.precision}")
        
        # 返回第一个匹配的模板（一期简单规则）
        # 二期可以改为权重排序
        return candidates[0]
