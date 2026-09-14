# -*- coding: utf-8 -*-
"""P1 Scene-Task Model Activation — planning review v1."""

from __future__ import annotations

import json
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

PHASE_ID = "Phase-P1-Midplatform-Scene-Task-Model-Activation-Planning-v1-001"
STA_REL = "capabilities/midplatform/model_test_lens/scene_task_model_activation"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/scene_task_model_activation"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
NO_SLAM_TEXT_REL = (
    "capabilities/midplatform/model_test_lens/schemas/multi_model_interaction/no_slam_for_text_policy_v1.json"
)

UPSTREAM_TEXT_FIRST_PLANNING_GO = "P1_MIDPLATFORM_TEXT_FIRST_TARGET_PROPOSAL_VALIDATION_PLANNING_GO"
UPSTREAM_DUAL_ROUTE_EXEC_GO = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_GO"
UPSTREAM_SCENE_AWARE_EXEC_GO = "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_GO"
UPSTREAM_MOBILESAM_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO"

FINAL_GO = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_BLOCKED"
PLANNING_ENDPOINT = "model_activation_plan_candidate"
NEXT_PHASE = "Phase-P1-Midplatform-Scene-Task-Model-Activation-Execution-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{STA_REL}/scene_task_model_activation_plan_v1.md",
    f"{STA_REL}/scene_task_model_activation_types_v1.py",
    f"{STA_REL}/scene_task_model_activation_smoke_v1.py",
    f"{SCHEMA_REL}/scene_profile_candidate_schema_v1.json",
    f"{SCHEMA_REL}/task_intent_candidate_schema_v1.json",
    f"{SCHEMA_REL}/model_activation_plan_schema_v1.json",
    f"{SCHEMA_REL}/model_noop_record_schema_v1.json",
    f"{SCHEMA_REL}/model_region_assignment_schema_v1.json",
    f"{SCHEMA_REL}/scene_task_model_activation_policy_v1.json",
    f"{SCHEMA_REL}/no_slam_for_text_activation_policy_v1.json",
    f"{GOV_REL}/scene_task_model_activation_governance_standard_v1.md",
    f"{_PKG}/run_scene_task_model_activation_smoke_v1.py",
    f"{_PKG}/review_model_test_lens_scene_task_model_activation_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "scene_profile_candidate_schema_record",
    "task_intent_candidate_schema_record",
    "model_activation_plan_schema_record",
    "model_noop_record_schema_record",
    "model_region_assignment_schema_record",
    "scene_task_model_activation_policy_record",
    "no_slam_for_text_activation_policy_record",
    "scene_task_model_activation_plan_record",
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
    {"guard_id": "T", "key": "no_runner_execution_in_planning", "desc": "planning 不跑 runner"},
    {"guard_id": "U", "key": "no_visual_expression_mutation", "desc": "不改变 Visual Expression"},
    {"guard_id": "V", "key": "no_boundary_clone", "desc": "不 clone boundary owner"},
    {"guard_id": "W", "key": "human_correction_not_ground_truth", "desc": "纠错非 ground truth"},
    {"guard_id": "X", "key": "browser_runtime_guard_inherited", "desc": "继承 browser guard"},
    {"guard_id": "Y", "key": "five_smoke_cases_defined", "desc": "五类 smoke 已定义"},
    {"guard_id": "Z", "key": "smoke_cases_pass", "desc": "smoke 通过"},
    {"guard_id": "AA", "key": "planning_endpoint_defined", "desc": "本阶段终点已定义"},
    {"guard_id": "AB", "key": "upstream_text_first_planning_go", "desc": "上游 Text-First Planning GO"},
    {"guard_id": "AC", "key": "governance_standard_defined", "desc": "治理标准已定义"},
    {"guard_id": "AD", "key": "recommended_next_phase_defined", "desc": "下一阶段已定义"},
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _load_upstream(rel: str) -> Dict[str, Any]:
    return _load_json(rel)


