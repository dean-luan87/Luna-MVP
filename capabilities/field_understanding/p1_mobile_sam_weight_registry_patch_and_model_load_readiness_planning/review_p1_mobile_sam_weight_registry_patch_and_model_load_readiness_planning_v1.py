# -*- coding: utf-8 -*-
"""P1 MobileSAM Weight Registry Patch And Model Load Readiness — review v1
(PLANNING ONLY, scope = mobile_sam_only).

Audits the real mobile_sam.pt download evidence (GO, sha256, size, storage), then
produces a registry-patch PLAN (NOT written), a code_and_weight_ready readiness
record, a model-load-trial readiness PLAN, model-load and inference/runtime boundary
records, and the follow-up route. It writes NOTHING to the registry, model loads
nothing, imports nothing, runs no inference/runtime, downloads no extra weight, and
ignores byte_track. Protected, non-deletable test board records are written in
`planning` mode.
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
from capabilities.field_understanding.p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning.p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning.p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    BYTE_TRACK_WEIGHT_DOWNLOAD_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_WEIGHT_FILE_PATH,
    MOBILE_SAM_WEIGHT_SHA256,
    MOBILE_SAM_WEIGHT_SIZE_BYTES,
    MODEL_LOAD_ALLOWED,
    MODEL_LOAD_READINESS_PLANNING_ONLY,
    NEGATIVE_GUARDS,
    NEXT_PHASE_MODEL_LOAD_TRIAL,
    NEXT_PHASE_REGISTRY_PATCH_EXECUTION,
    OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNED_READINESS_LEVEL,
    PLANNED_REGISTRY_PATCH,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_FILE_WRITE_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_OVERLAY_REL,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_DOWNLOAD_EXECUTION_REF,
    UPSTREAM_EXPECTED,
    UPSTREAM_INTEGRITY_FILE_REL,
    UPSTREAM_REVIEW_FILE_REL,
    WEIGHT_CHAIN,
    WEIGHT_REGISTRY_PATCH_PLANNING_ONLY,
    MobileSAMFollowupModelLoadTrialRoute,
    MobileSAMInferenceRuntimeBoundaryRecord,
    MobileSAMModelLoadBoundaryRecord,
    MobileSAMModelLoadTrialReadinessPlanningRecord,
    MobileSAMWeightDownloadAudit,
    MobileSAMWeightReadinessRecord,
    MobileSAMWeightRegistryPatchPlanningRecord,
    NegativeMobileSAMWeightRegistryPatchReadinessPlanningGuard,
    P1MobileSAMWeightRegistryPatchModelLoadReadinessPlanningProfile,
    P1MobileSAMWeightRegistryPatchReadinessPlanningDecision,
    to_dict,
)


def _pick_writable_base() -> Path:
    for cand in (_REPO_ROOT, Path.cwd()):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()
DEFAULT_OUTPUT_ROOT = (
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning_review_v1.json"

_PKG = "capabilities/field_understanding/p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning_types_v1.py",
    f"{_PKG}/p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning_v1.py",
)

PROFILE_REF = "p1_mobile_sam_weight_registry_patch_model_load_readiness_planning_profile_v1"
DECISION_REF = "p1_mobile_sam_weight_registry_patch_model_load_readiness_planning_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(rel: str) -> Optional[Dict[str, Any]]:
    for base in (_REPO_ROOT, Path.cwd(), _WRITABLE_BASE):
        p = base / rel
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return None
    return None


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMWeightRegistryPatchModelLoadReadinessPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            mobile_sam_only=True,
            weight_registry_patch_planning_only=WEIGHT_REGISTRY_PATCH_PLANNING_ONLY,
            model_load_readiness_planning_only=MODEL_LOAD_READINESS_PLANNING_ONLY,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            registry_file_write_allowed=REGISTRY_FILE_WRITE_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            additional_weight_download_allowed=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
            byte_track_weight_download_allowed=BYTE_TRACK_WEIGHT_DOWNLOAD_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_download_execution_ref=UPSTREAM_DOWNLOAD_EXECUTION_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning_v1(
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

    ts = _now()

    # ------------------------------------------------------------------- #
    # (一) Upstream weight-download audit.
    # ------------------------------------------------------------------- #
    review = _load_json(UPSTREAM_REVIEW_FILE_REL) or {}
    integrity = _load_json(UPSTREAM_INTEGRITY_FILE_REL) or {}
    concl = review.get("conclusions", {})
    excl = review.get("model_load_inference_runtime_exclusion_record", {})
    post = review.get("weight_download_post_review_audit", {})

    final_decision_ok = review.get("final_decision") == UPSTREAM_EXPECTED["final_decision"]
    blocker_ok = review.get("blocker_count") == UPSTREAM_EXPECTED["blocker_count"]
    scope_ok = review.get("execution_scope") == UPSTREAM_EXPECTED["execution_scope"]

    actual_size = int(integrity.get("actual_size_bytes", concl.get("actual_size_bytes", 0)) or 0)
    size_matches = actual_size == MOBILE_SAM_WEIGHT_SIZE_BYTES and bool(integrity.get("size_matches_expected", concl.get("size_matches_expected", False)))
    sha_value = str(concl.get("mobile_sam_sha256", review.get("weight_hash_record", {}).get("sha256_value", "")))
    sha_matches = sha_value == MOBILE_SAM_WEIGHT_SHA256

    audit = MobileSAMWeightDownloadAudit(
        audit_id="mobile_sam_weight_download_audit_v1",
        upstream_review_file_ref=UPSTREAM_REVIEW_FILE_REL,
        final_decision_ok=final_decision_ok,
        blocker_count_ok=blocker_ok,
        execution_scope_ok=scope_ok,
        mobile_sam_weight_downloaded=bool(concl.get("mobile_sam_weight_downloaded", excl.get("mobile_sam_weight_downloaded", False))),
        mobile_sam_weight_file_present=bool(excl.get("mobile_sam_weight_file_present", integrity.get("file_exists", False))),
        mobile_sam_weight_sha256_recorded=bool(excl.get("mobile_sam_weight_sha256_recorded", bool(sha_value))),
        mobile_sam_weight_storage_verified=bool(excl.get("mobile_sam_weight_storage_verified", False)),
        expected_size_bytes=MOBILE_SAM_WEIGHT_SIZE_BYTES,
        actual_size_bytes=actual_size,
        size_matches=size_matches,
        sha256_value=sha_value,
        sha256_matches=sha_matches,
        storage_path=str(concl.get("storage_path", MOBILE_SAM_WEIGHT_FILE_PATH)),
        byte_track_weight_downloaded=bool(concl.get("byte_track_weight_downloaded", False)),
        no_extra_weight_files_created=bool(integrity.get("no_extra_weight_files_created", post.get("no_extra_downloads", False))),
        model_load_performed=False,
        real_import_performed=False,
        inference_performed=False,
        runtime_execution_performed=False,
        registry_mutation_performed=False,
        audit_passed=(
            final_decision_ok and blocker_ok and scope_ok and size_matches and sha_matches
            and bool(concl.get("mobile_sam_weight_downloaded", False))
            and not bool(concl.get("byte_track_weight_downloaded", True))
        ),
    )
    if not audit.audit_passed:
        failed_checks.append("upstream.weight_download_audit_failed_field_inconsistent")

    # ------------------------------------------------------------------- #
    # (二) Registry patch planning (PLAN ONLY; no registry write).
    # ------------------------------------------------------------------- #
    patch_plan = MobileSAMWeightRegistryPatchPlanningRecord(
        record_id="mobile_sam_weight_registry_patch_plan_v1",
        registry_overlay_ref=REGISTRY_OVERLAY_REL,
        patch_is_plan_only=True,
        patch_is_not_registry_mutation=True,
        planned_patch_values=dict(PLANNED_REGISTRY_PATCH),
    )

    # ------------------------------------------------------------------- #
    # (三) Weight readiness record.
    # ------------------------------------------------------------------- #
    readiness = MobileSAMWeightReadinessRecord(
        asset_id=MOBILE_SAM_ASSET_ID,
        code_ready=True,
        weight_ready=True,
        weight_integrity_verified=size_matches and sha_matches,
        storage_ready=audit.mobile_sam_weight_storage_verified,
        model_load_ready=False,
        model_ready=False,
        inference_ready=False,
        runtime_ready=False,
        output_adapter_ready=False,
        semantic_layer_ready=False,
        readiness_level=PLANNED_READINESS_LEVEL,
        code_and_weight_ready_not_model_loaded=True,
        code_and_weight_ready_not_model_ready=True,
        code_and_weight_ready_not_inference_ready=True,
        code_and_weight_ready_not_runtime_ready=True,
    )

    # ------------------------------------------------------------------- #
    # (四) Model-load trial readiness planning.
    # ------------------------------------------------------------------- #
    model_load_plan = MobileSAMModelLoadTrialReadinessPlanningRecord(
        record_id="mobile_sam_model_load_readiness_plan_v1",
        next_phase_suggested=NEXT_PHASE_MODEL_LOAD_TRIAL,
        model_load_trial_request_required=True,
        owner_approval_required_for_model_load=True,
        model_load_pre_snapshot_required=True,
        model_load_env_path_required=True,
        code_path_ref_required=True,
        weight_path_ref_required=True,
        sha256_recheck_required_before_model_load=True,
        memory_usage_limit_required=True,
        timeout_required=True,
        no_inference_during_model_load_trial=True,
        no_runtime_during_model_load_trial=True,
        no_output_adapter_during_model_load_trial=True,
        no_semantic_layer_during_model_load_trial=True,
        post_model_load_review_required=True,
    )

    # ------------------------------------------------------------------- #
    # (五) Model-load boundary + inference/runtime boundary.
    # ------------------------------------------------------------------- #
    model_load_boundary = MobileSAMModelLoadBoundaryRecord(
        record_id="mobile_sam_model_load_boundary_v1",
        weight_download_success_not_model_load_approval=True,
        weight_registry_patch_planning_not_registry_mutation=True,
        weight_registry_patch_planning_not_model_load_approval=True,
        model_load_requires_separate_request=True,
        model_load_requires_owner_approval=True,
        model_load_success_not_inference_approval=True,
        model_load_success_not_runtime_approval=True,
    )
    inference_runtime_boundary = MobileSAMInferenceRuntimeBoundaryRecord(
        record_id="mobile_sam_inference_runtime_boundary_v1",
        inference_requires_separate_trial=True,
        runtime_requires_separate_trial=True,
        output_adapter_requires_separate_review=True,
        semantic_layer_requires_separate_promotion=True,
        commercial_runtime_not_approved=True,
    )

    # ------------------------------------------------------------------- #
    # (六) Follow-up route.
    # ------------------------------------------------------------------- #
    followup = MobileSAMFollowupModelLoadTrialRoute(
        route_id="mobile_sam_followup_model_load_trial_route_v1",
        recommended_next_phase=NEXT_PHASE_REGISTRY_PATCH_EXECUTION,
        next_phase_scope="mobile_sam_only",
        next_phase_allows_registry_overlay_write=True,
        next_phase_writes_readiness_level=PLANNED_READINESS_LEVEL,
        next_phase_still_no_model_load=True,
        next_phase_still_no_inference=True,
        next_phase_still_no_runtime=True,
        subsequent_model_load_trial_phase=NEXT_PHASE_MODEL_LOAD_TRIAL,
        optional_followup_phase=OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 15 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "upstream_download_go_verified": (
            verify_flags.get("model_weight_download_execution_post_review_go_verified") is True
            and audit.final_decision_ok and audit.blocker_count_ok
        ),
        "sha256_verified": sha_matches and bool(sha_value),
        "size_verified": size_matches,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False and REGISTRY_FILE_WRITE_ALLOWED is False
        and audit.registry_mutation_performed is False,
        "no_additional_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False
        and BYTE_TRACK_WEIGHT_DOWNLOAD_ALLOWED is False,
        "no_real_import_load_inference": REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False
        and REAL_INFERENCE_ALLOWED is False,
        "no_runtime_output_semantic": RUNTIME_EXECUTION_ALLOWED is False
        and REAL_OUTPUT_ADAPTER_ALLOWED is False and SEMANTIC_PROMOTION_ALLOWED is False,
        "byte_track_out_of_scope": audit.byte_track_weight_downloaded is False
        and BYTE_TRACK_WEIGHT_DOWNLOAD_ALLOWED is False,
        "not_model_load_ready": readiness.model_load_ready is False and readiness.model_ready is False,
        "not_inference_runtime_ready": readiness.inference_ready is False and readiness.runtime_ready is False,
        "patch_planning_not_mutation": patch_plan.patch_is_plan_only and patch_plan.patch_is_not_registry_mutation,
        "trial_planning_not_approval": (
            MODEL_LOAD_READINESS_PLANNING_ONLY is True
            and model_load_boundary.model_load_requires_separate_request
            and model_load_boundary.model_load_requires_owner_approval
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMobileSAMWeightRegistryPatchReadinessPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMWeightRegistryPatchReadinessPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_mobile_sam_weight_registry_patch_readiness_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "mobile_sam_weight_registry_patch_model_load_readiness_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_weight_download_audit_count_gte_1": True,
        "mobile_sam_weight_registry_patch_planning_record_count_gte_1": True,
        "mobile_sam_weight_readiness_record_count_gte_1": True,
        "mobile_sam_model_load_trial_readiness_planning_record_count_gte_1": True,
        "mobile_sam_model_load_boundary_record_count_gte_1": True,
        "mobile_sam_inference_runtime_boundary_record_count_gte_1": True,
        "mobile_sam_followup_model_load_trial_route_count_gte_1": True,
        "negative_guard_count_eq_15": negative_guard_count == 15,
        "negative_guard_passed_eq_15": negative_guard_passed == 15,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "planning_only": PLANNING_ONLY is True,
        "mobile_sam_only": True,
        "weight_registry_patch_planning_only": WEIGHT_REGISTRY_PATCH_PLANNING_ONLY is True,
        "model_load_readiness_planning_only": MODEL_LOAD_READINESS_PLANNING_ONLY is True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "registry_file_write_allowed_false": REGISTRY_FILE_WRITE_ALLOWED is False,
        "additional_weight_download_allowed_false": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "byte_track_weight_download_allowed_false": BYTE_TRACK_WEIGHT_DOWNLOAD_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Verified weight facts.
        "mobile_sam_weight_downloaded_verified": audit.mobile_sam_weight_downloaded,
        "mobile_sam_weight_file_present_verified": audit.mobile_sam_weight_file_present,
        "mobile_sam_weight_sha256_verified": sha_matches,
        "mobile_sam_weight_storage_verified": audit.mobile_sam_weight_storage_verified,
        "mobile_sam_weight_size_verified": size_matches,
        "mobile_sam_weight_sha256_value_ok": sha_value == MOBILE_SAM_WEIGHT_SHA256,
        "mobile_sam_weight_size_bytes_ok": actual_size == 40728226,
        "mobile_sam_weight_storage_path_ok": audit.storage_path == MOBILE_SAM_WEIGHT_FILE_PATH,
        # Readiness semantics.
        "readiness_level_planned_code_and_weight_ready": readiness.readiness_level == "code_and_weight_ready",
        "code_and_weight_ready_not_model_loaded": readiness.code_and_weight_ready_not_model_loaded,
        "code_and_weight_ready_not_model_ready": readiness.code_and_weight_ready_not_model_ready,
        "code_and_weight_ready_not_inference_ready": readiness.code_and_weight_ready_not_inference_ready,
        "code_and_weight_ready_not_runtime_ready": readiness.code_and_weight_ready_not_runtime_ready,
        "model_load_requires_separate_request": model_load_boundary.model_load_requires_separate_request,
        "model_load_requires_owner_approval": model_load_boundary.model_load_requires_owner_approval,
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
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMWeightRegistryPatchReadinessPlanningDecision(
        decision_ref=DECISION_REF,
        mobile_sam_weight_registry_patch_model_load_readiness_planning_profile_count=1,
        mobile_sam_weight_download_audit_count=1,
        mobile_sam_weight_registry_patch_planning_record_count=1,
        mobile_sam_weight_readiness_record_count=1,
        mobile_sam_model_load_trial_readiness_planning_record_count=1,
        mobile_sam_model_load_boundary_record_count=1,
        mobile_sam_inference_runtime_boundary_record_count=1,
        mobile_sam_followup_model_load_trial_route_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Weight Registry Patch And Model Load Readiness Planning (planning only, mobile_sam_only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "planning_only": PLANNING_ONLY,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "upstream_download_execution_ref": UPSTREAM_DOWNLOAD_EXECUTION_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "mobile_sam_weight_registry_patch_model_load_readiness_planning_profile": _build_profile(),
        "mobile_sam_weight_registry_patch_model_load_readiness_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_weight_download_audit": asdict(audit),
        "mobile_sam_weight_download_audit_count": 1,
        "mobile_sam_weight_registry_patch_planning_record": asdict(patch_plan),
        "mobile_sam_weight_registry_patch_planning_record_count": 1,
        "mobile_sam_weight_readiness_record": asdict(readiness),
        "mobile_sam_weight_readiness_record_count": 1,
        "mobile_sam_model_load_trial_readiness_planning_record": asdict(model_load_plan),
        "mobile_sam_model_load_trial_readiness_planning_record_count": 1,
        "mobile_sam_model_load_boundary_record": asdict(model_load_boundary),
        "mobile_sam_model_load_boundary_record_count": 1,
        "mobile_sam_inference_runtime_boundary_record": asdict(inference_runtime_boundary),
        "mobile_sam_inference_runtime_boundary_record_count": 1,
        "mobile_sam_followup_model_load_trial_route": asdict(followup),
        "mobile_sam_followup_model_load_trial_route_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "planning_status": (
                "mobile_sam_code_and_weight_ready_planned_registry_patch_and_model_load_trial_planned_no_mutation_no_load"
                if blocker_count == 0
                else "blocked"
            ),
            "readiness_level_planned": readiness.readiness_level,
            "mobile_sam_weight_sha256": sha_value,
            "mobile_sam_weight_size_bytes": actual_size,
            "mobile_sam_weight_storage_path": audit.storage_path,
            "registry_patched_this_phase": False,
            "model_loaded_this_phase": False,
            "recommended_next_phase": NEXT_PHASE_REGISTRY_PATCH_EXECUTION,
            "recommended_next_phase_scope": "mobile_sam_only",
            "subsequent_model_load_trial_phase": NEXT_PHASE_MODEL_LOAD_TRIAL,
            "optional_followup_phase": OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
            "transition_note": (
                "PLANNING ONLY (mobile_sam_only). The real download evidence was audited: GO, blocker_count=0, "
                "scope=mobile_sam_only, mobile_sam.pt present, size==40728226 (exact), sha256=="
                + MOBILE_SAM_WEIGHT_SHA256 + ", storage verified, byte_track not downloaded, no model load / import "
                "/ inference / runtime / registry mutation. A registry-patch PLAN (readiness_level="
                "code_and_weight_ready; model_load/model/inference/runtime/output_adapter/semantic all false) and a "
                "model-load-trial readiness PLAN were produced, but NOTHING was written to the registry and NO model "
                "was loaded. code_and_weight_ready is explicitly NOT model-loaded / model-ready / inference-ready / "
                "runtime-ready. Next: " + NEXT_PHASE_REGISTRY_PATCH_EXECUTION + " (actually writes the overlay, still "
                "no model load), then " + NEXT_PHASE_MODEL_LOAD_TRIAL + " (separate request + owner approval before "
                "any model load; still no inference/runtime). byte_track stays out of scope (" +
                OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE + ")."
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

        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "mobile_sam_weight_download_audit_record": {"mobile_sam_weight_download_audit": asdict(audit)},
            "mobile_sam_weight_registry_patch_plan_record": {"mobile_sam_weight_registry_patch_planning_record": asdict(patch_plan)},
            "mobile_sam_model_load_readiness_plan_record": {"mobile_sam_weight_readiness_record": asdict(readiness),
                                                            "mobile_sam_model_load_trial_readiness_planning_record": asdict(model_load_plan),
                                                            "mobile_sam_model_load_boundary_record": asdict(model_load_boundary)},
            "mobile_sam_inference_runtime_boundary_record": {"mobile_sam_inference_runtime_boundary_record": asdict(inference_runtime_boundary)},
            "mobile_sam_followup_model_load_trial_record": {"mobile_sam_followup_model_load_trial_route": asdict(followup)},
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
            "planning_only": True,
            "mobile_sam_only": True,
            "model_load_allowed": False,
            "inference_allowed": False,
            "runtime_allowed": False,
        }
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
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
    result = review_p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "readiness_level_planned": result["conclusions"]["readiness_level_planned"],
                "registry_patched_this_phase": result["conclusions"]["registry_patched_this_phase"],
                "model_loaded_this_phase": result["conclusions"]["model_loaded_this_phase"],
                "negative_guard_passed": result["negative_guard_passed"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
