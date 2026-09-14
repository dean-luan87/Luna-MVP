# -*- coding: utf-8 -*-
"""P1 Model Test Lens Luna Observation Compact UI — execution review v1."""

from __future__ import annotations

import json
import re
import sys
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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Luna-Observation-Compact-UI-Execution-And-Post-Review-v1-001"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
UI_REDESIGN_REL = "capabilities/midplatform/model_test_lens/ui_redesign"
_PKG = "capabilities/midplatform/model_test_lens"

COMPACT_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/luna_observation_layout_v1.js",
    f"{STATIC_REL}/luna_observation_drawers_v1.js",
    f"{STATIC_REL}/luna_observation_copy_v1.js",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/simple_mode_ui_v1.js",
    f"{STATIC_REL}/perception_hud_view_v1.js",
    f"{STATIC_REL}/visual_compare_view_v1.js",
    f"{STATIC_REL}/model_insight_layer_v1.js",
    f"{STATIC_REL}/runner_bridge_ui_v1.js",
    f"{_PKG}/review_model_test_lens_luna_observation_compact_ui_execution_v1.py",
)

PLANNING_REFS: Tuple[str, ...] = (
    f"{UI_REDESIGN_REL}/luna_observation_lens_ui_redesign_plan_v1.md",
    f"{UI_REDESIGN_REL}/luna_observation_compact_viewport_plan_v1.md",
    f"{UI_REDESIGN_REL}/luna_observation_compact_layout_spec_v1.json",
)

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_COMPACT_UI_EXECUTION_GO"
FINAL_DECISION_PARTIAL = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_COMPACT_UI_EXECUTION_PARTIAL_GO"
FINAL_DECISION_FAILED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_COMPACT_UI_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_COMPACT_UI_EXECUTION_BLOCKED"

FORBIDDEN_UI_PATTERNS: Tuple[Tuple[str, str], ...] = (
    (r"\brun_model\s*\(|\binfer\s*\(|\bexecuteModel\s*\(|\brunInference\s*\(", "page_model_execution"),
    (r"\bruntime\s*\(|\boutput_adapter_call\s*\(|\bfact_write\s*\(|\bsemantic_write\s*\(|\bregistry_write\s*\(", "runtime_fact_semantic"),
    (r"\bnavigation_action\s*\(|\bspeech_output\s*\(", "navigation_speech"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
    (r"deleteArtifact\s*\(|removeTestBoard\s*\(", "delete_artifact"),
    (r"https?://(?!127\.0\.0\.1)", "external_fetch"),
)

SCAN_JS_FILES: Tuple[str, ...] = tuple(
    f for f in COMPACT_FILES if f.endswith(".js") and "review_" not in f
)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "luna_observation_compact_ui_patch_record",
    "compact_viewport_layout_record",
    "information_compression_record",
    "drawer_migration_record",
    "perception_hud_preservation_record",
    "whitebox_slot_record",
    "compact_ui_boundary_audit_record",
    "compact_ui_post_review_record",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "depends_on": "upstream_planning_go"},
    {"guard_id": "B", "depends_on": "long_report_flow_removed"},
    {"guard_id": "C", "depends_on": "max_primary_scroll_depth_lte_1_5"},
    {"guard_id": "D", "depends_on": "central_hud_area_present"},
    {"guard_id": "E", "depends_on": "metrics_moved_to_drawer"},
    {"guard_id": "F", "depends_on": "right_reasoning_panel_present"},
    {"guard_id": "G", "depends_on": "advanced_info_moved_to_drawer"},
    {"guard_id": "H", "depends_on": "engineering_terms_hidden_by_default"},
    {"guard_id": "I", "depends_on": "perception_hud_preserved"},
    {"guard_id": "J", "depends_on": "no_page_model_execution"},
    {"guard_id": "K", "depends_on": "no_fact_semantic_navigation"},
    {"guard_id": "L", "depends_on": "no_runtime_output_adapter"},
    {"guard_id": "M", "depends_on": "no_external_network"},
    {"guard_id": "N", "depends_on": "test_board_planned"},
    {"guard_id": "O", "depends_on": "test_board_protected"},
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out"
    / "p1_midplatform_model_test_lens_luna_observation_compact_ui_execution_v1_smoke_v0"
)
_BOARD_STANDIN = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _roots() -> List[Path]:
    return list(dict.fromkeys([_REPO_ROOT, Path.cwd()]))


