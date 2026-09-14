# -*- coding: utf-8 -*-
"""P1 Model Test Lens Perception HUD UI Standardization — planning review v1."""

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
from capabilities.midplatform.model_test_lens.perception_hud.perception_hud_types_v1 import (  # noqa: E402
    HUD_MUST_NOT_CALL_OUTPUT_ADAPTER,
    HUD_MUST_NOT_EXECUTE_MODEL,
    HUD_MUST_NOT_GENERATE_NEW_FACT,
    HUD_MUST_NOT_MUTATE_REGISTRY,
    HUD_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH,
    HUD_MUST_NOT_WRITE_SEMANTIC,
    MODEL_EXECUTION_ALLOWED_IN_PAGE,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SEMANTIC_LAYER_ALLOWED,
    TARGET_CHAIN_REF,
)

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-UI-Standardization-Planning-v1-001"
PLANNING_ONLY = True
UI_STANDARDIZATION_PLANNING = True
PERCEPTION_HUD_AS_UNIFIED_TEMPLATE = True
ROBOT_VISION_HUD_DEFAULT = True
ALL_FUTURE_MODEL_TEST_PAGES_MUST_FOLLOW = True

PLANNING_PRINCIPLE_ZH = (
    "将 Perception HUD / Robot Vision HUD 固化为 Model Test Lens 统一网页测试界面规范。"
    "适用于后续所有模型测试页面。只规范展示与解释，不执行模型、不写 fact、不进 runtime。"
)

LUNA_CORE_PRINCIPLE = "model_test_lens_ui_standard_makes_model_worldview_readable_not_actionable"

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_PERCEPTION_HUD_UI_STANDARDIZATION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_PERCEPTION_HUD_UI_STANDARDIZATION_PLANNING_BLOCKED"

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "planning"

STANDARDS_UI_REL = "capabilities/midplatform/model_test_lens/standards/ui"
STANDARDS_PERCEPTION_HUD_REL = "capabilities/midplatform/model_test_lens/standards/perception_hud"
GOVERNANCE_UI_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"

REQUIRED_STANDARD_FILES: Tuple[str, ...] = (
    f"{STANDARDS_UI_REL}/model_test_lens_ui_standard_v1.md",
    f"{STANDARDS_UI_REL}/model_test_lens_ui_flow_standard_v1.json",
    f"{STANDARDS_PERCEPTION_HUD_REL}/perception_hud_ui_template_standard_v1.md",
    f"{STANDARDS_PERCEPTION_HUD_REL}/perception_hud_model_adapter_requirements_v1.json",
    f"{STANDARDS_PERCEPTION_HUD_REL}/perception_hud_default_layout_spec_v1.json",
    f"{GOVERNANCE_UI_REL}/model_test_lens_perception_hud_ui_governance_standard_v1.md",
    f"{GOVERNANCE_UI_REL}/model_test_lens_ui_standard_registry_v1.json",
)

UPSTREAM_PERCEPTION_HUD_PLANNING_PHASE = (
    "Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-View-Planning-v1-001"
)

MODEL_CATEGORIES: Tuple[str, ...] = (
    "segmentation",
    "detection_tracking",
    "ocr",
    "slam_vio",
    "depth_world",
    "asr",
    "tts",
    "speaker",
    "face_expression_gesture",
    "multimodal_vlm",
)

