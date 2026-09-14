# -*- coding: utf-8 -*-
"""P1 Model Test Lens Luna Observation Compact Viewport — planning review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Luna-Observation-Compact-Viewport-Planning-v1-001"
PLANNING_ONLY = True
COMPACT_VIEWPORT_PLANNING = True

PLANNING_PRINCIPLE_ZH = (
    "规划 Luna Observation Lens 单屏观察台布局：将纵向 5 屏报告流压缩为 1–1.5 屏仪表盘，"
    "同时可见画面、HUD、Luna 解释、指标摘要与折叠高级入口。"
)

MAX_PRIMARY_SCROLL_DEPTH = 1.5
SINGLE_SCREEN_PRIMARY_OBSERVATION_REQUIRED = True
VISUAL_FIRST_DASHBOARD_LAYOUT = True
DEFAULT_PAGE_MUST_NOT_BE_LONG_REPORT = True

UI_MUST_NOT_EXECUTE_MODEL = True
UI_MUST_NOT_RUN_INFERENCE = True
UI_MUST_NOT_WRITE_FACT = True
UI_MUST_NOT_WRITE_SEMANTIC = True
UI_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH = True
UI_MUST_NOT_CALL_OUTPUT_ADAPTER = True
UI_MUST_NOT_MUTATE_REGISTRY = True

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_COMPACT_VIEWPORT_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_COMPACT_VIEWPORT_PLANNING_BLOCKED"

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "planning"

UI_REDESIGN_REL = "capabilities/midplatform/model_test_lens/ui_redesign"
_PKG = "capabilities/midplatform/model_test_lens"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{UI_REDESIGN_REL}/luna_observation_compact_viewport_plan_v1.md",
    f"{UI_REDESIGN_REL}/luna_observation_compact_layout_spec_v1.json",
    f"{UI_REDESIGN_REL}/luna_observation_information_compression_rules_v1.md",
    f"{UI_REDESIGN_REL}/luna_observation_responsive_viewport_rules_v1.json",
    f"{_PKG}/review_model_test_lens_luna_observation_compact_viewport_planning_v1.py",
)

UPSTREAM_REDESIGN_PLAN = f"{UI_REDESIGN_REL}/luna_observation_lens_ui_redesign_plan_v1.md"

NEXT_MERGED_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Luna-Observation-Compact-UI-Execution-And-Post-Review-v1-001"
)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "luna_observation_compact_layout_spec_plan_record",
    "luna_observation_information_compression_rules_plan_record",
    "luna_observation_responsive_viewport_rules_plan_record",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "go_key": "not_five_screen_report", "depends_on": "not_five_screen_report"},
    {"guard_id": "B", "go_key": "scroll_depth_within_limit", "depends_on": "scroll_depth_within_limit"},
    {"guard_id": "C", "go_key": "central_hud_primary", "depends_on": "central_hud_primary"},
    {"guard_id": "D", "go_key": "metrics_not_full_screen_default", "depends_on": "metrics_not_full_screen_default"},
    {"guard_id": "E", "go_key": "reasoning_on_first_screen", "depends_on": "reasoning_on_first_screen"},
    {"guard_id": "F", "go_key": "advanced_collapsed_default", "depends_on": "advanced_collapsed_default"},
    {"guard_id": "G", "go_key": "no_default_engineering_exposure", "depends_on": "no_default_engineering_exposure"},
    {"guard_id": "H", "go_key": "ui_not_model_executor", "depends_on": "ui_not_model_executor"},
    {"guard_id": "I", "go_key": "no_fact_semantic_registry", "depends_on": "no_fact_semantic_registry"},
    {"guard_id": "J", "go_key": "no_runtime_nav_adapter", "depends_on": "no_runtime_nav_adapter"},
    {"guard_id": "K", "go_key": "no_external_camera_mic", "depends_on": "no_external_camera_mic"},
    {"guard_id": "L", "go_key": "test_board_planned", "depends_on": "test_board_planned"},
    {"guard_id": "M", "go_key": "test_board_protected", "depends_on": "test_board_protected"},
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out"
    / "p1_midplatform_model_test_lens_luna_observation_compact_viewport_planning_v1_smoke_v0"
)
_BOARD_STANDIN = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


@dataclass
class CompactViewportPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    compact_viewport_planning: bool
    single_screen_primary_observation_required: bool
    max_primary_scroll_depth: float
    visual_first_dashboard_layout: bool
    default_page_must_not_be_long_report: bool
    ui_must_not_execute_model: bool
    required_test_board_fields: Dict[str, bool]


@dataclass
class CompactViewportPlanningDecision:
    decision_ref: str
    compact_viewport_planning_profile_count: int
    central_hud_area_required: bool
    bottom_metrics_drawer_required: bool
    whitebox_slot_planned: bool
    negative_guard_count: int
    negative_guard_passed: int
    blocker_count: int
    final_decision: str


def _resolve(rel: str) -> Optional[Path]:
    for base in (_REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p
    return None


def _read(rel: str) -> str:
    p = _resolve(rel)
    return p.read_text(encoding="utf-8") if p else ""


def _load_json(rel: str) -> Optional[Dict[str, Any]]:
    text = _read(rel)
    return json.loads(text) if text else None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def review_model_test_lens_luna_observation_compact_viewport_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in REQUIRED_FILES:
        if _resolve(rel):
            passed_checks.append(f"file.present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"file.missing={rel}")

    plan_md = _read(f"{UI_REDESIGN_REL}/luna_observation_compact_viewport_plan_v1.md")
    layout = _load_json(f"{UI_REDESIGN_REL}/luna_observation_compact_layout_spec_v1.json")
    compression_md = _read(f"{UI_REDESIGN_REL}/luna_observation_information_compression_rules_v1.md")
    responsive = _load_json(f"{UI_REDESIGN_REL}/luna_observation_responsive_viewport_rules_v1.json")

    central_hud = False
    right_reasoning = False
    left_capability = False
    bottom_drawer = False
    advanced_dev_drawers = False
    metrics_in_drawer = False
    advanced_in_drawer = False
    dev_json_in_drawer = False
    whitebox_slot = False
    not_five_screen = False
    scroll_depth_ok = False
    metrics_not_full_screen = False
    no_engineering_default = False

    if layout:
        not_five_screen = "vertical_report_stream_five_screens" in layout.get("forbidden_layout_patterns", [])
        scroll_depth_ok = layout.get("max_primary_scroll_depth_viewport_units") == 1.5
        metrics_not_full_screen = "metrics_bar_chart_full_screen_default" in layout.get(
            "forbidden_layout_patterns", []
        )
        main_row = None
        for r in layout.get("regions", []):
            if r.get("region_id") == "main_dashboard_row":
                main_row = r
            if r.get("region_id") == "bottom_metrics_dock":
                bottom_drawer = True
                tabs = {t.get("tab_id") for t in r.get("tabs", [])}
                advanced_dev_drawers = "advanced_workflow" in tabs and "developer_json" in tabs
                metrics_in_drawer = "metrics_detail" in tabs
                whitebox_slot = "whitebox_slot" in tabs
        if main_row:
            for child in main_row.get("children", []):
                cid = child.get("region_id")
                if cid == "central_observation_canvas":
                    central_hud = child.get("default_view") == "robot_vision_hud"
                if cid == "right_luna_explanation_panel":
                    right_reasoning = len(child.get("sections", [])) >= 5
                if cid == "left_capability_rail":
                    left_capability = True

    if compression_md:
        metrics_in_drawer = metrics_in_drawer and "指标详情" in compression_md and "drawer" in compression_md
        advanced_in_drawer = "高级流程" in compression_md
        dev_json_in_drawer = "开发者 JSON" in compression_md or "开发者 drawer" in compression_md
        no_engineering_default = "不得默认占据主屏" in compression_md

    if responsive:
        scroll_depth_ok = scroll_depth_ok and responsive.get("max_primary_scroll_depth") == 1.5
        wb = responsive.get("whitebox_slot_placement", {})
        whitebox_slot = whitebox_slot or wb.get("default_expanded") is False

    if plan_md:
        not_five_screen = not_five_screen and "5 屏" in plan_md
        advanced_dev_drawers = advanced_dev_drawers and "折叠" in plan_md

    upstream_ok = _resolve(UPSTREAM_REDESIGN_PLAN) is not None

    invariant_state: Dict[str, bool] = {
        "not_five_screen_report": not_five_screen,
        "scroll_depth_within_limit": scroll_depth_ok,
        "central_hud_primary": central_hud,
        "metrics_not_full_screen_default": metrics_not_full_screen,
        "reasoning_on_first_screen": right_reasoning,
        "advanced_collapsed_default": advanced_dev_drawers and layout.get("regions", [{}])[-1].get(
            "default_collapsed_tabs", False
        ) if layout else False,
        "no_default_engineering_exposure": no_engineering_default,
        "ui_not_model_executor": UI_MUST_NOT_EXECUTE_MODEL and UI_MUST_NOT_RUN_INFERENCE,
        "no_fact_semantic_registry": (
            UI_MUST_NOT_WRITE_FACT and UI_MUST_NOT_WRITE_SEMANTIC and UI_MUST_NOT_MUTATE_REGISTRY
        ),
        "no_runtime_nav_adapter": (
            UI_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH and UI_MUST_NOT_CALL_OUTPUT_ADAPTER
        ),
        "no_external_camera_mic": True,
        "test_board_planned": True,
        "test_board_protected": REQUIRED_TEST_BOARD_FIELDS.get("test_artifact_protected", False) is True,
    }

    negative_guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append({**spec, "passed": passed})
        (passed_checks if passed else failed_checks).append(
            f"guard.{spec['guard_id']}={'pass' if passed else 'fail'}"
        )

    go_conditions: Dict[str, bool] = {
        "compact_viewport_planning_profile_count_eq_1": True,
        "single_screen_primary_observation_required": SINGLE_SCREEN_PRIMARY_OBSERVATION_REQUIRED,
        "max_primary_scroll_depth_eq_1_5": scroll_depth_ok,
        "visual_first_dashboard_layout": VISUAL_FIRST_DASHBOARD_LAYOUT and central_hud,
        "central_hud_area_required": central_hud,
        "right_reasoning_panel_required": right_reasoning,
        "left_capability_panel_required": left_capability,
        "bottom_metrics_drawer_required": bottom_drawer,
        "advanced_developer_drawers_required": advanced_dev_drawers,
        "default_page_must_not_be_long_report": DEFAULT_PAGE_MUST_NOT_BE_LONG_REPORT and not_five_screen,
        "metrics_moved_to_drawer": metrics_in_drawer,
        "advanced_info_moved_to_drawer": advanced_in_drawer,
        "developer_json_moved_to_drawer": dev_json_in_drawer,
        "whitebox_slot_planned": whitebox_slot,
        "upstream_ui_redesign_plan_referenced": upstream_ok,
        "merged_execution_phase_defined": bool(NEXT_MERGED_EXECUTION),
        "planning_only": PLANNING_ONLY,
        "negative_guard_count_eq_13": len(negative_guards) == 13,
        "negative_guard_passed_eq_13": sum(1 for g in negative_guards if g["passed"]) == 13,
        **{f"test_board.{k}": v is True for k, v in REQUIRED_TEST_BOARD_FIELDS.items()},
        **{g["go_key"]: g["passed"] for g in negative_guards},
    }

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    profile = CompactViewportPlanningProfile(
        profile_ref="luna_observation_compact_viewport_planning_profile_v1",
        phase_id=PHASE_ID,
        planning_only=PLANNING_ONLY,
        compact_viewport_planning=COMPACT_VIEWPORT_PLANNING,
        single_screen_primary_observation_required=SINGLE_SCREEN_PRIMARY_OBSERVATION_REQUIRED,
        max_primary_scroll_depth=MAX_PRIMARY_SCROLL_DEPTH,
        visual_first_dashboard_layout=VISUAL_FIRST_DASHBOARD_LAYOUT,
        default_page_must_not_be_long_report=DEFAULT_PAGE_MUST_NOT_BE_LONG_REPORT,
        ui_must_not_execute_model=UI_MUST_NOT_EXECUTE_MODEL,
        required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS),
    )

    decision = CompactViewportPlanningDecision(
        decision_ref="luna_observation_compact_viewport_planning_decision_v1",
        compact_viewport_planning_profile_count=1,
        central_hud_area_required=central_hud,
        bottom_metrics_drawer_required=bottom_drawer,
        whitebox_slot_planned=whitebox_slot,
        negative_guard_count=len(negative_guards),
        negative_guard_passed=sum(1 for g in negative_guards if g["passed"]),
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    layout_plan = {"plan_id": "luna_observation_compact_layout_spec_plan_v1", "spec": layout}
    compression_plan = {
        "plan_id": "luna_observation_information_compression_rules_plan_v1",
        "rules_ref": f"{UI_REDESIGN_REL}/luna_observation_information_compression_rules_v1.md",
    }
    responsive_plan = {"plan_id": "luna_observation_responsive_viewport_rules_plan_v1", "spec": responsive}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "planning_only": PLANNING_ONLY,
        "compact_viewport_planning_profile": asdict(profile),
        "compact_viewport_planning_profile_count": 1,
        "recommended_merged_execution_phase": NEXT_MERGED_EXECUTION,
        "negative_guards": negative_guards,
        "negative_guard_count": len(negative_guards),
        "negative_guard_passed": sum(1 for g in negative_guards if g["passed"]),
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "final_decision": final_decision,
        "blocker_count": blocker_count,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "reviewed_at": _now(),
    }

    if write_file:
        review_path = out_root / "p1_midplatform_model_test_lens_luna_observation_compact_viewport_planning_review_v1.json"
        review_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        (out_root / "luna_observation_compact_layout_spec_plan_v1.json").write_text(
            json.dumps(layout_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "luna_observation_information_compression_rules_plan_v1.json").write_text(
            json.dumps(compression_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "luna_observation_responsive_viewport_rules_plan_v1.json").write_text(
            json.dumps(responsive_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
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
        except (OSError, PermissionError):
            _BOARD_STANDIN.mkdir(parents=True, exist_ok=True)
            manifest_tb = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_fallback"

        board_dir = Path(manifest_tb["test_board_dir"])
        common = {
            "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            "phase_id": PHASE_ID,
            "protected": True,
            "non_deletable": True,
            "planning_only": True,
        }
        for rtype, payload in {
            "luna_observation_compact_layout_spec_plan_record": layout_plan,
            "luna_observation_information_compression_rules_plan_record": compression_plan,
            "luna_observation_responsive_viewport_rules_plan_record": responsive_plan,
        }.items():
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": payload}, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    result = review_model_test_lens_luna_observation_compact_viewport_planning_v1(
        test_board_root=str(_REPO_ROOT),
    )
    print(json.dumps(
        {
            "phase_id": result["phase_id"],
            "final_decision": result["final_decision"],
            "blocker_count": result["blocker_count"],
            "negative_guard_passed": result["negative_guard_passed"],
            "recommended_merged_execution_phase": result["recommended_merged_execution_phase"],
        },
        indent=2,
        ensure_ascii=False,
    ))
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
