# -*- coding: utf-8 -*-
"""P1 MobileSAM Multi Real Image Inference Trial Request Approval And Readiness — review v1
(COMPRESSED PLANNING / APPROVAL ONLY, scope = mobile_sam_only)."""

from __future__ import annotations

import json
import sys
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
from capabilities.field_understanding.p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness.p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_registry_v1 import (  # noqa: E402
    GOVERNANCE_CANONICAL_REFS,
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_artifact,
    load_registry_overlay,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness.p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    BROAD_READINESS_MUST_BE_FALSE,
    CANDIDATE_OUTPUT_TARGET_DIR,
    COMMERCIAL_RUNTIME_APPROVED,
    COMPRESSED_PHASE,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CURSOR_ASSETS_DIR,
    EXECUTION_MANIFEST_OUTPUT_REL,
    EXCLUDED_SINGLE_TRIAL_CURSOR_FILE,
    EXTERNAL_IMAGE_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    IMAGE_INPUT_TO_MODEL_ALLOWED,
    LIVE_CAMERA_ALLOWED,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_ONLY,
    MODEL_LOAD_ALLOWED,
    MULTI_IMAGE_ASSET_SPECS,
    MULTI_IMAGE_COUNT,
    MULTI_TEST_ASSETS_DIR_REL,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_MULTI_EXECUTION,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNED_MEMORY_LIMIT_MB,
    PLANNED_TIMEOUT_SECONDS,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    PREDICTION_ALLOWED,
    PROMPT_TARGET_TEMPLATES,
    PROMPT_POINTS_BOXES_PLANNING_ALLOWED,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_OVERLAY_REL,
    REQUIRED_READINESS_LEVEL,
    REQUIRED_REGISTRY_TRUE_FLAGS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPED_FOR_PHASE,
    SCOPED_LOCAL_TEST_ASSET_REGISTRATION,
    SCOPE,
    SEGMENTATION_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_TYPE,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TIMEOUT_RATIONALE,
    UNCONTROLLED_DATASET_ALLOWED,
    UPSTREAM_QUALITY_REVIEW_EXPECTED_GO,
    UPSTREAM_QUALITY_REVIEW_REF,
    WEIGHT_CHAIN,
    MultiRealImageAssetDiscoveryRecord,
    MultiRealImageAssetRegistrationRecord,
    MultiRealImageCandidateOutputBoundaryRecord,
    MultiRealImageCommandWhitelistRecord,
    MultiRealImageFollowupExecutionRoute,
    MultiRealImageManifestPlanningRecord,
    MultiRealImageMemoryTimeoutBoundaryRecord,
    MultiRealImageOwnerApprovalIssuanceRecord,
    MultiRealImagePromptPlanningRecord,
    MultiRealImageReadinessReview,
    MultiRealImageRollbackCleanupPlanningRecord,
    NegativeMultiRealImageInferenceTrialRequestApprovalGuard,
    P1MobileSAMMultiRealImageInferenceTrialRequestApprovalReadinessDecision,
    P1MobileSAMMultiRealImageInferenceTrialRequestApprovalReadinessProfile,
    to_dict,
)

_PKG = "capabilities/field_understanding/p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness"
STEP_FILES = (
    f"{_PKG}/__init__.py",
    f"{_PKG}/p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_types_v1.py",
    f"{_PKG}/p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_v1.py",
)

PROFILE_REF = "p1_mobile_sam_multi_real_image_inference_trial_request_approval_readiness_profile_v1"
DECISION_REF = "p1_mobile_sam_multi_real_image_inference_trial_request_approval_readiness_decision_v1"
REVIEW_FILENAME = (
    "p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_review_v1.json"
)
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"

ALLOWED_FUTURE_STEPS = (
    "pre_inference_snapshot",
    "registry_model_readiness_recheck",
    "sha256_recheck_for_weight",
    "sha256_size_width_height_for_multi_real_local_images",
    "controlled_sys_path_setup",
    "import_mobile_sam",
    "load_checkpoint",
    "read_manifest_images_only",
    "execute_planned_prompt_points_boxes_per_image",
    "save_candidate_masks_summaries_to_tmp_eval_out",
    "memory_timeout_monitor",
    "cleanup",
    "post_review",
)
FORBIDDEN_FUTURE_STEPS = (
    "live_camera",
    "external_url",
    "non_manifest_image",
    "batch_dataset",
    "runtime_server",
    "output_adapter_call",
    "semantic_write",
    "fact_write",
    "navigation_action_speech",
    "registry_mutation",
    "additional_download",
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
    / "p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_v1_smoke_v0"
)


