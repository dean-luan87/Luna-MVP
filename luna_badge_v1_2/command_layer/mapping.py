"""
Command Layer → ParsedIntent 映射

将 NormalizedCommand + ResolutionResult 映射为 ParsedIntent
保持与 v1.4.3 的 ParsedIntent 契约兼容
"""

from typing import Dict, Any
from .semantic_normalizer import NormalizedCommand
from .ecs_resolver import ResolutionResult
from core.intent_schema import ParsedIntent


def normalized_to_parsed_intent(
    normalized: NormalizedCommand,
    resolution: ResolutionResult
) -> ParsedIntent:
    """
    将 NormalizedCommand + ResolutionResult 映射为 ParsedIntent
    
    Args:
        normalized: 归一化后的命令
        resolution: 参数补全结果
    
    Returns:
        ParsedIntent: 符合 v1.4.3 契约的 ParsedIntent
        
    映射规则：
    - intent_name 由 intent_type 映射得出（固定映射表）
    - slots 优先使用 place_name，否则使用 place_category
    - need_confirm 从 NormalizedCommand 透传
    - source 设置为 "command_layer"（标识来自命令层）
    """
    # 映射 intent_type → intent_name
    intent_name = _map_intent_type_to_name(normalized.intent_type)
    
    # 构建 slots
    slots = _build_slots(normalized, resolution)
    
    # 构建 raw 文本（用于调试）
    raw_text = _build_raw_text(normalized, resolution)
    
    return ParsedIntent(
        intent_name=intent_name,
        slots=slots,
        source="command_layer",  # 标识来自命令层
        need_confirm=normalized.need_confirm,
        raw=raw_text
    )


def _map_intent_type_to_name(intent_type: str) -> str:
    """
    将 intent_type 映射为 ParsedIntent.intent_name
    
    映射表：
    - NAVIGATE -> START_TASK（如果无当前任务）或 CHANGE_DESTINATION（如果有当前任务）
    - CANCEL_TASK -> CANCEL_TASK
    - INSERT_TASK -> INSERT_TASK
    - REPLACE_TASK -> CHANGE_DESTINATION
    - UNKNOWN -> UNKNOWN
    """
    mapping = {
        "NAVIGATE": "START_TASK",  # 默认映射为 START_TASK，实际可能需要根据上下文判断
        "CANCEL_TASK": "CANCEL_TASK",
        "INSERT_TASK": "INSERT_TASK",
        "REPLACE_TASK": "CHANGE_DESTINATION",
        "UNKNOWN": "UNKNOWN",
    }
    return mapping.get(intent_type, "UNKNOWN")


def _build_slots(
    normalized: NormalizedCommand,
    resolution: ResolutionResult
) -> Dict[str, Any]:
    """
    构建 ParsedIntent.slots
    
    规则：
    - 优先使用 resolution.slots 中的 place_name
    - 如果没有 place_name，使用 place_category
    - 保留其他有用的信息
    """
    slots = {}
    
    # 使用补全后的 slots
    resolved_slots = resolution.slots
    
    # 提取地点信息
    place_name = resolved_slots.get("place_name")
    place_category = resolved_slots.get("place_category") or normalized.slots.get("place_category")
    place_address = resolved_slots.get("place_address")
    
    # 根据 intent_type 构建不同的 slots 结构
    if normalized.intent_type == "NAVIGATE":
        # 导航任务：使用 destination 或 target
        if place_name:
            slots["destination"] = place_name
            slots["target"] = place_name
        elif place_category:
            slots["destination"] = place_category
            slots["target"] = place_category
        
        if place_address:
            slots["address"] = place_address
    
    elif normalized.intent_type == "INSERT_TASK":
        # 插入任务：使用 task_type
        if place_category:
            slots["task_type"] = place_category
        if place_name:
            slots["place_name"] = place_name
        if place_address:
            slots["address"] = place_address
    
    elif normalized.intent_type == "REPLACE_TASK":
        # 替换任务：使用 destination
        if place_name:
            slots["destination"] = place_name
        elif place_category:
            slots["destination"] = place_category
        if place_address:
            slots["address"] = place_address
    
    elif normalized.intent_type == "CANCEL_TASK":
        # 取消任务：不需要额外 slots
        pass
    
    # 保留补全来源信息（用于调试）
    if resolution.source:
        slots["_resolution_source"] = resolution.source
    if resolution.reason:
        slots["_resolution_reason"] = resolution.reason
    
    return slots


def _build_raw_text(
    normalized: NormalizedCommand,
    resolution: ResolutionResult
) -> str:
    """
    构建 ParsedIntent.raw 文本（用于调试和日志）
    """
    parts = [
        f"[CommandLayer] intent_type={normalized.intent_type}",
    ]
    
    if resolution.resolved:
        parts.append(f"resolved={resolution.resolved}, source={resolution.source}")
    else:
        parts.append(f"resolved={resolution.resolved}, reason={resolution.reason}")
    
    if resolution.slots.get("place_name"):
        parts.append(f"place_name={resolution.slots.get('place_name')}")
    elif resolution.slots.get("place_category"):
        parts.append(f"place_category={resolution.slots.get('place_category')}")
    
    return " | ".join(parts)












