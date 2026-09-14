#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人工求助策略模块 (v1.8.1)

功能：在复杂场景下建议用户寻求人工帮助
原则：不强制中断当前流程，不修改 v1.8 错误处理逻辑
"""

from typing import Dict, Any, Optional


def should_suggest_human_help(context: Dict[str, Any]) -> bool:
    """
    人工求助触发判断
    
    判断是否应该建议用户寻求人工帮助
    
    Args:
        context: 上下文信息，可包含：
            - confirm_fail_count: 连续 CONFIRM 失败次数
            - observer_confidence: Observer Mode 置信度
            - scene_risk_level: 场景风险等级
    
    Returns:
        bool: True 表示应该建议人工帮助，False 表示不需要
    
    触发条件（任一满足）：
        - 连续 CONFIRM 失败 >= 2
        - observer_confidence < threshold（默认 0.3）
        - scene_risk_level == "HIGH"
    
    要求：
        - 仅返回 true/false
        - 不强制中断当前流程
        - 不修改 v1.8 错误处理逻辑
    """
    confirm_fail_count = context.get("confirm_fail_count", 0)
    observer_confidence = context.get("observer_confidence", 1.0)
    scene_risk_level = context.get("scene_risk_level", "LOW")
    confidence_threshold = context.get("confidence_threshold", 0.3)
    
    # 条件1: 连续 CONFIRM 失败 >= 2
    if confirm_fail_count >= 2:
        return True
    
    # 条件2: Observer 置信度过低
    if observer_confidence < confidence_threshold:
        return True
    
    # 条件3: 场景风险等级高
    if scene_risk_level == "HIGH":
        return True
    
    return False


def generate_human_assist_hint(
    has_staff_detected: bool = False,
    staff_direction: Optional[str] = None
) -> str:
    """
    人工求助话术模板
    
    生成建议用户寻求人工帮助的标准话术
    
    Args:
        has_staff_detected: 是否检测到工作人员
        staff_direction: 工作人员方向（如有）
    
    Returns:
        str: 标准化的求助提示文本
    
    标准输出：
        - 有工作人员: "这个场景不太适合我继续指引，建议你向右前方的工作人员求助。"
        - 无工作人员: "这个场景不太适合我继续指引，建议你询问路人或前往前台。"
    
    要求：
        - 不制造恐慌
        - 不承诺系统能力边界外的事情
        - 不自动终止任务
    """
    if has_staff_detected and staff_direction:
        return f"这个场景不太适合我继续指引，建议你向{staff_direction}的工作人员求助。"
    else:
        return "这个场景不太适合我继续指引，建议你询问路人或前往前台。"


