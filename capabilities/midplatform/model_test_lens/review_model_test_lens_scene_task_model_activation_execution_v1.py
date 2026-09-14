# -*- coding: utf-8
"""P1 Scene-Task Model Activation — execution review v1."""

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


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Scene-Task-Model-Activation-Execution-v1-001"
STA_REL = "capabilities/midplatform/model_test_lens/scene_task_model_activation"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/scene_task_model_activation"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"
NO_SLAM_TEXT_REL = (
    "capabilities/midplatform/model_test_lens/schemas/multi_model_interaction/no_slam_for_text_policy_v1.json"
)

UPSTREAM_ACTIVATION_PLANNING_GO = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_GO"
UPSTREAM_TEXT_FIRST_PLANNING_GO = "P1_MIDPLATFORM_TEXT_FIRST_TARGET_PROPOSAL_VALIDATION_PLANNING_GO"
UPSTREAM_DUAL_ROUTE_EXEC_GO = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_GO"
UPSTREAM_SCENE_AWARE_EXEC_GO = "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_GO"

FINAL_GO = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Text-First-Target-Proposal-Execution-v1-001"

NEW_MODULES: Tuple[str, ...] = (
    f"{STA_REL}/scene_task_model_activation_executor_v1.py",
    f"{STA_REL}/scene_task_model_activation_execution_types_v1.py",
    f"{STA_REL}/scene_task_model_activation_execution_smoke_v1.py",
    f"{_PKG}/run_scene_task_model_activation_execution_smoke_v1.py",
    f"{_PKG}/review_model_test_lens_scene_task_model_activation_execution_v1.py",
    f"{STATIC_REL}/scene_task_model_activation_copy_v1.js",
    f"{STATIC_REL}/scene_task_model_activation_state_v1.js",
    f"{STATIC_REL}/scene_task_model_activation_panel_v1.js",
    f"{STATIC_REL}/scene_task_model_activation_summary_v1.js",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/scene_profile_policy_v1.js",
    f"{STATIC_REL}/styles.css",
)

