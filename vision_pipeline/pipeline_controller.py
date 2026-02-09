# -*- coding: utf-8 -*-
"""
Vision Pipeline Controller（视觉流水线控制器）

职责：
- 统一管理视觉流水线的完整流程
- 协调 LV2-LV7 的执行
- 切断视觉输入 → core 的直通路径

设计原则：
- 所有视觉结果必须先进入 vision_pipeline
- core/world_model 只能接收来自 modeling_executor 的候选或 UserReportRouter 的用户反馈
"""

import time
from typing import Optional, Dict, Any, Tuple
import numpy as np
import cv2

from .lv2_quality_gate import QualityGate, QualityResult
from .lv3_semantic_router import SemanticRouter, RouteResult
from .lv4_executors import NavigationExecutor, ModelingExecutor

# v1.8.5 Phase B Step 1.1: CameraHandler 迁移到 PipelineController
from utils.camera_handler import CameraHandler

# C1: Continuous Vision Controller（连续视觉调度中台）
from c1_controller.c1_controller import C1Controller
from c1_controller.c1_types import C1Input
from c1_controller.c1_governor import FrameRateGovernor
from c1_controller.c1_logger import C1Logger
from c1_controller.c1_metrics import C1Metrics

# Phase C1: Shadow Mode（只观察，不控制）
from vision_pipeline.c1_controller.c1_shadow_controller import C1ShadowController
from vision_pipeline.c1_controller.c1_config import C1_MODE_SHADOW_ONLY

# Phase C1 Active Mode v0.2: 状态机
from vision_pipeline.c1_controller.c1_state_machine import C1StateMachine, C1State, OcclusionState
from vision_pipeline.c1_controller.c1_logger_v02 import C1LoggerV02
from vision_pipeline.c1_controller.c1_decision_logger import C1DecisionLogger
from vision_pipeline.c1_controller.c1_active_controller import C1ActiveController

# 被动 ROI v0: motion → roi_count（复杂度信号，不进 C1/C2）
from vision_perception_b1.passive_roi import compute_passive_roi_count
# Path v0 / Branch v0: optical flow 方向一致性 → path_instability, branch_load
from vision_perception_b1.passive_path import compute_path_and_branch

# B2 v0.1: 上帝视角的大场景观察器 + 未来 5-10 秒任务链预演器
from vision_pipeline.b2.b2_controller import B2Controller
from vision_pipeline.b2.b2_integration import SharedBlackboard
from vision_pipeline.b2.b2_world_update_builder import build_b2_world_update, build_b2_impact_events
from vision_pipeline.b2.b2_config import B2_V01_ENABLED


