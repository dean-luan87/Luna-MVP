# -*- coding: utf-8
"""Luna Situation Understanding Model — planning types v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

PHASE_REF = "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-Planning-v1-001"
SYSTEM_ID = "LunaSituationUnderstandingModelPlanningV1"
PLANNING_ONLY = True
LAYER_ID = "L1_Situation_Understanding"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_GO",
    "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_GO",
)

POLICY_REF = "luna_situation_understanding_policy_v1"

FRAME_SOURCES = ("upload", "camera", "replay", "test_fixture")
GOAL_TYPES = (
    "read", "navigate", "find", "avoid", "identify", "understand", "monitor", "unknown",
)
EVIDENCE_SOURCES = (
    "metadata", "sam", "text_detector", "detection", "ocr", "vlm",
    "human_correction", "test_trace", "case_library", "runner_scene_hint", "teacher_label",
)
EVIDENCE_TYPES = (
    "region", "text_density", "object_hint", "scene_hint", "motion_hint",
    "spatial_hint", "risk_hint", "user_signal",
)
SCENE_TYPES = (
    "shopfront_sign", "subway_platform", "street_crossing", "corridor",
    "indoor_store", "home", "office", "restaurant", "hospital",
    "shopping_mall", "unknown_scene", "custom",
)
ENVIRONMENT_TYPES = (
    "commercial_entry", "public_transport", "street_mobility", "indoor_navigation",
    "retail_consumption", "home_living", "work_context", "unknown",
)
TASK_TYPES = (
    "read_text", "find_direction", "assess_walkable", "avoid_obstacle",
    "identify_place", "find_object", "identify_person", "understand_environment",
    "monitor_change", "ask_user", "manual_review",
)
INFO_TYPES = (
    "text_content", "direction_info", "distance_info", "dynamic_motion",
    "object_identity", "place_identity", "walkable_area", "user_goal",
    "spatial_continuity", "social_identity", "unknown",
)
TARGET_TYPES = (
    "primary_text_block", "direction_sign", "entrance_exit", "obstacle_candidate",
    "moving_object", "walkable_path", "product_shelf", "price_tag",
    "person_candidate", "spatial_boundary", "unknown_region",
)
CAPABILITY_TYPES = (
    "ocr", "detection", "sam", "slam", "depth", "tracking", "vlm",
    "search", "map", "speech", "other",
)
PRIORITIES = ("P0", "P1", "P2", "P3")
RELEVANCE_LEVELS = ("none", "low", "medium", "high", "unknown")
RISK_LEVELS = ("low", "medium", "high", "unknown")

SMOKE_CASE_IDS = (
    "case_a_shopfront_sign",
    "case_b_subway_platform",
    "case_c_street_crossing",
    "case_d_corridor",
    "case_e_unknown_scene",
    "case_f_teacher_label_input",
    "case_g_runner_unknown_scene_override",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_PLANNING_BLOCKED"
SMOKE_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_PLANNING_SMOKE_GO"
SMOKE_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_PLANNING_SMOKE_BLOCKED"

RECOMMENDED_NEXT_PHASES = (
    "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001",
    "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-DryRun-v1-001",
    "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-DryRun-v1-001",
)
RECOMMENDED_NEXT_PHASE = RECOMMENDED_NEXT_PHASES[0]

COMMON_CANDIDATE_FIELDS = (
    "candidate_only",
    "not_fact",
    "trace_refs",
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "candidate_only": True,
    "situation_candidate_not_fact": True,
    "no_runner_invocation": True,
    "no_tool_install": True,
    "no_fact_admission_bypass": True,
    "no_navigation_decision": True,
    "scene_profile_owned_by_situation_layer": True,
    "runner_scene_hint_candidate_only": True,
    "teacher_output_not_direct_situation": True,
    "case_library_reference_not_fact": True,
    "human_correction_not_ground_truth": True,
    "deterministic_smoke_only": True,
}


def candidate_meta(
    *,
    trace_refs: Optional[List[Dict[str, Any]]] = None,
    policy_refs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": trace_refs or [],
        "policy_refs": policy_refs or [POLICY_REF],
    }


@dataclass
class FrameContext:
    frame_id: str
    image_id: str
    file_name: str
    timestamp: str
    source: str = "test_fixture"
    job_id_optional: str = ""
    environment_ref_optional: str = ""
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class UserGoalCandidate:
    goal_text_optional: str = ""
    goal_type: str = "unknown"
    confidence: float = 0.0
    source: str = "unknown"
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class VisualEvidenceCandidate:
    evidence_id: str
    source: str
    evidence_type: str
    value: str
    confidence: float
    source_trace_ref: str
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SituationCaseRef:
    case_id: str
    case_type: str
    similarity_score: float
    matched_clues: List[str]
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class EnvironmentMemoryCandidate:
    memory_ref: str
    environment_type_hint: str
    known_place_hint: str
    confidence: float
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class HumanCorrectionSignal:
    correction_ref: str
    correction_type: str
    proposed_scene_hint: str
    proposed_task_hint: str
    confidence: float
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AvailableCapability:
    capability_id: str
    capability_type: str
    availability: str = "unknown"
    cost_hint: str = ""
    latency_hint: str = ""
    local_or_remote: str = "unknown"
    permission_required: bool = False
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SituationUnderstandingInput:
    frame_context: Dict[str, Any]
    user_goal_candidate: Dict[str, Any]
    visual_evidence_candidates: List[Dict[str, Any]]
    situation_case_refs: List[Dict[str, Any]]
    environment_memory_candidates: List[Dict[str, Any]]
    human_correction_signals: List[Dict[str, Any]]
    available_capabilities: List[Dict[str, Any]]
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SceneProfileCandidate:
    scene_type: str
    confidence: float
    evidence_refs: List[str]
    case_refs: List[str]
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SurvivalContext:
    environment_type: str
    risk_level: str
    mobility_relevance: str
    information_relevance: str
    social_relevance: str
    task_pressure: str
    uncertainty_level: str
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TaskClueCandidate:
    task_type: str
    priority: str
    reason: str
    evidence_refs: List[str]
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class MissingInformationCandidate:
    info_type: str
    required_for: str
    suggested_capability: str
    reason: str
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AttentionTargetHint:
    target_hint_id: str
    target_type: str
    priority: str
    reason: str
    region_ref_optional: str = ""
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ModelNeedHint:
    capability_type: str
    reason: str
    policy_ref: str
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SituationUncertainty:
    needs_user_goal: bool
    needs_manual_review: bool
    ambiguity_reason_optional: str = ""
    confidence_gap_optional: str = ""
    fallback_suggestion: str = ""
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SituationUnderstandingTrace:
    trace_id: str
    stage: str
    input_refs: List[str]
    output_refs: List[str]
    conflict_resolution_optional: str = ""
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SituationUnderstandingCandidate:
    situation_id: str
    scene_profile_candidate: Dict[str, Any]
    survival_context: Dict[str, Any]
    task_clue_candidates: List[Dict[str, Any]]
    missing_information_candidates: List[Dict[str, Any]]
    attention_target_hints: List[Dict[str, Any]]
    model_need_hints: Dict[str, List[Dict[str, Any]]]
    uncertainty: Dict[str, Any]
    trace_refs: List[Dict[str, Any]]
    candidate_only: bool = True
    not_fact: bool = True
    policy_refs: List[str] = field(default_factory=lambda: [POLICY_REF])