def _audit() -> Dict[str, bool]:
    plan = _read(f"{STA_REL}/scene_task_model_activation_plan_v1.md")
    types_py = _read(f"{STA_REL}/scene_task_model_activation_types_v1.py")
    gov = _read(f"{GOV_REL}/scene_task_model_activation_governance_standard_v1.md")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")
    vis_gov = _read(
        "capabilities/midplatform/governance_standards/model_test_lens_ui/"
        "visual_expression_system_governance_standard_v1.md"
    )

    scene_profile = _load_json(f"{SCHEMA_REL}/scene_profile_candidate_schema_v1.json")
    task_intent = _load_json(f"{SCHEMA_REL}/task_intent_candidate_schema_v1.json")
    activation_plan = _load_json(f"{SCHEMA_REL}/model_activation_plan_schema_v1.json")
    noop_record = _load_json(f"{SCHEMA_REL}/model_noop_record_schema_v1.json")
    region_assign = _load_json(f"{SCHEMA_REL}/model_region_assignment_schema_v1.json")
    activation_policy = _load_json(f"{SCHEMA_REL}/scene_task_model_activation_policy_v1.json")
    no_slam_activation = _load_json(f"{SCHEMA_REL}/no_slam_for_text_activation_policy_v1.json")
    no_slam_text = _load_json(NO_SLAM_TEXT_REL)

    text_first = _load_upstream(
        "_tmp_eval_out/p1_midplatform_text_first_target_proposal_validation_planning_v1_smoke_v0/"
        "p1_midplatform_text_first_target_proposal_validation_planning_review_v1.json"
    )
    dual_route = _load_upstream(
        "_tmp_eval_out/p1_midplatform_dual_route_perception_validation_execution_v1_smoke_v0/"
        "p1_midplatform_dual_route_perception_validation_execution_review_v1.json"
    )
    scene_aware = _load_upstream(
        "_tmp_eval_out/p1_midplatform_scene_aware_segmentation_prompt_policy_execution_v1_smoke_v0/"
        "p1_midplatform_scene_aware_segmentation_prompt_policy_execution_review_v1.json"
    )
    mobilesam = _load_upstream(
        "_tmp_eval_out/p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0/"
        "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_review.json"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.midplatform.model_test_lens.scene_task_model_activation.scene_task_model_activation_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )

        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED, "failed_checks": ["smoke.import_error"]}

    smoke_cases = smoke_result.get("smoke_cases", [])
    case_a = next((c for c in smoke_cases if c.get("case_id") == "case_a_shopfront_sign"), {})
    case_b = next((c for c in smoke_cases if c.get("case_id") == "case_b_subway_direction_sign"), {})

    return {
        "no_slam_for_text_task": (
            no_slam_activation.get("boundary_flags", {}).get("no_slam_for_text_task") is True
            and activation_policy.get("boundary_flags", {}).get("no_slam_for_text_task") is True
            and "no_slam_for_text_task" in plan
        ),
        "no_slam_text_detection": (
            no_slam_activation.get("boundary_flags", {}).get("no_slam_text_detection") is True
            or no_slam_text.get("boundary_flags", {}).get("no_slam_text_detection") is True
        ),
        "no_slam_ocr_route_direct_generation": (
            no_slam_activation.get("boundary_flags", {}).get("no_slam_ocr_route_direct_generation") is True
            or "no_slam_ocr_route" in plan
            or "slam_for_text" in json.dumps(activation_policy.get("forbidden_patterns", []))
        ),
        "text_only_scene_activates_ocr_not_slam": (
            case_a.get("passed") is True
            and case_a.get("no_slam_for_text_task") is True
        ),
        "shopfront_sign_noops_slam": (
            no_slam_activation.get("boundary_flags", {}).get("shopfront_sign_noops_slam") is True
            and case_a.get("shopfront_sign_noops_slam") is True
        ),
        "subway_direction_sign_noops_slam_unless_navigation": (
            no_slam_activation.get("boundary_flags", {}).get(
                "subway_direction_sign_noops_slam_unless_navigation"
            )
            is True
            and case_b.get("subway_direction_sign_noops_slam_unless_navigation") is True
        ),
        "model_activation_candidate_not_fact": (
            activation_plan.get("boundary_flags", {}).get("model_activation_candidate_not_fact") is True
            and activation_plan.get("planning_endpoint") == PLANNING_ENDPOINT
        ),
        "task_intent_candidate_not_fact": (
            task_intent.get("boundary_flags", {}).get("task_intent_candidate_not_fact") is True
        ),
        "scene_profile_candidate_not_fact": (
            scene_profile.get("boundary_flags", {}).get("scene_profile_candidate_not_fact") is True
        ),
        "noop_record_required_for_inactive_models": (
            noop_record.get("boundary_flags", {}).get("noop_record_required_for_inactive_models") is True
            and activation_plan.get("boundary_flags", {}).get("noop_record_required_for_inactive_models") is True
        ),
        "active_model_requires_activation_reason": (
            region_assign.get("boundary_flags", {}).get("active_model_requires_activation_reason") is True
            and "activation_reason" in json.dumps(activation_plan.get("field_definitions", {}))
        ),
        "active_model_requires_region_assignment": (
            region_assign.get("boundary_flags", {}).get("active_model_requires_region_assignment") is True
            and "model_region_assignment" in activation_plan.get("required_fields", [])
        ),
        "inactive_model_must_not_generate_task": (
            noop_record.get("boundary_flags", {}).get("inactive_model_must_not_generate_task") is True
            and "inactive_model_generates_task" in json.dumps(activation_plan.get("forbidden_operations", []))
        ),
        "no_blanket_model_activation": (
            activation_policy.get("boundary_flags", {}).get("no_blanket_model_activation") is True
            and "blanket_activate_all_models" in json.dumps(activation_policy.get("forbidden_patterns", []))
        ),
        "no_fact_write": (
            activation_plan.get("boundary_flags", {}).get("no_fact_write") is True
            and activation_policy.get("boundary_flags", {}).get("no_fact_write") is True
            and smoke_result.get("no_fact_write") is True
        ),
        "no_navigation_decision": (
            activation_policy.get("boundary_flags", {}).get("no_navigation_decision") is True
            and "no_navigation_decision" in gov
        ),
        "no_ocr_execution": (
            smoke_result.get("no_model_call") is True
            and smoke_result.get("planning_only") is True
            and ("不接 runner" in plan or "不跑 runner" in plan or "真实 runner" in plan)
        ),
        "no_detection_execution": (
            smoke_result.get("no_model_call") is True
            and ("不接 runner" in plan or "不跑 runner" in plan)
        ),
        "no_vlm_execution": (
            smoke_result.get("no_model_call") is True
            and ("不接 runner" in plan or "不跑 runner" in plan)
        ),
        "no_runner_execution_in_planning": (
            activation_plan.get("boundary_flags", {}).get("no_runner_execution_in_planning") is True
            and smoke_result.get("no_runner_execution_in_planning") is True
        ),
        "no_visual_expression_mutation": (
            "Visual Expression" in plan
            and ("不改变 Visual Expression" in plan or "no_visual_expression_mutation" in plan)
            and "boundary owner" in vis_gov
        ),
        "no_boundary_clone": (
            "no_boundary_clone" in types_py
            or "boundary owner" in plan
        ),
        "human_correction_not_ground_truth": (
            "human_correction_not_ground_truth" in types_py
            or "纠错非 ground truth" in gov
            or "correction_signal" in json.dumps(task_intent.get("source_enum", []))
        ),
        "browser_runtime_guard_inherited": "BrowserRuntimeGuard" in browser,
        "five_smoke_cases_defined": "Smoke Cases（5）" in plan or len(smoke_result.get("smoke_cases", [])) == 5,
        "smoke_cases_pass": smoke_result.get("final_decision", "").endswith("_GO"),
        "planning_endpoint_defined": (
            PLANNING_ENDPOINT in types_py
            and activation_plan.get("planning_endpoint") == PLANNING_ENDPOINT
        ),
        "upstream_text_first_planning_go": text_first.get("final_decision") == UPSTREAM_TEXT_FIRST_PLANNING_GO,
        "governance_standard_defined": "SceneTaskModelActivationGovernanceStandardV1" in gov,
        "recommended_next_phase_defined": NEXT_PHASE in plan and NEXT_PHASE in types_py,
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()
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
        "p1_midplatform_scene_task_model_activation_planning_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": True,
        "planning_endpoint": PLANNING_ENDPOINT,
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
        rp = out / "p1_midplatform_scene_task_model_activation_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result, test_mode="planning", repo_root=root, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result, test_mode="planning", repo_root=standin, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb["test_board_dir"])
        common = {
            "phase_id": PHASE_ID, "protected": True, "non_deletable": True,
            "deletion_forbidden": True, "test_artifact_protected": True,
            "test_mode": "planning", "scene_task_model_activation_planning": True,
        }
        payloads = {
            "scene_profile_candidate_schema_record": _load_json(
                f"{SCHEMA_REL}/scene_profile_candidate_schema_v1.json"
            ),
            "task_intent_candidate_schema_record": _load_json(
                f"{SCHEMA_REL}/task_intent_candidate_schema_v1.json"
            ),
            "model_activation_plan_schema_record": _load_json(
                f"{SCHEMA_REL}/model_activation_plan_schema_v1.json"
            ),
            "model_noop_record_schema_record": _load_json(
                f"{SCHEMA_REL}/model_noop_record_schema_v1.json"
            ),
            "model_region_assignment_schema_record": _load_json(
                f"{SCHEMA_REL}/model_region_assignment_schema_v1.json"
            ),
            "scene_task_model_activation_policy_record": _load_json(
                f"{SCHEMA_REL}/scene_task_model_activation_policy_v1.json"
            ),
            "no_slam_for_text_activation_policy_record": _load_json(
                f"{SCHEMA_REL}/no_slam_for_text_activation_policy_v1.json"
            ),
            "scene_task_model_activation_plan_record": {
                "plan_ref": f"{STA_REL}/scene_task_model_activation_plan_v1.md"
            },
        }
        for rtype in EXTRA_TEST_BOARD_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": payloads.get(rtype, {"id": rtype})}, indent=2, ensure_ascii=False)
                + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)

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
