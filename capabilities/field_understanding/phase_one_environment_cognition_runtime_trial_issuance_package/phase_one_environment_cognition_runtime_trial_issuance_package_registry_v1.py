# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Issuance Package — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_issuance_package.phase_one_environment_cognition_runtime_trial_issuance_package_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    CLOSURE_SCENARIO_REF_MAP,
    ControlledRuntimeTrialIssuancePackageDecision,
    ControlledRuntimeTrialIssuancePackageItem,
    ControlledRuntimeTrialIssuancePackageProfile,
    FINAL_DECISION_GO,
    ISSUANCE_PACKAGE_GOVERNANCE_RULES,
    ISSUANCE_PACKAGE_GO_KEYS,
    ISSUANCE_PACKAGE_ITEM_REFS,
    IssuedTrialPackageAuditRecord,
    IssuedTrialPackageBlockerRecord,
    IssuedTrialPackageControlBinding,
    NEXT_PHASE_REF,
    OWNER_APPROVAL_ISSUANCE_REF,
    OWNER_APPROVAL_REQUEST_REF,
    PACKAGE_BOUNDARY_REF,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    PRE_RUNTIME_TRIAL_PACKAGE_REF,
    PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
    RUNTIME_TRIAL_MODE,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    UNIVERSAL_BLOCKED_OPERATIONS,
    candidate_to_dict,
)

REGISTRY_ID = "phase_one_environment_cognition_runtime_trial_issuance_package_registry_v1"
PROFILE_REF = "controlled_runtime_trial_issuance_package_profile_v1"
ROLLBACK_POLICY_REF = "runtime_trial_rollback_v1"
OBSERVATION_LOG_POLICY_REF = "runtime_trial_observation_log_v1"
FAILURE_HANDLING_POLICY_REF = "runtime_trial_failure_handling_policy_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "issuance_package_item_refs": ISSUANCE_PACKAGE_ITEM_REFS,
    "issuance_package_go_keys": ISSUANCE_PACKAGE_GO_KEYS,
    "issuance_package_governance_rules": ISSUANCE_PACKAGE_GOVERNANCE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
    "universal_blocked_operations": UNIVERSAL_BLOCKED_OPERATIONS,
}

_PACKAGE_GO_KEY_MAP: Dict[str, Tuple[str, str]] = {
    "mall_find_entrance_issuance_package": (
        "mall_find_entrance_packaged_for_trial_execution_planning",
        "packaged_for_trial_execution_planning",
    ),
    "subway_enter_station_issuance_package": (
        "subway_enter_station_packaged_with_constraints",
        "packaged_with_constraints_for_trial_execution_planning",
    ),
    "stadium_concert_ticket_gate_issuance_package": (
        "stadium_concert_packaged_observation_only",
        "packaged_observation_only",
    ),
    "plaza_market_crowd_issuance_package": (
        "plaza_market_packaged_observation_only",
        "packaged_observation_only",
    ),
    "gps_slam_conflict_issuance_package": (
        "gps_slam_conflict_packaged_as_blocked_record",
        "packaged_as_blocked_record",
    ),
    "home_return_issuance_package": (
        "home_return_packaged_for_trial_execution_planning",
        "packaged_for_trial_execution_planning",
    ),
}

