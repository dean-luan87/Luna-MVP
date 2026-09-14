# -*- coding: utf-8
"""Third-Party Teacher Adapter — planning types v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

PHASE_REF = "Phase-P1-Midplatform-Third-Party-Teacher-Adapter-Planning-v1-001"
SYSTEM_ID = "LunaThirdPartyTeacherAdapterPlanningV1"
PLANNING_ONLY = True
LAYER_ID = "Teacher_Adapter"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_PLANNING_GO",
    "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_DRYRUN_GO",
)

POLICY_REF = "luna_teacher_adapter_policy_v1"

TEACHER_ROLES = (
    "perception_teacher",
    "planning_teacher",
    "learning_teacher",
)

TEACHER_PROVIDERS = (
    "gemini",
    "qwen_vl",
    "gpt_vision",
    "internvl",
    "teacher_stub",
)

TASK_TYPES = (
    "scene_hypothesis",
    "alternative_plan",
    "learning_case",
    "visual_evidence",
    "uncertainty_reduction",
)

REQUIRED_OUTPUT_TYPES = (
    "teacher_evidence_candidate",
    "scene_hypothesis_candidate",
    "alternative_plan_candidate",
    "learning_candidate",
    "noop",
)

ADMISSION_STATUSES = (
    "admitted",
    "noop",
    "rejected",
)

TEACHER_VALIDATION_STATUSES = (
    "accepted_as_evidence",
    "accepted_as_alternative",
    "rejected_by_policy",
    "insufficient_information",
    "requires_human_review",
)

SPECIALIZED_TOOLS = (
    "ocr", "detection", "sam", "slam", "depth", "tracking",
)

SMOKE_CASE_IDS = (
    "case_a_shopfront_ocr_no_teacher",
    "case_b_unknown_scene_teacher_candidate",
    "case_c_planning_conflict_alternative_only",
    "case_d_bad_teacher_policy_reject",
    "case_e_learning_teacher_candidate_chain",
)

DRYRUN_CASE_IDS = (
    "case_a_teacher_supports_ocr_plan",
    "case_b_teacher_slam_rejected",
    "case_c_teacher_alternative_keep_plan",
    "case_d_teacher_wrong_scene_rejected",
    "case_e_learning_case_no_training",
)

FINAL_GO = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_BLOCKED"
DRYRUN_GO = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_DRYRUN_GO"
DRYRUN_BLOCKED = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_DRYRUN_BLOCKED"
SMOKE_GO = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_SMOKE_GO"
SMOKE_BLOCKED = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_SMOKE_BLOCKED"

RECOMMENDED_NEXT_PHASES = (
    "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-DryRun-v1-001",
)
RECOMMENDED_NEXT_PHASE = RECOMMENDED_NEXT_PHASES[0]

BOUNDARY_FLAGS = {
    "planning_only": True,
    "candidate_only": True,
    "teacher_evidence_not_fact": True,
    "no_direct_l1_scene_override": True,
    "no_direct_l2_selected_plan_override": True,
    "no_runner_invocation": True,
    "no_tool_execution": True,
    "no_fact_write": True,
    "no_direct_training": True,
    "teacher_admission_required": True,
    "specialized_tool_preferred_over_vlm": True,
    "alternative_plan_only": True,
    "learning_requires_policy_review": True,
    "deterministic_smoke_only": True,
    "no_real_network": True,
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
class TeacherAdapterInput:
    situation_understanding_candidate: Dict[str, Any]
    agent_plan_candidate_optional: Optional[Dict[str, Any]]
    available_capabilities: List[Dict[str, Any]]
    policy_context: Dict[str, Any]
    task_type: str
    required_output_type: str
    input_evidence: List[Dict[str, Any]]
    candidate_only: bool = True
    not_fact: bool = True


@dataclass
class TeacherAdmissionDecision:
    should_request_teacher: bool
    admission_status: str
    teacher_role: str
    preferred_provider: str
    noop_reason: str
    reject_reason: str
    policy_refs: List[str]
    candidate_only: bool = True
    not_fact: bool = True


@dataclass
class TeacherEvidenceCandidate:
    evidence_id: str
    teacher_role: str
    provider_id: str
    task_type: str
    output_type: str
    perception_output_optional: Optional[Dict[str, Any]]
    planning_output_optional: Optional[Dict[str, Any]]
    learning_output_optional: Optional[Dict[str, Any]]
    confidence: float
    candidate_only: bool = True
    not_fact: bool = True
    requires_policy_review: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)
