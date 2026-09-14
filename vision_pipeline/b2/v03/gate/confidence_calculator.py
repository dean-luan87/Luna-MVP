# vision_pipeline/b2/v03/gate/confidence_calculator.py
"""
B2 Gate v0.5 - Confidence Calculator
置信度拆分：perception / world / final
"""

from typing import Dict, Any, Optional


def calculate_confidence(
    perception_confidence: float,
    stability_score: float,
    temporal_consistency: float,
    gate_mode: str,
    evidence_state: Optional[str] = None
) -> Dict[str, float]:
    """
    计算拆分后的置信度
    
    :param perception_confidence: 模型/规则给的置信度 (0.0 ~ 1.0)
    :param stability_score: 稳定性分数 (0.0 ~ 1.0)
    :param temporal_consistency: 时间一致性分数 (0.0 ~ 1.0)
    :param gate_mode: Gate 模式 ("ACTIVE" | "READ_ONLY" | "SUSPENDED")
    :param evidence_state: 证据状态 ("OBSERVING" | "CONFIRMED" | "DEGRADED" | "DROPPED")
    :return: confidence 字典
    """
    
    # Hard Gate fail → final_confidence = 0
    if gate_mode == "SUSPENDED":
        return {
            "perception": round(perception_confidence, 3),
            "world": 0.0,
            "final": 0.0
        }
    
    # READ_ONLY → 不允许发给 C，但可以计算 world confidence
    if gate_mode == "READ_ONLY":
        world_confidence = stability_score * temporal_consistency
        return {
            "perception": round(perception_confidence, 3),
            "world": round(world_confidence, 3),
            "final": 0.0  # 不允许发给 C
        }
    
    # ACTIVE 模式
    # world_confidence = stability_score * temporal_consistency
    world_confidence = stability_score * temporal_consistency
    
    # 只有 CONFIRMED 才能发 to_c_message
    if evidence_state == "CONFIRMED":
        final_confidence = perception_confidence * world_confidence
    else:
        # OBSERVING / DEGRADED → 不发给 C
        final_confidence = 0.0
    
    return {
        "perception": round(perception_confidence, 3),
        "world": round(world_confidence, 3),
        "final": round(final_confidence, 3)
    }


def get_confidence_dict(
    perception_confidence: float,
    stability_score: float,
    temporal_consistency: float,
    gate_mode: str,
    evidence_state: Optional[str] = None
) -> Dict[str, Any]:
    """
    获取完整的 confidence 字典（用于 trace）
    """
    conf = calculate_confidence(
        perception_confidence=perception_confidence,
        stability_score=stability_score,
        temporal_consistency=temporal_consistency,
        gate_mode=gate_mode,
        evidence_state=evidence_state
    )
    
    return {
        "perception": conf["perception"],
        "world": conf["world"],
        "final": conf["final"]
    }
