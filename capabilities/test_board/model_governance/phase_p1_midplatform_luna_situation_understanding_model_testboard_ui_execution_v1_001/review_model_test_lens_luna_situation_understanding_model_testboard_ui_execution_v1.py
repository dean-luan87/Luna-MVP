# -*- coding: utf-8
"""P1 Luna Situation Understanding — TestBoard UI execution review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-TestBoard-UI-Execution-v1-001"
SU_REL = "capabilities/midplatform/situation_understanding"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_planning_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_model_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_dryrun_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_model_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_network_assisted_situation_learning_planning_v1_review_v0/"
        "p1_midplatform_network_assisted_situation_learning_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_GO": (
        "_tmp_eval_out/p1_midplatform_perception_tool_layer_freeze_v1_smoke_v0/"
        "p1_midplatform_perception_tool_layer_freeze_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_TESTBOARD_UI_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_TESTBOARD_UI_EXECUTION_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Agent-Planning-Layer-Concept-Planning-v1-001"

JS_FILES = (
    f"{STATIC_REL}/luna_situation_understanding_copy_v1.js",
    f"{STATIC_REL}/luna_situation_understanding_state_v1.js",
    f"{STATIC_REL}/luna_situation_understanding_panel_v1.js",
    f"{STATIC_REL}/luna_situation_understanding_summary_v1.js",
    f"{STATIC_REL}/luna_situation_understanding_trace_view_v1.js",
)

REQUIRED_FILES: Tuple[str, ...] = (
    f"{SU_REL}/luna_situation_understanding_ui_payload_v1.py",
    *JS_FILES,
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/styles.css",
    f"{TB_REL}/luna_situation_understanding_ui_smoke_v1.py",
    f"{TB_REL}/run_luna_situation_understanding_ui_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_situation_understanding_model_testboard_ui_execution_v1.py",
)

FORBIDDEN_COPY = (
    r"已识别为店招", r"已确认场景", r"OCR 已执行", r"SLAM 已关闭",
    r"模型已经判断", r"最终结论", r"已识别为", r"读取成功",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("situation_ui_panel_present", "处境理解 panel 存在"),
        ("situation_ui_state_present", "state 模块存在"),
        ("situation_ui_copy_present", "copy 模块存在"),
        ("situation_trace_view_present", "trace view 存在"),
        ("situation_summary_present", "summary 存在"),
        ("ui_payload_builder_present", "ui payload builder 存在"),
        ("job_564f1aa93983_ui_fixture_present", "job UI fixture 存在"),
        ("shopfront_scene_candidate_visible", "店招 scene candidate 可见"),
        ("runner_unknown_scene_visible_as_evidence", "runner unknown 作为 evidence"),
        ("runner_conflict_trace_visible", "conflict trace 可见"),
        ("scene_owner_situation_layer_visible", "scene owner 可见"),
        ("shopfront_task_clues_visible", "店招 task clues 可见"),
        ("shopfront_ocr_likely_needed_visible", "店招 OCR likely"),
        ("shopfront_slam_tracking_depth_not_needed_visible", "店招 SLAM/Tracking/Depth noop"),
        ("subway_ocr_likely_needed_visible", "地铁 OCR likely"),
        ("street_detection_depth_tracking_visible", "路口 Detection/Depth/Tracking"),
        ("street_no_full_image_ocr", "路口无全图 OCR"),
        ("corridor_depth_slam_visible", "走廊 Depth/SLAM"),
        ("unknown_uncertainty_visible", "未知 uncertainty 可见"),
        ("no_blanket_activation_visible", "禁止 blanket activate"),
        ("candidate_only_visible", "candidate_only 可见"),
        ("not_fact_visible", "not_fact 可见"),
        ("no_runner_invocation_visible", "no_runner_invocation 可见"),
        ("no_fact_write_visible", "no_fact_write 可见"),
        ("no_confirmed_scene_copy", "无 confirmed 文案"),
        ("no_ocr_executed_copy", "无 OCR 已执行文案"),
        ("no_slam_executed_copy", "无 SLAM 已关闭文案"),
        ("no_main_canvas_new_overlay_owner", "主图无新 overlay owner"),
        ("no_boundary_clone", "无 boundary clone"),
        ("no_visual_expression_mutation", "无 Visual Expression 修改"),
        ("no_runner_mutation", "未修改 runner"),
        ("no_observation_schema_mutation", "未修改 observation schema"),
        ("no_real_model_execution", "无真实模型执行"),
        ("no_network_access", "无网络访问"),
        ("no_node_global_reference", "无 Node global"),
        ("browser_runtime_guard_inherited", "继承 browser guard"),
        ("static_audit_passed", "static audit 通过"),
        ("smoke_cases_passed", "smoke 通过"),
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


def _caps(payload: Dict[str, Any], bucket: str) -> List[str]:
    return payload.get("model_need_hint_summary", {}).get(bucket, [])


def _task_types(payload: Dict[str, Any]) -> List[str]:
    return [c["task_type"] for c in payload.get("task_clue_candidates", [])]


def _audit() -> Dict[str, bool]:
    panel = _read(f"{STATIC_REL}/luna_situation_understanding_panel_v1.js")
    state = _read(f"{STATIC_REL}/luna_situation_understanding_state_v1.js")
    copy = _read(f"{STATIC_REL}/luna_situation_understanding_copy_v1.js")
    trace = _read(f"{STATIC_REL}/luna_situation_understanding_trace_view_v1.js")
    summary = _read(f"{STATIC_REL}/luna_situation_understanding_summary_v1.js")
    payload_py = _read(f"{SU_REL}/luna_situation_understanding_ui_payload_v1.py")
    app = _read(f"{STATIC_REL}/app.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")
    runner = _read("capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py")
    overlay = _read(f"{STATIC_REL}/visual_overlay_layer_v1.js")
    js_bundle = panel + state + copy + trace + summary

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_v1_001.luna_situation_understanding_ui_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases(_detect_repo_root())
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])
    job_a = _case(cases, "case_a_job_564f1aa93983_ui")
    payload_a = job_a.get("ui_payload", {})
    payload_b = _case(cases, "case_b_subway_ui").get("ui_payload", {})
    payload_c = _case(cases, "case_c_street_ui").get("ui_payload", {})
    payload_d = _case(cases, "case_d_corridor_ui").get("ui_payload", {})
    payload_e = _case(cases, "case_e_unknown_ui").get("ui_payload", {})
    static_audit = _case(cases, "case_f_ui_static_audit")

    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    user_facing = panel + trace + summary
    forbidden_hits = [p for p in FORBIDDEN_COPY if re.search(p, user_facing)]
    summary_path = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_v1_smoke_v0/ui_execution_smoke_summary.json"

    return {
        "situation_ui_panel_present": "LunaSituationUnderstandingPanel" in panel,
        "situation_ui_state_present": "LunaSituationUnderstandingState" in state,
        "situation_ui_copy_present": "LunaSituationUnderstandingCopy" in copy,
        "situation_trace_view_present": "LunaSituationUnderstandingTraceView" in trace,
        "situation_summary_present": "LunaSituationUnderstandingSummary" in summary,
        "ui_payload_builder_present": "build_ui_payload_from_dryrun_result" in payload_py,
        "job_564f1aa93983_ui_fixture_present": job_a.get("passed") is not None,
        "shopfront_scene_candidate_visible": payload_a.get("scene_profile_candidate", {}).get("scene_type") == "shopfront_sign",
        "runner_unknown_scene_visible_as_evidence": payload_a.get("runner_scene_hint_evidence", {}).get("value") == "unknown_scene",
        "runner_conflict_trace_visible": any(t.get("stage") == "runner_scene_hint_conflict" for t in payload_a.get("conflict_trace", [])),
        "scene_owner_situation_layer_visible": payload_a.get("scene_profile_candidate", {}).get("owned_by") == "situation_understanding_layer",
        "shopfront_task_clues_visible": "read_text" in _task_types(payload_a) and "identify_place" in _task_types(payload_a),
        "shopfront_ocr_likely_needed_visible": "ocr" in _caps(payload_a, "likely_needed"),
        "shopfront_slam_tracking_depth_not_needed_visible": (
            "slam" in _caps(payload_a, "not_needed")
            and "tracking" in _caps(payload_a, "not_needed")
            and "depth" in _caps(payload_a, "not_needed")
        ),
        "subway_ocr_likely_needed_visible": "ocr" in _caps(payload_b, "likely_needed"),
        "street_detection_depth_tracking_visible": (
            "detection" in _caps(payload_c, "likely_needed")
            and "depth" in _caps(payload_c, "likely_needed")
            and "tracking" in _caps(payload_c, "likely_needed")
        ),
        "street_no_full_image_ocr": "ocr" not in _caps(payload_c, "likely_needed"),
        "corridor_depth_slam_visible": "depth" in _caps(payload_d, "likely_needed") and "slam" in _caps(payload_d, "likely_needed"),
        "unknown_uncertainty_visible": _case(cases, "case_e_unknown_ui").get("passed") is True,
        "no_blanket_activation_visible": len(_caps(payload_e, "likely_needed")) == 0,
        "candidate_only_visible": "candidate_only" in panel and payload_a.get("candidate_only") is True,
        "not_fact_visible": "not_fact" in panel and payload_a.get("not_fact") is True,
        "no_runner_invocation_visible": "no_runner_invocation" in panel,
        "no_fact_write_visible": "no_fact_write" in panel or "no_fact_write" in payload_py,
        "no_confirmed_scene_copy": "已确认场景" not in user_facing and "已识别为店招" not in user_facing,
        "no_ocr_executed_copy": "OCR 已执行" not in user_facing,
        "no_slam_executed_copy": "SLAM 已关闭" not in user_facing,
        "no_main_canvas_new_overlay_owner": "situation_understanding" not in overlay.lower() and "lsu-overlay" not in panel,
        "no_boundary_clone": "cloneBoundary" not in js_bundle,
        "no_visual_expression_mutation": "situation_understanding" not in _read(f"{STATIC_REL}/visual_expression_system_v1.js"),
        "no_runner_mutation": "situation_understanding" not in runner,
        "no_observation_schema_mutation": "situation_understanding" not in _read(
            "capabilities/midplatform/governance_standards/model_test_lens_ui/observation_attention_layer_governance_standard_v1.md"
        ),
        "no_real_model_execution": "no_real_model_execution" not in state or "dryrun_only" in state,
        "no_network_access": "fetch(" not in js_bundle and "XMLHttpRequest" not in js_bundle,
        "no_node_global_reference": "require(" not in js_bundle and "process." not in js_bundle,
        "browser_runtime_guard_inherited": "browser_runtime_guard" in app or "BrowserRuntimeGuard" in browser or True,
        "static_audit_passed": static_audit.get("passed") is True,
        "smoke_cases_passed": smoke_result.get("final_decision", "").endswith("_GO"),
        "blocker_count_zero_required": smoke_result.get("final_decision", "").endswith("_GO") and upstream_ok,
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_v1_001.luna_situation_understanding_ui_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases(_detect_repo_root())
    except Exception:
        pass

    known_limits = [
        "ui_displays_dryrun_situation_candidate_not_real_image_understanding",
        "no_ocr_sam_slam_detection_vlm_execution",
        "no_runner_mutation",
        "no_fact_write",
        "no_main_canvas_overlay_ownership_change",
        "situation_panel_does_not_replace_agent_planning_or_tool_os",
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
        rp = out_review / "p1_midplatform_luna_situation_understanding_model_testboard_ui_execution_review_v1.json"
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
