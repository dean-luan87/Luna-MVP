"""
B2 Controller v0.2 - 节律 + TTL（B2 的核心行为特征）

职责：
- 触发判定（INIT / WORLD_CHANGE / TTL_EXPIRE）
- 节律控制（避免日志刷屏）
- 未来世界预演（v0.2 新增）
- 产出 B2Advisory
"""

import time
import math
from typing import Optional, Any
from .world_accumulator_v02 import WorldAccumulator
from .future_simulator_v02 import FutureSimulator
from .advisory_generator_v02 import B2AdvisoryGenerator
from .task_corridor_v02 import TaskCorridor
from .world_snapshot import WorldSnapshot
from .b2_types_v02 import B2Advisory
from .cache_v02 import FutureCache
# B2 v0.2 Part 1/2/3: 新增模块
from .future_simulator_v02 import FutureSimulator as FutureSimulatorV02  # Part 1: 新的预演器
from .future_simulator_input import FutureSimulatorInput, DynamicObject, StaticRegion
from .future_simulation_result import FutureSimulationResult
from .advisory_value_scorer import AdvisoryValueScorer
from .future_scene_cache import FutureSceneCache
# B2 v0.2 Part 2: Advisory Value System
from .advisory_value import AdvisoryValueSystem, Advisory
from .dynamic_ttl_manager import DynamicTTLManager
from .world_signature import WorldSignature
from .world_signature_builder import WorldSignatureBuilder
from .advisory_cache import AdvisoryCache


