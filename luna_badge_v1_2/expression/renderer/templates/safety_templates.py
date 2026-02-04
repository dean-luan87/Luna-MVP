"""
Safety Templates (C-3)

安全模板（一期：模板渲染，不允许自由生成）
"""

from typing import Dict, Any
from ...calibrator.protocol import ExpressionProtocol


class SafetyTemplates:
    """
    安全模板集合
    
    注意：
    - 不允许自由生成
    - 只允许模板渲染
    """
    
    def __init__(self):
        """初始化安全模板"""
        self._templates: Dict[str, Dict[str, str]] = {}
        self._initialize_templates()
    
    def _initialize_templates(self) -> None:
        """初始化模板（一期先做骨架）"""
        # 一期：先做骨架，后续填充
        pass
    
    def render(
        self,
        protocol: ExpressionProtocol,
        safety_type: str,
        direction: str,
        distance: float,
        **kwargs
    ) -> str:
        """
        渲染安全模板
        
        Args:
            protocol: 表达协议
            safety_type: 安全类型
            direction: 方向
            distance: 距离
            **kwargs: 其他参数
            
        Returns:
            str: 渲染后的文本
        """
        # 一期：先做骨架，返回占位文本
        return f"[SAFETY_TEMPLATE] {protocol.value} {safety_type} {direction} {distance}m"
