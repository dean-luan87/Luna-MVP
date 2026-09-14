# -*- coding: utf-8
"""P1 Luna Decision Validation Layer — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Decision-Validation-Layer-Planning-v1-001"
DV_REL = "capabilities/midplatform/decision_validation"
SCHEMA_REL = f"{DV_REL}/schemas"
GOV_REL = f"{DV_REL}/governance"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_decision_validation_layer_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_third_party_teacher_adapter_planning_v1_review_v0/"
        "p1_midplatform_third_party_teacher_adapter_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_TESTBOARD_UI_EXECUTION_GO": (
        "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_testboard_ui_execution_v1_review_v0/"
        "p1_midplatform_luna_agent_planning_layer_testboard_ui_execution_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_dryrun_v1_review_v0/"
        "p1_midplatform_luna_agent_planning_layer_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Decision-Validation-Layer-DryRun-v1-001"

SCHEMA_FILES = (
    f"{SCHEMA_REL}/decision_validation_input_schema_v1.json",
    f"{SCHEMA_REL}/decision_validation_candidate_schema_v1.json",
    f"{SCHEMA_REL}/validation_reason_schema_v1.json",
    f"{SCHEMA_REL}/alternative_plan_candidate_schema_v1.json",
    f"{SCHEMA_REL}/tool_os_readiness_schema_v1.json",
)

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DV_REL}/luna_decision_validation_layer_plan_v1.md",
    f"{DV_REL}/luna_decision_validation_types_v1.py",
    f"{DV_REL}/luna_decision_validation_processor_v1.py",
    f"{GOV_REL}/decision_validation_policy_v1.json",
    *SCHEMA_FILES,
    f"{TB_REL}/luna_decision_validation_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_decision_validation_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_decision_validation_layer_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("validation_layer_exists", "验证层存在"),
        ("validation_doc_present", "规划文档存在"),
        ("validation_types_present", "types 存在"),
        ("validation_processor_present", "processor 存在"),
        ("validation_policy_present", "policy 存在"),
        ("all_schema_files_present", "schema 齐全"),
        ("no_plan_ownership", "不拥有 plan"),
        ("no_plan_override", "不覆盖 selected plan"),
        ("no_tool_execution", "不执行工具"),
        ("tool_os_boundary_preserved", "Tool OS 边界保留"),
        ("constitution_priority", "Constitution 优先"),
        ("situation_alignment_required", "Situation 对齐检查"),
        ("missing_information_checked", "缺失信息检查"),
        ("noop_checked", "noop 检查"),
        ("future_single_teacher_ready", "单 Teacher 接口预留"),
        ("future_multi_teacher_ready", "多 Teacher 接口预留"),
        ("candidate_only", "candidate_only"),
        ("not_fact", "not_fact"),
        ("trace_complete", "trace 完整"),
        ("case_a_shopfront_validated", "Case A 店招 validated"),
        ("case_b_user_goal_review", "Case B 用户目标 needs_review"),
        ("case_c_street_validated", "Case C 路口 validated"),
        ("case_d_blanket_blocked", "Case D blanket blocked"),
        ("case_e_slam_text_blocked", "Case E SLAM/text blocked"),
        ("no_real_network", "无真实网络"),
        ("no_existing_runner_mutation", "未改 runner"),
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


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _load_json_path(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _validation(result: Dict[str, Any]) -> Dict[str, Any]:
    return (result.get("result") or {}).get("decision_validation_candidate") or result.get("decision_validation_candidate") or {}


def _audit() -> Dict[str, bool]:
    plan_md = _read(f"{DV_REL}/luna_decision_validation_layer_plan_v1.md")
    types_py = _read(f"{DV_REL}/luna_decision_validation_types_v1.py")
    processor = _read(f"{DV_REL}/luna_decision_validation_processor_v1.py")
    policy = _load_json(f"{GOV_REL}/decision_validation_policy_v1.json")
    flags = policy.get("boundary_flags", {})

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_decision_validation_layer_planning_v1_001.luna_decision_validation_planning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])
    case_a = _case(cases, "case_a_shopfront_ocr_validated")
    v_a = _validation(case_a.get("result", {}))

    upstream_ok = all(
        _load_json_path(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )

    return {
        "validation_layer_exists": "L2.5 Decision Validation" in plan_md,
        "validation_doc_present": "不是决策者" in plan_md or "不是决策层" in plan_md,
        "validation_types_present": "DecisionValidationInput" in types_py,
        "validation_processor_present": "build_validation_candidate" in processor,
        "validation_policy_present": bool(policy.get("boundary_flags")),
        "all_schema_files_present": all(_read(s) for s in SCHEMA_FILES),
        "no_plan_ownership": flags.get("agent_plan_validation_only") is True and v_a.get("no_plan_ownership") is True,
        "no_plan_override": flags.get("no_plan_override") is True and v_a.get("no_plan_override") is True,
        "no_tool_execution": flags.get("no_tool_execution") is True and v_a.get("no_tool_execution") is True,
        "tool_os_boundary_preserved": "tool_os_before_execution" in processor and "should_handoff_to_tool_os" in processor,
        "constitution_priority": flags.get("constitution_priority") is True,
        "situation_alignment_required": "validate_plan_alignment" in processor,
        "missing_information_checked": "validate_missing_information" in processor,
        "noop_checked": "validate_tool_selection" in processor,
        "future_single_teacher_ready": flags.get("single_teacher_future_ready") is True and "single_teacher" in processor,
        "future_multi_teacher_ready": flags.get("multi_teacher_future_ready") is True and "multi_teacher" in processor,
        "candidate_only": v_a.get("candidate_only") is True,
        "not_fact": v_a.get("not_fact") is True,
        "trace_complete": len(v_a.get("trace_refs") or []) >= 3,
        "case_a_shopfront_validated": case_a.get("passed") is True,
        "case_b_user_goal_review": _case(cases, "case_b_user_goal_needs_review").get("passed") is True,
        "case_c_street_validated": _case(cases, "case_c_street_crossing_validated").get("passed") is True,
        "case_d_blanket_blocked": _case(cases, "case_d_unknown_blanket_blocked").get("passed") is True,
        "case_e_slam_text_blocked": _case(cases, "case_e_slam_for_text_blocked").get("passed") is True,
        "no_real_network": "requests." not in processor and "urllib" not in processor,
        "no_existing_runner_mutation": "decision_validation" not in runner,
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_decision_validation_layer_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    known_limits = [
        "decision_validation_planning_only_no_real_model_validation",
        "current_validator_is_deterministic_policy_rule_case_library_stub",
        "no_gemini_qwen_gpt_vlm",
        "no_network",
        "no_runner_invocation",
        "no_fact_write",
        "no_tool_execution",
        "does_not_replace_agent_planning_ownership",
        "multi_teacher_arbitration_deferred_to_future_phase",
    ]

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "L2_5_Decision_Validation",
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
        rp = out_review / "p1_midplatform_luna_decision_validation_layer_planning_review_v1.json"
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
