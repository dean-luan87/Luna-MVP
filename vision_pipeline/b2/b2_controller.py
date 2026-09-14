"""
B2 Controller (v0.2) - 未来世界预演层

B2 v0.2 工程目标：
1. 在 不影响现有 C / pipeline 稳定性 的前提下，引入 B2 v0.2 = 未来世界预演层
2. 不控制 C、不改变 pipeline 行为：只提供"上帝视角信息包"
3. 可观测、可回放、可验证：日志里可还原触发原因、输出内容、频率

关键工程约束：
- B2 不允许修改 C 状态
- B2 不允许同步阻塞 pipeline
- B2 允许丢帧、允许低频
- B2 不做语义判断
"""

import time
import uuid
from typing import Optional, Dict, Any
from .b2_config import (
    B2_DIGEST_DELTA_THRESHOLD,
    B2_MAX_SILENCE_SEC,
    B2_LOG_INTERVAL_SEC,
)
from .b2_types import B2Output
from .b2_digest import compute_world_digest, digest_delta
from .b2_corridor import build_task_corridor
from .b2_preview import run_preview

# B2 v0.2 新增模块
from .b2_world_accumulator import WorldAccumulator
from .b2_task_corridor_builder import TaskCorridorBuilder
from .b2_future_simulator import FutureSimulator, FutureWorld
from .b2_advisory_generator import B2AdvisoryGenerator


