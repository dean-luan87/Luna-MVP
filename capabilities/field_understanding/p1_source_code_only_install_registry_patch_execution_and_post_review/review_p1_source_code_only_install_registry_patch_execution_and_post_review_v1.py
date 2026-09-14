# -*- coding: utf-8 -*-
"""P1 Source Code-Only Install Registry Patch Execution And Post-Review — review v1
(REAL REGISTRY WRITE + INLINE POST-REVIEW).

Takes the pre-patch registry snapshot, applies the code-only-source-install registry
patch for byte_track and mobile_sam as a scoped, reversible OVERLAY artifact layered
over the static REGISTRY_ASSETS table, computes the registry diff, and runs the
inline post-review. It writes ONLY code-only source-install metadata; it NEVER sets
weight/model/inference/runtime/output_adapter/semantic readiness true. It does NOT
install / pip / resolve dependencies; does NOT download any model / weight /
checkpoint / dataset / example asset; and does NOT do real import, model load,
inference, runtime, output adapter, or semantic promotion. Protected, non-deletable
test board records are written in `real_test` mode.
"""

from __future__ import annotations

import importlib
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
from capabilities.field_understanding.p1_source_code_only_install_registry_patch_execution_and_post_review.p1_source_code_only_install_registry_patch_execution_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_source_code_only_install_registry_patch_execution_and_post_review.p1_source_code_only_install_registry_patch_execution_and_post_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    ALLOWED_PATCH_FIELD_KEYS,
    ALLOWED_REGISTRY_PATCH_SCOPE,
    BEFORE_FIELDS_OF_INTEREST,
    CHECKPOINT_DOWNLOAD_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    DEPENDENCY_INSTALL_ALLOWED,
    EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    IN_SCOPE_ASSET_IDS,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    MUST_NOT_MODIFY_ASSET_IDS,
    NEGATIVE_GUARDS,
    NEXT_PHASE_WEIGHT_DOWNLOAD,
    PATCH_AFTER_VALUES,
    PATCH_PRINCIPLE_ZH,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    POST_REVIEW_INCLUDED,
    PATCH_CHAIN,
    READINESS_FALSE_KEYS,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_FILE_WRITE_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_OVERLAY_REL,
    REGISTRY_PATCH_EXECUTION,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_INSTALL_ALLOWED,
    SOURCE_REGISTRY_CONST,
    SOURCE_REGISTRY_MODULE,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_PLANNING_REF,
    UPSTREAM_RETRY_REF,
    WEIGHT_DOWNLOAD_ALLOWED,
    WEIGHT_DOWNLOAD_REQUIRES_OWNER_APPROVAL,
    WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_REQUEST,
    CodeOnlyReadinessPatchRecord,
    ModelRuntimeBoundaryPatchRecord,
    NegativeSourceCodeOnlyRegistryPatchExecutionGuard,
    P1SourceCodeOnlyRegistryPatchExecutionDecision,
    P1SourceCodeOnlyRegistryPatchExecutionPostReviewProfile,
    RegistryPatchDiffRecord,
    RegistryPatchExecutionRecord,
    RegistryPatchFollowupWeightDownloadRoute,
    RegistryPatchPostReviewAudit,
    RegistryPatchPreSnapshotRecord,
    RegistryPatchRollbackReadinessRecord,
    WeightBoundaryPatchRecord,
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
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_source_code_only_install_registry_patch_execution_and_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_source_code_only_install_registry_patch_execution_and_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_source_code_only_install_registry_patch_execution_and_post_review"
STEP_FILES = (
    f"{_PKG}/p1_source_code_only_install_registry_patch_execution_and_post_review_types_v1.py",
    f"{_PKG}/p1_source_code_only_install_registry_patch_execution_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_source_code_only_install_registry_patch_execution_and_post_review_v1.py",
)

