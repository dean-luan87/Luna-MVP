# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Owner Approval Issuance — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_owner_approval_issuance.phase_one_environment_cognition_runtime_trial_owner_approval_issuance_types_v1 import (
    ACTION_SAFETY_ENTRYPOINT,
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_GO,
    GUIDANCE_ENTRYPOINT,
    INTERFACE_LAYER_PROTOCOL_REF,
    ISSUANCE_GOVERNANCE_RULES,
    ISSUANCE_ITEM_GO_KEYS,
    ISSUANCE_ITEM_REFS,
    NEXT_PHASE_REF,
    OWNER_APPROVAL_REQUEST_REF,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    REQUEST_ITEM_REF_MAP,
    RUNTIME_TRIAL_MODE,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    SPEECH_GATE_ENTRYPOINT,
    TASK_MANAGER_ENTRYPOINT,
    RuntimeTrialIssuanceAuditRecord,
    RuntimeTrialIssuedBlockerRecord,
    RuntimeTrialIssuedControlBinding,
    RuntimeTrialIssuedScope,
    RuntimeTrialOwnerApprovalIssuanceDecision,
    RuntimeTrialOwnerApprovalIssuanceItem,
    RuntimeTrialOwnerApprovalIssuanceProfile,
    candidate_to_dict,
)

REGISTRY_ID = "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_registry_v1"
PROFILE_REF = "runtime_trial_owner_approval_issuance_profile_v1"
ROLLBACK_POLICY_REF = "runtime_trial_rollback_v1"
OBSERVATION_LOG_POLICY_REF = "runtime_trial_observation_log_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "issuance_item_refs": ISSUANCE_ITEM_REFS,
    "issuance_item_go_keys": ISSUANCE_ITEM_GO_KEYS,
    "issuance_governance_rules": ISSUANCE_GOVERNANCE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
}

_ITEM_GO_KEY_MAP: Dict[str, Tuple[str, str]] = {
    "mall_find_entrance": (
        "mall_find_entrance_issued_for_next_stage_planning",
        "issued_for_next_stage_planning",
    ),
    "subway_enter_station": (
        "subway_enter_station_issued_with_constraints",
        "issued_with_constraints_for_next_stage_planning",
    ),
    "stadium_concert_ticket_gate": (
        "stadium_concert_issued_observation_only",
        "issued_observation_only",
    ),
    "plaza_market_crowd": (
        "plaza_market_issued_observation_only",
        "issued_observation_only",
    ),
    "gps_slam_conflict": (
        "gps_slam_conflict_not_issued_blocked",
        "not_issued_blocked",
    ),
    "home_return": (
        "home_return_issued_for_next_stage_planning",
        "issued_for_next_stage_planning",
    ),
}

_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_planning_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_planning_review_v1.json"
)

