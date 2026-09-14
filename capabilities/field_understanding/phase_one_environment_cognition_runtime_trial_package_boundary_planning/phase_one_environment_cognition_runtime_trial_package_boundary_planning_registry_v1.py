# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Package Boundary Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_package_boundary_planning.phase_one_environment_cognition_runtime_trial_package_boundary_planning_types_v1 import (
    ACTION_SAFETY_ENTRYPOINT,
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_GO,
    GUIDANCE_ENTRYPOINT,
    INTERFACE_LAYER_PROTOCOL_REF,
    ISSUANCE_ITEM_REF_MAP,
    OWNER_APPROVAL_ISSUANCE_REF,
    OWNER_APPROVAL_REQUEST_REF,
    PACKAGE_GOVERNANCE_RULES,
    PACKAGE_ITEM_GO_KEYS,
    PACKAGE_ITEM_REFS,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    RUNTIME_TRIAL_MODE,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    SPEECH_GATE_ENTRYPOINT,
    TASK_MANAGER_ENTRYPOINT,
    UNIVERSAL_BLOCKED_OPERATIONS,
    ControlledRuntimeTrialPackageItem,
    ControlledRuntimeTrialPackageProfile,
    TrialPackageBoundaryPlanningDecision,
    TrialPackageFailureHandlingBinding,
    TrialPackageObservationLogBinding,
    TrialPackageRollbackBinding,
    candidate_to_dict,
)

REGISTRY_ID = "phase_one_environment_cognition_runtime_trial_package_boundary_planning_registry_v1"
PROFILE_REF = "controlled_runtime_trial_package_profile_v1"
ROLLBACK_POLICY_REF = "runtime_trial_rollback_v1"
OBSERVATION_LOG_POLICY_REF = "runtime_trial_observation_log_v1"
FAILURE_HANDLING_POLICY_REF = "runtime_trial_failure_handling_policy_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "package_item_refs": PACKAGE_ITEM_REFS,
    "package_item_go_keys": PACKAGE_ITEM_GO_KEYS,
    "package_governance_rules": PACKAGE_GOVERNANCE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
    "universal_blocked_operations": UNIVERSAL_BLOCKED_OPERATIONS,
}

