# -*- coding: utf-8
"""P1 Third-Party Teacher Adapter — dry-run review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Third-Party-Teacher-Adapter-DryRun-v1-001"
TA_REL = "capabilities/midplatform/teacher_adapter"
DRYRUN_REL = f"{TA_REL}/teacher_adapter_dryrun"
GOV_REL = f"{TA_REL}/governance"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_third_party_teacher_adapter_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_third_party_teacher_adapter_planning_v1_review_v0/"
        "p1_midplatform_third_party_teacher_adapter_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_decision_validation_layer_dryrun_v1_review_v0/"
        "p1_midplatform_luna_decision_validation_layer_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_decision_validation_layer_planning_v1_review_v0/"
        "p1_midplatform_luna_decision_validation_layer_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Single-Teacher-Integration-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DRYRUN_REL}/luna_teacher_adapter_dryrun_adapter_v1.py",
    f"{DRYRUN_REL}/luna_teacher_challenge_builder_v1.py",
    f"{TA_REL}/luna_teacher_validation_processor_v1.py",
    f"{TA_REL}/luna_teacher_adapter_processor_v1.py",
    f"{GOV_REL}/luna_teacher_adapter_dryrun_policy_v1.json",
    f"{GOV_REL}/luna_teacher_adapter_policy_v1.json",
    f"{TA_REL}/schemas/teacher_validation_review_schema_v1.json",
    f"{TB_REL}/luna_teacher_adapter_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_teacher_adapter_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_third_party_teacher_adapter_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("dryrun_adapter_present", "dryrun adapter 存在"),
        ("teacher_validation_processor_present", "teacher validation processor 存在"),
        ("challenge_builder_present", "challenge builder 存在"),
        ("dryrun_policy_present", "dryrun policy 存在"),
        ("full_chain_present", "L1→L2→L2.5→Teacher→Review 链路"),
        ("teacher_after_validation", "Teacher 在 validation 之后"),
        ("no_selected_plan_override", "不覆盖 selected plan"),
        ("no_l1_scene_override", "不覆盖 L1 scene"),
        ("no_tool_execution", "不执行工具"),
        ("no_fact_write", "不写 fact"),
        ("no_direct_training", "不直接训练"),
        ("no_real_api", "无真实 API"),
        ("case_a_teacher_supports_ocr", "Case A 支持 OCR"),
        ("case_b_slam_rejected", "Case B SLAM 拒绝"),
        ("case_c_alternative_keep_plan", "Case C alternative 保留 plan"),
        ("case_d_wrong_scene_rejected", "Case D 错误场景拒绝"),
        ("case_e_learning_no_training", "Case E learning 不训练"),
        ("job_564f1aa93983_fixture", "店招 job fixture"),
        ("teacher_evidence_not_answer", "evidence 非 answer"),
        ("validation_reviews_teacher", "validation 审核 teacher"),
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


def _load_json(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    adapter = _read(f"{DRYRUN_REL}/luna_teacher_adapter_dryrun_adapter_v1.py")
    validation_proc = _read(f"{TA_REL}/luna_teacher_validation_processor_v1.py")
    builder = _read(f"{DRYRUN_REL}/luna_teacher_challenge_builder_v1.py")
    policy = _load_json(_detect_repo_root() / f"{GOV_REL}/luna_teacher_adapter_dryrun_policy_v1.json")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )
    flags = policy.get("boundary_flags", {})

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_third_party_teacher_adapter_dryrun_v1_001.luna_teacher_adapter_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        dryrun_result = {"final_decision": FINAL_BLOCKED}

    cases = dryrun_result.get("dryrun_cases", [])
    core = dryrun_result.get("core_validations") or {}
    job = dryrun_result.get("job_564f1aa93983_teacher_result") or {}

    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "dryrun_adapter_present": "run_teacher_adapter_dryrun" in adapter,
        "teacher_validation_processor_present": "review_teacher_evidence" in validation_proc,
        "challenge_builder_present": "build_teacher_challenge_from_fixture" in builder,
        "dryrun_policy_present": bool(policy.get("boundary_flags")),
        "full_chain_present": "teacher_validation_review" in adapter and "decision_validation_candidate" in adapter,
        "teacher_after_validation": flags.get("teacher_after_validation") is True and "run_decision_validation_dryrun" in adapter,
        "no_selected_plan_override": flags.get("no_selected_plan_override") is True and core.get("no_plan_override_all") is True,
        "no_l1_scene_override": flags.get("no_l1_scene_override") is True and core.get("no_l1_override_all") is True,
        "no_tool_execution": flags.get("no_tool_execution") is True,
        "no_fact_write": flags.get("no_fact_write") is True,
        "no_direct_training": flags.get("no_direct_training") is True,
        "no_real_api": flags.get("no_real_api_in_dryrun") is True and "requests." not in adapter,
        "case_a_teacher_supports_ocr": _case(cases, "case_a_teacher_supports_ocr_plan").get("passed") is True,
        "case_b_slam_rejected": _case(cases, "case_b_teacher_slam_rejected").get("passed") is True,
        "case_c_alternative_keep_plan": _case(cases, "case_c_teacher_alternative_keep_plan").get("passed") is True,
        "case_d_wrong_scene_rejected": _case(cases, "case_d_teacher_wrong_scene_rejected").get("passed") is True,
        "case_e_learning_no_training": _case(cases, "case_e_learning_case_no_training").get("passed") is True,
        "job_564f1aa93983_fixture": job.get("job_id") == "job_564f1aa93983",
        "teacher_evidence_not_answer": "teacher_answer" not in adapter and "teacher_evidence_candidate" in adapter,
        "validation_reviews_teacher": flags.get("validation_reviews_teacher") is True,
        "no_existing_runner_mutation": "teacher_adapter_dryrun" not in runner,
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_third_party_teacher_adapter_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_third_party_teacher_adapter_dryrun_v1_001.luna_teacher_adapter_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        pass

    known_limits = [
        "dryrun_only_no_real_gemini_qwen_gpt_api",
        "teacher_stub_fixture_only",
        "no_network",
        "no_runner_invocation",
        "no_fact_write",
        "no_tool_execution",
        "teacher_does_not_override_selected_plan",
        "teacher_does_not_override_l1_scene",
        "multi_teacher_arbitration_deferred",
    ]

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Teacher_Adapter",
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
        "job_564f1aa93983_teacher_result": dryrun_result.get("job_564f1aa93983_teacher_result"),
        "known_limits": known_limits,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_third_party_teacher_adapter_dryrun_review_v1.json"
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
        "job_564f1aa93983_teacher_result": r.get("job_564f1aa93983_teacher_result"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
