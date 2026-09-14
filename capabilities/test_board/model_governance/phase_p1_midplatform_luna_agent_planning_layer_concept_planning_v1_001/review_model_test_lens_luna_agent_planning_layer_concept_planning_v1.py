# -*- coding: utf-8
"""P1 Luna Agent Planning Layer — concept planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Agent-Planning-Layer-Concept-Planning-v1-001"
AP_REL = "capabilities/midplatform/agent_planning"
SCHEMA_REL = f"{AP_REL}/schemas"
GOV_REL = f"{AP_REL}/governance"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_agent_planning_layer_concept_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_TESTBOARD_UI_EXECUTION_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_dryrun_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_model_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_planning_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_model_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_CONCEPT_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_CONCEPT_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Agent-Planning-Layer-DryRun-v1-001"

SCHEMA_FILES = (
    f"{SCHEMA_REL}/agent_planning_input_schema_v1.json",
    f"{SCHEMA_REL}/plan_goal_candidate_schema_v1.json",
    f"{SCHEMA_REL}/plan_strategy_schema_v1.json",
    f"{SCHEMA_REL}/agent_plan_step_schema_v1.json",
    f"{SCHEMA_REL}/tool_plan_candidate_schema_v1.json",
    f"{SCHEMA_REL}/noop_tool_plan_candidate_schema_v1.json",
    f"{SCHEMA_REL}/fallback_strategy_schema_v1.json",
    f"{SCHEMA_REL}/ask_user_strategy_schema_v1.json",
    f"{SCHEMA_REL}/stop_condition_schema_v1.json",
    f"{SCHEMA_REL}/tool_os_handoff_candidate_schema_v1.json",
    f"{SCHEMA_REL}/agent_plan_candidate_schema_v1.json",
)

REQUIRED_FILES: Tuple[str, ...] = (
    f"{AP_REL}/luna_agent_planning_layer_concept_plan_v1.md",
    f"{AP_REL}/luna_agent_planning_types_v1.py",
    f"{AP_REL}/luna_agent_planning_processor_v1.py",
    f"{GOV_REL}/luna_agent_planning_policy_v1.json",
    *SCHEMA_FILES,
    f"{TB_REL}/luna_agent_planning_layer_concept_smoke_v1.py",
    f"{TB_REL}/run_luna_agent_planning_layer_concept_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_agent_planning_layer_concept_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("agent_planning_doc_present", "规划文档存在"),
        ("agent_planning_types_present", "types 存在"),
        ("agent_planning_processor_present", "processor 存在"),
        ("agent_planning_policy_present", "policy 存在"),
        ("all_schema_files_present", "schema 齐全"),
        ("smoke_cases_present", "smoke 存在"),
        ("agent_plan_candidate_not_fact", "plan 非 fact"),
        ("no_runner_invocation", "不触发 runner"),
        ("no_tool_execution", "不执行工具"),
        ("no_tool_install", "不安装工具"),
        ("tool_os_handoff_required", "必须 Tool OS handoff"),
        ("runner_admission_required", "需 runner admission"),
        ("fact_admission_required_after_result", "结果需 fact admission"),
        ("situation_input_required", "必须依赖 L1"),
        ("missing_information_drives_plan", "missing info 驱动计划"),
        ("text_goal_prefers_ocr_plan", "文字目标优先 OCR"),
        ("text_goal_no_default_slam_plan", "文字目标不默认 SLAM"),
        ("street_crossing_prefers_risk_assessment_plan", "路口风险计划"),
        ("corridor_navigation_prefers_spatial_plan", "走廊空间计划"),
        ("unknown_scene_asks_user_or_vlm", "未知场景问用户"),
        ("noop_plan_required", "noop plan 必需"),
        ("no_blanket_tool_plan", "禁止 blanket tool plan"),
        ("all_steps_traceable", "steps 可溯源"),
        ("human_correction_not_ground_truth", "纠错非 ground truth"),
        ("shopfront_generates_ocr_plan", "店招 OCR plan"),
        ("shopfront_noops_slam_tracking_depth", "店招 spatial noop"),
        ("subway_generates_ocr_plan", "地铁 OCR plan"),
        ("street_generates_detection_depth_tracking_plan", "路口三工具"),
        ("corridor_generates_depth_slam_plan", "走廊 Depth/SLAM"),
        ("unknown_does_not_blanket_activate", "未知不 blanket"),
        ("unavailable_tool_generates_fallback", "不可用工具 fallback"),
        ("user_goal_can_override_task_clue_with_trace", "user_goal 可覆盖并留 trace"),
        ("no_existing_runner_mutation", "未改 runner"),
        ("no_existing_observation_schema_mutation", "未改 observation schema"),
        ("no_real_model_execution", "无真实模型执行"),
        ("no_network_access", "无网络"),
        ("deterministic_smoke_only", "仅 deterministic smoke"),
        ("smoke_cases_passed", "smoke 通过"),
        ("upstream_gos_confirmed", "上游 GO 确认"),
    ], start=1)
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json_path(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _tools(plan: Dict[str, Any]) -> List[str]:
    return [t.get("capability_type", "") for t in plan.get("tool_plan_candidates", [])]


def _noops(plan: Dict[str, Any]) -> List[str]:
    return [t.get("capability_type", "") for t in plan.get("noop_tool_plan_candidates", [])]


def _audit() -> Dict[str, bool]:
    plan_md = _read(f"{AP_REL}/luna_agent_planning_layer_concept_plan_v1.md")
    types_py = _read(f"{AP_REL}/luna_agent_planning_types_v1.py")
    processor = _read(f"{AP_REL}/luna_agent_planning_processor_v1.py")
    policy = _load_json(f"{GOV_REL}/luna_agent_planning_policy_v1.json")
    smoke_py = _read(f"{TB_REL}/luna_agent_planning_layer_concept_smoke_v1.py")
    runner = _read("capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py")
    flags = policy.get("boundary_flags", {})

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_concept_planning_v1_001.luna_agent_planning_layer_concept_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])
    a = _case(cases, "case_a_shopfront_sign").get("plan", {})
    b = _case(cases, "case_b_subway_platform").get("plan", {})
    c = _case(cases, "case_c_street_crossing").get("plan", {})
    d = _case(cases, "case_d_corridor").get("plan", {})
    e = _case(cases, "case_e_unknown_scene")
    f = _case(cases, "case_f_tool_unavailable")
    g = _case(cases, "case_g_user_goal_override")

    upstream_ok = all(
        _load_json_path(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "agent_planning_doc_present": "L2 Agent Planning" in plan_md,
        "agent_planning_types_present": "AgentPlanCandidate" in types_py,
        "agent_planning_processor_present": "build_agent_plan_candidate" in processor,
        "agent_planning_policy_present": bool(policy.get("boundary_flags")),
        "all_schema_files_present": all(_read(s) for s in SCHEMA_FILES),
        "smoke_cases_present": "run_smoke_cases" in smoke_py,
        "agent_plan_candidate_not_fact": flags.get("agent_plan_candidate_not_fact") is True and a.get("not_fact") is True,
        "no_runner_invocation": flags.get("no_runner_invocation") is True and a.get("no_runner_invocation") is True,
        "no_tool_execution": flags.get("no_tool_execution") is True,
        "no_tool_install": flags.get("no_tool_install") is True,
        "tool_os_handoff_required": flags.get("tool_os_handoff_required") is True and a.get("handoff_to_tool_os_candidate", {}).get("should_handoff") is True,
        "runner_admission_required": flags.get("runner_admission_required") is True,
        "fact_admission_required_after_result": flags.get("fact_admission_required_after_result") is True,
        "situation_input_required": flags.get("situation_input_required") is True and "situation_input_required" in processor,
        "missing_information_drives_plan": flags.get("missing_information_drives_plan") is True,
        "text_goal_prefers_ocr_plan": flags.get("text_goal_prefers_ocr_plan") is True,
        "text_goal_no_default_slam_plan": flags.get("text_goal_no_default_slam_plan") is True,
        "street_crossing_prefers_risk_assessment_plan": flags.get("street_crossing_prefers_risk_assessment_plan") is True,
        "corridor_navigation_prefers_spatial_plan": flags.get("corridor_navigation_prefers_spatial_plan") is True,
        "unknown_scene_asks_user_or_vlm": flags.get("unknown_scene_asks_user_or_vlm") is True,
        "noop_plan_required": flags.get("noop_plan_required") is True,
        "no_blanket_tool_plan": flags.get("no_blanket_tool_plan") is True,
        "all_steps_traceable": flags.get("all_steps_traceable") is True,
        "human_correction_not_ground_truth": flags.get("human_correction_not_ground_truth") is True,
        "shopfront_generates_ocr_plan": "ocr" in _tools(a),
        "shopfront_noops_slam_tracking_depth": "slam" in _noops(a) and "tracking" in _noops(a) and "depth" in _noops(a),
        "subway_generates_ocr_plan": "ocr" in _tools(b),
        "street_generates_detection_depth_tracking_plan": "detection" in _tools(c) and "depth" in _tools(c) and "tracking" in _tools(c),
        "corridor_generates_depth_slam_plan": "depth" in _tools(d) and "slam" in _tools(d),
        "unknown_does_not_blanket_activate": e.get("passed") is True and len(_tools(e.get("plan", {}))) <= 1,
        "unavailable_tool_generates_fallback": f.get("passed") is True,
        "user_goal_can_override_task_clue_with_trace": g.get("passed") is True,
        "no_existing_runner_mutation": "agent_planning" not in runner,
        "no_existing_observation_schema_mutation": "agent_planning" not in _read(
            "capabilities/midplatform/governance_standards/model_test_lens_ui/observation_attention_layer_governance_standard_v1.md"
        ),
        "no_real_model_execution": "no_tool_execution" in processor and smoke_result.get("deterministic_smoke_only") is True,
        "no_network_access": "requests." not in processor and "urllib" not in processor,
        "deterministic_smoke_only": smoke_result.get("deterministic_smoke_only") is True,
        "smoke_cases_passed": smoke_result.get("final_decision", "").endswith("_GO"),
        "upstream_gos_confirmed": upstream_ok,
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_concept_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    known_limits = [
        "l2_concept_planning_only_no_real_tool_execution",
        "agent_planning_v1_is_deterministic_policy_stub_not_trained_model",
        "no_network",
        "no_real_teacher_calls",
        "no_runner_invocation",
        "no_fact_write",
        "does_not_replace_tool_os",
        "does_not_replace_situation_understanding",
        "does_not_replace_final_action_execution",
    ]

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "L2_Agent_Planning",
        "planning_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "smoke_cases_passed": flags.get("smoke_cases_passed", False),
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
        rp = out_review / "p1_midplatform_luna_agent_planning_layer_concept_planning_review_v1.json"
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
        result["test_board_root"] = str(tb.get("test_board_dir", TB_REL))

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
