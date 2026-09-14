# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Owner Approval Request — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_owner_approval_request.phase_one_environment_cognition_runtime_trial_owner_approval_request_types_v1 import (
    ACTION_SAFETY_ENTRYPOINT,
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_GO,
    GUIDANCE_ENTRYPOINT,
    INTERFACE_LAYER_PROTOCOL_REF,
    NEXT_PHASE_REF,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    REQUEST_GOVERNANCE_RULES,
    REQUEST_ITEM_GO_KEYS,
    REQUEST_ITEM_REFS,
    RUNTIME_TRIAL_MODE,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    SPEECH_GATE_ENTRYPOINT,
    TASK_MANAGER_ENTRYPOINT,
    RuntimeTrialApprovalBlockerPolicy,
    RuntimeTrialApprovalObservationLogBinding,
    RuntimeTrialApprovalRiskSummary,
    RuntimeTrialApprovalRollbackBinding,
    RuntimeTrialApprovalScopeCandidate,
    RuntimeTrialOwnerApprovalRequestDecision,
    RuntimeTrialOwnerApprovalRequestItem,
    RuntimeTrialOwnerApprovalRequestProfile,
    candidate_to_dict,
)

REGISTRY_ID = "phase_one_environment_cognition_runtime_trial_owner_approval_request_registry_v1"
PROFILE_REF = "runtime_trial_owner_approval_request_profile_v1"
ROLLBACK_POLICY_REF = "runtime_trial_rollback_v1"
OBSERVATION_LOG_POLICY_REF = "runtime_trial_observation_log_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "request_item_refs": REQUEST_ITEM_REFS,
    "request_item_go_keys": REQUEST_ITEM_GO_KEYS,
    "request_governance_rules": REQUEST_GOVERNANCE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
}

_ITEM_GO_KEY_MAP: Dict[str, str] = {
    "mall_find_entrance_low_risk_trial_candidate": "mall_find_entrance_requestable",
    "subway_enter_station_cautious_trial_candidate": "subway_enter_station_requestable_with_constraints",
    "stadium_concert_ticket_gate_observation_trial_candidate": "stadium_concert_observation_only_requestable",
    "plaza_market_crowd_blocked_or_observation_only": "plaza_market_observation_only_requestable",
    "gps_slam_conflict_runtime_blocker": "gps_slam_conflict_not_requestable",
    "home_return_low_risk_trial_candidate": "home_return_requestable",
}

