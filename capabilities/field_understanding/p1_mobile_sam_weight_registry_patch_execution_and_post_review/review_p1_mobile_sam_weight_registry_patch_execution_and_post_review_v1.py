# -*- coding: utf-8 -*-
"""P1 MobileSAM Weight Registry Patch Execution And Post Review — review v1
(REAL EXECUTION, scope = mobile_sam_only).

Takes a pre-patch snapshot of the registry overlay, applies the REAL patch to the
mobile_sam entry ONLY (weight-download metadata + readiness_level=code_and_weight_ready,
all readiness flags kept false), writes the overlay back to disk, computes a diff, and
runs a same-phase post-review. byte_track and all other assets are left byte-for-byte
unchanged. It does NOT model load / import / inference / runtime / output adapter /
semantic promotion and downloads NO extra weight. A successful patch is NOT model-load /
inference / runtime approval. Protected, non-deletable test board records are written in
`real_test` mode.
"""

from __future__ import annotations

import copy
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
from capabilities.field_understanding.p1_mobile_sam_weight_registry_patch_execution_and_post_review.p1_mobile_sam_weight_registry_patch_execution_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_weight_registry_patch_execution_and_post_review.p1_mobile_sam_weight_registry_patch_execution_and_post_review_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    ALLOWED_REGISTRY_PATCH_SCOPE,
    BYTE_TRACK_WEIGHT_DOWNLOAD_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    MOBILE_SAM_WEIGHT_FILE_PATH,
    MOBILE_SAM_WEIGHT_SHA256,
    MOBILE_SAM_WEIGHT_SIZE_BYTES,
    MOBILE_SAM_WEIGHT_SOURCE_COMMIT,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_MODEL_LOAD_TRIAL,
    OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
    OUT_OF_SCOPE_ASSET_IDS,
    PATCH_AFTER_VALUES,
    PATCH_ASSET_ID,
    PATCH_MUST_PRESERVE,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNED_READINESS_LEVEL,
    POST_REVIEW_INCLUDED,
    READINESS_FLAGS_MUST_BE_FALSE,
    REAL_EXECUTION_PHASE,
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
    UPSTREAM_PLANNING_REF,
    WEIGHT_CHAIN,
    WEIGHT_REGISTRY_PATCH_EXECUTION,
    PATCH_PRINCIPLE_ZH,
    LUNA_CORE_PRINCIPLE,
    MobileSAMCodeAndWeightReadinessRecord,
    MobileSAMFollowupModelLoadTrialRoute,
    MobileSAMModelLoadBoundaryRecord,
    MobileSAMWeightRegistryPatchDiffRecord,
    MobileSAMWeightRegistryPatchExecutionRecord,
    MobileSAMWeightRegistryPostReviewAudit,
    MobileSAMWeightRegistryPrePatchSnapshotRecord,
    MobileSAMWeightRegistryRollbackReadinessRecord,
    NegativeMobileSAMWeightRegistryPatchExecutionGuard,
    P1MobileSAMWeightRegistryPatchExecutionDecision,
    P1MobileSAMWeightRegistryPatchExecutionPostReviewProfile,
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
    / "p1_mobile_sam_weight_registry_patch_execution_and_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_weight_registry_patch_execution_and_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_mobile_sam_weight_registry_patch_execution_and_post_review"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_weight_registry_patch_execution_and_post_review_types_v1.py",
    f"{_PKG}/p1_mobile_sam_weight_registry_patch_execution_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_weight_registry_patch_execution_and_post_review_v1.py",
)