class B2Controller:
    """
    B2 Controller v0.2
    
    核心职责：
    - 触发判定（INIT / WORLD_CHANGE / TTL_EXPIRE）
    - 节律控制（避免日志刷屏）
    - 未来世界预演（v0.2 新增）
    - 产出 B2Advisory
    """
    
    def __init__(
        self,
        ttl_sec: float = 10.0,
        min_interval_sec: float = 3.0,
        horizon_sec: float = 8.0,
        corridor_width_m: float = 1.2,
    ):
        """
        初始化 B2 Controller
        
        Args:
            ttl_sec: TTL 过期时间（秒）
            min_interval_sec: 最小输出间隔（秒）
            horizon_sec: 预演时间窗口（秒）
            corridor_width_m: 走廊宽度（米）
        """
        self.ttl_sec = ttl_sec
        self.min_interval_sec = min_interval_sec
        self.horizon_sec = horizon_sec
        self.corridor_width_m = corridor_width_m
        
        # v0.2 新增模块
        self.acc = WorldAccumulator()
        self.sim = FutureSimulator(horizon_sec=horizon_sec)  # 旧版（保留兼容）
        self.gen = B2AdvisoryGenerator()
        self.cache = FutureCache(ttl_sec=ttl_sec)  # 未来剧本缓存
        
        # B2 v0.2 Part 1/2/3: 新增模块
        self.future_sim_v02 = FutureSimulatorV02(horizon_sec=horizon_sec)  # Part 1: 多未来分支预演
        self.value_scorer = AdvisoryValueScorer()  # Part 2: 信息价值分级（旧版，保留兼容）
        self.scene_cache = FutureSceneCache(ttl_sec=ttl_sec)  # Part 3: 未来场景缓存
        # B2 v0.2 Part 2: Advisory Value System（新版）
        self.advisory_value_system = AdvisoryValueSystem()
        
        # B2 v0.2 C阶段：动态 TTL 管理器（决策节律动态拉长）
        self.dynamic_ttl = DynamicTTLManager(
            base_ttl_sec=ttl_sec,
            min_ttl_sec=3.0,  # 复杂路口：3s
            max_ttl_sec=20.0,  # 安全直路：20s
        )
        
        # B2 v0.2 缓存逻辑：第三层 - 建议缓存
        self.advisory_cache = AdvisoryCache(ttl_sec=15.0)  # Advisory TTL 比 Future TTL 更长
        
        # 内部状态
        self._last_emit_ts: Optional[float] = None
        self._last_sig: Optional[tuple] = None
        self._last_world_signature: Optional[WorldSignature] = None
    
    def _world_sig(self, world_snapshot: WorldSnapshot) -> tuple:
        """
        计算世界签名（v0.2：粗粒度签名）
        
        后续可替换为更强的 hash/embedding
        
        Args:
            world_snapshot: 世界快照
        
        Returns:
            tuple: 世界签名
        """
        return (len(world_snapshot.objects), len(world_snapshot.texts))
    
    def _build_corridor(
        self,
        world_snapshot: WorldSnapshot,
        navigation_route: Optional[Any] = None,
    ) -> TaskCorridor:
        """
        构建任务走廊
        
        Args:
            world_snapshot: 世界快照
            navigation_route: 导航路径（可选）
        
        Returns:
            TaskCorridor: 任务走廊
        """
        # 如果有导航任务，使用 route
        if navigation_route and hasattr(navigation_route, "points") and navigation_route.points:
            pts = navigation_route.points
            return TaskCorridor(
                mode="ROUTE",
                points=pts,
                width_m=self.corridor_width_m,
                horizon_sec=self.horizon_sec,
                meta={}
            )
        
        # A5.6: 没有任务链时，B2 怎么办？
        # 规则：如果没有 Navigation 任务链：
        # → 用 Ego heading + speed
        # → 构造一个"默认前进 corridor"
        # → 长度 = speed × horizon_sec
        
        # 构造默认前进 corridor（基于 heading 和 speed）
        import math
        heading_rad = math.radians(world_snapshot.ego.heading)
        speed = world_snapshot.ego.speed or 1.0  # 默认 1.0 m/s
        corridor_length = speed * self.horizon_sec
        
        # 生成简单的 polyline（从当前位置向前延伸）
        points = []
        if world_snapshot.ego.pos and len(world_snapshot.ego.pos) >= 2:
            start_pos = world_snapshot.ego.pos
            # 生成几个点（简化：直线）
            for i in range(5):
                t = i / 4.0  # 0.0 到 1.0
                dx = corridor_length * t * math.cos(heading_rad)
                dy = corridor_length * t * math.sin(heading_rad)
                points.append([start_pos[0] + dx, start_pos[1] + dy])
        else:
            # 如果没有位置信息，points 为空（但 B2 仍然能工作）
            points = []
        
        return TaskCorridor(
            mode="HEADING",
            points=points,
            width_m=self.corridor_width_m,
            horizon_sec=self.horizon_sec,
            meta={
                "heading": world_snapshot.ego.heading,
                "speed": speed,
                "corridor_length": corridor_length,
            }
        )
    
    def observe(
        self,
        world_snapshot: WorldSnapshot,
        navigation_result: Optional[Any] = None,
        modeling_result: Optional[Any] = None,
    ) -> Optional[B2Advisory]:
        """
        B2 主入口：观察并产出输出
        
        Args:
            world_snapshot: 世界快照
            navigation_result: 导航结果（可选）
            modeling_result: 建模结果（可选）
        
        Returns:
            B2Advisory 或 None（如果不需要产出）
        """
        now = world_snapshot.timestamp if world_snapshot else time.time()
        
        # 检查缓存：是否应该运行
        if not self.cache.should_run(now):
            # 返回缓存的 Advisory（如果有）
            return self.cache.get_last_advisory()
        
        # 检查最小间隔
        if self._last_emit_ts is not None and (now - self._last_emit_ts) < self.min_interval_sec:
            return None
        
        # 计算世界签名
        sig = self._world_sig(world_snapshot)
        world_changed = (self._last_sig is not None and sig != self._last_sig)
        ttl_expired = (self._last_emit_ts is None) or ((now - self._last_emit_ts) >= self.ttl_sec)
        
        # 判断触发原因
        if self._last_emit_ts is None:
            trigger = "INIT"
        elif world_changed:
            trigger = "WORLD_CHANGE"
        elif ttl_expired:
            trigger = "TTL_EXPIRE"
        else:
            return None
        
        # 构建任务走廊
        corridor = self._build_corridor(
            world_snapshot,
            navigation_route=getattr(navigation_result, "route", None) if navigation_result else None
        )
        
        # 更新世界累积器（先占位：后续稳定度可影响 ttl/horizon）
        _ = self.acc.update(world_snapshot)
        
        # B2 v0.2 Part 1/2/3: 多未来分支预演 + 价值分级 + 场景缓存
        # ==========================================================
        # B2 v0.2 缓存逻辑：完整决策流
        # ==========================================================
        
        # ==========================================================
        # Task 4.1: B2Controller 新流程（只加壳，不动核）
        # ==========================================================
        
        # Step 1: 生成 WorldSignature（第一层）
        current_world_signature = WorldSignatureBuilder.build(
            world_snapshot=world_snapshot,
            navigation_result=navigation_result,
        )
        # Task 1.3: WorldSignature 日志
        print(f"[B2] world_signature={current_world_signature.digest()}")
        
        # Step 2: FutureSimulation Cache（第二层）
        # Task 2.2: get_or_compute 接口
        def compute_future():
            input_data = self._build_future_simulator_input(
                world_snapshot=world_snapshot,
                navigation_result=navigation_result,
                modeling_result=modeling_result,
                timestamp=now,
            )
            return self.future_sim_v02.run(input_data)
        
        sim_result, reused = self.scene_cache.get_or_compute(
            world_signature=current_world_signature,
            compute_fn=compute_future,
            current_ts=now,
        )
        
        # Step 3: Part 2 - 使用 AdvisoryValueSystem 生成 Advisory
        # P1-9: B2 v0.2 的最小策略（定死）
        # if sim_result.collisions or sim_result.path_overlap:
        #     emit PREWARN
        # else:
        #     emit DEESCALATE
        
        # 判断是否有任务链
        has_task_chain = (navigation_result is not None and 
                         hasattr(navigation_result, 'route') and 
                         navigation_result.route is not None)
        
        # 使用 AdvisoryValueSystem 生成 Advisory（Part 2）
        advisory_obj = self.advisory_value_system.generate_advisory(
            sim_result=sim_result,
            has_task_chain=has_task_chain,
            c_state=None,  # 只读，不影响 C
        )
        
        # 转换为 B2Advisory（兼容现有接口）
        advisory = self._advisory_to_b2advisory(
            advisory_obj=advisory_obj,
            sim_result=sim_result,
            trigger_reason=trigger,
        )
        
        # Step 3: AdvisoryCache（第三层）
        # Task 3.2: Advisory 抑制逻辑
        should_suppress, cache_age = self.advisory_cache.should_suppress(
            advisory, current_world_signature, now
        )
        
        if should_suppress:
            # Task 3.3: 抑制日志（非常重要）
            print(f"[B2] advisory suppressed (same as last, age={cache_age:.1f}s)")
            # 仍然更新内部状态，但不输出
            self._last_emit_ts = now
            self._last_sig = sig
            self._last_world_signature = current_world_signature
            return None  # 不输出
        
        # 需要输出，更新 AdvisoryCache
        self.advisory_cache.update(advisory, current_world_signature, now)
        
        # C阶段：根据预演结果计算动态 TTL
        has_task_chain = (navigation_result is not None and 
                         hasattr(navigation_result, 'route') and 
                         navigation_result.route is not None)
        dynamic_ttl = self.dynamic_ttl.compute_ttl(
            sim_result=sim_result,
            has_task_chain=has_task_chain,
        )
        # 更新缓存的动态 TTL
        self.cache.set_dynamic_ttl(dynamic_ttl)
        
        # 更新内部状态
        self._last_emit_ts = now
        self._last_sig = sig
        self._last_world_signature = current_world_signature
        
        # 更新缓存
        corridor_sig = str(corridor.points) if corridor.points else None
        objects_count = len(world_snapshot.objects) if world_snapshot else 0
        self.cache.update(
            timestamp=now,
            advisory=advisory,
            corridor_sig=corridor_sig,
            objects_count=objects_count,
        )
        
        # 将动态 TTL 记录到 advisory meta（用于日志分析）
        advisory.meta["dynamic_ttl_sec"] = dynamic_ttl
        
        # P1-10: 日志与回放
        # 每次 B2 输出必须记录
        log_data = {
            "trigger": trigger,
            "horizon": sim_result.horizon_sec,
            "collisions": [(c.obj_id, c.t_sec) for c in sim_result.collisions],
            "path_overlap": sim_result.path_overlap,
            "region_enter": [(r.region_id, r.t_sec) for r in sim_result.region_enter],
            "advisory_type": advisory.advisory_type,
            "confidence": advisory.confidence,
        }
        # 将日志数据存入 meta（供后续分析）
        advisory.meta["log_data"] = log_data
        
        return advisory
    
    def _build_future_simulator_input(
        self,
        world_snapshot: WorldSnapshot,
        navigation_result: Optional[Any],
        modeling_result: Optional[Any],
        timestamp: float,
    ) -> FutureSimulatorInput:
        """
        构建 FutureSimulatorInput（来自真实 pipeline）
        
        Args:
            world_snapshot: 世界快照
            navigation_result: 导航结果
            modeling_result: 建模结果
            timestamp: 时间戳
        
        Returns:
            FutureSimulatorInput: 预演输入
        """
        # 提取 ego 信息
        ego_path = None
        if navigation_result and hasattr(navigation_result, 'route'):
            route = navigation_result.route
            if route and hasattr(route, 'points') and route.points:
                ego_path = route.points
        
        ego_velocity = [0.0, 0.0]
        ego_position = [0.0, 0.0]
        ego_heading = 0.0
        if world_snapshot.ego:
            # EgoPose 只有 speed，没有 vel，需要从 speed 和 heading 计算 velocity
            speed = world_snapshot.ego.speed or 0.0
            heading_rad = math.radians(world_snapshot.ego.heading or 0.0)
            ego_velocity = [speed * math.cos(heading_rad), speed * math.sin(heading_rad)]
            
            if world_snapshot.ego.pos and len(world_snapshot.ego.pos) >= 2:
                ego_position = world_snapshot.ego.pos
            ego_heading = world_snapshot.ego.heading or 0.0
        
        # 提取动态对象
        dynamic_objects = []
        for obj in world_snapshot.objects:
            if obj.bbox and len(obj.bbox) >= 4:
                vel = obj.vel if (obj.vel and len(obj.vel) >= 2) else [0.0, 0.0]
                confidence = obj.extra.get("confidence", 0.5) if obj.extra else 0.5
                dynamic_objects.append(DynamicObject(
                    obj_id=obj.obj_id,
                    bbox=obj.bbox,
                    velocity=vel,
                    confidence=confidence,
                    meta={"cls": obj.cls} if obj.cls else {},
                ))
        
        # 提取静态区域（简化：暂时为空，后续可从 modeling_result 提取）
        static_regions = []
        
        return FutureSimulatorInput(
            ego_path=ego_path,
            ego_velocity=ego_velocity,
            ego_position=ego_position,
            ego_heading=ego_heading,
            dynamic_objects=dynamic_objects,
            static_regions=static_regions,
            timestamp=timestamp,
        )
    
    def _make_advisory_from_sim_result(
        self,
        sim_result: FutureSimulationResult,
        advisory_type: str,
        value_score: Any,  # AdvisoryValueScore
        trigger_reason: str,
    ) -> B2Advisory:
        """
        从预演结果生成 Advisory
        
        Args:
            sim_result: 未来预演结果
            advisory_type: Advisory 类型
            value_score: 价值评分
            trigger_reason: 触发原因
        
        Returns:
            B2Advisory: B2 建议
        """
        # 计算 horizon（最早事件时间，或默认 horizon）
        horizon = sim_result.horizon_sec
        if sim_result.collisions:
            horizon = min(horizon, min(c.t_sec for c in sim_result.collisions))
        if sim_result.region_enter:
            horizon = min(horizon, min(r.t_sec for r in sim_result.region_enter))
        
        # 构建 impacts（从 collisions 转换）
        impacts = []
        for coll in sim_result.collisions:
            from .b2_types_v02 import ImpactEvent
            impacts.append(ImpactEvent(
                obj_id=coll.obj_id,
                t_sec=coll.t_sec,
                score=coll.overlap_ratio,
                ttc=coll.t_sec,
                overlap_ratio=coll.overlap_ratio,
                obj_confidence=coll.meta.get("confidence", 0.5),
                meta={}
            ))
        
        # 构建 suggestion
        suggestion = {
            "risk_weight": 1.3 if advisory_type == "PREWARN" else 0.7,
            "speech_cooldown_factor": 0.8 if advisory_type == "PREWARN" else 1.5,
        }
        if advisory_type == "PREWARN":
            suggestion["attention_raise"] = True
            if sim_result.collisions:
                suggestion["earliest_impact_time"] = min(c.t_sec for c in sim_result.collisions)
        
        return B2Advisory(
            advisory_type=advisory_type,
            horizon_sec=horizon,
            confidence=value_score.value,  # 使用价值评分作为 confidence
            trigger_reason=trigger_reason,
            impacts=impacts,
            suggestion=suggestion,
            meta={
                "ttl_sec": 10.0,
                "timestamp": time.time(),
                "level": value_score.level,  # MEDIUM / HIGH
                "value_score": value_score.value,
                "reasons": value_score.reasons,
            }
        )
    
    def _advisory_to_b2advisory(
        self,
        advisory_obj: Advisory,
        sim_result: FutureSimulationResult,
        trigger_reason: str,
    ) -> B2Advisory:
        """
        将 Advisory 转换为 B2Advisory（兼容现有接口）
        
        Args:
            advisory_obj: Advisory 对象
            sim_result: 未来预演结果
            trigger_reason: 触发原因
        
        Returns:
            B2Advisory: B2 建议
        """
        # 构建 impacts（从 collisions 转换）
        impacts = []
        for coll in sim_result.collisions:
            from .b2_types_v02 import ImpactEvent
            impacts.append(ImpactEvent(
                obj_id=coll.obj_id,
                t_sec=coll.t_sec,
                score=coll.overlap_ratio,
                ttc=coll.t_sec,
                overlap_ratio=coll.overlap_ratio,
                obj_confidence=coll.meta.get("confidence", 0.5),
                meta={}
            ))
        
        # 构建 suggestion
        suggestion = {
            "risk_weight": 1.3 if advisory_obj.type == "PREWARN" else 0.7,
            "speech_cooldown_factor": 0.8 if advisory_obj.type == "PREWARN" else 1.5,
        }
        if advisory_obj.type == "PREWARN":
            suggestion["attention_raise"] = True
            if sim_result.collisions:
                suggestion["earliest_impact_time"] = min(c.t_sec for c in sim_result.collisions)
        
        # 计算 horizon
        horizon = sim_result.horizon_sec
        if sim_result.collisions:
            horizon = min(horizon, min(c.t_sec for c in sim_result.collisions))
        if sim_result.region_enter:
            horizon = min(horizon, min(r.t_sec for r in sim_result.region_enter))
        
        return B2Advisory(
            advisory_type=advisory_obj.type,  # PREWARN / DEESCALATE / NEUTRAL
            horizon_sec=horizon,
            confidence=advisory_obj.confidence,
            trigger_reason=trigger_reason,
            impacts=impacts,
            suggestion=suggestion,
            meta={
                "ttl_sec": advisory_obj.ttl_sec,
                "timestamp": time.time(),
                "payload": advisory_obj.payload,  # Part 2: 事实描述
            }
        )

