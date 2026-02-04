"""
Render Engine (C-3)

渲染器引擎（一期：模板化输出）

同一 intent 不同协议不同句式
"""

from typing import Dict, Any
from .render_models import RenderedMessage
from .templates.nav_templates import NavigationTemplates
from .templates.safety_templates import SafetyTemplates
from ..calibrator.protocol import ExpressionProtocol
from ..context.embodiment_profiles import EmbodimentProfile


class RenderEngine:
    """
    渲染器引擎
    
    职责：
    - 根据 intent + protocol + embodiment 渲染文本
    - 一期：模板化输出（不允许自由生成）
    - 同一 intent 不同协议不同句式
    """
    
    def __init__(self):
        """初始化渲染器引擎"""
        self.nav_templates = NavigationTemplates()
        self.safety_templates = SafetyTemplates()
    
    def render(
        self,
        intent: Dict[str, Any],
        protocol: ExpressionProtocol,
        embodiment: EmbodimentProfile
    ) -> RenderedMessage:
        """
        渲染意图为文本
        
        Args:
            intent: 意图字典
            protocol: 表达协议
            embodiment: 身体形态配置
            
        Returns:
            RenderedMessage: 渲染后的消息
        """
        intent_type = intent.get("intent_type", "unknown")
        
        # 根据意图类型选择模板
        if intent_type == "navigation":
            text = self._render_navigation(intent, protocol, embodiment)
        elif intent_type == "safety":
            text = self._render_safety(intent, protocol, embodiment)
        else:
            text = f"[UNKNOWN_INTENT] {intent_type}"
        
        return RenderedMessage(
            text=text,
            tags={"intent_type": intent_type},
            protocol=protocol,
            embodiment=embodiment.name
        )
    
    def _render_navigation(
        self,
        intent: Dict[str, Any],
        protocol: ExpressionProtocol,
        embodiment: EmbodimentProfile
    ) -> str:
        """渲染导航意图"""
        action = intent.get("action", "go_straight")
        distance_m = intent.get("distance_m", 0.0)
        direction = intent.get("direction", "forward")
        
        return self.nav_templates.render(
            protocol=protocol,
            action=action,
            distance=distance_m,
            direction=direction
        )
    
    def _render_safety(
        self,
        intent: Dict[str, Any],
        protocol: ExpressionProtocol,
        embodiment: EmbodimentProfile
    ) -> str:
        """渲染安全意图"""
        safety_type = intent.get("safety_type", "warning")
        direction = intent.get("direction", "front")
        distance_m = intent.get("distance_m", 0.0)
        
        return self.safety_templates.render(
            protocol=protocol,
            safety_type=safety_type,
            direction=direction,
            distance=distance_m
        )
