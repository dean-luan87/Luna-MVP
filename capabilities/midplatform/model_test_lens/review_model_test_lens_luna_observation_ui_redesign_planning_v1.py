# -*- coding: utf-8 -*-
"""P1 Model Test Lens Luna Observation UI Redesign — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Luna-Observation-UI-Redesign-Planning-v1-001"
PLANNING_ONLY = True
LUNA_OBSERVATION_UI_REDESIGN_PLANNING = True

PLANNING_PRINCIPLE_ZH = (
    "将 Model Test Lens 默认 UI 重新规划为 Luna Observation Lens 观察窗口："
    "画面优先、HUD 优先、Luna 解释优先，工程内容默认折叠隐藏。"
)

LUNA_CORE_PRINCIPLE = "observation_window_first_not_configuration_form_first"

DEFAULT_UI_MUST_BE_NON_ENGINEERING = True
DEFAULT_VIEW_VISUAL_FIRST = True
ROBOT_VISION_HUD_DEFAULT = True
REASONING_PANEL_REQUIRED = True
ADVANCED_MODE_PRESERVED = True
DEVELOPER_MODE_PRESERVED = True
RUNNER_BRIDGE_PRESERVED = True
TESTBOARD_PRESERVED = True

UI_MUST_NOT_EXECUTE_MODEL = True
UI_MUST_NOT_RUN_INFERENCE = True
UI_MUST_NOT_WRITE_FACT = True
UI_MUST_NOT_WRITE_SEMANTIC = True
UI_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH = True
UI_MUST_NOT_CALL_OUTPUT_ADAPTER = True
UI_MUST_NOT_MUTATE_REGISTRY = True

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_UI_REDESIGN_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_UI_REDESIGN_PLANNING_BLOCKED"

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "planning"

UI_REDESIGN_REL = "capabilities/midplatform/model_test_lens/ui_redesign"
STANDARDS_UI_REL = "capabilities/midplatform/model_test_lens/standards/ui"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

REQUIRED_PLANNING_FILES: Tuple[str, ...] = (
    f"{UI_REDESIGN_REL}/luna_observation_lens_ui_redesign_plan_v1.md",
    f"{UI_REDESIGN_REL}/luna_observation_lens_layout_spec_v1.json",
    f"{UI_REDESIGN_REL}/luna_observation_lens_component_spec_v1.json",
    f"{UI_REDESIGN_REL}/luna_observation_lens_copywriting_standard_v1.md",
    f"{UI_REDESIGN_REL}/luna_observation_lens_interaction_flow_v1.json",
    f"{_PKG}/review_model_test_lens_luna_observation_ui_redesign_planning_v1.py",
)

UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    "Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-View-Planning-v1-001",
    "Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-UI-Standardization-Planning-v1-001",
    "Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-View-Execution-And-Post-Review-v1-001",
    "Phase-P1-Midplatform-Model-Test-Lens-Visual-Compare-View-Execution-And-Post-Review-v1-001",
    "Phase-P1-Midplatform-Model-Test-Lens-Simple-Mode-UX-Patch-Execution-And-Post-Review-v1-001",
)

NEXT_PHASE_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Luna-Observation-UI-Redesign-Execution-And-Post-Review-v1-001"
)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "luna_observation_lens_layout_spec_plan_record",
    "luna_observation_lens_component_spec_plan_record",
    "luna_observation_lens_interaction_flow_plan_record",
    "luna_observation_lens_copywriting_standard_plan_record",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "go_key": "not_engineering_form_default", "depends_on": "not_engineering_form_default"},
    {"guard_id": "B", "go_key": "no_default_raw_json", "depends_on": "no_default_raw_json"},
    {"guard_id": "C", "go_key": "central_observation_primary", "depends_on": "central_observation_primary"},
    {"guard_id": "D", "go_key": "reasoning_panel_defined", "depends_on": "reasoning_panel_defined"},
    {"guard_id": "E", "go_key": "robot_hud_entry_defined", "depends_on": "robot_hud_entry_defined"},
    {"guard_id": "F", "go_key": "advanced_developer_preserved", "depends_on": "advanced_developer_preserved"},
    {"guard_id": "G", "go_key": "ui_not_model_executor", "depends_on": "ui_not_model_executor"},
    {"guard_id": "H", "go_key": "no_fact_semantic_registry", "depends_on": "no_fact_semantic_registry"},
    {"guard_id": "I", "go_key": "no_runtime_nav_speech_adapter", "depends_on": "no_runtime_nav_speech_adapter"},
    {"guard_id": "J", "go_key": "no_external_camera_mic", "depends_on": "no_external_camera_mic"},
    {"guard_id": "K", "go_key": "test_board_planned", "depends_on": "test_board_planned"},
    {"guard_id": "L", "go_key": "test_board_protected", "depends_on": "test_board_protected"},
)

PROFILE_REF = "luna_observation_ui_redesign_planning_profile_v1"
DECISION_REF = "luna_observation_ui_redesign_planning_decision_v1"
REVIEW_FILENAME = "p1_midplatform_model_test_lens_luna_observation_ui_redesign_planning_review_v1.json"
DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out"
    / "p1_midplatform_model_test_lens_luna_observation_ui_redesign_planning_v1_smoke_v0"
)
_BOARD_STANDIN = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


@dataclass
class LunaObservationUIRedesignPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    luna_observation_ui_redesign_planning: bool
    default_ui_must_be_non_engineering: bool
    default_view_visual_first: bool
    robot_vision_hud_default: bool
    reasoning_panel_required: bool
    advanced_mode_preserved: bool
    developer_mode_preserved: bool
    runner_bridge_preserved: bool
    testboard_preserved: bool
    ui_must_not_execute_model: bool
    ui_must_not_run_inference: bool
    ui_must_not_write_fact: bool
    ui_must_not_write_semantic: bool
    ui_must_not_trigger_navigation_action_speech: bool
    ui_must_not_call_output_adapter: bool
    ui_must_not_mutate_registry: bool
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]


@dataclass
class P1LunaObservationUIRedesignPlanningDecision:
    decision_ref: str
    luna_observation_ui_redesign_profile_count: int
    central_observation_area_required: bool
    left_capability_cards_required: bool
    whitebox_view_slot_planned: bool
    governance_standard_referenced: bool
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
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
    if not text:
        return None
    return json.loads(text)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def review_model_test_lens_luna_observation_ui_redesign_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in REQUIRED_PLANNING_FILES:
        if _resolve(rel):
            passed_checks.append(f"file.present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"file.missing={rel}")

    plan_md = _read(f"{UI_REDESIGN_REL}/luna_observation_lens_ui_redesign_plan_v1.md")
    layout = _load_json(f"{UI_REDESIGN_REL}/luna_observation_lens_layout_spec_v1.json")
    components = _load_json(f"{UI_REDESIGN_REL}/luna_observation_lens_component_spec_v1.json")
    copy_md = _read(f"{UI_REDESIGN_REL}/luna_observation_lens_copywriting_standard_v1.md")
    flow = _load_json(f"{UI_REDESIGN_REL}/luna_observation_lens_interaction_flow_v1.json")

    central_observation = False
    left_capability_cards = False
    reasoning_panel = False
    robot_hud_default = False
    advanced_dev_preserved = False
    whitebox_slot = False
    not_engineering_default = False
    no_default_raw_json = False

    if layout:
        region_ids = {r.get("region_id") for r in layout.get("regions", [])}
        central_observation = "central_observation_canvas" in region_ids
        left_capability_cards = "left_capability_rail" in region_ids
        default_modes = layout.get("view_modes", [])
        robot_hud_default = any(
            m.get("mode_id") == "robot_vision_hud" and m.get("default") is True for m in default_modes
        ) or layout.get("regions", [{}])[2].get("default_view_mode") == "robot_vision_hud"

    if components:
        expl = components.get("components", {}).get("right_luna_explanation_panel", {})
        sections = expl.get("sections", [])
        reasoning_panel = len(sections) >= 5
        whitebox_slot = components.get("components", {}).get("whitebox_view_slot", {}).get("planned") is True
        rail = components.get("components", {}).get("left_capability_rail", {})
        forbidden = set(rail.get("forbidden_default_labels", []))
        left_capability_cards = left_capability_cards and "placeholder" in forbidden

    if plan_md:
        not_engineering_default = (
            "工程化表单" in plan_md
            and "Luna Observation Lens" in plan_md
            and "manifest" in plan_md
        )
        advanced_dev_preserved = "高级流程" in plan_md and "开发者" in plan_md
        runner_bridge_preserved = "8787" in plan_md or "runner bridge" in plan_md.lower()

    if copy_md:
        no_default_raw_json = "默认禁止" in copy_md and "manifest" in copy_md

    if flow:
        hp = flow.get("homepage_first_paint", {})
        must_not = hp.get("must_not_show_first", [])
        not_engineering_default = not_engineering_default and "manifest_form" in must_not
        advanced_dev_preserved = advanced_dev_preserved or "advanced_workflow" in flow.get("mode_presets", {})

    gov_standard_ok = _resolve(f"{STANDARDS_UI_REL}/model_test_lens_ui_standard_v1.md") is not None
    hud_execution_ok = _resolve(f"{STATIC_REL}/perception_hud_view_v1.js") is not None

    invariant_state: Dict[str, bool] = {
        "not_engineering_form_default": not_engineering_default,
        "no_default_raw_json": no_default_raw_json,
        "central_observation_primary": central_observation,
        "reasoning_panel_defined": reasoning_panel,
        "robot_hud_entry_defined": robot_hud_default,
        "advanced_developer_preserved": advanced_dev_preserved and DEVELOPER_MODE_PRESERVED,
        "ui_not_model_executor": UI_MUST_NOT_EXECUTE_MODEL and UI_MUST_NOT_RUN_INFERENCE,
        "no_fact_semantic_registry": (
            UI_MUST_NOT_WRITE_FACT and UI_MUST_NOT_WRITE_SEMANTIC and UI_MUST_NOT_MUTATE_REGISTRY
        ),
        "no_runtime_nav_speech_adapter": (
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
        "luna_observation_ui_redesign_profile_count_eq_1": True,
        "default_ui_must_be_non_engineering": DEFAULT_UI_MUST_BE_NON_ENGINEERING and not_engineering_default,
        "default_view_visual_first": DEFAULT_VIEW_VISUAL_FIRST and central_observation,
        "central_observation_area_required": central_observation,
        "robot_vision_hud_default": ROBOT_VISION_HUD_DEFAULT and robot_hud_default,
        "reasoning_panel_required": REASONING_PANEL_REQUIRED and reasoning_panel,
        "left_capability_cards_required": left_capability_cards,
        "advanced_mode_preserved": ADVANCED_MODE_PRESERVED and advanced_dev_preserved,
        "developer_mode_preserved": DEVELOPER_MODE_PRESERVED and advanced_dev_preserved,
        "whitebox_view_slot_planned": whitebox_slot,
        "runner_bridge_preserved": RUNNER_BRIDGE_PRESERVED,
        "testboard_preserved": TESTBOARD_PRESERVED,
        "ui_must_not_execute_model": UI_MUST_NOT_EXECUTE_MODEL,
        "ui_must_not_run_inference": UI_MUST_NOT_RUN_INFERENCE,
        "ui_must_not_write_fact": UI_MUST_NOT_WRITE_FACT,
        "ui_must_not_write_semantic": UI_MUST_NOT_WRITE_SEMANTIC,
        "ui_must_not_trigger_navigation_action_speech": UI_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH,
        "ui_must_not_call_output_adapter": UI_MUST_NOT_CALL_OUTPUT_ADAPTER,
        "ui_must_not_mutate_registry": UI_MUST_NOT_MUTATE_REGISTRY,
        "planning_only": PLANNING_ONLY,
        "governance_standard_referenced": gov_standard_ok,
        "perception_hud_execution_assets_present": hud_execution_ok,
        "negative_guard_count_eq_12": len(negative_guards) == 12,
        "negative_guard_passed_eq_12": sum(1 for g in negative_guards if g["passed"]) == 12,
        **{f"test_board.{k}": v is True for k, v in REQUIRED_TEST_BOARD_FIELDS.items()},
    }

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    profile = LunaObservationUIRedesignPlanningProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        planning_only=PLANNING_ONLY,
        luna_observation_ui_redesign_planning=LUNA_OBSERVATION_UI_REDESIGN_PLANNING,
        default_ui_must_be_non_engineering=DEFAULT_UI_MUST_BE_NON_ENGINEERING,
        default_view_visual_first=DEFAULT_VIEW_VISUAL_FIRST,
        robot_vision_hud_default=ROBOT_VISION_HUD_DEFAULT,
        reasoning_panel_required=REASONING_PANEL_REQUIRED,
        advanced_mode_preserved=ADVANCED_MODE_PRESERVED,
        developer_mode_preserved=DEVELOPER_MODE_PRESERVED,
        runner_bridge_preserved=RUNNER_BRIDGE_PRESERVED,
        testboard_preserved=TESTBOARD_PRESERVED,
        ui_must_not_execute_model=UI_MUST_NOT_EXECUTE_MODEL,
        ui_must_not_run_inference=UI_MUST_NOT_RUN_INFERENCE,
        ui_must_not_write_fact=UI_MUST_NOT_WRITE_FACT,
        ui_must_not_write_semantic=UI_MUST_NOT_WRITE_SEMANTIC,
        ui_must_not_trigger_navigation_action_speech=UI_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH,
        ui_must_not_call_output_adapter=UI_MUST_NOT_CALL_OUTPUT_ADAPTER,
        ui_must_not_mutate_registry=UI_MUST_NOT_MUTATE_REGISTRY,
        luna_core_principle=LUNA_CORE_PRINCIPLE,
        required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS),
    )

    decision = P1LunaObservationUIRedesignPlanningDecision(
        decision_ref=DECISION_REF,
        luna_observation_ui_redesign_profile_count=1,
        central_observation_area_required=central_observation,
        left_capability_cards_required=left_capability_cards,
        whitebox_view_slot_planned=whitebox_slot,
        governance_standard_referenced=gov_standard_ok,
        negative_guard_count=len(negative_guards),
        negative_guard_passed=sum(1 for g in negative_guards if g["passed"]),
        test_board_record_count=len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES),
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    layout_plan = {"plan_id": "luna_observation_lens_layout_spec_plan_v1", "spec_ref": layout}
    component_plan = {"plan_id": "luna_observation_lens_component_spec_plan_v1", "spec_ref": components}
    flow_plan = {"plan_id": "luna_observation_lens_interaction_flow_plan_v1", "spec_ref": flow}
    copy_plan = {
        "plan_id": "luna_observation_lens_copywriting_standard_plan_v1",
        "title": "Luna Observation Lens",
        "forbidden_default_terms": layout.get("forbidden_default_visible_terms", []) if layout else [],
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Model Test Lens Luna Observation UI Redesign Planning",
        "lifecycle_variant": "p1_midplatform_model_test_lens_luna_observation_ui_redesign_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "planning_only": PLANNING_ONLY,
        "luna_observation_ui_redesign_planning": LUNA_OBSERVATION_UI_REDESIGN_PLANNING,
        "upstream_phase_refs": list(UPSTREAM_PHASE_REFS),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "luna_observation_ui_redesign_profile": asdict(profile),
        "luna_observation_ui_redesign_profile_count": 1,
        "negative_guards": negative_guards,
        "negative_guard_count": len(negative_guards),
        "negative_guard_passed": sum(1 for g in negative_guards if g["passed"]),
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "final_decision": final_decision,
        "blocker_count": blocker_count,
        "recommended_next_phase": NEXT_PHASE_EXECUTION,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "reviewed_at": _now(),
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        (out_root / "luna_observation_lens_layout_spec_plan_v1.json").write_text(
            json.dumps(layout_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "luna_observation_lens_component_spec_plan_v1.json").write_text(
            json.dumps(component_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "luna_observation_lens_interaction_flow_plan_v1.json").write_text(
            json.dumps(flow_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "luna_observation_lens_copywriting_standard_plan_v1.json").write_text(
            json.dumps(copy_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
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
            "module": TEST_BOARD_MODULE,
            "test_mode": TEST_BOARD_TEST_MODE,
            "recorded_at_utc": _now(),
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "planning_only": True,
        }
        for rtype, payload in {
            "luna_observation_lens_layout_spec_plan_record": layout_plan,
            "luna_observation_lens_component_spec_plan_record": component_plan,
            "luna_observation_lens_interaction_flow_plan_record": flow_plan,
            "luna_observation_lens_copywriting_standard_plan_record": copy_plan,
        }.items():
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": payload}, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    result = review_model_test_lens_luna_observation_ui_redesign_planning_v1(
        test_board_root=str(_REPO_ROOT),
    )
    print(json.dumps(
        {
            "phase_id": result["phase_id"],
            "final_decision": result["final_decision"],
            "blocker_count": result["blocker_count"],
            "negative_guard_passed": result["negative_guard_passed"],
            "recommended_next_phase": result["recommended_next_phase"],
        },
        indent=2,
        ensure_ascii=False,
    ))
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
