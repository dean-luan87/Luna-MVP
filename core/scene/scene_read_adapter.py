# -*- coding: utf-8 -*-
"""
v1.8.5: Scene Read Adapter（场景读取适配器 - 防越权）

职责：
- 显式限制 Risk / Task / Emotion 各自能读什么
- 防止 Scene 层被滥用成"隐形决策层"
- 确保中台不直接读取 SceneState

原则：
- Scene 只提供事实，中台自己判断
- 每个中台只能读取允许的字段
- 禁止直接读取完整 SceneState
"""

from __future__ import annotations
from typing import Dict, Any, Optional, List

from .schema import SceneState


def get_scene_for_risk(scene: SceneState) -> Dict[str, Any]:
    """
    为 Risk 中台提供场景信息（受限读取）
    
    允许读取：
    - scene_type: 风险类型参考（湖畔 / 道路 / 商场）
    - static_model.structures: hazard 修正（是否存在护栏、台阶）
    - dynamic_model.temporary_events: dynamic active（施工 / 拥堵）
    - dynamic_model.crowd_density: 弱权重修正（不直接触发）
    - confidence: 置信度降权（低置信度只能降权）
    
    禁止读取：
    - scene_memory: 场景记忆
    - visited_count: 访问次数
    - Scene 不能直接返回 risk_level / should_warn
    
    Args:
        scene: 场景状态
    
    Returns:
        Dict[str, Any]: Risk 中台可读取的场景信息
    """
    return {
        "scene_type": scene.scene_type,
        "static_structures": (
            [{"type": s.type, "geometry": s.geometry, "confidence": s.confidence}
             for s in scene.static_model.structures]
            if scene.static_model and scene.static_model.structures
            else None
        ),
        "dynamic_events": (
            scene.dynamic_model.temporary_events
            if scene.dynamic_model and scene.dynamic_model.temporary_events
            else None
        ),
        "crowd_density": (
            scene.dynamic_model.crowd_density
            if scene.dynamic_model
            else None
        ),
        "confidence": scene.confidence,
    }


def get_scene_for_task(scene: SceneState) -> Dict[str, Any]:
    """
    为任务链中台提供场景信息（受限读取）
    
    允许读取：
    - scene_type: 任务适配（是否适合当前任务）
    - dynamic_model.scene_phase: 时段判断
    - scene_memory.useful_places: 任务补全（早餐 / 商店）
    - scene_memory.observed_risks: 任务注意点
    
    禁止读取：
    - static_model.structures.geometry: 具体几何结构
    - 不能直接控制任务流转（只能建议）
    
    Args:
        scene: 场景状态
    
    Returns:
        Dict[str, Any]: 任务链中台可读取的场景信息
    """
    return {
        "scene_type": scene.scene_type,
        "scene_phase": (
            scene.dynamic_model.scene_phase
            if scene.dynamic_model
            else None
        ),
        "useful_places": (
            scene.scene_memory.useful_places
            if scene.scene_memory and scene.scene_memory.useful_places
            else None
        ),
        "observed_risks": (
            scene.scene_memory.observed_risks
            if scene.scene_memory and scene.scene_memory.observed_risks
            else None
        ),
    }


def get_scene_for_emotion(scene: SceneState) -> Dict[str, Any]:
    """
    为情绪计算中台提供场景信息（受限读取）
    
    允许读取：
    - scene_type: 情绪基调（室外 / 室内）
    - scene_memory.visited_count: 熟悉度
    - dynamic_model.crowd_density: 压迫 / 放松
    - dynamic_model.traffic_level: 紧张度
    
    禁止读取：
    - 具体结构几何
    - 推断风险结论
    
    Args:
        scene: 场景状态
    
    Returns:
        Dict[str, Any]: 情绪计算中台可读取的场景信息
    """
    return {
        "scene_type": scene.scene_type,
        "visited_count": (
            scene.scene_memory.visited_count
            if scene.scene_memory
            else None
        ),
        "crowd_density": (
            scene.dynamic_model.crowd_density
            if scene.dynamic_model
            else None
        ),
        "traffic_level": (
            scene.dynamic_model.traffic_level
            if scene.dynamic_model
            else None
        ),
    }


