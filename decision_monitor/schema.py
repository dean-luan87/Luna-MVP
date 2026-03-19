# -*- coding: utf-8 -*-
"""
决策显示器 6 层数据契约。

统一结构 DecisionMonitorFrame：goal / inputs / state / decision / outputs / consequence。
每层最小字段见 docstring；允许部分占位，后续与真实系统对齐。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .local_goal_spatial_map import LocalGoalSpatialMap
from .local_goal_spatial_relations import SpatialRelation
from .skeleton_mix import SkeletonMix
from .skeleton_filter import SkeletonFilterResult
from .spatial_memory_pools import SpatialMemoryPools
from .spatial_forgetting import SpatialForgettingSummary
from .evidence_ledger import EvidenceLedger
from .hypothesis_layer import HypothesisLayer
from .recheck_planner import RecheckPlannerResult
from .object_temporal_ledger import ObjectTemporalLedger
from .object_search_interaction import ObjectSearchInteractionResult
from .task_arbitration import TaskArbitrationResult
from .task_bundle import TaskBundleResult
from .task_chain_bridge import TaskChainBridgeResult
from .experience_evolution import ExperienceEvolutionResult
from .mainline_integration import MainlineIntegrationResult
from .visual_candidate_audit import VisualCandidateAuditResult
from .spatial_expression_sidecar import SpatialExpressionResult
from .action_hint_copy import ActionHintCopyResult
from .confirmation_input_bridge import ConfirmationInputBridgeResult
from .confirmation_whitebox_trace import ConfirmationWhiteboxTraceResult
from .evidence_hypothesis_whitebox_trace import EvidenceHypothesisWhiteboxTraceResult
from .local_task_space_grid import LocalTaskSpaceGridResult
from .grid_search_expansion import GridSearchExpansionResult
from .grid_search_whitebox_trace import GridSearchWhiteboxTraceResult
from .recheck_whitebox_trace import RecheckWhiteboxTraceResult
from .action_hint_whitebox_trace import ActionHintWhiteboxTraceResult
from .experience_governance_whitebox_trace import ExperienceGovernanceWhiteboxTraceResult
from .reasoning_tree_metrics import ReasoningTreeMetricsResult
from .optimization_hint import OptimizationHintResult


@dataclass
class SpatialScaleContext:
    """
    M1.5 标尺层：宪法最小接入—场景剖面、用户物理包络、速度。
    供 Viewer / 下游消费；优先使用平滑后速度（当前可占位）。
    """
    scene_profile: Optional[str] = None  # outdoor / indoor
    effective_body_width_cm: Optional[float] = None
    effective_body_height_cm: Optional[float] = None
    clearance_required_cm: Optional[float] = None
    forward_speed_cm_s: Optional[float] = None
    speed_band: Optional[str] = None  # stopped / slow / normal / fast
    reaction_horizon_ms: Optional[float] = None


@dataclass
class GoalLayer:
    """目标层：系统现在到底在为谁服务。"""
    goal_id: Optional[str] = None
    goal_type: Optional[str] = None  # go_to_place / cross_road / find_elevator / find_sign / avoid_obstacle
    goal_description: Optional[str] = None
    goal_source: Optional[str] = None  # user / task_chain / system_generated
    goal_priority: Optional[float] = None
    goal_confidence: Optional[float] = None
    goal_status: Optional[str] = None  # active / paused / blocked / completed / uncertain
    subgoal_description: Optional[str] = None
    goal_switch_reason: Optional[str] = None


@dataclass
class InputsLayer:
    """输入层：系统基于什么观察在判断。"""
    frame_seq: Optional[int] = None
    produced_ts: Optional[float] = None
    current_ts: Optional[float] = None
    delta_t_ms: Optional[float] = None
    sampled: Optional[bool] = None
    route: Optional[str] = None
    active_b2_impact: Optional[bool] = None
    raw_observation_summary: Optional[str] = None
    goal_relevant_observations: Optional[str] = None
    sensor_notes: Optional[str] = None


@dataclass
class StateLayer:
    """理解/状态层：系统把当前环境理解成什么状态。"""
    c1_state: Optional[str] = None
    motion: Optional[float] = None
    diff: Optional[float] = None
    risk_score: Optional[float] = None
    safety_level: Optional[str] = None
    weak_evidence_level: Optional[int] = None
    traversability_state: Optional[str] = None
    local_risk_summary: Optional[str] = None
    goal_progress_state: Optional[str] = None  # advancing / waiting / rechecking / blocked / rerouting
    state_confidence: Optional[float] = None
    state_notes: Optional[str] = None
    # 主线 1.3：短时连续状态（上一帧镜像 + 差分 + 趋势）
    prev_state_summary: Optional[str] = None  # 上一时刻状态一句摘要
    state_delta_summary: Optional[str] = None  # 相对上一时刻的变化摘要
    state_trend: Optional[str] = None  # stable / improving / worsening / shifting / recovering
    goal_progress_delta: Optional[str] = None  # 目标推进状态的变化
    # 主线 1.3A：视线/视觉连续性守护（View Guard）
    view_alignment_state: Optional[str] = None  # aligned / misaligned / unknown / assumed_ok
    view_alignment_score: Optional[float] = None  # 0~1
    view_misaligned: Optional[bool] = None
    view_correction_needed: Optional[bool] = None
    view_correction_hint: Optional[str] = None
    vision_quality_state: Optional[str] = None  # good / degraded / invalid / unknown
    vision_reliability_score: Optional[float] = None  # 0~1
    vision_degraded: Optional[bool] = None
    vision_degrade_reason: Optional[str] = None  # occluded / blur / shake / no_forward_view
    vision_recovery_eta_ms: Optional[float] = None
    # 主线 1.3B：短时预演容错（Predictive Hold）
    predictive_hold_allowed: Optional[bool] = None
    predictive_hold_active: Optional[bool] = None
    predictive_hold_remaining_ms: Optional[float] = None
    predictive_hold_reason: Optional[str] = None
    predictive_hold_confidence: Optional[float] = None
    predictive_hold_expired: Optional[bool] = None
    predictive_recovery_action: Optional[str] = None  # recheck_environment / force_sample / freeze_to_minimum_mode
    # 主线 1.3C：运行域守卫（Runtime Domain Guard）
    runtime_domain_state: Optional[str] = None  # normal / degraded / frozen
    runtime_domain_confidence: Optional[float] = None
    domain_mismatch_detected: Optional[bool] = None
    domain_mismatch_reason: Optional[str] = None  # view_misaligned / vision_unusable / high_rotation_or_abnormal_motion
    cognitive_degrade_level: Optional[str] = None  # none / low / high
    cognitive_output_allowed: Optional[bool] = None
    degrade_action: Optional[str] = None  # warn_user / recheck_environment / freeze_to_minimum_mode
    recovery_condition: Optional[str] = None
    # Scene Gate v1：日常场景分类 + 非支持场景挂起
    scene_type: Optional[str] = None  # normal_walk_navigation / stationary_observation / close_range_check / cautious_navigation / unsupported_motion_context / unsupported_view_context / unknown_context
    scene_supported: Optional[bool] = None
    scene_gate_state: Optional[str] = None  # open / cautious / suspended
    scene_gate_reason: Optional[str] = None
    scene_gate_action: Optional[str] = None  # continue_normal / continue_cautious / pause_goal_progress / ignore_high_level_input / freeze_to_minimum_mode
    # Scene Gate 轻量控制输出（供主循环消费）
    goal_progress_paused: Optional[bool] = None
    minimum_mode_active: Optional[bool] = None
    high_level_output_suppressed: Optional[bool] = None
    scene_gate_control_applied: Optional[bool] = None
    # 人工沟通校准（Interaction Calibrator）
    human_check_needed: Optional[bool] = None
    human_check_reason: Optional[str] = None
    human_check_question: Optional[str] = None
    human_check_blocking_level: Optional[str] = None  # soft / confirm_before_degrade / confirm_before_freeze
    human_check_timeout_ms: Optional[float] = None
    human_check_default_action: Optional[str] = None
    human_check_response: Optional[str] = None
    human_check_resolved: Optional[bool] = None
    human_check_pending: Optional[bool] = None
    human_check_timeout_triggered: Optional[bool] = None  # 本帧因超时自动执行 default_action

    # 主线 2.1：LocalGoalState 行为接入（轻量提示 + 是否已应用）
    focus_region_hint: Optional[str] = None
    view_behavior_hint: Optional[str] = None
    local_goal_action_applied: Optional[bool] = None
    local_goal_focus_applied: Optional[bool] = None
    local_goal_recheck_applied: Optional[bool] = None

    # 主线 2.2：recheck 最小执行入口（可见责任链）
    local_goal_recheck_mode: Optional[str] = None  # none / pending / executed
    local_goal_recheck_type: Optional[str] = None  # close_range / environment
    local_goal_recheck_executed: Optional[bool] = None

    # 主线 2.3：观察优先级（由 LocalGoalState 轻量接管）
    local_goal_view_priority: Optional[str] = None  # forward_path_priority / close_range_priority / confirm_zone_priority
    local_goal_view_priority_applied: Optional[bool] = None


@dataclass
class DecisionLayer:
    """决策层：系统为什么这样决定。"""
    decision_id: Optional[str] = None
    for_goal_id: Optional[str] = None
    decision_owner: Optional[str] = None  # controller / sampling_gate / module_gate / b2_impact / floor_guard
    decision_type: Optional[str] = None  # sample / skip / upshift_policy / run_detector / run_ocr / hold
    decision_reason: Optional[str] = None
    policy_mode_before: Optional[str] = None
    policy_mode_after: Optional[str] = None
    b2_impact_applied: Optional[bool] = None
    escape_hatch_triggered: Optional[bool] = None
    floor_forced: Optional[bool] = None
    decision_confidence: Optional[float] = None


@dataclass
class OutputsLayer:
    """输出层：最后落成了什么动作。"""
    policy_intent_summary: Optional[str] = None
    sampling_target_fps: Optional[float] = None
    detector_stride: Optional[int] = None
    ocr_stride: Optional[int] = None
    modules_run: Optional[List[str]] = None
    modules_skipped: Optional[List[str]] = None
    action_summary: Optional[str] = None  # slow_down_observation / continue_navigation / hold_and_recheck
    user_facing_output: Optional[str] = None
    output_notes: Optional[str] = None


@dataclass
class ConsequenceLayer:
    """后果评估层：这样做，短时间内预期会怎样。"""
    expected_gain: Optional[str] = None
    expected_cost: Optional[str] = None
    expected_risk: Optional[str] = None
    consequence_confidence: Optional[float] = None
    evaluation_horizon_ms: Optional[float] = None
    rollback_hint: Optional[str] = None
    post_action_check_needed: Optional[bool] = None


@dataclass
class LocalGoalState:
    """
    主线 2.0：围绕当前目标的短时局部状态图（Local Goal State）。
    汇聚 goal/state/view_guard/scene_gate 等，产出可行动的局部世界表达。
    """
    goal_id: Optional[str] = None
    goal_type: Optional[str] = None  # observe_navigate / confirm_path / close_range_check 等
    goal_focus_region: Optional[str] = None  # 当前目标主要关注区域
    goal_progress_state: Optional[str] = None  # 推进中/需确认/需等待/受阻
    primary_view_direction: Optional[str] = None  # 前方/近场/左前/右前
    traversable_region_summary: Optional[str] = None  # 可通行区域摘要
    critical_objects: Optional[List[str]] = None  # 与目标相关的关键对象（电梯按钮/门牌/分叉口等）
    state_confidence: Optional[float] = None
    state_staleness_ms: Optional[float] = None  # 状态陈旧度
    recheck_required: Optional[bool] = None
    local_risk_summary: Optional[str] = None
    next_best_action: Optional[str] = None  # continue_forward_observation / recheck_close_range / hold_and_confirm / shift_view_left 等


@dataclass
class DecisionMonitorFrame:
    """
    一帧/一周期完整责任链：目标 → 输入 → 理解 → 决策 → 输出 → 后果评估。
    统一出口，供 JSONL / 终端 / 后续 viewer 使用。
    """
    goal: GoalLayer
    inputs: InputsLayer
    state: StateLayer
    decision: DecisionLayer
    outputs: OutputsLayer
    consequence: ConsequenceLayer
    local_goal_state: Optional[LocalGoalState] = None  # 主线 2.0：局部时空状态图
    local_goal_spatial_map: Optional[LocalGoalSpatialMap] = None  # 主线 2 第二阶段 M0/M1.5：局部目标空间图
    local_goal_spatial_relations: Optional[List[SpatialRelation]] = None  # M2：区域关系
    spatial_scale: Optional[SpatialScaleContext] = None  # M1.5：标尺层（场景/包络/速度）
    skeleton_mix: Optional[SkeletonMix] = None  # Skeleton Mix M0：当前帧骨架配比
    skeleton_filter: Optional[SkeletonFilterResult] = None  # 骨架过滤 M0：当前帧过滤策略结果
    spatial_memory_pools: Optional[SpatialMemoryPools] = None  # 骨架记忆分池 M0：四层空间记忆池
    spatial_forgetting: Optional[SpatialForgettingSummary] = None  # 空间遗忘 M0：本帧遗忘摘要
    evidence_ledger: Optional[EvidenceLedger] = None  # 证据账本 M0：当前证据账本
    hypothesis_layer: Optional[HypothesisLayer] = None  # 假设层 M0：最小候选解释层
    recheck_planner: Optional[RecheckPlannerResult] = None  # 补证规划 M0：最小补证执行入口
    object_temporal_ledger: Optional[ObjectTemporalLedger] = None  # 对象时空账本 M0/M1.5：单对象，最后可信与当前候选分离
    object_search_interaction: Optional[ObjectSearchInteractionResult] = None  # 交互式寻物 M0/M1：单对象最小交互建议
    task_arbitration: Optional[TaskArbitrationResult] = None  # 任务仲裁 M0：最小仲裁结果
    task_bundle: Optional[TaskBundleResult] = None  # 联合任务包 M0：merge_into_bundle 时生成的包结构
    task_chain_bridge: Optional[TaskChainBridgeResult] = None  # 任务链桥接 M0：arbitration/bundle/search 摘要
    experience_evolution: Optional[ExperienceEvolutionResult] = None  # 经验演化 M0：经验候选审计与约束
    mainline_integration: Optional[MainlineIntegrationResult] = None  # 主线接入 M0：认知内核摘要与轻量控制
    visual_candidate_audit: Optional[VisualCandidateAuditResult] = None  # 静态图输入桥 + 候选审计 M0
    spatial_expression_sidecar: Optional[SpatialExpressionResult] = None  # 坐标/方位表达旁路 M0
    action_hint_copy: Optional[ActionHintCopyResult] = None  # Action Hint Copy M0：推理→引导→确认 文案链
    confirmation_input_bridge: Optional[ConfirmationInputBridgeResult] = None  # Confirmation Input Bridge M0：用户反馈→系统推进
    confirmation_whitebox_trace: Optional[ConfirmationWhiteboxTraceResult] = None  # Confirmation Whitebox Trace M0：确认输入白盒轨迹（解释映射与推进）
    evidence_hypothesis_whitebox_trace: Optional[EvidenceHypothesisWhiteboxTraceResult] = None  # Evidence/Hypothesis Whitebox Trace M0：证据×假设白盒轨迹
    experience_governance_whitebox_trace: Optional[ExperienceGovernanceWhiteboxTraceResult] = None  # Experience Governance Whitebox Trace M0：经验治理白盒轨迹
    reasoning_tree_metrics: Optional[ReasoningTreeMetricsResult] = None  # Reasoning Tree Metrics M0：结构树指标化/决策质量度量
    optimization_hint: Optional[OptimizationHintResult] = None  # Optimization Hint M0：结构树优化建议层（规则版）
    local_task_space_grid: Optional[LocalTaskSpaceGridResult] = None  # Local Task Space Grid M0：局部任务二维空间格（组织层）
    grid_search_expansion: Optional[GridSearchExpansionResult] = None  # Grid-driven Search Expansion M0：最小扩搜建议层（不控制）
    grid_search_whitebox_trace: Optional[GridSearchWhiteboxTraceResult] = None  # Grid Search Whitebox Trace M0：扩搜建议层白盒轨迹
    recheck_whitebox_trace: Optional[RecheckWhiteboxTraceResult] = None  # Recheck Whitebox Trace M0：补证链路白盒轨迹
    action_hint_whitebox_trace: Optional[ActionHintWhiteboxTraceResult] = None  # Action Hint Whitebox Trace M0：引导话术白盒轨迹
    monitor_version: str = "1.0"
    trace_anchor_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """可序列化为 JSON 的字典（含嵌套 dataclass 转 dict）。"""
        from dataclasses import asdict
        return asdict(self)
