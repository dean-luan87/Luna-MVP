#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视觉输出控制器 (v1.8.1)

功能：控制视觉识别的输出状态和模板
原则：不修改现有视觉识别代码，仅新增输出控制层
"""

from typing import Dict, Any, Tuple, Optional
from core.vision_output_state import VisionOutputState


def determine_vision_output_state(input_data: Dict[str, Any]) -> VisionOutputState:
    """
    输出态判定函数
    
    根据输入数据判定应该使用的视觉输出状态
    
    Args:
        input_data: 输入数据，可包含：
            - risk_level: 风险等级（"LOW" / "MEDIUM" / "HIGH"）
            - branch_detected: 是否检测到分叉（bool）
    
    Returns:
        VisionOutputState: 判定的输出状态
    
    判定规则：
        - risk_level == "HIGH" → INTERVENE
        - branch_detected == True → CONFIRM
        - 其他情况 → BACKGROUND
    """
    risk_level = input_data.get("risk_level", "LOW")
    branch_detected = input_data.get("branch_detected", False)
    
    # 优先级：INTERVENE > CONFIRM > BACKGROUND
    if risk_level == "HIGH":
        return VisionOutputState.INTERVENE
    
    if branch_detected:
        return VisionOutputState.CONFIRM
    
    return VisionOutputState.BACKGROUND


def generate_output_template(
    output_state: VisionOutputState,
    context: Dict[str, Any]
) -> Tuple[str, bool, bool]:
    """
    三态输出模板绑定
    
    根据输出状态和上下文生成标准化的输出文本
    
    Args:
        output_state: 视觉输出状态
        context: 上下文信息，可包含：
            - target: 目标名称（用于 CONFIRM）
            - risk_description: 风险描述（用于 INTERVENE）
    
    Returns:
        Tuple[str, bool, bool]: (输出文本, 是否中断当前播报, 是否等待用户响应)
    
    模板定义：
        - BACKGROUND: "我在看着，前方通道正常。"
        - CONFIRM: "你现在对着的是【目标】，对吗？"
        - INTERVENE: "停一下，前方是【风险描述】。"
    
    规则：
        - INTERVENE 必须中断当前播报（interrupt=True）
        - CONFIRM 必须等待 yes/no 回答（wait_response=True）
    """
    if output_state == VisionOutputState.INTERVENE:
        risk_description = context.get("risk_description", "危险环境")
        text = f"停一下，前方是【{risk_description}】。"
        return (text, True, False)  # (text, interrupt, wait_response)
    
    elif output_state == VisionOutputState.CONFIRM:
        target = context.get("target", "目标")
        text = f"你现在对着的是【{target}】，对吗？"
        return (text, False, True)  # 不中断，但等待响应
    
    else:  # BACKGROUND
        text = "我在看着，前方通道正常。"
        return (text, False, False)  # 不中断，不等待响应


