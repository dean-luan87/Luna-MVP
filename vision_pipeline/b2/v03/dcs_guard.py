# vision_pipeline/b2/v03/dcs_guard.py
"""
DCS Guard (v0.4.1)
只审判，不学习

Patch 6: DCS 守卫（只审判，不学习）
"""

from typing import Dict, Any, List


def dcs_check(summary: Dict[str, Any]) -> List[str]:
    """
    DCS 边界检查
    
    :param summary: B2 的 summary 输出
    :return: 违规列表（空列表表示无违规）
    """
    violations = []
    
    # 检查 1: advisory_only 必须为 True
    if summary.get("advisory_only") is not True:
        violations.append("B_CONFIRMED_RISK")
    
    # 检查 2: NEED_STOP 必须有正确的干预级别
    impact = summary.get("impact")
    if hasattr(impact, "name"):
        impact_name = impact.name
    elif isinstance(impact, str):
        impact_name = impact
    else:
        impact_name = str(impact)
    
    if impact_name == "NEED_STOP":
        intervention_level = summary.get("intervention_level")
        if intervention_level != "HARD":
            violations.append("INVALID_INTERVENTION_LEVEL")
    
    # 检查 3: 禁止的 impact 类型
    forbidden_impacts = ["FORCE_STOP", "CONFIRMED_DANGER", "IMMEDIATE_ACTION"]
    if impact_name in forbidden_impacts:
        violations.append(f"FORBIDDEN_IMPACT_{impact_name}")
    
    # 检查 4: 角色声明必须存在
    if summary.get("role") != "B":
        violations.append("MISSING_ROLE_DECLARATION")
    
    # 检查 5: 系统时间必须存在
    if "system_ts" not in summary:
        violations.append("MISSING_SYSTEM_TIME")
    
    return violations


def calculate_dcs_penalty(violations: List[str]) -> int:
    """
    计算 DCS 扣分
    
    :param violations: 违规列表
    :return: 扣分数值（负数）
    """
    penalty_map = {
        "B_CONFIRMED_RISK": -50,  # CRITICAL
        "INVALID_INTERVENTION_LEVEL": -25,  # HIGH
        "FORBIDDEN_IMPACT_FORCE_STOP": -50,  # CRITICAL
        "FORBIDDEN_IMPACT_CONFIRMED_DANGER": -50,  # CRITICAL
        "FORBIDDEN_IMPACT_IMMEDIATE_ACTION": -50,  # CRITICAL
        "MISSING_ROLE_DECLARATION": -10,  # MEDIUM
        "MISSING_SYSTEM_TIME": -50,  # CRITICAL
    }
    
    total_penalty = 0
    for violation in violations:
        total_penalty += penalty_map.get(violation, -5)  # 默认 -5
    
    return total_penalty
