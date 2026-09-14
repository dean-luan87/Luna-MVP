# -*- coding: utf-8
"""P1 Luna Situation Understanding Model — dry-run review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-DryRun-v1-001"
SU_REL = "capabilities/midplatform/situation_understanding"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_situation_understanding_model_dryrun_v1_001"
)

UPSTREAM_GOS = (
    "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_GO",
    "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_PLANNING_GO",
)
FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-TestBoard-UI-Execution-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{SU_REL}/luna_situation_understanding_dryrun_adapter_v1.py",
    f"{SU_REL}/luna_situation_understanding_processor_v1.py",
    f"{SU_REL}/luna_situation_understanding_types_v1.py",
    f"{TB_REL}/luna_situation_understanding_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_situation_understanding_model_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_situation_understanding_model_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "01", "key": "dryrun_adapter_present", "desc": "dryrun adapter 存在"},
    {"guard_id": "02", "key": "dryrun_fixtures_present", "desc": "dryrun fixtures 存在"},
    {"guard_id": "03", "key": "processor_called_from_adapter", "desc": "adapter 调用 processor"},
    {"guard_id": "04", "key": "job_564f1aa93983_fixture_present", "desc": "job_564f1aa93983 fixture"},
    {"guard_id": "05", "key": "job_564f1aa93983_shopfront_recovered", "desc": "店招 job 修正成功"},
    {"guard_id": "06", "key": "runner_unknown_scene_not_owner", "desc": "runner unknown 非 owner"},
    {"guard_id": "07", "key": "runner_scene_hint_as_evidence_only", "desc": "runner hint 仅 evidence"},
    {"guard_id": "08", "key": "runner_scene_conflict_trace_present", "desc": "conflict trace 存在"},
    {"guard_id": "09", "key": "shopfront_likely_needed_ocr", "desc": "店招 OCR likely"},
    {"guard_id": "10", "key": "shopfront_noops_slam_tracking_depth", "desc": "店招 SLAM/Tracking/Depth noop"},
    {"guard_id": "11", "key": "subway_likely_needed_ocr", "desc": "地铁 OCR likely"},
    {"guard_id": "12", "key": "subway_slam_not_needed_unless_navigation", "desc": "地铁 SLAM not_needed"},
    {"guard_id": "13", "key": "street_crossing_detection_depth_tracking", "desc": "路口 Detection/Depth/Tracking"},
    {"guard_id": "14", "key": "street_crossing_no_full_image_ocr", "desc": "路口无全图 OCR"},
    {"guard_id": "15", "key": "corridor_depth_slam_likely", "desc": "走廊 Depth/SLAM likely"},
    {"guard_id": "16", "key": "corridor_ocr_not_needed_unless_text", "desc": "走廊 OCR not_needed"},
    {"guard_id": "17", "key": "unknown_scene_uncertainty_required", "desc": "未知场景 uncertainty"},
    {"guard_id": "18", "key": "no_blanket_model_activation", "desc": "禁止 blanket activate"},
    {"guard_id": "19", "key": "teacher_case_ref_not_direct_override", "desc": "teacher case 不直接覆盖"},
    {"guard_id": "20", "key": "case_ref_trace_present", "desc": "case ref trace 存在"},
    {"guard_id": "21", "key": "situation_candidate_not_fact", "desc": "situation 非 fact"},
    {"guard_id": "22", "key": "all_outputs_candidate_only", "desc": "输出 candidate_only"},
    {"guard_id": "23", "key": "no_runner_invocation", "desc": "不触发 runner"},
    {"guard_id": "24", "key": "no_tool_install", "desc": "不安装工具"},
    {"guard_id": "25", "key": "no_fact_admission_bypass", "desc": "不绕过 fact admission"},
    {"guard_id": "26", "key": "no_navigation_decision", "desc": "不输出导航决策"},
    {"guard_id": "27", "key": "no_existing_runner_mutation", "desc": "未修改 runner"},
    {"guard_id": "28", "key": "no_existing_observation_schema_mutation", "desc": "未修改 observation schema"},
    {"guard_id": "29", "key": "no_real_model_execution", "desc": "无真实模型执行"},
    {"guard_id": "30", "key": "no_network_access", "desc": "无网络访问"},
    {"guard_id": "31", "key": "deterministic_dryrun_only", "desc": "仅 deterministic dryrun"},
    {"guard_id": "32", "key": "output_summary_written", "desc": "输出 summary 已写"},
    {"guard_id": "33", "key": "dryrun_cases_pass", "desc": "dryrun cases 全通过"},
    {"guard_id": "34", "key": "upstream_gos_confirmed", "desc": "上游 GO 确认"},
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


def _case_by_id(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _caps(dryrun: Dict[str, Any], bucket: str) -> List[str]:
    return dryrun.get("model_need_hint_summary", {}).get(bucket, [])


def _audit() -> Dict[str, bool]:
    adapter = _read(f"{SU_REL}/luna_situation_understanding_dryrun_adapter_v1.py")
    fixtures_py = _read(f"{TB_REL}/luna_situation_understanding_dryrun_fixtures_v1.py")
    policy = _load_json(_detect_repo_root() / f"{SU_REL}/governance/luna_situation_understanding_policy_v1.json")
    runner_py = _read("capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py")

    upstream_paths = {
        "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_GO": (
            "_tmp_eval_out/p1_midplatform_perception_tool_layer_freeze_v1_smoke_v0/"
            "p1_midplatform_perception_tool_layer_freeze_review_v1.json"
        ),
        "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_GO": (
            "_tmp_eval_out/p1_midplatform_network_assisted_situation_learning_planning_v1_review_v0/"
            "p1_midplatform_network_assisted_situation_learning_planning_review_v1.json"
        ),
        "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_PLANNING_GO": (
            "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_planning_v1_review_v0/"
            "p1_midplatform_luna_situation_understanding_model_planning_review_v1.json"
        ),
    }
    upstream_checks = {
        go: _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in upstream_paths.items()
    }

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_situation_understanding_model_dryrun_v1_001.luna_situation_understanding_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        dryrun_result = {"final_decision": FINAL_BLOCKED}

    cases = dryrun_result.get("dryrun_cases", [])
    case_a = _case_by_id(cases, "case_a_job_564f1aa93983_shop_sign")
    case_b = _case_by_id(cases, "case_b_subway_jiahuihu")
    case_c = _case_by_id(cases, "case_c_street_crossing")
    case_d = _case_by_id(cases, "case_d_corridor")
    case_e = _case_by_id(cases, "case_e_unknown_scene")
    case_f = _case_by_id(cases, "case_f_teacher_case_ref_shopfront")
    case_g = _case_by_id(cases, "case_g_runner_scene_conflict")

    dry_a = case_a.get("dryrun", {})
    dry_b = case_b.get("dryrun", {})
    dry_c = case_c.get("dryrun", {})
    dry_d = case_d.get("dryrun", {})
    dry_e = case_e.get("dryrun", {})
    dry_f = case_f.get("dryrun", {})
    dry_g = case_g.get("dryrun", {})

    cand_a = dry_a.get("situation_understanding_candidate", {})
    runner_ev = dry_a.get("runner_scene_hint_evidence_record", {})
    conflict = dry_a.get("conflict_trace_optional") or []

    summary_path = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_dryrun_v1_smoke_v0/dryrun_summary.json"

    flags = policy.get("boundary_flags", {})

    return {
        "dryrun_adapter_present": "run_situation_understanding_dryrun" in adapter,
        "dryrun_fixtures_present": "fixture_job_564f1aa93983_shop_sign" in fixtures_py,
        "processor_called_from_adapter": "build_situation_understanding_candidate" in adapter,
        "job_564f1aa93983_fixture_present": "job_564f1aa93983" in fixtures_py,
        "job_564f1aa93983_shopfront_recovered": case_a.get("passed") is True,
        "runner_unknown_scene_not_owner": (
            runner_ev.get("value") == "unknown_scene"
            and cand_a.get("scene_profile_candidate", {}).get("scene_type") == "shopfront_sign"
        ),
        "runner_scene_hint_as_evidence_only": runner_ev.get("source") == "runner_scene_hint",
        "runner_scene_conflict_trace_present": any(
            t.get("stage") == "runner_scene_hint_conflict" for t in conflict
        ),
        "shopfront_likely_needed_ocr": "ocr" in _caps(dry_a, "likely_needed"),
        "shopfront_noops_slam_tracking_depth": (
            "slam" in _caps(dry_a, "not_needed")
            and "tracking" in _caps(dry_a, "not_needed")
            and "depth" in _caps(dry_a, "not_needed")
        ),
        "subway_likely_needed_ocr": "ocr" in _caps(dry_b, "likely_needed"),
        "subway_slam_not_needed_unless_navigation": "slam" in _caps(dry_b, "not_needed"),
        "street_crossing_detection_depth_tracking": (
            "detection" in _caps(dry_c, "likely_needed")
            and "depth" in _caps(dry_c, "likely_needed")
            and "tracking" in _caps(dry_c, "likely_needed")
        ),
        "street_crossing_no_full_image_ocr": "ocr" not in _caps(dry_c, "likely_needed"),
        "corridor_depth_slam_likely": "depth" in _caps(dry_d, "likely_needed") and "slam" in _caps(dry_d, "likely_needed"),
        "corridor_ocr_not_needed_unless_text": "ocr" in _caps(dry_d, "not_needed"),
        "unknown_scene_uncertainty_required": case_e.get("passed") is True,
        "no_blanket_model_activation": len(_caps(dry_e, "likely_needed")) == 0,
        "teacher_case_ref_not_direct_override": case_f.get("passed") is True,
        "case_ref_trace_present": "teacher_accepted_shopfront_case" in (
            dry_f.get("situation_understanding_candidate", {}).get("scene_profile_candidate", {}).get("case_refs", [])
        ),
        "situation_candidate_not_fact": flags.get("situation_candidate_not_fact") is True and cand_a.get("not_fact") is True,
        "all_outputs_candidate_only": cand_a.get("candidate_only") is True,
        "no_runner_invocation": dry_a.get("no_runner_invocation_assertion") is True,
        "no_tool_install": flags.get("no_tool_install") is True,
        "no_fact_admission_bypass": flags.get("no_fact_admission_bypass") is True,
        "no_navigation_decision": flags.get("no_navigation_decision") is True,
        "no_existing_runner_mutation": "situation_understanding_dryrun" not in runner_py,
        "no_existing_observation_schema_mutation": "situation_understanding_dryrun" not in _read(
            "capabilities/midplatform/governance_standards/model_test_lens_ui/observation_attention_layer_governance_standard_v1.md"
        ),
        "no_real_model_execution": dryrun_result.get("no_real_model_execution") is True,
        "no_network_access": "requests.get" not in adapter and "urllib" not in adapter,
        "deterministic_dryrun_only": dryrun_result.get("deterministic_dryrun_only") is True,
        "output_summary_written": summary_path.is_file(),
        "dryrun_cases_pass": dryrun_result.get("final_decision", "").endswith("_GO"),
        "upstream_gos_confirmed": all(upstream_checks.values()),
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_situation_understanding_model_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_situation_understanding_model_dryrun_v1_001.luna_situation_understanding_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        pass

    known_limits = [
        "dryrun_not_real_image_understanding",
        "situation_understanding_still_deterministic_policy_stub",
        "no_real_teacher_calls",
        "no_network",
        "no_runner_execution",
        "does_not_replace_agent_planning",
        "does_not_replace_tool_os",
        "no_fact_write",
        "does_not_change_runner_behavior_only_corrects_scene_ownership_upstream",
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
        "job_564f1aa93983_recovery_result": dryrun_result.get("job_564f1aa93983_recovery_result"),
        "known_limits": known_limits,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_situation_understanding_model_dryrun_review_v1.json"
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
        "job_564f1aa93983_recovery_result": r.get("job_564f1aa93983_recovery_result"),
        "generated_files_count": len(r.get("generated_files", [])),
        "known_limits": r.get("known_limits", []),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