class PipelineController:
    """
    视觉流水线控制器（最小可跑闭环）
    
    数据流：
    Camera → LV2 → LV3 → LV4.1 (实时) / LV4.2 (异步) → LV5 / LV6
    
    关键原则：
    - 实时链路：LV2 → LV3 → LV4.1 → LV5
    - 异步链路：LV3 → LV4.2 → LV6
    - 任何模块不得逆向调用上游
    - 只有 LV4.1 / 上层控制中心 可以请求重新观察
    
    ⚠️ v1.8.5 Phase B: 最小闭环
    
    今天的目标不是"功能完整"，而是：
    - 所有视觉入口开始走同一条管道
    - 后续所有能力都往这里挂
    
    最小结构：
    Camera → LV2 → LV3 → LV4.1 → Decision
    """
    
    def __init__(
        self,
        quality_gate: Optional[QualityGate] = None,
        semantic_router: Optional[SemanticRouter] = None,
        navigation_executor: Optional[NavigationExecutor] = None,
        modeling_executor: Optional[ModelingExecutor] = None,
        camera_handler: Optional[CameraHandler] = None,
        video_path: Optional[str] = None,
    ):
        """
        初始化视觉流水线控制器

        Args:
            quality_gate: 质量过滤层实例（可选，如果为 None 则创建默认实例）
            semantic_router: 语义路由器实例（可选，如果为 None 则创建默认实例）
            navigation_executor: 导航执行器实例（可选）
            modeling_executor: 世界建模执行器实例（可选）
            camera_handler: 摄像头处理器实例（可选，如果为 None 则创建默认实例）
            video_path: 视频文件路径（可选，指定时从视频读取而非摄像头）
        """
        self.quality_gate = quality_gate or QualityGate()
        self.semantic_router = semantic_router or SemanticRouter()
        self.navigation_executor = navigation_executor
        self.modeling_executor = modeling_executor
        # v1.8.5 Phase B Step 1.1: CameraHandler 迁移到 PipelineController
        if camera_handler is not None:
            self.camera_handler = camera_handler
        elif video_path:
            self.camera_handler = CameraHandler(video_path=video_path)
        else:
            self.camera_handler = CameraHandler()
        self._last_frame_gray: Optional[np.ndarray] = None
        self._last_frame_context: Dict[str, Any] = {}
        self.occlusion_ratio: float = 0.0
        self.perception_state: str = "DEGRADED"
        self.view_confidence: float = 1.0
        self.frame_quality: str = "INVALID"
        self._last_frame_ts: Optional[float] = None
        self._motion_ema: Optional[float] = None
        self.motion_instability: float = 0.0
        self.roi_count: int = 0  # 被动 ROI v0：motion 空间分布计数
        self.path_instability: float = 0.0  # Path v0：光流方向一致性
        self.branch_load: float = 0.0  # Branch v0：有效运动方向数量密度
        self._frame_id = 0
        self._continuity = {
            "valid_streak": 0,
            "invalid_streak": 0,
            "degraded_streak": 0,
            "low_diff_streak": 0,
        }
        
        # ✅ C1 控制器（新增）
        # C1 是有状态的（state machine），不能每帧 new
        # 生命周期和 PipelineController 绑定是对的
        self.c1_controller = C1Controller()
        
        # ✅ 帧率控制器（新增）
        # 根据 C1.target_fps 控制是否允许处理当前帧
        self.frame_governor = FrameRateGovernor()
        
        # ✅ C1 日志记录器（可选）
        self.c1_logger = C1Logger()
        
        # ✅ C1 效能评估器（可选）
        self.c1_metrics = C1Metrics()
        
        # ✅ Phase C1: Shadow Controller（只观察，不控制）
        # 如果 C1_MODE_SHADOW_ONLY=True，则使用 Shadow Controller
        # 否则使用正常的 C1Controller
        if C1_MODE_SHADOW_ONLY:
            self.c1_shadow = C1ShadowController()
        else:
            self.c1_shadow = None
        
        # ✅ Phase C1 Active Mode v0.2: Active Controller（稳定版）
        if not C1_MODE_SHADOW_ONLY:
            # 创建 C1 决策日志记录器（用于 log_frequency 验证）
            self.c1_decision_logger = C1DecisionLogger()
            # 创建 C1 Active Controller（包含状态机和节律闸门）
            self.c1_active_controller = C1ActiveController(
                decision_logger=self.c1_decision_logger,
            )
            # 保留状态机引用（用于兼容）
            self.c1_state_machine = self.c1_active_controller.state_machine
            self.c1_logger_v02 = C1LoggerV02()  # v0.2 结构化日志
        else:
            self.c1_decision_logger = None
            self.c1_active_controller = None
            self.c1_state_machine = None
            self.c1_logger_v02 = None
        
        # ✅ B2 v0.1: 上帝视角的大场景观察器 + 未来 5-10 秒任务链预演器
        # B2 不控制 C，只提供信息与置信度
        if B2_V01_ENABLED:
            self.b2_controller = B2Controller()
            self.b2_blackboard = SharedBlackboard()
        else:
            self.b2_controller = None
            self.b2_blackboard = None
        
        # ✅ B2 v0.2: 未来世界预演层（旁路模式，不影响现有 C）
        # 优先使用新的 B2V02（缓存与节律接管版）
        self.b2_v02 = None
        self.b2_controller_v02 = None
        self.b2_v02_enabled = False
        self.advisory_queue = None
        self._last_b2_advisory = None
        
        try:
            # 尝试导入新的 B2V02
            from vision_pipeline.b2.b2_v02 import B2V02
            self.b2_v02 = B2V02(debug_tick_log=True)
            self.b2_v02_enabled = True
            print("[Pipeline] B2 v0.2 (缓存与节律接管版) 已启用")
        except ImportError:
            # Fallback: 使用旧的 B2ControllerV02
            try:
                from vision_pipeline.b2.b2_controller_v02 import B2Controller as B2ControllerV02
                from vision_pipeline.b2.world_snapshot import WorldSnapshot, EgoPose, WorldObject
                from vision_pipeline.b2.advisory_queue import AdvisoryQueue
                self.b2_controller_v02 = B2ControllerV02()
                self.b2_v02_enabled = True
                # B2 → C 对接方案：Advisory Queue
                self.advisory_queue = AdvisoryQueue(max_active=3)  # 防爆炸规则
                print("[Pipeline] B2 v0.2 (旧版) 已启用")
            except Exception as e:
                print(f"[Pipeline] B2 v0.2 导入失败: {e}")
                self.b2_v02_enabled = False
        
        # ✅ B2 v0.3: 未来窗口情报（8s horizon，稀疏输出）
        # Part 0: Feature Flag 与回滚开关
        self.b2_v03 = None
        self.b2_v03_enabled = False
        
        # v0.3 和 v0.2 互斥（避免双跑污染日志与统计）
        # 方案 A: 如果 v0.3 启用，强制禁用 v0.2
        try:
            from vision_pipeline.b2.v03.b2_v03 import B2V03
            self.b2_v03 = B2V03(enable_debug=True)
            self.b2_v03_enabled = True
            # 强制禁用 v0.2（切断 v0.3 路径对 v0.2 observer 的任何调用）
            if self.b2_v02_enabled:
                print("[Pipeline] B2 v0.3 启用，强制禁用 v0.2（互斥）")
                self.b2_v02_enabled = False
                self.b2_v02 = None
                self.b2_controller_v02 = None
            print("[Pipeline] B2 v0.3 (8s horizon) 已启用")
        except Exception as e:
            print(f"[Pipeline] B2 v0.3 导入失败: {e}，降级为 disabled")
            self.b2_v03_enabled = False
    
    def process_frame(
        self,
        frame: np.ndarray,
        frame_id: Optional[str] = None,
        frame_ts: Optional[float] = None,  # 新增：视频时间轴
        task_state: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        user_position: Optional[Tuple[float, float]] = None,
    ) -> Dict[str, Any]:
        """
        处理单帧图像（主入口）
        
        Args:
            frame: 输入图像帧
            frame_id: 帧 ID（可选）
            task_state: 任务态（可选）
            context: 上下文（可选，包含 scene, map_hint, memory_bias, risk_bias 等）
            user_position: 用户位置（可选，用于风险评估）
        
        Returns:
            Dict[str, Any]: 处理结果，包含：
                - quality_result: QualityResult
                - route_result: RouteResult
                - navigation_result: NavigationResult（如果路由到 navigation）
                - modeling_result: ModelingResult（如果路由到 non_navigation）
        """
        result = {
            "frame_id": frame_id,
            "timestamp": time.time(),
            "b2_recomputed": False,
            "c1_recomputed": False,
        }
        
        # ===============================
        # Phase C1: Active Mode v0.2（状态机 + Protection Mode）
        # ===============================
        # 从 context 中提取 C1 需要的信号（如果 context 为 None 则使用最近帧的缓存）
        if context is None:
            context = self._last_frame_context or {}
        motion_score = context.get("motion_score", 0.0)
        frame_diff_score = context.get("frame_diff_score", 0.0)
        occlusion_state = context.get("occlusion_state", OcclusionState.UNKNOWN)
        scene_class = context.get("privacy_zone", "allow_camera") if context else "allow_camera"
        timestamp = time.time()
        
        # ⚠️ Shadow Mode: 只观察，不执行（用于对比）
        if self.c1_shadow:
            shadow_decisions = self.c1_shadow.observe(
                motion_score=motion_score,
                frame_diff=frame_diff_score,
                scene_class=scene_class,
                timestamp=timestamp,
            )
            result["c1_shadow_decisions"] = shadow_decisions
        
        # ===============================
        # C1 Active Mode v0.2: Active Controller（稳定版）
        # ===============================
        c1_skip_modeling = False  # 默认不跳过
        c1_decision = None
        c1_state_result = None
        
        # A5.2: 获取上一帧的 B2 建议（如果可用）
        # 注意：B2 在当前帧的 modeling_result 之后运行
        # 所以 C1 使用的是上一帧的 B2 建议（这是合理的，因为 B2 是"未来预演"）
        b2_advisory_for_c = getattr(self, "_last_b2_advisory", None)
        
        if not C1_MODE_SHADOW_ONLY and self.c1_active_controller:
            # 使用 C1 Active Controller 观察（节律闸门控制）
            c1_decision = self.c1_active_controller.observe(
                motion_score=motion_score,
                frame_diff=frame_diff_score,
                timestamp=timestamp,
                occlusion_state=occlusion_state,
                scene_class=scene_class,
                b2_advisory=b2_advisory_for_c,  # A5.2: 传递 B2 建议（可选，保留兼容）
                advisory_queue=self.advisory_queue,  # B2 → C 对接方案：Advisory Queue
            )
            
            # 如果产出 decision，使用 decision 的结果
            if c1_decision:
                c1_skip_modeling = not c1_decision.get("allow_modeling", True)
                result["c1_decision"] = c1_decision
                result["c1_skip_modeling"] = c1_skip_modeling
                
                # 构造兼容的 c1_state_result（用于日志）
                c1_state_result = {
                    "state": c1_decision.get("c1_state"),
                    "state_transition": c1_decision.get("state_transition"),
                    "protection_trigger_reason": c1_decision.get("protection_reason"),
                    "protection_remaining_sec": None,  # 如果需要，可以从 state_machine 获取
                }
                result["c1_state_result"] = c1_state_result
                
                if c1_skip_modeling:
                    result["c1_skip_reason"] = c1_decision.get("skip_reason", "unknown")
            else:
                # 没有产出 decision（节律闸门阻止），使用上次的决策状态
                # 使用 should_run_modeling() 作为兜底
                c1_skip_modeling = not self.c1_active_controller.should_run_modeling()
                result["c1_skip_modeling"] = c1_skip_modeling
                if c1_skip_modeling:
                    current_state = self.c1_active_controller.get_current_state()
                    result["c1_skip_reason"] = f"C1 state={current_state.value}"
        else:
            # Shadow Mode: 不执行控制
            decision_latency = 0.0
            current_state = None
        
        # LV2: Quality Gate
        quality_result = self.quality_gate.evaluate(
            frame=frame,
            frame_id=frame_id,
        )
        result["quality_result"] = quality_result
        
        # LV3: Semantic Router（即使质量检查未通过，也进行路由判断）
        route_result = self.semantic_router.route(
            frame_id=frame_id,
            quality_result=quality_result,
            task_state=task_state,
        )
        result["route_result"] = route_result
        
        # 如果质量检查未通过，直接返回（不进入 LV4）
        if not quality_result.passed:
            return result
        
        # 更新语义路由器的任务态
        if task_state:
            self.semantic_router.update_task_state(task_state)
        
        # LV4: 并行执行层
        # v1.8.5 Phase B Step 2.3: 为了支持 QwenVL 生成场景描述，需要同时执行两个 executor
        # 或者至少能够传递数据（objects 从 NavigationExecutor 传递到 ModelingExecutor）
        navigation_result = None
        if route_result.route == "navigation":
            # LV4.1: Navigation Executor（实时链路）
            if self.navigation_executor:
                navigation_result = self.navigation_executor.run(
                    frame=frame,
                    context=context or {},
                    user_position=user_position,
                )
                result["navigation_result"] = navigation_result
        
        # LV4.2: World Modeling Executor（异步链路）
        # Phase C1 Active Mode v0.2: 仅允许 C1 控制是否执行 ModelingExecutor
        # ⚠️ 注意：
        #   - LV2 / LV3 仍然跑
        #   - 只是重计算被暂停
        #   - 世界模型不会被污染
        modeling_result = None
        modeling_executed = False
        
        if C1_MODE_SHADOW_ONLY:
            # Shadow Mode: 正常执行 ModelingExecutor（不受 C1 控制）
            if self.modeling_executor:
                is_navigating = task_state and task_state.get("is_navigating", False)
                objects_for_modeling = None
                if navigation_result and navigation_result.objects:
                    objects_for_modeling = navigation_result.objects
                modeling_result = self.modeling_executor.run(
                    frame=frame,
                    context=context or {},
                    paused=is_navigating,
                    objects=objects_for_modeling,
                )
                modeling_executed = (modeling_result is not None)
        else:
            # Active Mode v0.2: C1 控制是否执行 ModelingExecutor（状态机 + Protection Mode）
            if self.modeling_executor and not c1_skip_modeling:
                is_navigating = task_state and task_state.get("is_navigating", False)
                objects_for_modeling = None
                if navigation_result and navigation_result.objects:
                    objects_for_modeling = navigation_result.objects
                modeling_result = self.modeling_executor.run(
                    frame=frame,
                    context=context or {},
                    paused=is_navigating,
                    objects=objects_for_modeling,
                )
                modeling_executed = (modeling_result is not None)
            else:
                # C1 判断跳过 ModelingExecutor
                modeling_executed = False
                if c1_skip_modeling:
                    result["c1_modeling_skipped"] = True
                    result["c1_modeling_skip_reason"] = f"C1 state={c1_state_result['state'].value if c1_state_result else 'unknown'}"
                    if c1_state_result and c1_state_result.get("protection_trigger_reason"):
                        result["c1_modeling_skip_reason"] += f", protection={c1_state_result['protection_trigger_reason']}"
        result["modeling_result"] = modeling_result
        result["c1_recomputed"] = modeling_executed  # 有效 tick：C1/Modeling 本帧实际执行

        # ===============================
        # B2 v0.3: 未来窗口情报（8s horizon，稀疏输出）
        # ===============================
        # Part 2: 真实输入映射 - 在 nav/modeling 之后调用
        if self.b2_v03_enabled and self.b2_v03 is not None:
            try:
                # 提取 objects（优先从 modeling_result，其次从 navigation_result）
                objects = []
                if modeling_result:
                    if hasattr(modeling_result, "objects") and modeling_result.objects:
                        for obj in modeling_result.objects:
                            if hasattr(obj, "__dict__"):
                                obj_dict = obj.__dict__
                            elif isinstance(obj, dict):
                                obj_dict = obj
                            else:
                                obj_dict = {"class": str(obj)}
                            objects.append(obj_dict)
                elif navigation_result:
                    if hasattr(navigation_result, "objects") and navigation_result.objects:
                        for obj in navigation_result.objects:
                            if hasattr(obj, "__dict__"):
                                obj_dict = obj.__dict__
                            elif isinstance(obj, dict):
                                obj_dict = obj
                            else:
                                obj_dict = {"class": str(obj)}
                            objects.append(obj_dict)
                
                # 提取 texts（从 modeling_result）
                texts = []
                if modeling_result:
                    # 方式 1: 直接从 modeling_result.texts 获取
                    if hasattr(modeling_result, "texts") and modeling_result.texts:
                        texts = modeling_result.texts if isinstance(modeling_result.texts, list) else list(modeling_result.texts)
                    # 方式 2: 从 content_candidates 中提取 raw_texts
                    elif hasattr(modeling_result, "content_candidates") and modeling_result.content_candidates:
                        for candidate in modeling_result.content_candidates:
                            if hasattr(candidate, "raw_texts") and candidate.raw_texts:
                                if isinstance(candidate.raw_texts, list):
                                    texts.extend(candidate.raw_texts)
                                else:
                                    texts.append(candidate.raw_texts)
                            elif hasattr(candidate, "raw_text") and candidate.raw_text:
                                texts.append(candidate.raw_text)
                
                # 构建 perception 字典（B2 v0.3 需要）
                perception = {}
                
                # path 信息（从 navigation_result 或 modeling_result）
                perception["path"] = {}
                if navigation_result:
                    if hasattr(navigation_result, "path_type"):
                        perception["path"]["surface"] = getattr(navigation_result, "path_type", "concrete")
                    if hasattr(navigation_result, "has_path"):
                        perception["path"]["has_path"] = getattr(navigation_result, "has_path", True)
                
                # env 信息（从 modeling_result）
                perception["env"] = {}
                if modeling_result:
                    scene = getattr(modeling_result, "scene_label", None) or getattr(modeling_result, "scene", None)
                    if scene:
                        perception["env"]["scene"] = scene
                    perception["env"]["density"] = "mid"  # 默认值，后续可从实际数据提取
                
                # people 信息（从 objects 中统计）
                person_count = sum(1 for obj in objects if obj.get("class", "").lower() in ("person", "people", "human"))
                perception["people"] = {
                    "count": person_count,
                    "moving": False  # 默认值，后续可从实际数据提取
                }
                
                # events（暂时为空，后续可从实际数据提取）
                perception["events"] = []
                
                # v0.4.3: 添加 view_state（最小实现）
                # 尝试从实际数据计算，如果无法获取则使用 fallback
                from vision_pipeline.b2.v03.utils.view_state_builder import (
                    build_view_state,
                    ensure_view_state_in_perception
                )
                
                # 尝试从 IMU 数据或相机数据计算 view_state
                # 这里使用简化实现，实际应该从 camera_handler 或 IMU 获取
                current_stability = 0.7  # 简化：假设中等稳定性
                estimated_range_m = 10.0  # 简化：假设 10 米
                current_visibility = 0.75  # 简化：假设中等可见度
                
                # 如果可以从实际数据获取，替换上述值
                # TODO: 从 camera_handler 或 IMU 获取真实数据
                
                perception["view_state"] = build_view_state(
                    stability_score=current_stability,
                    range_m=estimated_range_m,
                    visibility_score=current_visibility,
                    source="vision",
                    confidence=0.8,
                )
                
                # 兜底策略：确保 view_state 存在（防止历史脚本误炸）
                perception = ensure_view_state_in_perception(perception)
                
                # 调用 B2 v0.3 tick
                world_change = self.b2_v03.tick(
                    frame_ts=frame_ts if frame_ts else timestamp,
                    perception=perception
                )
                result["b2_recomputed"] = bool(world_change)  # 有效 tick：B2 本帧实际重算

                if world_change:
                    # 记录世界变化（不指挥 C）
                    result["b2_world_change_v03"] = world_change
                    result["b2_log_v03"] = {
                        "level": world_change.level.name,
                        "confidence": world_change.confidence,
                        "interrupt": world_change.interrupt,
                        "factors": list(world_change.factors.keys()),
                    }
                    # 记录日志（给测试/v0.4 用）
                    print(
                        f"[WORLD] level={world_change.level.name} "
                        f"interrupt={world_change.interrupt} "
                        f"confidence={world_change.confidence:.2f} "
                        f"factors={list(world_change.factors.keys())}"
                    )
            except Exception as e:
                print(f"[Pipeline] B2 v0.3 tick 失败: {e}")
                # 降级：不影响主流程
                pass
        
        # ===============================
        # B2 v0.2: 未来世界预演层（旁路模式，不影响现有 C）
        # ===============================
        # 调用顺序：Perception → ModelingExecutor → NavigationExecutor → B2.tick() → C.observe()
        # 原则：B2 不影响 C 的输入，B2 输出只进入 log + advisory channel
        # 关键修复：B2.tick() 必须每帧都调用，内部判断是否真正运行
        # ⚠️ 硬保护：v0.3 启用时，v0.2 必须被禁用（避免 observer 调用冲突）
        # 双重检查：确保 v0.3 启用时绝对不会进入 v0.2 路径
        if self.b2_v03_enabled:
            # v0.3 启用时，强制跳过 v0.2 路径
            pass
        elif self.b2_v02_enabled:
            try:
                # 优先使用新的 B2V02（缓存与节律接管版）
                if self.b2_v02 is not None:
                    # 准备 navigation_result 和 modeling_result 的字典格式
                    nav_dict = None
                    if navigation_result:
                        nav_dict = {
                            "route": getattr(navigation_result, "route", None),
                            "task_chain": getattr(navigation_result, "task_chain", None),
                        }
                    
                    model_dict = None
                    if modeling_result:
                        # 提取 objects 列表
                        objects = []
                        if hasattr(modeling_result, "objects"):
                            for obj in modeling_result.objects:
                                if hasattr(obj, "__dict__"):
                                    obj_dict = obj.__dict__
                                elif isinstance(obj, dict):
                                    obj_dict = obj
                                else:
                                    obj_dict = {"class": str(obj)}
                                objects.append(obj_dict)
                        
                        model_dict = {
                            "objects": objects,
                            "scene": getattr(modeling_result, "scene", None),
                            "scene_label": getattr(modeling_result, "scene_label", None),
                        }
                    
                    # 调用新的 B2 v0.3（tick 模式：每帧都调用，内部判断是否运行）
                    # 关键修复：从事件驱动改为 tick 驱动
                    b2_output = self.b2_v02.tick(
                        now_ts=timestamp,
                        navigation_result=nav_dict,
                        modeling_result=model_dict,
                    )
                    
                    if b2_output:
                        result["b2_recomputed"] = True
                        result["b2_output_v02"] = b2_output
                        result["b2_log"] = {
                            "world_signature": b2_output.get("world_signature"),
                            "epoch_id": b2_output.get("epoch_id"),
                            "trigger": b2_output.get("trigger"),
                            "cache": b2_output.get("cache"),
                            "advisories_count": len(b2_output.get("advisories", [])),
                        }
                # Fallback: 使用旧的 b2_controller_v02（如果存在）
                elif self.b2_controller_v02 is not None:
                    # 构建 WorldSnapshot（从真实 pipeline 输出映射）
                    world_snapshot = self._build_world_snapshot_v02(
                        modeling_result=modeling_result,
                        navigation_result=navigation_result,
                        context=context,
                        timestamp=timestamp,
                    )
                    
                    # 调用 B2 v0.2 observe（旁路模式，只写日志）
                    b2_advisory_v02 = self.b2_controller_v02.observe(
                        world_snapshot=world_snapshot,
                        navigation_result=navigation_result,
                        modeling_result=modeling_result,
                    )
                    
                    if b2_advisory_v02:
                        # B2 → C 对接方案：推送到 Advisory Queue
                        if self.advisory_queue:
                            self.advisory_queue.push(b2_advisory_v02)
                        
                        # 只写日志，不修改 C 的 decision，不修改执行链
                        min_ttc = min([e.ttc for e in b2_advisory_v02.impacts]) if b2_advisory_v02.impacts else None
                        log_msg = f"[B2-v0.2][{timestamp:.2f}] {b2_advisory_v02.advisory_type} | "
                        log_msg += f"trigger={b2_advisory_v02.trigger_reason} | "
                        log_msg += f"confidence={b2_advisory_v02.confidence:.2f} | "
                        log_msg += f"impacts={len(b2_advisory_v02.impacts)}"
                        if min_ttc is not None:
                            log_msg += f" | min_ttc={min_ttc:.2f}s"
                        print(log_msg)
                        result["b2_advisory_v02"] = b2_advisory_v02
                        
                        # 记录 B2 完整信息（用于后续分析，日志分离）
                        result["b2_log"] = {
                            "sim_ran": True,
                            "impact_events": len(b2_advisory_v02.impacts),
                            "min_ttc": min_ttc,
                            "advisory": b2_advisory_v02.advisory_type,
                            "trigger_reason": b2_advisory_v02.trigger_reason,
                            "horizon_sec": b2_advisory_v02.horizon_sec,
                        }
            except Exception as e:
                # 如果 B2 v0.2 出错，不影响现有功能
                print(f"[B2-v0.2] Error: {e}")
                import traceback
                traceback.print_exc()
        
        # ===============================
        # B2 v0.1: 上帝视角的大场景观察器（在 pipeline 结束后运行，不控制 C）
        # ===============================
        if B2_V01_ENABLED and self.b2_controller:
            try:
                # 组装 WorldSnapshot（从真实 pipeline 输出映射）
                from vision_pipeline.b2.world_snapshot import WorldSnapshot, EgoPose, WorldObject
                
                # 提取 ego 信息
                ego_motion = context.get("ego_motion", {}) if context else {}
                ego_pose = EgoPose(
                    heading=ego_motion.get("heading", 0.0),
                    speed=ego_motion.get("velocity", 0.0) or ego_motion.get("speed", 0.0),
                    pos=ego_motion.get("position"),
                )
                
                # 提取 objects（从 navigation_result）
                objects = []
                if navigation_result and navigation_result.objects:
                    for i, obj in enumerate(navigation_result.objects):
                        obj_id = obj.get("id") if isinstance(obj, dict) else f"obj_{i}"
                        cls = obj.get("class") if isinstance(obj, dict) else "unknown"
                        bbox = obj.get("bbox") if isinstance(obj, dict) else None
                        objects.append(WorldObject(
                            obj_id=obj_id,
                            cls=cls,
                            bbox=bbox,
                            pos=None,  # 后续可以从 bbox 或 position 提取
                            vel=None,  # 后续可以从 velocity 提取
                        ))
                
                # 提取 texts（从 modeling_result）
                texts = []
                if modeling_result and hasattr(modeling_result, "content_candidates"):
                    for candidate in modeling_result.content_candidates:
                        if hasattr(candidate, "raw_texts") and candidate.raw_texts:
                            texts.extend(candidate.raw_texts)
                
                # 构建 WorldSnapshot
                world_snapshot = WorldSnapshot(
                    timestamp=timestamp,
                    ego=ego_pose,
                    objects=objects,
                    texts=texts,
                )
                
                # 调用 B2 v0.2 observe（旁路模式，只写日志）
                # B2 → C 对接方案：B2 在"世界已知"后运行
                # ⚠️ 硬保护：v0.3 启用时，不允许调用 v0.2
                if self.b2_v03_enabled or self.b2_controller_v02 is None:
                    # v0.3 启用或 v0.2 未初始化，跳过
                    b2_advisory_v02 = None
                else:
                    b2_advisory_v02 = self.b2_controller_v02.observe(
                        world_snapshot=world_snapshot,
                        navigation_result=navigation_result,
                        modeling_result=modeling_result,
                    )
                
                if b2_advisory_v02:
                    # B2 → C 对接方案：推送到 Advisory Queue
                    if self.advisory_queue:
                        self.advisory_queue.push(b2_advisory_v02)
                    
                    # 只写日志，不修改 C 的 decision，不修改执行链
                    min_ttc = min([e.ttc for e in b2_advisory_v02.impacts]) if b2_advisory_v02.impacts else None
                    log_msg = f"[B2-v0.2][{timestamp:.2f}] {b2_advisory_v02.advisory_type} | "
                    log_msg += f"trigger={b2_advisory_v02.trigger_reason} | "
                    log_msg += f"confidence={b2_advisory_v02.confidence:.2f} | "
                    log_msg += f"impacts={len(b2_advisory_v02.impacts)}"
                    if min_ttc is not None:
                        log_msg += f" | min_ttc={min_ttc:.2f}s"
                    print(log_msg)
                    result["b2_advisory_v02"] = b2_advisory_v02
                    
                    # 记录 B2 完整信息（用于后续分析，日志分离）
                    result["b2_log"] = {
                        "sim_ran": True,
                        "impact_events": len(b2_advisory_v02.impacts),
                        "min_ttc": min_ttc,
                        "advisory": b2_advisory_v02.advisory_type,
                        "trigger_reason": b2_advisory_v02.trigger_reason,
                        "horizon_sec": b2_advisory_v02.horizon_sec,
                    }
            except Exception as e:
                # 如果 B2 v0.2 出错，不影响现有功能
                print(f"[B2-v0.2] Error: {e}")
        
        # ===============================
        # B2 v0.1: 上帝视角的大场景观察器（在 pipeline 结束后运行，不控制 C）
        # ===============================
        if B2_V01_ENABLED and self.b2_controller:
            # 构建 frame_ctx（使用真实的 pipeline 结果）
            frame_ctx = {
                "motion_score": context.get("motion_score", 0.0) if context else 0.0,
                "frame_diff_score": context.get("frame_diff_score", 0.0) if context else 0.0,
                "objects": navigation_result.objects if navigation_result and navigation_result.objects else [],
                "texts": [],  # 从 modeling_result 提取
                "avg_luminance": context.get("avg_luminance") if context else None,
                "ego_motion": context.get("ego_motion", {}) if context else {},
                "observability": 0.8,  # 默认值
            }
            
            # 从 modeling_result 中提取 texts
            if modeling_result and hasattr(modeling_result, "content_candidates"):
                texts = []
                for candidate in modeling_result.content_candidates:
                    if hasattr(candidate, "raw_texts") and candidate.raw_texts:
                        texts.extend(candidate.raw_texts)
                frame_ctx["texts"] = texts
            
            # v0.2 新接口：构建 world_snapshot
            world_update = build_b2_world_update(frame_ctx)
            ego_pose = {
                "heading": frame_ctx.get("ego_motion", {}).get("heading", 0),
                "position": frame_ctx.get("ego_motion", {}).get("position", (0.0, 0.0)),
                "velocity": frame_ctx.get("ego_motion", {}).get("velocity", 1.0),
            }
            
            world_snapshot = {
                "world_update": world_update,
                "ego_pose": ego_pose,
                "objects": frame_ctx.get("objects", []),
                "timestamp": timestamp,
            }
            
            # 调用 B2 observe（v0.2 新接口）
            b2_output = self.b2_controller.observe(
                world_snapshot=world_snapshot,
                navigation_result=navigation_result,
                modeling_result=modeling_result,
            )
            
            if b2_output:
                # 写入共享黑板
                self.b2_blackboard.put_b2(b2_output)
                # 按节律打印日志（避免刷屏）
                if self.b2_controller.should_log(b2_output.ts):
                    impact_count = b2_output.metrics.get("impact_count", 0)
                    print(f"[B2][{b2_output.ts:.2f}] {b2_output.trigger_reason} | "
                          f"advisories={len(b2_output.advisories)} | "
                          f"impacts={impact_count}")
                result["b2_output"] = b2_output
        
        # ===============================
        # C1 日志和效能评估（Active Mode v0.2）
        # ===============================
        if not C1_MODE_SHADOW_ONLY and self.c1_state_machine and self.c1_logger_v02:
            # v0.2 结构化日志（必须字段）
            if c1_state_result:
                c1_state = c1_state_result["state"]
                state_transition = c1_state_result.get("state_transition")
                protection_active = c1_state_result.get("protection_trigger_reason") is not None
                protection_reason = c1_state_result.get("protection_trigger_reason")
                protection_remaining = c1_state_result.get("protection_remaining_sec")
                
                self.c1_logger_v02.log(
                    c1_state=c1_state,
                    state_transition=state_transition,
                    motion_score=motion_score,
                    frame_diff=frame_diff_score,
                    protection_active=protection_active,
                    protection_reason=protection_reason,
                    protection_remaining_sec=protection_remaining,
                    modeling_executed=modeling_executed,
                    timestamp=timestamp,
                )
            
            # ⚠️ 对比日志：C1 决策 vs 实际是否执行 LV4（v0.2 增强版）
            if c1_skip_modeling:
                state_transition = c1_state_result.get("state_transition") if c1_state_result else None
                protection_reason = c1_state_result.get("protection_trigger_reason") if c1_state_result else None
                protection_remaining = c1_state_result.get("protection_remaining_sec") if c1_state_result else None
                
                log_parts = [
                    f"[C1-ACTIVE][{timestamp:.2f}]",
                    f"C1决策=SKIP_MODELING",
                    f"实际执行=NO",
                    f"状态={c1_state_result['state'].value if c1_state_result else 'unknown'}",
                ]
                
                if state_transition:
                    log_parts.append(f"state_transition={state_transition}")
                if protection_reason:
                    log_parts.append(f"protection_trigger_reason={protection_reason}")
                if protection_remaining is not None:
                    log_parts.append(f"protection_remaining_sec={protection_remaining:.1f}")
                
                print(" ".join(log_parts))
            elif modeling_executed:
                state_transition = c1_state_result.get("state_transition") if c1_state_result else None
                log_parts = [
                    f"[C1-ACTIVE][{timestamp:.2f}]",
                    f"C1决策=ALLOW_MODELING",
                    f"实际执行=YES",
                    f"状态={c1_state_result['state'].value if c1_state_result else 'unknown'}",
                ]
                
                if state_transition:
                    log_parts.append(f"state_transition={state_transition}")
                
                print(" ".join(log_parts)                )
            
            return result
    
    def _build_world_snapshot_v02(
        self,
        modeling_result: Optional[Any],
        navigation_result: Optional[Any] = None,
        context: Optional[Dict[str, Any]] = None,
        timestamp: Optional[float] = None,
    ) -> Any:
        """
        构建 WorldSnapshot（从真实 pipeline 输出映射）
        
        A4.2: 在 PipelineController 中新增 WorldSnapshot 构造函数
        
        目标：
        - 不改变现有 pipeline 行为
        - 不影响 C / Navigation / Modeling 的输出
        - 只是在 pipeline 中"旁路构造一个 WorldSnapshot 给 B2 用"
        
        ⚠️ 注意：
        - 不做任何理解
        - 不做任何过滤
        - 原样映射，保持"上帝视角的原始世界"
        
        Args:
            modeling_result: ModelingExecutor 输出
            navigation_result: NavigationExecutor 输出（可选）
            context: 上下文（可选）
            timestamp: 时间戳（可选）
        
        Returns:
            WorldSnapshot: B2 可用的世界快照
        """
        from vision_pipeline.b2.world_snapshot import WorldSnapshot, WorldObject, EgoPose
        import time
        
        now = timestamp if timestamp is not None else time.time()
        
        # --- Ego ---
        # 从 context 或内部状态获取 ego 信息
        ego_motion = context.get("ego_motion", {}) if context else {}
        current_heading = ego_motion.get("heading", 0.0)
        current_speed = ego_motion.get("velocity", 0.0) or ego_motion.get("speed", 0.0)
        current_position = ego_motion.get("position")
        
        ego = EgoPose(
            heading=current_heading,
            speed=current_speed,
            pos=current_position,
        )
        
        # --- Objects ---
        # 从 modeling_result 或 navigation_result 提取 objects
        objects = []
        
        # 优先从 navigation_result.objects 获取（如果存在）
        if navigation_result and hasattr(navigation_result, "objects") and navigation_result.objects:
            for i, o in enumerate(navigation_result.objects):
                if isinstance(o, dict):
                    objects.append(
                        WorldObject(
                            obj_id=o.get("id", f"obj_{i}"),
                            cls=o.get("class", o.get("cls", "unknown")),
                            bbox=o.get("bbox"),
                            pos=o.get("position"),
                            vel=o.get("velocity"),
                            extra={
                                "confidence": o.get("confidence", 0.0),
                            },
                        )
                    )
                else:
                    # 如果不是 dict，尝试从对象属性获取
                    objects.append(
                        WorldObject(
                            obj_id=getattr(o, "id", f"obj_{i}"),
                            cls=getattr(o, "class", getattr(o, "cls", "unknown")),
                            bbox=getattr(o, "bbox", None),
                            pos=getattr(o, "position", None),
                            vel=getattr(o, "velocity", None),
                            extra={
                                "confidence": getattr(o, "confidence", 0.0),
                            },
                        )
                    )
        
        # 如果 navigation_result 没有 objects，尝试从 modeling_result 获取
        if not objects and modeling_result:
            # 检查 modeling_result 是否有 objects 字段
            if hasattr(modeling_result, "objects") and modeling_result.objects:
                for i, o in enumerate(modeling_result.objects):
                    if isinstance(o, dict):
                        objects.append(
                            WorldObject(
                                obj_id=o.get("id", f"obj_{i}"),
                                cls=o.get("class", o.get("cls", "unknown")),
                                bbox=o.get("bbox"),
                                pos=o.get("position"),
                                vel=o.get("velocity"),
                                extra={
                                    "confidence": o.get("confidence", 0.0),
                                },
                            )
                        )
        
        # --- Texts ---
        # 从 modeling_result 提取 texts
        texts = []
        if modeling_result:
            # 方式 1: 直接从 modeling_result.texts 获取
            if hasattr(modeling_result, "texts") and modeling_result.texts:
                texts = modeling_result.texts if isinstance(modeling_result.texts, list) else list(modeling_result.texts)
            
            # 方式 2: 从 content_candidates 中提取 raw_texts
            elif hasattr(modeling_result, "content_candidates"):
                for candidate in modeling_result.content_candidates:
                    if hasattr(candidate, "raw_texts") and candidate.raw_texts:
                        if isinstance(candidate.raw_texts, list):
                            texts.extend(candidate.raw_texts)
                        else:
                            texts.append(candidate.raw_texts)
                    # 方式 3: 从 raw_text 字段提取
                    elif hasattr(candidate, "raw_text") and candidate.raw_text:
                        texts.append(candidate.raw_text)
        
        return WorldSnapshot(
            timestamp=now,
            ego=ego,
            objects=objects,
            texts=texts,
            extra={
                "nav_available": navigation_result is not None,
            }
        )
    
    def update_task_state(self, task_state: Dict[str, Any]) -> None:
        """
        更新任务态（来自上层控制中心）
        
        Args:
            task_state: 任务态字典
        """
        self.semantic_router.update_task_state(task_state)
    
    # v1.8.5 Phase B Step 1.1: CameraHandler 委托方法
    def read_frame(self) -> Optional[np.ndarray]:
        """
        读取一帧图像（委托给 CameraHandler）

        Returns:
            图像数据，如果失败返回None
        """
        frame = self.camera_handler.read_frame()
        self._frame_id += 1
        self._update_frame_context(frame, ts=time.time())
        return frame

    @property
    def input_ended(self) -> bool:
        """视频文件是否已播放完毕（仅当输入为视频时有效）"""
        return getattr(self.camera_handler, "_video_ended", False)

    @property
    def video_fps(self) -> float:
        """视频文件帧率（仅当输入为视频时有效，否则为 0）"""
        if not getattr(self.camera_handler, "video_path", None):
            return 0.0
        return self.camera_handler.get_fps()

    def get_frame_context(self) -> Dict[str, Any]:
        """
        获取最近一帧的感知上下文（用于 C1 / A3）
        """
        return dict(self._last_frame_context)

    def _is_frame_valid(self, frame: Optional[np.ndarray]) -> bool:
        if frame is None:
            return False
        if getattr(frame, "size", 0) == 0:
            return False
        mean_val = float(np.mean(frame))
        return mean_val >= 2.0

    def _compute_frame_metrics(self, frame: np.ndarray) -> Dict[str, Any]:
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame

        mean_luma = float(np.mean(gray))
        avg_luminance = mean_luma / 255.0

        if self._last_frame_gray is None:
            frame_diff = 0.0
            roi_count = 0
            path_instability = 0.0
            branch_load = 0.0
        else:
            diff = cv2.absdiff(gray, self._last_frame_gray)
            frame_diff = float(np.mean(diff)) / 255.0
            h, w = gray.shape[:2]
            # 被动 ROI v0：motion 空间分布 → 候选区域计数
            roi_count = compute_passive_roi_count(diff, h * w)
            # Path v0 / Branch v0：单次光流 → path_instability, branch_load
            path_instability, branch_load = compute_path_and_branch(self._last_frame_gray, gray)

        # 运动评分：最小可用版本，使用帧差归一化值
        motion_score = frame_diff

        # 遮挡估计：基于边缘稀疏度（手挡/遮挡通常边缘极少）
        edges = cv2.Canny(gray, 50, 150)
        edge_density = float(np.mean(edges > 0))
        edge_ref = 0.02
        occlusion_ratio = 1.0 - min(1.0, edge_density / edge_ref) if edge_ref > 0 else 0.0

        # 视角事实层 v0: 额外指标
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        clarity = 1.0 / (1.0 + np.exp(-(laplacian_var - 100) / 20))
        blur_score = 1.0 - min(1.0, max(0.0, clarity))
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        high_energy = float(np.mean(np.abs(laplacian)))
        noise_level = min(1.0, max(0.0, high_energy / 50.0))
        eps = 0.01
        freeze_score = 1.0 - min(1.0, frame_diff / eps) if eps > 0 else 0.0

        self._last_frame_gray = gray

        return {
            "mean_luma": mean_luma,
            "avg_luminance": avg_luminance,
            "frame_diff_score": frame_diff,
            "motion_score": motion_score,
            "occlusion_ratio": occlusion_ratio,
            "blur_score": blur_score,
            "noise_level": noise_level,
            "frame_diff": frame_diff,
            "freeze_score": freeze_score,
            "roi_count": roi_count,
            "path_instability": path_instability,
            "branch_load": branch_load,
        }

    def _update_continuity(self, frame_valid: bool, frame_quality: str, frame_diff: float) -> Dict[str, Any]:
        if frame_valid:
            self._continuity["valid_streak"] += 1
            self._continuity["invalid_streak"] = 0
        else:
            self._continuity["invalid_streak"] += 1
            self._continuity["valid_streak"] = 0

        if frame_quality == "DEGRADED":
            self._continuity["degraded_streak"] += 1
        else:
            self._continuity["degraded_streak"] = 0

        if frame_diff < 0.05:
            self._continuity["low_diff_streak"] += 1
        else:
            self._continuity["low_diff_streak"] = 0

        return {
            "valid_streak": self._continuity["valid_streak"],
            "invalid_streak": self._continuity["invalid_streak"],
            "degraded_streak": self._continuity["degraded_streak"],
        }

    def _model_status(self) -> Dict[str, str]:
        ocr_up = False
        if self.modeling_executor and getattr(self.modeling_executor, "ocr_processor", None):
            ocr_up = True
        return {
            "b2_v02": "UP" if self.b2_v02_enabled else "DOWN",
            "b2_v03": "UP" if self.b2_v03_enabled else "DOWN",
            "ocr": "UP" if ocr_up else "DOWN",
        }

    def _compute_view_confidence(self, frame_quality: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        if frame_quality == "INVALID":
            return {
                "view_confidence": 0.0,
                "confidence_reason": "INVALID_FRAME",
                "model_status": self._model_status(),
            }

        blur_score = float(metrics.get("blur_score", 0.0))
        noise_level = float(metrics.get("noise_level", 0.0))
        quality_score = max(0.0, 1.0 - max(blur_score, noise_level) * 0.5)

        if frame_quality == "DEGRADED":
            severity = max(blur_score, noise_level)
            view_conf = max(0.3, min(0.5, 0.5 - 0.2 * severity))
            return {
                "view_confidence": view_conf,
                "confidence_reason": "DEGRADED_QUALITY",
                "model_status": self._model_status(),
            }

        model_status = self._model_status()
        if any(v == "DOWN" for v in model_status.values()):
            view_conf = min(0.6, 0.8 + 0.2 * quality_score)
            return {
                "view_confidence": view_conf,
                "confidence_reason": "MODEL_DOWN",
                "model_status": model_status,
            }

        return {
            "view_confidence": 0.8 + 0.2 * quality_score,
            "confidence_reason": "NORMAL",
            "model_status": model_status,
        }

    def _update_frame_context(self, frame: Optional[np.ndarray], ts: Optional[float] = None) -> None:
        # View Fact Layer v0: 仅事实，不做语义推断
        now_ts = ts if ts is not None else time.time()
        sampling_interval_ms = None
        if self._last_frame_ts is not None:
            sampling_interval_ms = (now_ts - self._last_frame_ts) * 1000.0
        self._last_frame_ts = now_ts

        if frame is None or getattr(frame, "size", 0) == 0:
            frame_valid = False
            metrics = {
                "mean_luma": None,
                "avg_luminance": None,
                "blur_score": 1.0,
                "noise_level": 1.0,
                "frame_diff": 0.0,
                "freeze_score": 1.0,
                "motion_score": 0.0,
                "frame_diff_score": 0.0,
                "occlusion_ratio": 0.0,
                "roi_count": 0,
                "path_instability": 0.0,
                "branch_load": 0.0,
            }
        else:
            metrics = self._compute_frame_metrics(frame)
            if sampling_interval_ms is not None and sampling_interval_ms > 200:
                metrics["freeze_score"] = 0.0
            freeze_score = float(metrics.get("freeze_score", 0.0))
            mean_luma = metrics.get("mean_luma")
            frame_valid = bool(mean_luma is not None and mean_luma >= 2.0 and freeze_score < 0.98)

        frame_quality = "INVALID" if not frame_valid else "GOOD"
        blur_score = float(metrics.get("blur_score", 0.0))
        noise_level = float(metrics.get("noise_level", 0.0))
        frame_diff = float(metrics.get("frame_diff", 0.0))

        # v0.1: motion_instability (EMA + linear mapping)
        alpha = 0.2
        if self._motion_ema is None:
            self._motion_ema = frame_diff
        else:
            self._motion_ema = alpha * frame_diff + (1.0 - alpha) * self._motion_ema
        self.motion_instability = max(0.0, min(1.0, self._motion_ema * 8.0))

        if frame_quality != "INVALID":
            if blur_score > 0.6 or noise_level > 0.5:
                frame_quality = "DEGRADED"
            if frame_diff < 0.05:
                if self._continuity["low_diff_streak"] + 1 >= 3:
                    frame_quality = "DEGRADED"

        continuity = self._update_continuity(frame_valid, frame_quality, frame_diff)
        view_confidence = self._compute_view_confidence(frame_quality, metrics)

        # 硬约束：仅在 GOOD 时允许遮挡判断
        occlusion_ratio = float(metrics.get("occlusion_ratio", 0.0))
        if frame_quality == "GOOD":
            occlusion_state = OcclusionState.OCCLUDED if occlusion_ratio >= 0.8 else OcclusionState.CLEAR
        else:
            occlusion_state = OcclusionState.UNKNOWN

        self.occlusion_ratio = occlusion_ratio
        self.perception_state = "NORMAL" if frame_quality == "GOOD" else "DEGRADED"
        self.view_confidence = float(view_confidence.get("view_confidence", 0.0))
        self.frame_quality = frame_quality

        # 被动 ROI v0 / Path v0 / Branch v0：只进 A3，不进 perception/C1/C2
        self.roi_count = int(metrics.get("roi_count", 0))
        self.path_instability = float(metrics.get("path_instability", 0.0))
        self.branch_load = float(metrics.get("branch_load", 0.0))

        self._last_frame_context = {
            "ts": time.time(),
            "frame_id": self._frame_id,
            "frame_valid": frame_valid,
            "frame_quality": frame_quality,
            "metrics": {
                "mean_luma": metrics.get("mean_luma"),
                "blur_score": metrics.get("blur_score"),
                "noise_level": metrics.get("noise_level"),
                "frame_diff": metrics.get("frame_diff"),
                "freeze_score": metrics.get("freeze_score"),
                "sampling_interval_ms": sampling_interval_ms,
            },
            "continuity": continuity,
            "view_confidence": view_confidence.get("view_confidence"),
            "confidence_reason": view_confidence.get("confidence_reason"),
            "model_status": view_confidence.get("model_status"),
            "motion_instability": self.motion_instability,
            "roi_count": self.roi_count,
            "path_instability": self.path_instability,
            "branch_load": self.branch_load,
            "occlusion_state": occlusion_state,
            "perception_state": self.perception_state,
            "motion_score": float(metrics.get("motion_score", 0.0)),
            "frame_diff_score": float(metrics.get("frame_diff_score", 0.0)),
            "avg_luminance": metrics.get("avg_luminance"),
        }
    
    def is_opened(self) -> bool:
        """
        检查摄像头是否打开（委托给 CameraHandler）
        
        Returns:
            是否打开
        """
        return self.camera_handler.is_opened()
    
    def release(self) -> None:
        """
        释放摄像头资源（委托给 CameraHandler）
        """
        self.camera_handler.release()

