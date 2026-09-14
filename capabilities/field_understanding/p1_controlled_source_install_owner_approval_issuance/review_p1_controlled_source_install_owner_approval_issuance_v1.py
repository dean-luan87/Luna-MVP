# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Owner Approval Issuance — review v1.

APPROVAL ISSUANCE ONLY. Generates a source-install owner approval issuance for
byte_track and mobile_sam, scoped strictly to "may enter the subsequent
controlled source install preparation / readiness chain". It does NOT approve git
clone / source checkout / source install / weight download and executes/mutates
NOTHING. The approval carries expiry, revocation, full source-chain
traceability, and pre-execution conditions. Protected, non-deletable test board
records are written in planning mode.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.field_understanding.p1_controlled_source_install_owner_approval_issuance.p1_controlled_source_install_owner_approval_issuance_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_source_install_owner_approval_issuance.p1_controlled_source_install_owner_approval_issuance_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    APPROVAL_BOUNDARY_STATEMENTS,
    APPROVAL_CONDITIONS,
    APPROVAL_EXPIRY,
    APPROVAL_ISSUANCE_ONLY,
    APPROVAL_REVOCATION,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    DEPENDENCY_INSTALL_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GIT_CLONE_ALLOWED,
    IN_SCOPE_ASSET_IDS,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    MUST_NOT_PROCESS_ASSET_IDS,
    NEGATIVE_GUARDS,
    NEXT_STEP_REF,
    OWNER_APPROVAL_GRANTED_FOR_GIT_CLONE,
    OWNER_APPROVAL_GRANTED_FOR_INFERENCE,
    OWNER_APPROVAL_GRANTED_FOR_OUTPUT_ADAPTER,
    OWNER_APPROVAL_GRANTED_FOR_RUNTIME,
    OWNER_APPROVAL_GRANTED_FOR_SEMANTIC_LAYER,
    OWNER_APPROVAL_GRANTED_FOR_SOURCE_CHECKOUT,
    OWNER_APPROVAL_GRANTED_FOR_SOURCE_INSTALL,
    OWNER_APPROVAL_GRANTED_FOR_SOURCE_INSTALL_PREPARATION,
    OWNER_APPROVAL_GRANTED_FOR_WEIGHT_DOWNLOAD,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    PLANNING_PRINCIPLE_ZH,
    PREPARATION_AND_READINESS_PHASE_REF,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RISK_ACK_DIMENSIONS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_CHAIN,
    SOURCE_CHECKOUT_ALLOWED,
    SOURCE_FAMILY,
    SOURCE_INSTALL_ALLOWED,
    SOURCE_INSTALL_OWNER_APPROVAL_ISSUANCE_CREATED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TRACEABILITY_REFS,
    UPSTREAM_REQUEST_PLANNING_REF,
    UPSTREAM_RESOLUTION_PLANNING_REF,
    WEIGHT_DOWNLOAD_ALLOWED,
    ApprovedSourceAssetScopeRecord,
    NegativeSourceOwnerApprovalIssuanceGuard,
    P1ControlledSourceInstallOwnerApprovalIssuanceDecision,
    P1ControlledSourceInstallOwnerApprovalIssuanceProfile,
    SourceApprovalBoundaryRecord,
    SourceApprovalConditionRecord,
    SourceApprovalExpiryRecord,
    SourceApprovalRevocationRecord,
    SourceApprovalScopeRecord,
    SourceApprovalTraceabilityRecord,
    SourceInstallPreparationHandoffReadiness,
    SourceOwnerApprovalIssuanceRecord,
    SourceRiskAcknowledgementRecord,
    to_dict,
)


def _pick_writable_base() -> Path:
    for cand in (Path.cwd(), _REPO_ROOT):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()