_PACKAGE_GO_KEY_MAP: Dict[str, str] = {
    "mall_find_entrance_package": "mall_find_entrance_package_ready",
    "subway_enter_station_package": "subway_enter_station_package_constraints_ready",
    "stadium_concert_ticket_gate_package": "stadium_concert_observation_package_ready",
    "plaza_market_crowd_package": "plaza_market_observation_package_ready",
    "gps_slam_conflict_package": "gps_slam_conflict_package_blocked",
    "home_return_package": "home_return_package_ready",
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

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
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
        "require_issuance_go": True,
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
        "require_request_go": True,
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
        "require_planning_go": True,
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
    if len(PACKAGE_ITEM_REFS) != 6:
        issues.append("package_item_refs_count_not_6")
    if len(PACKAGE_ITEM_GO_KEYS) != 6:
        issues.append("package_item_go_keys_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 8:
        issues.append("sealed_upstream_phase_refs_count_not_8")
    if len(PACKAGE_GOVERNANCE_RULES) != 14:
        issues.append("package_governance_rules_count_not_14")
    if len(ISSUANCE_ITEM_REF_MAP) != 6:
        issues.append("issuance_item_ref_map_count_not_6")
    return len(issues) == 0, issues


def _merge_blocked(*ops: str) -> Tuple[str, ...]:
    merged = list(UNIVERSAL_BLOCKED_OPERATIONS)
    for op in ops:
        if op not in merged:
            merged.append(op)
    return tuple(merged)


def build_package_items_v1() -> Tuple[ControlledRuntimeTrialPackageItem, ...]:
    return (
        ControlledRuntimeTrialPackageItem(
            package_ref="mall_find_entrance_package",
            issuance_item_ref="mall_find_entrance",
            issued_status="issued_for_next_stage_planning",
            package_scope="low_risk_controlled_trial_candidate",
            allowed_operations=(
                "candidate_field_synthesis_replay",
                "candidate_task_alignment_replay",
                "guidance_candidate_generation",
                "evidence_request_candidate_generation",
            ),
            blocked_operations=_merge_blocked(
                "direct_navigation",
                "live_sensor_trigger",
            ),
            package_constraints=(),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_ISSUANCE_REF, OWNER_APPROVAL_REQUEST_REF, PLANNING_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialPackageItem(
            package_ref="subway_enter_station_package",
            issuance_item_ref="subway_enter_station",
            issued_status="issued_with_constraints_for_next_stage_planning",
            package_scope="cautious_candidate_trial",
            allowed_operations=(
                "candidate_field_synthesis_replay",
                "candidate_task_alignment_replay",
                "guidance_candidate_generation",
                "evidence_request_candidate_generation",
            ),
            blocked_operations=_merge_blocked(
                "action_like_guidance_without_safety_candidate",
                "direct_navigation",
            ),
            package_constraints=(
                "gps_degraded_acknowledged",
                "local_spatial_evidence_required",
                "indoor_uncertainty_downgrade_required",
                "more_evidence_required_before_action_like_guidance",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_ISSUANCE_REF, OWNER_APPROVAL_REQUEST_REF, PLANNING_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialPackageItem(
            package_ref="stadium_concert_ticket_gate_package",
            issuance_item_ref="stadium_concert_ticket_gate",
            issued_status="issued_observation_only",
            package_scope="observation_only",
            allowed_operations=(
                "observation_candidate_replay",
                "event_overlay_label_validation",
                "crowd_flow_risk_candidate_generation",
            ),
            blocked_operations=_merge_blocked(
                "movement_command",
                "route_activation",
            ),
            package_constraints=(),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_ISSUANCE_REF, OWNER_APPROVAL_REQUEST_REF, PLANNING_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialPackageItem(
            package_ref="plaza_market_crowd_package",
            issuance_item_ref="plaza_market_crowd",
            issued_status="issued_observation_only",
            package_scope="observation_only",
            allowed_operations=(
                "crowd_queue_risk_observation",
                "temporary_layout_uncertainty_logging",
                "wait_observe_candidate_generation",
            ),
            blocked_operations=_merge_blocked(
                "movement_guidance_trial",
                "route_activation",
            ),
            package_constraints=(),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_ISSUANCE_REF, OWNER_APPROVAL_REQUEST_REF, PLANNING_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialPackageItem(
            package_ref="gps_slam_conflict_package",
            issuance_item_ref="gps_slam_conflict",
            issued_status="not_issued_blocked",
            package_scope="blocked",
            allowed_operations=(
                "conflict_record_review",
                "conflict_resolution_planning_placeholder",
            ),
            blocked_operations=_merge_blocked(
                "runtime_trial_package_activation",
                "route_hint_activation",
                "action_like_guidance",
                "speech_guidance",
            ),
            package_constraints=(),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_ISSUANCE_REF, OWNER_APPROVAL_REQUEST_REF, PLANNING_REF),
            source_chain=SOURCE_CHAIN,
            package_ready=False,
        ),
        ControlledRuntimeTrialPackageItem(
            package_ref="home_return_package",
            issuance_item_ref="home_return",
            issued_status="issued_for_next_stage_planning",
            package_scope="low_risk_controlled_trial_candidate",
            allowed_operations=(
                "candidate_field_task_guidance_replay",
                "coarse_map_route_candidate_check",
                "local_spatial_check_candidate_generation",
            ),
            blocked_operations=_merge_blocked(),
            package_constraints=(),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_ISSUANCE_REF, OWNER_APPROVAL_REQUEST_REF, PLANNING_REF),
            source_chain=SOURCE_CHAIN,
        ),
    )


def build_shared_bindings_v1() -> Dict[str, Any]:
    return {
        "rollback_binding": candidate_to_dict(
            TrialPackageRollbackBinding(
                binding_ref="trial_package_rollback_binding_v1",
                rollback_policy_ref=ROLLBACK_POLICY_REF,
                rollback_policy_bound=True,
                candidate_only_rollback=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "observation_log_binding": candidate_to_dict(
            TrialPackageObservationLogBinding(
                binding_ref="trial_package_observation_log_binding_v1",
                observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
                observation_log_policy_bound=True,
                log_package_boundary=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "failure_handling_binding": candidate_to_dict(
            TrialPackageFailureHandlingBinding(
                binding_ref="trial_package_failure_handling_binding_v1",
                failure_handling_policy_ref=FAILURE_HANDLING_POLICY_REF,
                failure_handling_policy_bound=True,
                downgrade_on_high_risk=True,
                block_on_unresolved_conflict=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_package_profile_v1() -> ControlledRuntimeTrialPackageProfile:
    return ControlledRuntimeTrialPackageProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        owner_approval_issuance_ref=OWNER_APPROVAL_ISSUANCE_REF,
        planning_ref=PLANNING_REF,
        owner_approval_request_ref=OWNER_APPROVAL_REQUEST_REF,
        phase_one_chain_ref=PHASE_ONE_CHAIN_REF,
        phase_one_chain_status=PHASE_ONE_CHAIN_STATUS,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        task_manager_entrypoint=TASK_MANAGER_ENTRYPOINT,
        guidance_entrypoint=GUIDANCE_ENTRYPOINT,
        speech_gate_entrypoint=SPEECH_GATE_ENTRYPOINT,
        action_safety_entrypoint=ACTION_SAFETY_ENTRYPOINT,
        interface_layer_protocol_ref=INTERFACE_LAYER_PROTOCOL_REF,
        package_item_refs=PACKAGE_ITEM_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=PACKAGE_GOVERNANCE_RULES,
        candidate_only_source_chain_required=CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    )


def build_package_item_go_map(
    items: Tuple[ControlledRuntimeTrialPackageItem, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for item in items:
        go_key = _PACKAGE_GO_KEY_MAP[item.package_ref]
        if go_key == "gps_slam_conflict_package_blocked":
            result[go_key] = (
                item.package_scope == "blocked"
                and item.issued_status == "not_issued_blocked"
                and item.package_ready is False
            )
        elif go_key == "subway_enter_station_package_constraints_ready":
            result[go_key] = bool(item.package_constraints) and item.package_ready is True
        elif go_key.endswith("_observation_package_ready"):
            result[go_key] = (
                item.package_scope == "observation_only"
                and item.issued_status == "issued_observation_only"
                and item.package_ready is True
            )
        else:
            result[go_key] = item.package_ready is True
    return result


def build_package_decision_v1(
    *,
    owner_approval_issuance_go_verified: bool,
    owner_approval_request_go_verified: bool,
    planning_go_verified: bool,
    sealed_phase_one_chain_verified: bool,
    package_scope_preserved_for_all: bool,
    issued_status_preserved_for_all: bool,
    items: Tuple[ControlledRuntimeTrialPackageItem, ...],
) -> TrialPackageBoundaryPlanningDecision:
    return TrialPackageBoundaryPlanningDecision(
        decision_ref="trial_package_boundary_planning_decision_v1",
        profile_ref=PROFILE_REF,
        trial_package_profile_count=1,
        trial_package_item_count=len(items),
        owner_approval_issuance_go_verified=owner_approval_issuance_go_verified,
        owner_approval_request_go_verified=owner_approval_request_go_verified,
        planning_go_verified=planning_go_verified,
        sealed_phase_one_chain_verified=sealed_phase_one_chain_verified,
        package_scope_preserved_for_all=package_scope_preserved_for_all,
        issued_status_preserved_for_all=issued_status_preserved_for_all,
        final_decision=FINAL_DECISION_GO,
    )


def build_phase_one_environment_cognition_runtime_trial_package_boundary_planning_matrix_v1() -> Dict[str, Any]:
    profile = build_package_profile_v1()
    items = build_package_items_v1()
    shared = build_shared_bindings_v1()
    decision = build_package_decision_v1(
        owner_approval_issuance_go_verified=True,
        owner_approval_request_go_verified=True,
        planning_go_verified=True,
        sealed_phase_one_chain_verified=True,
        package_scope_preserved_for_all=True,
        issued_status_preserved_for_all=True,
        items=items,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "controlled_runtime_trial_package_profile": candidate_to_dict(profile),
        "trial_package_items": [candidate_to_dict(i) for i in items],
        "shared_bindings": shared,
        "package_decision": candidate_to_dict(decision),
        "package_item_go_map": build_package_item_go_map(items),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "issuance_artifact_rel": _ISSUANCE_ARTIFACT_REL,
        "request_artifact_rel": _REQUEST_ARTIFACT_REL,
        "planning_artifact_rel": _PLANNING_ARTIFACT_REL,
        "package_governance_rules": list(PACKAGE_GOVERNANCE_RULES),
        "universal_blocked_operations": list(UNIVERSAL_BLOCKED_OPERATIONS),
    }