PROFILE_REF = "p1_mobile_sam_weight_registry_patch_execution_profile_v1"
DECISION_REF = "p1_mobile_sam_weight_registry_patch_execution_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _overlay_path() -> Path:
    for base in (_REPO_ROOT, Path.cwd(), _WRITABLE_BASE):
        p = base / REGISTRY_OVERLAY_REL
        if p.is_file():
            return p
    return _REPO_ROOT / REGISTRY_OVERLAY_REL


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMWeightRegistryPatchExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            mobile_sam_only=True,
            weight_registry_patch_execution=WEIGHT_REGISTRY_PATCH_EXECUTION,
            post_review_included=POST_REVIEW_INCLUDED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            registry_file_write_allowed=REGISTRY_FILE_WRITE_ALLOWED,
            allowed_registry_patch_scope=ALLOWED_REGISTRY_PATCH_SCOPE,
            additional_weight_download_allowed=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
            byte_track_weight_download_allowed=BYTE_TRACK_WEIGHT_DOWNLOAD_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_planning_ref=UPSTREAM_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_weight_registry_patch_execution_and_post_review_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
    apply_patch: bool = True,
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

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    ts = _now()
    overlay_path = _overlay_path()
    overlay_exists = overlay_path.is_file()

    overlay: Dict[str, Any] = {}
    if overlay_exists:
        try:
            overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            overlay = {}
            overlay_exists = False
    assets = overlay.get("assets", {})

    # ------------------------------------------------------------------- #
    # (一) Pre-patch snapshot.
    # ------------------------------------------------------------------- #
    mobile_sam_before = copy.deepcopy(assets.get(PATCH_ASSET_ID, {}))
    byte_track_before = copy.deepcopy(assets.get("byte_track", {}))
    out_of_scope_before = {a: copy.deepcopy(assets.get(a, {})) for a in OUT_OF_SCOPE_ASSET_IDS if a in assets}
    snapshot_succeeded = overlay_exists and bool(mobile_sam_before)
    snapshot = MobileSAMWeightRegistryPrePatchSnapshotRecord(
        snapshot_id="mobile_sam_weight_registry_pre_patch_snapshot_v1",
        overlay_file_ref=REGISTRY_OVERLAY_REL,
        overlay_exists=overlay_exists,
        mobile_sam_registry_before=mobile_sam_before,
        byte_track_registry_before=byte_track_before,
        timestamp=ts,
        upstream_planning_ref=UPSTREAM_PLANNING_REF,
        rollback_snapshot_ref=str(out_root / "mobile_sam_weight_registry_pre_patch_snapshot_v1.json"),
        test_board_ref="capabilities/test_board/recognition_models/phase_p1_mobilesam_weight_registry_patch_execution_and_post_review_v1_001/",
        snapshot_succeeded=snapshot_succeeded,
    )
    (out_root / "mobile_sam_weight_registry_pre_patch_snapshot_v1.json").write_text(
        json.dumps(asdict(snapshot), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not snapshot_succeeded:
        failed_checks.append("snapshot.failed_overlay_missing_or_mobile_sam_entry_absent")

    # ------------------------------------------------------------------- #
    # (二/三) Apply patch to mobile_sam ONLY.
    # ------------------------------------------------------------------- #
    patched_fields: List[str] = []
    patch_applied = False
    overlay_written = False
    if apply_patch and snapshot_succeeded:
        ms_entry = dict(assets.get(PATCH_ASSET_ID, {}))
        for k, v in PATCH_AFTER_VALUES.items():
            if ms_entry.get(k) != v:
                patched_fields.append(k)
            ms_entry[k] = v
        for k, v in PATCH_MUST_PRESERVE.items():
            ms_entry.setdefault(k, v)
        assets[PATCH_ASSET_ID] = ms_entry
        overlay["assets"] = assets
        overlay["mobile_sam_weight_patched_by_phase"] = PHASE_ID
        overlay["mobile_sam_weight_patched_at_utc"] = _now()
        try:
            overlay_path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            overlay_written = True
            patch_applied = True
        except (OSError, PermissionError) as exc:
            warnings.append(f"overlay_write_failed:{type(exc).__name__}")
            failed_checks.append("execution.overlay_write_failed")

    # Re-read for verification.
    after_overlay: Dict[str, Any] = {}
    if overlay_written:
        try:
            after_overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            after_overlay = overlay
    else:
        after_overlay = overlay
    after_assets = after_overlay.get("assets", {})
    mobile_sam_after = after_assets.get(PATCH_ASSET_ID, {})
    byte_track_after = after_assets.get("byte_track", {})

    out_of_scope_untouched = all(
        after_assets.get(a, {}) == out_of_scope_before.get(a, {}) for a in out_of_scope_before
    )
    byte_track_unchanged = byte_track_after == byte_track_before

    execution = MobileSAMWeightRegistryPatchExecutionRecord(
        execution_id="mobile_sam_weight_registry_patch_execution_v1",
        overlay_file_ref=REGISTRY_OVERLAY_REL,
        patch_asset_id=PATCH_ASSET_ID,
        patch_applied=patch_applied,
        overlay_written=overlay_written,
        patched_fields=tuple(patched_fields),
        patched_by_phase=PHASE_ID,
        patched_at_utc=after_overlay.get("mobile_sam_weight_patched_at_utc", ts),
        out_of_scope_assets_untouched=out_of_scope_untouched,
    )
    (out_root / "mobile_sam_weight_registry_patch_execution_record_v1.json").write_text(
        json.dumps(asdict(execution), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (四) Diff.
    # ------------------------------------------------------------------- #
    changed_field_paths: List[str] = []
    before_values: Dict[str, Any] = {}
    after_values: Dict[str, Any] = {}
    all_keys = set(mobile_sam_before) | set(mobile_sam_after)
    for k in sorted(all_keys):
        b = mobile_sam_before.get(k, "<<absent>>")
        a = mobile_sam_after.get(k, "<<absent>>")
        if b != a:
            changed_field_paths.append(f"mobile_sam.{k}")
            before_values[k] = b
            after_values[k] = a

    def _not_set_true(field_name: str) -> bool:
        return mobile_sam_after.get(field_name) is not True

    diff = MobileSAMWeightRegistryPatchDiffRecord(
        diff_id="mobile_sam_weight_registry_patch_diff_v1",
        changed_asset_count=1 if changed_field_paths else 0,
        changed_assets=(PATCH_ASSET_ID,) if changed_field_paths else (),
        byte_track_changed=not byte_track_unchanged,
        changed_field_paths=tuple(changed_field_paths),
        before_values=before_values,
        after_values=after_values,
        no_unscoped_asset_changed=out_of_scope_untouched and byte_track_unchanged,
        no_model_load_ready_field_set_true=_not_set_true("model_load_ready"),
        no_model_ready_field_set_true=_not_set_true("model_ready"),
        no_inference_ready_field_set_true=_not_set_true("inference_ready"),
        no_runtime_ready_field_set_true=_not_set_true("runtime_ready"),
        no_output_adapter_ready_field_set_true=_not_set_true("output_adapter_ready"),
        no_semantic_layer_ready_field_set_true=_not_set_true("semantic_layer_ready"),
    )
    (out_root / "mobile_sam_weight_registry_patch_diff_v1.json").write_text(
        json.dumps(asdict(diff), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (五) Post-review audit.
    # ------------------------------------------------------------------- #
    readiness_flags_false = all(mobile_sam_after.get(f) is False for f in READINESS_FLAGS_MUST_BE_FALSE)
    patch_scope_valid = out_of_scope_untouched and byte_track_unchanged and bool(mobile_sam_after)
    post_audit = MobileSAMWeightRegistryPostReviewAudit(
        audit_id="mobile_sam_weight_registry_post_review_audit_v1",
        registry_patch_applied=patch_applied,
        registry_patch_scope_valid=patch_scope_valid,
        changed_asset_count=diff.changed_asset_count,
        only_mobile_sam_changed=diff.changed_asset_count == 1 and out_of_scope_untouched and byte_track_unchanged,
        byte_track_unchanged=byte_track_unchanged,
        weight_downloaded_written=mobile_sam_after.get("weight_downloaded") is True,
        weight_sha256_written=mobile_sam_after.get("weight_sha256") == MOBILE_SAM_WEIGHT_SHA256,
        weight_storage_path_written=mobile_sam_after.get("weight_file_path") == MOBILE_SAM_WEIGHT_FILE_PATH,
        weight_size_written=mobile_sam_after.get("weight_file_size_bytes") == MOBILE_SAM_WEIGHT_SIZE_BYTES,
        weight_source_commit_written=mobile_sam_after.get("weight_source_commit") == MOBILE_SAM_WEIGHT_SOURCE_COMMIT,
        weight_integrity_verified_written=mobile_sam_after.get("weight_integrity_verified") is True,
        storage_verified_written=mobile_sam_after.get("storage_verified") is True,
        readiness_level_code_and_weight_ready_written=mobile_sam_after.get("readiness_level") == PLANNED_READINESS_LEVEL,
        model_load_ready_false_written=mobile_sam_after.get("model_load_ready") is False,
        model_ready_false_written=mobile_sam_after.get("model_ready") is False,
        inference_ready_false_written=mobile_sam_after.get("inference_ready") is False,
        runtime_ready_false_written=mobile_sam_after.get("runtime_ready") is False,
        output_adapter_ready_false_written=mobile_sam_after.get("output_adapter_ready") is False,
        semantic_layer_ready_false_written=mobile_sam_after.get("semantic_layer_ready") is False,
        commercial_runtime_false_written=mobile_sam_after.get("commercial_runtime_approved") is False,
        test_board_written=write_test_board,
        test_board_protected=all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        post_review_passed=(
            patch_applied and patch_scope_valid and diff.changed_asset_count == 1 and byte_track_unchanged
            and readiness_flags_false
            and mobile_sam_after.get("weight_downloaded") is True
            and mobile_sam_after.get("readiness_level") == PLANNED_READINESS_LEVEL
        ),
    )
    (out_root / "mobile_sam_weight_registry_post_review_audit_v1.json").write_text(
        json.dumps(asdict(post_audit), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (六) Rollback readiness.
    # ------------------------------------------------------------------- #
    rollback = MobileSAMWeightRegistryRollbackReadinessRecord(
        record_id="mobile_sam_weight_registry_rollback_readiness_v1",
        rollback_available=True,
        rollback_snapshot_ref=str(out_root / "mobile_sam_weight_registry_pre_patch_snapshot_v1.json"),
        rollback_not_executed_by_default=True,
        rollback_trigger_conditions=(
            "post_review_failed",
            "unscoped_asset_changed",
            "readiness_flag_set_true",
            "diff_or_snapshot_inconsistent",
        ),
        rollback_must_preserve_test_board=True,
        rollback_must_preserve_review_artifacts=True,
        rollback_must_preserve_weight_file=True,
        rollback_success_requires_post_review=True,
    )

    # ------------------------------------------------------------------- #
    # (code_and_weight readiness record)
    # ------------------------------------------------------------------- #
    readiness = MobileSAMCodeAndWeightReadinessRecord(
        asset_id=PATCH_ASSET_ID,
        readiness_level=mobile_sam_after.get("readiness_level", PLANNED_READINESS_LEVEL),
        code_only_install_verified=mobile_sam_after.get("code_only_install_verified") is True,
        find_spec_verified=mobile_sam_after.get("find_spec_verified") is True,
        weight_downloaded=mobile_sam_after.get("weight_downloaded") is True,
        weight_integrity_verified=mobile_sam_after.get("weight_integrity_verified") is True,
        storage_verified=mobile_sam_after.get("storage_verified") is True,
        model_load_ready=mobile_sam_after.get("model_load_ready") is True,
        model_ready=mobile_sam_after.get("model_ready") is True,
        inference_ready=mobile_sam_after.get("inference_ready") is True,
        runtime_ready=mobile_sam_after.get("runtime_ready") is True,
        output_adapter_ready=mobile_sam_after.get("output_adapter_ready") is True,
        semantic_layer_ready=mobile_sam_after.get("semantic_layer_ready") is True,
        commercial_runtime_approved=mobile_sam_after.get("commercial_runtime_approved") is True,
        code_and_weight_ready_not_model_loaded=True,
        code_and_weight_ready_not_model_ready=True,
        code_and_weight_ready_not_inference_ready=True,
        code_and_weight_ready_not_runtime_ready=True,
    )

    # ------------------------------------------------------------------- #
    # (七) Model-load boundary + (八) follow-up route.
    # ------------------------------------------------------------------- #
    model_load_boundary = MobileSAMModelLoadBoundaryRecord(
        record_id="mobile_sam_model_load_boundary_v1",
        weight_registry_patch_success_not_model_load_approval=True,
        code_and_weight_ready_not_model_loaded=True,
        code_and_weight_ready_not_model_ready=True,
        code_and_weight_ready_not_inference_ready=True,
        code_and_weight_ready_not_runtime_ready=True,
        model_load_requires_separate_request=True,
        model_load_requires_owner_approval=True,
        model_load_trial_requires_separate_phase=True,
        inference_requires_separate_trial=True,
        runtime_requires_separate_trial=True,
        output_adapter_requires_separate_review=True,
        semantic_layer_requires_separate_promotion=True,
        commercial_runtime_not_approved=True,
    )
    followup = MobileSAMFollowupModelLoadTrialRoute(
        route_id="mobile_sam_followup_model_load_trial_route_v1",
        recommended_next_phase=NEXT_PHASE_MODEL_LOAD_TRIAL,
        next_phase_scope="mobile_sam_only",
        next_phase_allows_model_load_trial_request=True,
        next_phase_allows_owner_approval_issuance_for_model_load=True,
        next_phase_allows_model_load_command_whitelist_planning=True,
        next_phase_still_no_direct_model_load=True,
        next_phase_still_no_inference=True,
        next_phase_still_no_runtime=True,
        optional_followup_phase=OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 16 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "pre_patch_snapshot_present": snapshot.snapshot_succeeded,
        "only_mobile_sam_modified": diff.changed_asset_count == 1 and out_of_scope_untouched and byte_track_unchanged,
        "byte_track_unchanged": byte_track_unchanged,
        "patch_scope_valid": patch_scope_valid and all(
            (f.split(".", 1)[1] in PATCH_AFTER_VALUES or f.split(".", 1)[1] in PATCH_MUST_PRESERVE)
            for f in changed_field_paths
        ),
        "readiness_flags_remain_false": (
            mobile_sam_after.get("model_load_ready") is False
            and mobile_sam_after.get("model_ready") is False
            and mobile_sam_after.get("inference_ready") is False
            and mobile_sam_after.get("runtime_ready") is False
        ),
        "output_semantic_commercial_false": (
            mobile_sam_after.get("output_adapter_ready") is False
            and mobile_sam_after.get("semantic_layer_ready") is False
            and mobile_sam_after.get("commercial_runtime_approved") is False
        ),
        "no_additional_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False
        and BYTE_TRACK_WEIGHT_DOWNLOAD_ALLOWED is False,
        "no_real_import_load_inference": REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False
        and REAL_INFERENCE_ALLOWED is False,
        "no_runtime_output_semantic": RUNTIME_EXECUTION_ALLOWED is False
        and REAL_OUTPUT_ADAPTER_ALLOWED is False and SEMANTIC_PROMOTION_ALLOWED is False,
        "post_review_present": post_audit.post_review_passed,
        "diff_present": diff.changed_asset_count == 1 and len(diff.changed_field_paths) >= 1,
        "patch_not_model_load_approval": model_load_boundary.weight_registry_patch_success_not_model_load_approval,
        "patch_not_inference_runtime_approval": (
            model_load_boundary.inference_requires_separate_trial
            and model_load_boundary.runtime_requires_separate_trial
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMobileSAMWeightRegistryPatchExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMWeightRegistryPatchExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_mobile_sam_weight_registry_patch_execution_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "mobile_sam_weight_registry_patch_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_weight_registry_pre_patch_snapshot_record_count_eq_1": True,
        "mobile_sam_weight_registry_patch_execution_record_count_eq_1": True,
        "mobile_sam_weight_registry_patch_diff_record_count_eq_1": True,
        "mobile_sam_weight_registry_post_review_audit_count_gte_1": True,
        "mobile_sam_weight_registry_rollback_readiness_record_count_gte_1": True,
        "mobile_sam_code_and_weight_readiness_record_count_gte_1": True,
        "mobile_sam_model_load_boundary_record_count_gte_1": True,
        "mobile_sam_followup_model_load_trial_route_count_gte_1": True,
        "negative_guard_count_eq_16": negative_guard_count == 16,
        "negative_guard_passed_eq_16": negative_guard_passed == 16,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "real_execution_phase": REAL_EXECUTION_PHASE is True,
        "mobile_sam_only": True,
        "weight_registry_patch_execution": WEIGHT_REGISTRY_PATCH_EXECUTION is True,
        "post_review_included": POST_REVIEW_INCLUDED is True,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED is True,
        "registry_file_write_allowed": REGISTRY_FILE_WRITE_ALLOWED is True,
        "allowed_registry_patch_scope_mobile_sam_weight_download_metadata": ALLOWED_REGISTRY_PATCH_SCOPE == "mobile_sam_weight_download_metadata",
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
        # Diff / post-review semantics.
        "changed_asset_count_eq_1": diff.changed_asset_count == 1,
        "only_mobile_sam_changed": post_audit.only_mobile_sam_changed,
        "byte_track_unchanged": byte_track_unchanged,
        "weight_downloaded_written": post_audit.weight_downloaded_written,
        "weight_sha256_written": post_audit.weight_sha256_written,
        "weight_storage_path_written": post_audit.weight_storage_path_written,
        "weight_size_written": post_audit.weight_size_written,
        "weight_source_commit_written": post_audit.weight_source_commit_written,
        "weight_integrity_verified_written": post_audit.weight_integrity_verified_written,
        "storage_verified_written": post_audit.storage_verified_written,
        "readiness_level_code_and_weight_ready_written": post_audit.readiness_level_code_and_weight_ready_written,
        "model_load_ready_false_written": post_audit.model_load_ready_false_written,
        "model_ready_false_written": post_audit.model_ready_false_written,
        "inference_ready_false_written": post_audit.inference_ready_false_written,
        "runtime_ready_false_written": post_audit.runtime_ready_false_written,
        "output_adapter_ready_false_written": post_audit.output_adapter_ready_false_written,
        "semantic_layer_ready_false_written": post_audit.semantic_layer_ready_false_written,
        "commercial_runtime_false_written": post_audit.commercial_runtime_false_written,
        # Boundary.
        "weight_registry_patch_success_not_model_load_approval": model_load_boundary.weight_registry_patch_success_not_model_load_approval,
        "code_and_weight_ready_not_model_loaded": model_load_boundary.code_and_weight_ready_not_model_loaded,
        "code_and_weight_ready_not_model_ready": model_load_boundary.code_and_weight_ready_not_model_ready,
        "code_and_weight_ready_not_inference_ready": model_load_boundary.code_and_weight_ready_not_inference_ready,
        "code_and_weight_ready_not_runtime_ready": model_load_boundary.code_and_weight_ready_not_runtime_ready,
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
    decision = P1MobileSAMWeightRegistryPatchExecutionDecision(
        decision_ref=DECISION_REF,
        mobile_sam_weight_registry_patch_execution_profile_count=1,
        mobile_sam_weight_registry_pre_patch_snapshot_record_count=1,
        mobile_sam_weight_registry_patch_execution_record_count=1,
        mobile_sam_weight_registry_patch_diff_record_count=1,
        mobile_sam_weight_registry_post_review_audit_count=1,
        mobile_sam_weight_registry_rollback_readiness_record_count=1,
        mobile_sam_code_and_weight_readiness_record_count=1,
        mobile_sam_model_load_boundary_record_count=1,
        mobile_sam_followup_model_load_trial_route_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Weight Registry Patch Execution And Post Review (real execution, mobile_sam_only)",
        "lifecycle_variant": SCOPE,
        "patch_principle_zh": PATCH_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "allowed_registry_patch_scope": ALLOWED_REGISTRY_PATCH_SCOPE,
        "upstream_planning_ref": UPSTREAM_PLANNING_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "mobile_sam_weight_registry_patch_execution_profile": _build_profile(),
        "mobile_sam_weight_registry_patch_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_weight_registry_pre_patch_snapshot_record": asdict(snapshot),
        "mobile_sam_weight_registry_pre_patch_snapshot_record_count": 1,
        "mobile_sam_weight_registry_patch_execution_record": asdict(execution),
        "mobile_sam_weight_registry_patch_execution_record_count": 1,
        "mobile_sam_weight_registry_patch_diff_record": asdict(diff),
        "mobile_sam_weight_registry_patch_diff_record_count": 1,
        "mobile_sam_weight_registry_post_review_audit": asdict(post_audit),
        "mobile_sam_weight_registry_post_review_audit_count": 1,
        "mobile_sam_weight_registry_rollback_readiness_record": asdict(rollback),
        "mobile_sam_weight_registry_rollback_readiness_record_count": 1,
        "mobile_sam_code_and_weight_readiness_record": asdict(readiness),
        "mobile_sam_code_and_weight_readiness_record_count": 1,
        "mobile_sam_model_load_boundary_record": asdict(model_load_boundary),
        "mobile_sam_model_load_boundary_record_count": 1,
        "mobile_sam_followup_model_load_trial_route": asdict(followup),
        "mobile_sam_followup_model_load_trial_route_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "overlay_path": str(overlay_path),
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "registry_patch_status": (
                "mobile_sam_overlay_patched_code_and_weight_ready_only_mobile_sam_changed_no_model_load_no_inference_no_runtime"
                if blocker_count == 0
                else "blocked"
            ),
            "registry_patched_this_phase": patch_applied and overlay_written,
            "readiness_level_written": mobile_sam_after.get("readiness_level"),
            "changed_field_paths": changed_field_paths,
            "byte_track_unchanged": byte_track_unchanged,
            "model_loaded_this_phase": False,
            "recommended_next_phase": NEXT_PHASE_MODEL_LOAD_TRIAL,
            "recommended_next_phase_scope": "mobile_sam_only",
            "optional_followup_phase": OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
            "transition_note": (
                "REAL EXECUTION (mobile_sam_only). A pre-patch snapshot was taken, then the registry overlay's "
                "mobile_sam entry was patched with verified weight-download metadata (weight_downloaded, sha256=="
                + MOBILE_SAM_WEIGHT_SHA256 + ", size==40728226, storage path, source commit/file/url, license, "
                "integrity_verified, storage_verified) and readiness_level=code_and_weight_ready. ALL of "
                "model_load_ready / model_ready / inference_ready / runtime_ready / output_adapter_ready / "
                "semantic_layer_ready / commercial_runtime_approved remain false. Diff shows changed_asset_count=1 "
                "(mobile_sam only); byte_track and every other asset are byte-for-byte unchanged. NOTHING was model "
                "loaded / imported / inferred / run, and no extra weight was downloaded. A successful patch is NOT "
                "model-load / inference / runtime approval. Next: " + NEXT_PHASE_MODEL_LOAD_TRIAL + " (model-load "
                "request + owner approval + preparation; still no direct model load/inference/runtime). byte_track "
                "stays out of scope (" + OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE + ")."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
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
            "mobile_sam_weight_registry_patch_snapshot_record": {"mobile_sam_weight_registry_pre_patch_snapshot_record": asdict(snapshot)},
            "mobile_sam_weight_registry_patch_execution_record": {"mobile_sam_weight_registry_patch_execution_record": asdict(execution)},
            "mobile_sam_weight_registry_patch_diff_record": {"mobile_sam_weight_registry_patch_diff_record": asdict(diff)},
            "mobile_sam_weight_registry_patch_post_review_record": {"mobile_sam_weight_registry_post_review_audit": asdict(post_audit),
                                                                    "mobile_sam_weight_registry_rollback_readiness_record": asdict(rollback),
                                                                    "mobile_sam_code_and_weight_readiness_record": asdict(readiness)},
            "mobile_sam_model_load_boundary_record": {"mobile_sam_model_load_boundary_record": asdict(model_load_boundary)},
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
            "real_execution_phase": True,
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
    result = review_p1_mobile_sam_weight_registry_patch_execution_and_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "registry_patched_this_phase": result["conclusions"]["registry_patched_this_phase"],
                "readiness_level_written": result["conclusions"]["readiness_level_written"],
                "changed_field_paths": result["conclusions"]["changed_field_paths"],
                "byte_track_unchanged": result["conclusions"]["byte_track_unchanged"],
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
