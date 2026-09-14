"""
B2 Decision Gate (v0.1 - 修改版)

v0.1 修改清单：
1. 稳定性阈值从 30/60 秒改成 8/15 秒两级
2. 输出从"拉长心跳"改成"生成 FutureBuffer + Advisory"
3. 使用粗粒度 digest（迁移到 b2_world_digest.py）

注意：此模块为过渡版本，后续将迁移到完整的 B2 架构
"""

import time
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional

# 添加项目根目录到路径
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))

# 注意：此模块为过渡版本，后续将迁移到完整的 B2 架构
# 暂时使用简化的 digest 计算，不依赖 b2_world_digest
from vision_pipeline.b2.b2_digest import compute_world_digest, digest_delta


class B2DecisionGate:
    """
    B2 v0.1（修改版）
    
    修改目标：
    - 让"稳定场景"能够被识别出来（哪怕是复杂视频里的一小段）
    - 让 B2 能产生"FutureBuffer/Advisory"的输出记录
    - 保持安全兜底不变（不影响 C）
    """

    def __init__(self):
        """初始化 B2 决策闸门"""
        self.last_decision_type: Optional[str] = None
        self.world_digest = B2WorldDigest()
        
        # v0.1 修改：稳定性阈值降低
        self.stable_level_1_sec = 8.0  # 原 30s
        self.stable_level_2_sec = 15.0  # 原 60s

    def should_emit(
        self,
        ts: float,
        state: str,
        decision_type: str,
        scene_stats: Dict,
        motion_stats: Dict,
        base_heartbeat: float,
    ) -> Tuple[bool, Dict]:
        """
        判断是否应该产出决策
        
        v0.1 修改：输出 FutureBuffer + Advisory，而非仅拉长心跳
        
        Args:
            ts: 当前时间戳
            state: 当前状态（STABLE / SUSPENDED / RECOVERING）
            decision_type: 决策类型（heartbeat / forced_event）
            scene_stats: 场景统计信息（包含 scene_hash）
            motion_stats: 运动统计信息
            base_heartbeat: 基础心跳间隔（HEARTBEAT_INTERVAL_SEC）
        
        Returns:
            (emit: bool, meta: Dict)
            - emit: 是否应该产出决策
            - meta: 元数据，包含 b2_applied, b2_reason, future_buffer, advisory
        """
        meta = {
            "b2_applied": False,
            "b2_reason": None,
            "effective_heartbeat": base_heartbeat,
            "future_buffer": None,
            "advisory": None,
        }

        # 计算世界摘要（使用粗粒度 digest）
        world_update_dict = {
            "density": len(scene_stats.get("objects", [])) * 2,  # 简化映射
            "motion_level": int(motion_stats.get("motion_score", 0.0) * 100),
            "illumination": 50,  # 默认值
            "dominant_direction": 0,  # 默认值
        }
        digest = compute_world_digest(world_update_dict)
        delta = digest_delta(digest, self.last_digest)
        
        # 检查稳定性
        if digest == self.last_digest:
            if self.scene_stable_since is None:
                self.scene_stable_since = ts
        else:
            self.scene_stable_since = None
        
        stable_duration = (ts - self.scene_stable_since) if self.scene_stable_since else 0.0
        self.last_digest = digest

        # ----------------------------
        # 1. 场景稳定度感知（v0.1 修改：阈值降低）
        # ----------------------------
        if state == "STABLE" and stable_duration > 0:
            # v0.1 修改：生成 FutureBuffer + Advisory
            if stable_duration >= self.stable_level_2_sec:
                # 稳定 15 秒以上：生成 DEESCALATE 建议
                meta["b2_applied"] = True
                meta["b2_reason"] = "long_stable_scene"
                meta["effective_heartbeat"] = base_heartbeat * 2.0
                
                # 生成 FutureBuffer
                meta["future_buffer"] = FutureSegmentBuffer(
                    horizon_sec=10.0,
                    corridor_key="default",
                    safe_window_sec=10.0,
                    invalidation={"digest_hash": digest.digest_hash},
                )
                
                # 生成 Advisory
                meta["advisory"] = Advisory(
                    type=AdvisoryType.DEESCALATE,
                    priority=AdvisoryPriority.P2,
                    time_to_impact_sec=0.0,
                    impact_range_m=0.0,
                    confidence=0.8,
                    reason_code="long_stable_scene",
                )
                
            elif stable_duration >= self.stable_level_1_sec:
                # 稳定 8 秒以上：生成 DEESCALATE 建议
                meta["b2_applied"] = True
                meta["b2_reason"] = "stable_scene"
                meta["effective_heartbeat"] = base_heartbeat * 1.5
                
                # 生成 FutureBuffer
                meta["future_buffer"] = FutureSegmentBuffer(
                    horizon_sec=8.0,
                    corridor_key="default",
                    safe_window_sec=8.0,
                    invalidation={"digest_hash": digest.digest_hash},
                )
                
                # 生成 Advisory
                meta["advisory"] = Advisory(
                    type=AdvisoryType.DEESCALATE,
                    priority=AdvisoryPriority.P2,
                    time_to_impact_sec=0.0,
                    impact_range_m=0.0,
                    confidence=0.6,
                    reason_code="stable_scene",
                )

        # ----------------------------
        # 2. 决策冗余抑制
        # ----------------------------
        if (
            state == "STABLE"
            and decision_type == self.last_decision_type
            and meta["effective_heartbeat"] > base_heartbeat
        ):
            meta["b2_reason"] = "redundant_decision_suppressed"
            meta["b2_applied"] = True
            return False, meta

        # ----------------------------
        # 3. 正常放行
        # ----------------------------
        self.last_decision_type = decision_type
        return True, meta
