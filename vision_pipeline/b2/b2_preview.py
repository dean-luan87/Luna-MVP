"""
B2 Preview - 未来预演（v0.1：只做冲突粗判）
"""

from typing import Dict, Any, List, Tuple
from .b2_types import ImpactEvent, FutureSegmentBuffer, Advisory, ConfidenceReport
from .b2_config import B2_BUFFER_TTL_SEC


def run_preview(
    task_corridor, observe_input: Dict[str, Any]
) -> Tuple[FutureSegmentBuffer, List[Advisory], ConfidenceReport]:
    """
    运行预演（v0.1 不做复杂，只做"是否可能有事"）
    
    Args:
        task_corridor: 任务走廊
        observe_input: 观察输入，包含：
            - impact_events: 影响事件列表（list[dict]）
            - world_observability: 世界可观测性（0~1）
    
    Returns:
        (future_buffer, advisories, confidence): 未来缓存、建议列表、置信报告
    """
    raw_events = observe_input.get("impact_events", [])  # list[dict]
    
    # 筛选与走廊相关的冲突
    conflicts = []
    for e in raw_events:
        if e.get("affects_corridor", False):
            conflicts.append(ImpactEvent(
                event_id=e.get("event_id", "unknown"),
                event_type=e.get("event_type", "unknown"),
                affects_corridor=True,
                risk_level=float(e.get("risk_level", 0.5)),
                time_to_impact_sec=e.get("time_to_impact_sec"),
                meta=e.get("meta", {}),
            ))
    
    # 根据是否有冲突生成不同的 FutureBuffer 和 Advisory
    if conflicts:
        # 有冲突：计算风险窗口
        risk_times = [c.time_to_impact_sec for c in conflicts if c.time_to_impact_sec is not None]
        risk_t = min(risk_times) if risk_times else task_corridor.horizon_sec
        
        fb = FutureSegmentBuffer(
            horizon_sec=task_corridor.horizon_sec,
            corridor_id=task_corridor.corridor_id,
            predicted_conflicts=conflicts,
            safe_window_sec=None,
            risk_window_sec=risk_t,
            ttl_sec=B2_BUFFER_TTL_SEC,
            invalidation_keys=["world_digest"],
        )
        
        advisories = [Advisory(
            advisory_type="PREWARN",
            priority=0,
            confidence=0.7,
            time_to_impact_sec=risk_t,
            reason_code="FUTURE_CONFLICT",
            related_corridor_id=task_corridor.corridor_id,
        )]
    else:
        # 无冲突：安全窗口
        fb = FutureSegmentBuffer(
            horizon_sec=task_corridor.horizon_sec,
            corridor_id=task_corridor.corridor_id,
            predicted_conflicts=[],
            safe_window_sec=task_corridor.horizon_sec,
            risk_window_sec=None,
            ttl_sec=B2_BUFFER_TTL_SEC,
            invalidation_keys=["world_digest"],
        )
        
        advisories = [Advisory(
            advisory_type="DEESCALATE",
            priority=2,
            confidence=0.6,
            time_to_impact_sec=None,
            reason_code="FUTURE_CLEAR",
            related_corridor_id=task_corridor.corridor_id,
        )]
    
    # 生成置信报告
    confidence = ConfidenceReport(
        world_observability=float(observe_input.get("world_observability", 0.8)),
        model_dependency=0.3,
        corridor_certainty=task_corridor.confidence,
        overall=0.75,
    )
    
    return fb, advisories, confidence

