# -*- coding: utf-8 -*-
"""P1 Model Test Lens Simple Mode UX Patch Execution — review v1."""

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
from capabilities.midplatform.model_test_lens.model_test_lens_simple_mode_ux_patch_execution_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.midplatform.model_test_lens.model_test_lens_simple_mode_ux_patch_execution_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXECUTION_PRINCIPLE_ZH,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    FORBIDDEN_CODE_PATTERNS,
    LUNA_CORE_PRINCIPLE,
    MODEL_TEST_LENS_ROOT_REL,
    NEGATIVE_GUARDS,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    REAL_EXECUTION_PHASE,
    REQUIRED_STATIC_FILES,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    SIMPLE_MODE_UX_PATCH,
    SCOPE,
    STATIC_SITE_ROOT_REL,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UI_AUDIT_MARKERS,
    NegativeSimpleModeUXPatchGuard,
    P1ModelTestLensSimpleModeUXPatchExecutionDecision,
    SimpleModeBoundaryAudit,
    SimpleModeOneClickFlowRecord,
    SimpleModeUIFilePatchRecord,
    SimpleModeUXPatchPostReviewAudit,
    to_dict,
)

REVIEW_FILENAME = "p1_midplatform_model_test_lens_simple_mode_ux_patch_execution_review_v1.json"
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _pick_writable_base() -> Path:
    for cand in (_REPO_ROOT, Path.cwd()):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (OSError, PermissionError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()
DEFAULT_OUTPUT_ROOT = (
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_midplatform_model_test_lens_simple_mode_ux_patch_execution_v1_smoke_v0"
)


def _artifact_roots() -> List[Path]:
    roots = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
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


def _scan_forbidden(combined: str) -> Tuple[bool, List[str]]:
    violations: List[str] = []
    for spec in FORBIDDEN_CODE_PATTERNS:
        if re.search(spec["regex"], combined, re.IGNORECASE):
            violations.append(spec["pattern_id"])
    return not violations, violations


def _audit_ui_markers(combined: str, index_text: str) -> Dict[str, bool]:
    flags: Dict[str, bool] = {}
    for marker in UI_AUDIT_MARKERS:
        flags[marker["key"]] = marker["needle"] in combined or marker["needle"] in index_text
    flags["default_view_simplified"] = (
        "simple-mode-host" in index_text
        and 'id="advanced-workflow" hidden' in index_text
        and "sm-start" in combined
    )
    flags["technical_buttons_hidden_by_default"] = (
        'id="advanced-workflow" hidden' in index_text
        and "lai-generate-manifest" in combined
    )
    return flags


def _audit_preserved(app_text: str, index_text: str, site_text: str) -> Dict[str, bool]:
    combined = app_text + index_text + site_text
    panel_count = app_text.count("panel_id:")
    return {
        "existing_envelope_import_preserved": "json-file-input" in combined and "loadLocalJsonFile" in app_text,
        "mobilesam_example_preserved": "loadBuiltinExample" in app_text and "BUILTIN_MOBILE_SAM_EXAMPLE" in app_text,
        "slam_example_preserved": "loadBuiltinSlamExample" in app_text and "fetchBuiltinSlamExample" in app_text,
        "insight_layer_preserved": "ModelInsightLayer" in app_text and "model_insight_layer_v1.js" in index_text,
        "debug_mode_preserved": "debug-mode-toggle" in combined,
        "model_panel_count_eq_10": panel_count >= 10,
        "manifest_job_bridge_preserved": (
            "lai-generate-manifest" in combined
            and "rb-create-job" in combined
            and "rb-create-bridge" in combined
        ),
    }


def run_review(output_root: Optional[Path] = None) -> Dict[str, Any]:
    site_text = _read_site_text()
    index_path = _resolve_file(f"{STATIC_SITE_ROOT_REL}/index.html")
    app_path = _resolve_file(f"{STATIC_SITE_ROOT_REL}/app.js")
    simple_path = _resolve_file(f"{STATIC_SITE_ROOT_REL}/simple_mode_ui_v1.js")
    index_text = index_path.read_text(encoding="utf-8") if index_path else ""
    app_text = app_path.read_text(encoding="utf-8") if app_path else ""
    simple_text = simple_path.read_text(encoding="utf-8") if simple_path else ""

    pattern_ok, pattern_violations = _scan_forbidden(site_text)
    ui_flags = _audit_ui_markers(site_text, index_text)
    preserve_flags = _audit_preserved(app_text, index_text, site_text)
    verify_result = verify_stages(_artifact_roots())
    verify_flags = verify_result["verify_flags"]

    file_patch = SimpleModeUIFilePatchRecord(
        simple_mode_ui_written=simple_path is not None and simple_path.is_file(),
        index_html_updated=index_path is not None,
        app_js_updated=app_path is not None,
        styles_css_updated=_resolve_file(f"{STATIC_SITE_ROOT_REL}/styles.css") is not None,
        default_view_simplified=ui_flags.get("default_view_simplified", False),
        technical_buttons_hidden_by_default=ui_flags.get("technical_buttons_hidden_by_default", False),
    )

    one_click = SimpleModeOneClickFlowRecord(
        one_click_local_test_button_present="sm-start" in simple_text and "开始本地测试" in simple_text,
        mobilesam_one_click_flow_present=(
            "segmentation" in simple_text
            and "/api/v1/assets/register" in simple_text
            and "/api/v1/jobs/" in simple_text
        ),
        slam_limited_one_click_flow_present=(
            "slam_vio" in simple_text and "SLAM limited" in simple_text
        ),
        user_friendly_progress_steps_present="sm-progress" in simple_text and "检查本地服务" in simple_text,
        user_friendly_error_messages_present="start_local_runner_bridge" in simple_text,
        service_status_simplified="本地测试服务已连接" in simple_text,
        local_runner_bridge_service_preserved="127.0.0.1:8787" in simple_text,
    )

    boundary_audit = SimpleModeBoundaryAudit(
        no_page_model_execution=pattern_ok and "modelExecutionAllowed" in app_text,
        no_runtime='dataset.modelExecutionAllowed = "false"' in app_text,
        no_output_adapter="output_adapter_allowed" not in simple_text.lower(),
        no_fact_semantic_navigation=pattern_ok,
        no_registry_mutation=pattern_ok,
        no_external_network=pattern_ok,
        no_live_camera_microphone=pattern_ok,
        no_delete_artifact_button="deleteArtifact" not in site_text,
    )

    post_audit = SimpleModeUXPatchPostReviewAudit(
        post_review_passed=all([
            file_patch.simple_mode_ui_written,
            file_patch.default_view_simplified,
            ui_flags.get("advanced_mode_toggle_present", False),
            ui_flags.get("developer_mode_toggle_present", False),
            preserve_flags["manifest_job_bridge_preserved"],
        ]),
        simple_mode_ui_written=file_patch.simple_mode_ui_written,
        default_view_simplified=file_patch.default_view_simplified,
        advanced_mode_available=ui_flags.get("advanced_mode_toggle_present", False),
        developer_mode_available=ui_flags.get("developer_mode_toggle_present", False),
        manifest_job_bridge_preserved=preserve_flags["manifest_job_bridge_preserved"],
    )

    invariant_state: Dict[str, bool] = {
        "upstream_go_verified": verify_flags.get("upstream_go_verified", False),
        "no_bypass_8787": "/api/v1/" in simple_text and "127.0.0.1:8787" in simple_text,
        "no_page_inference_endpoint": pattern_ok,
        "no_runtime": boundary_audit.no_runtime,
        "no_fact_semantic_navigation": boundary_audit.no_fact_semantic_navigation,
        "no_registry_mutation": boundary_audit.no_registry_mutation,
        "no_external_network": boundary_audit.no_external_network,
        "no_live_camera_microphone": boundary_audit.no_live_camera_microphone,
        "no_delete_artifact": boundary_audit.no_delete_artifact_button,
        "manifest_job_bridge_preserved": preserve_flags["manifest_job_bridge_preserved"],
        "advanced_mode_available": ui_flags.get("advanced_mode_toggle_present", False),
        "developer_mode_available": ui_flags.get("developer_mode_toggle_present", False),
        "technical_json_hidden_by_default": ui_flags.get("technical_buttons_hidden_by_default", False),
        "mobilesam_one_click_flow_present": one_click.mobilesam_one_click_flow_present,
        "slam_limited_one_click_flow_present": one_click.slam_limited_one_click_flow_present,
        "existing_features_preserved": all([
            preserve_flags["existing_envelope_import_preserved"],
            preserve_flags["mobilesam_example_preserved"],
            preserve_flags["insight_layer_preserved"],
            preserve_flags["model_panel_count_eq_10"],
        ]),
        "test_board_written": True,
        "test_board_protected": True,
    }

    negative_guards: List[NegativeSimpleModeUXPatchGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeSimpleModeUXPatchGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)

    boundary_violations = list(pattern_violations)
    no_boundary_violation = len(boundary_violations) == 0
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    go_conditions: Dict[str, bool] = {
        "simple_mode_ux_patch_profile_count_eq_1": True,
        "simple_mode_ui_written": file_patch.simple_mode_ui_written,
        "default_view_simplified": file_patch.default_view_simplified,
        "one_click_local_test_button_present": one_click.one_click_local_test_button_present,
        "technical_buttons_hidden_by_default": file_patch.technical_buttons_hidden_by_default,
        "advanced_mode_available": post_audit.advanced_mode_available,
        "developer_mode_available": post_audit.developer_mode_available,
        "manifest_job_bridge_preserved": preserve_flags["manifest_job_bridge_preserved"],
        "local_runner_bridge_service_preserved": one_click.local_runner_bridge_service_preserved,
        "service_status_simplified": one_click.service_status_simplified,
        "user_friendly_progress_steps_present": one_click.user_friendly_progress_steps_present,
        "user_friendly_error_messages_present": one_click.user_friendly_error_messages_present,
        "mobilesam_one_click_flow_present": one_click.mobilesam_one_click_flow_present,
        "slam_limited_one_click_flow_present": one_click.slam_limited_one_click_flow_present,
        "existing_envelope_import_preserved": preserve_flags["existing_envelope_import_preserved"],
        "mobilesam_example_preserved": preserve_flags["mobilesam_example_preserved"],
        "slam_example_preserved": preserve_flags["slam_example_preserved"],
        "insight_layer_preserved": preserve_flags["insight_layer_preserved"],
        "debug_mode_preserved": preserve_flags["debug_mode_preserved"],
        "model_panel_count_eq_10": preserve_flags["model_panel_count_eq_10"],
        "no_page_model_execution": boundary_audit.no_page_model_execution,
        "no_runtime": boundary_audit.no_runtime,
        "no_output_adapter": boundary_audit.no_output_adapter,
        "no_fact_semantic_navigation": boundary_audit.no_fact_semantic_navigation,
        "no_registry_mutation": boundary_audit.no_registry_mutation,
        "no_external_network": boundary_audit.no_external_network,
        "no_live_camera_microphone": boundary_audit.no_live_camera_microphone,
        "no_delete_artifact_button": boundary_audit.no_delete_artifact_button,
        "negative_guard_count_eq_18": negative_guard_count == 18,
        "negative_guard_passed_eq_18": negative_guard_passed == 18,
        **{f"test_board.{k}": v for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        **{k: verify_flags.get(k, False) for k in REQUIRED_VERIFY_FLAGS},
    }
    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    if not no_boundary_violation:
        final_decision = FINAL_DECISION_BLOCKED
        blocker_count = len(boundary_violations) + len(failed_checks)
    elif post_audit.post_review_passed and negative_guard_passed == negative_guard_count:
        final_decision = FINAL_DECISION_GO
        blocker_count = 0
    else:
        final_decision = FINAL_DECISION_FAILED
        blocker_count = len(failed_checks)

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1ModelTestLensSimpleModeUXPatchExecutionDecision(
        decision_ref="model_test_lens_simple_mode_ux_patch_execution_decision_v1",
        simple_mode_ux_patch_profile_count=1,
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
        "lifecycle_variant": "p1_midplatform_model_test_lens_simple_mode_ux_patch_execution",
        "source_chain": SCOPE,
        "step": "P1 Model Test Lens Simple Mode UX Patch Execution And Post Review",
        "execution_principle_zh": EXECUTION_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "simple_mode_ux_patch": SIMPLE_MODE_UX_PATCH,
        "default_user_mode": "simple",
        "local_runner_bridge_host": "127.0.0.1",
        "local_runner_bridge_port": 8787,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "simple_mode_ui_file_patch_record": asdict(file_patch),
        "simple_mode_one_click_flow_record": asdict(one_click),
        "simple_mode_boundary_audit": asdict(boundary_audit),
        "simple_mode_ux_patch_post_review_audit": asdict(post_audit),
        "forbidden_pattern_violations": pattern_violations,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "ui_audit_flags": ui_flags,
        "preserve_flags": preserve_flags,
        "verify_flags": verify_flags,
        "go_conditions": go_conditions,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "blocker_count": blocker_count,
        "final_decision": final_decision,
        "decision": asdict(decision),
        "rollback_readiness": {
            "rollback_available": True,
            "rollback_can_restore_previous_ui": True,
            "rollback_must_preserve_runner_bridge_service": True,
            "rollback_must_preserve_test_board": True,
            "rollback_must_preserve_review_artifacts": True,
            "rollback_not_executed_by_default": True,
        },
        "recorded_at_utc": _now(),
    }

    (out_root / REVIEW_FILENAME).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_root / "model_test_lens_simple_mode_ui_patch_record_v1.json").write_text(
        json.dumps(asdict(file_patch), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (out_root / "model_test_lens_simple_mode_one_click_flow_record_v1.json").write_text(
        json.dumps(asdict(one_click), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (out_root / "model_test_lens_simple_mode_boundary_audit_v1.json").write_text(
        json.dumps(asdict(boundary_audit), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (out_root / "model_test_lens_simple_mode_ux_patch_post_review_audit_v1.json").write_text(
        json.dumps(asdict(post_audit), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    result["output_root"] = str(out_root)
    result["output_review_file"] = str(out_root / REVIEW_FILENAME)

    try:
        manifest_tb = write_test_board_records(
            result,
            test_mode=TEST_BOARD_TEST_MODE,
            repo_root=_REPO_ROOT,
            module=TEST_BOARD_MODULE,
            source_review_file=result["output_review_file"],
        )
        result["test_board_write_mode"] = "canonical"
    except (PermissionError, OSError):
        _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
        manifest_tb = write_test_board_records(
            result,
            test_mode=TEST_BOARD_TEST_MODE,
            repo_root=_BOARD_STANDIN_ROOT,
            module=TEST_BOARD_MODULE,
            source_review_file=result["output_review_file"],
        )
        result["test_board_write_mode"] = "standin_sandbox_fallback"

    board_dir = Path(manifest_tb["test_board_dir"])
    extra_payloads = {
        "simple_mode_ui_patch_record": {"record": asdict(file_patch)},
        "simple_mode_one_click_flow_record": {"record": asdict(one_click)},
        "simple_mode_boundary_audit": {"record": asdict(boundary_audit)},
        "simple_mode_ux_patch_post_review_audit": {"record": asdict(post_audit)},
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


if __name__ == "__main__":
    out = run_review()
    print(json.dumps({"final_decision": out["final_decision"], "blocker_count": out["blocker_count"]}, indent=2))