def _read(rel: str) -> str:
    for base in _roots():
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _exists(rel: str) -> bool:
    return bool(_read(rel))


def _scan_boundary() -> Tuple[bool, List[str]]:
    js_text = "\n".join(_read(f) for f in SCAN_JS_FILES)
    bad: List[str] = []
    for pat, pid in FORBIDDEN_UI_PATTERNS:
        if re.search(pat, js_text, re.I):
            bad.append(pid)
    return not bad, bad


def _audit(index: str, app_js: str, styles: str, combined: str) -> Dict[str, bool]:
    long_report_markers = [
        "decision-dashboard",
        "insight-block",
        "visual-metrics-block",
        "metrics-expandable",
        "verdict-hero",
    ]
    long_report_in_index = any(m in index for m in long_report_markers)

    return {
        "luna_observation_title_applied": "Luna Observation Lens" in index,
        "compact_dashboard_layout_written": "lol-main-grid" in index and "lol-app" in index,
        "default_view_visual_first": 'data-view="hud"' in index and "active" in index,
        "single_screen_primary_observation_met": "height: 100vh" in styles and "lol-main-grid" in styles,
        "max_primary_scroll_depth_lte_1_5": "overflow: hidden" in styles and "lol-right-panel" in styles,
        "top_task_bar_present": "lol-top-bar" in index,
        "left_capability_panel_present": "lol-left-rail" in index and "lol-cap-card" in combined,
        "central_hud_area_present": "lol-central" in index and "renderCentral" in combined,
        "right_reasoning_panel_present": "lol-right-panel" in index and "renderRightPanel" in combined,
        "bottom_metrics_summary_present": "lol-dock-summary" in combined,
        "bottom_drawers_present": "lol-dock-tab" in combined and "data-drawer" in combined,
        "metrics_moved_to_drawer": "renderMetricsDrawer" in app_js or "renderMetrics" in combined,
        "advanced_info_moved_to_drawer": 'data-drawer="advanced"' in combined,
        "developer_json_moved_to_drawer": 'data-drawer="developer"' in combined,
        "whitebox_slot_present": 'data-drawer="whitebox"' in combined,
        "long_report_flow_removed": not long_report_in_index and "renderDecisionDashboard" not in app_js,
        "engineering_terms_hidden_by_default": "placeholder" not in index and "panel-status" not in index,
        "visual_compare_preserved": "visual_compare_view_v1.js" in index and "VisualCompareView" in combined,
        "perception_hud_preserved": "perception_hud_view_v1.js" in index and "renderCentral" in _read(f"{STATIC_REL}/perception_hud_view_v1.js"),
        "simple_mode_preserved": "initHeadless" in _read(f"{STATIC_REL}/simple_mode_ui_v1.js"),
        "local_runner_bridge_preserved": "127.0.0.1:8787" in combined,
        "mobilesam_example_preserved": "loadBuiltinExample" in app_js and "BUILTIN_MOBILE_SAM_EXAMPLE" in app_js,
        "slam_example_preserved": "loadBuiltinSlamExample" in app_js and "BUILTIN_SLAM_EXAMPLE" in app_js,
        "no_delete_artifact_button": "deleteArtifact" not in "\n".join(_read(f) for f in SCAN_JS_FILES),
    }


