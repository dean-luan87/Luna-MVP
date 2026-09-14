# -*- coding: utf-8 -*-
"""Task to Guidance Safety Gate Dry-Run — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Task-To-Guidance-Safety-Gate-DryRun-v1-001"
SCOPE = "task_to_guidance_safety_gate_dryrun_only"
SOURCE_CHAIN = "task_to_guidance_safety_gate_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "Task → Guidance / Speech Gate / Action Safety dry-run：验证 Task 层候选如何进入 "
    "GuidanceCandidate / SpeechGateCandidate / ActionSafetyCandidate，"
    "形成安全引导候选链路，不触发真实导航、语音或动作。"
)

TASK_MANAGER_ENTRYPOINT = "task_manager_v1"
GUIDANCE_ENTRYPOINT = "navigation_guidance_candidate_v1"
SPEECH_GATE_ENTRYPOINT = "speech_gate_v1"
ACTION_SAFETY_ENTRYPOINT = "action_safety_candidate_v1"

FIELD_TO_TASK_DRYRUN_REF = "Phase-Field-To-Task-Alignment-DryRun-v1-001"
FIELD_SYNTHESIS_DRYRUN_REF = (
    "Phase-Field-Synthesis-Map-Place-Realtime-Event-Overlay-DryRun-v1-001"
)
TASK_MANAGER_REF = (
    "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001"
)
BASIC_NAVIGATION_GUIDANCE_LOOP_REF = "Phase-Basic-Navigation-Guidance-Loop-DryRun-v1-001"
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"

FINAL_DECISION_DRYRUN_GO = "TASK_TO_GUIDANCE_SAFETY_GATE_DRYRUN_GO"
FINAL_DECISION_DRYRUN_BLOCKED = "TASK_TO_GUIDANCE_SAFETY_GATE_DRYRUN_BLOCKED"

POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "mall_find_entrance_guidance_candidate",
    "subway_enter_station_guidance_candidate",
    "stadium_concert_ticket_gate_guidance_candidate",
    "plaza_market_crowd_safety_guidance_candidate",
    "gps_slam_conflict_guidance_blocked",
    "home_return_stable_guidance_candidate",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_task_route_hint_as_navigation_action",
    "invalid_speech_gate_triggers_tts",
    "invalid_conflict_action_like_guidance",
    "invalid_guidance_bypasses_action_safety",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "TaskToGuidanceDryRunCase",
    "TaskToGuidanceInputBundle",
    "GuidanceCandidate",
    "SpeechGateCandidate",
    "ActionSafetyCandidate",
    "GuidanceEvidenceRequestCandidate",
    "TaskToGuidanceDryRunTrace",
    "TaskToGuidanceReviewDecision",
)

GUIDANCE_PIPELINE: Tuple[str, ...] = (
    "TaskContextCandidate",
    "TaskEvidenceNeedCandidate",
    "TaskRouteHintCandidate",
    "TaskRiskCandidate",
    "GuidanceEvidenceRequestCandidate",
    "GuidanceCandidate",
    "SpeechGateCandidate",
    "ActionSafetyCandidate",
    "GuidanceSafetyDryRunDecision",
)

GUIDANCE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "task_route_hint_is_not_action",
    "guidance_candidate_is_not_navigation_runtime",
    "speech_gate_candidate_is_not_tts_output",
    "action_safety_required_before_action_like_guidance",
    "gps_slam_conflict_blocks_action_like_guidance",
    "high_risk_downgrades_guidance",
    "guidance_may_request_evidence_no_live_sensor",
    "field_interaction_label_wording_only_no_map_place_rewrite",
    "all_outputs_candidate_only",
    "no_direct_action_speech_fact_write_navigation_runtime",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "dryrun_only": True,
    "no_real_navigation": True,
    "no_real_speech_tts": True,
    "no_live_sensor": True,
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
class TaskToGuidanceInputBundle:
    bundle_ref: str
    case_ref: str
    task_trace: Dict[str, Any]
    source_chain: Tuple[str, ...]
    task_manager_entrypoint: str
    guidance_entrypoint: str
    speech_gate_entrypoint: str
    action_safety_entrypoint: str
    candidate_only: bool = True


@dataclass(frozen=True)
class TaskToGuidanceDryRunCase:
    case_ref: str
    case_kind: str
    task_case_ref: str
    input_bundle_ref: str
    expected_outcome: Dict[str, Any]
    candidate_only: bool = True


@dataclass(frozen=True)
class GuidanceEvidenceRequestCandidate:
    candidate_ref: str
    evidence_request_id: str
    requested_evidence_kinds: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    guidance_entrypoint: str
    candidate_only: bool = True
    live_sensor_trigger_allowed: bool = False


@dataclass(frozen=True)
class GuidanceCandidate:
    candidate_ref: str
    guidance_id: str
    guidance_type: str
    guidance_status: str
    field_label: str
    underlying_map_place_ref: str
    source_chain: Tuple[str, ...]
    guidance_entrypoint: str
    candidate_only: bool = True
    is_navigation_runtime: bool = False
    direct_action_allowed: bool = False


@dataclass(frozen=True)
class SpeechGateCandidate:
    candidate_ref: str
    speech_gate_id: str
    utterance_kind: str
    wording_hint: str
    source_chain: Tuple[str, ...]
    speech_gate_entrypoint: str
    candidate_only: bool = True
    trigger_tts: bool = False
    direct_speech_allowed: bool = False


@dataclass(frozen=True)
class ActionSafetyCandidate:
    candidate_ref: str
    safety_id: str
    safety_status: str
    risk_kinds: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    action_safety_entrypoint: str
    candidate_only: bool = True
    direct_action_allowed: bool = False


@dataclass(frozen=True)
class TaskToGuidanceDryRunTrace:
    trace_ref: str
    case_ref: str
    guidance_ok: bool
    guidance_evidence_request_candidate: Dict[str, Any]
    guidance_candidate: Dict[str, Any]
    speech_gate_candidate: Dict[str, Any]
    action_safety_candidate: Dict[str, Any]
    guidance_safety_decision: Dict[str, Any]
    guidance_issues: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class TaskToGuidanceReviewDecision:
    decision_ref: str
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