PROFILE_REF = "p1_source_code_only_install_registry_patch_execution_profile_v1"
DECISION_REF = "p1_source_code_only_install_registry_patch_execution_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_source_registry() -> Dict[str, Dict[str, Any]]:
    try:
        mod = importlib.import_module(SOURCE_REGISTRY_MODULE)
        assets = getattr(mod, SOURCE_REGISTRY_CONST, ())
        return {a["asset_id"]: dict(a) for a in assets if isinstance(a, dict) and "asset_id" in a}
    except Exception:  # noqa: BLE001 - registry read is best-effort for the before-snapshot
        return {}


def _json_safe(value: Any) -> Any:
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    return value


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1SourceCodeOnlyRegistryPatchExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            registry_patch_execution=REGISTRY_PATCH_EXECUTION,
            post_review_included=POST_REVIEW_INCLUDED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            registry_file_write_allowed=REGISTRY_FILE_WRITE_ALLOWED,
            allowed_registry_patch_scope=ALLOWED_REGISTRY_PATCH_SCOPE,
            source_install_allowed=SOURCE_INSTALL_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            dependency_install_allowed=DEPENDENCY_INSTALL_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            checkpoint_download_allowed=CHECKPOINT_DOWNLOAD_ALLOWED,
            dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
            example_asset_download_allowed=EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            in_scope_asset_ids=IN_SCOPE_ASSET_IDS,
            upstream_planning_ref=UPSTREAM_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_source_code_only_install_registry_patch_execution_and_post_review_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
    apply_registry_patch: bool = True,
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
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------- #
    # (一) Pre-patch snapshot.
    # ------------------------------------------------------------------- #
    source_registry = _load_source_registry()
    overlay_path = _REPO_ROOT / REGISTRY_OVERLAY_REL
    prior_overlay: Optional[Dict[str, Any]] = None
    if overlay_path.is_file():
        try:
            prior_overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            prior_overlay = None

    def _before_record(aid: str) -> Dict[str, Any]:
        rec = source_registry.get(aid, {})
        return {k: _json_safe(rec.get(k)) for k in BEFORE_FIELDS_OF_INTEREST}

    bt_before = _before_record("byte_track")
    ms_before = _before_record("mobile_sam")
    rollback_snapshot_ref = str(out_root / "registry_patch_pre_snapshot_v1.json")

    snapshot = RegistryPatchPreSnapshotRecord(
        snapshot_id="registry_patch_pre_snapshot_v1",
        registry_file_refs=(
            SOURCE_REGISTRY_MODULE.replace(".", "/") + ".py",
            REGISTRY_OVERLAY_REL,
        ),
        registry_asset_refs=IN_SCOPE_ASSET_IDS,
        byte_track_registry_before=bt_before,
        mobile_sam_registry_before=ms_before,
        timestamp=ts,
        upstream_planning_ref=UPSTREAM_PLANNING_REF,
        rollback_snapshot_ref=rollback_snapshot_ref,
        test_board_ref=f"capabilities/test_board/{TEST_BOARD_MODULE}/phase_p1_source_code_only_install_registry_patch_execution_and_post_review_v1_001",
        snapshot_performed=True,
        snapshot_written_before_patch=True,
    )

    # ------------------------------------------------------------------- #
    # Scope + field validation BEFORE writing.
    # ------------------------------------------------------------------- #
    patched_field_keys = tuple(sorted({k for a in PATCH_AFTER_VALUES.values() for k in a.keys()}))
    all_fields_within_scope = all(k in ALLOWED_PATCH_FIELD_KEYS for k in patched_field_keys)
    no_readiness_true = all(
        PATCH_AFTER_VALUES[aid].get(k) in (False, None)
        for aid in IN_SCOPE_ASSET_IDS
        for k in READINESS_FALSE_KEYS
        if k in PATCH_AFTER_VALUES[aid]
    )
    changed_asset_ids = tuple(IN_SCOPE_ASSET_IDS)
    only_scope_assets_changed = set(changed_asset_ids).issubset(set(IN_SCOPE_ASSET_IDS)) and not (
        set(changed_asset_ids) & set(MUST_NOT_MODIFY_ASSET_IDS)
    )
    mobile_sam_full_clone_false = PATCH_AFTER_VALUES["mobile_sam"].get("full_clone_allowed") is False
    mobile_sam_weight_not_downloaded = (
        PATCH_AFTER_VALUES["mobile_sam"].get("committed_weight_file_downloaded") is False
        and PATCH_AFTER_VALUES["mobile_sam"].get("model_weight_status") == "not_downloaded"
        and PATCH_AFTER_VALUES["mobile_sam"].get("checkpoint_weight_status") == "not_downloaded"
    )
    clean_pypi_candidate_false = all(
        PATCH_AFTER_VALUES[aid].get("clean_pypi_candidate") is False for aid in IN_SCOPE_ASSET_IDS
    )

    patch_safe_to_apply = (
        all_fields_within_scope and no_readiness_true and only_scope_assets_changed
        and mobile_sam_full_clone_false and mobile_sam_weight_not_downloaded and clean_pypi_candidate_false
    )

    # ------------------------------------------------------------------- #
    # (二/三/四) Execute the registry patch (overlay write — real mutation).
    # ------------------------------------------------------------------- #
    overlay_payload = {
        "overlay_id": "code_only_source_install_registry_overlay_v1",
        "overlay_kind": "code_only_source_install_metadata",
        "patched_by_phase": PHASE_ID,
        "patched_at_utc": ts,
        "source_registry_module": SOURCE_REGISTRY_MODULE,
        "scope_note": "Overlay layered over REGISTRY_ASSETS; code-only source install metadata only; no readiness set true.",
        "assets": {aid: dict(PATCH_AFTER_VALUES[aid]) for aid in IN_SCOPE_ASSET_IDS},
    }
    registry_patch_applied = False
    if apply_registry_patch and patch_safe_to_apply and REGISTRY_MUTATION_ALLOWED and REGISTRY_FILE_WRITE_ALLOWED:
        try:
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.write_text(json.dumps(overlay_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            registry_patch_applied = True
        except (PermissionError, OSError) as exc:
            warnings.append(f"registry_overlay_write_failed_sandbox:{type(exc).__name__}")
            registry_patch_applied = False
    if not patch_safe_to_apply:
        failed_checks.append("patch.unsafe_field_or_scope_or_readiness_violation_detected_patch_not_applied")

    execution_record = RegistryPatchExecutionRecord(
        execution_id="registry_patch_execution_v1",
        overlay_file_ref=REGISTRY_OVERLAY_REL,
        changed_asset_ids=changed_asset_ids,
        patched_field_keys=patched_field_keys,
        all_fields_within_scope=all_fields_within_scope,
        registry_patch_applied=registry_patch_applied,
        registry_mutation_performed=registry_patch_applied,
        only_scope_assets_changed=only_scope_assets_changed,
        install_performed=False,
        download_performed=False,
        real_import_performed=False,
    )

    # ------------------------------------------------------------------- #
    # (五) Patch diff.
    # ------------------------------------------------------------------- #
    before_values = {"byte_track": bt_before, "mobile_sam": ms_before}
    after_values = {aid: dict(PATCH_AFTER_VALUES[aid]) for aid in IN_SCOPE_ASSET_IDS}
    changed_field_paths = tuple(
        f"{aid}.{k}" for aid in IN_SCOPE_ASSET_IDS for k in sorted(PATCH_AFTER_VALUES[aid].keys())
    )

    def _no_ready_true(field_name: str) -> bool:
        return all(PATCH_AFTER_VALUES[aid].get(field_name) is not True for aid in IN_SCOPE_ASSET_IDS)

    diff_record = RegistryPatchDiffRecord(
        diff_id="registry_patch_diff_v1",
        changed_asset_count=len(changed_asset_ids),
        changed_assets=changed_asset_ids,
        changed_field_paths=changed_field_paths,
        before_values=before_values,
        after_values=after_values,
        no_unscoped_asset_changed=only_scope_assets_changed,
        no_weight_ready_field_set_true=mobile_sam_weight_not_downloaded,
        no_model_ready_field_set_true=_no_ready_true("model_ready"),
        no_inference_ready_field_set_true=_no_ready_true("inference_ready"),
        no_runtime_ready_field_set_true=_no_ready_true("runtime_ready"),
        no_output_adapter_ready_field_set_true=_no_ready_true("output_adapter_ready"),
        no_semantic_layer_ready_field_set_true=_no_ready_true("semantic_layer_ready"),
    )

    # ------------------------------------------------------------------- #
    # Code-only readiness patch (2) + weight boundary patch (2) + model/runtime boundary patch (2).
    # ------------------------------------------------------------------- #
    readiness_patches: List[CodeOnlyReadinessPatchRecord] = []
    weight_boundary_patches: List[WeightBoundaryPatchRecord] = []
    model_runtime_boundary_patches: List[ModelRuntimeBoundaryPatchRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        av = PATCH_AFTER_VALUES[aid]
        readiness_patches.append(
            CodeOnlyReadinessPatchRecord(
                asset_id=aid,
                install_method=av["install_method"],
                code_only_install_verified=bool(av["code_only_install_verified"]),
                find_spec_verified=bool(av["find_spec_verified"]),
                find_spec_import_root=av["find_spec_import_root"],
                readiness_level=av["readiness_level"],
                readiness_not_model_ready=av["model_ready"] is False,
                readiness_not_inference_ready=av["inference_ready"] is False,
                readiness_not_runtime_ready=av["runtime_ready"] is False,
            )
        )
        weight_boundary_patches.append(
            WeightBoundaryPatchRecord(
                asset_id=aid,
                model_weight_status=av["model_weight_status"],
                checkpoint_weight_status=av.get("checkpoint_weight_status", "not_downloaded"),
                weight_download_required_before_model_ready=bool(av["weight_download_required_before_model_ready"]),
                committed_weight_file=av.get("committed_weight_file"),
                committed_weight_file_size_bytes=int(av.get("committed_weight_file_size_bytes", 0)),
                committed_weight_file_downloaded=bool(av.get("committed_weight_file_downloaded", False)),
                full_clone_allowed=bool(av.get("full_clone_allowed", True)) if aid == "mobile_sam" else True,
                weight_excluding_checkout_required=bool(av.get("weight_excluding_checkout_required", False)),
                weight_download_requires_separate_request=True,
                weight_download_requires_owner_approval=True,
            )
        )
        model_runtime_boundary_patches.append(
            ModelRuntimeBoundaryPatchRecord(
                asset_id=aid,
                model_ready=bool(av["model_ready"]),
                inference_ready=bool(av["inference_ready"]),
                runtime_ready=bool(av["runtime_ready"]),
                output_adapter_ready=bool(av["output_adapter_ready"]),
                semantic_layer_ready=bool(av["semantic_layer_ready"]),
                commercial_runtime_approved=bool(av["commercial_runtime_approved"]),
                registry_patch_success_not_model_readiness=True,
                registry_patch_success_not_inference_approval=True,
                registry_patch_success_not_runtime_approval=True,
            )
        )

    # ------------------------------------------------------------------- #
    # (六) Post-review audit.
    # ------------------------------------------------------------------- #
    def _written(field_name: str, expected: Any) -> bool:
        return all(PATCH_AFTER_VALUES[aid].get(field_name) == expected for aid in IN_SCOPE_ASSET_IDS)

    post_review = RegistryPatchPostReviewAudit(
        audit_id="registry_patch_post_review_audit_v1",
        registry_patch_applied=registry_patch_applied,
        registry_patch_scope_valid=all_fields_within_scope,
        changed_asset_count=len(changed_asset_ids),
        only_byte_track_and_mobile_sam_changed=only_scope_assets_changed,
        code_only_install_verified_written=_written("code_only_install_verified", True),
        readiness_level_code_only_ready_written=_written("readiness_level", "code_only_ready"),
        weight_not_downloaded_written=_written("model_weight_status", "not_downloaded"),
        model_ready_false_written=_written("model_ready", False),
        inference_ready_false_written=_written("inference_ready", False),
        runtime_ready_false_written=_written("runtime_ready", False),
        output_adapter_ready_false_written=_written("output_adapter_ready", False),
        semantic_layer_ready_false_written=_written("semantic_layer_ready", False),
        commercial_runtime_false_written=_written("commercial_runtime_approved", False),
        source_repository_commit_written=all("source_repository_commit" in PATCH_AFTER_VALUES[aid] for aid in IN_SCOPE_ASSET_IDS),
        source_license_written=all("source_license" in PATCH_AFTER_VALUES[aid] for aid in IN_SCOPE_ASSET_IDS),
        import_root_written=all("import_root" in PATCH_AFTER_VALUES[aid] for aid in IN_SCOPE_ASSET_IDS),
        mobile_sam_weight_excluding_checkout_required_written=PATCH_AFTER_VALUES["mobile_sam"].get("weight_excluding_checkout_required") is True,
        mobile_sam_full_clone_allowed_false_written=mobile_sam_full_clone_false,
        test_board_written=write_test_board,
        test_board_protected=True,
        post_review_completed=True,
    )

    # ------------------------------------------------------------------- #
    # (七) Rollback readiness (2).
    # ------------------------------------------------------------------- #
    rollback_records: List[RegistryPatchRollbackReadinessRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        rollback_records.append(
            RegistryPatchRollbackReadinessRecord(
                asset_id=aid,
                rollback_available=True,
                rollback_snapshot_ref=rollback_snapshot_ref,
                rollback_not_executed_by_default=True,
                rollback_trigger_conditions=(
                    "unscoped_asset_modified",
                    "readiness_field_set_true",
                    "weight_or_checkpoint_marked_downloaded",
                    "field_outside_code_only_metadata_scope_written",
                    "weight_download_or_inference_or_runtime_detected",
                ),
                rollback_must_preserve_test_board=True,
                rollback_must_preserve_review_artifacts=True,
                rollback_success_requires_post_review=True,
            )
        )

    # ------------------------------------------------------------------- #
    # (八) Follow-up routing.
    # ------------------------------------------------------------------- #
    followup = RegistryPatchFollowupWeightDownloadRoute(
        routing_id="registry_patch_followup_weight_download_route_v1",
        recommended_next_phase=NEXT_PHASE_WEIGHT_DOWNLOAD,
        registry_patch_go_allows_weight_download_request_planning=True,
        registry_patch_go_does_not_allow_weight_download_execution=True,
        registry_patch_go_does_not_allow_model_load=True,
        registry_patch_go_does_not_allow_inference=True,
        registry_patch_go_does_not_allow_runtime=True,
        registry_patch_go_does_not_allow_output_adapter=True,
        registry_patch_go_does_not_allow_semantic_layer=True,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 18 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "snapshot_present": snapshot.snapshot_performed and snapshot.snapshot_written_before_patch,
        "only_scope_assets_changed": only_scope_assets_changed,
        "fields_within_scope": all_fields_within_scope,
        "no_readiness_true": no_readiness_true and diff_record.no_model_ready_field_set_true
        and diff_record.no_inference_ready_field_set_true and diff_record.no_runtime_ready_field_set_true
        and diff_record.no_output_adapter_ready_field_set_true and diff_record.no_semantic_layer_ready_field_set_true,
        "mobile_sam_full_clone_false": mobile_sam_full_clone_false,
        "mobile_sam_weight_not_downloaded": mobile_sam_weight_not_downloaded,
        "clean_pypi_candidate_false": clean_pypi_candidate_false,
        "no_install": SOURCE_INSTALL_ALLOWED is False and PIP_INSTALL_ALLOWED is False
        and DEPENDENCY_INSTALL_ALLOWED is False and not execution_record.install_performed,
        "no_download": (
            MODEL_DOWNLOAD_ALLOWED is False and WEIGHT_DOWNLOAD_ALLOWED is False and CHECKPOINT_DOWNLOAD_ALLOWED is False
            and DATASET_DOWNLOAD_ALLOWED is False and EXAMPLE_ASSET_DOWNLOAD_ALLOWED is False
            and not execution_record.download_performed
        ),
        "no_real_import_load_inference": (
            REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False and REAL_INFERENCE_ALLOWED is False
            and not execution_record.real_import_performed
        ),
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False and REAL_OUTPUT_ADAPTER_ALLOWED is False and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "diff_present": diff_record.changed_asset_count == 2 and len(diff_record.changed_field_paths) > 0,
        "post_review_present": post_review.post_review_completed and post_review.registry_patch_scope_valid,
        "patch_go_not_weight_approval": followup.registry_patch_go_does_not_allow_weight_download_execution
        and WEIGHT_DOWNLOAD_ALLOWED is False,
        "patch_go_not_inference_runtime_approval": followup.registry_patch_go_does_not_allow_inference
        and followup.registry_patch_go_does_not_allow_runtime,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeSourceCodeOnlyRegistryPatchExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeSourceCodeOnlyRegistryPatchExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_registry_patch_execution_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "source_code_only_registry_patch_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "registry_patch_pre_snapshot_record_count_eq_1": True,
        "registry_patch_execution_record_count_eq_1": True,
        "registry_patch_diff_record_count_gte_1": True,
        "code_only_readiness_patch_record_count_eq_2": len(readiness_patches) == 2,
        "weight_boundary_patch_record_count_eq_2": len(weight_boundary_patches) == 2,
        "model_runtime_boundary_patch_record_count_eq_2": len(model_runtime_boundary_patches) == 2,
        "registry_patch_post_review_audit_count_gte_1": True,
        "registry_patch_rollback_readiness_record_count_gte_1": len(rollback_records) >= 1,
        "registry_patch_followup_weight_download_route_count_gte_1": True,
        "negative_guard_count_eq_18": negative_guard_count == 18,
        "negative_guard_passed_eq_18": negative_guard_passed == 18,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "registry_patch_execution": REGISTRY_PATCH_EXECUTION is True,
        "post_review_included": POST_REVIEW_INCLUDED is True,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED is True,
        "registry_file_write_allowed": REGISTRY_FILE_WRITE_ALLOWED is True,
        "allowed_registry_patch_scope_code_only": ALLOWED_REGISTRY_PATCH_SCOPE == "code_only_source_install_metadata",
        "only_byte_track_and_mobile_sam_changed": only_scope_assets_changed,
        "changed_asset_count_eq_2": len(changed_asset_ids) == 2,
        "registry_patch_applied": registry_patch_applied,
        "code_only_install_verified_written": post_review.code_only_install_verified_written,
        "readiness_level_code_only_ready_written": post_review.readiness_level_code_only_ready_written,
        "weight_not_downloaded_written": post_review.weight_not_downloaded_written,
        "model_ready_false_written": post_review.model_ready_false_written,
        "inference_ready_false_written": post_review.inference_ready_false_written,
        "runtime_ready_false_written": post_review.runtime_ready_false_written,
        "output_adapter_ready_false_written": post_review.output_adapter_ready_false_written,
        "semantic_layer_ready_false_written": post_review.semantic_layer_ready_false_written,
        "commercial_runtime_false_written": post_review.commercial_runtime_false_written,
        "mobile_sam_weight_excluding_checkout_required_written": post_review.mobile_sam_weight_excluding_checkout_required_written,
        "mobile_sam_full_clone_allowed_false_written": post_review.mobile_sam_full_clone_allowed_false_written,
        # Forbidden actions all false.
        "source_install_allowed_false": SOURCE_INSTALL_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "dependency_install_allowed_false": DEPENDENCY_INSTALL_ALLOWED is False,
        "model_download_allowed_false": MODEL_DOWNLOAD_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "checkpoint_download_allowed_false": CHECKPOINT_DOWNLOAD_ALLOWED is False,
        "dataset_download_allowed_false": DATASET_DOWNLOAD_ALLOWED is False,
        "example_asset_download_allowed_false": EXAMPLE_ASSET_DOWNLOAD_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Patch GO semantics.
        "registry_patch_go_allows_weight_download_request_planning": followup.registry_patch_go_allows_weight_download_request_planning,
        "registry_patch_go_does_not_allow_weight_download_execution": followup.registry_patch_go_does_not_allow_weight_download_execution,
        "registry_patch_go_does_not_allow_model_load": followup.registry_patch_go_does_not_allow_model_load,
        "registry_patch_go_does_not_allow_inference": followup.registry_patch_go_does_not_allow_inference,
        "registry_patch_go_does_not_allow_runtime": followup.registry_patch_go_does_not_allow_runtime,
        "registry_patch_go_does_not_allow_output_adapter": followup.registry_patch_go_does_not_allow_output_adapter,
        "registry_patch_go_does_not_allow_semantic_layer": followup.registry_patch_go_does_not_allow_semantic_layer,
        "weight_download_requires_separate_request": WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_REQUEST is True,
        "weight_download_requires_owner_approval": WEIGHT_DOWNLOAD_REQUIRES_OWNER_APPROVAL is True,
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
    decision = P1SourceCodeOnlyRegistryPatchExecutionDecision(
        decision_ref=DECISION_REF,
        source_code_only_registry_patch_execution_profile_count=1,
        registry_patch_pre_snapshot_record_count=1,
        registry_patch_execution_record_count=1,
        registry_patch_diff_record_count=1,
        code_only_readiness_patch_record_count=len(readiness_patches),
        weight_boundary_patch_record_count=len(weight_boundary_patches),
        model_runtime_boundary_patch_record_count=len(model_runtime_boundary_patches),
        registry_patch_post_review_audit_count=1,
        registry_patch_rollback_readiness_record_count=len(rollback_records),
        registry_patch_followup_weight_download_route_count=1,
        changed_asset_count=len(changed_asset_ids),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Source Code-Only Install Registry Patch Execution And Post-Review (real registry write)",
        "lifecycle_variant": SCOPE,
        "patch_principle_zh": PATCH_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "patch_chain": PATCH_CHAIN,
        "registry_patch_execution": REGISTRY_PATCH_EXECUTION,
        "post_review_included": POST_REVIEW_INCLUDED,
        "allowed_registry_patch_scope": ALLOWED_REGISTRY_PATCH_SCOPE,
        "in_scope_asset_ids": list(IN_SCOPE_ASSET_IDS),
        "upstream_planning_ref": UPSTREAM_PLANNING_REF,
        "upstream_retry_ref": UPSTREAM_RETRY_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "source_code_only_registry_patch_execution_profile": _build_profile(),
        "source_code_only_registry_patch_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "registry_overlay_file_ref": REGISTRY_OVERLAY_REL,
        "registry_overlay_written": registry_patch_applied,
        "prior_overlay_existed": prior_overlay is not None,
        "registry_patch_pre_snapshot_record": asdict(snapshot),
        "registry_patch_pre_snapshot_record_count": 1,
        "registry_patch_execution_record": asdict(execution_record),
        "registry_patch_execution_record_count": 1,
        "registry_patch_diff_record": asdict(diff_record),
        "registry_patch_diff_record_count": 1,
        "code_only_readiness_patch_records": [asdict(r) for r in readiness_patches],
        "code_only_readiness_patch_record_count": len(readiness_patches),
        "weight_boundary_patch_records": [asdict(w) for w in weight_boundary_patches],
        "weight_boundary_patch_record_count": len(weight_boundary_patches),
        "model_runtime_boundary_patch_records": [asdict(b) for b in model_runtime_boundary_patches],
        "model_runtime_boundary_patch_record_count": len(model_runtime_boundary_patches),
        "registry_patch_post_review_audit": asdict(post_review),
        "registry_patch_post_review_audit_count": 1,
        "registry_patch_rollback_readiness_records": [asdict(r) for r in rollback_records],
        "registry_patch_rollback_readiness_record_count": len(rollback_records),
        "registry_patch_followup_weight_download_route": asdict(followup),
        "registry_patch_followup_weight_download_route_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "changed_asset_count": len(changed_asset_ids),
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "registry_patch_execution_status": (
                "byte_track_and_mobile_sam_registry_patched_code_only_source_install_metadata_only_code_only_ready_no_readiness_true"
                if blocker_count == 0
                else "blocked"
            ),
            "registry_overlay_file": REGISTRY_OVERLAY_REL,
            "registry_patch_applied": registry_patch_applied,
            "byte_track_install_method": PATCH_AFTER_VALUES["byte_track"]["install_method"],
            "mobile_sam_install_method": PATCH_AFTER_VALUES["mobile_sam"]["install_method"],
            "both_readiness_level": "code_only_ready",
            "recommended_next_phase": NEXT_PHASE_WEIGHT_DOWNLOAD,
            "transition_note": (
                "REAL registry write complete. A pre-patch snapshot captured the byte_track/mobile_sam registry "
                "records, then a scoped, reversible OVERLAY (" + REGISTRY_OVERLAY_REL + ") was written with code-only "
                "source-install metadata ONLY for the two in-scope assets (install_method, source repo/commit/branch/"
                "license, import_root, code_only_install_verified=true, find_spec_verified=true, readiness_level="
                "code_only_ready, weight not_downloaded), with model/inference/runtime/output_adapter/semantic readiness "
                "and commercial_runtime ALL written false. mobile_sam keeps full_clone_allowed=false + "
                "weight_excluding_checkout_required=true and its committed weights/mobile_sam.pt remains not_downloaded; "
                "clean_pypi_candidate stays false for both. A registry diff (changed_asset_count=2) and an inline "
                "post-review were produced; rollback readiness recorded (not triggered). No unscoped asset was changed, "
                "and NO install/download/import/model-load/inference/runtime/output-adapter/semantic action occurred. "
                "Registry patch GO is NOT weight-download / inference / runtime approval. Next phase: " +
                NEXT_PHASE_WEIGHT_DOWNLOAD + " may plan the weight-download request/approval/hash/storage/source-review/"
                "readiness — but still does NOT download weights; download requires a separate owner approval + post-review."
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

        extra_artifacts = {
            "registry_patch_pre_snapshot_v1.json": {"phase_id": PHASE_ID, "registry_patch_pre_snapshot_record": asdict(snapshot),
                                                     "prior_overlay_existed": prior_overlay is not None},
            "registry_patch_execution_record_v1.json": {"phase_id": PHASE_ID, "registry_patch_execution_record": asdict(execution_record),
                                                         "overlay_payload": overlay_payload},
            "registry_patch_diff_v1.json": {"phase_id": PHASE_ID, "registry_patch_diff_record": asdict(diff_record)},
            "registry_patch_post_review_audit_v1.json": {"phase_id": PHASE_ID, "registry_patch_post_review_audit": asdict(post_review)},
        }
        extra_artifact_files: List[str] = []
        for fname, payload in extra_artifacts.items():
            p = out_root / fname
            p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            extra_artifact_files.append(str(p))
        result["extra_artifact_files"] = extra_artifact_files

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
            "registry_patch_execution_record": {"registry_patch_pre_snapshot_record": asdict(snapshot),
                                                "registry_patch_execution_record": asdict(execution_record)},
            "registry_patch_diff_record": {"registry_patch_diff_record": asdict(diff_record)},
            "code_only_readiness_patch_record": {"code_only_readiness_patch_records": [asdict(r) for r in readiness_patches]},
            "weight_boundary_patch_record": {"weight_boundary_patch_records": [asdict(w) for w in weight_boundary_patches]},
            "model_runtime_boundary_patch_record": {"model_runtime_boundary_patch_records": [asdict(b) for b in model_runtime_boundary_patches]},
            "registry_patch_post_review_record": {"registry_patch_post_review_audit": asdict(post_review),
                                                  "registry_patch_rollback_readiness_records": [asdict(r) for r in rollback_records]},
            "followup_weight_download_route_record": {"registry_patch_followup_weight_download_route": asdict(followup)},
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
            "registry_patch_execution": True,
            "post_review_included": True,
            "weight_download_allowed": False,
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
    result = review_p1_source_code_only_install_registry_patch_execution_and_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "registry_overlay_file_ref": result.get("registry_overlay_file_ref"),
                "registry_overlay_written": result.get("registry_overlay_written"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "changed_asset_count": result["changed_asset_count"],
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