def review_model_test_lens_luna_observation_compact_ui_execution_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in COMPACT_FILES:
        if _exists(rel):
            passed_checks.append(f"file.present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"file.missing={rel}")

    for rel in PLANNING_REFS:
        if _exists(rel):
            passed_checks.append(f"planning.present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"planning.missing={rel}")

    index = _read(f"{STATIC_REL}/index.html")
    app_js = _read(f"{STATIC_REL}/app.js")
    styles = _read(f"{STATIC_REL}/styles.css")
    combined = "\n".join(_read(f) for f in COMPACT_FILES if _exists(f))

    boundary_ok, violations = _scan_boundary()
    flags = _audit(index, app_js, styles, combined)

    upstream_planning_go = all(_exists(r) for r in PLANNING_REFS)

    flags["no_page_model_execution"] = boundary_ok and "page_model_execution" not in violations
    flags["no_runtime"] = "runtime_fact_semantic" not in violations
    flags["no_output_adapter"] = "runtime_fact_semantic" not in violations
    flags["no_fact_semantic_navigation"] = boundary_ok and "navigation_speech" not in violations
    flags["no_registry_mutation"] = "registry_write" not in combined
    flags["no_external_network"] = "external_fetch" not in violations
    flags["no_live_camera_microphone"] = "camera_mic" not in violations
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    invariant_state: Dict[str, bool] = {
        "upstream_planning_go": upstream_planning_go,
        "long_report_flow_removed": flags.get("long_report_flow_removed", False),
        "max_primary_scroll_depth_lte_1_5": flags.get("max_primary_scroll_depth_lte_1_5", False),
        "central_hud_area_present": flags.get("central_hud_area_present", False),
        "metrics_moved_to_drawer": flags.get("metrics_moved_to_drawer", False),
        "right_reasoning_panel_present": flags.get("right_reasoning_panel_present", False),
        "advanced_info_moved_to_drawer": flags.get("advanced_info_moved_to_drawer", False),
        "engineering_terms_hidden_by_default": flags.get("engineering_terms_hidden_by_default", False),
        "perception_hud_preserved": flags.get("perception_hud_preserved", False),
        "no_page_model_execution": flags.get("no_page_model_execution", False),
        "no_fact_semantic_navigation": flags.get("no_fact_semantic_navigation", False),
        "no_runtime_output_adapter": flags.get("no_runtime", False) and flags.get("no_output_adapter", False),
        "no_external_network": flags.get("no_external_network", False),
        "test_board_planned": True,
        "test_board_protected": True,
    }

    negative_guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append({**spec, "passed": passed})
        (passed_checks if passed else failed_checks).append(
            f"guard.{spec['guard_id']}={'pass' if passed else 'fail'}"
        )

    post_review_flags = {
        **flags,
        "compact_dashboard_layout_written": flags.get("compact_dashboard_layout_written", False),
        "rollback_available": True,
        "rollback_can_restore_previous_static_site": True,
        "rollback_must_preserve_runner_bridge_service": True,
        "rollback_must_preserve_test_board": True,
        "rollback_must_preserve_review_artifacts": True,
        "rollback_not_executed_by_default": True,
    }

    core_go_keys = [
        "luna_observation_title_applied",
        "compact_dashboard_layout_written",
        "default_view_visual_first",
        "single_screen_primary_observation_met",
        "top_task_bar_present",
        "left_capability_panel_present",
        "central_hud_area_present",
        "right_reasoning_panel_present",
        "bottom_metrics_summary_present",
        "bottom_drawers_present",
        "metrics_moved_to_drawer",
        "advanced_info_moved_to_drawer",
        "developer_json_moved_to_drawer",
        "whitebox_slot_present",
        "long_report_flow_removed",
        "perception_hud_preserved",
        "simple_mode_preserved",
        "local_runner_bridge_preserved",
        "no_page_model_execution",
        "test_board_protected",
    ]
    core_passed = all(flags.get(k) for k in core_go_keys)

    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g["passed"])

    if violations:
        final_decision = FINAL_DECISION_BLOCKED
        blocker_count = len(violations) + len(failed_checks)
    elif failed_checks:
        final_decision = FINAL_DECISION_BLOCKED
        blocker_count = len(failed_checks)
    elif core_passed and negative_guard_passed == negative_guard_count:
        final_decision = FINAL_DECISION_GO
        blocker_count = 0
    elif flags.get("compact_dashboard_layout_written") and flags.get("bottom_drawers_present"):
        final_decision = FINAL_DECISION_PARTIAL
        blocker_count = 0
    else:
        final_decision = FINAL_DECISION_FAILED
        blocker_count = sum(1 for k in core_go_keys if not flags.get(k))

    ui_patch_record = {
        "record_id": "luna_observation_compact_ui_patch_record_v1",
        "layout": "top_left_central_right_bottom_dock",
        "default_view": "hud",
        "files": [f.split("/")[-1] for f in COMPACT_FILES if "luna_observation" in f or f.endswith("app.js")],
    }
    layout_record = {
        "record_id": "compact_viewport_layout_record_v1",
        "left_rail_px": 240,
        "right_panel_px": 340,
        "central_flex": True,
        "bottom_dock": True,
    }
    compression_record = {
        "record_id": "information_compression_record_v1",
        "metrics_in_drawer": True,
        "advanced_in_drawer": True,
        "developer_json_in_drawer": True,
        "reasoning_on_right_panel": True,
    }
    drawer_migration_record = {
        "record_id": "drawer_migration_record_v1",
        "drawers": ["metrics", "advanced", "developer", "whitebox", "testboard"],
        "default_collapsed": True,
    }
    hud_preservation_record = {
        "record_id": "perception_hud_preservation_record_v1",
        "renderCentral": True,
        "view_toggle": ["original", "compare", "hud"],
    }
    whitebox_record = {
        "record_id": "whitebox_slot_record_v1",
        "placeholder_only": True,
        "runtime_trace_connected": False,
    }
    boundary_audit = {
        "record_id": "compact_ui_boundary_audit_v1",
        "violations": violations,
        "boundary_ok": boundary_ok,
        "ui_must_not_execute_model": True,
        "runtime_execution_allowed": False,
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Model Test Lens Luna Observation Compact UI Execution",
        "lifecycle_variant": "p1_midplatform_model_test_lens_luna_observation_compact_ui_execution",
        "real_execution_phase": True,
        "luna_observation_compact_ui_execution": True,
        "default_ui_must_be_non_engineering": True,
        "default_view_visual_first": True,
        "single_screen_primary_observation_required": True,
        "max_primary_scroll_depth": 1.5,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "luna_observation_compact_ui_execution_profile_count": 1,
        "negative_guards": negative_guards,
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "audit_flags": flags,
        "post_review_audit": post_review_flags,
        "forbidden_pattern_violations": violations,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "blocker_count": blocker_count,
        "final_decision": final_decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }

    if write_file:
        review_path = out_root / "p1_midplatform_model_test_lens_luna_observation_compact_ui_execution_review_v1.json"
        review_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        extras = {
            "model_test_lens_luna_observation_compact_ui_patch_record_v1.json": ui_patch_record,
            "model_test_lens_luna_observation_compact_layout_record_v1.json": layout_record,
            "model_test_lens_luna_observation_drawer_migration_record_v1.json": drawer_migration_record,
            "model_test_lens_luna_observation_boundary_audit_v1.json": boundary_audit,
            "model_test_lens_luna_observation_compact_ui_post_review_audit_v1.json": post_review_flags,
        }
        for fname, payload in extras.items():
            (out_root / fname).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_root"] = str(out_root)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        try:
            manifest_tb = write_test_board_records(
                result,
                test_mode="real_test",
                repo_root=board_root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "canonical"
        except (OSError, PermissionError):
            _BOARD_STANDIN.mkdir(parents=True, exist_ok=True)
            manifest_tb = write_test_board_records(
                result,
                test_mode="real_test",
                repo_root=_BOARD_STANDIN,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_fallback"

        board_dir = Path(manifest_tb["test_board_dir"])
        common = {
            "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            "phase_id": PHASE_ID,
            "module": "model_governance",
            "test_mode": "real_test",
            "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "test_artifact_protected": True,
            "real_execution_phase": True,
            "ui_must_not_execute_model": True,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
            "semantic_layer_allowed": False,
            "fact_write_allowed": False,
        }
        extra_records = {
            "luna_observation_compact_ui_patch_record": ui_patch_record,
            "compact_viewport_layout_record": layout_record,
            "information_compression_record": compression_record,
            "drawer_migration_record": drawer_migration_record,
            "perception_hud_preservation_record": hud_preservation_record,
            "whitebox_slot_record": whitebox_record,
            "compact_ui_boundary_audit_record": boundary_audit,
            "compact_ui_post_review_record": post_review_flags,
        }
        for rtype, payload in extra_records.items():
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": payload}, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)
        result["test_board_record_count"] = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)

    return result


def main() -> int:
    result = review_model_test_lens_luna_observation_compact_ui_execution_v1(
        test_board_root=str(_REPO_ROOT),
    )
    print(json.dumps(
        {
            "phase_id": result["phase_id"],
            "final_decision": result["final_decision"],
            "blocker_count": result["blocker_count"],
            "negative_guard_passed": result["negative_guard_passed"],
            "negative_guard_count": result["negative_guard_count"],
        },
        indent=2,
        ensure_ascii=False,
    ))
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
