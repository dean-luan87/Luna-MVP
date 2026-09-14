# -*- coding: utf-8
"""Network-Assisted Situation Learning — planning types v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

PHASE_REF = "Phase-P1-Midplatform-Network-Assisted-Situation-Learning-Planning-v1-001"
SYSTEM_ID = "LunaMidplatformNetworkAssistedSituationLearningPlanningV1"
PLANNING_ONLY = True

UPSTREAM_GO = (
    "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_GO",
    "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_GO",
    "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_GO",
)

PLANNING_ENDPOINT = "situation_training_dataset_candidate"

SOURCE_TYPES = (
    "web_reference",
    "teacher_model",
    "human_correction",
    "test_trace",
    "synthetic_case",
    "internal_policy",
)

TRUST_TIERS = ("high", "medium", "low", "unknown")

REVIEW_STATUSES = (
    "pending_policy_review",
    "policy_accepted",
    "policy_rejected",
    "pending_human_review",
    "accepted_as_case",
    "rejected",
    "pending_human_approval",
)

CASE_TYPES = (
    "shopfront_sign",
    "subway_platform",
    "street_crossing",
    "corridor",
    "indoor_store",
    "unknown_scene",
    "custom",
)

SMOKE_CASE_IDS = (
    "case_a_teacher_shopfront_sign",
    "case_b_teacher_bad_slam_for_text",
    "case_c_web_reference_candidate",
    "case_d_human_correction",
    "case_e_test_trace_regression",
    "case_f_training_dataset_candidate",
)

OBJECT_TYPES = (
    "ExternalLearningSource",
    "TeacherModelLabelCandidate",
    "WebReferenceCandidate",
    "HumanCorrectionLearningSignal",
    "TestTraceLearningSignal",
    "SituationLearningCandidate",
    "SituationCaseRecord",
    "SituationTrainingDatasetCandidate",
    "LearningPolicyReviewResult",
    "LearningProvenanceRecord",
    "LearningRiskFlag",
)

COMMON_LEARNING_OBJECT_FIELDS = (
    "candidate_only",
    "not_fact",
    "source_ref",
    "provenance_ref",
    "review_status",
    "created_from",
    "policy_refs",
    "trace_refs",
)

POLICY_REF = "network_assisted_situation_learning_policy_v1"


def learning_object_base(
    *,
    source_ref: str,
    provenance_ref: str,
    created_from: str,
    review_status: str = "pending_policy_review",
    policy_refs: Optional[List[str]] = None,
    trace_refs: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Shared metadata envelope for all network-assisted learning objects."""
    return {
        "candidate_only": True,
        "not_fact": True,
        "source_ref": source_ref,
        "provenance_ref": provenance_ref,
        "review_status": review_status,
        "created_from": created_from,
        "policy_refs": policy_refs or [POLICY_REF],
        "trace_refs": trace_refs or [{"stage": created_from, "ref": source_ref}],
    }


@dataclass
class LearningRiskFlag:
    flag_id: str
    risk_type: str
    severity: str
    description: str
    candidate_only: bool = True
    not_fact: bool = True
    source_ref: str = ""
    provenance_ref: str = ""
    review_status: str = "pending_policy_review"
    created_from: str = "policy_reviewer"
    policy_refs: List[str] = field(default_factory=lambda: [POLICY_REF])
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)

FINAL_GO = "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_BLOCKED"
SMOKE_GO = "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_SMOKE_GO"
SMOKE_BLOCKED = "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_SMOKE_BLOCKED"

RECOMMENDED_NEXT_PHASES = (
    "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-Planning-v1-001",
    "Phase-P1-Midplatform-Third-Party-Teacher-Model-Adapter-Planning-v1-001",
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "candidate_only": True,
    "all_outputs_candidate_only": True,
    "no_direct_web_training": True,
    "no_direct_teacher_weight_update": True,
    "teacher_output_candidate_only": True,
    "web_reference_candidate_only": True,
    "learning_candidate_not_fact": True,
    "case_record_not_fact": True,
    "no_runner_invocation_from_learning_candidate": True,
    "no_tool_install_from_learning_candidate": True,
    "no_fact_admission_bypass": True,
    "deterministic_smoke_only": True,
}
