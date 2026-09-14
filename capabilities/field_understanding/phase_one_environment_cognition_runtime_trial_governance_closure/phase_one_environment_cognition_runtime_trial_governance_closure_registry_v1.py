# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Runtime Trial Governance Closure — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_STAGES,
    build_controlled_trial_governance_lifecycle_template_matrix_v1,
)
from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_governance_closure.phase_one_environment_cognition_runtime_trial_governance_closure_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXECUTION_PLANNING_REF,
    FINAL_DECISION_GO,
    GOVERNANCE_CLOSURE_RULES,
    GOVERNANCE_CLOSURE_PRINCIPLE_ZH,
    GOVERNANCE_STAGE_GO_KEYS,
    GOVERNANCE_STAGE_REFS,
    ISSUANCE_PACKAGE_REF,
    OWNER_APPROVAL_ISSUANCE_REF,
    OWNER_APPROVAL_REQUEST_REF,
    PACKAGE_BOUNDARY_REF,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    PRE_RUNTIME_TRIAL_PACKAGE_REF,
    PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
    PhaseOneRuntimeTrialGovernanceClosure,
    PhaseOneRuntimeTrialGovernanceClosureDecision,
    PhaseOneRuntimeTrialGovernanceCoverage,
    PhaseOneRuntimeTrialGovernanceReuseBinding,
    PhaseOneRuntimeTrialGovernanceStageRef,
    RUNTIME_TRIAL_MODE,
    SCENARIO_COVERAGE_GO_KEYS,
    SCENARIO_COVERAGE_REFS,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    candidate_to_dict,
)

REGISTRY_ID = "phase_one_environment_cognition_runtime_trial_governance_closure_registry_v1"
CLOSURE_REF = "phase_one_runtime_trial_governance_closure_v1"

_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_planning_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_planning_review_v1.json"
)
_REQUEST_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_owner_approval_request_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_owner_approval_request_review_v1.json"
)
_OWNER_ISSUANCE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_owner_approval_issuance_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_review_v1.json"
)
_PACKAGE_BOUNDARY_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_package_boundary_planning_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_package_boundary_planning_review_v1.json"
)
_CLOSURE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1.json"
)
_ISSUANCE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_issuance_package_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_issuance_package_review_v1.json"
)
_EXECUTION_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_execution_planning_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_execution_planning_review_v1.json"
)
_CHAIN_CLOSURE_ARTIFACT_REL = (
    "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
    "field_task_guidance_safety_chain_closure_review_v1.json"
)