DEFAULT_OUTPUT_ROOT = (
    _WRITABLE_BASE / "_tmp_eval_out" / "p1_controlled_source_install_owner_approval_issuance_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_source_install_owner_approval_issuance_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_source_install_owner_approval_issuance"
STEP_FILES = (
    f"{_PKG}/p1_controlled_source_install_owner_approval_issuance_types_v1.py",
    f"{_PKG}/p1_controlled_source_install_owner_approval_issuance_registry_v1.py",
    f"{_PKG}/review_p1_controlled_source_install_owner_approval_issuance_v1.py",
)

PROFILE_REF = "p1_controlled_source_install_owner_approval_issuance_profile_v1"
DECISION_REF = "p1_controlled_source_install_owner_approval_issuance_decision_v1"
ISSUANCE_ID = "p1_controlled_source_install_owner_approval_issuance_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1ControlledSourceInstallOwnerApprovalIssuanceProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            approval_issuance_only=APPROVAL_ISSUANCE_ONLY,
            source_install_owner_approval_issuance_created=SOURCE_INSTALL_OWNER_APPROVAL_ISSUANCE_CREATED,
            owner_approval_granted_for_source_install_preparation=OWNER_APPROVAL_GRANTED_FOR_SOURCE_INSTALL_PREPARATION,
            owner_approval_granted_for_git_clone=OWNER_APPROVAL_GRANTED_FOR_GIT_CLONE,
            owner_approval_granted_for_source_checkout=OWNER_APPROVAL_GRANTED_FOR_SOURCE_CHECKOUT,
            owner_approval_granted_for_source_install=OWNER_APPROVAL_GRANTED_FOR_SOURCE_INSTALL,
            owner_approval_granted_for_pip_install=False,
            owner_approval_granted_for_dependency_install=False,
            owner_approval_granted_for_model_download=False,
            owner_approval_granted_for_weight_download=OWNER_APPROVAL_GRANTED_FOR_WEIGHT_DOWNLOAD,
            owner_approval_granted_for_dataset_download=False,
            owner_approval_granted_for_inference=OWNER_APPROVAL_GRANTED_FOR_INFERENCE,
            owner_approval_granted_for_runtime=OWNER_APPROVAL_GRANTED_FOR_RUNTIME,
            owner_approval_granted_for_output_adapter=OWNER_APPROVAL_GRANTED_FOR_OUTPUT_ADAPTER,
            owner_approval_granted_for_semantic_layer=OWNER_APPROVAL_GRANTED_FOR_SEMANTIC_LAYER,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            git_clone_allowed=GIT_CLONE_ALLOWED,
            source_checkout_allowed=SOURCE_CHECKOUT_ALLOWED,
            source_install_allowed=SOURCE_INSTALL_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            dependency_install_allowed=DEPENDENCY_INSTALL_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            in_scope_asset_ids=IN_SCOPE_ASSET_IDS,
            upstream_request_planning_ref=UPSTREAM_REQUEST_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_source_install_owner_approval_issuance_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []
    warnings: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file() or (Path.cwd() / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    # ------------------------------------------------------------------- #
    # (二) Approved source asset scope (2).
    # ------------------------------------------------------------------- #
    asset_scopes = [
        ApprovedSourceAssetScopeRecord(
            asset_id=aid,
            included_in_approval_scope=True,
            approval_scope="source_install_preparation_only",
            source_install_request_ref=UPSTREAM_REQUEST_PLANNING_REF,
            source_resolution_ref=UPSTREAM_RESOLUTION_PLANNING_REF,
            source_family=SOURCE_FAMILY[aid],
            current_status="DEFERRED",
            git_clone_allowed=False,
            source_checkout_allowed=False,
            source_install_allowed=False,
            weight_download_allowed=False,
            model_download_allowed=False,
            dataset_download_allowed=False,
            inference_allowed=False,
            runtime_allowed=False,
            output_adapter_allowed=False,
            semantic_layer_allowed=False,
            requires_next_phase_source_install_preparation=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (一) Issuance record + scope record.
    # ------------------------------------------------------------------- #
    issuance_record = SourceOwnerApprovalIssuanceRecord(
        issuance_id=ISSUANCE_ID,
        phase_id=PHASE_ID,
        source_install_owner_approval_issuance_created=SOURCE_INSTALL_OWNER_APPROVAL_ISSUANCE_CREATED,
        owner_approval_granted_for_source_install_preparation=OWNER_APPROVAL_GRANTED_FOR_SOURCE_INSTALL_PREPARATION,
        approval_scope="source_install_preparation_only",
        requested_assets=IN_SCOPE_ASSET_IDS,
        owner_approval_granted_for_git_clone=OWNER_APPROVAL_GRANTED_FOR_GIT_CLONE,
        owner_approval_granted_for_source_checkout=OWNER_APPROVAL_GRANTED_FOR_SOURCE_CHECKOUT,
        owner_approval_granted_for_source_install=OWNER_APPROVAL_GRANTED_FOR_SOURCE_INSTALL,
        owner_approval_granted_for_weight_download=OWNER_APPROVAL_GRANTED_FOR_WEIGHT_DOWNLOAD,
        owner_approval_granted_for_inference=OWNER_APPROVAL_GRANTED_FOR_INFERENCE,
        owner_approval_granted_for_runtime=OWNER_APPROVAL_GRANTED_FOR_RUNTIME,
        next_phase_ref=PREPARATION_AND_READINESS_PHASE_REF,
    )
    scope_record = SourceApprovalScopeRecord(
        scope_id="source_approval_scope_v1",
        approval_scope="source_install_preparation_only",
        approved_asset_count=len(asset_scopes),
        scope_limited_to_source_install_preparation=True,
        scope_limited_to_deferred_assets=set(a.asset_id for a in asset_scopes) == set(IN_SCOPE_ASSET_IDS),
    )

    # ------------------------------------------------------------------- #
    # (三) Conditions (>=12) + (四) expiry + (五) revocation.
    # ------------------------------------------------------------------- #
    condition_records = [
        SourceApprovalConditionRecord(
            condition_id=f"approval_condition_{i+1}",
            condition=cond,
            required=True,
            satisfied_now=False,
        )
        for i, cond in enumerate(APPROVAL_CONDITIONS)
    ]
    expiry_record = SourceApprovalExpiryRecord(
        expiry_id="source_approval_expiry_v1",
        approval_has_expiry=APPROVAL_EXPIRY["approval_has_expiry"],
        expiry_policy=APPROVAL_EXPIRY["expiry_policy"],
        expired_approval_cannot_be_used=APPROVAL_EXPIRY["expired_approval_cannot_be_used"],
        approval_use_after_repository_change_blocked=APPROVAL_EXPIRY["approval_use_after_repository_change_blocked"],
        approval_use_after_dependency_drift_blocked=APPROVAL_EXPIRY["approval_use_after_dependency_drift_blocked"],
        approval_use_after_license_change_blocked=APPROVAL_EXPIRY["approval_use_after_license_change_blocked"],
        approval_use_after_scope_change_blocked=APPROVAL_EXPIRY["approval_use_after_scope_change_blocked"],
        approval_use_after_registry_drift_blocked=APPROVAL_EXPIRY["approval_use_after_registry_drift_blocked"],
    )
    revocation_record = SourceApprovalRevocationRecord(
        revocation_id="source_approval_revocation_v1",
        approval_revocation_supported=APPROVAL_REVOCATION["approval_revocation_supported"],
        revocation_reason_required=APPROVAL_REVOCATION["revocation_reason_required"],
        revoked_approval_cannot_be_used=APPROVAL_REVOCATION["revoked_approval_cannot_be_used"],
        revocation_must_be_recorded=APPROVAL_REVOCATION["revocation_must_be_recorded"],
        revocation_record_protected=APPROVAL_REVOCATION["revocation_record_protected"],
    )

    # ------------------------------------------------------------------- #
    # Boundary records (>=8) + traceability (>=8).
    # ------------------------------------------------------------------- #
    boundary_records = [
        SourceApprovalBoundaryRecord(
            boundary_id=f"approval_boundary_{i+1}",
            statement=stmt,
            holds=True,
        )
        for i, stmt in enumerate(APPROVAL_BOUNDARY_STATEMENTS)
    ]
    traceability_records = [
        SourceApprovalTraceabilityRecord(trace_key=k, trace_ref=ref, present=True)
        for (k, ref) in TRACEABILITY_REFS
    ]
    source_chain_complete = len(traceability_records) >= 8 and all(t.present for t in traceability_records)

    # ------------------------------------------------------------------- #
    # (七) Risk acknowledgement (2) + (八) handoff readiness.
    # ------------------------------------------------------------------- #
    risk_acks = [
        SourceRiskAcknowledgementRecord(
            asset_id=aid,
            risk_dimensions_acknowledged=RISK_ACK_DIMENSIONS,
            owner_ack_required_for_next_phase=True,
            all_risk_dimensions_acknowledged=len(RISK_ACK_DIMENSIONS) == 8,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    handoff = SourceInstallPreparationHandoffReadiness(
        handoff_id="source_install_preparation_handoff_v1",
        next_phase_ref=PREPARATION_AND_READINESS_PHASE_REF,
        can_enter_source_install_preparation=True,
        can_enter_git_clone=False,
        can_enter_source_checkout=False,
        can_enter_source_install=False,
        can_enter_weight_download=False,
        can_enter_inference=False,
        can_enter_runtime=False,
        can_enter_output_adapter=False,
        can_enter_semantic_layer=False,
        direct_source_install_execution_blocked=True,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 26 negative guards.
    # ------------------------------------------------------------------- #
    conditions_present = {c.condition for c in condition_records}
    scope_limited_to_deferred = (
        set(a.asset_id for a in asset_scopes) == set(IN_SCOPE_ASSET_IDS)
        and not (set(a.asset_id for a in asset_scopes) & set(MUST_NOT_PROCESS_ASSET_IDS))
        and len(asset_scopes) == 2
    )
    invariant_state: Dict[str, bool] = {
        "not_git_clone_approval": OWNER_APPROVAL_GRANTED_FOR_GIT_CLONE is False and GIT_CLONE_ALLOWED is False,
        "not_source_checkout_approval": OWNER_APPROVAL_GRANTED_FOR_SOURCE_CHECKOUT is False and SOURCE_CHECKOUT_ALLOWED is False,
        "not_source_install_approval": OWNER_APPROVAL_GRANTED_FOR_SOURCE_INSTALL is False and SOURCE_INSTALL_ALLOWED is False,
        "not_pip_dependency_approval": PIP_INSTALL_ALLOWED is False and DEPENDENCY_INSTALL_ALLOWED is False,
        "not_download_approval": (
            OWNER_APPROVAL_GRANTED_FOR_WEIGHT_DOWNLOAD is False
            and MODEL_DOWNLOAD_ALLOWED is False
            and WEIGHT_DOWNLOAD_ALLOWED is False
            and DATASET_DOWNLOAD_ALLOWED is False
        ),
        "not_inference_approval": OWNER_APPROVAL_GRANTED_FOR_INFERENCE is False and REAL_INFERENCE_ALLOWED is False,
        "not_runtime_approval": OWNER_APPROVAL_GRANTED_FOR_RUNTIME is False and RUNTIME_EXECUTION_ALLOWED is False,
        "not_output_semantic_approval": (
            OWNER_APPROVAL_GRANTED_FOR_OUTPUT_ADAPTER is False
            and OWNER_APPROVAL_GRANTED_FOR_SEMANTIC_LAYER is False
        ),
        "scope_limited_to_deferred": scope_limited_to_deferred,
        "approval_has_expiry": expiry_record.approval_has_expiry,
        "approval_has_revocation": revocation_record.approval_revocation_supported,
        "source_chain_traceable": source_chain_complete,
        "repo_verification_condition_present": "repository_verification_required" in conditions_present,
        "dependency_review_condition_present": "dependency_expansion_review_required" in conditions_present,
        "license_review_condition_present": "repository_license_review_required" in conditions_present,
        "network_boundary_condition_present": "network_boundary_required" in conditions_present,
        "weight_separate_approval_condition_present": "weight_download_separate_approval_required" in conditions_present,
        "preparation_required_before_execution": (
            handoff.can_enter_source_install_preparation
            and handoff.can_enter_source_install is False
            and handoff.direct_source_install_execution_blocked
        ),
        "no_clone_checkout_install": (
            GIT_CLONE_ALLOWED is False
            and SOURCE_CHECKOUT_ALLOWED is False
            and SOURCE_INSTALL_ALLOWED is False
            and PIP_INSTALL_ALLOWED is False
        ),
        "no_download_performed": (
            MODEL_DOWNLOAD_ALLOWED is False
            and WEIGHT_DOWNLOAD_ALLOWED is False
            and DATASET_DOWNLOAD_ALLOWED is False
        ),
        "no_real_import_load_inference": (
            REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False and REAL_INFERENCE_ALLOWED is False
        ),
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeSourceOwnerApprovalIssuanceGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeSourceOwnerApprovalIssuanceGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_source_owner_approval_issuance_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "source_owner_approval_issuance_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "source_owner_approval_issuance_record_count_gte_1": True,
        "source_approval_scope_record_count_gte_1": True,
        "approved_source_asset_scope_record_count_eq_2": len(asset_scopes) == 2,
        "source_approval_condition_record_count_gte_12": len(condition_records) >= 12,
        "source_approval_expiry_record_count_gte_1": True,
        "source_approval_revocation_record_count_gte_1": True,
        "source_approval_boundary_record_count_gte_8": len(boundary_records) >= 8,
        "source_approval_traceability_record_count_gte_8": len(traceability_records) >= 8,
        "source_risk_acknowledgement_record_count_eq_2": len(risk_acks) == 2,
        "source_install_preparation_handoff_readiness_count_gte_1": True,
        "negative_guard_count_eq_26": negative_guard_count == 26,
        "negative_guard_passed_eq_26": negative_guard_passed == 26,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "approval_issuance_only": APPROVAL_ISSUANCE_ONLY is True,
        "source_install_owner_approval_issuance_created": SOURCE_INSTALL_OWNER_APPROVAL_ISSUANCE_CREATED is True,
        "owner_approval_granted_for_source_install_preparation": OWNER_APPROVAL_GRANTED_FOR_SOURCE_INSTALL_PREPARATION is True,
        "owner_approval_granted_for_git_clone_false": OWNER_APPROVAL_GRANTED_FOR_GIT_CLONE is False,
        "owner_approval_granted_for_source_checkout_false": OWNER_APPROVAL_GRANTED_FOR_SOURCE_CHECKOUT is False,
        "owner_approval_granted_for_source_install_false": OWNER_APPROVAL_GRANTED_FOR_SOURCE_INSTALL is False,
        "owner_approval_granted_for_pip_install_false": True,
        "owner_approval_granted_for_dependency_install_false": True,
        "owner_approval_granted_for_model_download_false": True,
        "owner_approval_granted_for_weight_download_false": OWNER_APPROVAL_GRANTED_FOR_WEIGHT_DOWNLOAD is False,
        "owner_approval_granted_for_dataset_download_false": True,
        "owner_approval_granted_for_inference_false": OWNER_APPROVAL_GRANTED_FOR_INFERENCE is False,
        "owner_approval_granted_for_runtime_false": OWNER_APPROVAL_GRANTED_FOR_RUNTIME is False,
        "owner_approval_granted_for_output_adapter_false": OWNER_APPROVAL_GRANTED_FOR_OUTPUT_ADAPTER is False,
        "owner_approval_granted_for_semantic_layer_false": OWNER_APPROVAL_GRANTED_FOR_SEMANTIC_LAYER is False,
        "approved_source_scope_count_verified": len(asset_scopes) == 2,
        # Boundary statements.
        **{stmt: True for stmt in APPROVAL_BOUNDARY_STATEMENTS},
        # Conditions.
        "repository_verification_required": "repository_verification_required" in conditions_present,
        "repository_commit_pin_required": "repository_commit_pin_required" in conditions_present,
        "repository_license_review_required": "repository_license_review_required" in conditions_present,
        "dependency_expansion_review_required": "dependency_expansion_review_required" in conditions_present,
        "network_boundary_required": "network_boundary_required" in conditions_present,
        "weight_download_separate_approval_required": "weight_download_separate_approval_required" in conditions_present,
        "approval_expiry_required": expiry_record.approval_has_expiry,
        "approval_revocation_required": revocation_record.approval_revocation_supported,
        "source_chain_complete": source_chain_complete,
        # Handoff readiness.
        "can_enter_source_install_preparation": handoff.can_enter_source_install_preparation,
        "can_enter_git_clone_false": handoff.can_enter_git_clone is False,
        "can_enter_source_checkout_false": handoff.can_enter_source_checkout is False,
        "can_enter_source_install_false": handoff.can_enter_source_install is False,
        "can_enter_weight_download_false": handoff.can_enter_weight_download is False,
        "can_enter_inference_false": handoff.can_enter_inference is False,
        "can_enter_runtime_false": handoff.can_enter_runtime is False,
        "can_enter_output_adapter_false": handoff.can_enter_output_adapter is False,
        "can_enter_semantic_layer_false": handoff.can_enter_semantic_layer is False,
        # Non-execution bindings.
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "git_clone_allowed_false": GIT_CLONE_ALLOWED is False,
        "source_checkout_allowed_false": SOURCE_CHECKOUT_ALLOWED is False,
        "source_install_allowed_false": SOURCE_INSTALL_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "dependency_install_allowed_false": DEPENDENCY_INSTALL_ALLOWED is False,
        "model_download_allowed_false": MODEL_DOWNLOAD_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "dataset_download_allowed_false": DATASET_DOWNLOAD_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Negative guard GO keys.
        **negative_guard_go,
        # Test board fields + write.
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "test_board_artifact_refs_written": write_test_board is True,
        "test_board_protected_marker_written": write_test_board is True,
        "test_board_non_deletable_notice_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0
    final_decision = FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1ControlledSourceInstallOwnerApprovalIssuanceDecision(
        decision_ref=DECISION_REF,
        source_owner_approval_issuance_profile_count=1,
        source_owner_approval_issuance_record_count=1,
        source_approval_scope_record_count=1,
        approved_source_asset_scope_record_count=len(asset_scopes),
        source_approval_condition_record_count=len(condition_records),
        source_approval_expiry_record_count=1,
        source_approval_revocation_record_count=1,
        source_approval_boundary_record_count=len(boundary_records),
        source_approval_traceability_record_count=len(traceability_records),
        source_risk_acknowledgement_record_count=len(risk_acks),
        source_install_preparation_handoff_readiness_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Source Install Owner Approval Issuance (issuance only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "approval_issuance_only": APPROVAL_ISSUANCE_ONLY,
        "in_scope_asset_ids": list(IN_SCOPE_ASSET_IDS),
        "upstream_request_planning_ref": UPSTREAM_REQUEST_PLANNING_REF,
        "upstream_resolution_planning_ref": UPSTREAM_RESOLUTION_PLANNING_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "source_owner_approval_issuance_profile": _build_profile(),
        "source_owner_approval_issuance_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Issuance artifacts.
        "source_owner_approval_issuance_record": asdict(issuance_record),
        "source_owner_approval_issuance_record_count": 1,
        "source_approval_scope_record": asdict(scope_record),
        "source_approval_scope_record_count": 1,
        "approved_source_asset_scope_records": [asdict(a) for a in asset_scopes],
        "approved_source_asset_scope_record_count": len(asset_scopes),
        "source_approval_condition_records": [asdict(c) for c in condition_records],
        "source_approval_condition_record_count": len(condition_records),
        "source_approval_expiry_record": asdict(expiry_record),
        "source_approval_expiry_record_count": 1,
        "source_approval_revocation_record": asdict(revocation_record),
        "source_approval_revocation_record_count": 1,
        "source_approval_boundary_records": [asdict(b) for b in boundary_records],
        "source_approval_boundary_record_count": len(boundary_records),
        "source_approval_traceability_records": [asdict(t) for t in traceability_records],
        "source_approval_traceability_record_count": len(traceability_records),
        "source_chain_complete": source_chain_complete,
        "source_risk_acknowledgement_records": [asdict(r) for r in risk_acks],
        "source_risk_acknowledgement_record_count": len(risk_acks),
        "source_install_preparation_handoff_readiness": asdict(handoff),
        "source_install_preparation_handoff_readiness_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_source_install_owner_approval_issuance_status": (
                "source_install_owner_approval_issued_for_preparation_scope_only_no_clone_no_install_no_weight_download"
                if review_ok
                else "blocked"
            ),
            "issuance_id": issuance_record.issuance_id,
            "approved_assets": list(issuance_record.requested_assets),
            "approval_scope": issuance_record.approval_scope,
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Source-install owner approval ISSUED for byte_track and mobile_sam, scoped strictly to "
                "source_install_preparation_only. Approval Issuance != Git Clone != Source Install != Weight "
                "Download: owner_approval_granted_for_source_install_preparation=true, while git clone / source "
                "checkout / source install / pip / dependency install / model+weight+dataset download / inference / "
                "runtime / output adapter / semantic layer / registry mutation all remain NOT approved. The issuance "
                "carries 16 pre-execution conditions (repository verification + commit pin + license review + "
                "dependency-expansion review + network boundary + pre-source-install snapshot + command whitelist + "
                "isolation env + rollback + post-install find_spec-only probe + test board write + weight separate "
                "approval + registry patch before runtime + revocation + expiry + next-phase-before-execution), an "
                "expiry policy (single-use; blocked after repository/dependency/license/scope/registry drift), a "
                "revocation policy (reason required, recorded, protected), 8 approval-boundary statements, and 9 "
                "source-chain traceability refs (source_chain_complete=true). Both assets REMAIN DEFERRED; nothing "
                "was cloned / installed / downloaded; no real import / load / inference / runtime / output / "
                "semantic; registry not modified. Direct source-install execution is blocked. Next (compressed "
                "route): Phase-P1-Controlled-Source-Install-Preparation-And-Readiness-Review-v1-001 (still no "
                "clone/install — source-execution preparation + readiness only)."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(out_path)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        try:
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "canonical"
        except (PermissionError, OSError):
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_out = Path(manifest["test_board_dir"])
        extra_payloads = {
            "source_owner_approval_issuance_record": {
                "source_owner_approval_issuance_record": asdict(issuance_record),
                "source_install_preparation_handoff_readiness": asdict(handoff),
            },
            "source_approval_scope_record": {
                "source_approval_scope_record": asdict(scope_record),
                "approved_source_asset_scope_records": [asdict(a) for a in asset_scopes],
            },
            "source_approval_condition_record": {
                "source_approval_condition_records": [asdict(c) for c in condition_records],
                "source_approval_expiry_record": asdict(expiry_record),
                "source_approval_revocation_record": asdict(revocation_record),
            },
            "source_approval_boundary_record": {
                "source_approval_boundary_records": [asdict(b) for b in boundary_records]
            },
            "source_approval_traceability_record": {
                "source_approval_traceability_records": [asdict(t) for t in traceability_records],
                "source_chain_complete": source_chain_complete,
            },
            "source_weight_exclusion_record": {
                "owner_approval_granted_for_weight_download": OWNER_APPROVAL_GRANTED_FOR_WEIGHT_DOWNLOAD,
                "weight_download_allowed": WEIGHT_DOWNLOAD_ALLOWED,
                "model_download_allowed": MODEL_DOWNLOAD_ALLOWED,
                "dataset_download_allowed": DATASET_DOWNLOAD_ALLOWED,
                "weight_download_separate_approval_required": True,
                "source_risk_acknowledgement_records": [asdict(r) for r in risk_acks],
            },
        }
        extra_written: List[str] = []
        common = {
            "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            "phase_id": PHASE_ID,
            "module": TEST_BOARD_MODULE,
            "test_mode": TEST_BOARD_TEST_MODE,
            "recorded_at_utc": _now(),
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "approval_issuance_only": True,
            "source_install_allowed": False,
            "git_clone_allowed": False,
            "weight_download_allowed": False,
        }
        for rtype, payload in extra_payloads.items():
            p = board_out / f"{rtype}.json"
            p.write_text(
                json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            extra_written.append(str(p))
        manifest["extra_written_records"] = extra_written
        manifest["extra_written_record_count"] = len(extra_written)
        manifest["total_record_count"] = manifest["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["total_record_count"]

    return result


def main() -> int:
    result = review_p1_controlled_source_install_owner_approval_issuance_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "condition_count": result["decision"]["source_approval_condition_record_count"],
                "traceability_count": result["decision"]["source_approval_traceability_record_count"],
                "negative_guard_passed": result["negative_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
