# -*- coding: utf-8 -*-
"""
v1.8.5: Task Planner（任务规划器）

职责：
- 消费 Scene / Map / Memory / Risk 的上下文
- 在可行路径中，选"对这个用户更合适"的那条

设计原则：
- Risk 不是"播报系统"，在任务链里是一个路径评分因子
- 任务链消费的是 Risk 的软信号（risk_attention_boost / avoid_bias），不消费播报文本
- Risk 与 Map/Memory 一样，只影响选择，不下结论
"""

from typing import List, Tuple, Dict, Any
from dataclasses import dataclass

from .types import Path, ContextBundle


@dataclass
class PathScore:
    """路径评分结果"""
    path: Path
    score: float
    reasons: List[Dict[str, Any]]


class TaskPlanner:
    """
    任务规划器（消费 Scene / Map / Memory / Risk / Emotion 的上下文）
    
    唯一职责：
    在可行路径中，选"对这个用户更合适"的那条
    
    任务链不直接看 GPS、不直接看视觉
    它只看 ContextBundle
    """
    W_EMOTION: float = 0.05  # Phase D Lite: 情绪权重（默认 0.05，极弱影响，可关闭）
    ENABLE_EMOTION_INFLUENCE: bool = False  # Phase D Lite: 是否启用情绪影响（默认 False，一期关闭）
    
    def choose_path(
        self,
        paths: List[Path],
        context: ContextBundle,
        risk_weight: float = 0.4,
        map_risk_weight: float = 0.3,
        memory_weight: float = 0.5,
        length_weight: float = 0.05,
    ) -> Tuple[Path, float, List[Dict[str, Any]]]:
        """
        选择路径（基于上下文，包含风险）
        
        评分公式：
        final_score = base_utility - length_cost - map_risk_cost 
                    - memory_discomfort_cost - risk_cost
        
        其中：
        - risk_cost = risk_bias.risk_level * risk_weight
        - map_risk_cost = map_hint.seasonal_risk 惩罚
        - memory_discomfort_cost = memory_bias.discomfort_score * memory_weight
        
        Args:
            paths: 路径选项列表
            context: 上下文包
            risk_weight: 风险权重（默认 0.4）
            map_risk_weight: 地图风险权重（默认 0.3）
            memory_weight: 记忆权重（默认 0.5）
            length_weight: 长度权重（默认 0.05）
        
        Returns:
            Tuple[Path, float, List[Dict[str, Any]]]: (选择的路径, 评分, 原因列表)
        """
        scored: List[PathScore] = []
        
        for path in paths:
            score = 1.0  # base_utility
            reasons: List[Dict[str, Any]] = []
            
            # 1. 路径长度（越短越好）
            length_cost = path.length * length_weight
            score -= length_cost
            reasons.append({
                "type": "LENGTH",
                "cost": length_cost,
                "path_length": path.length,
            })
            
            # 2. 地图风险惩罚
            if context.map_hint.seasonal_risk:
                if "ice" in context.map_hint.seasonal_risk:
                    cost = map_risk_weight * 0.3
                    score -= cost
                    reasons.append({
                        "type": "MAP_RISK",
                        "tag": "ice",
                        "cost": cost,
                    })
                if "snow" in context.map_hint.seasonal_risk:
                    cost = map_risk_weight * 0.2
                    score -= cost
                    reasons.append({
                        "type": "MAP_RISK",
                        "tag": "snow",
                        "cost": cost,
                    })
            
            # 坡度惩罚
            if context.map_hint.slope > 10:
                cost = map_risk_weight * 0.2
                score -= cost
                reasons.append({
                    "type": "MAP_SLOPE",
                    "slope": context.map_hint.slope,
                    "cost": cost,
                })
            
            # 3. 用户不适惩罚（权重大）
            if context.memory_bias:
                cost = context.memory_bias.discomfort_score * memory_weight
                score -= cost
                reasons.append({
                    "type": "MEMORY_DISCOMFORT",
                    "discomfort_score": context.memory_bias.discomfort_score,
                    "tags": context.memory_bias.tags,
                    "cost": cost,
                })
            
            # 4. 风险惩罚（包 A：RiskBias 接入）
            if context.risk_bias:
                risk_cost = context.risk_bias.risk_level * risk_weight
                score -= risk_cost
                reasons.append({
                    "type": "RISK",
                    "risk_level": context.risk_bias.risk_level,
                    "dominant_type": context.risk_bias.dominant_type,
                    "cost": risk_cost,
                })
            
            # 5. Phase D Lite: 情绪影响（可选，极弱影响）
            if self.ENABLE_EMOTION_INFLUENCE and context.emotional_context:
                # 只允许"风险/不适的放大或缓和"，不能颠覆选择
                valence = context.emotional_context.aggregate_valence
                if valence < -0.5:
                    # 负面情绪 → 更保守（降低评分）
                    emotion_cost = abs(valence) * self.W_EMOTION
                    score -= emotion_cost
                    reasons.append({
                        "type": "EMOTION",
                        "valence": valence,
                        "cost": emotion_cost,
                    })
                elif valence > 0.5:
                    # 正面情绪 → 稍微积极（提升评分）
                    emotion_bonus = valence * self.W_EMOTION * 0.5  # 正面影响更弱
                    score += emotion_bonus
                    reasons.append({
                        "type": "EMOTION",
                        "valence": valence,
                        "bonus": emotion_bonus,
                    })
            
            # 6. 照明情况（夜间）
            if context.map_hint.lighting == "poor_at_night":
                cost = 0.1
                score -= cost
                reasons.append({
                    "type": "LIGHTING",
                    "lighting": "poor_at_night",
                    "cost": cost,
                })
            
            scored.append(PathScore(
                path=path,
                score=score,
                reasons=reasons,
            ))
        
        # 选择得分最高的路径
        chosen = max(scored, key=lambda x: x.score)
        return chosen.path, chosen.score, chosen.reasons

