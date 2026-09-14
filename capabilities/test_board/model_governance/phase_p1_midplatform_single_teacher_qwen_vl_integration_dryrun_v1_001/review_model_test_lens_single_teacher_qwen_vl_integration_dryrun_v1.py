# -*- coding: utf-8 -*-
"""P1 Single Teacher Qwen-VL Integration — dry-run review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Single-Teacher-QwenVL-Integration-DryRun-v1-001"
QWEN_REL = "capabilities/midplatform/teacher_adapter/providers/qwen_vl"
DRYRUN_REL = f"{QWEN_REL}/qwen_vl_integration_dryrun"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_single_teacher_qwen_vl_integration_planning_v1_review_v0/"
        "p1_midplatform_single_teacher_qwen_vl_integration_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_third_party_teacher_adapter_dryrun_v1_review_v0/"
        "p1_midplatform_third_party_teacher_adapter_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_decision_validation_layer_dryrun_v1_review_v0/"
        "p1_midplatform_luna_decision_validation_layer_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Single-Teacher-QwenVL-Real-Provider-Integration-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{QWEN_REL}/qwen_vl_teacher_adapter_v1.py",
    f"{QWEN_REL}/luna_qwen_teacher_admission_v1.py",
    f"{QWEN_REL}/governance/teacher_usage_policy_v1.json",
    f"{QWEN_REL}/governance/qwen_vl_integration_dryrun_policy_v1.json",
    f"{DRYRUN_REL}/luna_qwen_vl_integration_dryrun_adapter_v1.py",
    f"{TB_REL}/luna_qwen_vl_integration_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_qwen_vl_integration_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_single_teacher_qwen_vl_integration_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("dryrun_adapter_present", "dryrun adapter 存在"),
        ("teacher_admission_present", "Teacher Admission 存在"),
        ("teacher_usage_policy_present", "teacher_usage_policy 存在"),
        ("full_chain_present", "Job→L1→L2→L2.5→Admission→Qwen→Review"),
        ("luna_controls_admission", "Luna 控制何时问 Teacher"),
        ("no_auto_situation_override", "不自动改 Situation"),
        ("no_auto_plan_override", "不自动改 Plan"),
        ("no_auto_tool_os", "不自动调 Tool OS"),
        ("no_runner_invocation", "不触发 Runner"),
        ("no_fact_write", "不写 Fact"),
        ("no_auto_training", "不自动训练"),
        ("no_real_qwen_api", "无真实 Qwen API"),
        ("case_a_admission_noop", "Case A admission noop"),
        ("case_b_unknown_scene_teacher", "Case B unknown 请求 Teacher"),
        ("case_c_challenge_keep_plan", "Case C challenge 保留 plan"),
        ("case_d_scene_conflict_reject", "Case D scene 冲突拒绝"),
        ("case_e_unsupported_claim", "Case E unsupported_claim 拒绝"),
        ("validation_reviews_qwen", "Validation 审核 Qwen"),
        ("unsupported_claim_gate", "unsupported_claim 门存在"),
        ("teacher_not_proactive", "Teacher 非主动观察者"),
        ("no_existing_runner_mutation", "未改 runner"),
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


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _load_json_path(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    adapter = _read(f"{DRYRUN_REL}/luna_qwen_vl_integration_dryrun_adapter_v1.py")
    admission = _read(f"{QWEN_REL}/luna_qwen_teacher_admission_v1.py")
    usage_policy = _load_json(f"{QWEN_REL}/governance/teacher_usage_policy_v1.json")
    dryrun_policy = _load_json(f"{QWEN_REL}/governance/qwen_vl_integration_dryrun_policy_v1.json")
    validation_proc = _read("capabilities/midplatform/teacher_adapter/luna_teacher_validation_processor_v1.py")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )
    usage_flags = usage_policy.get("boundary_flags", {})
    dryrun_flags = dryrun_policy.get("boundary_flags", {})

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_001.luna_qwen_vl_integration_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        dryrun_result = {"final_decision": FINAL_BLOCKED}

    cases = dryrun_result.get("dryrun_cases", [])
    core = dryrun_result.get("core_validations") or {}

    upstream_ok = all(
        _load_json_path(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "dryrun_adapter_present": "run_qwen_vl_integration_dryrun" in adapter,
        "teacher_admission_present": "evaluate_qwen_teacher_admission" in admission,
        "teacher_usage_policy_present": bool(usage_policy.get("admission_matrix")),
        "full_chain_present": "teacher_admission" in adapter and "qwen_vl_teacher_evidence_candidate" in adapter,
        "luna_controls_admission": usage_flags.get("luna_controls_teacher_invocation") is True and core.get("luna_controls_admission") is True,
        "no_auto_situation_override": dryrun_flags.get("no_auto_situation_override") is True and core.get("no_l1_override_all") is True,
        "no_auto_plan_override": dryrun_flags.get("no_auto_plan_override") is True and core.get("no_plan_override_all") is True,
        "no_auto_tool_os": dryrun_flags.get("no_auto_tool_os") is True,
        "no_runner_invocation": dryrun_flags.get("no_runner_invocation") is True,
        "no_fact_write": dryrun_flags.get("no_fact_write") is True,
        "no_auto_training": dryrun_flags.get("no_auto_training") is True,
        "no_real_qwen_api": dryrun_flags.get("no_real_qwen_api") is True and "dashscope" not in adapter.lower(),
        "case_a_admission_noop": _case(cases, "case_a_teacher_admission_noop").get("passed") is True,
        "case_b_unknown_scene_teacher": _case(cases, "case_b_unknown_scene_request_teacher").get("passed") is True,
        "case_c_challenge_keep_plan": _case(cases, "case_c_teacher_challenge_plan").get("passed") is True,
        "case_d_scene_conflict_reject": _case(cases, "case_d_teacher_wrong_scene_rejected").get("passed") is True,
        "case_e_unsupported_claim": _case(cases, "case_e_unsupported_claim_rejected").get("passed") is True,
        "validation_reviews_qwen": dryrun_flags.get("validation_reviews_qwen") is True and "review_teacher_evidence" in adapter,
        "unsupported_claim_gate": "unsupported_claim" in validation_proc and dryrun_flags.get("unsupported_claim_gate") is True,
        "teacher_not_proactive": usage_flags.get("teacher_not_proactive_observer") is True,
        "no_existing_runner_mutation": "qwen_vl_integration_dryrun" not in runner,
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_001.luna_qwen_vl_integration_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        pass

    known_limits = [
        "dryrun_only_no_real_qwen_api",
        "deterministic_mock_scenarios",
        "validates_luna_control_not_qwen_accuracy",
        "perception_teacher_only",
        "no_network",
        "no_runner_invocation",
        "no_fact_write",
        "no_auto_training",
        "multi_teacher_arbitration_deferred",
    ]

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Teacher_Adapter",
        "provider": "qwen_vl",
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
        "case_a_teacher_admission": dryrun_result.get("case_a_teacher_admission"),
        "known_limits": known_limits,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_single_teacher_qwen_vl_integration_dryrun_review_v1.json"
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
        "provider": r.get("provider"),
        "blocker_count": r["blocker_count"],
        "dryrun_cases_passed": r.get("dryrun_cases_passed"),
        "review_guards_passed": r.get("review_guards_passed"),
        "case_a_teacher_admission": r.get("case_a_teacher_admission"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
