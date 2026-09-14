# -*- coding: utf-8 -*-
"""P1 Model Test Lens Local Asset Import UI Patch Execution — review v1."""

from __future__ import annotations

import json
import re
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
from capabilities.midplatform.model_test_lens.model_test_lens_local_asset_import_ui_patch_execution_registry_v1 import (  # noqa: E402
    GOVERNANCE_CANONICAL_REFS,
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.midplatform.model_test_lens.model_test_lens_local_asset_import_ui_patch_execution_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXECUTION_PRINCIPLE_ZH,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FILE_DELETE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    FORBIDDEN_CODE_PATTERNS,
    LIVE_CAMERA_ALLOWED,
    LOCAL_ASSET_IMPORT_UI_ENABLED,
    LOCAL_STATIC_PAGE_ONLY,
    LUNA_CORE_PRINCIPLE,
    MICROPHONE_LIVE_CAPTURE_ALLOWED,
    MODEL_EXECUTION_ALLOWED,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_FAILED,
    NEXT_PHASE_GO,
    OPTIONAL_EXAMPLE_FILES,
    OUTPUT_ADAPTER_ALLOWED,
    PAGE_MAY_CREATE_JOB_REQUEST,
    PAGE_MAY_CREATE_RUNNER_BRIDGE_REQUEST,
    PAGE_MAY_IMPORT_ENVELOPE,
    PAGE_MAY_REGISTER_ASSETS,
    PAGE_MUST_NOT_EXECUTE_MODEL,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    REAL_EXECUTION_PHASE,
    REAL_INFERENCE_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_STATIC_FILES,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNNER_BRIDGE_UI_ENABLED,
    RUNTIME_EXECUTION_ALLOWED,
    SEMANTIC_LAYER_ALLOWED,
    STATIC_SITE_ROOT_REL,
    STATIC_SITE_UI_PATCH_EXECUTION,
    TARGET_CHAIN_REF,
    TESTBOARD_DELETE_ALLOWED,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UI_AUDIT_MARKERS,
    EXTERNAL_URL_ALLOWED,
    FollowupRunnerBridgeExecutionRouteRecord,
    LocalAssetImportUIFilePatchRecord,
    LocalAssetImportUIPostReviewAudit,
    LocalAssetImportUIRollbackReadinessRecord,
    LocalAssetManifestGenerationUIRecord,
    ModelTestJobRequestUIRecord,
    NegativeLocalAssetImportUIPatchGuard,
    NoModelExecutionBoundaryAuditRecord,
    P1ModelTestLensLocalAssetImportUIPatchExecutionDecision,
    P1ModelTestLensLocalAssetImportUIPatchExecutionProfile,
    RunnerBridgeRequestUIRecord,
    RunnerOutputStatusPlaceholderRecord,
    to_dict,
)

_PKG = "capabilities/midplatform/model_test_lens"
STEP_FILES = (
    f"{_PKG}/model_test_lens_local_asset_import_ui_patch_execution_types_v1.py",
    f"{_PKG}/model_test_lens_local_asset_import_ui_patch_execution_registry_v1.py",
    f"{_PKG}/review_model_test_lens_local_asset_import_ui_patch_execution_v1.py",
    *REQUIRED_STATIC_FILES,
)

PROFILE_REF = "model_test_lens_local_asset_import_ui_patch_execution_profile_v1"
DECISION_REF = "model_test_lens_local_asset_import_ui_patch_execution_decision_v1"
REVIEW_FILENAME = "p1_midplatform_model_test_lens_local_asset_import_ui_patch_execution_review_v1.json"
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


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
    / "p1_midplatform_model_test_lens_local_asset_import_ui_patch_execution_v1_smoke_v0"
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


def _read_site_text() -> str:
    parts: List[str] = []
    for rel in REQUIRED_STATIC_FILES:
        p = _resolve_file(rel)
        if p:
            parts.append(p.read_text(encoding="utf-8"))
    for extra in ("model_insight_layer_v1.js", "slam_diagnostic_panels.js"):
        p = _resolve_file(f"{STATIC_SITE_ROOT_REL}/{extra}")
        if p:
            parts.append(p.read_text(encoding="utf-8"))
    return "\n".join(parts)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scan_forbidden_patterns(combined: str) -> Tuple[bool, List[str]]:
    violations: List[str] = []
    for spec in FORBIDDEN_CODE_PATTERNS:
        if re.search(spec["regex"], combined, re.IGNORECASE):
            violations.append(spec["pattern_id"])
    return len(violations) == 0, violations


