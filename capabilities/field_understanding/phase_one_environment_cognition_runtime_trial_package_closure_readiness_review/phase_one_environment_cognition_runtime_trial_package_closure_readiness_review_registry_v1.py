# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Package Closure Readiness Review — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_package_closure_readiness_review.phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    CLOSURE_GOVERNANCE_RULES,
    CLOSURE_STAGE_REFS,
    FINAL_DECISION_GO,
    OWNER_APPROVAL_ISSUANCE_REF,
    OWNER_APPROVAL_REQUEST_REF,
    PACKAGE_BOUNDARY_REF,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    PRE_RUNTIME_TRIAL_CHAIN_REFS,
    RUNTIME_TRIAL_MODE,
    SCENARIO_READINESS_GO_KEYS,
    SCENARIO_READINESS_REFS,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    UNIVERSAL_BLOCKED_OPERATIONS,
    RuntimeTrialPackageBoundaryReadiness,
    RuntimeTrialPackageClosureReadinessDecision,
    RuntimeTrialPackageClosureReadinessProfile,
    RuntimeTrialPackageClosureStageRef,
    RuntimeTrialPackageGovernanceReadiness,
    RuntimeTrialPackageScenarioReadiness,
    candidate_to_dict,
)

REGISTRY_ID = "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_registry_v1"
PROFILE_REF = "runtime_trial_package_closure_readiness_profile_v1"
ROLLBACK_POLICY_REF = "runtime_trial_rollback_v1"
OBSERVATION_LOG_POLICY_REF = "runtime_trial_observation_log_v1"
FAILURE_HANDLING_POLICY_REF = "runtime_trial_failure_handling_policy_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "closure_stage_refs": CLOSURE_STAGE_REFS,
    "scenario_readiness_refs": SCENARIO_READINESS_REFS,
    "scenario_readiness_go_keys": SCENARIO_READINESS_GO_KEYS,
    "closure_governance_rules": CLOSURE_GOVERNANCE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
    "universal_blocked_operations": UNIVERSAL_BLOCKED_OPERATIONS,
}

_SCENARIO_GO_KEY_MAP: Dict[str, str] = {
    "mall_find_entrance_package": "mall_find_entrance_ready_for_pre_runtime_trial_review",
    "subway_enter_station_package": "subway_enter_station_ready_with_constraints",
    "stadium_concert_ticket_gate_package": "stadium_concert_observation_only_ready",
    "plaza_market_crowd_package": "plaza_market_observation_only_ready",
    "gps_slam_conflict_package": "gps_slam_conflict_blocked_preserved",
    "home_return_package": "home_return_ready_for_pre_runtime_trial_review",
}

_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_planning_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_planning_review_v1.json"
)

_REQUEST_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_owner_approval_request_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_owner_approval_request_review_v1.json"
)

_ISSUANCE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_owner_approval_issuance_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_review_v1.json"
)

_PACKAGE_BOUNDARY_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_package_boundary_planning_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_package_boundary_planning_review_v1.json"
)

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": PLANNING_REF,
        "artifact_rel": _PLANNING_ARTIFACT_REL,
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_planning/"
            "phase_one_environment_cognition_runtime_trial_planning_types_v1.py"
        ),
        "require_go": True,
        "stage_ref": "planning_stage_closed",
    },
    {
        "phase_ref": OWNER_APPROVAL_REQUEST_REF,
        "artifact_rel": _REQUEST_ARTIFACT_REL,
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_REQUEST_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_request/"
            "phase_one_environment_cognition_runtime_trial_owner_approval_request_types_v1.py"
        ),
        "require_go": True,
        "stage_ref": "owner_approval_request_stage_closed",
    },
    {
        "phase_ref": OWNER_APPROVAL_ISSUANCE_REF,
        "artifact_rel": _ISSUANCE_ARTIFACT_REL,
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_ISSUANCE_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_issuance/"
            "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_types_v1.py"
        ),
        "require_go": True,
        "stage_ref": "owner_approval_issuance_stage_closed",
    },
    {
        "phase_ref": PACKAGE_BOUNDARY_REF,
        "artifact_rel": _PACKAGE_BOUNDARY_ARTIFACT_REL,
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PACKAGE_BOUNDARY_PLANNING_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_boundary_planning/"
            "phase_one_environment_cognition_runtime_trial_package_boundary_planning_types_v1.py"
        ),
        "require_go": True,
        "stage_ref": "package_boundary_stage_closed",
    },
    {
        "phase_ref": PHASE_ONE_CHAIN_REF,
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
            "field_task_guidance_safety_chain_closure_types_v1.py"
        ),
        "require_go": True,
        "require_sealed": True,
    },
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
        "require_go": True,
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
        "require_go": True,
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
        "require_go": True,
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
        "require_go": True,
    },
)

