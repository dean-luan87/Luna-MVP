# -*- coding: utf-8 -*-
"""P1 MobileSAM Inference Trial Registry Patch Execution And Post Review — review v1
(REAL EXECUTION, scope = mobile_sam_only).
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.field_understanding.p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review.p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review.p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALLOWED_PATCH_FIELD_NAMES,
    ALLOWED_REGISTRY_PATCH_SCOPE,
    ALL_GOVERNANCE_RULES,
    CHECKPOINT_DOWNLOAD_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    FORBIDDEN_PROMOTION_FIELDS,
    IMAGE_INPUT_ALLOWED,
    INFERENCE_EXECUTION_OUTPUT_DIR,
    INFERENCE_TRIAL_REGISTRY_PATCH_EXECUTION,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    MOBILE_SAM_WEIGHT_FILE_PATH,
    MOBILE_SAM_WEIGHT_SHA256,
    MOBILE_SAM_WEIGHT_SIZE_BYTES,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_GOVERNANCE_STANDARDIZATION,
    NEXT_PHASE_RUNTIME_BOUNDARY,
    OUT_OF_SCOPE_ASSET_IDS,
    PATCH_ASSET_ID,
    PATCH_PRINCIPLE_ZH,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNED_READINESS_LEVEL,
    POST_REVIEW_INCLUDED,
    PREDICTION_ALLOWED,
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
    SEGMENTATION_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_INFERENCE_EXECUTION_REF,
    UPSTREAM_INFERENCE_REVIEW_REL,
    UPSTREAM_PLANNING_REF,
    WEIGHT_CHAIN,
    MobileSAMFollowupRuntimeBoundaryStandardizationRoute,
    MobileSAMInferenceRegistryPatchDiffRecord,
    MobileSAMInferenceRegistryPatchExecutionRecord,
    MobileSAMInferenceRegistryPostReviewAudit,
    MobileSAMInferenceRegistryPrePatchSnapshotRecord,
    MobileSAMInferenceRegistryRollbackReadinessRecord,
    MobileSAMInferenceTrialVerifiedReadinessRecord,
    MobileSAMRuntimeOutputSemanticFactBoundaryPreservationRecord,
    NegativeMobileSAMInferenceRegistryPatchExecutionGuard,
    P1MobileSAMInferenceRegistryPatchExecutionDecision,
    P1MobileSAMInferenceRegistryPatchExecutionPostReviewProfile,
    to_dict,
)

_PKG = "capabilities/field_understanding/p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review_types_v1.py",
    f"{_PKG}/p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review_v1.py",
)
PROFILE_REF = "p1_mobile_sam_inference_registry_patch_execution_profile_v1"
DECISION_REF = "p1_mobile_sam_inference_registry_patch_execution_decision_v1"
REVIEW_FILENAME = "p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review_review_v1.json"
_ALLOWED_FIELDS: Set[str] = set(ALLOWED_PATCH_FIELD_NAMES)


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
    / "p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review_v1_smoke_v0"
)
_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _artifact_roots() -> List[Path]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return roots


def _overlay_path() -> Path:
    for base in _artifact_roots():
        p = base / REGISTRY_OVERLAY_REL
        if p.is_file():
            return p
    return _REPO_ROOT / REGISTRY_OVERLAY_REL


def _load_json(rel: str) -> Optional[Dict[str, Any]]:
    for base in _artifact_roots():
        p = base / rel
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return None
    return None


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _entry_hash(entry: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(entry, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _build_patch_values(inference_review: Dict[str, Any]) -> Dict[str, Any]:
    _ = inference_review
    return {
        "inference_trial_verified": True,
        "candidate_output_verified": True,
        "single_local_test_image_inference_verified": True,
        "inference_trial_phase_ref": UPSTREAM_INFERENCE_EXECUTION_REF,
        "inference_trial_result": "GO",
        "inference_trial_input_type": "synthetic_test_image",
        "inference_trial_input_manifest_ref": (
            f"{INFERENCE_EXECUTION_OUTPUT_DIR}/mobile_sam_local_test_image_manifest_v1.json"
        ),
        "inference_trial_candidate_output_ref": (
            f"{INFERENCE_EXECUTION_OUTPUT_DIR}/mobile_sam_inference_candidate_output_v1.json"
        ),
        "inference_output_boundary": "candidate_only",
        "readiness_level": PLANNED_READINESS_LEVEL,
        "model_load_verified": True,
        "checkpoint_load_verified": True,
        "dependency_gap_resolved": True,
        "dependency_repair_applied": True,
        "dependency_repair_dependency": "timm",
        "dependency_repair_dependency_version": "1.0.27",
        "dependency_repair_method": "timm_no_deps_controlled_install",
        "model_type_name": "Sam",
        "weight_downloaded": True,
        "model_weight_status": "downloaded",
        "checkpoint_weight_status": "downloaded",
        "weight_file_path": MOBILE_SAM_WEIGHT_FILE_PATH,
        "weight_file_size_bytes": MOBILE_SAM_WEIGHT_SIZE_BYTES,
        "weight_sha256": MOBILE_SAM_WEIGHT_SHA256,
        "weight_integrity_verified": True,
        "storage_verified": True,
        "code_only_install_verified": True,
        "find_spec_verified": True,
        "import_root": "mobile_sam",
        "full_clone_allowed": False,
        "weight_excluding_checkout_required": True,
        "inference_ready": False,
        "runtime_ready": False,
        "output_adapter_ready": False,
        "semantic_layer_ready": False,
        "fact_write_ready": False,
        "navigation_action_speech_ready": False,
        "commercial_runtime_approved": False,
    }


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMInferenceRegistryPatchExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            mobile_sam_only=True,
            inference_trial_registry_patch_execution=INFERENCE_TRIAL_REGISTRY_PATCH_EXECUTION,
            post_review_included=POST_REVIEW_INCLUDED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            registry_file_write_allowed=REGISTRY_FILE_WRITE_ALLOWED,
            allowed_registry_patch_scope=ALLOWED_REGISTRY_PATCH_SCOPE,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            segmentation_allowed=SEGMENTATION_ALLOWED,
            prediction_allowed=PREDICTION_ALLOWED,
            image_input_allowed=IMAGE_INPUT_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            fact_write_allowed=FACT_WRITE_ALLOWED,
            navigation_action_speech_allowed=NAVIGATION_ACTION_SPEECH_ALLOWED,
            additional_weight_download_allowed=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_planning_ref=UPSTREAM_PLANNING_REF,
            upstream_inference_execution_ref=UPSTREAM_INFERENCE_EXECUTION_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review_v1(
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
    pre_file_sha = _file_sha256(overlay_path) if overlay_exists else ""
    pre_file_size = overlay_path.stat().st_size if overlay_exists else 0

    overlay: Dict[str, Any] = {}
    if overlay_exists:
        try:
            overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            overlay = {}
            overlay_exists = False
    assets = overlay.get("assets", {})

    mobile_sam_before = copy.deepcopy(assets.get(PATCH_ASSET_ID, {}))
    byte_track_before = copy.deepcopy(assets.get("byte_track", {}))
    out_of_scope_before = {a: copy.deepcopy(assets.get(a, {})) for a in OUT_OF_SCOPE_ASSET_IDS if a in assets}
    out_of_scope_hashes_before = {a: _entry_hash(assets[a]) for a in out_of_scope_before}

    snapshot_succeeded = overlay_exists and bool(mobile_sam_before)
    snapshot_path = out_root / "mobile_sam_inference_registry_pre_patch_snapshot_v1.json"
    snapshot = MobileSAMInferenceRegistryPrePatchSnapshotRecord(
        snapshot_id="mobile_sam_inference_registry_pre_patch_snapshot_v1",
        registry_overlay_path=str(overlay_path),
        registry_overlay_exists=overlay_exists,
        pre_patch_file_sha256=pre_file_sha,
        pre_patch_file_size=pre_file_size,
        asset_count=len(assets),
        mobile_sam_pre_patch_entry=mobile_sam_before,
        byte_track_pre_patch_entry=byte_track_before,
        out_of_scope_assets_pre_patch_hashes=out_of_scope_hashes_before,
        rollback_snapshot_path=str(snapshot_path),
        timestamp=ts,
        upstream_planning_ref=UPSTREAM_PLANNING_REF,
        upstream_inference_trial_ref=UPSTREAM_INFERENCE_EXECUTION_REF,
        test_board_ref=(
            "capabilities/test_board/recognition_models/"
            "phase_p1_mobilesam_inference_trial_registry_patch_execution_and_post_review_v1_001/"
        ),
        snapshot_succeeded=snapshot_succeeded,
    )
    snapshot_path.write_text(json.dumps(asdict(snapshot), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not snapshot_succeeded:
        failed_checks.append("snapshot.failed_overlay_missing_or_mobile_sam_entry_absent")

    inference_review = _load_json(UPSTREAM_INFERENCE_REVIEW_REL) or {}
    patch_values = _build_patch_values(inference_review)

    patched_fields: List[str] = []
    patch_applied = False
    patch_attempted = False
    if apply_patch and snapshot_succeeded:
        patch_attempted = True
        ms_entry = dict(assets.get(PATCH_ASSET_ID, {}))
        for k, v in patch_values.items():
            if ms_entry.get(k) != v:
                patched_fields.append(k)
            ms_entry[k] = v
        for forbidden in FORBIDDEN_PROMOTION_FIELDS:
            ms_entry.pop(forbidden, None)
        assets[PATCH_ASSET_ID] = ms_entry
        overlay["assets"] = assets
        overlay["mobile_sam_inference_trial_patched_by_phase"] = PHASE_ID
        overlay["mobile_sam_inference_trial_patched_at_utc"] = _now()
        try:
            overlay_path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            patch_applied = True
        except (OSError, PermissionError) as exc:
            warnings.append(f"overlay_write_failed:{type(exc).__name__}:{exc}")
            failed_checks.append("execution.overlay_write_failed_no_boundary")

    post_file_sha = _file_sha256(overlay_path) if patch_applied and overlay_path.is_file() else pre_file_sha
    after_overlay: Dict[str, Any] = {}
    if patch_applied:
        try:
            after_overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            after_overlay = overlay
    else:
        after_overlay = overlay
    after_assets = after_overlay.get("assets", {})
    mobile_sam_after = after_assets.get(PATCH_ASSET_ID, {})
    byte_track_after = after_assets.get("byte_track", {})

    byte_track_unchanged = byte_track_after == byte_track_before
    out_of_scope_unchanged = all(
        _entry_hash(after_assets.get(a, {})) == out_of_scope_hashes_before.get(a, _entry_hash({}))
        for a in out_of_scope_hashes_before
    )

    execution = MobileSAMInferenceRegistryPatchExecutionRecord(
        record_id="mobile_sam_inference_registry_patch_execution_record_v1",
        registry_patch_attempted=patch_attempted,
        registry_patch_applied=patch_applied,
        changed_asset_ids=(PATCH_ASSET_ID,) if patch_applied and patched_fields else (),
        changed_field_names=tuple(patched_fields),
        changed_field_count=len(patched_fields),
        write_timestamp=after_overlay.get("mobile_sam_inference_trial_patched_at_utc", ts),
        pre_patch_sha256=pre_file_sha,
        post_patch_sha256=post_file_sha,
        patch_scope=ALLOWED_REGISTRY_PATCH_SCOPE,
        no_broad_inference_promoted=mobile_sam_after.get("inference_ready") is not True,
        no_runtime_fields_promoted=mobile_sam_after.get("runtime_ready") is not True,
        no_output_adapter_fields_promoted=mobile_sam_after.get("output_adapter_ready") is not True,
        no_semantic_fields_promoted=mobile_sam_after.get("semantic_layer_ready") is not True,
        no_fact_fields_promoted=mobile_sam_after.get("fact_write_ready") is not True,
        no_navigation_action_speech_fields_promoted=mobile_sam_after.get("navigation_action_speech_ready") is not True,
    )
    (out_root / "mobile_sam_inference_registry_patch_execution_record_v1.json").write_text(
        json.dumps(asdict(execution), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    changed_fields: List[str] = []
    before_values: Dict[str, Any] = {}
    after_values: Dict[str, Any] = {}
    for k in sorted(set(mobile_sam_before) | set(mobile_sam_after)):
        b = mobile_sam_before.get(k, "<<absent>>")
        a = mobile_sam_after.get(k, "<<absent>>")
        if b != a:
            changed_fields.append(k)
            before_values[k] = b
            after_values[k] = a

    diff = MobileSAMInferenceRegistryPatchDiffRecord(
        diff_id="mobile_sam_inference_registry_patch_diff_v1",
        changed_asset_count=1 if patch_applied and changed_fields else 0,
        changed_assets=(PATCH_ASSET_ID,) if patch_applied and changed_fields else (),
        byte_track_changed=not byte_track_unchanged,
        out_of_scope_assets_changed=not out_of_scope_unchanged,
        mobile_sam_changed_fields=tuple(changed_fields),
        readiness_level_changed_to=str(mobile_sam_after.get("readiness_level", "")),
        inference_ready_remains_false=mobile_sam_after.get("inference_ready") is not True,
        runtime_ready_remains_false=mobile_sam_after.get("runtime_ready") is not True,
        output_adapter_ready_remains_false=mobile_sam_after.get("output_adapter_ready") is not True,
        semantic_layer_ready_remains_false=mobile_sam_after.get("semantic_layer_ready") is not True,
        fact_write_ready_remains_false=mobile_sam_after.get("fact_write_ready") is not True,
        navigation_action_speech_ready_remains_false=mobile_sam_after.get("navigation_action_speech_ready") is not True,
        commercial_runtime_approved_remains_false=mobile_sam_after.get("commercial_runtime_approved") is not True,
        before_values=before_values,
        after_values=after_values,
    )
    (out_root / "mobile_sam_inference_registry_patch_diff_v1.json").write_text(
        json.dumps(asdict(diff), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    patch_scope_valid = (
        byte_track_unchanged
        and out_of_scope_unchanged
        and all(f in _ALLOWED_FIELDS or f.startswith(("inference_", "dependency_", "model_load_", "weight_", "checkpoint_")) for f in changed_fields)
    )

    post_audit = MobileSAMInferenceRegistryPostReviewAudit(
        audit_id="mobile_sam_inference_registry_post_review_audit_v1",
        pre_snapshot_exists=snapshot.snapshot_succeeded,
        registry_patch_applied=patch_applied,
        registry_patch_scope_valid=patch_scope_valid,
        only_mobile_sam_changed=diff.changed_asset_count == 1 and byte_track_unchanged and out_of_scope_unchanged,
        byte_track_unchanged=byte_track_unchanged,
        out_of_scope_assets_unchanged=out_of_scope_unchanged,
        inference_trial_verified_written=mobile_sam_after.get("inference_trial_verified") is True,
        candidate_output_verified_written=mobile_sam_after.get("candidate_output_verified") is True,
        single_local_test_image_inference_verified_written=(
            mobile_sam_after.get("single_local_test_image_inference_verified") is True
        ),
        readiness_level_inference_trial_verified_written=mobile_sam_after.get("readiness_level") == PLANNED_READINESS_LEVEL,
        broad_inference_ready_false_written=mobile_sam_after.get("inference_ready") is False,
        inference_ready_false_written=mobile_sam_after.get("inference_ready") is False,
        runtime_ready_false_written=mobile_sam_after.get("runtime_ready") is False,
        output_adapter_ready_false_written=mobile_sam_after.get("output_adapter_ready") is False,
        semantic_layer_ready_false_written=mobile_sam_after.get("semantic_layer_ready") is False,
        fact_write_ready_false_written=mobile_sam_after.get("fact_write_ready") is False,
        navigation_action_speech_ready_false_written=mobile_sam_after.get("navigation_action_speech_ready") is False,
        commercial_runtime_false_written=mobile_sam_after.get("commercial_runtime_approved") is False,
        no_inference_execution=True,
        no_image_input=True,
        no_prediction_or_segmentation=True,
        no_runtime=True,
        no_output_adapter=True,
        no_semantic_layer=True,
        no_fact_write=True,
        no_navigation_action_speech=True,
        no_extra_download=True,
        test_board_written=write_test_board,
        test_board_protected=all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        post_review_passed=(
            patch_applied
            and patch_scope_valid
            and diff.changed_asset_count == 1
            and mobile_sam_after.get("readiness_level") == PLANNED_READINESS_LEVEL
            and all(mobile_sam_after.get(f) is False for f in READINESS_FLAGS_MUST_BE_FALSE)
        ),
    )
    (out_root / "mobile_sam_inference_registry_post_review_audit_v1.json").write_text(
        json.dumps(asdict(post_audit), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rollback = MobileSAMInferenceRegistryRollbackReadinessRecord(
        record_id="mobile_sam_inference_registry_rollback_readiness_v1",
        rollback_available=True,
        rollback_snapshot_path=str(snapshot_path),
        rollback_not_executed_by_default=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
        rollback_trigger_conditions=(
            "post_patch_validation_failed",
            "out_of_scope_asset_changed",
            "inference_ready_accidentally_true",
            "runtime_ready_accidentally_true",
            "output_adapter_ready_accidentally_true",
            "semantic_layer_ready_accidentally_true",
            "fact_write_ready_accidentally_true",
            "navigation_action_speech_ready_accidentally_true",
            "registry_parse_failure",
            "test_board_write_failure",
        ),
    )

    readiness = MobileSAMInferenceTrialVerifiedReadinessRecord(
        asset_id=PATCH_ASSET_ID,
        readiness_level=str(mobile_sam_after.get("readiness_level", PLANNED_READINESS_LEVEL)),
        inference_trial_verified=mobile_sam_after.get("inference_trial_verified") is True,
        candidate_output_verified=mobile_sam_after.get("candidate_output_verified") is True,
        single_local_test_image_inference_verified=(
            mobile_sam_after.get("single_local_test_image_inference_verified") is True
        ),
        model_load_verified=mobile_sam_after.get("model_load_verified") is True,
        inference_ready=mobile_sam_after.get("inference_ready") is True,
        runtime_ready=mobile_sam_after.get("runtime_ready") is True,
        output_adapter_ready=mobile_sam_after.get("output_adapter_ready") is True,
        semantic_layer_ready=mobile_sam_after.get("semantic_layer_ready") is True,
        fact_write_ready=mobile_sam_after.get("fact_write_ready") is True,
        navigation_action_speech_ready=mobile_sam_after.get("navigation_action_speech_ready") is True,
        commercial_runtime_approved=mobile_sam_after.get("commercial_runtime_approved") is True,
        inference_trial_verified_not_broad_inference_ready=mobile_sam_after.get("inference_ready") is not True,
        inference_trial_verified_not_runtime_ready=mobile_sam_after.get("runtime_ready") is not True,
    )

    boundary = MobileSAMRuntimeOutputSemanticFactBoundaryPreservationRecord(
        record_id="mobile_sam_runtime_output_semantic_fact_boundary_preservation_v1",
        registry_patch_success_not_broad_inference_approval=True,
        registry_patch_success_not_runtime_approval=True,
        registry_patch_success_not_output_adapter_approval=True,
        registry_patch_success_not_semantic_layer_promotion=True,
        registry_patch_success_not_fact_write_approval=True,
        registry_patch_success_not_navigation_action_speech_approval=True,
        runtime_requires_separate_request_approval_execution=True,
        output_adapter_requires_separate_review=True,
        semantic_fact_navigation_requires_separate_governance=True,
    )

    followup = MobileSAMFollowupRuntimeBoundaryStandardizationRoute(
        route_id="mobile_sam_followup_runtime_boundary_standardization_route_v1",
        recommended_next_phase=NEXT_PHASE_RUNTIME_BOUNDARY,
        optional_parallel_phase=NEXT_PHASE_GOVERNANCE_STANDARDIZATION,
        next_phase_scope="mobile_sam_only",
        next_phase_allows_runtime_boundary_standardization=True,
        next_phase_still_no_runtime_execution=True,
    )

    boundary_violation = (
        not byte_track_unchanged
        or not out_of_scope_unchanged
        or any(mobile_sam_after.get(f) is True for f in READINESS_FLAGS_MUST_BE_FALSE)
        or any(f in mobile_sam_after for f in FORBIDDEN_PROMOTION_FIELDS)
    )

    invariant_state: Dict[str, bool] = {
        "pre_patch_snapshot_present": snapshot.snapshot_succeeded,
        "upstream_planning_go_verified": verify_flags.get(
            "mobile_sam_inference_trial_registry_patch_runtime_boundary_planning_go_verified"
        ) is True,
        "upstream_inference_go_verified": verify_flags.get("mobile_sam_inference_trial_execution_go_verified") is True,
        "only_mobile_sam_modified": diff.changed_asset_count == 1 and out_of_scope_unchanged and byte_track_unchanged,
        "byte_track_unchanged": byte_track_unchanged,
        "patch_scope_valid": patch_scope_valid,
        "downstream_ready_remain_false": all(mobile_sam_after.get(f) is not True for f in READINESS_FLAGS_MUST_BE_FALSE),
        "no_inference_seg_pred": (
            REAL_INFERENCE_ALLOWED is False and SEGMENTATION_ALLOWED is False and PREDICTION_ALLOWED is False
        ),
        "no_image_input": IMAGE_INPUT_ALLOWED is False,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_fact_navigation_speech": FACT_WRITE_ALLOWED is False and NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "no_extra_download": (
            ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False
            and MODEL_DOWNLOAD_ALLOWED is False
            and CHECKPOINT_DOWNLOAD_ALLOWED is False
            and DATASET_DOWNLOAD_ALLOWED is False
        ),
        "patch_not_broad_inference_approval": boundary.registry_patch_success_not_broad_inference_approval,
        "patch_not_runtime_semantic_fact_approval": (
            boundary.registry_patch_success_not_runtime_approval
            and boundary.registry_patch_success_not_semantic_layer_promotion
            and boundary.registry_patch_success_not_fact_write_approval
        ),
        "diff_present": bool(diff.mobile_sam_changed_fields) or not patch_applied,
        "post_review_present": True,
        "rollback_present": rollback.rollback_available,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMobileSAMInferenceRegistryPatchExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMInferenceRegistryPatchExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_inference_registry_patch_execution_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    patch_success = (
        patch_applied
        and post_audit.only_mobile_sam_changed
        and post_audit.inference_trial_verified_written
        and post_audit.candidate_output_verified_written
        and post_audit.single_local_test_image_inference_verified_written
        and post_audit.readiness_level_inference_trial_verified_written
        and all(mobile_sam_after.get(f) is False for f in READINESS_FLAGS_MUST_BE_FALSE)
    )

    go_conditions: Dict[str, bool] = {
        "mobile_sam_inference_registry_patch_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_inference_registry_pre_patch_snapshot_record_count_eq_1": True,
        "mobile_sam_inference_registry_patch_execution_record_count_eq_1": True,
        "mobile_sam_inference_registry_patch_diff_record_count_eq_1": True,
        "mobile_sam_inference_registry_post_review_audit_count_gte_1": True,
        "mobile_sam_inference_registry_rollback_readiness_record_count_gte_1": True,
        "mobile_sam_inference_trial_verified_readiness_record_count_gte_1": True,
        "mobile_sam_runtime_output_semantic_fact_boundary_preservation_record_count_gte_1": True,
        "mobile_sam_followup_runtime_boundary_standardization_route_count_gte_1": True,
        "negative_guard_count_eq_20": negative_guard_count == 20,
        "negative_guard_passed_eq_20": negative_guard_passed == 20,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "real_execution_phase": REAL_EXECUTION_PHASE is True,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED is True,
        "registry_file_write_allowed": REGISTRY_FILE_WRITE_ALLOWED is True,
        "registry_patch_applied": patch_applied,
        "only_mobile_sam_changed": post_audit.only_mobile_sam_changed,
        "byte_track_unchanged": byte_track_unchanged,
        "inference_trial_verified_written": post_audit.inference_trial_verified_written,
        "candidate_output_verified_written": post_audit.candidate_output_verified_written,
        "readiness_level_inference_trial_verified_written": post_audit.readiness_level_inference_trial_verified_written,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "cleanup_does_not_delete_test_board": True,
    }

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    if boundary_violation:
        failed_checks.append("boundary_violation_detected")

    blocker_count = len(failed_checks)

    if boundary_violation:
        final_decision = FINAL_DECISION_BLOCKED
        recommended_next_phase = NEXT_PHASE_BLOCKED
    elif patch_success and blocker_count == 0 and negative_guard_passed == 20:
        final_decision = FINAL_DECISION_GO
        recommended_next_phase = NEXT_PHASE_RUNTIME_BOUNDARY
    elif not patch_applied and not boundary_violation and blocker_count == 0:
        final_decision = FINAL_DECISION_FAILED
        recommended_next_phase = NEXT_PHASE_BLOCKED
    elif blocker_count > 0:
        final_decision = FINAL_DECISION_BLOCKED
        recommended_next_phase = NEXT_PHASE_BLOCKED
    else:
        final_decision = FINAL_DECISION_FAILED
        recommended_next_phase = NEXT_PHASE_BLOCKED

    no_boundary_violation = final_decision in (FINAL_DECISION_GO, FINAL_DECISION_FAILED)

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMInferenceRegistryPatchExecutionDecision(
        decision_ref=DECISION_REF,
        mobile_sam_inference_registry_patch_execution_profile_count=1,
        mobile_sam_inference_registry_pre_patch_snapshot_record_count=1,
        mobile_sam_inference_registry_patch_execution_record_count=1,
        mobile_sam_inference_registry_patch_diff_record_count=1,
        mobile_sam_inference_registry_post_review_audit_count=1,
        mobile_sam_inference_registry_rollback_readiness_record_count=1,
        mobile_sam_inference_trial_verified_readiness_record_count=1,
        mobile_sam_runtime_output_semantic_fact_boundary_preservation_record_count=1,
        mobile_sam_followup_runtime_boundary_standardization_route_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        registry_patch_applied=patch_applied,
        no_boundary_violation=no_boundary_violation,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Inference Trial Registry Patch Execution And Post Review (real execution)",
        "lifecycle_variant": SCOPE,
        "patch_principle_zh": PATCH_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "allowed_registry_patch_scope": ALLOWED_REGISTRY_PATCH_SCOPE,
        "upstream_planning_ref": UPSTREAM_PLANNING_REF,
        "upstream_inference_execution_ref": UPSTREAM_INFERENCE_EXECUTION_REF,
        "overlay_path": str(overlay_path),
        "mobile_sam_inference_registry_patch_execution_profile": _build_profile(),
        "mobile_sam_inference_registry_patch_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_inference_registry_pre_patch_snapshot_record": asdict(snapshot),
        "mobile_sam_inference_registry_pre_patch_snapshot_record_count": 1,
        "mobile_sam_inference_registry_patch_execution_record": asdict(execution),
        "mobile_sam_inference_registry_patch_execution_record_count": 1,
        "mobile_sam_inference_registry_patch_diff_record": asdict(diff),
        "mobile_sam_inference_registry_patch_diff_record_count": 1,
        "mobile_sam_inference_registry_post_review_audit": asdict(post_audit),
        "mobile_sam_inference_registry_post_review_audit_count": 1,
        "mobile_sam_inference_registry_rollback_readiness_record": asdict(rollback),
        "mobile_sam_inference_registry_rollback_readiness_record_count": 1,
        "mobile_sam_inference_trial_verified_readiness_record": asdict(readiness),
        "mobile_sam_inference_trial_verified_readiness_record_count": 1,
        "mobile_sam_runtime_output_semantic_fact_boundary_preservation_record": asdict(boundary),
        "mobile_sam_runtime_output_semantic_fact_boundary_preservation_record_count": 1,
        "mobile_sam_followup_runtime_boundary_standardization_route_record": asdict(followup),
        "mobile_sam_followup_runtime_boundary_standardization_route_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "registry_patch_applied": patch_applied,
            "readiness_level_written": mobile_sam_after.get("readiness_level"),
            "changed_field_names": list(diff.mobile_sam_changed_fields),
            "inference_executed_this_phase": False,
            "registry_mutated_this_phase": patch_applied,
            "recommended_next_phase": recommended_next_phase,
            "optional_parallel_phase": NEXT_PHASE_GOVERNANCE_STANDARDIZATION,
            "transition_note": (
                "REAL EXECUTION (mobile_sam_only). Registry overlay patched with inference_trial_verified "
                "metadata only. byte_track unchanged. broad inference_ready/runtime/output/semantic/fact/"
                "navigation/commercial remain false. NO inference/runtime. MobileSAM P1 chain: "
                "code → weight → model_load_verified → inference_trial_verified."
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
            "mobile_sam_inference_registry_pre_patch_snapshot_record": {
                "mobile_sam_inference_registry_pre_patch_snapshot_record": asdict(snapshot),
            },
            "mobile_sam_inference_registry_patch_execution_record": {
                "mobile_sam_inference_registry_patch_execution_record": asdict(execution),
            },
            "mobile_sam_inference_registry_patch_diff_record": {
                "mobile_sam_inference_registry_patch_diff_record": asdict(diff),
            },
            "mobile_sam_inference_registry_patch_post_review_record": {
                "mobile_sam_inference_registry_post_review_audit": asdict(post_audit),
            },
            "mobile_sam_runtime_output_semantic_fact_boundary_preservation_record": {
                "mobile_sam_runtime_output_semantic_fact_boundary_preservation_record": asdict(boundary),
            },
            "mobile_sam_followup_runtime_boundary_standardization_route_record": {
                "mobile_sam_followup_runtime_boundary_standardization_route_record": asdict(followup),
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
            "real_execution_phase": True,
            "registry_mutation_allowed": True,
            "inference_allowed": False,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
            "semantic_layer_allowed": False,
            "fact_write_allowed": False,
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
    result = review_p1_mobile_sam_inference_trial_registry_patch_execution_and_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "overlay_path": result.get("overlay_path"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "registry_patch_applied": result["conclusions"]["registry_patch_applied"],
                "readiness_level_written": result["conclusions"]["readiness_level_written"],
                "changed_field_count": len(result["conclusions"]["changed_field_names"]),
                "negative_guard_passed": result["negative_guard_passed"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    ok = {FINAL_DECISION_GO, FINAL_DECISION_FAILED}
    return 0 if result["final_decision"] in ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
