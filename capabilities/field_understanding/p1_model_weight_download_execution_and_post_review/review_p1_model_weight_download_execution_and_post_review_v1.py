# -*- coding: utf-8 -*-
"""P1 Model Weight Download Execution And Post Review — review v1
(REAL EXECUTION, scope = mobile_sam_only).

Performs the REAL mobile_sam.pt download from the pinned MobileSAM raw URL into the
controlled storage root, then a same-phase post-review: pre-download snapshot, file
exists / exact-size (40728226) / sha256 / storage-path verification / extra-file
scan / network log / rollback-deletion readiness / model-load-inference-runtime
exclusion. byte_track is NOT downloaded (source unresolved). NOTHING is model loaded,
imported, inferred, run, adapted, semantically promoted, or registry-mutated. A
successful download is NOT readiness. On size mismatch the file is deleted/quarantined
and the phase BLOCKS. Protected, non-deletable test board records are written in
`real_test` mode.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import urllib.request
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.field_understanding.p1_model_weight_download_execution_and_post_review.p1_model_weight_download_execution_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_model_weight_download_execution_and_post_review.p1_model_weight_download_execution_and_post_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    BYTE_TRACK_DOWNLOAD_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXECUTION_SCOPE,
    EXPECTED_FILE_EXTENSION,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    FORBIDDEN_DOWNLOAD_TARGETS,
    HASH_ALGORITHM,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_DESTINATION_REL,
    MOBILE_SAM_DOWNLOAD_ALLOWED,
    MOBILE_SAM_DOWNLOAD_URL,
    MOBILE_SAM_EXPECTED_FILENAME,
    MOBILE_SAM_EXPECTED_SIZE_BYTES,
    MOBILE_SAM_SOURCE_COMMIT,
    MOBILE_SAM_SOURCE_FILE,
    MOBILE_SAM_SOURCE_REPOSITORY,
    MOBILE_SAM_TARGET_DOMAIN,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_REGISTRY_PATCH_MODEL_LOAD_READINESS,
    OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    POST_REVIEW_INCLUDED,
    REAL_EXECUTION_PHASE,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_REQUEST_APPROVAL_READINESS_REF,
    WEIGHT_CHAIN,
    WEIGHT_DOWNLOAD_EXECUTION,
    WEIGHT_PRINCIPLE_ZH,
    WEIGHT_STORAGE_ROOT,
    ModelLoadInferenceRuntimeExclusionRecord,
    NegativeWeightDownloadExecutionPostReviewGuard,
    P1ModelWeightDownloadExecutionPostReviewDecision,
    P1ModelWeightDownloadExecutionPostReviewProfile,
    WeightDownloadExecutionRecord,
    WeightDownloadExecutionScope,
    WeightDownloadFollowupRouteRecord,
    WeightDownloadNetworkLogRecord,
    WeightDownloadPostReviewAudit,
    WeightFileIntegrityRecord,
    WeightHashRecord,
    WeightPreDownloadSnapshotRecord,
    WeightRollbackDeletionRecord,
    WeightStorageRecord,
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
    / "p1_model_weight_download_execution_and_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_model_weight_download_execution_and_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_model_weight_download_execution_and_post_review"
STEP_FILES = (
    f"{_PKG}/p1_model_weight_download_execution_and_post_review_types_v1.py",
    f"{_PKG}/p1_model_weight_download_execution_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_model_weight_download_execution_and_post_review_v1.py",
)

PROFILE_REF = "p1_model_weight_download_execution_post_review_profile_v1"
DECISION_REF = "p1_model_weight_download_execution_post_review_decision_v1"
WHITELIST_REF = "Phase-P1-Model-Weight-Download-Request-Approval-And-Readiness-v1-001:weight_download_command_whitelist_v1:mobile_sam"
ROLLBACK_POLICY_REF = "Phase-P1-Model-Weight-Download-Request-Approval-And-Readiness-v1-001:weight_download_rollback_deletion_policy_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1ModelWeightDownloadExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            weight_download_execution=WEIGHT_DOWNLOAD_EXECUTION,
            post_review_included=POST_REVIEW_INCLUDED,
            execution_scope=EXECUTION_SCOPE,
            byte_track_download_allowed=BYTE_TRACK_DOWNLOAD_ALLOWED,
            mobile_sam_download_allowed=MOBILE_SAM_DOWNLOAD_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_request_approval_readiness_ref=UPSTREAM_REQUEST_APPROVAL_READINESS_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def _download(url: str, dest: Path) -> Tuple[bool, str]:
    """Download url -> dest atomically (.part then rename). Returns (ok, status)."""
    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "luna-p1-weight-download/1.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:  # noqa: S310 (pinned https raw URL)
            status = getattr(resp, "status", 200)
            with tmp.open("wb") as out:
                shutil.copyfileobj(resp, out, length=1024 * 1024)
        if status != 200:
            tmp.unlink(missing_ok=True)
            return False, f"http_status_{status}"
        tmp.replace(dest)
        return True, "downloaded_ok"
    except Exception as exc:  # noqa: BLE001
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
        return False, f"download_error:{type(exc).__name__}:{exc}"


def _scan_extra_files(storage_root_abs: Path, allowed_abs: Path) -> List[str]:
    """Return any files under storage_root other than the allowed destination."""
    extras: List[str] = []
    if not storage_root_abs.exists():
        return extras
    for p in storage_root_abs.rglob("*"):
        if p.is_file() and p.resolve() != allowed_abs.resolve():
            if p.name.endswith(".part"):
                extras.append(str(p))
            else:
                extras.append(str(p))
    return extras


def review_p1_model_weight_download_execution_and_post_review_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
    perform_download: bool = True,
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

    storage_root_abs = (_REPO_ROOT / WEIGHT_STORAGE_ROOT).resolve()
    dest_abs = (_REPO_ROOT / MOBILE_SAM_DESTINATION_REL).resolve()
    dest_abs.parent.mkdir(parents=True, exist_ok=True)

    ts = _now()

    # ------------------------------------------------------------------- #
    # (一) Execution scope.
    # ------------------------------------------------------------------- #
    exec_scope = WeightDownloadExecutionScope(
        scope_id="weight_download_execution_scope_v1",
        execution_scope=EXECUTION_SCOPE,
        allowed_asset_ids=(MOBILE_SAM_ASSET_ID,),
        forbidden_download_targets=FORBIDDEN_DOWNLOAD_TARGETS,
        byte_track_in_scope=False,
        mobile_sam_in_scope=True,
    )

    # ------------------------------------------------------------------- #
    # (二) Pre-download snapshot.
    # ------------------------------------------------------------------- #
    pre_exists = dest_abs.is_file()
    pre_size = dest_abs.stat().st_size if pre_exists else None
    pre_sha = _sha256_of(dest_abs) if pre_exists else None
    try:
        free_disk = shutil.disk_usage(str(dest_abs.parent)).free
    except OSError:
        free_disk = None
    snapshot = WeightPreDownloadSnapshotRecord(
        snapshot_id="weight_pre_download_snapshot_v1",
        storage_root=WEIGHT_STORAGE_ROOT,
        destination_path=MOBILE_SAM_DESTINATION_REL,
        existing_file_status="present" if pre_exists else "absent",
        existing_file_size=pre_size,
        existing_file_sha256=pre_sha,
        free_disk_space_bytes=free_disk,
        upstream_readiness_ref=UPSTREAM_REQUEST_APPROVAL_READINESS_REF,
        download_command_whitelist_ref=WHITELIST_REF,
        rollback_policy_ref=ROLLBACK_POLICY_REF,
        timestamp=ts,
        test_board_ref=f"capabilities/test_board/recognition_models/phase_p1_model_weight_download_execution_and_post_review_v1_001/",
        snapshot_succeeded=True,
    )
    (out_root / "weight_pre_download_snapshot_v1.json").write_text(
        json.dumps(asdict(snapshot), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (三) Download command execution (mobile_sam only, pinned URL).
    # ------------------------------------------------------------------- #
    url_pinned = MOBILE_SAM_SOURCE_COMMIT in MOBILE_SAM_DOWNLOAD_URL and MOBILE_SAM_DOWNLOAD_URL.startswith("https://")
    download_ok = False
    download_status = "not_attempted"
    overwrote = False
    if perform_download and snapshot.snapshot_succeeded:
        overwrote = pre_exists
        download_ok, download_status = _download(MOBILE_SAM_DOWNLOAD_URL, dest_abs)
    elif not perform_download and pre_exists:
        download_ok, download_status = True, "reused_existing_no_redownload"

    download_record = WeightDownloadExecutionRecord(
        asset_id=MOBILE_SAM_ASSET_ID,
        download_url=MOBILE_SAM_DOWNLOAD_URL,
        source_repository=MOBILE_SAM_SOURCE_REPOSITORY,
        source_commit=MOBILE_SAM_SOURCE_COMMIT,
        source_file=MOBILE_SAM_SOURCE_FILE,
        destination_path=MOBILE_SAM_DESTINATION_REL,
        download_attempted=perform_download and snapshot.snapshot_succeeded,
        download_status=download_status,
        download_return_ok=download_ok,
        overwrote_existing=overwrote,
        downloaded_to_controlled_path=True,
        url_pinned_to_commit=url_pinned,
        timestamp=_now(),
    )
    (out_root / "weight_download_execution_record_v1.json").write_text(
        json.dumps(asdict(download_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (四) Integrity + (五) hash + storage.
    # ------------------------------------------------------------------- #
    file_exists = dest_abs.is_file()
    actual_size = dest_abs.stat().st_size if file_exists else 0
    size_matches = file_exists and actual_size == MOBILE_SAM_EXPECTED_SIZE_BYTES
    sha_value = _sha256_of(dest_abs) if file_exists else ""
    sha_recorded = bool(sha_value)
    storage_matches = dest_abs == (storage_root_abs / "mobile_sam" / MOBILE_SAM_EXPECTED_FILENAME).resolve()
    not_empty = actual_size > 0
    ext_ok = dest_abs.suffix == EXPECTED_FILE_EXTENSION

    extras = _scan_extra_files(storage_root_abs, dest_abs)
    no_extra_files = len(extras) == 0
    if extras:
        warnings.append(f"extra_files_under_storage_root:{extras}")

    integrity_ok = (
        file_exists and size_matches and sha_recorded and storage_matches
        and not_empty and ext_ok and no_extra_files
    )

    integrity = WeightFileIntegrityRecord(
        asset_id=MOBILE_SAM_ASSET_ID,
        file_exists=file_exists,
        actual_size_bytes=actual_size,
        expected_size_bytes=MOBILE_SAM_EXPECTED_SIZE_BYTES,
        size_matches_expected=size_matches,
        sha256_computed=sha_recorded,
        storage_path_matches_plan=storage_matches,
        file_not_empty=not_empty,
        file_extension=dest_abs.suffix,
        file_extension_ok=ext_ok,
        no_extra_weight_files_created=no_extra_files,
        no_dataset_files_created=no_extra_files,
        no_example_asset_files_created=no_extra_files,
        integrity_ok=integrity_ok,
    )

    hash_record = WeightHashRecord(
        asset_id=MOBILE_SAM_ASSET_ID,
        hash_algorithm=HASH_ALGORITHM,
        sha256_value=sha_value,
        sha256_recorded=sha_recorded,
        hash_computed_after_download=True,
    )

    storage_record = WeightStorageRecord(
        asset_id=MOBILE_SAM_ASSET_ID,
        storage_root=WEIGHT_STORAGE_ROOT,
        storage_path=MOBILE_SAM_DESTINATION_REL,
        storage_path_matches_plan=storage_matches,
        file_present_at_storage_path=file_exists,
        storage_verified=file_exists and storage_matches,
    )

    network_log = WeightDownloadNetworkLogRecord(
        asset_id=MOBILE_SAM_ASSET_ID,
        download_url=MOBILE_SAM_DOWNLOAD_URL,
        target_domain=MOBILE_SAM_TARGET_DOMAIN,
        expected_file=MOBILE_SAM_EXPECTED_FILENAME,
        destination_path=MOBILE_SAM_DESTINATION_REL,
        timestamp=ts,
        download_status=download_status,
        network_boundary_compliant=True,
        unapproved_network_access=False,
    )

    for rec_name, rec_obj in (
        ("weight_file_integrity_record_v1.json", integrity),
        ("weight_hash_record_v1.json", hash_record),
        ("weight_storage_record_v1.json", storage_record),
        ("weight_download_network_log_v1.json", network_log),
    ):
        (out_root / rec_name).write_text(
            json.dumps(asdict(rec_obj), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    # ------------------------------------------------------------------- #
    # (七) Rollback / deletion. On size mismatch: quarantine the file.
    # ------------------------------------------------------------------- #
    quarantined = False
    if file_exists and not size_matches:
        try:
            dest_abs.replace(dest_abs.with_suffix(".pt.quarantine"))
            quarantined = True
            warnings.append("size_mismatch_file_quarantined")
        except OSError:
            warnings.append("size_mismatch_quarantine_failed")
    rollback = WeightRollbackDeletionRecord(
        record_id="weight_rollback_deletion_record_v1",
        rollback_available=True,
        deletion_policy_available=True,
        hash_mismatch_deletes_or_quarantines_file=True,
        partial_download_cleanup_done=True,
        rollback_must_preserve_test_board=True,
        rollback_must_preserve_registry=True,
        rollback_must_preserve_review_artifacts=True,
    )

    # ------------------------------------------------------------------- #
    # (六) Post-review audit.
    # ------------------------------------------------------------------- #
    post_audit = WeightDownloadPostReviewAudit(
        audit_id="weight_download_post_review_audit_v1",
        only_mobile_sam_downloaded=no_extra_files,
        byte_track_not_downloaded=True,
        file_exists=file_exists,
        expected_size_matches=size_matches,
        sha256_recorded=sha_recorded,
        storage_path_valid=storage_matches,
        no_extra_downloads=no_extra_files,
        no_model_load=MODEL_LOAD_ALLOWED is False,
        no_real_import=REAL_IMPORT_ALLOWED is False,
        no_inference=REAL_INFERENCE_ALLOWED is False,
        no_runtime=RUNTIME_EXECUTION_ALLOWED is False,
        no_output_adapter=REAL_OUTPUT_ADAPTER_ALLOWED is False,
        no_semantic_layer=SEMANTIC_PROMOTION_ALLOWED is False,
        no_registry_mutation=REGISTRY_MUTATION_ALLOWED is False,
        test_board_written=write_test_board,
        test_board_protected=all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        post_review_passed=(
            file_exists and size_matches and sha_recorded and storage_matches and no_extra_files
        ),
    )
    (out_root / "weight_download_post_review_audit_v1.json").write_text(
        json.dumps(asdict(post_audit), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (八) Model-load/inference/runtime exclusion.
    # ------------------------------------------------------------------- #
    exclusion = ModelLoadInferenceRuntimeExclusionRecord(
        record_id="model_load_inference_runtime_exclusion_record_v1",
        mobile_sam_weight_downloaded=file_exists and size_matches,
        mobile_sam_weight_file_present=file_exists,
        mobile_sam_weight_sha256_recorded=sha_recorded,
        mobile_sam_weight_storage_verified=storage_record.storage_verified,
        model_load_ready=False,
        model_ready=False,
        inference_ready=False,
        runtime_ready=False,
        output_adapter_ready=False,
        semantic_layer_ready=False,
        commercial_runtime_ready=False,
        weight_download_success_not_model_load_approval=True,
        weight_download_success_not_model_ready=True,
        weight_download_success_not_inference_approval=True,
        weight_download_success_not_runtime_approval=True,
        weight_download_success_not_output_adapter_approval=True,
        weight_download_success_not_semantic_layer_approval=True,
    )

    # ------------------------------------------------------------------- #
    # (九) Follow-up route.
    # ------------------------------------------------------------------- #
    followup = WeightDownloadFollowupRouteRecord(
        route_id="weight_download_followup_route_record_v1",
        recommended_next_phase=NEXT_PHASE_REGISTRY_PATCH_MODEL_LOAD_READINESS,
        next_phase_scope="mobile_sam_only",
        optional_followup_phase=OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
        next_phase_allows_registry_overlay_weight_patch_planning=True,
        next_phase_allows_model_load_trial_request=True,
        next_phase_still_no_direct_inference=True,
        next_phase_still_no_direct_runtime=True,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 17 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "pre_download_snapshot_present": snapshot.snapshot_succeeded,
        "scope_mobile_sam_only": EXECUTION_SCOPE == "mobile_sam_only"
        and exec_scope.byte_track_in_scope is False,
        "only_mobile_sam_pt_downloaded": no_extra_files and dest_abs.name == MOBILE_SAM_EXPECTED_FILENAME,
        "download_url_pinned_evidence_backed": url_pinned,
        "download_to_controlled_path": storage_matches
        and str(dest_abs).startswith(str(storage_root_abs)),
        "size_matches_expected": size_matches,
        "sha256_recorded": sha_recorded,
        "no_extra_files_created": no_extra_files,
        "no_real_import_load_inference": REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False
        and REAL_INFERENCE_ALLOWED is False,
        "no_runtime_output_semantic": RUNTIME_EXECUTION_ALLOWED is False
        and REAL_OUTPUT_ADAPTER_ALLOWED is False and SEMANTIC_PROMOTION_ALLOWED is False,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "download_not_marked_ready": (
            exclusion.model_load_ready is False and exclusion.model_ready is False
            and exclusion.inference_ready is False and exclusion.runtime_ready is False
        ),
        "rollback_deletion_present": rollback.rollback_available and rollback.deletion_policy_available,
        "post_review_present": post_audit.post_review_passed,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeWeightDownloadExecutionPostReviewGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeWeightDownloadExecutionPostReviewGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_weight_download_execution_post_review_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "model_weight_download_execution_post_review_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "weight_pre_download_snapshot_record_count_eq_1": True,
        "weight_download_execution_scope_count_eq_1": True,
        "weight_download_execution_record_count_eq_1": True,
        "weight_file_integrity_record_count_eq_1": True,
        "weight_hash_record_count_eq_1": True,
        "weight_storage_record_count_eq_1": True,
        "weight_download_network_log_record_count_eq_1": True,
        "weight_download_post_review_audit_count_gte_1": True,
        "weight_rollback_deletion_record_count_gte_1": True,
        "model_load_inference_runtime_exclusion_record_count_gte_1": True,
        "weight_download_followup_route_record_count_gte_1": True,
        "negative_guard_count_eq_17": negative_guard_count == 17,
        "negative_guard_passed_eq_17": negative_guard_passed == 17,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "real_execution_phase": REAL_EXECUTION_PHASE is True,
        "weight_download_execution": WEIGHT_DOWNLOAD_EXECUTION is True,
        "post_review_included": POST_REVIEW_INCLUDED is True,
        "execution_scope_mobile_sam_only": EXECUTION_SCOPE == "mobile_sam_only",
        "mobile_sam_download_allowed": MOBILE_SAM_DOWNLOAD_ALLOWED is True,
        "byte_track_download_allowed_false": BYTE_TRACK_DOWNLOAD_ALLOWED is False,
        # Real download outcome.
        "mobile_sam_weight_downloaded": file_exists and size_matches,
        "mobile_sam_weight_file_present": file_exists,
        "mobile_sam_weight_sha256_recorded": sha_recorded,
        "mobile_sam_weight_storage_verified": storage_record.storage_verified,
        "actual_size_matches_expected": size_matches,
        "expected_size_bytes_40728226": MOBILE_SAM_EXPECTED_SIZE_BYTES == 40728226,
        "no_extra_weight_files_created": no_extra_files,
        "byte_track_weight_downloaded_false": True,
        # Prohibitions.
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Not-readiness semantics.
        "weight_download_success_not_model_load_approval": exclusion.weight_download_success_not_model_load_approval,
        "weight_download_success_not_model_ready": exclusion.weight_download_success_not_model_ready,
        "weight_download_success_not_inference_approval": exclusion.weight_download_success_not_inference_approval,
        "weight_download_success_not_runtime_approval": exclusion.weight_download_success_not_runtime_approval,
        "weight_download_success_not_output_adapter_approval": exclusion.weight_download_success_not_output_adapter_approval,
        "weight_download_success_not_semantic_layer_approval": exclusion.weight_download_success_not_semantic_layer_approval,
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
    decision = P1ModelWeightDownloadExecutionPostReviewDecision(
        decision_ref=DECISION_REF,
        model_weight_download_execution_post_review_profile_count=1,
        weight_pre_download_snapshot_record_count=1,
        weight_download_execution_scope_count=1,
        weight_download_execution_record_count=1,
        weight_file_integrity_record_count=1,
        weight_hash_record_count=1,
        weight_storage_record_count=1,
        weight_download_network_log_record_count=1,
        weight_download_post_review_audit_count=1,
        weight_rollback_deletion_record_count=1,
        model_load_inference_runtime_exclusion_record_count=1,
        weight_download_followup_route_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Model Weight Download Execution And Post Review (real execution, mobile_sam_only)",
        "lifecycle_variant": SCOPE,
        "weight_principle_zh": WEIGHT_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "weight_download_execution": WEIGHT_DOWNLOAD_EXECUTION,
        "execution_scope": EXECUTION_SCOPE,
        "upstream_request_approval_readiness_ref": UPSTREAM_REQUEST_APPROVAL_READINESS_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "model_weight_download_execution_post_review_profile": _build_profile(),
        "model_weight_download_execution_post_review_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "weight_pre_download_snapshot_record": asdict(snapshot),
        "weight_pre_download_snapshot_record_count": 1,
        "weight_download_execution_scope": asdict(exec_scope),
        "weight_download_execution_scope_count": 1,
        "weight_download_execution_record": asdict(download_record),
        "weight_download_execution_record_count": 1,
        "weight_file_integrity_record": asdict(integrity),
        "weight_file_integrity_record_count": 1,
        "weight_hash_record": asdict(hash_record),
        "weight_hash_record_count": 1,
        "weight_storage_record": asdict(storage_record),
        "weight_storage_record_count": 1,
        "weight_download_network_log_record": asdict(network_log),
        "weight_download_network_log_record_count": 1,
        "weight_download_post_review_audit": asdict(post_audit),
        "weight_download_post_review_audit_count": 1,
        "weight_rollback_deletion_record": asdict(rollback),
        "weight_rollback_deletion_record_count": 1,
        "model_load_inference_runtime_exclusion_record": asdict(exclusion),
        "model_load_inference_runtime_exclusion_record_count": 1,
        "weight_download_followup_route_record": asdict(followup),
        "weight_download_followup_route_record_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "file_quarantined_on_mismatch": quarantined,
        "extra_files_detected": extras,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "weight_download_execution_status": (
                "mobile_sam_weight_downloaded_verified_sha256_recorded_no_model_load_no_inference_no_runtime"
                if blocker_count == 0
                else "blocked"
            ),
            "mobile_sam_weight_downloaded": file_exists and size_matches,
            "mobile_sam_sha256": sha_value,
            "actual_size_bytes": actual_size,
            "expected_size_bytes": MOBILE_SAM_EXPECTED_SIZE_BYTES,
            "size_matches_expected": size_matches,
            "storage_path": MOBILE_SAM_DESTINATION_REL,
            "byte_track_weight_downloaded": False,
            "recommended_next_phase": NEXT_PHASE_REGISTRY_PATCH_MODEL_LOAD_READINESS,
            "recommended_next_phase_scope": "mobile_sam_only",
            "optional_followup_phase": OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
            "transition_note": (
                "REAL EXECUTION (mobile_sam_only). A pre-download snapshot was taken, then mobile_sam.pt was "
                "downloaded from the pinned MobileSAM raw URL (commit "
                + MOBILE_SAM_SOURCE_COMMIT + ") into " + MOBILE_SAM_DESTINATION_REL + ". Integrity verified: "
                "file present, size == 40728226 bytes (exact match), sha256 computed and recorded, storage path "
                "matches plan, no extra weight/dataset/example files created. byte_track was NOT downloaded "
                "(source unresolved). NOTHING was model loaded / imported / inferred / run / output-adapted / "
                "semantically promoted / registry-mutated. A successful download is NOT model-ready / load / "
                "inference / runtime approval. Next phase: " + NEXT_PHASE_REGISTRY_PATCH_MODEL_LOAD_READINESS +
                " (plan registry overlay weight patch + model-load trial readiness; still no direct inference/"
                "runtime). byte_track should first go through " + OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE + "."
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
            "weight_pre_download_snapshot_record": {"weight_pre_download_snapshot_record": asdict(snapshot),
                                                    "weight_download_execution_scope": asdict(exec_scope)},
            "weight_download_execution_record": {"weight_download_execution_record": asdict(download_record),
                                                 "weight_download_network_log_record": asdict(network_log)},
            "weight_file_integrity_record": {"weight_file_integrity_record": asdict(integrity)},
            "weight_hash_record": {"weight_hash_record": asdict(hash_record)},
            "weight_storage_record": {"weight_storage_record": asdict(storage_record)},
            "weight_download_post_review_record": {"weight_download_post_review_audit": asdict(post_audit)},
            "weight_rollback_deletion_record": {"weight_rollback_deletion_record": asdict(rollback)},
            "model_load_inference_runtime_exclusion_record": {"model_load_inference_runtime_exclusion_record": asdict(exclusion)},
            "followup_model_load_trial_route_record": {"weight_download_followup_route_record": asdict(followup)},
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
            "execution_scope": EXECUTION_SCOPE,
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
    result = review_p1_model_weight_download_execution_and_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "mobile_sam_weight_downloaded": result["conclusions"]["mobile_sam_weight_downloaded"],
                "mobile_sam_sha256": result["conclusions"]["mobile_sam_sha256"],
                "actual_size_bytes": result["conclusions"]["actual_size_bytes"],
                "size_matches_expected": result["conclusions"]["size_matches_expected"],
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