_STAGE_REQUIRED_CHECKS: Dict[str, Tuple[str, ...]] = {
    "planning_stage_closed": (
        "planning_go_verified",
        "admission_level_declared_for_all",
        "rollback_policy_required",
        "observation_log_policy_required",
        "owner_approval_required",
        "runtime_activation_allowed_false",
    ),
    "owner_approval_request_stage_closed": (
        "request_go_verified",
        "admission_level_preserved_for_all",
        "blocked_scenario_not_requestable",
        "observation_only_not_movement_trial",
        "owner_approval_issued_false",
    ),
    "owner_approval_issuance_stage_closed": (
        "issuance_go_verified",
        "request_scope_preserved_for_all",
        "blocked_scenario_not_issued",
        "observation_only_not_upgraded",
        "issuance_not_runtime_activation",
    ),
    "package_boundary_stage_closed": (
        "package_boundary_go_verified",
        "package_scope_preserved_for_all",
        "issued_status_preserved_for_all",
        "blocked_operations_declared_for_all",
        "allowed_operations_candidate_only",
        "trial_runtime_started_false",
    ),
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(CLOSURE_STAGE_REFS) != 4:
        issues.append("closure_stage_refs_count_not_4")
    if len(SCENARIO_READINESS_REFS) != 6:
        issues.append("scenario_readiness_refs_count_not_6")
    if len(SCENARIO_READINESS_GO_KEYS) != 6:
        issues.append("scenario_readiness_go_keys_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 9:
        issues.append("sealed_upstream_phase_refs_count_not_9")
    if len(CLOSURE_GOVERNANCE_RULES) != 13:
        issues.append("closure_governance_rules_count_not_13")
    return len(issues) == 0, issues


def build_closure_stages_v1() -> Tuple[RuntimeTrialPackageClosureStageRef, ...]:
    return (
        RuntimeTrialPackageClosureStageRef(
            stage_ref="planning_stage_closed",
            phase_ref=PLANNING_REF,
            stage_zh="Controlled Runtime Trial Planning 已封存",
            required_checks=_STAGE_REQUIRED_CHECKS["planning_stage_closed"],
            stage_closed=True,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialPackageClosureStageRef(
            stage_ref="owner_approval_request_stage_closed",
            phase_ref=OWNER_APPROVAL_REQUEST_REF,
            stage_zh="Owner Approval Request 已封存",
            required_checks=_STAGE_REQUIRED_CHECKS["owner_approval_request_stage_closed"],
            stage_closed=True,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialPackageClosureStageRef(
            stage_ref="owner_approval_issuance_stage_closed",
            phase_ref=OWNER_APPROVAL_ISSUANCE_REF,
            stage_zh="Owner Approval Issuance 已封存",
            required_checks=_STAGE_REQUIRED_CHECKS["owner_approval_issuance_stage_closed"],
            stage_closed=True,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialPackageClosureStageRef(
            stage_ref="package_boundary_stage_closed",
            phase_ref=PACKAGE_BOUNDARY_REF,
            stage_zh="Trial Package Boundary Planning 已封存",
            required_checks=_STAGE_REQUIRED_CHECKS["package_boundary_stage_closed"],
            stage_closed=True,
            source_chain=SOURCE_CHAIN,
        ),
    )


def build_scenario_readiness_v1() -> Tuple[RuntimeTrialPackageScenarioReadiness, ...]:
    return (
        RuntimeTrialPackageScenarioReadiness(
            scenario_ref="mall_find_entrance_package",
            package_ref="mall_find_entrance_package",
            readiness_status="ready_for_pre_runtime_trial_review",
            package_scope="low_risk_controlled_trial_candidate",
            readiness_constraints=(
                "candidate_only_operations",
                "action_safety_candidate_required",
                "speech_gate_candidate_required",
                "rollback_logging_failure_handling_bound",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=PRE_RUNTIME_TRIAL_CHAIN_REFS,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialPackageScenarioReadiness(
            scenario_ref="subway_enter_station_package",
            package_ref="subway_enter_station_package",
            readiness_status="ready_with_constraints_for_pre_runtime_trial_review",
            package_scope="cautious_candidate_trial",
            readiness_constraints=(
                "gps_degraded_acknowledged",
                "local_spatial_evidence_required",
                "indoor_uncertainty_downgrade",
                "more_evidence_required_before_action_like_guidance",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=PRE_RUNTIME_TRIAL_CHAIN_REFS,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialPackageScenarioReadiness(
            scenario_ref="stadium_concert_ticket_gate_package",
            package_ref="stadium_concert_ticket_gate_package",
            readiness_status="observation_only_ready",
            package_scope="observation_only",
            readiness_constraints=(
                "no_movement_command",
                "crowd_flow_risk_required",
                "event_overlay_does_not_rewrite_map_place_ref",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=PRE_RUNTIME_TRIAL_CHAIN_REFS,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialPackageScenarioReadiness(
            scenario_ref="plaza_market_crowd_package",
            package_ref="plaza_market_crowd_package",
            readiness_status="observation_only_ready",
            package_scope="observation_only",
            readiness_constraints=(
                "crowd_queue_risk_observation_only",
                "movement_guidance_blocked",
                "temporary_layout_uncertainty_logged",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=PRE_RUNTIME_TRIAL_CHAIN_REFS,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialPackageScenarioReadiness(
            scenario_ref="gps_slam_conflict_package",
            package_ref="gps_slam_conflict_package",
            readiness_status="blocked_preserved",
            package_scope="blocked",
            readiness_constraints=(
                "unresolved_conflict_blocks_trial",
                "no_route_activation",
                "no_action_like_guidance",
                "requires_conflict_resolution_planning",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=PRE_RUNTIME_TRIAL_CHAIN_REFS,
            source_chain=SOURCE_CHAIN,
            readiness_ok=False,
        ),
        RuntimeTrialPackageScenarioReadiness(
            scenario_ref="home_return_package",
            package_ref="home_return_package",
            readiness_status="ready_for_pre_runtime_trial_review",
            package_scope="low_risk_controlled_trial_candidate",
            readiness_constraints=(
                "coarse_map_route_candidate",
                "local_spatial_check_candidate",
                "rollback_logging_failure_handling_bound",
                "no_fact_write",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=PRE_RUNTIME_TRIAL_CHAIN_REFS,
            source_chain=SOURCE_CHAIN,
        ),
    )


def build_governance_readiness_v1() -> RuntimeTrialPackageGovernanceReadiness:
    return RuntimeTrialPackageGovernanceReadiness(
        readiness_ref="runtime_trial_package_governance_readiness_v1",
        scenario_scope_preserved_for_all=True,
        blocked_scenario_remains_blocked=True,
        observation_only_not_upgraded=True,
        constrained_item_constraints_preserved=True,
        low_risk_candidates_do_not_start_runtime=True,
        allowed_operations_candidate_only=True,
        source_chain_required=True,
        upstream_refs_required=True,
        source_chain=SOURCE_CHAIN,
    )


def build_boundary_readiness_v1() -> RuntimeTrialPackageBoundaryReadiness:
    return RuntimeTrialPackageBoundaryReadiness(
        readiness_ref="runtime_trial_package_boundary_readiness_v1",
        blocked_operations_declared_for_all=True,
        direct_action_blocked_for_all=True,
        direct_speech_blocked_for_all=True,
        direct_fact_write_blocked_for_all=True,
        real_navigation_blocked_for_all=True,
        live_sensor_trigger_blocked_for_all=True,
        source_chain=SOURCE_CHAIN,
    )


def build_closure_profile_v1() -> RuntimeTrialPackageClosureReadinessProfile:
    return RuntimeTrialPackageClosureReadinessProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        pre_runtime_trial_chain_refs=PRE_RUNTIME_TRIAL_CHAIN_REFS,
        phase_one_chain_ref=PHASE_ONE_CHAIN_REF,
        phase_one_chain_status=PHASE_ONE_CHAIN_STATUS,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        closure_stage_refs=CLOSURE_STAGE_REFS,
        scenario_readiness_refs=SCENARIO_READINESS_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=CLOSURE_GOVERNANCE_RULES,
        candidate_only_source_chain_required=CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    )


def build_scenario_readiness_go_map(
    scenarios: Tuple[RuntimeTrialPackageScenarioReadiness, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for scenario in scenarios:
        go_key = _SCENARIO_GO_KEY_MAP[scenario.scenario_ref]
        if go_key == "gps_slam_conflict_blocked_preserved":
            result[go_key] = (
                scenario.readiness_status == "blocked_preserved"
                and scenario.package_scope == "blocked"
            )
        elif go_key == "subway_enter_station_ready_with_constraints":
            result[go_key] = (
                scenario.readiness_status == "ready_with_constraints_for_pre_runtime_trial_review"
                and bool(scenario.readiness_constraints)
            )
        elif go_key.endswith("_observation_only_ready"):
            result[go_key] = (
                scenario.readiness_status == "observation_only_ready"
                and scenario.package_scope == "observation_only"
            )
        else:
            result[go_key] = scenario.readiness_status == "ready_for_pre_runtime_trial_review"
    return result


def build_closure_decision_v1(
    *,
    planning_go_verified: bool,
    owner_approval_request_go_verified: bool,
    owner_approval_issuance_go_verified: bool,
    package_boundary_go_verified: bool,
    sealed_phase_one_chain_verified: bool,
) -> RuntimeTrialPackageClosureReadinessDecision:
    return RuntimeTrialPackageClosureReadinessDecision(
        decision_ref="runtime_trial_package_closure_readiness_decision_v1",
        profile_ref=PROFILE_REF,
        closure_readiness_profile_count=1,
        closure_stage_count=len(CLOSURE_STAGE_REFS),
        scenario_readiness_count=len(SCENARIO_READINESS_REFS),
        planning_go_verified=planning_go_verified,
        owner_approval_request_go_verified=owner_approval_request_go_verified,
        owner_approval_issuance_go_verified=owner_approval_issuance_go_verified,
        package_boundary_go_verified=package_boundary_go_verified,
        sealed_phase_one_chain_verified=sealed_phase_one_chain_verified,
        final_decision=FINAL_DECISION_GO,
    )


def build_phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_matrix_v1() -> Dict[str, Any]:
    profile = build_closure_profile_v1()
    stages = build_closure_stages_v1()
    scenarios = build_scenario_readiness_v1()
    governance = build_governance_readiness_v1()
    boundary = build_boundary_readiness_v1()
    decision = build_closure_decision_v1(
        planning_go_verified=True,
        owner_approval_request_go_verified=True,
        owner_approval_issuance_go_verified=True,
        package_boundary_go_verified=True,
        sealed_phase_one_chain_verified=True,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "closure_readiness_profile": candidate_to_dict(profile),
        "closure_stages": [candidate_to_dict(s) for s in stages],
        "scenario_readiness": [candidate_to_dict(s) for s in scenarios],
        "governance_readiness": candidate_to_dict(governance),
        "boundary_readiness": candidate_to_dict(boundary),
        "closure_decision": candidate_to_dict(decision),
        "scenario_readiness_go_map": build_scenario_readiness_go_map(scenarios),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "stage_required_checks": {k: list(v) for k, v in _STAGE_REQUIRED_CHECKS.items()},
        "pre_runtime_trial_chain_artifacts": {
            "planning": _PLANNING_ARTIFACT_REL,
            "request": _REQUEST_ARTIFACT_REL,
            "issuance": _ISSUANCE_ARTIFACT_REL,
            "package_boundary": _PACKAGE_BOUNDARY_ARTIFACT_REL,
        },
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "universal_blocked_operations": list(UNIVERSAL_BLOCKED_OPERATIONS),
    }
