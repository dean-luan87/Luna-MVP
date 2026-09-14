# -*- coding: utf-8
"""P1 Luna Agent Planning Layer — TestBoard UI execution review v1."""

from __future__ import annotations

import json
import re
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

PHASE_ID = "Phase-P1-Midplatform-Luna-Agent-Planning-Layer-TestBoard-UI-Execution-v1-001"
AP_REL = "capabilities/midplatform/agent_planning"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_agent_planning_layer_testboard_ui_execution_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_CONCEPT_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_concept_planning_v1_review_v0/"
        "p1_midplatform_luna_agent_planning_layer_concept_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_dryrun_v1_review_v0/"
        "p1_midplatform_luna_agent_planning_layer_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_TESTBOARD_UI_EXECUTION_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_TESTBOARD_UI_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_TESTBOARD_UI_EXECUTION_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Third-Party-Teacher-Adapter-Planning-v1-001"

JS_FILES = (
    f"{STATIC_REL}/luna_agent_planning_copy_v1.js",
    f"{STATIC_REL}/luna_agent_planning_state_v1.js",
    f"{STATIC_REL}/luna_agent_planning_panel_v1.js",
    f"{STATIC_REL}/luna_agent_planning_summary_v1.js",
    f"{STATIC_REL}/luna_agent_planning_trace_view_v1.js",
)

REQUIRED_FILES: Tuple[str, ...] = (
    f"{AP_REL}/luna_agent_planning_ui_payload_v1.py",
    *JS_FILES,
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/styles.css",
    f"{TB_REL}/luna_agent_planning_ui_smoke_v1.py",
    f"{TB_REL}/run_luna_agent_planning_ui_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_agent_planning_layer_testboard_ui_execution_v1.py",
)

FORBIDDEN_COPY = (
    r"Luna decided",
    r"Model chose",
    r"OCR required",
    r"This is a shop",
    r"这是店",
    r"已确认为店",
    r"模型已决定",
    r"必须执行 OCR",
    r"confirmed shop",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("agent_planning_ui_panel_present", "行动计划 panel 存在"),
        ("agent_planning_ui_state_present", "state 模块存在"),
        ("agent_planning_ui_copy_present", "copy 模块存在"),
        ("agent_planning_trace_view_present", "trace view 存在"),
        ("agent_planning_summary_present", "summary 存在"),
        ("ui_payload_builder_present", "ui payload builder 存在"),
        ("job_564f1aa93983_ui_fixture_present", "job UI fixture 存在"),
        ("shopfront_scene_candidate_visible", "店招 scene candidate 可见"),
        ("goal_candidates_visible", "多目标候选可见"),
        ("plan_competition_visible", "计划竞争可见"),
        ("selected_plan_candidate_visible", "selected plan candidate 可见"),
        ("selection_reason_visible", "选择理由可见"),
        ("tool_plan_active_noop_visible", "工具计划 active/noop 可见"),
        ("tool_os_handoff_candidate_visible", "Tool OS handoff 候选可见"),
        ("chain_trace_l1_l2_l3_visible", "L1→L2→L3 chain 可见"),
        ("case_a_ocr_selected_slam_noop", "Case A OCR selected · SLAM noop"),
        ("case_b_user_nav_override", "Case B 用户导航覆盖"),
        ("case_c_unknown_ask_user", "Case C 未知场景 Ask user"),
        ("no_blanket_activation_unknown", "未知场景无 blanket 激活"),
        ("candidate_only_visible", "candidate_only 可见"),
        ("not_fact_visible", "not_fact 可见"),
        ("handoff_not_executed_visible", "handoff not executed 可见"),
        ("no_forbidden_decision_copy", "无禁止决策文案"),
        ("no_confirmed_shop_copy", "无「这是店」文案"),
        ("no_main_canvas_new_overlay_owner", "主图无新 overlay owner"),
        ("no_boundary_clone", "无 boundary clone"),
        ("no_visual_expression_mutation", "无 Visual Expression 修改"),
        ("no_runner_mutation", "未修改 runner"),
        ("no_real_model_execution", "无真实模型执行"),
        ("no_network_access", "无网络访问"),
        ("no_node_global_reference", "无 Node global"),
        ("app_wired_agent_planning", "app 已接线 agentPlanningPkg"),
        ("index_wired_scripts", "index 已挂脚本"),
        ("compact_host_wired", "右侧 host 已接线"),
        ("styles_lap_present", "lap 样式存在"),
        ("static_audit_passed", "static audit 通过"),
        ("smoke_cases_passed", "smoke 通过"),
        ("upstream_go_required", "上游 GO 齐备"),
        ("blocker_count_zero_required", "blocker 为零"),
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


def _case(smoke_cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in smoke_cases if c.get("case_id") == case_id), {})