def _artifact_roots() -> List[Path]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return roots


def _resolve_file(rel: str) -> Optional[Path]:
    for base in _artifact_roots():
        p = base / rel
        if p.is_file():
            return p
    return None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _audit_registry_mobile_sam(overlay: Dict[str, Any]) -> Dict[str, Any]:
    asset = (overlay.get("assets") or {}).get(MOBILE_SAM_ASSET_ID) or {}
    readiness = asset.get("readiness_level")
    true_flags_ok = all(asset.get(f) is True for f in REQUIRED_REGISTRY_TRUE_FLAGS)
    broad_false = all(asset.get(f) is False for f in BROAD_READINESS_MUST_BE_FALSE)
    return {
        "readiness_level": readiness,
        "inference_trial_verified": asset.get("inference_trial_verified"),
        "true_flags_ok": true_flags_ok,
        "broad_readiness_all_false": broad_false,
        "audit_passed": (
            readiness == REQUIRED_READINESS_LEVEL
            and true_flags_ok
            and broad_false
        ),
        "asset_snapshot": {k: asset.get(k) for k in (
            ["readiness_level"] + list(REQUIRED_REGISTRY_TRUE_FLAGS) + list(BROAD_READINESS_MUST_BE_FALSE)
        )},
    }


def _audit_upstream_quality_review(repo_root: Path) -> Dict[str, Any]:
    artifact_rel = (
        "_tmp_eval_out/p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_v1_smoke_v0/"
        "p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_review_v1.json"
    )
    artifact, exists, resolved = load_artifact(repo_root, artifact_rel)
    go_ok = exists and (artifact or {}).get("final_decision") == UPSTREAM_QUALITY_REVIEW_EXPECTED_GO
    return {
        "artifact_exists": exists,
        "resolved_path": resolved,
        "final_decision": (artifact or {}).get("final_decision"),
        "can_enter_multi_real_image_trial_request_next": (artifact or {}).get(
            "can_enter_multi_real_image_trial_request_next"
        ),
        "go_verified": go_ok,
        "candidate_output_must_remain_candidate": True,
        "live_camera_forbidden": True,
        "external_url_forbidden": True,
    }


def _audit_governance_refs() -> Dict[str, Any]:
    refs_ok = all(_resolve_file(r) is not None for r in GOVERNANCE_CANONICAL_REFS)
    manifest_path = _resolve_file(GOVERNANCE_CANONICAL_REFS[0])
    manifest_ok = False
    if manifest_path is not None:
        try:
            m = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_ok = m.get("migration_mode") == "canonical_copy_no_delete"
        except (OSError, json.JSONDecodeError):
            pass
    return {
        "canonical_refs_ok": refs_ok,
        "canonical_standard_library_created": manifest_ok,
        "reference_policy_ok": _resolve_file(GOVERNANCE_CANONICAL_REFS[1]) is not None,
        "runtime_boundary_plan_ok": _resolve_file(GOVERNANCE_CANONICAL_REFS[2]) is not None,
        "runtime_admission_criteria_ok": _resolve_file(GOVERNANCE_CANONICAL_REFS[3]) is not None,
    }


