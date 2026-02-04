"""
Template Registry (C-3.2)

模板注册与管理
"""

from typing import Dict, List
from .template_models import ExpressionTemplate


class TemplateRegistry:
    """
    模板注册器
    
    职责：
    - 注册模板
    - 提供模板查询
    """
    
    def __init__(self):
        """初始化模板注册器"""
        self._templates: Dict[str, ExpressionTemplate] = {}
    
    def register(self, template: ExpressionTemplate):
        """
        注册模板
        
        Args:
            template: 表达模板
        """
        self._templates[template.template_id] = template
    
    def all(self) -> List[ExpressionTemplate]:
        """
        获取所有模板
        
        Returns:
            List[ExpressionTemplate]: 所有模板列表
        """
        return list(self._templates.values())
    
    def get(self, template_id: str) -> ExpressionTemplate:
        """
        根据 ID 获取模板
        
        Args:
            template_id: 模板 ID
            
        Returns:
            ExpressionTemplate: 模板对象
            
        Raises:
            KeyError: 模板不存在
        """
        if template_id not in self._templates:
            raise KeyError(f"Template {template_id} not found")
        return self._templates[template_id]
