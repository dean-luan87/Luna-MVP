#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Observer Mode 核心评估指标计算 (v1.8.1)

功能：计算 Observer Mode 的核心评估指标
原则：基于日志数据计算，不修改日志系统
"""

from typing import Dict, Any, List
from collections import defaultdict


def calculate_observer_metrics(log_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    v1.8.1: 核心评估指标计算
    
    目标：只提供可计算函数，不接 UI、不接告警、不影响运行。
    
    硬约束：
    - 仅提供函数/脚本入口
    - 不自动运行（避免污染性能与日志）
    - 不影响 v1.8 主链路
    
    Args:
        log_data: 日志数据列表，每个元素应包含：
            - source: 日志来源（应为 "observer_mode"）
            - metadata: 元数据，包含：
                - observer_level: Observer Mode 级别
                - observer_user_response: 用户响应（如有）
                - observer_trigger_reason: 触发原因
                - intervene_reason: 干预原因（如有）
    
    Returns:
        Dict[str, Any]: 评估指标字典，包含：
            - confirm_success_rate: CONFIRM 成功率
            - intervene_trigger_count: INTERVENE 触发次数
            - human_help_trigger_count: 人工求助触发次数
            - avg_confirm_rounds_per_scene: 平均每场景 CONFIRM 轮数
    
    最小指标集合：
        - confirm_success_rate: CONFIRM 成功率
        - intervene_trigger_count: INTERVENE 触发次数
        - human_help_trigger_count: 人工求助触发次数
        - avg_confirm_rounds_per_scene: 平均每场景 CONFIRM 轮数
    """
    # 过滤出 Observer Mode 相关日志
    observer_logs = [
        log for log in log_data
        if log.get("source") == "observer_mode"
    ]
    
    if not observer_logs:
        return {
            "confirm_success_rate": 0.0,
            "intervene_trigger_count": 0,
            "human_help_trigger_count": 0,
            "avg_confirm_rounds_per_scene": 0.0,
            "total_sessions": 0,
            "total_observer_events": 0
        }
    
    # 统计变量
    confirm_responses = defaultdict(int)  # accepted, rejected, ignored
    intervene_count = 0
    human_help_count = 0
    confirm_rounds_by_scene = defaultdict(int)  # 每个场景的 CONFIRM 轮数
    scene_ids = set()
    
    # 遍历日志计算指标
    for log in observer_logs:
        metadata = log.get("metadata", {})
        observer_level = metadata.get("observer_level", "")
        scene_id = metadata.get("scene_id", "unknown")
        scene_ids.add(scene_id)
        
        # CONFIRM 成功率统计
        if observer_level == "confirm":
            user_response = metadata.get("observer_user_response", "")
            if user_response:
                confirm_responses[user_response] += 1
                confirm_rounds_by_scene[scene_id] += 1
        
        # INTERVENE 触发次数统计
        if observer_level == "intervene":
            intervene_count += 1
        
        # 人工求助触发次数统计（通过 trigger_reason 判断）
        trigger_reason = metadata.get("observer_trigger_reason", "")
        if "human_assist" in trigger_reason.lower() or "human_help" in trigger_reason.lower() or "fallback" in trigger_reason.lower():
            human_help_count += 1
    
    # 计算指标
    total_confirm = sum(confirm_responses.values())
    confirm_success_rate = (
        confirm_responses.get("accepted", 0) / total_confirm
        if total_confirm > 0 else 0.0
    )
    
    # 平均每场景 CONFIRM 轮数
    total_scenes = len(scene_ids) if scene_ids else 1
    total_confirm_rounds = sum(confirm_rounds_by_scene.values())
    avg_confirm_rounds_per_scene = (
        total_confirm_rounds / total_scenes
        if total_scenes > 0 else 0.0
    )
    
    return {
        "confirm_success_rate": round(confirm_success_rate, 3),
        "intervene_trigger_count": intervene_count,
        "human_help_trigger_count": human_help_count,
        "avg_confirm_rounds_per_scene": round(avg_confirm_rounds_per_scene, 2),
        "total_sessions": len(scene_ids),
        "total_observer_events": len(observer_logs)
    }

