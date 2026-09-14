# -*- coding: utf-8
"""P1 Luna Agent Planning Layer — dry-run review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Agent-Planning-Layer-DryRun-v1-001"
AP_REL = "capabilities/midplatform/agent_planning"
GOV_REL = f"{AP_REL}/governance"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_CONCEPT_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_concept_planning_v1_review_v0/"
        "p1_midplatform_luna_agent_planning_layer_concept_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_dryrun_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_model_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_TESTBOARD_UI_EXECUTION_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Agent-Planning-Layer-TestBoard-UI-Execution-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{AP_REL}/luna_agent_planning_dryrun_adapter_v1.py",
    f"{AP_REL}/luna_agent_planning_processor_v1.py",
    f"{GOV_REL}/luna_agent_planning_dryrun_policy_v1.json",
    f"{GOV_REL}/luna_agent_planning_policy_v1.json",
    f"{TB_REL}/luna_agent_planning_layer_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_agent_planning_layer_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_agent_planning_layer_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("dryrun_adapter_present", "dryrun adapter 存在"),
        ("dryrun_fixtures_present", "fixtures 存在"),
        ("dryrun_policy_present", "dryrun policy 存在"),
        ("l1_to_l2_chain_present", "L1→L2 链路存在"),
        ("plan_competition_present", "plan_competition 存在"),
        ("selected_plan_candidate_present", "selected_plan 存在"),
        ("job_564f1aa93983_fixture_present", "店招 job fixture"),
        ("job_564f1aa93983_l1_shopfront", "L1 修正为 shopfront"),
        ("job_564f1aa93983_l2_ocr_plan", "L2 OCR plan"),
        ("job_564f1aa93983_slam_not_activated", "店招不启动 SLAM"),
        ("shopfront_noops_depth_tracking", "店招 Depth/Tracking noop"),
        ("subway_ocr_no_slam", "地铁 OCR、无 SLAM"),
        ("street_detection_depth_tracking", "路口三工具"),
        ("street_no_full_image_ocr", "路口无全图 OCR"),
        ("user_goal_overrides_scene_default", "用户目标覆盖场景默认"),
        ("user_goal_not_ocr_first", "找入口非 OCR-first"),
        ("l1_drives_l2_all_cases", "全部 case L1 驱动 L2"),
        ("l2_constrains_tools_all_cases", "全部 case L2 约束工具"),
        ("no_blanket_scheduler", "非 blanket 调度器"),
        ("tool_os_handoff_candidate_only", "handoff 仅候选"),
        ("no_tool_execution", "不执行工具"),
        ("no_runner_invocation", "不触发 runner"),
        ("no_fact_write", "不写 fact"),
        ("no_existing_runner_mutation", "未改 runner"),
        ("deterministic_dryrun_only", "仅 deterministic dryrun"),
        ("output_summary_written", "summary 已写"),
        ("dryrun_cases_pass", "dryrun cases 通过"),
        ("upstream_gos_confirmed", "上游 GO 确认"),
    ], start=1)
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    adapter = _read(f"{AP_REL}/luna_agent_planning_dryrun_adapter_v1.py")
    fixtures = _read(f"{TB_REL}/luna_agent_planning_layer_dryrun_fixtures_v1.py")
    policy = _load_json(_detect_repo_root() / f"{GOV_REL}/luna_agent_planning_dryrun_policy_v1.json")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )
    flags = policy.get("boundary_flags", {})

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        dryrun_result = {"final_decision": FINAL_BLOCKED}

    cases = dryrun_result.get("dryrun_cases", [])
    a = _case(cases, "case_a_job_564f1aa93983_shop_sign")
    b = _case(cases, "case_b_subway_find_direction")
    c = _case(cases, "case_c_street_cross_safely")
    d = _case(cases, "case_d_user_goal_overrides_scene")
    a_res = a.get("result") or {}
    b_res = b.get("result") or {}
    c_res = c.get("result") or {}
    d_res = d.get("result") or {}
    job_l2 = dryrun_result.get("job_564f1aa93983_l2_result") or {}
    core = dryrun_result.get("core_validations") or {}

    summary_path = (
        _detect_repo_root()
        / "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_dryrun_v1_smoke_v0/dryrun_summary.json"
    )

    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    a_tools = (a_res.get("tool_plan_summary") or {}).get("active", [])
    a_noops = (a_res.get("tool_plan_summary") or {}).get("noop", [])
    b_tools = (b_res.get("tool_plan_summary") or {}).get("active", [])
    b_noops = (b_res.get("tool_plan_summary") or {}).get("noop", [])
    c_tools = (c_res.get("tool_plan_summary") or {}).get("active", [])
    d_goal = ((d_res.get("selected_plan_candidate") or {}).get("plan_goal_candidate") or {}).get("goal_type")
    d_tools = (d_res.get("tool_plan_summary") or {}).get("active", [])

    return {
        "dryrun_adapter_present": "run_agent_planning_dryrun" in adapter,
        "dryrun_fixtures_present": "fixture_job_564f1aa93983_shop_sign" in fixtures,
        "dryrun_policy_present": flags.get("l1_drives_l2") is True,
        "l1_to_l2_chain_present": "build_agent_planning_input_from_situation" in adapter
        and "run_situation_understanding_dryrun" in adapter,
        "plan_competition_present": "build_plan_competition" in adapter and core.get("plan_competition_present") is True,
        "selected_plan_candidate_present": "selected_plan_candidate" in adapter,
        "job_564f1aa93983_fixture_present": "job_564f1aa93983" in fixtures,
        "job_564f1aa93983_l1_shopfront": job_l2.get("l1_scene") == "shopfront_sign",
        "job_564f1aa93983_l2_ocr_plan": "ocr" in (job_l2.get("active_tools") or a_tools),
        "job_564f1aa93983_slam_not_activated": job_l2.get("slam_not_activated") is True and "slam" not in a_tools,
        "shopfront_noops_depth_tracking": "depth" in a_noops and "tracking" in a_noops,
        "subway_ocr_no_slam": "ocr" in b_tools and "slam" in b_noops and "slam" not in b_tools,
        "street_detection_depth_tracking": "detection" in c_tools and "depth" in c_tools and "tracking" in c_tools,
        "street_no_full_image_ocr": "ocr" not in c_tools,
        "user_goal_overrides_scene_default": d.get("passed") is True and d_goal == "navigate",
        "user_goal_not_ocr_first": not (d_goal in ("read_text", "identify_place") and d_tools == ["ocr"]),
        "l1_drives_l2_all_cases": core.get("l1_drives_l2") is True,
        "l2_constrains_tools_all_cases": core.get("l2_constrains_tools") is True,
        "no_blanket_scheduler": all(
            len(((c.get("result") or {}).get("tool_plan_summary") or {}).get("active", [])) < 6
            for c in cases
        ) if cases else False,
        "tool_os_handoff_candidate_only": all(
            ((c.get("result") or {}).get("tool_os_handoff_candidate") or {}).get("candidate_only") is True
            or ((c.get("result") or {}).get("tool_os_handoff_candidate") or {}).get("not_fact") is True
            for c in cases
        ) if cases else False,
        "no_tool_execution": flags.get("no_tool_execution_in_dryrun") is True
        and a_res.get("no_tool_execution_assertion") is True,
        "no_runner_invocation": flags.get("no_runner_invocation_in_dryrun") is True
        and a_res.get("no_runner_invocation_assertion") is True,
        "no_fact_write": a_res.get("no_fact_write_assertion") is True,
        "no_existing_runner_mutation": "agent_planning" not in runner,
        "deterministic_dryrun_only": dryrun_result.get("deterministic_dryrun_only") is True,
        "output_summary_written": summary_path.is_file(),
        "dryrun_cases_pass": dryrun_result.get("final_decision", "").endswith("_GO"),
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

    out_review = (
        _detect_repo_root()
        / "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_dryrun_v1_review_v0"
    )
    out_review.mkdir(parents=True, exist_ok=True)

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        pass

    known_limits = [
        "dryrun_not_real_tool_execution",
        "l2_still_deterministic_policy_stub",
        "plan_competition_is_heuristic_scoring_not_trained",
        "no_network",
        "no_real_teacher",
        "no_runner_invocation",
        "no_fact_write",
        "models_are_tools_not_luna_brain",
    ]

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "dryrun_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "dryrun_cases_passed": flags.get("dryrun_cases_pass", False),
        "review_guards_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "job_564f1aa93983_l2_result": dryrun_result.get("job_564f1aa93983_l2_result"),
        "core_validations": dryrun_result.get("core_validations"),
        "known_limits": known_limits,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_agent_planning_layer_dryrun_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
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
        "dryrun_cases_passed": r.get("dryrun_cases_passed"),
        "review_guards_passed": r.get("review_guards_passed"),
        "job_564f1aa93983_l2_result": r.get("job_564f1aa93983_l2_result"),
        "core_validations": r.get("core_validations"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
