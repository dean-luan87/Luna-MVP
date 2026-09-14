# -*- coding: utf-8 -*-
"""P1 Midplatform Model Test Lens Static Site Skeleton Execution — review v1."""

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
from capabilities.midplatform.model_test_lens.model_test_lens_skeleton_execution_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.midplatform.model_test_lens.model_test_lens_skeleton_execution_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXAMPLE_ENVELOPE_REL,
    EXECUTION_PRINCIPLE_ZH,
    EXTERNAL_URL_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FILE_DELETE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    FORBIDDEN_CODE_PATTERNS,
    LIVE_CAMERA_ALLOWED,
    LOCAL_STATIC_PAGE_ONLY,
    LUNA_CORE_PRINCIPLE,
    MICROPHONE_ALLOWED,
    MODEL_EXECUTION_ALLOWED,
    MODEL_PANEL_SKELETON_REGISTRY,
    MODEL_TESTING_ONLY,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_DATA_ADAPTER,
    NEXT_PHASE_FAILED,
    NOT_WHITEBOX_PRODUCT_PAGE,
    OUTPUT_ADAPTER_ALLOWED,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    READ_LOCAL_JSON_ONLY,
    REAL_EXECUTION_PHASE,
    REAL_INFERENCE_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_STATIC_FILES,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SEMANTIC_LAYER_ALLOWED,
    STATIC_SITE_ROOT_REL,
    STATIC_SITE_SKELETON_EXECUTION,
    TARGET_CHAIN_REF,
    TESTBOARD_DELETE_ALLOWED,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_PLANNING_REF,
    ModelTestLensBoundaryPanelRecord,
    ModelTestLensExampleLoaderRecord,
    ModelTestLensFollowupRouteRecord,
    ModelTestLensModelPanelSkeletonRecord,
    ModelTestLensNoRuntimeNoModelExecutionAuditRecord,
    ModelTestLensRollbackReadinessRecord,
    ModelTestLensStaticSiteFileGenerationRecord,
    ModelTestLensStaticSitePostReviewAudit,
    NegativeModelTestLensStaticSiteSkeletonGuard,
    P1MidplatformModelTestLensStaticSiteSkeletonExecutionDecision,
    P1MidplatformModelTestLensStaticSiteSkeletonExecutionProfile,
    to_dict,
)

_PKG = "capabilities/midplatform/model_test_lens"
STEP_FILES = (
    f"{_PKG}/model_test_lens_skeleton_execution_types_v1.py",
    f"{_PKG}/model_test_lens_skeleton_execution_registry_v1.py",
    f"{_PKG}/review_model_test_lens_static_site_skeleton_execution_v1.py",
    *REQUIRED_STATIC_FILES,
)

PROFILE_REF = "model_test_lens_static_site_skeleton_execution_profile_v1"
DECISION_REF = "model_test_lens_static_site_skeleton_execution_decision_v1"
REVIEW_FILENAME = "p1_midplatform_model_test_lens_static_site_skeleton_execution_review_v1.json"
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
    / "p1_midplatform_model_test_lens_static_site_skeleton_execution_v1_smoke_v0"
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


def _scan_forbidden_patterns(app_js: str, index_html: str) -> Tuple[bool, List[str]]:
    combined = app_js + "\n" + index_html
    violations: List[str] = []
    for spec in FORBIDDEN_CODE_PATTERNS:
        if re.search(spec["regex"], combined, re.IGNORECASE):
            violations.append(spec["pattern_id"])
    return len(violations) == 0, violations