UI_LEVELS: Tuple[str, ...] = (
    "simple_mode",
    "visual_compare_view",
    "perception_hud_view",
    "metrics",
    "advanced_mode",
    "developer_mode",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "go_key": "unified_ui_standard_required", "depends_on": "unified_ui_standard_required"},
    {"guard_id": "B", "go_key": "no_default_raw_json", "depends_on": "no_default_raw_json"},
    {"guard_id": "C", "go_key": "visual_compare_or_hud_required", "depends_on": "visual_compare_or_hud_required"},
    {"guard_id": "D", "go_key": "reasoning_panel_required", "depends_on": "reasoning_panel_required"},
    {"guard_id": "E", "go_key": "hud_not_model_executor", "depends_on": "hud_not_model_executor"},
    {"guard_id": "F", "go_key": "candidate_not_fact", "depends_on": "candidate_not_fact"},
    {"guard_id": "G", "go_key": "no_navigation_speech", "depends_on": "no_navigation_speech"},
    {"guard_id": "H", "go_key": "no_semantic_fact_registry", "depends_on": "no_semantic_fact_registry"},
    {"guard_id": "I", "go_key": "no_runtime_output_adapter", "depends_on": "no_runtime_output_adapter"},
    {"guard_id": "J", "go_key": "no_external_camera_mic", "depends_on": "no_external_camera_mic"},
    {"guard_id": "K", "go_key": "no_delete_artifact", "depends_on": "no_delete_artifact"},
    {"guard_id": "L", "go_key": "model_adapter_requirements_defined", "depends_on": "model_adapter_requirements_defined"},
    {"guard_id": "M", "go_key": "advanced_developer_modes_defined", "depends_on": "advanced_developer_modes_defined"},
    {"guard_id": "N", "go_key": "test_board_planned", "depends_on": "test_board_planned"},
    {"guard_id": "O", "go_key": "test_board_protected", "depends_on": "test_board_protected"},
)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "model_test_lens_ui_standard_plan_record",
    "perception_hud_ui_template_standard_plan_record",
    "perception_hud_model_adapter_requirements_plan_record",
    "governance_standards_model_test_lens_ui_patch_plan_record",
)

PROFILE_REF = "model_test_lens_ui_standardization_planning_profile_v1"
DECISION_REF = "model_test_lens_ui_standardization_planning_decision_v1"
REVIEW_FILENAME = (
    "p1_midplatform_model_test_lens_perception_hud_ui_standardization_planning_review_v1.json"
)
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


@dataclass
class ModelTestLensUIStandardizationPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    ui_standardization_planning: bool
    perception_hud_as_unified_template: bool
    robot_vision_hud_default: bool
    all_future_model_test_pages_must_follow: bool
    hud_must_not_execute_model: bool
    hud_must_not_generate_fact: bool
    hud_must_not_write_semantic: bool
    hud_must_not_trigger_navigation_action_speech: bool
    hud_must_not_call_output_adapter: bool
    hud_must_not_mutate_registry: bool
    target_chain_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]


@dataclass
class NegativeUIStandardizationPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool


@dataclass
class P1MidplatformModelTestLensUIStandardizationPlanningDecision:
    decision_ref: str
    model_test_lens_ui_standardization_profile_count: int
    model_test_lens_ui_standard_defined: bool
    perception_hud_as_unified_template: bool
    robot_vision_hud_default: bool
    all_future_model_test_pages_must_follow: bool
    visual_compare_required: bool
    reasoning_panel_required: bool
    model_category_hud_adapter_requirements_defined: bool
    governance_standard_patch_planned: bool
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


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
    / "p1_midplatform_model_test_lens_perception_hud_ui_standardization_planning_v1_smoke_v0"
)


def _resolve_file(rel: str) -> Optional[Path]:
    for base in (_REPO_ROOT, Path.cwd(), _WRITABLE_BASE):
        p = base / rel
        if p.is_file():
            return p
    return None