class B2Controller:
    """
    B2 Controller v0.2
    
    核心职责：
    - 触发判定（INIT / WORLD_CHANGE / TTL_EXPIRE）
    - 节律控制（避免日志刷屏）
    - 未来世界预演（v0.2 新增）
    - 产出 B2Output
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化 B2 Controller
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        
        # v0.1 保留的字段
        self._last_digest = None
        self._last_output_ts = 0.0
        self._last_log_ts = 0.0
        
        # v0.2 新增模块
        self.world_accumulator = WorldAccumulator(self.config)
        self.task_corridor_builder = TaskCorridorBuilder(self.config)
        self.future_simulator = FutureSimulator(self.config)
        self.advisory_generator = B2AdvisoryGenerator(self.config)
    
    def observe(
        self,
        observe_input: Optional[Dict[str, Any]] = None,
        world_snapshot: Optional[Dict[str, Any]] = None,
        navigation_result: Optional[Any] = None,
        modeling_result: Optional[Any] = None,
    ) -> Optional[B2Output]:
        """
        B2 主入口：观察并产出输出（v0.2 支持新接口）
        
        Args:
            observe_input: v0.1 兼容接口（可选）
            world_snapshot: v0.2 世界快照（可选），包含：
                - world_update: 世界更新字典
                - ego_pose: 自位姿
                - objects: 对象列表
                - timestamp: 时间戳
            navigation_result: 导航结果（可选）
            modeling_result: 建模结果（可选）
        
        Returns:
            B2Output 或 None（如果不需要产出）
        """
        now = time.time()
        
        # v0.2 新接口：优先使用 world_snapshot
        if world_snapshot is not None:
            return self._observe_v02(world_snapshot, navigation_result, modeling_result, now)
        
        # v0.1 兼容接口
        if observe_input is not None:
            return self._observe_v01(observe_input, now)
        
        return None
    
    def _observe_v01(self, observe_input: Dict[str, Any], now: float) -> Optional[B2Output]:
        """v0.1 兼容接口"""
        # 计算世界摘要
        wu = observe_input.get("world_update", {}) or {}
        digest = compute_world_digest(wu)
        delta = digest_delta(digest, self._last_digest)
        self._last_digest = digest
        
        # 判断触发原因
        trigger_reason = None
        if self._last_output_ts == 0.0:
            trigger_reason = "INIT"
        elif delta >= B2_DIGEST_DELTA_THRESHOLD:
            trigger_reason = "WORLD_CHANGE"
        elif (now - self._last_output_ts) >= B2_MAX_SILENCE_SEC:
            trigger_reason = "TTL_EXPIRE"
        
        # 如果不需要触发，返回 None
        if trigger_reason is None:
            return None
        
        # 构建任务走廊
        corridor = build_task_corridor(observe_input)
        
        # 运行预演
        fb, advisories, confidence = run_preview(corridor, observe_input)
        
        # 构造输出
        out = B2Output(
            ts=now,
            b2_run_id=str(uuid.uuid4()),
            trigger_reason=trigger_reason,
            future_buffer=fb,
            advisories=advisories,
            confidence=confidence,
            metrics={
                "digest_delta": delta,
                "digest": list(digest),
            },
        )
        
        self._last_output_ts = now
        return out
    
    def _observe_v02(
        self,
        world_snapshot: Dict[str, Any],
        navigation_result: Optional[Any],
        modeling_result: Optional[Any],
        now: float,
    ) -> Optional[B2Output]:
        """
        v0.2 新接口：未来世界预演
        
        Args:
            world_snapshot: 世界快照
            navigation_result: 导航结果
            modeling_result: 建模结果
            now: 当前时间戳
        
        Returns:
            B2Output 或 None
        """
        # 判断是否应该运行（v0.2：基于世界稳定性）
        if not self._should_run_v02(world_snapshot, now):
            return None
        
        # 更新世界累积器
        world_stable = self.world_accumulator.update(world_snapshot)
        
        # 构建任务走廊
        ego_pose = world_snapshot.get("ego_pose", {})
        route = navigation_result.route if navigation_result and hasattr(navigation_result, "route") else None
        corridor = self.task_corridor_builder.build(ego_pose, route)
        
        # 运行未来预演
        future_world = self.future_simulator.simulate_future(
            world_snapshot,
            corridor,
            horizon_sec=8.0,
        )
        
        # 生成建议
        advisory = self.advisory_generator.generate_advisory(future_world)
        
        if advisory is None:
            return None
        
        # 构造 B2Output（v0.2 格式）
        from .b2_types import FutureSegmentBuffer, ConfidenceReport
        
        # 将 potential_intersections 转为 ImpactEvent
        impact_events = []
        for intersection in future_world.potential_intersections:
            impact_events.append({
                "event_id": intersection.get("event_id", "unknown"),
                "event_type": "future_conflict",
                "affects_corridor": True,
                "risk_level": 0.7,
                "time_to_impact_sec": intersection.get("time_sec"),
                "meta": intersection,
            })
        
        # 构建 FutureBuffer
        future_buffer = FutureSegmentBuffer(
            horizon_sec=future_world.horizon_sec,
            corridor_id=corridor.corridor_id,
            predicted_conflicts=[],  # 简化：暂时为空
            safe_window_sec=None if future_world.potential_intersections else future_world.horizon_sec,
            risk_window_sec=min(
                [i.get("time_sec", future_world.horizon_sec) for i in future_world.potential_intersections],
                default=None
            ) if future_world.potential_intersections else None,
        )
        
        # 构建置信报告
        confidence = ConfidenceReport(
            world_observability=0.8,
            model_dependency=0.3,
            corridor_certainty=corridor.confidence,
            overall=0.75,
        )
        
        # 判断触发原因
        trigger_reason = "WORLD_CHANGE" if not world_stable else "TTL_EXPIRE"
        if self._last_output_ts == 0.0:
            trigger_reason = "INIT"
        
        out = B2Output(
            ts=now,
            b2_run_id=str(uuid.uuid4()),
            trigger_reason=trigger_reason,
            future_buffer=future_buffer,
            advisories=[advisory],
            confidence=confidence,
            metrics={
                "world_stable": world_stable,
                "impact_count": len(future_world.potential_intersections),
                "horizon_sec": future_world.horizon_sec,
            },
        )
        
        self._last_output_ts = now
        return out
    
    def _should_run_v02(self, world_snapshot: Dict[str, Any], now: float) -> bool:
        """
        判断是否应该运行 B2 v0.2（基于世界稳定性）
        
        Args:
            world_snapshot: 世界快照
            now: 当前时间戳
        
        Returns:
            bool: 是否应该运行
        """
        # 首次运行
        if self._last_output_ts == 0.0:
            return True
        
        # 检查时间间隔（避免过于频繁）
        if (now - self._last_output_ts) < 2.0:  # 最小间隔 2 秒
            return False
        
        # 检查世界是否稳定（如果稳定，可以降低频率）
        # 这里简化：总是运行（实际可以根据 world_stable 调整）
        return True
    
    def should_log(self, ts: float) -> bool:
        """
        判断是否应该记录日志（防止 B2 日志刷屏）
        
        Args:
            ts: 当前时间戳
        
        Returns:
            bool: 是否应该记录日志
        """
        if (ts - self._last_log_ts) >= B2_LOG_INTERVAL_SEC:
            self._last_log_ts = ts
            return True
        return False