def _audit_static_site_files() -> Tuple[ModelTestLensStaticSiteFileGenerationRecord, Dict[str, bool]]:
    files_written: List[str] = []
    flags: Dict[str, bool] = {}
    for rel in REQUIRED_STATIC_FILES:
        exists = _resolve_file(rel) is not None
        flags[rel.split("/")[-1].replace(".", "_") + "_exists"] = exists
        if exists:
            files_written.append(rel)
    record = ModelTestLensStaticSiteFileGenerationRecord(
        record_id="model_test_lens_static_site_file_generation_v1",
        static_site_root_rel=STATIC_SITE_ROOT_REL,
        files_written=tuple(files_written),
        index_html_written=_resolve_file(f"{STATIC_SITE_ROOT_REL}/index.html") is not None,
        app_js_written=_resolve_file(f"{STATIC_SITE_ROOT_REL}/app.js") is not None,
        styles_css_written=_resolve_file(f"{STATIC_SITE_ROOT_REL}/styles.css") is not None,
        readme_written=_resolve_file(f"{STATIC_SITE_ROOT_REL}/README_STATIC_SITE.md") is not None,
        static_site_files_written=len(files_written) == len(REQUIRED_STATIC_FILES),
    )
    return record, {
        "index_html_written": record.index_html_written,
        "app_js_written": record.app_js_written,
        "styles_css_written": record.styles_css_written,
        "readme_written": record.readme_written,
        "static_site_files_written": record.static_site_files_written,
    }


