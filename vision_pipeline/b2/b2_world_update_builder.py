"""
B2 World Update Builder - 真实输入映射

将现有系统里的真实信号映射到 B2 的 4 个粗维度

B2 v0.1 世界摘要输入标准（定死）：
- density: 视觉检测汇总（len(objects) + len(texts)）
- motion_level: C1 motion_score / frame_diff（线性映射到 0~100）
- illumination: 亮度均值 / 暗光判断（0~100）
- dominant_direction: ego_motion.heading（离散到 0/1/2/3）

重要原则：
- 不要精确
- 不要连续
- 要"稳 + 粗 + 抗抖"
"""

from typing import Dict, Any, List, Optional


def build_b2_world_update(frame_ctx: Dict[str, Any]) -> Dict[str, Any]:
    """
    构建 B2 世界更新（从现有 pipeline 上下文映射）
    
    Args:
        frame_ctx: 帧上下文，包含：
            - objects: 检测到的对象列表（可选）
            - texts: OCR 文本列表（可选）
            - motion_score: C1 运动评分（可选）
            - frame_diff_score: C1 帧差异评分（可选）
            - avg_luminance: 平均亮度（可选，0~1）
            - ego_motion: 自运动信息（可选，包含 heading）
    
    Returns:
        Dict[str, Any]: B2 世界更新，包含：
            - density: 0~100
            - motion_level: 0~100
            - illumination: 0~100
            - dominant_direction: 0~3（前/左/右/后）
    """
    # 1. density: 视觉检测汇总
    objects = frame_ctx.get("objects", [])
    texts = frame_ctx.get("texts", [])
    density = min(len(objects) + len(texts), 100)
    
    # 2. motion_level: C1 motion_score / frame_diff（线性映射到 0~100）
    motion_score = frame_ctx.get("motion_score", 0.0)
    frame_diff_score = frame_ctx.get("frame_diff_score", 0.0)
    # 合并运动信号（取较大值，避免漏检）
    motion_level = int(min(max(motion_score, frame_diff_score) * 100, 100))
    
    # 3. illumination: 亮度均值 / 暗光判断（0~100）
    avg_luminance = frame_ctx.get("avg_luminance")
    if avg_luminance is not None:
        # 如果提供了亮度值（0~1），映射到 0~100
        illumination = int(min(max(avg_luminance * 100, 0), 100))
    else:
        # 如果没有亮度信息，使用默认值（中等亮度）
        illumination = 50
    
    # 4. dominant_direction: ego_motion.heading（离散到 0/1/2/3）
    ego_motion = frame_ctx.get("ego_motion", {})
    heading = ego_motion.get("heading", 0)
    # 将 heading（0~360 度）离散到 4 个方向：0=前，1=右，2=后，3=左
    dominant_direction = int((heading % 360) / 90) % 4
    
    return {
        "density": density,
        "motion_level": motion_level,
        "illumination": illumination,
        "dominant_direction": dominant_direction,
    }


def build_b2_impact_events(
    frame_ctx: Dict[str, Any],
    task_corridor: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    构建 B2 影响事件列表（v0.1 最低接入标准）
    
    v0.1 不要求你真的判断"危险"，只要求有东西进入任务走廊。
    
    Args:
        frame_ctx: 帧上下文，包含：
            - objects: 检测到的对象列表（可选）
            - ego_motion: 自运动信息（可选，包含 velocity）
        task_corridor: 任务走廊信息（可选）
    
    Returns:
        List[Dict[str, Any]]: 影响事件列表，每个事件包含：
            - event_id: 事件 ID
            - event_type: 事件类型
            - affects_corridor: 是否影响走廊
            - risk_level: 风险等级（0~1）
            - time_to_impact_sec: 预计影响时间（可选）
            - meta: 元数据
    """
    impact_events = []
    
    objects = frame_ctx.get("objects", [])
    ego_motion = frame_ctx.get("ego_motion", {})
    ego_velocity = ego_motion.get("velocity", 1.0)  # 默认 1.0 m/s
    
    # v0.1 简化：只要对象在视野前方，就认为可能影响走廊
    for i, obj in enumerate(objects):
        # 简化判断：如果对象有 bbox 且在图像前方区域，认为影响走廊
        bbox = obj.get("bbox") if isinstance(obj, dict) else None
        if bbox is None:
            # 如果没有 bbox，默认认为不影响
            continue
        
        # 简化：如果 bbox 中心在图像下半部分（前方），认为影响走廊
        # 这里假设 bbox 格式为 [x1, y1, x2, y2] 或类似
        if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            cy = (bbox[1] + bbox[3]) / 2 if len(bbox) >= 4 else 0.5
            # 如果中心在图像下半部分（y > 0.5），认为在前方
            affects_corridor = cy > 0.5
        else:
            affects_corridor = False
        
        if affects_corridor:
            # 估算时间到影响（简化：基于距离和速度）
            # v0.1 使用固定估算
            time_to_impact_sec = 5.0  # 默认 5 秒
            
            impact_events.append({
                "event_id": f"obj_{i}",
                "event_type": obj.get("class", "unknown") if isinstance(obj, dict) else "unknown",
                "affects_corridor": True,
                "risk_level": 0.6,  # 默认中等风险
                "time_to_impact_sec": time_to_impact_sec,
                "meta": {
                    "class": obj.get("class", "unknown") if isinstance(obj, dict) else "unknown",
                    "confidence": obj.get("confidence", 0.5) if isinstance(obj, dict) else 0.5,
                }
            })
    
    return impact_events

