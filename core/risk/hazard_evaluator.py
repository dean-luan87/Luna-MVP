# -*- coding: utf-8 -*-
"""
v1.8.4: 环境危险评估器（HazardLevel 计算）

职责：
- 计算环境本身的危险程度（HazardLevel）
- 融合规则/来源/世界模型（1.8.4 先用规则 + confidence）
"""

from typing import Dict, Any, Optional
from core.risk.risk_types import get_risk_config
from core.risk.interfaces.world_model_iface import WorldModelInterface


class HazardEvaluator:
    """
    环境危险评估器
    
    说明：
    - 1.8.4 先用 hazard_base + 来源 confidence
    - 后续世界模型可修正 hazard_level（有护栏则下调等）
    """
    
    def __init__(self, world_model: Optional[WorldModelInterface] = None):
        """
        初始化危险评估器
        
        Args:
            world_model: 世界模型接口（可选，1.8.4 可为 None）
        """
        self.world_model = world_model
    
    def evaluate_hazard(
        self,
        risk_object: "RiskObject",
        scene_context: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        计算环境危险程度（HazardLevel）
        
        Hazard 评估顺序约定：
        1. 基础 hazard（规则 / 静态）
        2. 世界模型修正（护栏、结构）
        3. 动态区域修正（hazard_multiplier）- 由 RiskAdvisoryService 在外部应用
        
        注意：本函数只负责步骤 1-2，步骤 3 由 RiskAdvisoryService 通过 apply_hazard_modifier() 完成
        
        Args:
            risk_object: 风险对象
            scene_context: 场景上下文（包含 objects, signs 等，可选）
        
        Returns:
            float: HazardLevel (0.0 ~ 1.0)
        """
        # 获取基础 hazard_level（从 risk_object 中获取）
        # 如果 risk_object 已经有 hazard_level，直接使用；否则从配置获取
        if risk_object.hazard_level > 0:
            hazard_level = risk_object.hazard_level
        else:
            config = get_risk_config(risk_object.risk_type)
            hazard_base = config.get("hazard_base", 0.5)
            hazard_level = hazard_base * risk_object.confidence
        
        # 如果世界模型可用，尝试修正 hazard_level
        if self.world_model:
            correction = self.world_model.get_hazard_correction(risk_object.risk_type, scene_context)
            if correction is not None:
                # 例如：有护栏则 hazard_level 下调
                hazard_level = max(0.0, min(1.0, hazard_level * correction))
        
        return max(0.0, min(1.0, hazard_level))