_GOVERNANCE_STAGE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "stage_ref": "phase_one_chain_closure",
        "phase_ref": PHASE_ONE_CHAIN_REF,
        "template_stage_id": "chain_closure",
        "expected_final_decision": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "expected_status": "chain_status=sealed",
        "artifact_rel": _CHAIN_CLOSURE_ARTIFACT_REL,
        "module_rel": (
            "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
            "field_task_guidance_safety_chain_closure_types_v1.py"
        ),
        "go_key": "phase_one_chain_closure_go_verified",
    },
    {
        "stage_ref": "controlled_runtime_trial_planning",
        "phase_ref": PLANNING_REF,
        "template_stage_id": "trial_planning",
        "expected_final_decision": "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PLANNING_GO",
        "expected_status": "trial_planning_go",
        "artifact_rel": _PLANNING_ARTIFACT_REL,
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_planning/"
            "phase_one_environment_cognition_runtime_trial_planning_types_v1.py"
        ),
        "go_key": "controlled_runtime_trial_planning_go_verified",
    },
    {
        "stage_ref": "owner_approval_request",
        "phase_ref": OWNER_APPROVAL_REQUEST_REF,
        "template_stage_id": "owner_approval_request",
        "expected_final_decision": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_REQUEST_GO"
        ),
        "expected_status": "owner_approval_request_go",
        "artifact_rel": _REQUEST_ARTIFACT_REL,
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_request/"
            "phase_one_environment_cognition_runtime_trial_owner_approval_request_types_v1.py"
        ),
        "go_key": "owner_approval_request_go_verified",
    },
    {
        "stage_ref": "owner_approval_issuance",
        "phase_ref": OWNER_APPROVAL_ISSUANCE_REF,
        "template_stage_id": "owner_approval_issuance",
        "expected_final_decision": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_ISSUANCE_GO"
        ),
        "expected_status": "owner_approval_issuance_go",
        "artifact_rel": _OWNER_ISSUANCE_ARTIFACT_REL,
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_issuance/"
            "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_types_v1.py"
        ),
        "go_key": "owner_approval_issuance_go_verified",
    },
    {
        "stage_ref": "package_boundary_planning",
        "phase_ref": PACKAGE_BOUNDARY_REF,
        "template_stage_id": "package_boundary",
        "expected_final_decision": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PACKAGE_BOUNDARY_PLANNING_GO"
        ),
        "expected_status": "package_boundary_go",
        "artifact_rel": _PACKAGE_BOUNDARY_ARTIFACT_REL,
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_boundary_planning/"
            "phase_one_environment_cognition_runtime_trial_package_boundary_planning_types_v1.py"
        ),
        "go_key": "package_boundary_planning_go_verified",
    },
    {
        "stage_ref": "package_closure_readiness",
        "phase_ref": PRE_RUNTIME_TRIAL_PACKAGE_REF,
        "template_stage_id": "pre_runtime_package_closure",
        "expected_final_decision": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PACKAGE_CLOSURE_READINESS_REVIEW_GO"
        ),
        "expected_status": "pre_runtime_trial_package_status=sealed",
        "artifact_rel": _CLOSURE_ARTIFACT_REL,
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_closure_readiness_review/"
            "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_types_v1.py"
        ),
        "go_key": "package_closure_readiness_go_verified",
        "require_pre_package_sealed": True,
    },
    {
        "stage_ref": "issuance_package",
        "phase_ref": ISSUANCE_PACKAGE_REF,
        "template_stage_id": "pre_runtime_package_closure",
        "expected_final_decision": "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_ISSUANCE_PACKAGE_GO",
        "expected_status": "issuance_package_go",
        "artifact_rel": _ISSUANCE_ARTIFACT_REL,
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_issuance_package/"
            "phase_one_environment_cognition_runtime_trial_issuance_package_types_v1.py"
        ),
        "go_key": "issuance_package_go_verified",
    },
    {
        "stage_ref": "execution_planning",
        "phase_ref": EXECUTION_PLANNING_REF,
        "template_stage_id": "execution_planning",
        "expected_final_decision": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_EXECUTION_PLANNING_GO"
        ),
        "expected_status": "execution_planning_go",
        "artifact_rel": _EXECUTION_PLANNING_ARTIFACT_REL,
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_execution_planning/"
            "phase_one_environment_cognition_runtime_trial_execution_planning_types_v1.py"
        ),
        "go_key": "execution_planning_go_verified",
    },
)

_SCENARIO_SPECS: Tuple[Dict[str, str], ...] = (
    {
        "scenario_ref": "mall_find_entrance",
        "plan_ref": "mall_find_entrance_execution_plan",
        "expected_scope": "low_risk_controlled_trial_candidate",
        "expected_execution_plan_status": "planned_candidate_replay_only",
        "go_key": "mall_find_entrance_scope_preserved",
    },
    {
        "scenario_ref": "subway_enter_station",
        "plan_ref": "subway_enter_station_execution_plan",
        "expected_scope": "cautious_candidate_trial",
        "expected_execution_plan_status": "planned_constrained_candidate_replay_only",
        "go_key": "subway_enter_station_scope_preserved",
    },
    {
        "scenario_ref": "stadium_concert_ticket_gate",
        "plan_ref": "stadium_concert_ticket_gate_execution_plan",
        "expected_scope": "observation_only",
        "expected_execution_plan_status": "planned_observation_replay_only",
        "go_key": "stadium_concert_observation_only_preserved",
    },
    {
        "scenario_ref": "plaza_market_crowd",
        "plan_ref": "plaza_market_crowd_execution_plan",
        "expected_scope": "observation_only",
        "expected_execution_plan_status": "planned_observation_replay_only",
        "go_key": "plaza_market_observation_only_preserved",
    },
    {
        "scenario_ref": "gps_slam_conflict",
        "plan_ref": "gps_slam_conflict_execution_plan",
        "expected_scope": "blocked",
        "expected_execution_plan_status": "blocked_no_execution_plan",
        "go_key": "gps_slam_conflict_blocked_preserved",
    },
    {
        "scenario_ref": "home_return",
        "plan_ref": "home_return_execution_plan",
        "expected_scope": "low_risk_controlled_trial_candidate",
        "expected_execution_plan_status": "planned_candidate_replay_only",
        "go_key": "home_return_scope_preserved",
    },
)