def _discover_multi_assets() -> Tuple[MultiRealImageAssetDiscoveryRecord, List[Dict[str, Any]], int]:
    discovery_sources = [CURSOR_ASSETS_DIR, MULTI_TEST_ASSETS_DIR_REL]
    discovered: List[Dict[str, Any]] = []
    cursor_dir = Path(CURSOR_ASSETS_DIR)
    excluded_present = cursor_dir / EXCLUDED_SINGLE_TRIAL_CURSOR_FILE
    excluded_not_in_multi = not any(
        spec["cursor_asset_filename"] == EXCLUDED_SINGLE_TRIAL_CURSOR_FILE
        for spec in MULTI_IMAGE_ASSET_SPECS
    )

    for spec in MULTI_IMAGE_ASSET_SPECS:
        canonical_rel = f"{MULTI_TEST_ASSETS_DIR_REL}/{spec['canonical_filename']}"
        canonical_path = _resolve_file(canonical_rel)
        cursor_path = cursor_dir / spec["cursor_asset_filename"] if cursor_dir.is_dir() else None
        cursor_exists = cursor_path is not None and cursor_path.is_file()
        canonical_exists = canonical_path is not None
        if canonical_exists:
            discovered.append({
                "test_asset_id": spec["test_asset_id"],
                "canonical_path": str(canonical_path),
                "canonical_rel": canonical_rel,
                "source_file_id": spec["source_file_id"],
                "cursor_asset_filename": spec["cursor_asset_filename"],
                "cursor_asset_exists": cursor_exists,
                "scene_type": spec["scene_type"],
                "source_type": SOURCE_TYPE,
                "live_camera_frame": False,
                "external_url_source": False,
                "uncontrolled_dataset_source": False,
                "personal_sensitive_image": False,
                "sha256": "pending_verification_in_execution_phase",
                "width": "pending_verification_in_execution_phase",
                "height": "pending_verification_in_execution_phase",
                "discovery_status": "canonical_registered",
            })

    discovery_record = MultiRealImageAssetDiscoveryRecord(
        record_id="multi_real_image_asset_discovery_v1",
        discovery_sources=tuple(discovery_sources),
        discovered_count=len(discovered),
        required_count=MULTI_IMAGE_COUNT,
        excluded_single_trial_asset=EXCLUDED_SINGLE_TRIAL_CURSOR_FILE,
        discovery_succeeded=(
            len(discovered) == MULTI_IMAGE_COUNT
            and excluded_not_in_multi
            and (not excluded_present.is_file() or excluded_not_in_multi)
        ),
    )
    return discovery_record, discovered, len(discovered)


def _build_manifest_entries(registered: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], ...]:
    entries: List[Dict[str, Any]] = []
    for asset in registered:
        entries.append({
            "test_asset_id": asset["test_asset_id"],
            "image_path": asset["canonical_rel"],
            "source_file_id": asset["source_file_id"],
            "scene_type": asset["scene_type"],
            "source_type": SOURCE_TYPE,
            "live_camera_frame": False,
            "external_url_source": False,
            "dataset_source": False,
            "personal_sensitive_image": False,
            "sha256": "pending_verification_in_execution_phase",
            "width": "pending_verification_in_execution_phase",
            "height": "pending_verification_in_execution_phase",
        })
    return tuple(entries)


