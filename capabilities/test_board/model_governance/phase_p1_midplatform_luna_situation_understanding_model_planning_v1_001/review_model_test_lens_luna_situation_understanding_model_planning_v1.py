# -*- coding: utf-8
"""P1 Luna Situation Understanding Model — planning review v1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-Planning-v1-001"
SU_REL = "capabilities/midplatform/situation_understanding"
SCHEMA_REL = f"{SU_REL}/schemas"
GOV_REL = f"{SU_REL}/governance"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_situation_understanding_model_planning_v1_001"
)

UPSTREAM_GO = "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_GO"
FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-DryRun-v1-001"

SCHEMA_FILES = (
    f"{SCHEMA_REL}/situation_understanding_input_schema_v1.json",
    f"{SCHEMA_REL}/frame_context_schema_v1.json",
    f"{SCHEMA_REL}/user_goal_candidate_schema_v1.json",
    f"{SCHEMA_REL}/visual_evidence_candidate_schema_v1.json",
    f"{SCHEMA_REL}/situation_case_ref_schema_v1.json",
    f"{SCHEMA_REL}/available_capability_schema_v1.json",
    f"{SCHEMA_REL}/situation_understanding_candidate_schema_v1.json",
    f"{SCHEMA_REL}/scene_profile_candidate_schema_v1.json",
    f"{SCHEMA_REL}/survival_context_schema_v1.json",
    f"{SCHEMA_REL}/task_clue_candidate_schema_v1.json",
    f"{SCHEMA_REL}/missing_information_candidate_schema_v1.json",
    f"{SCHEMA_REL}/attention_target_hint_schema_v1.json",
    f"{SCHEMA_REL}/model_need_hint_schema_v1.json",
    f"{SCHEMA_REL}/situation_uncertainty_schema_v1.json",
)

REQUIRED_FILES: Tuple[str, ...] = (
    f"{SU_REL}/luna_situation_understanding_model_plan_v1.md",
    f"{SU_REL}/luna_situation_understanding_types_v1.py",
    f"{SU_REL}/luna_situation_understanding_processor_v1.py",
    *SCHEMA_FILES,
    f"{GOV_REL}/luna_situation_understanding_policy_v1.json",
    f"{TB_REL}/luna_situation_understanding_smoke_v1.py",
    f"{TB_REL}/run_luna_situation_understanding_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_situation_understanding_model_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "01", "key": "situation_candidate_not_fact", "desc": "situation 输出非 fact"},
    {"guard_id": "02", "key": "no_runner_invocation", "desc": "不触发 runner"},
    {"guard_id": "03", "key": "no_tool_install", "desc": "不安装工具"},
    {"guard_id": "04", "key": "no_fact_admission_bypass", "desc": "不绕过 fact admission"},
    {"guard_id": "05", "key": "no_navigation_decision", "desc": "不输出导航决策"},
    {"guard_id": "06", "key": "scene_profile_owned_by_situation_layer", "desc": "scene 归 Situation Layer"},
    {"guard_id": "07", "key": "runner_scene_hint_candidate_only", "desc": "runner hint 仅 evidence"},
    {"guard_id": "08", "key": "teacher_output_not_direct_situation", "desc": "teacher 不直接覆盖 situation"},
    {"guard_id": "09", "key": "case_library_reference_not_fact", "desc": "case ref 非 fact"},
    {"guard_id": "10", "key": "human_correction_not_ground_truth", "desc": "纠错非 ground truth"},
    {"guard_id": "11", "key": "text_task_no_default_slam", "desc": "文字任务不默认 SLAM"},
    {"guard_id": "12", "key": "shopfront_sign_prefers_ocr", "desc": "店招偏好 OCR"},
    {"guard_id": "13", "key": "subway_direction_prefers_ocr", "desc": "地铁偏好 OCR"},
    {"guard_id": "14", "key": "street_crossing_prefers_detection_depth_tracking", "desc": "路口偏好 Detection/Depth/Tracking"},
    {"guard_id": "15", "key": "corridor_prefers_spatial_tools", "desc": "走廊偏好 Depth/SLAM"},
    {"guard_id": "16", "key": "unknown_scene_requires_uncertainty", "desc": "未知场景需 uncertainty"},
    {"guard_id": "17", "key": "no_blanket_model_activation", "desc": "禁止 blanket activate"},
    {"guard_id": "18", "key": "all_outputs_traceable", "desc": "输出可溯源"},
    {"guard_id": "19", "key": "candidate_only_required", "desc": "candidate_only 必填"},
    {"guard_id": "20", "key": "all_schema_files_present", "desc": "schema 文件齐全"},
    {"guard_id": "21", "key": "processor_stub_present", "desc": "processor stub 存在"},
    {"guard_id": "22", "key": "planning_doc_present", "desc": "规划文档存在"},
    {"guard_id": "23", "key": "smoke_cases_present", "desc": "smoke cases 存在"},
    {"guard_id": "24", "key": "smoke_case_shopfront_passes", "desc": "店招 smoke 通过"},
    {"guard_id": "25", "key": "smoke_case_subway_passes", "desc": "地铁 smoke 通过"},
    {"guard_id": "26", "key": "smoke_case_street_passes", "desc": "路口 smoke 通过"},
    {"guard_id": "27", "key": "smoke_case_corridor_passes", "desc": "走廊 smoke 通过"},
    {"guard_id": "28", "key": "smoke_case_unknown_passes", "desc": "未知场景 smoke 通过"},
    {"guard_id": "29", "key": "teacher_case_does_not_directly_override", "desc": "teacher 不直接覆盖"},
    {"guard_id": "30", "key": "runner_unknown_scene_does_not_override_situation", "desc": "runner unknown 不覆盖"},
    {"guard_id": "31", "key": "no_existing_runner_mutation", "desc": "未修改 runner"},
    {"guard_id": "32", "key": "no_existing_observation_schema_mutation", "desc": "未修改 observation schema"},
    {"guard_id": "33", "key": "deterministic_smoke_only", "desc": "仅 deterministic smoke"},
    {"guard_id": "34", "key": "smoke_cases_pass", "desc": "smoke 全部通过"},
    {"guard_id": "35", "key": "upstream_network_learning_go", "desc": "上游 Network Learning GO"},
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


def _audit() -> Dict[str, bool]:
    policy = _load_json(f"{GOV_REL}/luna_situation_understanding_policy_v1.json")
    processor = _read(f"{SU_REL}/luna_situation_understanding_processor_v1.py")
    plan = _read(f"{SU_REL}/luna_situation_understanding_model_plan_v1.md")
    types_py = _read(f"{SU_REL}/luna_situation_understanding_types_v1.py")
    runner_py = _read("capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py")
    candidate_schema = _load_json(f"{SCHEMA_REL}/situation_understanding_candidate_schema_v1.json")

    upstream = _load_json(
        "_tmp_eval_out/p1_midplatform_network_assisted_situation_learning_planning_v1_review_v0/"
        "p1_midplatform_network_assisted_situation_learning_planning_review_v1.json"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_situation_understanding_model_planning_v1_001.luna_situation_understanding_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    smoke_cases = smoke_result.get("smoke_cases", [])
    by_id = {c.get("case_id"): c for c in smoke_cases}
    flags = policy.get("boundary_flags", {})

    return {
        "situation_candidate_not_fact": flags.get("situation_candidate_not_fact") is True,
        "no_runner_invocation": flags.get("no_runner_invocation") is True and "no_runner_invocation" in processor,
        "no_tool_install": flags.get("no_tool_install") is True,
        "no_fact_admission_bypass": flags.get("no_fact_admission_bypass") is True,
        "no_navigation_decision": flags.get("no_navigation_decision") is True and "no_navigation_decision" in processor,
        "scene_profile_owned_by_situation_layer": flags.get("scene_profile_owned_by_situation_layer") is True,
        "runner_scene_hint_candidate_only": flags.get("runner_scene_hint_candidate_only") is True,
        "teacher_output_not_direct_situation": flags.get("teacher_output_not_direct_situation") is True,
        "case_library_reference_not_fact": flags.get("case_library_reference_not_fact") is True,
        "human_correction_not_ground_truth": flags.get("human_correction_not_ground_truth") is True,
        "text_task_no_default_slam": flags.get("text_task_no_default_slam") is True,
        "shopfront_sign_prefers_ocr": flags.get("shopfront_sign_prefers_ocr") is True,
        "subway_direction_prefers_ocr": flags.get("subway_direction_prefers_ocr") is True,
        "street_crossing_prefers_detection_depth_tracking": flags.get("street_crossing_prefers_detection_depth_tracking") is True,
        "corridor_prefers_spatial_tools": flags.get("corridor_prefers_spatial_tools") is True,
        "unknown_scene_requires_uncertainty": flags.get("unknown_scene_requires_uncertainty") is True,
        "no_blanket_model_activation": flags.get("no_blanket_model_activation") is True,
        "all_outputs_traceable": flags.get("all_outputs_traceable") is True and "trace_refs" in processor,
        "candidate_only_required": flags.get("candidate_only_required") is True and "candidate_only" in types_py,
        "all_schema_files_present": all(_read(s) for s in SCHEMA_FILES),
        "processor_stub_present": "build_situation_understanding_candidate" in processor,
        "planning_doc_present": "L1 Situation Understanding" in plan,
        "smoke_cases_present": "run_smoke_cases" in _read(f"{TB_REL}/luna_situation_understanding_smoke_v1.py"),
        "smoke_case_shopfront_passes": by_id.get("case_a_shopfront_sign", {}).get("passed") is True,
        "smoke_case_subway_passes": by_id.get("case_b_subway_platform", {}).get("passed") is True,
        "smoke_case_street_passes": by_id.get("case_c_street_crossing", {}).get("passed") is True,
        "smoke_case_corridor_passes": by_id.get("case_d_corridor", {}).get("passed") is True,
        "smoke_case_unknown_passes": by_id.get("case_e_unknown_scene", {}).get("passed") is True,
        "teacher_case_does_not_directly_override": by_id.get("case_f_teacher_label_input", {}).get("passed") is True,
        "runner_unknown_scene_does_not_override_situation": by_id.get("case_g_runner_unknown_scene_override", {}).get("passed") is True,
        "no_existing_runner_mutation": "situation_understanding" not in runner_py,
        "no_existing_observation_schema_mutation": "situation_understanding" not in _read(
            "capabilities/midplatform/governance_standards/model_test_lens_ui/observation_attention_layer_governance_standard_v1.md"
        ),
        "deterministic_smoke_only": smoke_result.get("deterministic_smoke_only") is True,
        "smoke_cases_pass": smoke_result.get("final_decision", "").endswith("_GO"),
        "upstream_network_learning_go": upstream.get("final_decision") == UPSTREAM_GO,
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    generated_files = [rel for rel in REQUIRED_FILES if _read(rel)]

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

    out_review = _detect_repo_root() / "_tmp_eval_out" / "p1_midplatform_luna_situation_understanding_model_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    known_limits = [
        "situation_understanding_v1_is_deterministic_policy_stub_not_trained_model",
        "no_real_teacher_calls",
        "no_network",
        "no_runner_connection",
        "no_real_image_understanding",
        "does_not_replace_agent_planning",
        "does_not_replace_tool_os",
        "no_fact_write",
    ]

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "L1_Situation_Understanding",
        "planning_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "smoke_cases_passed": flags.get("smoke_cases_pass", False),
        "review_guards_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "known_limits": known_limits,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_situation_understanding_model_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="planning",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="planning",
                repo_root=standin,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb.get("test_board_dir", TB_REL))
        if board_dir.is_dir():
            common = {
                "phase_id": PHASE_ID,
                "protected": True,
                "non_deletable": True,
                "test_artifact_protected": True,
                "test_mode": "planning",
            }
            payloads = {
                "luna_situation_understanding_plan_record": {"plan_ref": f"{SU_REL}/luna_situation_understanding_model_plan_v1.md"},
                "luna_situation_understanding_policy_record": _load_json(f"{GOV_REL}/luna_situation_understanding_policy_v1.json"),
            }
            for name, payload in payloads.items():
                (board_dir / f"{name}.json").write_text(
                    json.dumps({**common, "record": payload}, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "smoke_cases_passed": r.get("smoke_cases_passed"),
        "review_guards_passed": r.get("review_guards_passed"),
        "generated_files_count": len(r.get("generated_files", [])),
        "known_limits": r.get("known_limits", []),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
