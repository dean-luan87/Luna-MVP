# -*- coding: utf-8 -*-
"""
v1.8.5 Phase C 包 C: User Report Router（用户报告路由器）

职责：
- 将用户报告分流到 MemoryRegistry / FactCandidatePool
- 三道防线：类型分流、限频去重、贡献上限

设计原则：
- 所有 user_report 都不能直接入 Library
- 用户报告不提升 confidence，只记一次支持/冲突
- 当 should_freeze_world_writes(position_state)=True 时，直接拒绝写入
"""

import time
from typing import Dict, Any, Optional

from core.world_model.common.types import PositionState
from core.world_model.common.gates import should_freeze_world_writes
from core.world_model.common.rate_limiter import SimpleRateLimiter
from core.world_model.interfaces.user_report_iface import UserReportEvent
from core.world_model.memory.memory_registry import MemoryRegistry
from core.world_model.memory.candidate_pool import FactCandidatePool


class UserReportRouter:
    """
    用户报告路由器
    
    分流规则（写死，防污染）：
    - DISCOMFORT → 只进 Memory（体验资产）
    - PREFERENCE → 只进 Memory（偏好）
    - FACT_CONFIRM / FACT_CONFLICT → 只进 CandidatePool（事实信号）
    - 任何 user_report 不允许直接写 Library
    
    防污染与抗恶意护栏：
    - 限频：同一用户、同一 scene、同一 claim_key，在窗口内只记一次
    - 贡献上限：用户报告最多贡献 support_count +1 或 conflict_count +1，但不提升 confidence
    - 冻结 gate：当 should_freeze_world_writes(position_state)=True 时，直接拒绝写入
    """
    
    def __init__(
        self,
        memory_registry: MemoryRegistry,
        candidate_pool: FactCandidatePool,
        rate_limiter: Optional[SimpleRateLimiter] = None,
    ):
        """
        初始化用户报告路由器
        
        Args:
            memory_registry: 记忆注册表实例
            candidate_pool: 事实候选池实例
            rate_limiter: 限频器实例（如果为 None 则创建默认实例）
        """
        self.memory = memory_registry
        self.pool = candidate_pool
        self.limiter = rate_limiter or SimpleRateLimiter(window_s=120.0)
    
    def ingest(
        self,
        scene_id: str,
        map_id: Optional[str],
        position_state: PositionState,
        event: UserReportEvent,
        now_ts: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        处理用户报告（分流到 Memory / CandidatePool）
        
        Args:
            scene_id: 场景 ID
            map_id: 地图单元 ID（可选）
            position_state: 位置状态
            event: 用户报告事件
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            Dict[str, Any]: 处理结果（accepted, reason）
        """
        now = now_ts or event.ts or time.time()
        
        # Gate：重定位/失衡时禁止写入（与包 B 统一）
        if should_freeze_world_writes(position_state):
            return {"accepted": False, "reason": "world_write_frozen"}
        
        # 限频 Key：user + scene + claim/discomfort
        claim_key = event.claim_type or "_no_claim_"
        key = f"{event.user_id}:{scene_id}:{event.report_type}:{claim_key}"
        if not self.limiter.allow(key, now_ts=now):
            return {"accepted": False, "reason": "rate_limited"}
        
        # 分流：体验/偏好 → Memory
        if event.report_type in ("DISCOMFORT", "PREFERENCE"):
            result = self.memory.update(
                scene_id=scene_id,
                map_id=map_id,
                position_state=position_state,
                feedback={
                    "type": "EXPERIENCE" if event.report_type == "DISCOMFORT" else "PREFERENCE",
                    "tags": event.tags,
                    "valence": "NEGATIVE" if event.report_type == "DISCOMFORT" else "NEUTRAL",
                    "intensity": float(event.intensity or 0.5),
                    "source": "user_report",
                    "raw_text": event.raw_text,
                },
                now_ts=now,
            )
            return {
                "accepted": result.get("written", 0) > 0,
                "reason": "memory_written" if result.get("written", 0) > 0 else result.get("reason", "unknown"),
                "result": result,
            }
        
        # 分流：事实类 → CandidatePool（只作为信号，不入库）
        if event.report_type in ("FACT_CONFIRM", "FACT_CONFLICT"):
            if not event.claim_type:
                return {"accepted": False, "reason": "missing_claim_type"}
            
            # 注意：用户报告不提升 confidence，只记一次支持/冲突
            if event.report_type == "FACT_CONFIRM":
                try:
                    self.pool.upsert_observation(
                        claim_type=event.claim_type,
                        scene_id=scene_id,
                        map_id=map_id,
                        scope={"scene_id": scene_id, "map_id": map_id},
                        source="user_report",
                        is_conflict=False,
                        statement=event.raw_text,
                        now_ts=now,
                        reason="from_user_report_router",
                        position_state=position_state,
                    )
                    return {"accepted": True, "reason": "fact_signal_recorded"}
                except ValueError as e:
                    if "world_write_frozen" in str(e):
                        return {"accepted": False, "reason": "world_write_frozen"}
                    raise
            
            if event.report_type == "FACT_CONFLICT":
                try:
                    self.pool.register_conflict(
                        scene_id=scene_id,
                        map_id=map_id,
                        claim_type=event.claim_type,
                        source="user_report",
                        statement=event.raw_text,
                        now_ts=now,
                        position_state=position_state,
                    )
                    return {"accepted": True, "reason": "fact_conflict_recorded"}
                except ValueError as e:
                    if "world_write_frozen" in str(e):
                        return {"accepted": False, "reason": "world_write_frozen"}
                    raise
        
        return {"accepted": False, "reason": "unknown_report_type"}