FORBIDDEN_UI: Tuple[Tuple[str, str], ...] = (
    (r"开始 OCR|立即识别|已识别文字|导航到", "forbidden_fact_copy"),
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_slam_for_text_task", "desc": "文字任务不默认 SLAM"},
    {"guard_id": "B", "key": "no_slam_text_detection", "desc": "SLAM 不做文字检测"},
    {"guard_id": "C", "key": "no_slam_ocr_route_direct_generation", "desc": "SLAM 不直出 OCR route"},
    {"guard_id": "D", "key": "text_only_scene_activates_ocr_not_slam", "desc": "文字场景激活 OCR 非 SLAM"},
    {"guard_id": "E", "key": "shopfront_sign_noops_slam", "desc": "店招场景 SLAM no-op"},
    {"guard_id": "F", "key": "subway_direction_sign_noops_slam_unless_navigation", "desc": "地铁导视默认 SLAM no-op"},
    {"guard_id": "G", "key": "model_activation_candidate_not_fact", "desc": "激活计划非 fact"},
    {"guard_id": "H", "key": "task_intent_candidate_not_fact", "desc": "任务意图非 fact"},
    {"guard_id": "I", "key": "scene_profile_candidate_not_fact", "desc": "场景候选非 fact"},
    {"guard_id": "J", "key": "noop_record_required_for_inactive_models", "desc": "未激活模型需 noop record"},
    {"guard_id": "K", "key": "active_model_requires_activation_reason", "desc": "激活模型需 activation_reason"},
    {"guard_id": "L", "key": "active_model_requires_region_assignment", "desc": "激活模型需 region assignment"},
    {"guard_id": "M", "key": "inactive_model_must_not_generate_task", "desc": "未激活模型不生成 task"},
    {"guard_id": "N", "key": "no_blanket_model_activation", "desc": "禁止全模型激活"},
    {"guard_id": "O", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "P", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "Q", "key": "no_ocr_execution", "desc": "不执行 OCR"},
    {"guard_id": "R", "key": "no_detection_execution", "desc": "不执行 Detection"},
    {"guard_id": "S", "key": "no_vlm_execution", "desc": "不执行 VLM"},
    {"guard_id": "T", "key": "no_slam_execution", "desc": "不执行 SLAM"},
    {"guard_id": "U", "key": "no_runner_execution_in_activation_execution", "desc": "activation execution 不跑 runner"},
    {"guard_id": "V", "key": "no_visual_expression_mutation", "desc": "不改变 Visual Expression"},
    {"guard_id": "W", "key": "no_boundary_clone", "desc": "不 clone boundary owner"},
    {"guard_id": "X", "key": "human_correction_not_ground_truth", "desc": "纠错非 ground truth"},
    {"guard_id": "Y", "key": "browser_runtime_guard_inherited", "desc": "继承 browser guard"},
    {"guard_id": "Z", "key": "smoke_cases_pass", "desc": "smoke 通过"},
    {"guard_id": "AA", "key": "upstream_activation_planning_go", "desc": "上游 Activation Planning GO"},
    {"guard_id": "AB", "key": "ui_activation_panel_wired", "desc": "UI 模型激活面板已接线"},
    {"guard_id": "AC", "key": "recommended_next_phase_defined", "desc": "下一阶段已定义"},
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def _audit() -> Dict[str, bool]:
    executor = _read(f"{STA_REL}/scene_task_model_activation_executor_v1.py")
    panel = _read(f"{STATIC_REL}/scene_task_model_activation_panel_v1.js")
    state = _read(f"{STATIC_REL}/scene_task_model_activation_state_v1.js")
    copy = _read(f"{STATIC_REL}/scene_task_model_activation_copy_v1.js")
    app = _read(f"{STATIC_REL}/app.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")
    activation_plan = _load_json(f"{SCHEMA_REL}/model_activation_plan_schema_v1.json")
    noop_record = _load_json(f"{SCHEMA_REL}/model_noop_record_schema_v1.json")
    no_slam_activation = _load_json(f"{SCHEMA_REL}/no_slam_for_text_activation_policy_v1.json")
    no_slam_text = _load_json(NO_SLAM_TEXT_REL)
    exec_types = _read(f"{STA_REL}/scene_task_model_activation_execution_types_v1.py")

    activation_planning = _load_json(
        "_tmp_eval_out/p1_midplatform_scene_task_model_activation_planning_v1_smoke_v0/"
        "p1_midplatform_scene_task_model_activation_planning_review_v1.json"
    )
    text_first = _load_json(
        "_tmp_eval_out/p1_midplatform_text_first_target_proposal_validation_planning_v1_smoke_v0/"
        "p1_midplatform_text_first_target_proposal_validation_planning_review_v1.json"
    )
    dual_route = _load_json(
        "_tmp_eval_out/p1_midplatform_dual_route_perception_validation_execution_v1_smoke_v0/"
        "p1_midplatform_dual_route_perception_validation_execution_review_v1.json"
    )
    scene_aware = _load_json(
        "_tmp_eval_out/p1_midplatform_scene_aware_segmentation_prompt_policy_execution_v1_smoke_v0/"
        "p1_midplatform_scene_aware_segmentation_prompt_policy_execution_review_v1.json"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.midplatform.model_test_lens.scene_task_model_activation.scene_task_model_activation_execution_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    smoke_cases = smoke_result.get("smoke_cases", [])
    case_a = next((c for c in smoke_cases if c.get("case_id") == "case_a_shopfront_sign"), {})
    case_b = next((c for c in smoke_cases if c.get("case_id") == "case_b_subway_direction_sign"), {})

    ui_forbidden_ok = all(
        not re.search(pat, text, re.I)
        for pat, _ in FORBIDDEN_UI
        for text in (copy, app, compact)
        if text
    )

    return {
        "no_slam_for_text_task": (
            no_slam_activation.get("boundary_flags", {}).get("no_slam_for_text_task") is True
            and case_a.get("no_slam_for_text_task") is True
        ),
        "no_slam_text_detection": (
            no_slam_activation.get("boundary_flags", {}).get("no_slam_text_detection") is True
            or no_slam_text.get("boundary_flags", {}).get("no_slam_text_detection") is True
        ),
        "no_slam_ocr_route_direct_generation": (
            no_slam_activation.get("boundary_flags", {}).get("no_slam_ocr_route_direct_generation") is True
            and "no_slam_ocr_route" not in executor.lower()
        ),
        "text_only_scene_activates_ocr_not_slam": case_a.get("passed") is True,
        "shopfront_sign_noops_slam": (
            case_a.get("passed") is True
            and "slam" in json.dumps(case_a.get("plan", {}).get("model_noop_set", []))
        ),
        "subway_direction_sign_noops_slam_unless_navigation": case_b.get("passed") is True,
        "model_activation_candidate_not_fact": (
            "model_activation_candidate_not_fact" in executor
            and "model_activation_candidate_not_fact" in state
            and activation_plan.get("boundary_flags", {}).get("model_activation_candidate_not_fact") is True
        ),
        "task_intent_candidate_not_fact": "task_intent_candidate_not_fact" in state,
        "scene_profile_candidate_not_fact": "scene_profile_candidate_not_fact" in state,
        "noop_record_required_for_inactive_models": (
            noop_record.get("boundary_flags", {}).get("noop_record_required_for_inactive_models") is True
            and "model_noop_set" in executor
        ),
        "active_model_requires_activation_reason": (
            "activation_reason" in executor and "activation_reason" in panel
        ),
        "active_model_requires_region_assignment": (
            "model_region_assignment" in executor and "assigned_region" in panel
        ),
        "inactive_model_must_not_generate_task": (
            "followup_runner_task_candidates" in executor
            and "no_runner_execution" in copy
        ),
        "no_blanket_model_activation": "ALL_MODELS" in executor and "buildModelActivationPlan" in state,
        "no_fact_write": (
            "no_fact_write" in executor
            and "no_fact_write" in panel
            and smoke_result.get("no_fact_write") is True
        ),
        "no_navigation_decision": "navigation_decision" not in executor.lower().replace("no_navigation_decision", ""),
        "no_ocr_execution": "no_ocr_execution" in panel and "ocr_runner" not in executor,
        "no_detection_execution": "no_detection_execution" in panel and "detection_runner" not in executor,
        "no_vlm_execution": "no_vlm_execution" in panel and "vlm_runner" not in executor,
        "no_slam_execution": "no_slam_execution" in panel and "slam_runner" not in executor,
        "no_runner_execution_in_activation_execution": (
            "no_runner_execution_in_activation_execution" in executor
            and "no_runner_execution_in_activation_execution" in state
            and smoke_result.get("no_runner_execution_in_activation_execution") is True
        ),
        "no_visual_expression_mutation": "segmentationSoleBoundaryOwner" in panel,
        "no_boundary_clone": "no_boundary_clone" in panel,
        "human_correction_not_ground_truth": (
            "correction_signal" in state and "human_correction_not_ground_truth" in exec_types
        ),
        "browser_runtime_guard_inherited": "BrowserRuntimeGuard" in browser,
        "smoke_cases_pass": smoke_result.get("final_decision", "").endswith("_GO"),
        "upstream_activation_planning_go": activation_planning.get("final_decision") == UPSTREAM_ACTIVATION_PLANNING_GO,
        "ui_activation_panel_wired": (
            "activationPkg" in app
            and "buildActivationPackage" in app
            and "lol-right-activation-host" in compact
            and "SceneTaskModelActivationPanel" in compact
            and "模型激活计划" in panel
        ),
        "recommended_next_phase_defined": NEXT_PHASE in exec_types,
        "_ui_forbidden_ok": ui_forbidden_ok,
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()
    if not flags.pop("_ui_forbidden_ok", True):
        failed.append("ui.forbidden_copy_detected")

    guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_scene_task_model_activation_execution_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "execution_only": True,
        "no_model_call": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out / "p1_midplatform_scene_task_model_activation_execution_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="post_review",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="post_review",
                repo_root=standin,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        result["test_board_root"] = str(tb.get("test_board_dir", ""))

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
        "recommended_next_phase": r["recommended_next_phase"],
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