_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_planning_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_planning_review_v1.json"
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
        "phase_ref": "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/midplatform_task_manager_controlled_skeleton_implementation_dryrun/"
            "summary.json"
        ),
        "expected_go": None,
        "module_rel": (
            "capabilities/midplatform/midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1.py"
        ),
        "require_go": False,
        "skeleton_module_rel": "capabilities/midplatform/core/task_manager_skeleton_v1.py",
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
    if len(REQUEST_ITEM_REFS) != 6:
        issues.append("request_item_refs_count_not_6")
    if len(REQUEST_ITEM_GO_KEYS) != 6:
        issues.append("request_item_go_keys_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 7:
        issues.append("sealed_upstream_phase_refs_count_not_7")
    if len(REQUEST_GOVERNANCE_RULES) != 14:
        issues.append("request_governance_rules_count_not_14")
    return len(issues) == 0, issues


def build_request_items_v1() -> Tuple[RuntimeTrialOwnerApprovalRequestItem, ...]:
    return (
        RuntimeTrialOwnerApprovalRequestItem(
            item_ref="mall_find_entrance_low_risk_trial_candidate",
            planning_policy_ref="mall_find_entrance_low_risk_trial_candidate",
            admission_level="low_risk_controlled_trial_candidate",
            approval_request_status="requestable",
            request_scope="controlled_trial_candidate",
            required_controls=(
                "action_safety_candidate_required",
                "speech_gate_candidate_required",
                "rollback_policy_required",
                "observation_log_required",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialOwnerApprovalRequestItem(
            item_ref="subway_enter_station_cautious_trial_candidate",
            planning_policy_ref="subway_enter_station_cautious_trial_candidate",
            admission_level="cautious_candidate_trial",
            approval_request_status="requestable_with_constraints",
            request_scope="cautious_trial_candidate",
            required_controls=(
                "gps_degraded_acknowledged",
                "local_spatial_evidence_required",
                "indoor_uncertainty_downgrade_required",
                "no_action_like_guidance_without_more_evidence",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialOwnerApprovalRequestItem(
            item_ref="stadium_concert_ticket_gate_observation_trial_candidate",
            planning_policy_ref="stadium_concert_ticket_gate_observation_trial_candidate",
            admission_level="observation_only",
            approval_request_status="observation_only_requestable",
            request_scope="observation_only",
            required_controls=(
                "crowd_flow_risk_required",
                "event_overlay_does_not_rewrite_map_place",
                "no_movement_command",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialOwnerApprovalRequestItem(
            item_ref="plaza_market_crowd_blocked_or_observation_only",
            planning_policy_ref="plaza_market_crowd_blocked_or_observation_only",
            admission_level="observation_only",
            approval_request_status="observation_only_requestable",
            request_scope="observation_only",
            required_controls=(
                "crowd_density_blocks_movement_guidance",
                "temporary_layout_uncertainty_recorded",
                "only_evidence_request_observe_wait_allowed",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialOwnerApprovalRequestItem(
            item_ref="gps_slam_conflict_runtime_blocker",
            planning_policy_ref="gps_slam_conflict_runtime_blocker",
            admission_level="blocked",
            approval_request_status="not_requestable",
            request_scope="blocked",
            required_controls=(
                "unresolved_conflict_blocks_runtime_trial",
                "no_route_hint_activation",
                "no_action_like_guidance",
                "requires_conflict_resolution_planning",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialOwnerApprovalRequestItem(
            item_ref="home_return_low_risk_trial_candidate",
            planning_policy_ref="home_return_low_risk_trial_candidate",
            admission_level="low_risk_controlled_trial_candidate",
            approval_request_status="requestable",
            request_scope="controlled_trial_candidate",
            required_controls=(
                "coarse_map_route_plus_local_spatial_check",
                "action_safety_pending_required",
                "rollback_policy_required",
                "observation_log_required",
                "no_fact_write",
            ),
            rollback_policy_ref=ROLLBACK_POLICY_REF,
            observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
            upstream_refs=(PLANNING_REF, PHASE_ONE_CHAIN_REF),
            source_chain=SOURCE_CHAIN,
        ),
    )


def build_approval_scope_candidates_v1() -> Tuple[RuntimeTrialApprovalScopeCandidate, ...]:
    return (
        RuntimeTrialApprovalScopeCandidate(
            scope_ref="controlled_trial_candidate_scope_v1",
            request_scope="controlled_trial_candidate",
            admission_levels=("low_risk_controlled_trial_candidate",),
            approval_request_statuses=("requestable",),
            movement_guidance_allowed=False,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialApprovalScopeCandidate(
            scope_ref="cautious_trial_candidate_scope_v1",
            request_scope="cautious_trial_candidate",
            admission_levels=("cautious_candidate_trial",),
            approval_request_statuses=("requestable_with_constraints",),
            movement_guidance_allowed=False,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialApprovalScopeCandidate(
            scope_ref="observation_only_scope_v1",
            request_scope="observation_only",
            admission_levels=("observation_only",),
            approval_request_statuses=("observation_only_requestable",),
            movement_guidance_allowed=False,
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialApprovalScopeCandidate(
            scope_ref="blocked_scope_v1",
            request_scope="blocked",
            admission_levels=("blocked",),
            approval_request_statuses=("not_requestable",),
            movement_guidance_allowed=False,
            source_chain=SOURCE_CHAIN,
        ),
    )


def build_shared_bindings_v1() -> Dict[str, Any]:
    return {
        "risk_summary": candidate_to_dict(
            RuntimeTrialApprovalRiskSummary(
                summary_ref="runtime_trial_approval_risk_summary_v1",
                gps_slam_conflict_blocks_runtime_trial=True,
                crowd_high_risk_blocks_movement_guidance_trial=True,
                event_overlay_does_not_rewrite_map_place=True,
                field_interaction_label_not_fact=True,
                speech_gate_candidate_not_tts=True,
                action_safety_candidate_not_action=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "rollback_binding": candidate_to_dict(
            RuntimeTrialApprovalRollbackBinding(
                binding_ref="runtime_trial_approval_rollback_binding_v1",
                rollback_policy_ref=ROLLBACK_POLICY_REF,
                rollback_policy_required=True,
                fallback_observe_wait=True,
                candidate_only_rollback=True,
                no_fact_write_on_rollback=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "observation_log_binding": candidate_to_dict(
            RuntimeTrialApprovalObservationLogBinding(
                binding_ref="runtime_trial_approval_observation_log_binding_v1",
                observation_log_policy_ref=OBSERVATION_LOG_POLICY_REF,
                observation_log_policy_required=True,
                log_upstream_source_refs=True,
                log_admission_level=True,
                log_approval_request_status=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "blocker_policy": candidate_to_dict(
            RuntimeTrialApprovalBlockerPolicy(
                policy_ref="runtime_trial_approval_blocker_policy_v1",
                blocked_scenario_not_requestable=True,
                observation_only_not_movement_trial=True,
                conflict_blocks_route_hint_activation=True,
                crowd_density_blocks_movement_guidance=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_request_profile_v1() -> RuntimeTrialOwnerApprovalRequestProfile:
    return RuntimeTrialOwnerApprovalRequestProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
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
        request_item_refs=REQUEST_ITEM_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=REQUEST_GOVERNANCE_RULES,
        owner_approval_required=True,
        owner_approval_issued=False,
        trial_issuance_allowed=False,
        candidate_only_source_chain_required=CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    )


def _count_by_status(items: Tuple[RuntimeTrialOwnerApprovalRequestItem, ...]) -> Dict[str, int]:
    return {
        "requestable_item_count": sum(
            1 for i in items if i.approval_request_status == "requestable"
        ),
        "requestable_with_constraints_item_count": sum(
            1 for i in items if i.approval_request_status == "requestable_with_constraints"
        ),
        "observation_only_requestable_item_count": sum(
            1 for i in items if i.approval_request_status == "observation_only_requestable"
        ),
        "not_requestable_item_count": sum(
            1 for i in items if i.approval_request_status == "not_requestable"
        ),
    }


def build_request_item_go_map(
    items: Tuple[RuntimeTrialOwnerApprovalRequestItem, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for item in items:
        go_key = _ITEM_GO_KEY_MAP.get(item.item_ref, item.item_ref)
        if go_key == "gps_slam_conflict_not_requestable":
            result[go_key] = item.approval_request_status == "not_requestable"
        elif go_key.endswith("_requestable"):
            result[go_key] = item.approval_request_status in (
                "requestable",
                "requestable_with_constraints",
                "observation_only_requestable",
            )
        else:
            result[go_key] = item.request_active is True
    return result


def build_request_decision_v1(
    *,
    planning_go_verified: bool,
    sealed_phase_one_chain_verified: bool,
    admission_level_preserved_for_all: bool,
    items: Tuple[RuntimeTrialOwnerApprovalRequestItem, ...],
) -> RuntimeTrialOwnerApprovalRequestDecision:
    counts = _count_by_status(items)
    return RuntimeTrialOwnerApprovalRequestDecision(
        decision_ref="runtime_trial_owner_approval_request_decision_v1",
        profile_ref=PROFILE_REF,
        approval_request_profile_count=1,
        approval_request_item_count=len(items),
        planning_go_verified=planning_go_verified,
        sealed_phase_one_chain_verified=sealed_phase_one_chain_verified,
        admission_level_preserved_for_all=admission_level_preserved_for_all,
        requestable_item_count=counts["requestable_item_count"],
        requestable_with_constraints_item_count=counts["requestable_with_constraints_item_count"],
        observation_only_requestable_item_count=counts["observation_only_requestable_item_count"],
        not_requestable_item_count=counts["not_requestable_item_count"],
        final_decision=FINAL_DECISION_GO,
        owner_approval_issued=False,
        trial_issuance_allowed=False,
    )


def build_phase_one_environment_cognition_runtime_trial_owner_approval_request_matrix_v1() -> Dict[str, Any]:
    profile = build_request_profile_v1()
    items = build_request_items_v1()
    scopes = build_approval_scope_candidates_v1()
    shared = build_shared_bindings_v1()
    decision = build_request_decision_v1(
        planning_go_verified=True,
        sealed_phase_one_chain_verified=True,
        admission_level_preserved_for_all=True,
        items=items,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "owner_approval_request_profile": candidate_to_dict(profile),
        "approval_request_items": [candidate_to_dict(i) for i in items],
        "approval_scope_candidates": [candidate_to_dict(s) for s in scopes],
        "shared_bindings": shared,
        "request_decision": candidate_to_dict(decision),
        "request_item_go_map": build_request_item_go_map(items),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "planning_artifact_rel": _PLANNING_ARTIFACT_REL,
        "request_governance_rules": list(REQUEST_GOVERNANCE_RULES),
    }