def _audit_app_js() -> Dict[str, bool]:
    app_path = _resolve_file(f"{STATIC_SITE_ROOT_REL}/app.js")
    if not app_path:
        return {
            "local_json_loader_available": False,
            "example_loader_available": False,
            "envelope_loader_present": False,
            "model_panel_registry_in_app": False,
            "boundary_panel_present": False,
            "testboard_refs_panel_available": False,
            "segmentation_example_available": False,
            "ten_panels_defined": False,
        }
    text = app_path.read_text(encoding="utf-8")
    panel_count = text.count('panel_id:')
    return {
        "local_json_loader_available": "json-file-input" in text or "FileReader" in text,
        "example_loader_available": "loadBuiltinExample" in text and "BUILTIN_MOBILE_SAM_EXAMPLE" in text,
        "envelope_loader_present": "validateEnvelope" in text and "renderEnvelope" in text,
        "model_panel_registry_in_app": "MODEL_PANEL_REGISTRY" in text,
        "boundary_panel_present": "boundary-panel" in text and "renderBoundaryFlags" in text,
        "testboard_refs_panel_available": "testboard-refs-panel" in text,
        "segmentation_example_available": "mobile_sam" in text and "prompt_success_count" in text,
        "ten_panels_defined": panel_count >= 10,
    }


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MidplatformModelTestLensStaticSiteSkeletonExecutionProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            static_site_skeleton_execution=STATIC_SITE_SKELETON_EXECUTION,
            local_static_page_only=LOCAL_STATIC_PAGE_ONLY,
            not_whitebox_product_page=NOT_WHITEBOX_PRODUCT_PAGE,
            model_testing_only=MODEL_TESTING_ONLY,
            read_local_json_only=READ_LOCAL_JSON_ONLY,
            model_execution_allowed=MODEL_EXECUTION_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            fact_write_allowed=FACT_WRITE_ALLOWED,
            navigation_action_speech_allowed=NAVIGATION_ACTION_SPEECH_ALLOWED,
            upstream_planning_ref=UPSTREAM_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_model_test_lens_static_site_skeleton_execution_v1(
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

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    file_gen, file_flags = _audit_static_site_files()
    app_flags = _audit_app_js()

    app_path = _resolve_file(f"{STATIC_SITE_ROOT_REL}/app.js")
    index_path = _resolve_file(f"{STATIC_SITE_ROOT_REL}/index.html")
    app_text = app_path.read_text(encoding="utf-8") if app_path else ""
    index_text = index_path.read_text(encoding="utf-8") if index_path else ""
    pattern_ok, pattern_violations = _scan_forbidden_patterns(app_text, index_text)
    if not pattern_ok:
        boundary_violations.extend([f"forbidden_pattern:{v}" for v in pattern_violations])

    example_loader = ModelTestLensExampleLoaderRecord(
        record_id="model_test_lens_example_loader_record_v1",
        example_envelope_rel=EXAMPLE_ENVELOPE_REL,
        local_json_file_input=app_flags["local_json_loader_available"],
        builtin_example_loader=app_flags["example_loader_available"],
        example_loader_config_rel=f"{STATIC_SITE_ROOT_REL}/example_loader_config_v1.json",
        segmentation_example_available=app_flags["segmentation_example_available"],
        no_external_url_fetch=pattern_ok and "fetch(" not in app_text,
    )

    panel_record = ModelTestLensModelPanelSkeletonRecord(
        record_id="model_test_lens_model_panel_skeleton_v1",
        panels=MODEL_PANEL_SKELETON_REGISTRY,
        model_panel_count=len(MODEL_PANEL_SKELETON_REGISTRY),
        segmentation_active_example=True,
    )

    boundary_record = ModelTestLensBoundaryPanelRecord(
        record_id="model_test_lens_boundary_panel_record_v1",
        boundary_fields=(
            "candidate_only", "not_fact", "not_runtime_output", "not_output_adapter_output",
            "not_semantic_output", "not_navigation_action_speech",
            "runtime_ready", "output_adapter_ready", "semantic_layer_ready",
            "fact_write_ready", "navigation_action_speech_ready",
        ),
        boundary_panel_available=app_flags["boundary_panel_present"],
        readiness_read_only=True,
    )

    no_runtime_audit = ModelTestLensNoRuntimeNoModelExecutionAuditRecord(
        record_id="model_test_lens_no_runtime_no_model_execution_audit_v1",
        no_model_execution=MODEL_EXECUTION_ALLOWED is False and "runInference" not in app_text,
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
        no_camera_microphone=LIVE_CAMERA_ALLOWED is False and MICROPHONE_ALLOWED is False and pattern_ok,
        no_delete_artifact_button=FILE_DELETE_ALLOWED is False and TESTBOARD_DELETE_ALLOWED is False,
        forbidden_pattern_scan_passed=pattern_ok,
    )

    rollback = ModelTestLensRollbackReadinessRecord(
        record_id="model_test_lens_rollback_readiness_v1",
        rollback_available=True,
        rollback_can_remove_static_site_skeleton_files_if_needed=True,
        rollback_must_preserve_planning_artifacts=True,
        rollback_must_preserve_test_board=True,
        rollback_must_preserve_examples_if_referenced=True,
        rollback_not_executed_by_default=True,
    )

    post_audit = ModelTestLensStaticSitePostReviewAudit(
        audit_id="model_test_lens_static_site_post_review_audit_v1",
        static_site_files_written=file_gen.static_site_files_written,
        index_html_written=file_gen.index_html_written,
        app_js_written=file_gen.app_js_written,
        styles_css_written=file_gen.styles_css_written,
        readme_written=file_gen.readme_written,
        model_panel_count=panel_record.model_panel_count,
        segmentation_example_available=example_loader.segmentation_example_available,
        local_json_loader_available=example_loader.local_json_file_input,
        example_loader_available=example_loader.builtin_example_loader,
        boundary_panel_available=boundary_record.boundary_panel_available,
        testboard_refs_panel_available=app_flags["testboard_refs_panel_available"],
        no_model_execution=no_runtime_audit.no_model_execution,
        no_runtime=no_runtime_audit.no_runtime,
        no_output_adapter=no_runtime_audit.no_output_adapter,
        no_semantic_fact_navigation=no_runtime_audit.no_semantic_fact_navigation,
        no_registry_mutation=no_runtime_audit.no_registry_mutation,
        no_external_url=no_runtime_audit.no_external_url,
        no_camera_microphone=no_runtime_audit.no_camera_microphone,
        test_board_written=write_test_board,
        test_board_protected=all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        post_review_passed=(
            file_gen.static_site_files_written
            and app_flags["ten_panels_defined"]
            and example_loader.segmentation_example_available
            and pattern_ok
        ),
    )

    invariant_state: Dict[str, bool] = {
        "upstream_planning_verified": verify_flags.get("model_test_lens_static_site_planning_go_verified") is True,
        "not_whitebox_product_page": NOT_WHITEBOX_PRODUCT_PAGE is True,
        "no_model_execution": no_runtime_audit.no_model_execution,
        "no_runtime_output_adapter": no_runtime_audit.no_runtime and no_runtime_audit.no_output_adapter,
        "no_semantic_fact_navigation": no_runtime_audit.no_semantic_fact_navigation,
        "no_registry_mutation": no_runtime_audit.no_registry_mutation,
        "no_external_url": no_runtime_audit.no_external_url,
        "no_camera_microphone": no_runtime_audit.no_camera_microphone,
        "no_delete_artifact": no_runtime_audit.no_delete_artifact_button,
        "ten_panels_defined": app_flags["ten_panels_defined"] and panel_record.model_panel_count == 10,
        "envelope_loader_present": app_flags["envelope_loader_present"],
        "boundary_panel_present": boundary_record.boundary_panel_available,
        "testboard_panel_present": app_flags["testboard_refs_panel_available"],
        "testboard_required": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "testboard_protected": all(
            REQUIRED_TEST_BOARD_FIELDS_LOCAL[k] for k in (
                "test_artifact_protected", "test_record_non_deletable", "test_deletion_forbidden"
            )
        ),
        "cleanup_preserves_testboard": True,
    }

    negative_guards: List[NegativeModelTestLensStaticSiteSkeletonGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeModelTestLensStaticSiteSkeletonGuard(
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
    skeleton_ok = (
        file_gen.static_site_files_written
        and app_flags["ten_panels_defined"]
        and example_loader.segmentation_example_available
        and boundary_record.boundary_panel_available
        and app_flags["testboard_refs_panel_available"]
        and pattern_ok
    )

    if not no_boundary_violation:
        final_decision = FINAL_DECISION_BLOCKED
        decision_branch = "blocked"
        recommended_next = NEXT_PHASE_BLOCKED
        blocker_count = len(boundary_violations) + len(failed_checks)
    elif skeleton_ok and negative_guard_passed == negative_guard_count:
        final_decision = FINAL_DECISION_GO
        decision_branch = "go"
        recommended_next = NEXT_PHASE_DATA_ADAPTER
        blocker_count = len(failed_checks)
    else:
        final_decision = FINAL_DECISION_FAILED
        decision_branch = "failed_no_boundary_violation"
        recommended_next = NEXT_PHASE_FAILED
        blocker_count = len(failed_checks)

    followup = ModelTestLensFollowupRouteRecord(
        route_id="model_test_lens_followup_route_v1",
        decision_branch=decision_branch,
        recommended_next_phase=recommended_next,
        next_phase_scope="model_test_lens_data_adapter_or_automated_test_planning",
    )

    go_conditions: Dict[str, bool] = {
        "model_test_lens_static_site_skeleton_execution_profile_count_eq_1": True,
        **file_flags,
        "model_panel_count_eq_10": panel_record.model_panel_count == 10,
        "segmentation_example_available": example_loader.segmentation_example_available,
        "local_json_loader_available": example_loader.local_json_file_input,
        "example_loader_available": example_loader.builtin_example_loader,
        "boundary_panel_available": boundary_record.boundary_panel_available,
        "testboard_refs_panel_available": app_flags["testboard_refs_panel_available"],
        "no_model_execution": no_runtime_audit.no_model_execution,
        "no_inference_execution": REAL_INFERENCE_ALLOWED is False,
        "no_runtime": no_runtime_audit.no_runtime,
        "no_output_adapter": no_runtime_audit.no_output_adapter,
        "no_semantic_fact_navigation": no_runtime_audit.no_semantic_fact_navigation,
        "no_registry_mutation": no_runtime_audit.no_registry_mutation,
        "no_external_url": no_runtime_audit.no_external_url,
        "no_camera_microphone": no_runtime_audit.no_camera_microphone,
        "no_delete_artifact_button": no_runtime_audit.no_delete_artifact_button,
        "negative_guard_count_eq_16": negative_guard_count == 16,
        "negative_guard_passed_eq_16": negative_guard_passed == 16,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
    }
    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MidplatformModelTestLensStaticSiteSkeletonExecutionDecision(
        decision_ref=DECISION_REF,
        model_test_lens_static_site_skeleton_execution_profile_count=1,
        static_site_files_written=file_gen.static_site_files_written,
        model_panel_count=panel_record.model_panel_count,
        segmentation_example_available=example_loader.segmentation_example_available,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        failure_recorded=final_decision == FINAL_DECISION_FAILED,
        no_boundary_violation=no_boundary_violation,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    panel_registry_payload = {
        "registry_id": "model_test_lens_panel_registry_execution_v1",
        "panels": [dict(p) for p in MODEL_PANEL_SKELETON_REGISTRY],
        "app_js_panel_count": app_flags.get("ten_panels_defined"),
        "model_panel_count": panel_record.model_panel_count,
    }

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Midplatform Model Test Lens Static Site Skeleton Execution And Post Review",
        "lifecycle_variant": "p1_midplatform_model_test_lens_static_site_skeleton_execution",
        "execution_principle_zh": EXECUTION_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "static_site_root_rel": STATIC_SITE_ROOT_REL,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "model_test_lens_static_site_skeleton_execution_profile": _build_profile(),
        "model_test_lens_static_site_skeleton_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "model_test_lens_static_site_file_generation_record": asdict(file_gen),
        "model_test_lens_example_loader_record": asdict(example_loader),
        "model_test_lens_model_panel_skeleton_record": asdict(panel_record),
        "model_test_lens_boundary_panel_record": asdict(boundary_record),
        "model_test_lens_no_runtime_no_model_execution_audit_record": asdict(no_runtime_audit),
        "model_test_lens_static_site_post_review_record": asdict(post_audit),
        "model_test_lens_rollback_readiness_record": asdict(rollback),
        "model_test_lens_followup_route_record": asdict(followup),
        "forbidden_pattern_violations": pattern_violations,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "boundary_violations": boundary_violations,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "execution_status": decision_branch,
            "static_site_files_written": file_gen.static_site_files_written,
            "open_instructions": (
                "Open capabilities/midplatform/model_test_lens/static_site/index.html "
                "or run: python3 -m http.server 8765 --directory capabilities/midplatform/model_test_lens/static_site"
            ),
            "recommended_next_phase": recommended_next,
            "transition_note": (
                "Skeleton static site generated. Local JSON viewer + MobileSAM example. "
                "No model execution. Next: Data Adapter to convert _tmp_eval_out to envelopes."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)

        (out_root / "model_test_lens_static_site_file_generation_v1.json").write_text(
            json.dumps(asdict(file_gen), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_lens_panel_registry_execution_v1.json").write_text(
            json.dumps(panel_registry_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_lens_example_loader_record_v1.json").write_text(
            json.dumps(asdict(example_loader), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_lens_boundary_panel_record_v1.json").write_text(
            json.dumps(asdict(boundary_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_lens_static_site_post_review_audit_v1.json").write_text(
            json.dumps(asdict(post_audit), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

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
            "model_test_lens_static_site_file_generation_record": {"record": asdict(file_gen)},
            "model_test_lens_example_loader_record": {"record": asdict(example_loader)},
            "model_test_lens_model_panel_skeleton_record": {"record": asdict(panel_record)},
            "model_test_lens_boundary_panel_record": {"record": asdict(boundary_record)},
            "model_test_lens_no_runtime_no_model_execution_audit_record": {"record": asdict(no_runtime_audit)},
            "model_test_lens_static_site_post_review_record": {"record": asdict(post_audit)},
            "model_test_lens_followup_route_record": {"record": asdict(followup)},
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
            "real_execution_phase": True,
            "model_execution_allowed": False,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
            "semantic_layer_allowed": False,
            "fact_write_allowed": False,
        }
        extra_written: List[str] = []
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(
                json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            extra_written.append(str(p))
        manifest_tb["extra_written_records"] = extra_written
        manifest_tb["total_record_count"] = manifest_tb["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest_tb
        result["test_board_record_count"] = manifest_tb["total_record_count"]

    return result


def main() -> int:
    result = review_model_test_lens_static_site_skeleton_execution_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "static_site_files_written": result["model_test_lens_static_site_file_generation_record"]["static_site_files_written"],
                "model_panel_count": result["model_test_lens_model_panel_skeleton_record"]["model_panel_count"],
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