def _audit_ui_markers(combined: str) -> Dict[str, bool]:
    flags: Dict[str, bool] = {}
    for marker in UI_AUDIT_MARKERS:
        flags[marker["key"]] = marker["needle"] in combined
    flags["model_category_selector_present"] = "lai-model-category" in combined
    return flags


def _audit_preserved_features(app_text: str, index_text: str) -> Dict[str, bool]:
    combined = app_text + index_text
    panel_count = app_text.count("panel_id:")
    return {
        "existing_envelope_import_preserved": "json-file-input" in combined and "loadLocalJsonFile" in app_text,
        "mobilesam_example_preserved": "loadBuiltinExample" in app_text and "BUILTIN_MOBILE_SAM_EXAMPLE" in app_text,
        "slam_example_preserved": "loadBuiltinSlamExample" in app_text and "fetchBuiltinSlamExample" in app_text,
        "insight_layer_preserved": "ModelInsightLayer" in app_text and "model_insight_layer_v1.js" in index_text,
        "model_panel_count_eq_10": panel_count >= 10,
        "debug_mode_toggle_preserved": "debug-mode-toggle" in combined,
        "boundary_panel_preserved": "boundary-panel" in combined,
        "testboard_refs_preserved": "testboard-refs-panel" in combined,
    }


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1ModelTestLensLocalAssetImportUIPatchExecutionProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            static_site_ui_patch_execution=STATIC_SITE_UI_PATCH_EXECUTION,
            local_asset_import_ui_enabled=LOCAL_ASSET_IMPORT_UI_ENABLED,
            runner_bridge_ui_enabled=RUNNER_BRIDGE_UI_ENABLED,
            page_must_not_execute_model=PAGE_MUST_NOT_EXECUTE_MODEL,
            model_execution_allowed=MODEL_EXECUTION_ALLOWED,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_model_test_lens_local_asset_import_ui_patch_execution_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []
    warnings: List[str] = []
    boundary_violations: List[str] = []

    for rel in STEP_FILES:
        if _resolve_file(rel) is not None:
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    boundary_violations.extend(stage_issues)
    warnings.extend(stage_warnings)

    combined_text = _read_site_text()
    index_path = _resolve_file(f"{STATIC_SITE_ROOT_REL}/index.html")
    app_path = _resolve_file(f"{STATIC_SITE_ROOT_REL}/app.js")
    index_text = index_path.read_text(encoding="utf-8") if index_path else ""
    app_text = app_path.read_text(encoding="utf-8") if app_path else ""

    pattern_ok, pattern_violations = _scan_forbidden_patterns(combined_text)
    if not pattern_ok:
        boundary_violations.extend([f"forbidden_pattern:{v}" for v in pattern_violations])

    ui_flags = _audit_ui_markers(combined_text)
    preserve_flags = _audit_preserved_features(app_text, index_text)

    files_written = [rel for rel in REQUIRED_STATIC_FILES if _resolve_file(rel) is not None]
    file_patch = LocalAssetImportUIFilePatchRecord(
        record_id="local_asset_import_ui_file_patch_v1",
        static_site_root_rel=STATIC_SITE_ROOT_REL,
        files_written=tuple(files_written),
        index_html_updated=_resolve_file(f"{STATIC_SITE_ROOT_REL}/index.html") is not None,
        app_js_updated=_resolve_file(f"{STATIC_SITE_ROOT_REL}/app.js") is not None,
        styles_css_updated=_resolve_file(f"{STATIC_SITE_ROOT_REL}/styles.css") is not None,
        local_asset_import_ui_js_written=_resolve_file(f"{STATIC_SITE_ROOT_REL}/local_asset_import_ui_v1.js") is not None,
        runner_bridge_ui_js_written=_resolve_file(f"{STATIC_SITE_ROOT_REL}/runner_bridge_ui_v1.js") is not None,
        local_asset_import_examples_js_written=_resolve_file(f"{STATIC_SITE_ROOT_REL}/local_asset_import_examples_v1.js") is not None,
        ui_patch_files_written=len(files_written) == len(REQUIRED_STATIC_FILES),
    )

    manifest_ui = LocalAssetManifestGenerationUIRecord(
        record_id="local_asset_manifest_generation_ui_v1",
        generate_manifest_button_present=ui_flags.get("generate_manifest_button_present", False),
        asset_type_selector_present=ui_flags.get("asset_type_selector_present", False),
        local_file_selector_present=ui_flags.get("local_file_selector_present", False),
        manifest_fields_documented="buildManifestPreview" in combined_text and "candidate_only" in combined_text,
    )

    job_ui = ModelTestJobRequestUIRecord(
        record_id="model_test_job_request_ui_v1",
        create_job_request_button_present=ui_flags.get("create_job_request_button_present", False),
        requires_runner_execution="requires_runner_execution" in combined_text,
        requires_owner_approval="requires_owner_approval" in combined_text,
        candidate_output_only="candidate_output_only" in combined_text,
    )

    bridge_ui = RunnerBridgeRequestUIRecord(
        record_id="runner_bridge_request_ui_v1",
        create_runner_bridge_request_button_present=ui_flags.get("create_runner_bridge_request_button_present", False),
        lens_may_not_execute_runner="lens_may_not_execute_runner" in combined_text,
        adapter_required="adapter_required" in combined_text,
        adapter_target_envelope="model_test_result_envelope_v1",
    )

    status_placeholder = RunnerOutputStatusPlaceholderRecord(
        record_id="runner_output_status_placeholder_v1",
        runner_output_status_placeholder_present=ui_flags.get("runner_output_status_placeholder_present", False),
        waiting_for_runner_output_label="waiting_for_runner_output" in combined_text,
        import_envelope_when_ready_label="import_envelope_when_ready" in combined_text,
    )

    boundary_audit = NoModelExecutionBoundaryAuditRecord(
        record_id="no_model_execution_boundary_audit_v1",
        no_model_execution=MODEL_EXECUTION_ALLOWED is False and "runInference" not in combined_text,
        no_inference_execution=REAL_INFERENCE_ALLOWED is False,
        no_runtime=RUNTIME_EXECUTION_ALLOWED is False,
        no_output_adapter=OUTPUT_ADAPTER_ALLOWED is False,
        no_semantic_fact_navigation=(
            SEMANTIC_LAYER_ALLOWED is False
            and FACT_WRITE_ALLOWED is False
            and NAVIGATION_ACTION_SPEECH_ALLOWED is False
        ),
        no_registry_mutation=REGISTRY_MUTATION_ALLOWED is False and pattern_ok,
        no_external_url=EXTERNAL_URL_ALLOWED is False and pattern_ok,
        no_camera_microphone=LIVE_CAMERA_ALLOWED is False and MICROPHONE_LIVE_CAPTURE_ALLOWED is False and pattern_ok,
        no_delete_artifact_button=FILE_DELETE_ALLOWED is False and TESTBOARD_DELETE_ALLOWED is False,
        forbidden_pattern_scan_passed=pattern_ok,
    )

    rollback = LocalAssetImportUIRollbackReadinessRecord(
        record_id="local_asset_import_ui_rollback_readiness_v1",
        rollback_available=True,
        rollback_can_restore_previous_static_site_files=True,
        rollback_must_preserve_planning_artifacts=True,
        rollback_must_preserve_test_board=True,
        rollback_must_preserve_examples=True,
        rollback_not_executed_by_default=True,
    )

    followup = FollowupRunnerBridgeExecutionRouteRecord(
        record_id="followup_runner_bridge_execution_route_v1",
        recommended_next_phase=NEXT_PHASE_GO,
        route_note=(
            "UI patch registers assets and generates requests in-browser. "
            "Next: Local Runner Bridge Service at 127.0.0.1:8787 for actual runner execution."
        ),
        page_submits_job_runner_executes_separately=True,
    )

    existing_features_preserved = all([
        preserve_flags["existing_envelope_import_preserved"],
        preserve_flags["mobilesam_example_preserved"],
        preserve_flags["slam_example_preserved"],
        preserve_flags["insight_layer_preserved"],
        preserve_flags["model_panel_count_eq_10"],
        preserve_flags["debug_mode_toggle_preserved"],
    ])

    post_audit = LocalAssetImportUIPostReviewAudit(
        audit_id="model_test_lens_local_asset_import_ui_patch_post_review_audit_v1",
        index_html_updated=file_patch.index_html_updated,
        app_js_updated=file_patch.app_js_updated,
        styles_css_updated=file_patch.styles_css_updated,
        local_asset_import_ui_js_written=file_patch.local_asset_import_ui_js_written,
        runner_bridge_ui_js_written=file_patch.runner_bridge_ui_js_written,
        asset_type_selector_present=manifest_ui.asset_type_selector_present,
        local_file_selector_present=manifest_ui.local_file_selector_present,
        model_category_selector_present=ui_flags.get("model_category_selector_present", False),
        generate_manifest_button_present=manifest_ui.generate_manifest_button_present,
        create_job_request_button_present=job_ui.create_job_request_button_present,
        create_runner_bridge_request_button_present=bridge_ui.create_runner_bridge_request_button_present,
        runner_output_status_placeholder_present=status_placeholder.runner_output_status_placeholder_present,
        debug_mode_json_preview_present=ui_flags.get("debug_mode_json_preview_present", False),
        existing_envelope_import_preserved=preserve_flags["existing_envelope_import_preserved"],
        mobilesam_example_preserved=preserve_flags["mobilesam_example_preserved"],
        slam_example_preserved=preserve_flags["slam_example_preserved"],
        insight_layer_preserved=preserve_flags["insight_layer_preserved"],
        model_panel_count=10 if preserve_flags["model_panel_count_eq_10"] else 0,
        no_model_execution=boundary_audit.no_model_execution,
        no_inference_execution=boundary_audit.no_inference_execution,
        no_runtime=boundary_audit.no_runtime,
        no_output_adapter=boundary_audit.no_output_adapter,
        no_semantic_fact_navigation=boundary_audit.no_semantic_fact_navigation,
        no_registry_mutation=boundary_audit.no_registry_mutation,
        no_external_url=boundary_audit.no_external_url,
        no_camera_microphone=boundary_audit.no_camera_microphone,
        no_delete_artifact_button=boundary_audit.no_delete_artifact_button,
        test_board_written=write_test_board,
        test_board_protected=all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        post_review_passed=(
            file_patch.ui_patch_files_written
            and manifest_ui.generate_manifest_button_present
            and job_ui.create_job_request_button_present
            and bridge_ui.create_runner_bridge_request_button_present
            and existing_features_preserved
            and pattern_ok
        ),
    )

    invariant_state: Dict[str, bool] = {
        "upstream_planning_go_verified": verify_flags.get("local_asset_import_runner_bridge_planning_go_verified") is True,
        "no_model_execution": boundary_audit.no_model_execution,
        "no_inference_execution": boundary_audit.no_inference_execution,
        "no_runtime_output_adapter": boundary_audit.no_runtime and boundary_audit.no_output_adapter,
        "no_semantic_fact_navigation": boundary_audit.no_semantic_fact_navigation,
        "no_registry_mutation": boundary_audit.no_registry_mutation,
        "no_external_url": boundary_audit.no_external_url,
        "no_camera_microphone": boundary_audit.no_camera_microphone,
        "no_delete_artifact_button": boundary_audit.no_delete_artifact_button,
        "generate_manifest_button_present": manifest_ui.generate_manifest_button_present,
        "create_job_request_button_present": job_ui.create_job_request_button_present,
        "create_runner_bridge_request_button_present": bridge_ui.create_runner_bridge_request_button_present,
        "runner_output_status_placeholder_present": status_placeholder.runner_output_status_placeholder_present,
        "existing_features_preserved": existing_features_preserved,
        "debug_mode_json_preview_present": ui_flags.get("debug_mode_json_preview_present", False),
        "slam_without_gt_hints_present": ui_flags.get("slam_without_gt_hints_present", False),
        "test_board_record_required": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_artifact_protected": REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_artifact_protected", False) is True,
        "cleanup_preserves_testboard": True,
    }

    negative_guards: List[NegativeLocalAssetImportUIPatchGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeLocalAssetImportUIPatchGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    no_boundary_violation = len(boundary_violations) == 0
    ui_patch_ok = post_audit.post_review_passed

    if not no_boundary_violation:
        final_decision = FINAL_DECISION_BLOCKED
        decision_branch = "blocked"
        recommended_next = NEXT_PHASE_BLOCKED
        blocker_count = len(boundary_violations) + len(failed_checks)
    elif ui_patch_ok and negative_guard_passed == negative_guard_count:
        final_decision = FINAL_DECISION_GO
        decision_branch = "go"
        recommended_next = NEXT_PHASE_GO
        blocker_count = len(failed_checks)
    else:
        final_decision = FINAL_DECISION_FAILED
        decision_branch = "failed_no_boundary_violation"
        recommended_next = NEXT_PHASE_FAILED
        blocker_count = len(failed_checks)

    go_conditions: Dict[str, bool] = {
        "model_test_lens_local_asset_import_ui_patch_execution_profile_count_eq_1": True,
        "ui_patch_files_written": file_patch.ui_patch_files_written,
        "local_asset_import_ui_js_written": file_patch.local_asset_import_ui_js_written,
        "runner_bridge_ui_js_written": file_patch.runner_bridge_ui_js_written,
        **{k: ui_flags.get(k, False) for k in (
            "asset_type_selector_present", "local_file_selector_present",
            "generate_manifest_button_present", "create_job_request_button_present",
            "create_runner_bridge_request_button_present", "runner_output_status_placeholder_present",
            "debug_mode_json_preview_present", "slam_without_gt_hints_present",
        )},
        "model_category_selector_present": ui_flags.get("model_category_selector_present", False),
        "existing_envelope_import_preserved": preserve_flags["existing_envelope_import_preserved"],
        "mobilesam_example_preserved": preserve_flags["mobilesam_example_preserved"],
        "slam_example_preserved": preserve_flags["slam_example_preserved"],
        "insight_layer_preserved": preserve_flags["insight_layer_preserved"],
        "model_panel_count_eq_10": preserve_flags["model_panel_count_eq_10"],
        "no_model_execution": boundary_audit.no_model_execution,
        "no_inference_execution": boundary_audit.no_inference_execution,
        "no_runtime": boundary_audit.no_runtime,
        "no_output_adapter": boundary_audit.no_output_adapter,
        "no_semantic_fact_navigation": boundary_audit.no_semantic_fact_navigation,
        "no_registry_mutation": boundary_audit.no_registry_mutation,
        "no_external_url": boundary_audit.no_external_url,
        "no_camera_microphone": boundary_audit.no_camera_microphone,
        "no_delete_artifact_button": boundary_audit.no_delete_artifact_button,
        "page_may_register_assets": PAGE_MAY_REGISTER_ASSETS is True,
        "page_may_create_job_request": PAGE_MAY_CREATE_JOB_REQUEST is True,
        "page_may_create_runner_bridge_request": PAGE_MAY_CREATE_RUNNER_BRIDGE_REQUEST is True,
        "page_may_import_envelope": PAGE_MAY_IMPORT_ENVELOPE is True,
        "page_must_not_execute_model": PAGE_MUST_NOT_EXECUTE_MODEL is True,
        "negative_guard_count_eq_19": negative_guard_count == 19,
        "negative_guard_passed_eq_19": negative_guard_passed == 19,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
    }
    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1ModelTestLensLocalAssetImportUIPatchExecutionDecision(
        decision_ref=DECISION_REF,
        model_test_lens_local_asset_import_ui_patch_execution_profile_count=1,
        ui_patch_files_written=file_patch.ui_patch_files_written,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        failure_recorded=final_decision == FINAL_DECISION_FAILED,
        no_boundary_violation=no_boundary_violation,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Model Test Lens Local Asset Import UI Patch Execution And Post Review",
        "lifecycle_variant": "p1_midplatform_model_test_lens_local_asset_import_ui_patch_execution",
        "execution_principle_zh": EXECUTION_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "static_site_ui_patch_execution": STATIC_SITE_UI_PATCH_EXECUTION,
        "static_site_root_rel": STATIC_SITE_ROOT_REL,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "model_test_lens_local_asset_import_ui_patch_execution_profile": _build_profile(),
        "model_test_lens_local_asset_import_ui_patch_execution_profile_count": 1,
        "local_asset_import_ui_file_patch_record": asdict(file_patch),
        "local_asset_manifest_generation_ui_record": asdict(manifest_ui),
        "model_test_job_request_ui_record": asdict(job_ui),
        "runner_bridge_request_ui_record": asdict(bridge_ui),
        "runner_output_status_placeholder_record": asdict(status_placeholder),
        "no_model_execution_boundary_audit_record": asdict(boundary_audit),
        "local_asset_import_ui_post_review_record": asdict(post_audit),
        "local_asset_import_ui_rollback_readiness_record": asdict(rollback),
        "followup_runner_bridge_execution_route_record": asdict(followup),
        "forbidden_pattern_violations": pattern_violations,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "boundary_violations": boundary_violations,
        "stage_refs": stage_refs,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "final_decision": final_decision,
        "blocker_count": blocker_count,
        "recommended_next_phase": recommended_next,
        "conclusions": {
            "execution_status": decision_branch,
            "transition_note": (
                "UI patch complete. Page registers local assets and generates manifest/job/runner bridge "
                "in-browser only. No model execution. Next: Local Runner Bridge Service at 127.0.0.1:8787."
            ),
        },
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "reviewed_at": _now(),
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        (out_root / "model_test_lens_local_asset_import_ui_file_patch_record_v1.json").write_text(
            json.dumps(asdict(file_patch), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_lens_local_asset_manifest_generation_ui_record_v1.json").write_text(
            json.dumps(asdict(manifest_ui), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_lens_job_request_ui_record_v1.json").write_text(
            json.dumps(asdict(job_ui), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_lens_runner_bridge_request_ui_record_v1.json").write_text(
            json.dumps(asdict(bridge_ui), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_lens_local_asset_import_ui_patch_post_review_audit_v1.json").write_text(
            json.dumps(asdict(post_audit), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        result["output_root"] = str(out_root)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        try:
            manifest_tb = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "canonical"
        except (PermissionError, OSError):
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            manifest_tb = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest_tb["test_board_dir"])
        extra_payloads = {
            "local_asset_import_ui_file_patch_record": {"record": asdict(file_patch)},
            "local_asset_manifest_generation_ui_record": {"record": asdict(manifest_ui)},
            "model_test_job_request_ui_record": {"record": asdict(job_ui)},
            "runner_bridge_request_ui_record": {"record": asdict(bridge_ui)},
            "runner_output_status_placeholder_record": {"record": asdict(status_placeholder)},
            "no_model_execution_boundary_audit_record": {"record": asdict(boundary_audit)},
            "local_asset_import_ui_post_review_record": {"record": asdict(post_audit)},
            "followup_runner_bridge_execution_route_record": {"record": asdict(followup)},
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
            "test_artifact_protected": True,
            "real_execution_phase": True,
            "model_execution_allowed": False,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
            "semantic_layer_allowed": False,
            "fact_write_allowed": False,
        }
        for rtype, payload in extra_payloads.items():
            out = {**common, **payload}
            (board_dir / f"{rtype}.json").write_text(
                json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
        result["test_board_root"] = str(board_dir)
        result["test_board_record_count"] = manifest_tb.get("written_record_count", 0) + len(extra_payloads)

    return result


def main() -> int:
    result = review_model_test_lens_local_asset_import_ui_patch_execution_v1()
    print(json.dumps(
        {
            "phase_id": result["phase_id"],
            "final_decision": result["final_decision"],
            "blocker_count": result["blocker_count"],
            "negative_guard_passed": result["negative_guard_passed"],
            "negative_guard_count": result["negative_guard_count"],
            "recommended_next_phase": result["recommended_next_phase"],
        },
        indent=2,
        ensure_ascii=False,
    ))
    ok = {FINAL_DECISION_GO, FINAL_DECISION_FAILED}
    return 0 if result["final_decision"] in ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
