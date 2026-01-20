# -*- coding: utf-8 -*-
"""
v1.8.4: 警告策略（触发条件、cooldown、话术模板选择）

职责：
- 生成警告文本（只描述空间关系，不描述行为）
- 管理警告触发策略
"""

from typing import Dict, Optional
from core.risk.risk_object import RiskObject
from core.risk.risk_types import RiskType


# 警告模板（边界告知型话术，严禁行为推断和后果推断）
TEMPLATES: Dict[str, list[str]] = {
    "WATER_EDGE": [
        "您已接近水边，请注意与边缘保持安全距离。"
    ],
    "STAIRS": [
        "前方是连续台阶，请注意脚下。"
    ],
    "CONSTRUCTION": [
        "前方可能有施工区域，请注意绕行并留意脚下。"
    ],
    "FENCE": [
        "您已接近边缘或护栏，请注意保持安全距离。"
    ],
    "CROWD": [
        "前方可能拥挤，请放慢速度并注意通行安全。"
    ],
    "CLIFF_EDGE": [
        "您已接近悬崖边缘，请注意与边缘保持安全距离。"
    ],
    "OBSTACLE": [
        "前方有障碍物，请注意避让。"
    ],
}


class WarningPolicy:
    """
    警告策略
    
    核心原则：
    - 只描述空间关系，不描述行为
    - 只做提醒，不做结论
    - 一次触发，不持续骚扰
    """
    
    def __init__(self, templates: Optional[Dict[str, list[str]]] = None):
        """
        初始化警告策略
        
        Args:
            templates: 警告模板字典（如果为 None 则使用默认模板）
        """
        self.templates = templates or TEMPLATES
    
    def generate_advisory_text(self, risk_object: RiskObject) -> str:
        """
        生成警告文本（只描述空间关系，不描述行为）
        
        Args:
            risk_object: 危险对象
        
        Returns:
            str: 警告文本
        """
        risk_type = risk_object.risk_type
        
        # 获取模板列表
        template_list = self.templates.get(risk_type, [])
        
        if not template_list:
            # 默认模板
            return f"您已接近{risk_type}，请注意与边缘保持安全距离。"
        
        # 1.8.4: 简单返回第一个模板（后续可扩展为基于距离/趋势选择不同模板）
        return template_list[0]
    
    def should_trigger(
        self,
        risk_object: RiskObject,
        current_risk_level: float,
        delta_risk: float
    ) -> bool:
        """
        判断是否应该触发警告（策略层检查）
        
        注意：此函数主要做策略层检查，核心触发逻辑在 RiskEngine.should_warn()
        
        Args:
            risk_object: 危险对象
            current_risk_level: 当前 RiskLevel
            delta_risk: ΔRisk
        
        Returns:
            bool: 是否应该触发警告
        """
        # 1.8.4: 策略层不做额外检查，核心逻辑在 RiskEngine
        # 后续可扩展：基于用户偏好、历史记录等做策略调整
        return True