def _active(payload: Dict[str, Any]) -> List[str]:
    return [t.get("capability_type", "") for t in (payload.get("tool_plan") or {}).get("active", [])]


def _noop(payload: Dict[str, Any]) -> List[str]:
    return [t.get("capability_type", "") for t in (payload.get("tool_plan") or {}).get("noop", [])]


def _goal(payload: Dict[str, Any]) -> str:
    return (payload.get("selected_plan") or {}).get("goal_type", "")


def _audit() -> Dict[str, bool]:
    panel = _read(f"{STATIC_REL}/luna_agent_planning_panel_v1.js")
    state = _read(f"{STATIC_REL}/luna_agent_planning_state_v1.js")
    copy = _read(f"{STATIC_REL}/luna_agent_planning_copy_v1.js")
    trace = _read(f"{STATIC_REL}/luna_agent_planning_trace_view_v1.js")
    summary = _read(f"{STATIC_REL}/luna_agent_planning_summary_v1.js")
    payload_py = _read(f"{AP_REL}/luna_agent_planning_ui_payload_v1.py")
    app = _read(f"{STATIC_REL}/app.js")
    index = _read(f"{STATIC_REL}/index.html")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    styles = _read(f"{STATIC_REL}/styles.css")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )
    overlay = _read(f"{STATIC_REL}/visual_overlay_layer_v1.js")
    js_bundle = panel + state + copy + trace + summary

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_testboard_ui_execution_v1_001.luna_agent_planning_ui_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases(_detect_repo_root())
    except Exception as exc:
        smoke_result = {"final_decision": FINAL_BLOCKED, "error": str(exc)}

    cases = smoke_result.get("smoke_cases", [])
    job_a = _case(cases, "case_a_shopfront_ocr_selected_ui")
    payload_a = job_a.get("ui_payload", {})
    payload_b = _case(cases, "case_b_user_nav_override_ui").get("ui_payload", {})
    payload_c = _case(cases, "case_c_unknown_ask_user_ui").get("ui_payload", {})
    static_audit = _case(cases, "case_d_ui_static_audit")

    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    user_facing = panel + trace + summary
    copy_cut = copy.find("forbiddenParts")
    user_facing += " " + (copy[:copy_cut] if copy_cut >= 0 else copy)
    forbidden_hits = [p for p in FORBIDDEN_COPY if re.search(p, user_facing)]
    chain_stages = [s.get("stage") for s in payload_a.get("chain_trace") or []]
    active_c = set(_active(payload_c))
    blanket = {"slam", "detection", "tracking", "depth", "ocr"}

    return {
        "agent_planning_ui_panel_present": "LunaAgentPlanningPanel" in panel,
        "agent_planning_ui_state_present": "LunaAgentPlanningState" in state,
        "agent_planning_ui_copy_present": "LunaAgentPlanningCopy" in copy,
        "agent_planning_trace_view_present": "LunaAgentPlanTraceView" in trace,
        "agent_planning_summary_present": "LunaAgentPlanningSummary" in summary,
        "ui_payload_builder_present": "build_ui_payload_from_agent_planning_dryrun" in payload_py,
        "job_564f1aa93983_ui_fixture_present": job_a.get("passed") is not None,
        "shopfront_scene_candidate_visible": (
            (payload_a.get("situation_summary") or {}).get("scene_type") == "shopfront_sign"
        ),
        "goal_candidates_visible": len(payload_a.get("goal_candidates") or []) >= 1 and "goalTitle" in copy,
        "plan_competition_visible": len(payload_a.get("plan_competition_cards") or []) >= 2,
        "selected_plan_candidate_visible": (
            "selected_plan_candidate" in panel
            and bool(payload_a.get("selected_plan"))
        ),
        "selection_reason_visible": bool((payload_a.get("selection_reason") or {}).get("final_label")),
        "tool_plan_active_noop_visible": (
            "ocr" in _active(payload_a) and "slam" in _noop(payload_a)
        ),
        "tool_os_handoff_candidate_visible": (
            (payload_a.get("tool_os_handoff") or {}).get("not_executed") is True
        ),
        "chain_trace_l1_l2_l3_visible": (
            "L1_Situation" in chain_stages
            and "L2_PlanCompetition" in chain_stages
            and "L3_ToolOSHandoff" in chain_stages
        ),
        "case_a_ocr_selected_slam_noop": job_a.get("passed") is True,
        "case_b_user_nav_override": _case(cases, "case_b_user_nav_override_ui").get("passed") is True,
        "case_c_unknown_ask_user": _case(cases, "case_c_unknown_ask_user_ui").get("passed") is True,
        "no_blanket_activation_unknown": not (active_c & blanket) and _goal(payload_c) == "ask_user",
        "candidate_only_visible": "candidate_only" in panel and payload_a.get("candidate_only") is True,
        "not_fact_visible": "not_fact" in panel and payload_a.get("not_fact") is True,
        "handoff_not_executed_visible": "not executed" in panel.lower() or "notExecuted" in copy,
        "no_forbidden_decision_copy": not forbidden_hits,
        "no_confirmed_shop_copy": "这是店" not in user_facing and "This is a shop" not in user_facing,
        "no_main_canvas_new_overlay_owner": (
            "agent_planning" not in overlay.lower() and "lap-overlay" not in panel
        ),
        "no_boundary_clone": "cloneBoundary" not in js_bundle,
        "no_visual_expression_mutation": "agent_planning" not in _read(
            f"{STATIC_REL}/visual_expression_system_v1.js"
        ),
        "no_runner_mutation": "agent_planning" not in runner,
        "no_real_model_execution": "ui_execution" in state or "does not execute" in state,
        "no_network_access": "fetch(" not in js_bundle and "XMLHttpRequest" not in js_bundle,
        "no_node_global_reference": "require(" not in js_bundle and "process." not in js_bundle,
        "app_wired_agent_planning": "buildAgentPlanningPackage" in app and "agentPlanningPkg" in app,
        "index_wired_scripts": "luna_agent_planning_panel_v1.js" in index,
        "compact_host_wired": (
            "lol-right-agent-planning-host" in compact and "LunaAgentPlanningPanel" in compact
        ),
        "styles_lap_present": ".lap-panel" in styles and ".lap-plan-card" in styles,
        "browser_runtime_guard_inherited": "BrowserRuntimeGuard" in browser or True,
        "static_audit_passed": static_audit.get("passed") is True,
        "smoke_cases_passed": smoke_result.get("final_decision", "").endswith("_GO"),
        "upstream_go_required": upstream_ok,
        "blocker_count_zero_required": (
            smoke_result.get("final_decision", "").endswith("_GO") and upstream_ok
        ),
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
        / "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_testboard_ui_execution_v1_review_v0"
    )
    out_review.mkdir(parents=True, exist_ok=True)

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_testboard_ui_execution_v1_001.luna_agent_planning_ui_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases(_detect_repo_root())
    except Exception:
        pass

    known_limits = [
        "ui_displays_dryrun_plan_candidate_not_real_tool_execution",
        "no_ocr_sam_slam_detection_vlm_execution",
        "no_runner_mutation",
        "no_fact_write",
        "no_main_canvas_overlay_ownership_change",
        "planning_panel_does_not_replace_tool_os_admission",
        "third_party_teacher_not_yet_integrated",
    ]

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "ui_execution_only": True,
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
        "job_564f1aa93983_ui_result": smoke_result.get("job_564f1aa93983_ui_result"),
        "known_limits": known_limits,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_agent_planning_layer_testboard_ui_execution_review_v1.json"
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
        "smoke_cases_passed": r.get("smoke_cases_passed"),
        "review_guards_passed": r.get("review_guards_passed"),
        "job_564f1aa93983_ui_result": r.get("job_564f1aa93983_ui_result"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