_CLOSURE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1.json"
)

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
        "phase_ref": PRE_RUNTIME_TRIAL_PACKAGE_REF,
        "artifact_rel": _CLOSURE_ARTIFACT_REL,
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PACKAGE_CLOSURE_READINESS_REVIEW_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_closure_readiness_review/"
            "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_types_v1.py"
        ),
        "require_go": True,
        "require_pre_package_sealed": True,
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
    },
    {
        "phase_ref": PLANNING_REF,
        "artifact_rel": _PLANNING_ARTIFACT_REL,
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_planning/"
            "phase_one_environment_cognition_runtime_trial_planning_types_v1.py"
        ),
        "require_go": True,
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


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(ISSUANCE_PACKAGE_ITEM_REFS) != 6:
        issues.append("issuance_package_item_refs_count_not_6")
    if len(ISSUANCE_PACKAGE_GO_KEYS) != 6:
        issues.append("issuance_package_go_keys_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 10:
        issues.append("sealed_upstream_phase_refs_count_not_10")
    if len(ISSUANCE_PACKAGE_GOVERNANCE_RULES) != 14:
        issues.append("issuance_package_governance_rules_count_not_14")
    if len(CLOSURE_SCENARIO_REF_MAP) != 6:
        issues.append("closure_scenario_ref_map_count_not_6")
    return len(issues) == 0, issues


def _merge_blocked(*ops: str) -> Tuple[str, ...]:
    merged = list(UNIVERSAL_BLOCKED_OPERATIONS)
    for op in ops:
        if op not in merged:
            merged.append(op)
    return tuple(merged)


def build_issuance_package_items_v1() -> Tuple[ControlledRuntimeTrialIssuancePackageItem, ...]:
    return (
        ControlledRuntimeTrialIssuancePackageItem(
            package_ref="mall_find_entrance_issuance_package",
            closure_scenario_ref="mall_find_entrance_package",
            source_readiness="ready_for_pre_runtime_trial_review",
            package_scope="low_risk_controlled_trial_candidate",
            issuance_package_status="packaged_for_trial_execution_planning",
            allowed_next_step="trial_execution_planning_only",
            package_boundaries=(
                "candidate_only_replay_allowed",
                "guidance_candidate_generation_allowed",
                "evidence_request_candidate_generation_allowed",
                "action_safety_candidate_required",
            ),
            package_constraints=(),
            blocked_operations=_merge_blocked("direct_navigation"),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(PRE_RUNTIME_TRIAL_PACKAGE_REF, PACKAGE_BOUNDARY_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialIssuancePackageItem(
            package_ref="subway_enter_station_issuance_package",
            closure_scenario_ref="subway_enter_station_package",
            source_readiness="ready_with_constraints_for_pre_runtime_trial_review",
            package_scope="cautious_candidate_trial",
            issuance_package_status="packaged_with_constraints_for_trial_execution_planning",
            allowed_next_step="constrained_trial_execution_planning_only",
            package_boundaries=(),
            package_constraints=(
                "gps_degraded_acknowledged",
                "local_spatial_evidence_required",
                "indoor_uncertainty_downgrade_required",
                "more_evidence_required_before_action_like_guidance",
            ),
            blocked_operations=_merge_blocked(
                "action_like_guidance_without_action_safety_candidate",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(PRE_RUNTIME_TRIAL_PACKAGE_REF, PACKAGE_BOUNDARY_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialIssuancePackageItem(
            package_ref="stadium_concert_ticket_gate_issuance_package",
            closure_scenario_ref="stadium_concert_ticket_gate_package",
            source_readiness="observation_only_ready",
            package_scope="observation_only",
            issuance_package_status="packaged_observation_only",
            allowed_next_step="observation_trial_execution_planning_only",
            package_boundaries=(
                "event_overlay_validation",
                "crowd_flow_risk_observation",
                "ocr_sign_evidence_request_placeholder",
            ),
            package_constraints=(),
            blocked_operations=_merge_blocked(
                "movement_command",
                "route_activation",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(PRE_RUNTIME_TRIAL_PACKAGE_REF, PACKAGE_BOUNDARY_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialIssuancePackageItem(
            package_ref="plaza_market_crowd_issuance_package",
            closure_scenario_ref="plaza_market_crowd_package",
            source_readiness="observation_only_ready",
            package_scope="observation_only",
            issuance_package_status="packaged_observation_only",
            allowed_next_step="observation_trial_execution_planning_only",
            package_boundaries=(
                "crowd_queue_risk_observation",
                "temporary_layout_uncertainty_logging",
                "wait_observe_candidate_generation",
            ),
            package_constraints=(),
            blocked_operations=_merge_blocked(
                "movement_guidance_trial",
                "route_activation",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(PRE_RUNTIME_TRIAL_PACKAGE_REF, PACKAGE_BOUNDARY_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialIssuancePackageItem(
            package_ref="gps_slam_conflict_issuance_package",
            closure_scenario_ref="gps_slam_conflict_package",
            source_readiness="blocked_preserved",
            package_scope="blocked",
            issuance_package_status="packaged_as_blocked_record",
            allowed_next_step="conflict_resolution_planning_only",
            package_boundaries=(
                "conflict_record_review",
                "conflict_resolution_planning_placeholder",
            ),
            package_constraints=(),
            blocked_operations=_merge_blocked(
                "runtime_trial_execution_planning",
                "route_activation",
                "action_like_guidance",
                "speech_guidance",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(PRE_RUNTIME_TRIAL_PACKAGE_REF, PACKAGE_BOUNDARY_REF),
            source_chain=SOURCE_CHAIN,
            package_active=False,
        ),
        ControlledRuntimeTrialIssuancePackageItem(
            package_ref="home_return_issuance_package",
            closure_scenario_ref="home_return_package",
            source_readiness="ready_for_pre_runtime_trial_review",
            package_scope="low_risk_controlled_trial_candidate",
            issuance_package_status="packaged_for_trial_execution_planning",
            allowed_next_step="trial_execution_planning_only",
            package_boundaries=(
                "candidate_field_task_guidance_replay",
                "coarse_map_route_candidate_check",
                "local_spatial_check_candidate_generation",
                "action_safety_candidate_required",
            ),
            package_constraints=(),
            blocked_operations=_merge_blocked(),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(PRE_RUNTIME_TRIAL_PACKAGE_REF, PACKAGE_BOUNDARY_REF),
            source_chain=SOURCE_CHAIN,
        ),
    )


def build_shared_records_v1() -> Dict[str, Any]:
    return {
        "control_binding": candidate_to_dict(
            IssuedTrialPackageControlBinding(
                binding_ref="issued_trial_package_control_binding_v1",
                rollback_policy_ref=ROLLBACK_POLICY_REF,
                observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
                failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
                rollback_policy_bound=True,
                observation_log_policy_bound=True,
                failure_handling_policy_bound=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "blocker_record": candidate_to_dict(
            IssuedTrialPackageBlockerRecord(
                record_ref="issued_trial_package_blocker_record_v1",
                blocked_scenario_remains_blocked=True,
                observation_only_not_upgraded=True,
                constrained_item_constraints_preserved=True,
                live_sensor_trigger_blocked_for_all=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "audit_record": candidate_to_dict(
            IssuedTrialPackageAuditRecord(
                audit_ref="issued_trial_package_audit_record_v1",
                pre_runtime_trial_package_go_verified=True,
                pre_runtime_trial_package_status_sealed=True,
                sealed_phase_one_chain_verified=True,
                allowed_next_step_planning_only=True,
                issuance_package_not_runtime_activation=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_issuance_package_profile_v1() -> ControlledRuntimeTrialIssuancePackageProfile:
    return ControlledRuntimeTrialIssuancePackageProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        pre_runtime_trial_package_ref=PRE_RUNTIME_TRIAL_PACKAGE_REF,
        pre_runtime_trial_package_status=PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
        phase_one_chain_ref=PHASE_ONE_CHAIN_REF,
        phase_one_chain_status=PHASE_ONE_CHAIN_STATUS,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        issuance_package_item_refs=ISSUANCE_PACKAGE_ITEM_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=ISSUANCE_PACKAGE_GOVERNANCE_RULES,
        candidate_only_source_chain_required=CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    )


def build_issuance_package_item_go_map(
    items: Tuple[ControlledRuntimeTrialIssuancePackageItem, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for item in items:
        go_key, expected_status = _PACKAGE_GO_KEY_MAP[item.package_ref]
        result[go_key] = item.issuance_package_status == expected_status
    return result


def build_issuance_package_decision_v1(
    *,
    pre_runtime_trial_package_go_verified: bool,
    pre_runtime_trial_package_status_sealed: bool,
    sealed_phase_one_chain_verified: bool,
    scenario_scope_preserved_for_all: bool,
) -> ControlledRuntimeTrialIssuancePackageDecision:
    return ControlledRuntimeTrialIssuancePackageDecision(
        decision_ref="controlled_runtime_trial_issuance_package_decision_v1",
        profile_ref=PROFILE_REF,
        issuance_package_profile_count=1,
        issuance_package_item_count=len(ISSUANCE_PACKAGE_ITEM_REFS),
        pre_runtime_trial_package_go_verified=pre_runtime_trial_package_go_verified,
        pre_runtime_trial_package_status_sealed=pre_runtime_trial_package_status_sealed,
        sealed_phase_one_chain_verified=sealed_phase_one_chain_verified,
        scenario_scope_preserved_for_all=scenario_scope_preserved_for_all,
        final_decision=FINAL_DECISION_GO,
    )


def build_phase_one_environment_cognition_runtime_trial_issuance_package_matrix_v1() -> Dict[str, Any]:
    profile = build_issuance_package_profile_v1()
    items = build_issuance_package_items_v1()
    shared = build_shared_records_v1()
    decision = build_issuance_package_decision_v1(
        pre_runtime_trial_package_go_verified=True,
        pre_runtime_trial_package_status_sealed=True,
        sealed_phase_one_chain_verified=True,
        scenario_scope_preserved_for_all=True,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "controlled_runtime_trial_issuance_package_profile": candidate_to_dict(profile),
        "issuance_package_items": [candidate_to_dict(i) for i in items],
        "shared_records": shared,
        "issuance_package_decision": candidate_to_dict(decision),
        "issuance_package_item_go_map": build_issuance_package_item_go_map(items),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "closure_artifact_rel": _CLOSURE_ARTIFACT_REL,
        "issuance_package_governance_rules": list(ISSUANCE_PACKAGE_GOVERNANCE_RULES),
        "universal_blocked_operations": list(UNIVERSAL_BLOCKED_OPERATIONS),
        "next_phase_ref": NEXT_PHASE_REF,
    }