_REQUEST_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_owner_approval_request_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_owner_approval_request_review_v1.json"
)

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
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
    if len(ISSUANCE_ITEM_REFS) != 6:
        issues.append("issuance_item_refs_count_not_6")
    if len(ISSUANCE_ITEM_GO_KEYS) != 6:
        issues.append("issuance_item_go_keys_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 7:
        issues.append("sealed_upstream_phase_refs_count_not_7")
    if len(ISSUANCE_GOVERNANCE_RULES) != 14:
        issues.append("issuance_governance_rules_count_not_14")
    if len(REQUEST_ITEM_REF_MAP) != 6:
        issues.append("request_item_ref_map_count_not_6")
    return len(issues) == 0, issues


def build_issuance_items_v1() -> Tuple[RuntimeTrialOwnerApprovalIssuanceItem, ...]:
    return (
        RuntimeTrialOwnerApprovalIssuanceItem(
            item_ref="mall_find_entrance",
            request_item_ref="mall_find_entrance_low_risk_trial_candidate",
            admission_level="low_risk_controlled_trial_candidate",
            request_status="requestable",
            request_scope="controlled_trial_candidate",
            issued_status="issued_for_next_stage_planning",
            issued_scope="low_risk_controlled_trial_candidate",
            required_controls=(
                "action_safety_candidate_required",
                "speech_gate_candidate_required",
                "rollback_policy_bound",
                "observation_log_policy_bound",
                "no_runtime_activation",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_REQUEST_REF, PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialOwnerApprovalIssuanceItem(
            item_ref="subway_enter_station",
            request_item_ref="subway_enter_station_cautious_trial_candidate",
            admission_level="cautious_candidate_trial",
            request_status="requestable_with_constraints",
            request_scope="cautious_trial_candidate",
            issued_status="issued_with_constraints_for_next_stage_planning",
            issued_scope="cautious_candidate_trial",
            required_controls=(
                "gps_degraded_acknowledged",
                "local_spatial_evidence_required",
                "indoor_uncertainty_downgrade_required",
                "more_evidence_required_before_action_like_guidance",
                "no_runtime_activation",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_REQUEST_REF, PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialOwnerApprovalIssuanceItem(
            item_ref="stadium_concert_ticket_gate",
            request_item_ref="stadium_concert_ticket_gate_observation_trial_candidate",
            admission_level="observation_only",
            request_status="observation_only_requestable",
            request_scope="observation_only",
            issued_status="issued_observation_only",
            issued_scope="observation_only",
            required_controls=(
                "crowd_flow_risk_required",
                "event_overlay_does_not_rewrite_map_place",
                "no_movement_command",
                "no_runtime_activation",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_REQUEST_REF, PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialOwnerApprovalIssuanceItem(
            item_ref="plaza_market_crowd",
            request_item_ref="plaza_market_crowd_blocked_or_observation_only",
            admission_level="observation_only",
            request_status="observation_only_requestable",
            request_scope="observation_only",
            issued_status="issued_observation_only",
            issued_scope="observation_only",
            required_controls=(
                "crowd_density_blocks_movement_guidance",
                "temporary_layout_uncertainty_recorded",
                "only_evidence_request_observe_wait_allowed",
                "no_runtime_activation",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_REQUEST_REF, PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialOwnerApprovalIssuanceItem(
            item_ref="gps_slam_conflict",
            request_item_ref="gps_slam_conflict_runtime_blocker",
            admission_level="blocked",
            request_status="not_requestable",
            request_scope="blocked",
            issued_status="not_issued_blocked",
            issued_scope="blocked",
            required_controls=(
                "unresolved_conflict_blocks_issuance",
                "no_route_hint_activation",
                "no_action_like_guidance",
                "requires_conflict_resolution_planning",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_REQUEST_REF, PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialOwnerApprovalIssuanceItem(
            item_ref="home_return",
            request_item_ref="home_return_low_risk_trial_candidate",
            admission_level="low_risk_controlled_trial_candidate",
            request_status="requestable",
            request_scope="controlled_trial_candidate",
            issued_status="issued_for_next_stage_planning",
            issued_scope="low_risk_controlled_trial_candidate",
            required_controls=(
                "coarse_map_route_plus_local_spatial_check",
                "action_safety_pending_required",
                "rollback_policy_bound",
                "observation_log_policy_bound",
                "no_fact_write",
                "no_runtime_activation",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(OWNER_APPROVAL_REQUEST_REF, PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
    )


def build_issued_scopes_v1() -> Tuple[RuntimeTrialIssuedScope, ...]:
    return (
        RuntimeTrialIssuedScope(
            scope_ref="low_risk_controlled_trial_candidate_scope_v1",
            issued_scope="low_risk_controlled_trial_candidate",
            admission_level="low_risk_controlled_trial_candidate",
            request_scope="controlled_trial_candidate",
            movement_guidance_allowed=False,
            runtime_activation_allowed=False,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialIssuedScope(
            scope_ref="cautious_candidate_trial_scope_v1",
            issued_scope="cautious_candidate_trial",
            admission_level="cautious_candidate_trial",
            request_scope="cautious_trial_candidate",
            movement_guidance_allowed=False,
            runtime_activation_allowed=False,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialIssuedScope(
            scope_ref="observation_only_scope_v1",
            issued_scope="observation_only",
            admission_level="observation_only",
            request_scope="observation_only",
            movement_guidance_allowed=False,
            runtime_activation_allowed=False,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialIssuedScope(
            scope_ref="blocked_scope_v1",
            issued_scope="blocked",
            admission_level="blocked",
            request_scope="blocked",
            movement_guidance_allowed=False,
            runtime_activation_allowed=False,
            source_chain=SOURCE_CHAIN,
        ),
    )


def build_shared_records_v1() -> Dict[str, Any]:
    return {
        "control_binding": candidate_to_dict(
            RuntimeTrialIssuedControlBinding(
                binding_ref="runtime_trial_issued_control_binding_v1",
                rollback_policy_ref=ROLLBACK_POLICY_REF,
                observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
                rollback_policy_bound=True,
                observation_log_policy_bound=True,
                no_runtime_activation=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "blocker_record": candidate_to_dict(
            RuntimeTrialIssuedBlockerRecord(
                record_ref="runtime_trial_issued_blocker_record_v1",
                blocked_scenario_not_issued=True,
                observation_only_not_upgraded=True,
                constrained_item_not_unconstrained=True,
                gps_slam_conflict_blocks_issuance=True,
                crowd_high_risk_blocks_movement_guidance_trial=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_issuance_profile_v1() -> RuntimeTrialOwnerApprovalIssuanceProfile:
    return RuntimeTrialOwnerApprovalIssuanceProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        owner_approval_request_ref=OWNER_APPROVAL_REQUEST_REF,
        planning_ref=PLANNING_REF,
        phase_one_chain_ref=PHASE_ONE_CHAIN_REF,
        phase_one_chain_status=PHASE_ONE_CHAIN_STATUS,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        task_manager_entrypoint=TASK_MANAGER_ENTRYPOINT,
        guidance_entrypoint=GUIDANCE_ENTRYPOINT,
        speech_gate_entrypoint=SPEECH_GATE_ENTRYPOINT,
        action_safety_entrypoint=ACTION_SAFETY_ENTRYPOINT,
        interface_layer_protocol_ref=INTERFACE_LAYER_PROTOCOL_REF,
        issuance_item_refs=ISSUANCE_ITEM_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=ISSUANCE_GOVERNANCE_RULES,
        candidate_only_source_chain_required=CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    )


def _count_by_issued_status(items: Tuple[RuntimeTrialOwnerApprovalIssuanceItem, ...]) -> Dict[str, int]:
    return {
        "issued_for_next_stage_planning_count": sum(
            1 for i in items if i.issued_status == "issued_for_next_stage_planning"
        ),
        "issued_with_constraints_count": sum(
            1
            for i in items
            if i.issued_status == "issued_with_constraints_for_next_stage_planning"
        ),
        "issued_observation_only_count": sum(
            1 for i in items if i.issued_status == "issued_observation_only"
        ),
        "not_issued_blocked_count": sum(
            1 for i in items if i.issued_status == "not_issued_blocked"
        ),
    }


def build_issuance_item_go_map(
    items: Tuple[RuntimeTrialOwnerApprovalIssuanceItem, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for item in items:
        go_key, expected_status = _ITEM_GO_KEY_MAP[item.item_ref]
        result[go_key] = item.issued_status == expected_status
    return result


def build_issuance_decision_v1(
    *,
    owner_approval_request_go_verified: bool,
    planning_go_verified: bool,
    sealed_phase_one_chain_verified: bool,
    admission_level_preserved_for_all: bool,
    request_scope_preserved_for_all: bool,
    items: Tuple[RuntimeTrialOwnerApprovalIssuanceItem, ...],
) -> RuntimeTrialOwnerApprovalIssuanceDecision:
    counts = _count_by_issued_status(items)
    return RuntimeTrialOwnerApprovalIssuanceDecision(
        decision_ref="runtime_trial_owner_approval_issuance_decision_v1",
        profile_ref=PROFILE_REF,
        issuance_profile_count=1,
        issuance_item_count=len(items),
        owner_approval_request_go_verified=owner_approval_request_go_verified,
        planning_go_verified=planning_go_verified,
        sealed_phase_one_chain_verified=sealed_phase_one_chain_verified,
        admission_level_preserved_for_all=admission_level_preserved_for_all,
        request_scope_preserved_for_all=request_scope_preserved_for_all,
        issued_for_next_stage_planning_count=counts["issued_for_next_stage_planning_count"],
        issued_with_constraints_count=counts["issued_with_constraints_count"],
        issued_observation_only_count=counts["issued_observation_only_count"],
        not_issued_blocked_count=counts["not_issued_blocked_count"],
        final_decision=FINAL_DECISION_GO,
        trial_runtime_started=False,
        runtime_activation_allowed=False,
    )


def build_phase_one_environment_cognition_runtime_trial_owner_approval_issuance_matrix_v1() -> Dict[str, Any]:
    profile = build_issuance_profile_v1()
    items = build_issuance_items_v1()
    scopes = build_issued_scopes_v1()
    shared = build_shared_records_v1()
    decision = build_issuance_decision_v1(
        owner_approval_request_go_verified=True,
        planning_go_verified=True,
        sealed_phase_one_chain_verified=True,
        admission_level_preserved_for_all=True,
        request_scope_preserved_for_all=True,
        items=items,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "owner_approval_issuance_profile": candidate_to_dict(profile),
        "issuance_items": [candidate_to_dict(i) for i in items],
        "issued_scopes": [candidate_to_dict(s) for s in scopes],
        "shared_records": shared,
        "issuance_decision": candidate_to_dict(decision),
        "issuance_item_go_map": build_issuance_item_go_map(items),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "request_artifact_rel": _REQUEST_ARTIFACT_REL,
        "planning_artifact_rel": _PLANNING_ARTIFACT_REL,
        "issuance_governance_rules": list(ISSUANCE_GOVERNANCE_RULES),
    }
