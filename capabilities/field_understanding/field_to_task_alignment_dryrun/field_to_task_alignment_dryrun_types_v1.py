# -*- coding: utf-8 -*-
"""Field to Task Alignment Dry-Run — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Field-To-Task-Alignment-DryRun-v1-001"
SCOPE = "field_to_task_alignment_dryrun_only"
SOURCE_CHAIN = "field_to_task_alignment_dryrun_v1"

ALIGNMENT_PRINCIPLE_ZH = (
    "Field → Task 对齐 dry-run：验证 field_synthesis_v1 输出的 Field 决策能进入 Task Manager，"
    "形成 TaskContext / TaskEvidenceNeed / TaskRouteHint / TaskRisk 候选，"
    "服务任务规划但不触发真实 action / speech / navigation。"
)

FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
TASK_MANAGER_ENTRYPOINT = "task_manager_v1"

FIELD_SYNTHESIS_DRYRUN_REF = (
    "Phase-Field-Synthesis-Map-Place-Realtime-Event-Overlay-DryRun-v1-001"
)
FIELD_ALIGNMENT_REF = "Phase-Field-Map-Place-Realtime-Event-Overlay-Alignment-v1-001"
SPATIAL_EVIDENCE_CHAIN_REF = "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001"
SPATIAL_ODOMETRY_FUSION_REF = "Phase-Spatial-Odometry-Fusion-Interface-GPS-SLAM-Planning-v1-001"
TASK_MANAGER_REF = (
    "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001"
)
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"

FINAL_DECISION_ALIGNMENT_GO = "FIELD_TO_TASK_ALIGNMENT_DRYRUN_GO"
FINAL_DECISION_ALIGNMENT_BLOCKED = "FIELD_TO_TASK_ALIGNMENT_DRYRUN_BLOCKED"

POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "mall_find_entrance_task",
    "subway_station_enter_station_task",
    "stadium_concert_ticket_check_task",
    "plaza_temporary_market_find_stall_task",
    "gps_slam_conflict_delay_navigation_task",
    "home_return_task_stable_field",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_missing_field_interaction_label",
    "invalid_field_conflict_ignored",
    "invalid_event_overlay_rewrites_map_place_in_task",
    "invalid_task_route_hint_direct_action",
)

ALIGNMENT_OBJECT_TYPES: Tuple[str, ...] = (
    "FieldToTaskAlignmentCase",
    "FieldToTaskInputBundle",
    "TaskContextCandidate",
    "TaskEvidenceNeedCandidate",
    "TaskRouteHintCandidate",
    "TaskRiskCandidate",
    "FieldToTaskDryRunTrace",
    "FieldToTaskReviewDecision",
)

ALIGNMENT_PIPELINE: Tuple[str, ...] = (
    "FieldCandidate",
    "FieldStateCandidate",
    "FieldInteractionLabelCandidate",
    "FieldConflictCandidate",
    "TaskContextCandidate",
    "TaskEvidenceNeedCandidate",
    "TaskRouteHintCandidate",
    "TaskRiskCandidate",
    "task_manager_v1",
)

ALIGNMENT_GOVERNANCE_RULES: Tuple[str, ...] = (
    "field_output_candidate_only_in_task_manager",
    "task_manager_must_not_treat_field_label_as_fact_without_admission",
    "field_interaction_label_separated_from_internal_field_state",
    "event_overlay_influences_task_context_not_map_place_ref",
    "gps_slam_conflict_blocks_or_downgrades_route_hint",
    "task_route_hint_is_not_action",
    "task_risk_candidate_is_not_speech",
    "task_evidence_need_no_live_sensor_in_this_phase",
    "no_direct_action_speech_fact_write",
    "source_chain_and_field_candidate_refs_preserved",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "dryrun_only": True,
    "no_real_navigation": True,
    "no_real_map_api": True,
    "no_real_gps_gnss": True,
    "no_live_sensor": True,
    "no_runtime_activation": True,
    "real_navigation_started": False,
    "runtime_activation_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "no_action_output": True,
    "no_speech_output": True,
    "no_fact_write": True,
}


@dataclass(frozen=True)
class FieldToTaskInputBundle:
    bundle_ref: str
    case_ref: str
    user_task: str
    field_trace: Dict[str, Any]
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    task_manager_entrypoint: str
    candidate_only: bool = True


@dataclass(frozen=True)
class FieldToTaskAlignmentCase:
    case_ref: str
    case_kind: str
    user_task: str
    input_bundle_ref: str
    expected_outcome: Dict[str, Any]
    candidate_only: bool = True


@dataclass(frozen=True)
class TaskContextCandidate:
    candidate_ref: str
    task_context_id: str
    field_label: str
    underlying_map_place_ref: str
    user_task: str
    field_state: str
    gps_weight: str
    source_chain: Tuple[str, ...]
    field_candidate_refs: Tuple[str, ...]
    task_manager_entrypoint: str
    candidate_only: bool = True


@dataclass(frozen=True)
class TaskEvidenceNeedCandidate:
    candidate_ref: str
    evidence_need_id: str
    requested_evidence_kinds: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    task_manager_entrypoint: str
    candidate_only: bool = True
    live_sensor_trigger_allowed: bool = False


@dataclass(frozen=True)
class TaskRouteHintCandidate:
    candidate_ref: str
    route_hint_id: str
    hint_kind: str
    status: str
    source_chain: Tuple[str, ...]
    task_manager_entrypoint: str
    candidate_only: bool = True
    direct_action_allowed: bool = False


@dataclass(frozen=True)
class TaskRiskCandidate:
    candidate_ref: str
    risk_id: str
    risk_kinds: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    task_manager_entrypoint: str
    candidate_only: bool = True
    direct_speech_allowed: bool = False


@dataclass(frozen=True)
class FieldToTaskDryRunTrace:
    trace_ref: str
    case_ref: str
    alignment_ok: bool
    task_context_candidate: Dict[str, Any]
    task_evidence_need_candidate: Dict[str, Any]
    task_route_hint_candidate: Dict[str, Any]
    task_risk_candidate: Dict[str, Any]
    task_manager_decision: Dict[str, Any]
    alignment_issues: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class FieldToTaskReviewDecision:
    decision_ref: str
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    field_synthesis_entrypoint_locked: str
    task_manager_entrypoint_locked: str
    real_navigation_started: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