_MIDPLATFORM_UPSTREAM_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/provider_manager_runtime_skeleton_dryrun_v1_smoke_v0/"
            "provider_manager_runtime_skeleton_verification_and_review_v1.json"
        ),
        "expected_go": "PROVIDER_MANAGER_RUNTIME_SKELETON_POST_DRYRUN_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/provider_manager_runtime_skeleton/"
            "provider_manager_runtime_skeleton_types_v1.py"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/task_manager_owner_approval_request_module_handoff_v1_smoke_v0/"
            "owner_approval_request_module_handoff_report_v1.json"
        ),
        "expected_go": (
            "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_"
            "READY_FOR_BROADER_MIDPLATFORM_TASK_MANAGER_CLOSURE_ROADMAP"
        ),
        "module_rel": (
            "capabilities/midplatform/task_manager_owner_approval_request_module_handoff_v1.py"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "module_rel": (
            "capabilities/midplatform/interface_layer_governance/"
            "interface_layer_governance_types_v1.py"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/model_admission_governance/"
            "model_admission_governance_types_v1.py"
        ),
    },
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "governance_stage_refs": GOVERNANCE_STAGE_REFS,
    "governance_stage_go_keys": GOVERNANCE_STAGE_GO_KEYS,
    "scenario_coverage_refs": SCENARIO_COVERAGE_REFS,
    "scenario_coverage_go_keys": SCENARIO_COVERAGE_GO_KEYS,
    "governance_closure_rules": GOVERNANCE_CLOSURE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
    "template_stages": TEMPLATE_STAGES,
}


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(GOVERNANCE_STAGE_REFS) != 8:
        issues.append("governance_stage_refs_count_not_8")
    if len(GOVERNANCE_STAGE_GO_KEYS) != 8:
        issues.append("governance_stage_go_keys_count_not_8")
    if len(SCENARIO_COVERAGE_REFS) != 6:
        issues.append("scenario_coverage_refs_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 12:
        issues.append("sealed_upstream_phase_refs_count_not_12")
    if len(GOVERNANCE_CLOSURE_RULES) != 13:
        issues.append("governance_closure_rules_count_not_13")
    if len(_GOVERNANCE_STAGE_SPECS) != 8:
        issues.append("governance_stage_specs_count_not_8")
    return len(issues) == 0, issues


def build_governance_closure_v1() -> PhaseOneRuntimeTrialGovernanceClosure:
    return PhaseOneRuntimeTrialGovernanceClosure(
        closure_ref=CLOSURE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        pre_runtime_trial_package_status=PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
        phase_one_chain_status=PHASE_ONE_CHAIN_STATUS,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        governance_stage_refs=GOVERNANCE_STAGE_REFS,
        scenario_coverage_refs=SCENARIO_COVERAGE_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=GOVERNANCE_CLOSURE_RULES,
        candidate_only_source_chain_required=CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    )


def build_governance_stage_refs_v1() -> Tuple[PhaseOneRuntimeTrialGovernanceStageRef, ...]:
    return tuple(
        PhaseOneRuntimeTrialGovernanceStageRef(
            stage_ref=spec["stage_ref"],
            phase_ref=spec["phase_ref"],
            template_stage_id=spec["template_stage_id"],
            expected_final_decision=spec["expected_final_decision"],
            expected_status=spec["expected_status"],
            source_chain=SOURCE_CHAIN,
            stage_verified=True,
        )
        for spec in _GOVERNANCE_STAGE_SPECS
    )


def build_scenario_coverage_v1() -> Tuple[PhaseOneRuntimeTrialGovernanceCoverage, ...]:
    return tuple(
        PhaseOneRuntimeTrialGovernanceCoverage(
            scenario_ref=spec["scenario_ref"],
            expected_scope=spec["expected_scope"],
            expected_execution_plan_status=spec["expected_execution_plan_status"],
            scope_preserved=True,
            source_chain=SOURCE_CHAIN,
        )
        for spec in _SCENARIO_SPECS
    )


def build_reuse_binding_v1() -> PhaseOneRuntimeTrialGovernanceReuseBinding:
    return PhaseOneRuntimeTrialGovernanceReuseBinding(
        binding_ref="phase_one_environment_cognition_governance_reuse_binding_v1",
        governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        reuse_profile_id="phase_one_environment_cognition_controlled_trial_governance_reuse_v1",
        target_domain="phase_one_environment_cognition",
        future_governance_reuse_template_required=True,
        execution_planning_marked_terminal_for_planning_only_chain=True,
        no_further_gate_package_issuance_split_required=True,
        template_supports_compressed_mode=True,
        source_chain=SOURCE_CHAIN,
    )


def build_governance_closure_decision_v1(
    *,
    all_governance_stage_refs_verified: bool,
    pre_runtime_package_sealed: bool,
    scenario_scope_preserved_for_all: bool,
) -> PhaseOneRuntimeTrialGovernanceClosureDecision:
    return PhaseOneRuntimeTrialGovernanceClosureDecision(
        decision_ref="phase_one_runtime_trial_governance_closure_decision_v1",
        closure_ref=CLOSURE_REF,
        governance_closure_profile_count=1,
        controlled_trial_governance_template_created=True,
        controlled_trial_governance_template_stage_count=len(TEMPLATE_STAGES),
        governance_stage_ref_count=len(GOVERNANCE_STAGE_REFS),
        all_governance_stage_refs_verified=all_governance_stage_refs_verified,
        pre_runtime_package_sealed=pre_runtime_package_sealed,
        scenario_scope_preserved_for_all=scenario_scope_preserved_for_all,
        final_decision=FINAL_DECISION_GO,
    )


def build_governance_stage_go_map(
    stage_refs: Tuple[PhaseOneRuntimeTrialGovernanceStageRef, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for spec, stage in zip(_GOVERNANCE_STAGE_SPECS, stage_refs):
        result[spec["go_key"]] = stage.stage_verified is True
    return result


def build_scenario_coverage_go_map(
    coverage: Tuple[PhaseOneRuntimeTrialGovernanceCoverage, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for spec, item in zip(_SCENARIO_SPECS, coverage):
        result[spec["go_key"]] = (
            item.scope_preserved is True
            and item.expected_scope == spec["expected_scope"]
            and item.expected_execution_plan_status == spec["expected_execution_plan_status"]
        )
    return result


def build_phase_one_environment_cognition_runtime_trial_governance_closure_matrix_v1() -> Dict[str, Any]:
    template_matrix = build_controlled_trial_governance_lifecycle_template_matrix_v1()
    closure = build_governance_closure_v1()
    stage_refs = build_governance_stage_refs_v1()
    coverage = build_scenario_coverage_v1()
    reuse_binding = build_reuse_binding_v1()
    decision = build_governance_closure_decision_v1(
        all_governance_stage_refs_verified=True,
        pre_runtime_package_sealed=True,
        scenario_scope_preserved_for_all=True,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "governance_closure_principle_zh": GOVERNANCE_CLOSURE_PRINCIPLE_ZH,
        "phase_one_runtime_trial_governance_closure": candidate_to_dict(closure),
        "governance_stage_refs": [candidate_to_dict(s) for s in stage_refs],
        "scenario_coverage": [candidate_to_dict(c) for c in coverage],
        "reuse_binding": candidate_to_dict(reuse_binding),
        "governance_closure_decision": candidate_to_dict(decision),
        "governance_stage_go_map": build_governance_stage_go_map(stage_refs),
        "scenario_coverage_go_map": build_scenario_coverage_go_map(coverage),
        "controlled_trial_governance_template_matrix": template_matrix,
        "governance_stage_specs": list(_GOVERNANCE_STAGE_SPECS),
        "midplatform_upstream_specs": list(_MIDPLATFORM_UPSTREAM_SPECS),
        "execution_planning_artifact_rel": _EXECUTION_PLANNING_ARTIFACT_REL,
        "governance_closure_rules": list(GOVERNANCE_CLOSURE_RULES),
        "next_phase_ref": "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-Planning-v1-001",
    }