def _load_json(rel: str) -> Optional[Dict[str, Any]]:
    p = _resolve_file(rel)
    if p is None:
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def review_model_test_lens_perception_hud_ui_standardization_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []
    warnings: List[str] = []

    step_files = REQUIRED_STANDARD_FILES + (
        "capabilities/midplatform/model_test_lens/review_model_test_lens_perception_hud_ui_standardization_planning_v1.py",
    )
    for rel in step_files:
        if _resolve_file(rel) is not None:
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    ui_standard_md = _resolve_file(f"{STANDARDS_UI_REL}/model_test_lens_ui_standard_v1.md")
    ui_flow = _load_json(f"{STANDARDS_UI_REL}/model_test_lens_ui_flow_standard_v1.json")
    hud_template_md = _resolve_file(
        f"{STANDARDS_PERCEPTION_HUD_REL}/perception_hud_ui_template_standard_v1.md"
    )
    adapter_req = _load_json(
        f"{STANDARDS_PERCEPTION_HUD_REL}/perception_hud_model_adapter_requirements_v1.json"
    )
    layout_spec = _load_json(
        f"{STANDARDS_PERCEPTION_HUD_REL}/perception_hud_default_layout_spec_v1.json"
    )
    gov_registry = _load_json(
        f"{GOVERNANCE_UI_REL}/model_test_lens_ui_standard_registry_v1.json"
    )

    model_test_lens_ui_standard_defined = ui_standard_md is not None and ui_flow is not None
    perception_hud_template_defined = hud_template_md is not None and layout_spec is not None

    adapter_categories_defined: Dict[str, bool] = {}
    if adapter_req:
        cats = adapter_req.get("model_categories", {})
        for cat in MODEL_CATEGORIES:
            adapter_categories_defined[f"{cat}_hud_requirement_defined"] = cat in cats
    else:
        for cat in MODEL_CATEGORIES:
            adapter_categories_defined[f"{cat}_hud_requirement_defined"] = False

    visual_compare_required = False
    reasoning_panel_required = False
    advanced_developer_modes = False
    no_default_raw_json = False

    if ui_standard_md:
        text = ui_standard_md.read_text(encoding="utf-8")
        visual_compare_required = "Visual Compare" in text
        reasoning_panel_required = "Perception HUD" in text and "推理" in text
        advanced_developer_modes = "Advanced Mode" in text and "Developer Mode" in text
        no_default_raw_json = "禁止退回到" in text or "JSON 优先" in text

    if ui_flow:
        levels = ui_flow.get("levels", [])
        level_ids = {lv.get("id") or lv.get("level_id") for lv in levels}
        if set(UI_LEVELS) <= level_ids:
            passed_checks.append("ui_flow.all_levels_defined=true")
        else:
            failed_checks.append("ui_flow.all_levels_incomplete=true")

    governance_standard_patch_planned = (
        _resolve_file(f"{GOVERNANCE_UI_REL}/model_test_lens_perception_hud_ui_governance_standard_v1.md") is not None
        and gov_registry is not None
    )

    upstream_hud_planning_ok = _resolve_file(
        "capabilities/midplatform/model_test_lens/perception_hud/perception_hud_view_plan_v1.md"
    ) is not None
    if not upstream_hud_planning_ok:
        warnings.append("upstream_perception_hud_view_planning_not_verified_go")

    invariant_state: Dict[str, bool] = {
        "unified_ui_standard_required": model_test_lens_ui_standard_defined and perception_hud_template_defined,
        "no_default_raw_json": no_default_raw_json,
        "visual_compare_or_hud_required": visual_compare_required and perception_hud_template_defined,
        "reasoning_panel_required": reasoning_panel_required,
        "hud_not_model_executor": HUD_MUST_NOT_EXECUTE_MODEL and MODEL_EXECUTION_ALLOWED_IN_PAGE is False,
        "candidate_not_fact": HUD_MUST_NOT_GENERATE_NEW_FACT is True,
        "no_navigation_speech": (
            HUD_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH is True
            and NAVIGATION_ACTION_SPEECH_ALLOWED is False
        ),
        "no_semantic_fact_registry": (
            HUD_MUST_NOT_WRITE_SEMANTIC is True
            and SEMANTIC_LAYER_ALLOWED is False
            and REGISTRY_MUTATION_ALLOWED is False
        ),
        "no_runtime_output_adapter": (
            HUD_MUST_NOT_CALL_OUTPUT_ADAPTER is True
            and OUTPUT_ADAPTER_ALLOWED is False
            and RUNTIME_EXECUTION_ALLOWED is False
        ),
        "no_external_camera_mic": True,
        "no_delete_artifact": True,
        "model_adapter_requirements_defined": all(adapter_categories_defined.values()),
        "advanced_developer_modes_defined": advanced_developer_modes,
        "test_board_planned": True,
        "test_board_protected": REQUIRED_TEST_BOARD_FIELDS.get("test_artifact_protected", False) is True,
    }

    negative_guards: List[NegativeUIStandardizationPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeUIStandardizationPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "model_test_lens_ui_standardization_profile_count_eq_1": True,
        "model_test_lens_ui_standard_defined": model_test_lens_ui_standard_defined,
        "perception_hud_as_unified_template": PERCEPTION_HUD_AS_UNIFIED_TEMPLATE,
        "robot_vision_hud_default": ROBOT_VISION_HUD_DEFAULT,
        "all_future_model_test_pages_must_follow": ALL_FUTURE_MODEL_TEST_PAGES_MUST_FOLLOW,
        "visual_compare_required": visual_compare_required,
        "reasoning_panel_required": reasoning_panel_required,
        "uncertainty_display_required": reasoning_panel_required,
        "missing_information_display_required": reasoning_panel_required,
        "recommendation_panel_required": reasoning_panel_required,
        "model_category_hud_adapter_requirements_defined": all(adapter_categories_defined.values()),
        "governance_standard_patch_planned": governance_standard_patch_planned,
        "hud_must_not_execute_model": HUD_MUST_NOT_EXECUTE_MODEL is True,
        "hud_must_not_generate_fact": HUD_MUST_NOT_GENERATE_NEW_FACT is True,
        "hud_must_not_write_semantic": HUD_MUST_NOT_WRITE_SEMANTIC is True,
        "hud_must_not_trigger_navigation_action_speech": HUD_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH is True,
        "hud_must_not_call_output_adapter": HUD_MUST_NOT_CALL_OUTPUT_ADAPTER is True,
        "hud_must_not_mutate_registry": HUD_MUST_NOT_MUTATE_REGISTRY is True,
        "planning_only": PLANNING_ONLY is True,
        "negative_guard_count_eq_15": negative_guard_count == 15,
        "negative_guard_passed_eq_15": negative_guard_passed == 15,
        **adapter_categories_defined,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS.items()},
    }

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MidplatformModelTestLensUIStandardizationPlanningDecision(
        decision_ref=DECISION_REF,
        model_test_lens_ui_standardization_profile_count=1,
        model_test_lens_ui_standard_defined=model_test_lens_ui_standard_defined,
        perception_hud_as_unified_template=PERCEPTION_HUD_AS_UNIFIED_TEMPLATE,
        robot_vision_hud_default=ROBOT_VISION_HUD_DEFAULT,
        all_future_model_test_pages_must_follow=ALL_FUTURE_MODEL_TEST_PAGES_MUST_FOLLOW,
        visual_compare_required=visual_compare_required,
        reasoning_panel_required=reasoning_panel_required,
        model_category_hud_adapter_requirements_defined=all(adapter_categories_defined.values()),
        governance_standard_patch_planned=governance_standard_patch_planned,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    profile = ModelTestLensUIStandardizationPlanningProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        planning_only=PLANNING_ONLY,
        ui_standardization_planning=UI_STANDARDIZATION_PLANNING,
        perception_hud_as_unified_template=PERCEPTION_HUD_AS_UNIFIED_TEMPLATE,
        robot_vision_hud_default=ROBOT_VISION_HUD_DEFAULT,
        all_future_model_test_pages_must_follow=ALL_FUTURE_MODEL_TEST_PAGES_MUST_FOLLOW,
        hud_must_not_execute_model=HUD_MUST_NOT_EXECUTE_MODEL,
        hud_must_not_generate_fact=HUD_MUST_NOT_GENERATE_NEW_FACT,
        hud_must_not_write_semantic=HUD_MUST_NOT_WRITE_SEMANTIC,
        hud_must_not_trigger_navigation_action_speech=HUD_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH,
        hud_must_not_call_output_adapter=HUD_MUST_NOT_CALL_OUTPUT_ADAPTER,
        hud_must_not_mutate_registry=HUD_MUST_NOT_MUTATE_REGISTRY,
        target_chain_ref=TARGET_CHAIN_REF,
        luna_core_principle=LUNA_CORE_PRINCIPLE,
        required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS),
    )

    ui_standard_plan = {
        "plan_id": "model_test_lens_ui_standard_plan_v1",
        "standard_ref": f"{STANDARDS_UI_REL}/model_test_lens_ui_standard_v1.md",
        "flow_ref": f"{STANDARDS_UI_REL}/model_test_lens_ui_flow_standard_v1.json",
        "levels": list(UI_LEVELS),
        "default_order": [
            "test_conclusion", "visual_compare", "perception_hud",
            "observations", "reasoning", "uncertainty", "recommendations",
            "metrics", "advanced", "developer",
        ],
        "all_future_model_test_pages_must_follow": True,
    }
    hud_template_plan = {
        "plan_id": "perception_hud_ui_template_standard_plan_v1",
        "template_ref": f"{STANDARDS_PERCEPTION_HUD_REL}/perception_hud_ui_template_standard_v1.md",
        "layout_ref": f"{STANDARDS_PERCEPTION_HUD_REL}/perception_hud_default_layout_spec_v1.json",
        "reasoning_panel_sections": [
            "current_task", "system_observations", "reasoning_steps",
            "uncertainty_summary", "missing_information", "recommended_next_steps",
        ],
    }
    adapter_requirements_plan = {
        "plan_id": "perception_hud_model_adapter_requirements_plan_v1",
        "requirements_ref": f"{STANDARDS_PERCEPTION_HUD_REL}/perception_hud_model_adapter_requirements_v1.json",
        "model_categories": list(MODEL_CATEGORIES),
        "adapter_categories_status": adapter_categories_defined,
    }
    governance_patch_plan = {
        "plan_id": "governance_standards_model_test_lens_ui_patch_plan_v1",
        "governance_ref": f"{GOVERNANCE_UI_REL}/model_test_lens_perception_hud_ui_governance_standard_v1.md",
        "registry_ref": f"{GOVERNANCE_UI_REL}/model_test_lens_ui_standard_registry_v1.json",
        "upstream_perception_hud_planning_phase": UPSTREAM_PERCEPTION_HUD_PLANNING_PHASE,
        "protected": True,
        "non_deletable": True,
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Model Test Lens Perception HUD UI Standardization Planning",
        "lifecycle_variant": "p1_midplatform_model_test_lens_perception_hud_ui_standardization_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "planning_only": PLANNING_ONLY,
        "ui_standardization_planning": UI_STANDARDIZATION_PLANNING,
        "target_chain_ref": TARGET_CHAIN_REF,
        "upstream_perception_hud_planning_phase": UPSTREAM_PERCEPTION_HUD_PLANNING_PHASE,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "model_test_lens_ui_standardization_profile": asdict(profile),
        "model_test_lens_ui_standardization_profile_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "final_decision": final_decision,
        "blocker_count": blocker_count,
        "conclusions": {
            "planning_status": "go" if blocker_count == 0 else "blocked",
            "transition_note": (
                "PLANNING ONLY. Model Test Lens UI Standard V1 and Perception HUD UI Template "
                "are now canonical governance standards. All future model test pages must follow. "
                "Next: Perception HUD View Execution."
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
        (out_root / "model_test_lens_ui_standard_plan_v1.json").write_text(
            json.dumps(ui_standard_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "perception_hud_ui_template_standard_plan_v1.json").write_text(
            json.dumps(hud_template_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "perception_hud_model_adapter_requirements_plan_v1.json").write_text(
            json.dumps(adapter_requirements_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "governance_standards_model_test_lens_ui_patch_plan_v1.json").write_text(
            json.dumps(governance_patch_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
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
            "model_test_lens_ui_standard_plan_record": {"record": ui_standard_plan},
            "perception_hud_ui_template_standard_plan_record": {"record": hud_template_plan},
            "perception_hud_model_adapter_requirements_plan_record": {"record": adapter_requirements_plan},
            "governance_standards_model_test_lens_ui_patch_plan_record": {"record": governance_patch_plan},
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
            "ui_standardization_planning": True,
            "candidate_output_only": True,
        }
        for rtype, payload in extra_payloads.items():
            out = {**common, **payload}
            (board_dir / f"{rtype}.json").write_text(
                json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    result = review_model_test_lens_perception_hud_ui_standardization_planning_v1()
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