def _build_prompt_plans(registered: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], ...]:
    plans: List[Dict[str, Any]] = []
    for asset in registered:
        for tmpl in PROMPT_TARGET_TEMPLATES:
            plans.append({
                "test_asset_id": asset["test_asset_id"],
                "scene_type": asset["scene_type"],
                "prompt_id": tmpl["prompt_id"],
                "target_description": tmpl["target_description"],
                "prompt_type_preferred": tmpl["prompt_type_preferred"],
                "approximate_region_placeholder": tmpl["approximate_region_placeholder"],
                "execution_coordinate_generation_required": True,
                "semantic_assertion_allowed": False,
                "fact_write_allowed": False,
                "segmentation_output_is_candidate_mask_only": True,
            })
    return tuple(plans)


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMMultiRealImageInferenceTrialRequestApprovalReadinessProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            compressed_phase=COMPRESSED_PHASE,
            planning_only=PLANNING_ONLY,
            mobile_sam_only=MOBILE_SAM_ONLY,
            multi_real_image_trial_request_included=True,
            multi_real_image_owner_approval_issuance_included=True,
            multi_real_image_trial_readiness_review_included=True,
            scoped_local_test_asset_registration=SCOPED_LOCAL_TEST_ASSET_REGISTRATION,
            multi_image_manifest_planning_allowed=True,
            prompt_points_boxes_planning_allowed=PROMPT_POINTS_BOXES_PLANNING_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            image_input_to_model_allowed=IMAGE_INPUT_TO_MODEL_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            upstream_quality_review_ref=UPSTREAM_QUALITY_REVIEW_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_v1(
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
        if _resolve_file(rel) is not None:
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    quality_audit = _audit_upstream_quality_review(_REPO_ROOT)
    if not quality_audit["go_verified"]:
        failed_checks.append("upstream.quality_review_not_go")

    gov_audit = _audit_governance_refs()
    if not gov_audit["canonical_refs_ok"]:
        failed_checks.append("governance.canonical_refs_incomplete")

    overlay, overlay_path = load_registry_overlay(_REPO_ROOT, REGISTRY_OVERLAY_REL)
    if overlay is None:
        failed_checks.append("registry.overlay_missing")
        reg_audit = {"audit_passed": False}
    else:
        reg_audit = _audit_registry_mobile_sam(overlay)
        if not reg_audit["audit_passed"]:
            failed_checks.append(f"registry.mobile_sam_audit_failed:{reg_audit}")

    discovery, registered_assets, source_image_count = _discover_multi_assets()
    if not discovery.discovery_succeeded:
        failed_checks.append(
            f"assets.discovery_failed:discovered={discovery.discovered_count}/required={discovery.required_count}"
        )

    asset_registration = MultiRealImageAssetRegistrationRecord(
        record_id="multi_real_image_asset_registration_v1",
        registered_assets=tuple(registered_assets),
        registered_count=source_image_count,
        source_type=SOURCE_TYPE,
        scoped_for_phase=SCOPED_FOR_PHASE,
        candidate_only_use=True,
        image_read_this_phase=False,
    )

    manifest_entries = _build_manifest_entries(registered_assets)
    manifest_plan = MultiRealImageManifestPlanningRecord(
        record_id="multi_real_image_manifest_plan_v1",
        execution_manifest_output_rel=EXECUTION_MANIFEST_OUTPUT_REL,
        planned_manifest_entries=manifest_entries,
        sha256_verification_deferred_to_execution=True,
    )

    prompt_plans = _build_prompt_plans(registered_assets)
    prompt_plan = MultiRealImagePromptPlanningRecord(
        record_id="multi_real_image_prompt_plan_v1",
        prompt_plans=prompt_plans,
        prompt_labels_are_test_descriptions_only=True,
        semantic_fact_assertion_allowed=False,
    )

    candidate_boundary = MultiRealImageCandidateOutputBoundaryRecord(
        record_id="multi_real_image_candidate_output_boundary_v1",
        candidate_output_only=True,
        output_target_dir=CANDIDATE_OUTPUT_TARGET_DIR,
        per_image_candidate_masks_required=True,
        per_prompt_quality_summary_required=True,
        aggregate_quality_summary_required=True,
        output_not_fact=True,
        output_requires_post_review=True,
    )

    approval = MultiRealImageOwnerApprovalIssuanceRecord(
        record_id="multi_real_image_owner_approval_issuance_v1",
        owner_approval_granted_for_multi_real_image_inference_preparation=True,
        owner_approval_granted_for_multi_real_image_inference_execution_next=True,
        runtime_approved=False,
        output_adapter_approved=False,
        semantic_layer_approved=False,
        fact_write_approved=False,
        multi_image_inference_approval_not_runtime_approval=True,
    )

    whitelist = MultiRealImageCommandWhitelistRecord(
        record_id="multi_real_image_command_whitelist_v1",
        allowed_future_steps=ALLOWED_FUTURE_STEPS,
        forbidden_future_steps=FORBIDDEN_FUTURE_STEPS,
        command_template_only=True,
    )

    memory_timeout = MultiRealImageMemoryTimeoutBoundaryRecord(
        record_id="multi_real_image_memory_timeout_boundary_v1",
        memory_limit_mb=PLANNED_MEMORY_LIMIT_MB,
        timeout_seconds=PLANNED_TIMEOUT_SECONDS,
        timeout_rationale=TIMEOUT_RATIONALE,
        oom_handling_required=True,
        no_persistent_runtime_process_allowed=True,
    )

    rollback = MultiRealImageRollbackCleanupPlanningRecord(
        record_id="multi_real_image_rollback_cleanup_plan_v1",
        pre_inference_snapshot_required=True,
        rollback_required=True,
        rollback_preserves_source_uploaded_images=True,
        rollback_preserves_test_board=True,
        no_registry_mutation_on_failure=True,
    )

    can_enter_execution = (
        quality_audit["go_verified"]
        and reg_audit.get("audit_passed")
        and gov_audit["canonical_refs_ok"]
        and discovery.discovery_succeeded
        and asset_registration.candidate_only_use
        and source_image_count == MULTI_IMAGE_COUNT
    )

    readiness = MultiRealImageReadinessReview(
        review_id="multi_real_image_readiness_review_v1",
        can_enter_multi_real_image_inference_trial_execution_next=bool(can_enter_execution),
        multi_real_image_trial_execution_scope="mobile_sam_multi_user_supplied_local_images_candidate_only",
        execution_requires_manifest=True,
        execution_requires_prompt_plan=True,
        can_enter_runtime_after_this_phase=False,
    )

    followup = MultiRealImageFollowupExecutionRoute(
        route_id="multi_real_image_followup_execution_route_v1",
        recommended_next_phase=NEXT_PHASE_MULTI_EXECUTION,
        next_phase_still_candidate_only=True,
    )

    image_source_allowed = (
        asset_registration.source_type == SOURCE_TYPE
        and all(
            a.get("live_camera_frame") is False
            and a.get("external_url_source") is False
            and a.get("uncontrolled_dataset_source") is False
            and a.get("personal_sensitive_image") is False
            for a in registered_assets
        )
    )
    prompt_labels_not_facts = all(
        p.get("semantic_assertion_allowed") is False and p.get("fact_write_allowed") is False
        for p in prompt_plans
    )
    whitelist_strict = (
        "runtime_server" in whitelist.forbidden_future_steps
        and "output_adapter_call" in whitelist.forbidden_future_steps
        and "semantic_write" in whitelist.forbidden_future_steps
        and "fact_write" in whitelist.forbidden_future_steps
        and "navigation_action_speech" in whitelist.forbidden_future_steps
        and "registry_mutation" in whitelist.forbidden_future_steps
        and "additional_download" in whitelist.forbidden_future_steps
        and "live_camera" in whitelist.forbidden_future_steps
        and "external_url" in whitelist.forbidden_future_steps
    )

    invariant_state: Dict[str, bool] = {
        "upstream_quality_review_go": quality_audit["go_verified"],
        "registry_inference_trial_verified": reg_audit.get("audit_passed") is True,
        "no_real_inference": REAL_INFERENCE_ALLOWED is False,
        "no_image_input_to_model": IMAGE_INPUT_TO_MODEL_ALLOWED is False and asset_registration.image_read_this_phase is False,
        "no_real_import_load": REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_fact_navigation_speech": FACT_WRITE_ALLOWED is False and NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False and rollback.no_registry_mutation_on_failure is True,
        "no_extra_download": (
            ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False
            and EXTERNAL_IMAGE_DOWNLOAD_ALLOWED is False
        ),
        "image_source_allowed": image_source_allowed,
        "not_personal_sensitive": all(a.get("personal_sensitive_image") is False for a in registered_assets),
        "four_assets_discovered": discovery.discovery_succeeded and source_image_count == MULTI_IMAGE_COUNT,
        "prompt_labels_not_facts": prompt_labels_not_facts and prompt_plan.prompt_labels_are_test_descriptions_only,
        "candidate_boundary_present": (
            candidate_boundary.candidate_output_only
            and candidate_boundary.output_not_fact
            and candidate_boundary.output_requires_post_review
        ),
        "approval_not_downstream": (
            approval.multi_image_inference_approval_not_runtime_approval
            and approval.runtime_approved is False
            and approval.output_adapter_approved is False
            and approval.fact_write_approved is False
        ),
        "whitelist_strict": whitelist_strict and whitelist.command_template_only is True,
        "rollback_present": (
            rollback.pre_inference_snapshot_required
            and rollback.rollback_required
            and rollback.rollback_preserves_test_board
            and rollback.rollback_preserves_source_uploaded_images
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMultiRealImageInferenceTrialRequestApprovalGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMultiRealImageInferenceTrialRequestApprovalGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_multi_real_image_request_approval_readiness_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "mobile_sam_multi_real_image_inference_request_readiness_profile_count_eq_1": True,
        "stage_ref_count_gte_10": len(stage_refs) >= 10,
        "multi_real_image_asset_discovery_record_count_gte_1": True,
        "multi_real_image_asset_registration_record_count_gte_1": True,
        "multi_real_image_manifest_plan_record_count_gte_1": True,
        "multi_real_image_prompt_plan_record_count_gte_1": True,
        "multi_real_image_candidate_output_boundary_record_count_gte_1": True,
        "multi_real_image_owner_approval_issuance_record_count_gte_1": True,
        "multi_real_image_command_whitelist_record_count_gte_1": True,
        "multi_real_image_memory_timeout_boundary_record_count_gte_1": True,
        "multi_real_image_rollback_cleanup_plan_record_count_gte_1": True,
        "multi_real_image_readiness_review_record_count_gte_1": True,
        "multi_real_image_followup_execution_route_record_count_gte_1": True,
        "negative_guard_count_eq_20": negative_guard_count == 20,
        "negative_guard_passed_eq_20": negative_guard_passed == 20,
        "source_image_count_eq_4": source_image_count == MULTI_IMAGE_COUNT,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "compressed_phase": COMPRESSED_PHASE is True,
        "planning_only": PLANNING_ONLY is True,
        "mobile_sam_only": MOBILE_SAM_ONLY is True,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "image_input_to_model_allowed_false": IMAGE_INPUT_TO_MODEL_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "owner_approval_granted_for_multi_real_image_inference_preparation": approval.owner_approval_granted_for_multi_real_image_inference_preparation,
        "owner_approval_granted_for_multi_real_image_inference_execution_next": approval.owner_approval_granted_for_multi_real_image_inference_execution_next,
        "can_enter_multi_real_image_inference_trial_execution_next": readiness.can_enter_multi_real_image_inference_trial_execution_next,
        "can_enter_runtime_after_this_phase_false": readiness.can_enter_runtime_after_this_phase is False,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
    }

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    no_boundary_violation = all(g.passed for g in negative_guards)
    failure_recorded = source_image_count < MULTI_IMAGE_COUNT

    if failure_recorded and no_boundary_violation:
        final_decision = FINAL_DECISION_FAILED
    elif blocker_count == 0:
        final_decision = FINAL_DECISION_GO
    else:
        final_decision = FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMMultiRealImageInferenceTrialRequestApprovalReadinessDecision(
        decision_ref=DECISION_REF,
        mobile_sam_multi_real_image_inference_request_readiness_profile_count=1,
        multi_real_image_asset_discovery_record_count=1,
        multi_real_image_asset_registration_record_count=1,
        multi_real_image_manifest_plan_record_count=1,
        multi_real_image_prompt_plan_record_count=1,
        multi_real_image_candidate_output_boundary_record_count=1,
        multi_real_image_owner_approval_issuance_record_count=1,
        multi_real_image_command_whitelist_record_count=1,
        multi_real_image_memory_timeout_boundary_record_count=1,
        multi_real_image_rollback_cleanup_plan_record_count=1,
        multi_real_image_readiness_review_record_count=1,
        multi_real_image_followup_execution_route_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        source_image_count=source_image_count,
        test_board_record_count=test_board_total,
        can_enter_multi_real_image_inference_trial_execution_next=(
            readiness.can_enter_multi_real_image_inference_trial_execution_next and final_decision == FINAL_DECISION_GO
        ),
        failure_recorded=failure_recorded,
        no_boundary_violation=no_boundary_violation,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Multi Real Image Inference Trial Request Approval And Readiness (planning only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "compressed_phase": COMPRESSED_PHASE,
        "planning_only": PLANNING_ONLY,
        "mobile_sam_only": MOBILE_SAM_ONLY,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "upstream_quality_review_ref": UPSTREAM_QUALITY_REVIEW_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "mobile_sam_multi_real_image_inference_trial_request_approval_readiness_profile": _build_profile(),
        "mobile_sam_multi_real_image_inference_request_readiness_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "upstream_quality_review_audit": quality_audit,
        "governance_standards_audit": gov_audit,
        "registry_overlay_path": overlay_path,
        "mobile_sam_registry_audit": reg_audit,
        "multi_real_image_asset_discovery_record": asdict(discovery),
        "multi_real_image_asset_registration_record": asdict(asset_registration),
        "multi_real_image_manifest_plan_record": asdict(manifest_plan),
        "multi_real_image_prompt_plan_record": asdict(prompt_plan),
        "multi_real_image_candidate_output_boundary_record": asdict(candidate_boundary),
        "multi_real_image_owner_approval_issuance_record": asdict(approval),
        "multi_real_image_command_whitelist_record": asdict(whitelist),
        "multi_real_image_memory_timeout_boundary_record": asdict(memory_timeout),
        "multi_real_image_rollback_cleanup_plan_record": asdict(rollback),
        "multi_real_image_readiness_review_record": asdict(readiness),
        "multi_real_image_followup_execution_route_record": asdict(followup),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "source_image_count": source_image_count,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "multi_real_image_request_approval_readiness_status": (
                "go" if final_decision == FINAL_DECISION_GO else (
                    "failed_no_boundary_violation" if final_decision == FINAL_DECISION_FAILED else "blocked"
                )
            ),
            "inference_executed_this_phase": False,
            "image_read_this_phase": False,
            "imported_this_phase": False,
            "model_loaded_this_phase": False,
            "registry_mutated_this_phase": False,
            "source_image_count": source_image_count,
            "can_enter_multi_real_image_inference_trial_execution_next": decision.can_enter_multi_real_image_inference_trial_execution_next,
            "recommended_next_phase": NEXT_PHASE_MULTI_EXECUTION,
            "transition_note": (
                "PLANNING / APPROVAL ONLY (mobile_sam_only). Four user-supplied daytime street scenes "
                "registered as scoped local test assets. Multi-image manifest, per-image prompt plan, "
                "candidate-only output boundary, command whitelist, memory/timeout(600s), rollback/cleanup, "
                "readiness review produced. Narrow owner approval issued for execution-next. "
                "NO inference, NO image input, NO import/load, NO runtime/output/semantic/fact/navigation. "
                "Next: " + NEXT_PHASE_MULTI_EXECUTION + " (manifest image read, planned prompts, candidate masks only)."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
        "can_enter_multi_real_image_trial_request_next": decision.can_enter_multi_real_image_inference_trial_execution_next,
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)

        (out_root / "multi_real_image_asset_discovery_v1.json").write_text(
            json.dumps(asdict(discovery), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "multi_real_image_asset_registration_v1.json").write_text(
            json.dumps(asdict(asset_registration), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "multi_real_image_manifest_plan_v1.json").write_text(
            json.dumps(asdict(manifest_plan), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "multi_real_image_prompt_plan_v1.json").write_text(
            json.dumps(asdict(prompt_plan), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "multi_real_image_readiness_review_v1.json").write_text(
            json.dumps(asdict(readiness), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        extra_refs = [result.get("output_review_file")]
        try:
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
                extra_artifact_refs=[r for r in extra_refs if r],
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
                extra_artifact_refs=[r for r in extra_refs if r],
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "multi_real_image_asset_discovery_record": {"record": asdict(discovery)},
            "multi_real_image_asset_registration_record": {"record": asdict(asset_registration)},
            "multi_real_image_manifest_plan_record": {"record": asdict(manifest_plan)},
            "multi_real_image_prompt_plan_record": {"record": asdict(prompt_plan)},
            "multi_real_image_candidate_output_boundary_record": {"record": asdict(candidate_boundary)},
            "multi_real_image_owner_approval_issuance_record": {"record": asdict(approval)},
            "multi_real_image_command_whitelist_record": {"record": asdict(whitelist)},
            "multi_real_image_memory_timeout_boundary_record": {"record": asdict(memory_timeout)},
            "multi_real_image_rollback_cleanup_plan_record": {"record": asdict(rollback)},
            "multi_real_image_readiness_review_record": {"record": asdict(readiness)},
            "multi_real_image_followup_execution_route_record": {"record": asdict(followup)},
        }
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
            "real_inference_allowed": False,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
            "semantic_layer_allowed": False,
            "fact_write_allowed": False,
            "registry_mutation_allowed": False,
        }
        extra_written: List[str] = []
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(
                json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            extra_written.append(str(p))
        manifest["extra_written_records"] = extra_written
        manifest["total_record_count"] = manifest["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["total_record_count"]

    return result


def main() -> int:
    result = review_p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "negative_guard_passed": result["negative_guard_passed"],
                "source_image_count": result["source_image_count"],
                "can_enter_multi_real_image_inference_trial_execution_next": result["conclusions"][
                    "can_enter_multi_real_image_inference_trial_execution_next"
                ],
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
